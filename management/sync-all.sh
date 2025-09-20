#!/bin/bash
# Script de synchronisation globale de tous les submodules
# Gère la synchronisation, mise à jour et santé de tous les repositories

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
LOG_FILE="$HOME/.github-centralized-sync.log"

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log() {
    local msg="$1"
    echo -e "${BLUE}[SYNC]${NC} $msg"
    echo "$(date '+%Y-%m-%d %H:%M:%S') - SYNC - $msg" >> "$LOG_FILE"
}

success() {
    local msg="$1"
    echo -e "${GREEN}[SUCCESS]${NC} $msg"
    echo "$(date '+%Y-%m-%d %H:%M:%S') - SUCCESS - $msg" >> "$LOG_FILE"
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

# Fonction pour synchroniser un submodule
sync_submodule() {
    local submodule_path="$1"
    local submodule_name=$(basename "$submodule_path")
    
    if [ ! -d "$submodule_path" ]; then
        warning "Submodule $submodule_name non trouvé: $submodule_path"
        return 1
    fi
    
    cd "$submodule_path"
    
    log "Synchronisation $submodule_name..."
    
    # Vérifier si c'est un repo git
    if [ ! -d ".git" ]; then
        error "$submodule_name n'est pas un repository git"
        return 1
    fi
    
    # Fetch des dernières modifications
    if ! git fetch origin 2>/dev/null; then
        error "Échec fetch pour $submodule_name"
        return 1
    fi
    
    # Vérifier l'état
    local current_branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "detached")
    local main_branch="main"
    
    # Tenter de détecter la branche principale
    if git show-ref --verify --quiet refs/remotes/origin/master; then
        main_branch="master"
    fi
    
    # Obtenir les informations de synchronisation
    local ahead=0
    local behind=0
    
    if [ "$current_branch" != "detached" ]; then
        ahead=$(git rev-list --count origin/$main_branch..HEAD 2>/dev/null || echo "0")
        behind=$(git rev-list --count HEAD..origin/$main_branch 2>/dev/null || echo "0")
    fi
    
    # Vérifier les modifications non commitées
    local has_changes="false"
    if ! git diff-index --quiet HEAD -- 2>/dev/null; then
        has_changes="true"
    fi
    
    # Afficher le statut
    if [ "$has_changes" = "true" ]; then
        echo -e "  ${YELLOW}📝${NC} Modifications non commitées"
    fi
    
    if [ "$ahead" -gt 0 ] && [ "$behind" -gt 0 ]; then
        echo -e "  ${RED}🔄${NC} Divergé ($ahead en avance, $behind en retard)"
    elif [ "$ahead" -gt 0 ]; then
        echo -e "  ${BLUE}📈${NC} $ahead commits en avance"
    elif [ "$behind" -gt 0 ]; then
        echo -e "  ${YELLOW}📥${NC} $behind commits en retard"
    else
        echo -e "  ${GREEN}✅${NC} À jour"
    fi
    
    return 0
}

# Fonction pour synchroniser une famille de projets
sync_family() {
    local family_path="$1"
    local family_name=$(basename "$family_path")
    
    if [ ! -d "$family_path" ]; then
        warning "Famille $family_name non trouvée: $family_path"
        return
    fi
    
    log "=== Synchronisation famille $family_name ==="
    
    local total=0
    local success_count=0
    
    for submodule in "$family_path"/*; do
        if [ -d "$submodule" ]; then
            total=$((total + 1))
            if sync_submodule "$submodule"; then
                success_count=$((success_count + 1))
            fi
        fi
    done
    
    if [ $total -eq $success_count ]; then
        success "Famille $family_name: $success_count/$total submodules synchronisés"
    else
        warning "Famille $family_name: $success_count/$total submodules synchronisés"
    fi
    
    cd "$REPO_ROOT"
}

# Fonction pour mettre à jour les submodules vers les derniers commits
update_submodules() {
    log "Mise à jour des submodules vers les derniers commits..."
    
    cd "$REPO_ROOT"
    
    if git submodule update --remote --merge; then
        success "Submodules mis à jour"
    else
        warning "Certains submodules n'ont pas pu être mis à jour"
    fi
}

# Fonction pour générer un rapport de santé
generate_health_report() {
    local report_file="$REPO_ROOT/management/health_report_$(date +%Y%m%d_%H%M%S).md"
    
    log "Génération rapport de santé: $report_file"
    
    cat > "$report_file" << EOF
# Rapport de Santé GitHub Centralized
**Date:** $(date '+%Y-%m-%d %H:%M:%S')
**Généré par:** sync-all.sh

## Résumé Global

EOF

    # Compter les submodules par famille
    for family_dir in "$REPO_ROOT/projects"/*; do
        if [ -d "$family_dir" ]; then
            local family_name=$(basename "$family_dir")
            local count=$(find "$family_dir" -maxdepth 1 -type d | wc -l)
            count=$((count - 1))  # Exclure le dossier parent
            echo "- **$family_name**: $count repositories" >> "$report_file"
        fi
    done
    
    echo "" >> "$report_file"
    echo "## Détails par Famille" >> "$report_file"
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
                    echo "- $submodule_name" >> "$report_file"
                fi
            done
            echo "" >> "$report_file"
        fi
    done
    
    success "Rapport de santé généré: $report_file"
}

# Fonction principale
main() {
    local action="$1"
    
    log "=== Synchronisation Globale GitHub Centralized ==="
    
    cd "$REPO_ROOT"
    
    # Vérifier que nous sommes dans le bon repository
    if [ ! -f "README.md" ] || ! grep -q "GitHub Centralized" README.md; then
        error "Ce script doit être exécuté depuis GitHub-Centralized"
        exit 1
    fi
    
    case "$action" in
        "status"|"")
            # Synchroniser toutes les familles
            for family_dir in projects/*; do
                if [ -d "$family_dir" ]; then
                    sync_family "$family_dir"
                fi
            done
            ;;
        "update")
            update_submodules
            ;;
        "report")
            generate_health_report
            ;;
        "full")
            # Synchronisation complète
            for family_dir in projects/*; do
                if [ -d "$family_dir" ]; then
                    sync_family "$family_dir"
                fi
            done
            update_submodules
            generate_health_report
            ;;
        *)
            echo "Usage: $0 [status|update|report|full]"
            echo ""
            echo "  status  - Affiche le statut de tous les submodules (défaut)"
            echo "  update  - Met à jour tous les submodules"
            echo "  report  - Génère un rapport de santé"
            echo "  full    - Synchronisation complète + rapport"
            exit 1
            ;;
    esac
    
    success "Synchronisation terminée - Logs: $LOG_FILE"
}

main "$@"