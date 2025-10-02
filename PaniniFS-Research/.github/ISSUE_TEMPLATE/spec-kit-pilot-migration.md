---
name: Migration Spec-Kit - Projet Pilote Panini-OntoWave
about: Mission de migration du système copilotage vers GitHub Spec-Kit sur projet pilote
title: "[PILOT] Migration Spec-Kit - Panini-OntoWave"
labels: migration, spec-kit, pilot, architecture
assignees: stephanedenis
---

## 🎯 MISSION - Projet Pilote Migration Spec-Kit

**Date création** : 2025-10-02  
**Type** : Architecture & Migration  
**Priorité** : Haute  
**Phase** : Pilote (avant rollout 12+ projets)

---

## 📋 CONTEXTE

### Situation Actuelle
- **14+ projets Panini** utilisent système copilotage interne
- **PaniniFS-CopilotageShared** : Repository central avec règles YAML partagées
- **Copilotage** intégré via Git submodules dans Panini principal
- **PaniniFS-Research** : Spec-Kit déjà installé (isolé, sans shared)

### Objectif Stratégique
Migrer l'écosystème Panini du système copilotage vers **GitHub Spec-Kit officiel** (v0.0.55) tout en préservant la cohérence et les règles partagées via un nouveau repository central **PaniniFS-SpecKit-Shared**.

### Pourquoi un Pilote ?
- Tester l'intégration submodule avant migration critique Panini main (50k+ files)
- Valider la cohérence constitution universelle + spécifique projet
- Identifier problèmes bloquants sur projet plus petit
- Établir procédure reproductible pour les 12+ autres projets

---

## 🎯 OBJECTIFS PILOTE

### 1. Créer PaniniFS-SpecKit-Shared (Repository Central)
- [ ] Initialiser nouveau repository GitHub
- [ ] Installer Spec-Kit (`uv tool install specify-cli`)
- [ ] Migrer règles copilotage existantes :
  - `code-standards.yml` (894 bytes)
  - `conventional-commits.yml` (959 bytes)
  - `pull-requests.yml` (806 bytes)
- [ ] Créer `constitutions/panini-universal-constitution.md` avec `/constitution`
- [ ] Créer templates Spec-Kit partagés (feature-spec, api-spec)
- [ ] Documentation README avec guide intégration submodule

### 2. Migrer Panini-OntoWave (Projet Pilote)
- [ ] Vérifier état actuel projet (git status, dependencies)
- [ ] Installer Spec-Kit (`uv tool install specify-cli`, `specify init`)
- [ ] Ajouter PaniniFS-SpecKit-Shared comme submodule :
  ```bash
  git submodule add https://github.com/stephanedenis/PaniniFS-SpecKit-Shared.git .specify/shared
  git submodule update --init --recursive
  ```
- [ ] Créer `.specify/config.yml` référençant shared
- [ ] Créer constitution projet spécifique (`.specify/memory/constitution.md`)
- [ ] Tester slash commands : `/specify`, `/clarify`, `/plan`, `/tasks`
- [ ] Valider cohérence constitution universelle + projet

### 3. Validation & Documentation
- [ ] Tests fonctionnels :
  - Spec-Kit commands fonctionnent
  - Submodule synchronisé correctement
  - Constitution accessible par agents
  - Templates partagés utilisables
- [ ] Métriques :
  - Temps installation total
  - Nombre commandes nécessaires
  - Problèmes rencontrés + solutions
- [ ] Documenter lessons learned :
  - Difficultés techniques
  - Améliorations procédure
  - Recommendations pour autres projets

---

## 🏗️ ARCHITECTURE TECHNIQUE

### Structure PaniniFS-SpecKit-Shared
```
PaniniFS-SpecKit-Shared/
├── .specify/
│   ├── memory/
│   │   └── constitution.md
│   ├── scripts/
│   └── templates/
├── constitutions/
│   └── panini-universal-constitution.md
├── templates/
│   ├── feature-spec-template.md
│   ├── api-spec-template.md
│   └── refactor-spec-template.md
├── rules/
│   ├── code-standards.yml
│   ├── conventional-commits.yml
│   └── pull-requests.yml
└── README.md
```

