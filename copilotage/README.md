# 🎯 COPILOTAGE CENTRALISÉ - GOUVERNANCE GLOBALE

## 🚫 AGENTS IA - ARRÊT OBLIGATOIRE

**NOUVEAUX AGENTS IA**: Vous DEVEZ lire `INTRODUCTION_AGENTS_IA.md` et passer l'onboarding avant toute contribution sur TOUS les repositories.

```bash
python3 copilotage/utilities/agent_onboarding.py --start
```

## 📋 ARCHITECTURE GOUVERNANCE GLOBALE

Le copilotage centralisé gouverne TOUS les projets selon le principe fondamental :
**Les outils s'intègrent au copilotage, PAS l'inverse**

## 🏗️ STRUCTURE UNIFIÉE

Cette structure s'applique à tous les repositories via submodules ou héritage :

```
copilotage/
├── README.md                  # Ce fichier
├── INTRODUCTION_AGENTS_IA.md  # Onboarding obligatoire
├── config.yml                 # Configuration maître
├── regles/                    # Règles globales
│   ├── REGLES_GLOBALES.md     # Règles pour tous projets
│   ├── REGLES_PANINI.md       # Spécifiques PaniniFS
│   └── REGLES_EQUIPMENT.md    # Spécifiques Equipment
├── protocols/                 # Protocoles standardisés
│   ├── development.md         # Workflow développement
│   ├── ai-collaboration.md    # Collaboration avec IA
│   └── release.md             # Processus de release
├── utilities/                 # Outils centralisés
│   ├── tools/                 # Modules Python réutilisables
│   │   ├── __init__.py
│   │   ├── system_tools.py
│   │   ├── database_tools.py
│   │   ├── web_tools.py
│   │   ├── analytics_tools.py
│   │   └── reporting_tools.py
│   ├── scripts/               # Scripts de gestion
│   │   ├── submodule_manager.py
│   │   ├── health_checker.py
│   │   └── sync_coordinator.py
│   └── agent_onboarding.py    # Onboarding agents
├── documentation/             # Documentation centralisée
│   ├── architecture.md        # Architecture globale
│   ├── workflows.md           # Workflows standardisés
│   └── troubleshooting.md     # Guide de résolution
├── maintenance/               # Maintenance globale
│   ├── health_reports/        # Rapports de santé
│   ├── metrics/               # Métriques globales
│   └── backups/               # Sauvegardes
└── shared/                    # Assets partagés
    ├── templates/             # Templates de code
    ├── configs/               # Configurations communes
    └── schemas/               # Schémas de données
```

## 🚀 GOUVERNANCE EN ACTION

### Initialisation Workspace Complet
```bash
./management/init-workspace.sh
```

### Onboarding Agent IA (OBLIGATOIRE)
```bash
python3 copilotage/utilities/agent_onboarding.py --start
```

### Synchronisation Globale
```bash
./management/sync-all.sh
```

## 🎯 OBJECTIFS

1. **Cohérence**: Standards unifiés sur tous les projets
2. **Efficacité**: Outils partagés et réutilisables
3. **Qualité**: Gouvernance automatisée
4. **Autonomie**: Agents IA formés et alignés

## 🔄 ÉVOLUTION

Ce système de gouvernance évolue automatiquement et s'adapte aux besoins de tous les projets. Il apprend des interactions et optimise les workflows.

---

*Pour l'initialisation des submodules partagés, voir les instructions dans les scripts de management*