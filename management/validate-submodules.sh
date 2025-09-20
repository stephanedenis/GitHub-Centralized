#!/bin/bash
# Script de validation et réparation des submodules
# Répare les submodules défaillants et valide la configuration

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log() {
    echo -e "${BLUE}[VALIDATE]${NC} $1"
}

success() {
    echo -e "${GREEN}[OK]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Fonction pour valider et réparer un submodule
validate_submodule() {
    local submodule_path="$1"
    local submodule_name=$(basename "$submodule_path")
    
    if [ ! -d "$submodule_path" ]; then
        error "❌ $submodule_name: Dossier manquant"
        return 1
    fi
    
    cd "$submodule_path"
    
    # Vérifier si c'est un repo git
    if [ ! -d ".git" ] && [ ! -f ".git" ]; then
        error "❌ $submodule_name: Pas un repository git"
        
        # Tenter une réparation
        cd "$REPO_ROOT"
        warning "🔧 Tentative de réparation de $submodule_name..."
        if git submodule update --init "$submodule_path"; then
            success "✅ $submodule_name: Réparé avec succès"
            return 0
        else
            error "❌ $submodule_name: Échec de réparation"
            return 1
        fi
    fi
    
    # Vérifier l'état git
    if [ -f ".git" ]; then
        # Submodule avec gitdir
        local gitdir=$(cat .git | sed 's/gitdir: //')
        if [ ! -d "$gitdir" ]; then
            warning "⚠️  $submodule_name: gitdir manquant, tentative de réparation..."
            cd "$REPO_ROOT"
            git submodule update --init "$submodule_path"
            return $?
        fi
    fi
    
    # Vérifier si on peut accéder au repository
    if ! git status >/dev/null 2>&1; then
        warning "⚠️  $submodule_name: État git corrompu, tentative de réparation..."
        cd "$REPO_ROOT"
        git submodule update --init "$submodule_path"
        return $?
    fi
    
    success "✅ $submodule_name: Valide"
    return 0
}

# Fonction pour valider une famille
validate_family() {
    local family_path="$1"
    local family_name=$(basename "$family_path")
    
    if [ ! -d "$family_path" ]; then
        error "Famille $family_name non trouvée: $family_path"
        return
    fi
    
    log "=== Validation famille $family_name ==="
    
    local total=0
    local valid_count=0
    local repaired_count=0
    
    for submodule in "$family_path"/*; do
        if [ -d "$submodule" ]; then
            total=$((total + 1))
            if validate_submodule "$submodule"; then
                valid_count=$((valid_count + 1))
            fi
        fi
    done
    
    if [ $total -eq $valid_count ]; then
        success "Famille $family_name: $valid_count/$total submodules valides"
    else
        warning "Famille $family_name: $valid_count/$total submodules valides"
    fi
    
    cd "$REPO_ROOT"
}

# Fonction pour nettoyer les submodules orphelins
cleanup_orphans() {
    log "Nettoyage des submodules orphelins..."
    
    # Vérifier .gitmodules
    if [ -f ".gitmodules" ]; then
        # Extraire les chemins des submodules déclarés
        local declared_paths=($(git config --file .gitmodules --get-regexp path | awk '{print $2}'))
        
        for declared_path in "${declared_paths[@]}"; do
            if [ ! -d "$declared_path" ]; then
                warning "Submodule déclaré mais absent: $declared_path"
                
                # Tenter de l'initialiser
                if git submodule update --init "$declared_path"; then
                    success "Submodule $declared_path restauré"
                else
                    error "Impossible de restaurer $declared_path"
                fi
            fi
        done
    fi
    
    # Nettoyer les dossiers .git/modules orphelins
    if [ -d ".git/modules" ]; then
        find .git/modules -type d -name "projects" -exec find {} -mindepth 2 -maxdepth 2 -type d \; | while read module_dir; do
            local relative_path=$(echo "$module_dir" | sed 's|.git/modules/||')
            if [ ! -d "$relative_path" ]; then
                warning "Module git orphelin: $module_dir"
                # On ne supprime pas automatiquement pour la sécurité
            fi
        done
    fi
}

# Fonction principale
main() {
    local action="$1"
    
    log "=== Validation GitHub Centralized ==="
    
    cd "$REPO_ROOT"
    
    # Vérifier que nous sommes dans le bon repository
    if [ ! -f "README.md" ] || ! grep -q "GitHub Centralized" README.md; then
        error "Ce script doit être exécuté depuis GitHub-Centralized"
        exit 1
    fi
    
    case "$action" in
        "check"|"")
            # Validation de tous les submodules
            for family_dir in projects/*; do
                if [ -d "$family_dir" ]; then
                    validate_family "$family_dir"
                fi
            done
            ;;
        "repair")
            # Validation + réparation automatique
            for family_dir in projects/*; do
                if [ -d "$family_dir" ]; then
                    validate_family "$family_dir"
                fi
            done
            cleanup_orphans
            ;;
        "clean")
            cleanup_orphans
            ;;
        *)
            echo "Usage: $0 [check|repair|clean]"
            echo ""
            echo "  check  - Valide tous les submodules (défaut)"
            echo "  repair - Valide et répare les submodules défaillants"
            echo "  clean  - Nettoie les submodules orphelins"
            exit 1
            ;;
    esac
    
    success "Validation terminée"
}

main "$@"