### Intégration dans Panini-OntoWave
```
Panini-OntoWave/
├── .specify/
│   ├── shared/              # ← Submodule vers PaniniFS-SpecKit-Shared
│   │   ├── constitutions/
│   │   ├── templates/
│   │   └── rules/
│   ├── config.yml           # Références vers shared
│   ├── memory/
│   │   └── constitution.md  # Constitution spécifique OntoWave
│   ├── scripts/
│   └── templates/
└── .gitmodules              # Configuration submodule
```

### Référencement Shared (config.yml)
```yaml
# .specify/config.yml dans Panini-OntoWave
shared_constitution: .specify/shared/constitutions/panini-universal-constitution.md
project_constitution: .specify/memory/constitution.md

rules:
  - .specify/shared/rules/code-standards.yml
  - .specify/shared/rules/conventional-commits.yml
  - .specify/shared/rules/pull-requests.yml

templates:
  feature: .specify/shared/templates/feature-spec-template.md
  api: .specify/shared/templates/api-spec-template.md
```

---

## 📝 CHECKLIST EXÉCUTION

### Phase 1 : Préparation (Jour 1)
- [ ] Créer repository GitHub `PaniniFS-SpecKit-Shared`
- [ ] Cloner localement : `/home/stephane/GitHub/PaniniFS-SpecKit-Shared`
- [ ] Installer uv si nécessaire : `curl -LsSf https://astral.sh/uv/install.sh | sh`
- [ ] Installer Spec-Kit : `uv tool install specify-cli`
- [ ] Initialiser Spec-Kit : `specify init`

### Phase 2 : Migration Règles (Jour 1)
- [ ] Copier règles YAML depuis `PaniniFS-CopilotageShared/rules/`
- [ ] Créer `constitutions/` directory
- [ ] Générer constitution universelle avec `/constitution` :
  - Contexte : Écosystème Panini multilingue (grammaire Pāṇini)
  - Domaine : NLP, compression sémantique, ontologies
  - Standards : ISO 8601, Git conventional commits
- [ ] Créer templates Spec-Kit génériques
- [ ] Commit & push vers GitHub

### Phase 3 : Pilote Panini-OntoWave (Jour 2)
- [ ] Cloner Panini-OntoWave si pas local
- [ ] Vérifier état : `git status`, `git log --oneline -5`
- [ ] Installer Spec-Kit : `specify init`
- [ ] Ajouter submodule shared :
  ```bash
  git submodule add https://github.com/stephanedenis/PaniniFS-SpecKit-Shared.git .specify/shared
  git submodule update --init --recursive
  ```
- [ ] Créer `.specify/config.yml` avec références shared
- [ ] Créer constitution spécifique OntoWave :
  - Mission : Analyse ondes sémantiques
  - Tech stack : Python, NetworkX, embeddings
  - Spécificités : Graphes, propagation vectorielle
- [ ] Tester commandes Spec-Kit
- [ ] Commit & push avec message conventionnel

### Phase 4 : Validation (Jour 2)
- [ ] Tests fonctionnels :
  - `specify check` → OK
  - `/constitution` → Charge universal + projet
  - `/specify "Feature X"` → Génère spec cohérente
  - `git submodule status` → Commit SHA affiché
- [ ] Tests synchronisation :
  - Modifier shared constitution
  - `git submodule update --remote .specify/shared`
  - Vérifier changements propagés
- [ ] Documenter temps total : _____ minutes
- [ ] Noter problèmes : _______________

### Phase 5 : Documentation (Jour 3)
- [ ] Créer `PILOT_REPORT_PANINI_ONTOWAVE.md` :
  - Étapes exécutées
  - Temps par phase
  - Problèmes + solutions
  - Métriques (commits, files, lignes)
  - Recommendations pour rollout
