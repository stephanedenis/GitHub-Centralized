# 📊 STANDARDS DASHBOARD ÉCOSYSTÈME PANINI

**Date** : 2025-09-30  
**Statut** : SPÉCIFICATIONS TECHNIQUES OBLIGATOIRES

## 🎯 SCOPE ÉLARGI

### ❌ ANCIEN : Dashboard seulement PaniniFS
### ✅ NOUVEAU : Dashboard ENSEMBLE recherches Panini

**Modules couverts** :
- PaniniFS (filesystem compression sémantique)
- Atomes sémantiques (découverte universaux)
- Traducteurs (métadonnées qui/quand/où)
- Corpus multilingues
- Métriques compression
- Symétries composition/décomposition

## 🏗️ ARCHITECTURE MODULAIRE

### Principe fondamental
- **Sources multiples** configurables
- **Panels croisés** pour corrélation données
- **Extensible** : ajout nouvelles sources sans refonte

### Structure recommandée
```
dashboard/
├── modules/
│   ├── panini_fs.js          # Métriques filesystem
│   ├── semantic_atoms.js     # Évolution atomes
│   ├── translators.js        # Métadonnées traducteurs
│   ├── corpus.js             # État corpus
│   └── symmetries.js         # Patterns détectés
├── data/
│   ├── panini_fs.json
│   ├── atoms.json
│   ├── translators.json
│   └── corpus.json
└── index.html                # Interface principale
```

## 🖥️ OPTIMISATION UHD/4K

### Résolutions cibles
- **4K UHD** : 3840×2160 (prioritaire)
- **1440p** : 2560×1440 (secondaire)
- **1080p** : 1920×1080 (minimum)

### Principes design
- **Grille fluide** responsive
- **Typographie scalable** (rem/em)
- **Densité information** adaptée écrans larges
- **Layout multi-colonnes** (3-4 colonnes en 4K)

### Exemple layout 4K
```
┌─────────────┬─────────────┬─────────────┬─────────────┐
│  PaniniFS   │   Atomes    │ Traducteurs │   Corpus    │
│  Métriques  │ Sémantiques │             │             │
├─────────────┴─────────────┴─────────────┴─────────────┤
│         Symétries Composition/Décomposition            │
│              (Graphe patterns détectés)                │
├────────────────────────────────────────────────────────┤
│              Timeline Découvertes (ISO 8601)           │
└────────────────────────────────────────────────────────┘
```

## 🎨 ANIMATIONS - STRICTEMENT UTILITAIRES

### ❌ INTERDIT
- Animations décoratives (transitions esthétiques inutiles)
- Effets de parallaxe
- Animations au chargement sans information
- Rotations/zooms décoratifs

### ✅ AUTORISÉ (si et seulement si)

#### 1. Améliorer perspectives données complexes
```javascript
// Exemple : transition fluide entre vues graphe
graph.transition()
  .duration(750)
  .attr("transform", newTransform);
```

**Cas usage valides** :
- Zoom progressif graphe symétries
- Rotation 3D pour montrer faces cachées données
- Transition entre états temporels

#### 2. Attirer attention nouvelles données
```javascript
// Exemple : highlight nouveau pattern détecté
newPattern.classList.add('flash-new-data');
// flash-new-data = pulse 2x puis disparaît
```

**Cas usage valides** :
- Flash visuel nouveau pattern découvert
- Pulsation compteur nouveaux fichiers ingérés
- Changement couleur métrique franchissant seuil

## 🔢 PORTS STANDARDISÉS ÉCOSYSTÈME PANINI

### Principe
- **Port unique par usage** dans écosystème local
- **Réutiliser même port** pour nouvelles versions
- **Documentation centralisée** ce fichier

### Allocation ports

| Port | Usage | Service |
|------|-------|---------|
| 8889 | Dashboard principal | HTTP dashboard écosystème Panini |
| 8890 | API données temps réel | REST API métriques JSON |
| 8891 | WebSocket live updates | WS notifications changements |
| 8892 | PaniniFS monitoring | Métriques filesystem spécifiques |
| 8893 | Atomes sémantiques API | Requêtes état atomes découverts |
| 8894 | Traducteurs DB | API métadonnées traducteurs |

