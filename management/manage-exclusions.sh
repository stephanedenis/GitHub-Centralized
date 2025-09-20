#!/bin/bash
# Gestionnaire d'exclusions pour la synchronisation
# Permet d'ajouter/supprimer des repositories de la liste d'exclusions

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EXCLUSIONS_FILE="$SCRIPT_DIR/exclusions.conf"

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log() {
    echo -e "${BLUE}[EXCLUSIONS]${NC} $1"
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Fonction pour lister les exclusions actuelles
list_exclusions() {
    log "Exclusions configurées:"
    
    if [ ! -f "$EXCLUSIONS_FILE" ]; then
        warning "Aucun fichier d'exclusions trouvé"
        return
    fi
    
    local found=false
    while IFS= read -r line; do
        # Ignorer les commentaires et lignes vides
        if [[ ! "$line" =~ ^[[:space:]]*# ]] && [[ -n "${line// }" ]]; then
            local repo=$(echo "$line" | cut -d'#' -f1 | xargs)
            local comment=$(echo "$line" | cut -d'#' -f2- | xargs)
            if [ -n "$repo" ]; then
                if [ -n "$comment" ] && [ "$comment" != "$repo" ]; then
                    echo -e "  🚫 ${YELLOW}$repo${NC} - $comment"
                else
                    echo -e "  🚫 ${YELLOW}$repo${NC}"
                fi
                found=true
            fi
        fi
    done < "$EXCLUSIONS_FILE"
    
    if [ "$found" = false ]; then
        warning "Aucune exclusion active"
    fi
}

# Fonction pour ajouter une exclusion
add_exclusion() {
    local repo="$1"
    local reason="$2"
    
    if [ -z "$repo" ]; then
        error "Repository requis"
        return 1
    fi
    
    # Créer le fichier si nécessaire
    if [ ! -f "$EXCLUSIONS_FILE" ]; then
        touch "$EXCLUSIONS_FILE"
    fi
    
    # Vérifier si déjà exclu
    if grep -q "^[[:space:]]*$repo[[:space:]]*" "$EXCLUSIONS_FILE"; then
        warning "Repository $repo déjà exclu"
        return 1
    fi
    
    # Ajouter l'exclusion
    if [ -n "$reason" ]; then
        echo "$repo  # $reason" >> "$EXCLUSIONS_FILE"
        success "Ajouté: $repo - $reason"
    else
        echo "$repo" >> "$EXCLUSIONS_FILE"
        success "Ajouté: $repo"
    fi
}

# Fonction pour supprimer une exclusion
remove_exclusion() {
    local repo="$1"
    
    if [ -z "$repo" ]; then
        error "Repository requis"
        return 1
    fi
    
    if [ ! -f "$EXCLUSIONS_FILE" ]; then
        error "Aucun fichier d'exclusions trouvé"
        return 1
    fi
    
    # Supprimer l'exclusion
    if grep -q "^[[:space:]]*$repo[[:space:]]*" "$EXCLUSIONS_FILE"; then
        sed -i "/^[[:space:]]*$repo[[:space:]]*/d" "$EXCLUSIONS_FILE"
        success "Supprimé: $repo"
    else
        warning "Repository $repo non trouvé dans les exclusions"
        return 1
    fi
}

# Fonction pour ajouter une exclusion temporaire (avec timestamp)
add_temp_exclusion() {
    local repo="$1"
    local duration="$2"
    local reason="$3"
    
    if [ -z "$duration" ]; then
        duration="1h"
    fi
    
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    local temp_reason="Temporaire ($duration) - $timestamp"
    if [ -n "$reason" ]; then
        temp_reason="$temp_reason - $reason"
    fi
    
    add_exclusion "$repo" "$temp_reason"
}

# Fonction principale
main() {
    local action="$1"
    shift || true
    
    case "$action" in
        "list"|"ls"|"")
            list_exclusions
            ;;
        "add")
            local repo="$1"
            local reason="$2"
            add_exclusion "$repo" "$reason"
            ;;
        "remove"|"rm")
            local repo="$1"
            remove_exclusion "$repo"
            ;;
        "temp")
            local repo="$1"
            local duration="$2"
            local reason="$3"
            add_temp_exclusion "$repo" "$duration" "$reason"
            ;;
        "edit")
            if command -v nano >/dev/null 2>&1; then
                nano "$EXCLUSIONS_FILE"
            elif command -v vim >/dev/null 2>&1; then
                vim "$EXCLUSIONS_FILE"
            else
                echo "Éditez manuellement: $EXCLUSIONS_FILE"
            fi
            ;;
        "clear")
            if [ -f "$EXCLUSIONS_FILE" ]; then
                > "$EXCLUSIONS_FILE"
                success "Toutes les exclusions supprimées"
            else
                warning "Aucun fichier d'exclusions à effacer"
            fi
            ;;
        *)
            echo "Gestionnaire d'exclusions GitHub Centralized"
            echo ""
            echo "Usage: $0 [action] [arguments]"
            echo ""
            echo "Actions:"
            echo "  list               - Liste les exclusions actuelles (défaut)"
            echo "  add REPO [RAISON]  - Ajoute une exclusion"
            echo "  remove REPO        - Supprime une exclusion"
            echo "  temp REPO [DURÉE] [RAISON] - Ajoute une exclusion temporaire"
            echo "  edit               - Édite le fichier d'exclusions"
            echo "  clear              - Supprime toutes les exclusions"
            echo ""
            echo "Exemples:"
            echo "  $0 add panini/PaniniFS-Research 'Travail en cours'"
            echo "  $0 temp PaniniFS-Research 2h 'Debugging'"
            echo "  $0 remove PaniniFS-Research"
            echo ""
            echo "Format repository:"
            echo "  - Nom simple: PaniniFS-Research"
            echo "  - Chemin complet: panini/PaniniFS-Research"
            exit 1
            ;;
    esac
}

main "$@"