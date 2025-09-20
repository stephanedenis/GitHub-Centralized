# 🏗️ GitHub Centralized - Governance Repository

## 🎯 Mission

Repository central de gouvernance pour tous mes projets GitHub. Utilise une architecture de submodules pour centraliser la gestion, les règles et les outils de tous les repositories.

## 🏛️ Architecture Fondamentale

```
┌─────────────────────────────────────────┐
│  GOUVERNANCE CENTRALISÉE                │
│  Tous les repos en submodules          │
│  Règles et outils unifiés              │
└─────────────────────────────────────────┘
```

### Principe Cardinal
**Les outils s'intègrent au copilotage, PAS l'inverse**

## 📁 Structure

```
GitHub-Centralized/
├── copilotage/                    # Gouvernance centrale
│   ├── README.md                  # Documentation principale
│   ├── INTRODUCTION_AGENTS_IA.md  # Onboarding agents IA
│   ├── config.yml                 # Configuration globale
│   ├── regles/                    # Règles de gouvernance
│   ├── protocols/                 # Protocoles de développement
│   ├── utilities/                 # Outils centralisés
│   │   ├── tools/                 # Modules réutilisables
│   │   └── scripts/               # Scripts de gestion
│   ├── documentation/             # Documentation centralisée
│   ├── maintenance/               # Outils de maintenance
│   └── shared/                    # Assets partagés
├── projects/                      # Tous les repositories en submodules
│   ├── panini/                    # Famille PaniniFS
│   │   ├── PaniniFS/
│   │   ├── PaniniFS-Research/
│   │   ├── PaniniFS-CopilotageShared/
│   │   └── ...
│   ├── equipment/                 # Famille Equipment
│   │   ├── equipment-hauru/
│   │   ├── equipment-remarkable/
│   │   └── ...
│   ├── tooling/                   # Outils et bibliothèques
│   └── exploration/               # Projets expérimentaux
└── management/                    # Scripts de gestion globale
    ├── sync-all.sh               # Synchronisation globale
    ├── update-submodules.sh      # Mise à jour submodules
    └── health-check.sh           # Vérification état global
```

## 🚀 Démarrage Rapide

### 1. Initialisation
```bash
git clone https://github.com/stephanedenis/GitHub-Centralized.git
cd GitHub-Centralized
./management/init-workspace.sh
```

### 2. Synchronisation des submodules
```bash
./management/sync-all.sh
```

### 3. Agents IA - Onboarding obligatoire
```bash
python3 copilotage/utilities/agent_onboarding.py --start
```

## 🤖 Pour les Agents IA

**ARRÊT OBLIGATOIRE** - Lisez `copilotage/INTRODUCTION_AGENTS_IA.md` avant toute contribution.

### Workflow Standard
1. Lire la documentation de gouvernance
2. Passer l'onboarding
3. Utiliser les outils centralisés
4. Respecter l'architecture

## 🔧 Gestion des Submodules

### Ajouter un nouveau repository
```bash
git submodule add https://github.com/stephanedenis/REPO_NAME.git projects/CATEGORY/REPO_NAME
git commit -m "Add REPO_NAME submodule"
```

### Mettre à jour tous les submodules
```bash
git submodule update --remote --recursive
```

### Synchronisation complète
```bash
./management/sync-all.sh
```

## 📊 Familles de Projets

- **PaniniFS**: Système de fichiers génératif
- **Equipment**: Gestion matériel et infrastructure
- **Tooling**: Outils et bibliothèques
- **Exploration**: Projets expérimentaux

## 🛡️ Gouvernance

La gouvernance est centralisée dans le dossier `copilotage/` et s'applique à tous les submodules. Les règles, outils et protocoles sont unifiés pour assurer la cohérence.

---

**🎯 Objectif**: Un point d'entrée unique pour gérer tous mes repositories avec une gouvernance cohérente et des outils partagés.