### Fichier config partagé
```json
{
  "ports": {
    "dashboard": 8889,
    "api": 8890,
    "websocket": 8891,
    "panini_fs": 8892,
    "atoms": 8893,
    "translators": 8894
  }
}
```

## 📅 DATES ISO 8601 OBLIGATOIRE

### Standard
**ISO 8601** pour TOUTES dates techniques affichées

### Formats acceptés

#### Dates complètes avec timezone
```
2025-09-30T14:23:45Z          # UTC (préféré)
2025-09-30T10:23:45-04:00     # Avec offset
2025-09-30T14:23:45.123Z      # Avec millisecondes
```

#### Dates seulement (si heure non pertinente)
```
2025-09-30
```

#### Durées
```
PT1H30M       # 1 heure 30 minutes
P3DT4H        # 3 jours 4 heures
```

### ❌ FORMATS INTERDITS
```
09/30/2025              # Format US ambigu
30/09/2025              # Format EU ambigu
Sept 30, 2025           # Texte localisé
```

### Implémentation JavaScript
```javascript
// Affichage date
const isoDate = new Date().toISOString();
document.getElementById('timestamp').textContent = isoDate;

// Parsing
const date = new Date('2025-09-30T14:23:45Z');
```

## 🌐 GITHUB PAGES DÉPLOIEMENT

### Objectif
- **Accès centralisé** dashboard depuis GitHub
- **Lecture JSON** directement branche main
- **Mise à jour auto** via CI/CD

### Configuration

#### 1. Activer GitHub Pages
```bash
# Dans settings repo
Pages → Source: gh-pages branch → /root
```

#### 2. Structure branche gh-pages
```
gh-pages/
├── index.html           # Dashboard principal
├── modules/             # Modules JS
├── css/                 # Styles
└── config.json          # Config ports (statique pour ref)
```

#### 3. CI/CD automatique
```yaml
# .github/workflows/deploy-dashboard.yml
name: Deploy Dashboard
on:
  push:
    branches: [main]
    paths:
      - 'data/**.json'
      - 'dashboard/**'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build dashboard
        run: |
          # Copier dashboard + données JSON
          cp -r dashboard/* gh-pages/
          cp data/*.json gh-pages/data/
      - name: Deploy to gh-pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./gh-pages
```

#### 4. Accès données JSON main branch
```javascript
// Depuis dashboard GitHub Pages
const dataUrl = 'https://raw.githubusercontent.com/stephanedenis/PaniniFS-Research/main/data/atoms.json';
fetch(dataUrl)
  .then(res => res.json())
  .then(data => updateAtomsPanel(data));
```

### Avantages
- ✅ Dashboard accessible URL publique
- ✅ Mise à jour auto push main
- ✅ Lecture directe données JSON
- ✅ Pas de serveur à maintenir

## 📊 PANELS CROISÉS - EXEMPLES

### Panel 1 : Corrélation Atomes ↔ Compression
```
Atome X découvert
├── Utilisé dans Y fichiers
├── Amélioration compression : +3.2%
└── Symétries détectées : [A↔B, C↔D]
```

### Panel 2 : Traducteurs ↔ Biais Patterns
```
Traducteur "Jean Dupont" (1985-2010)
├── Corpus traduits : 12
├── Biais détecté : formalisation excessive
└── Pattern stylistique : subordinations complexes
```

### Panel 3 : Timeline Découvertes
```
2025-09-30T14:23:45Z : Nouvel atome "TRANSFORM"
2025-09-30T10:12:03Z : Symétrie parfaite détectée
2025-09-29T18:45:22Z : Corpus +1000 fichiers
```

## ✅ CHECKLIST CONFORMITÉ

Dashboard conforme si :

- [ ] Architecture modulaire (sources multiples)
- [ ] Optimisé 4K/UHD
- [ ] Ports standardisés (voir tableau)
- [ ] Dates ISO 8601 partout
- [ ] Animations seulement si utilité
- [ ] GitHub Pages configuré
- [ ] JSON accessibles depuis gh-pages
- [ ] Panels croisés implémentés
- [ ] Documentation ports à jour

---

**VERSION** : 1.0.0  
**DERNIÈRE RÉVISION** : 2025-09-30  
**MAINTENU PAR** : Écosystème Panini
