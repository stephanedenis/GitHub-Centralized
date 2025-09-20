#!/bin/bash
# Script de vérification de santé globale
# Vérifie l'état de tous les submodules sans les modifier

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
LOG_FILE="$HOME/.github-centralized-health.log"

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log() {
    local msg="$1"
    echo -e "${BLUE}[HEALTH]${NC} $msg"
    echo "$(date '+%Y-%m-%d %H:%M:%S') - HEALTH - $msg" >> "$LOG_FILE"
}

success() {
    local msg="$1"
    echo -e "${GREEN}[OK]${NC} $msg"
    echo "$(date '+%Y-%m-%d %H:%M:%S') - OK - $msg" >> "$LOG_FILE"
}

warning() {
    local msg="$1"
    echo -e "${YELLOW}[WARNING]${NC} $msg"
    echo "$(date '+%Y-%m-%d %H:%M:%S') - WARNING - $msg" >> "$LOG_FILE"
}

error() {
    local msg="$1"
    echo -e "${RED}[ERROR]${NC} $msg"
    echo "$(date '+%Y-%m-%d %H:%M:%S') - ERROR - $msg" >> "$LOG_FILE"
}

# Fonction pour charger la liste d'exclusions
load_exclusions() {
    local exclusions_file="$SCRIPT_DIR/exclusions.conf"
    EXCLUDED_REPOS=()
    
    if [ -f "$exclusions_file" ]; then
        while IFS= read -r line; do
            # Ignorer les commentaires et lignes vides
            if [[ ! "$line" =~ ^[[:space:]]*# ]] && [[ -n "${line// }" ]]; then
                # Extraire la partie avant le commentaire
                local repo=$(echo "$line" | cut -d'#' -f1 | xargs)
                if [ -n "$repo" ]; then
                    EXCLUDED_REPOS+=("$repo")
                fi
            fi
        done < "$exclusions_file"
        
        if [ ${#EXCLUDED_REPOS[@]} -gt 0 ]; then
            log "Exclusions configurées: ${EXCLUDED_REPOS[*]}"
        fi
    fi
}

# Fonction pour vérifier si un repository est exclu
is_repo_excluded() {
    local repo_path="$1"
    local family_name=$(basename "$(dirname "$repo_path")")
    local repo_name=$(basename "$repo_path")
    local full_path="$family_name/$repo_name"
    
    for excluded in "${EXCLUDED_REPOS[@]}"; do
        if [ "$excluded" = "$repo_name" ] || [ "$excluded" = "$full_path" ]; then
            return 0  # Exclu
        fi
    done
    
    return 1  # Pas exclu
}

# Fonction pour détecter si un repository est en cours d'utilisation
is_repo_busy() {
    local repo_path="$1"
    local repo_name=$(basename "$repo_path")
    
    # D'abord vérifier les exclusions manuelles (prioritaire)
    if is_repo_excluded "$repo_path"; then
        return 0  # Traiter comme occupé
    fi
    
    # Vérifier les fichiers de lock Git (seule détection fiable)
    if [ -f "$repo_path/.git/index.lock" ]; then
        return 0  # Busy
    fi
    
    return 1  # Not busy
}

# Fonction pour vérifier la santé d'un submodule
check_submodule_health() {
    local submodule_path="$1"
    local submodule_name=$(basename "$submodule_path")
    
    if [ ! -d "$submodule_path" ]; then
        error "❌ $submodule_name: Dossier manquant"
        return 1
    fi
    
    # Vérifier si le repo est exclu ou en cours d'utilisation
    if is_repo_busy "$submodule_path"; then
        if is_repo_excluded "$submodule_path"; then
            warning "� $submodule_name: Exclu par configuration - analyse limitée"
        else
            warning "🔒 $submodule_name: Git lock détecté - analyse limitée"
        fi
        return 0
    fi
    
    cd "$submodule_path"
    
    # Vérifier si c'est un repo git
    if [ ! -d ".git" ]; then
        error "❌ $submodule_name: Pas un repository git"
        return 1
    fi
    
    # Vérification basique sans fetch (pour éviter les conflits)
    local current_branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "detached")
    
    # Vérifier les modifications non commitées
    local has_changes="false"
    if ! git diff-index --quiet HEAD -- 2>/dev/null; then
        has_changes="true"
    fi
    
    # Vérifier les fichiers non trackés
    local has_untracked="false"
    if [ -n "$(git ls-files --others --exclude-standard)" ]; then
        has_untracked="true"
    fi
    
    # Afficher le statut
    local status_msg="✅ $submodule_name: "
    if [ "$current_branch" = "detached" ]; then
        status_msg+="(HEAD détachée) "
    else
        status_msg+="($current_branch) "
    fi
    
    if [ "$has_changes" = "true" ]; then
        status_msg+="📝 modifs "
    fi
    
    if [ "$has_untracked" = "true" ]; then
        status_msg+="📄 nouveaux fichiers "
    fi
    
    if [ "$has_changes" = "false" ] && [ "$has_untracked" = "false" ]; then
        status_msg+="propre"
        success "$status_msg"
    else
        warning "$status_msg"
    fi
    
    return 0
}

# Fonction pour vérifier une famille de projets
check_family_health() {
    local family_path="$1"
    local family_name=$(basename "$family_path")
    
    if [ ! -d "$family_path" ]; then
        error "Famille $family_name non trouvée: $family_path"
        return
    fi
    
    log "=== Vérification famille $family_name ==="
    
    local total=0
    local ok_count=0
    local busy_count=0
    
    for submodule in "$family_path"/*; do
        if [ -d "$submodule" ]; then
            total=$((total + 1))
            if is_repo_busy "$submodule"; then
                busy_count=$((busy_count + 1))
                warning "🔒 $(basename "$submodule"): En cours d'utilisation"
            elif check_submodule_health "$submodule"; then
                ok_count=$((ok_count + 1))
            fi
        fi
    done
    
    local checked=$((total - busy_count))
    if [ $checked -eq $ok_count ]; then
        success "Famille $family_name: $ok_count/$checked OK ($busy_count occupés)"
    else
        warning "Famille $family_name: $ok_count/$checked OK ($busy_count occupés)"
    fi
    
    cd "$REPO_ROOT"
}

# Fonction pour générer un rapport de santé complet
generate_health_report() {
    local report_file="$REPO_ROOT/management/health_report_$(date +%Y%m%d_%H%M%S).md"
    
    log "Génération rapport de santé: $report_file"
    
    cat > "$report_file" << EOF
# 🏥 Rapport de Santé GitHub Centralized

**Date:** $(date '+%Y-%m-%d %H:%M:%S')  
**Généré par:** health-check.sh

## 📊 Résumé Global

EOF

    # Statistiques par famille
    for family_dir in "$REPO_ROOT/projects"/*; do
        if [ -d "$family_dir" ]; then
            local family_name=$(basename "$family_dir")
            local total=$(find "$family_dir" -maxdepth 1 -type d | wc -l)
            total=$((total - 1))  # Exclure le dossier parent
            
            local busy=0
            for submodule in "$family_dir"/*; do
                if [ -d "$submodule" ] && is_repo_busy "$submodule"; then
                    busy=$((busy + 1))
                fi
            done
            
            echo "- **$family_name**: $total repositories ($busy en cours d'utilisation)" >> "$report_file"
        fi
    done
    
    echo "" >> "$report_file"
    echo "## 🔍 Détails par Famille" >> "$report_file"
    echo "" >> "$report_file"
    
    # Détails par famille
    for family_dir in "$REPO_ROOT/projects"/*; do
        if [ -d "$family_dir" ]; then
            local family_name=$(basename "$family_dir")
            echo "### $family_name" >> "$report_file"
            echo "" >> "$report_file"
            
            for submodule in "$family_dir"/*; do
                if [ -d "$submodule" ]; then
                    local submodule_name=$(basename "$submodule")
                    if is_repo_busy "$submodule"; then
                        echo "- 🔒 **$submodule_name** - En cours d'utilisation" >> "$report_file"
                    else
                        echo "- ✅ **$submodule_name** - Disponible" >> "$report_file"
                    fi
                fi
            done
            echo "" >> "$report_file"
        fi
    done
    
    echo "## 📝 Recommandations" >> "$report_file"
    echo "" >> "$report_file"
    echo "- Éviter la synchronisation des repositories marqués 🔒" >> "$report_file"
    echo "- Utiliser \`./management/sync-all.sh --safe\` pour synchronisation intelligente" >> "$report_file"
    echo "- Vérifier les logs: $LOG_FILE" >> "$report_file"
    
    success "Rapport de santé généré: $report_file"
}

# Fonction principale
main() {
    local action="$1"
    
    log "=== Vérification Santé GitHub Centralized ==="
    
    # Charger les exclusions
    load_exclusions
    
    cd "$REPO_ROOT"
    
    # Vérifier que nous sommes dans le bon repository
    if [ ! -f "README.md" ] || ! grep -q "GitHub Centralized" README.md; then
        error "Ce script doit être exécuté depuis GitHub-Centralized"
        exit 1
    fi
    
    case "$action" in
        "quick"|"")
            # Vérification rapide
            log "Vérification rapide de la santé..."
            for family_dir in projects/*; do
                if [ -d "$family_dir" ]; then
                    check_family_health "$family_dir"
                fi
            done
            ;;
        "full")
            # Vérification complète avec rapport
            for family_dir in projects/*; do
                if [ -d "$family_dir" ]; then
                    check_family_health "$family_dir"
                fi
            done
            generate_health_report
            ;;
        "busy")
            # Liste seulement les repos occupés/exclus
            log "Repositories protégés (exclusions + git locks):"
            for family_dir in projects/*; do
                if [ -d "$family_dir" ]; then
                    for submodule in "$family_dir"/*; do
                        if [ -d "$submodule" ]; then
                            if is_repo_excluded "$submodule"; then
                                warning "🚫 $(basename "$(dirname "$submodule")")/$(basename "$submodule") - Exclu par configuration"
                            elif is_repo_busy "$submodule"; then
                                warning "🔒 $(basename "$(dirname "$submodule")")/$(basename "$submodule") - Git lock"
                            fi
                        fi
                    done
                fi
            done
            ;;
        *)
            echo "Usage: $0 [quick|full|busy]"
            echo ""
            echo "  quick  - Vérification rapide (défaut)"
            echo "  full   - Vérification complète + rapport"
            echo "  busy   - Liste les repos en cours d'utilisation"
            exit 1
            ;;
    esac
    
    success "Vérification terminée - Logs: $LOG_FILE"
}

main "$@"