- [ ] Mettre à jour `MIGRATION_COPILOTAGE_TO_SPEC_KIT.md` avec insights pilote
- [ ] Commit rapport dans PaniniFS-Research
- [ ] Fermer cette issue avec référence rapport

---

## 🎯 CRITÈRES SUCCÈS

### Techniques
- ✅ PaniniFS-SpecKit-Shared créé et peuplé
- ✅ Panini-OntoWave intègre shared via submodule
- ✅ Toutes commandes Spec-Kit fonctionnelles
- ✅ Constitution universelle + spécifique accessible
- ✅ Synchronisation submodule testée avec succès

### Processus
- ✅ Procédure reproductible documentée
- ✅ Temps d'exécution mesuré (baseline pour autres projets)
- ✅ Problèmes identifiés + solutions documentées
- ✅ Zero régression (build, tests, git status clean)

### Documentation
- ✅ Rapport pilote complet créé
- ✅ Lessons learned capturées
- ✅ Guide intégration submodule rédigé
- ✅ Templates prêts pour rollout autres projets

---

## 📊 MÉTRIQUES À CAPTURER

```json
{
  "duration": {
    "total_minutes": null,
    "phase_1_preparation": null,
    "phase_2_shared_setup": null,
    "phase_3_pilot_migration": null,
    "phase_4_validation": null,
    "phase_5_documentation": null
  },
  "files": {
    "shared_repo_files": null,
    "ontowave_modified_files": null,
    "documentation_files": null
  },
  "git": {
    "commits_shared": null,
    "commits_ontowave": null,
    "commits_research": null
  },
  "issues_encountered": [],
  "commands_executed": []
}
```

---

## 🔗 RÉFÉRENCES

### Documents Stratégiques
- `MIGRATION_COPILOTAGE_TO_SPEC_KIT.md` (plan 8 semaines)
- `MIGRATION_EXECUTIVE_SUMMARY.md` (décision Option B)
- `SPEC_KIT_INTEGRATION.md` (guide Spec-Kit)

### Repositories Concernés
- **PaniniFS-Research** : Migration docs + Spec-Kit déjà installé
- **PaniniFS-SpecKit-Shared** : À créer (central shared)
- **Panini-OntoWave** : Projet pilote cible
- **PaniniFS-CopilotageShared** : Ancien système (référence)

### Standards
- `copilotage_date_iso_standard.json` : Format dates ISO 8601
- GitHub Spec-Kit : https://github.com/github/spec-kit
- Spec-Kit Docs : https://github.com/github/spec-kit/tree/main/docs

---

## 🚀 PROCHAINES ÉTAPES APRÈS PILOTE

Si pilote succès (tous critères ✅) :
1. **Batch 2** : Panini main + PaniniFS + SemanticCore (semaines 3-5)
2. **Batch 3** : 4 orchestrateurs (semaine 6)
3. **Batch 4** : 5+ projets support (semaine 7)
4. **Consolidation** : Décommission copilotage (semaine 8)

Si pilote échec partiel (critères ⚠️) :
1. Analyser root causes
2. Ajuster architecture (Option A vs B reconsidération)
3. Itérer pilote v2 sur projet plus simple
4. Réévaluer timeline migration

---

## ✅ DÉFINITION OF DONE

Cette issue est **DONE** quand :
- [ ] PaniniFS-SpecKit-Shared existe sur GitHub avec contenu complet
- [ ] Panini-OntoWave migré avec Spec-Kit + submodule shared fonctionnel
- [ ] Rapport pilote `PILOT_REPORT_PANINI_ONTOWAVE.md` créé et committé
- [ ] Tous tests validation passent (✅)
- [ ] Timeline capturée et documentée
- [ ] Recommendations rollout formulées
- [ ] Issue fermée avec tag `completed` et référence rapport

---

**Assigné à** : @stephanedenis  
**Dépendances** : Aucune (première étape migration)  
**Bloque** : Migration des 12+ autres projets Panini

**Labels** : `migration`, `spec-kit`, `pilot`, `architecture`, `high-priority`
