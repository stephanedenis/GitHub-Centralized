#!/bin/bash
# Script d'initialisation du workspace centralisé
# Initialise tous les submodules et configure l'environnement

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
    echo -e "${BLUE}[INIT]${NC} $1"
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

# Configuration des repositories par famille
declare -A PANINI_REPOS=(
    ["PaniniFS"]="https://github.com/stephanedenis/PaniniFS.git"
    ["PaniniFS-Research"]="https://github.com/stephanedenis/PaniniFS-Research.git"
    ["PaniniFS-CopilotageShared"]="https://github.com/stephanedenis/PaniniFS-CopilotageShared.git"
    ["PaniniFS-AttributionRegistry"]="https://github.com/stephanedenis/PaniniFS-AttributionRegistry.git"
    ["PaniniFS-DatasetsIngestion"]="https://github.com/stephanedenis/PaniniFS-DatasetsIngestion.git"
    ["PaniniFS-ExecutionOrchestrator"]="https://github.com/stephanedenis/PaniniFS-ExecutionOrchestrator.git"
    ["PaniniFS-UltraReactive"]="https://github.com/stephanedenis/PaniniFS-UltraReactive.git"
    ["PaniniFS-PublicationEngine"]="https://github.com/stephanedenis/PaniniFS-PublicationEngine.git"
    ["PaniniFS-SemanticCore"]="https://github.com/stephanedenis/PaniniFS-SemanticCore.git"
    ["PaniniFS-AutonomousMissions"]="https://github.com/stephanedenis/PaniniFS-AutonomousMissions.git"
    ["PaniniFS-CoLabController"]="https://github.com/stephanedenis/PaniniFS-CoLabController.git"
    ["PaniniFS-CloudOrchestrator"]="https://github.com/stephanedenis/PaniniFS-CloudOrchestrator.git"
)

declare -A EQUIPMENT_REPOS=(
    ["equipment-hauru"]="https://github.com/stephanedenis/equipment-hauru.git"
    ["equipment-remarkable"]="https://github.com/stephanedenis/equipment-remarkable.git"
)

declare -A TOOLING_REPOS=(
    ["copilotage"]="https://github.com/stephanedenis/copilotage.git"
    ["copilotage-shared"]="https://github.com/stephanedenis/copilotage-shared.git"
)

declare -A EXPLORATION_REPOS=(
    ["CALME"]="https://github.com/stephanedenis/CALME.git"
    ["OntoWave"]="https://github.com/stephanedenis/OntoWave.git"
)

# Fonction pour ajouter des submodules par famille
add_submodules_family() {
    local family_name="$1"
    local -n repos_ref=$2
    
    log "Configuration famille $family_name..."
    
    for repo_name in "${!repos_ref[@]}"; do
        local repo_url="${repos_ref[$repo_name]}"
        local submodule_path="projects/$family_name/$repo_name"
        
        if [ -d "$submodule_path" ]; then
            warning "Submodule $repo_name déjà existant"
        else
            log "Ajout submodule $repo_name..."
            if git submodule add "$repo_url" "$submodule_path" 2>/dev/null; then
                success "Submodule $repo_name ajouté avec succès"
            else
                error "Échec ajout submodule $repo_name"
            fi
        fi
    done
}

# Fonction principale
main() {
    log "Initialisation du workspace centralisé..."
    
    cd "$REPO_ROOT"
    
    # Vérifier que nous sommes dans un repo git
    if [ ! -d ".git" ]; then
        error "Ce script doit être exécuté dans le repository GitHub-Centralized"
        exit 1
    fi
    
    # Ajouter les submodules par famille
    add_submodules_family "panini" PANINI_REPOS
    add_submodules_family "equipment" EQUIPMENT_REPOS
    add_submodules_family "tooling" TOOLING_REPOS
    add_submodules_family "exploration" EXPLORATION_REPOS
    
    # Initialiser tous les submodules
    log "Initialisation de tous les submodules..."
    if git submodule update --init --recursive; then
        success "Tous les submodules initialisés"
    else
        warning "Certains submodules ont échoué"
    fi
    
    # Créer le commit initial si nécessaire
    if git diff --staged --quiet; then
        log "Aucun changement à committer"
    else
        log "Commit des submodules..."
        git add .gitmodules projects/
        git commit -m "Initial setup: Add all project submodules by family

- PaniniFS family: Système de fichiers génératif
- Equipment family: Infrastructure et matériel  
- Tooling family: Outils de développement
- Exploration family: Projets expérimentaux

Centralizes governance and management of all repositories."
        success "Submodules committés"
    fi
    
    # Vérifier la configuration
    log "Vérification de la configuration..."
    if [ -f "copilotage/README.md" ]; then
        success "Structure copilotage OK"
    else
        warning "Structure copilotage manquante"
    fi
    
    if [ -d "projects/panini" ] && [ -d "projects/equipment" ]; then
        success "Structure projets OK"
    else
        warning "Structure projets incomplète"
    fi
    
    success "Initialisation terminée !"
    echo
    echo "Prochaines étapes :"
    echo "1. ./management/sync-all.sh    - Synchroniser tous les submodules"
    echo "2. python3 copilotage/utilities/agent_onboarding.py --start"
    echo "3. ./management/health-check.sh - Vérifier la santé globale"
}

main "$@"