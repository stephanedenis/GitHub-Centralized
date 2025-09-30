@copilot 

## ⚠️ CLARIFICATIONS MISSION CRITIQUES - Impact PR #14

**Date** : 2025-09-30  
**Docs mis à jour** : Commit 5179b50  
**Références complètes** : [STANDARDS_DASHBOARD_ECOSYSTEME_PANINI.md](https://github.com/stephanedenis/PaniniFS-Research/blob/main/STANDARDS_DASHBOARD_ECOSYSTEME_PANINI.md)

### 📊 DASHBOARD - SCOPE ÉLARGI

❌ **ANCIEN** : Dashboard seulement PaniniFS  
✅ **NOUVEAU** : Dashboard **ENSEMBLE recherches Panini**

**Modules à couvrir** :
- PaniniFS (filesystem compression sémantique)
- Atomes sémantiques (découverte universaux)
- Traducteurs (métadonnées qui/quand/où)
- Corpus multilingues
- Métriques compression
- Symétries composition/décomposition

### 🏗️ ARCHITECTURE MODULAIRE OBLIGATOIRE

**Exigences** :
- **Sources multiples** configurables
- **Panels croisés** pour corrélation données
- **Extensible** : ajout nouvelles sources sans refonte

### 🖥️ OPTIMISATION UHD/4K

**Résolutions cibles** :
- 4K UHD : 3840×2160 (prioritaire)
- 1440p : 2560×1440 (secondaire)  
- 1080p : 1920×1080 (minimum)

**Layout multi-colonnes** :
- 3-4 colonnes en 4K
- Grille fluide responsive
- Densité information adaptée grands écrans

### 🎨 ANIMATIONS - STRICTEMENT UTILITAIRES

❌ **INTERDIT** :
- Animations décoratives
- Effets parallaxe
- Rotations/zooms esthétiques

✅ **AUTORISÉ** (si et seulement si) :
1. **Améliorer perspectives** données complexes (zoom graphe, rotation 3D)
2. **Attirer attention** nouvelles données (flash pattern détecté, pulse compteur)

### 🔢 PORTS STANDARDISÉS

**Allocation écosystème Panini** :
- `8889` : Dashboard principal
- `8890` : API données temps réel
- `8891` : WebSocket live updates
- `8892` : PaniniFS monitoring
- `8893` : Atomes sémantiques API
- `8894` : Traducteurs DB

**Principe** : Réutiliser même port pour nouvelles versions (pas de prolifération)

### 📅 DATES ISO 8601 OBLIGATOIRE

**Format unique** : ISO 8601 pour TOUTES dates techniques

```javascript
// ✅ Correct
const timestamp = new Date().toISOString();  // 2025-09-30T14:23:45Z

// ❌ Interdit
const timestamp = "09/30/2025";  // Format US ambigu
const timestamp = "30/09/2025";  // Format EU ambigu
```

### 🌐 GITHUB PAGES DÉPLOIEMENT

**Objectif** :
- Accès centralisé dashboard depuis GitHub
- Lecture JSON directement branche main
- Mise à jour auto via CI/CD

**Configuration suggérée** :
1. Activer GitHub Pages sur branche `gh-pages`
2. CI/CD copie dashboard + JSON lors push main
3. Dashboard lit JSON via raw.githubusercontent.com

---

**Actions requises** :
1. Refactorer architecture modulaire (pas monolithique)
2. Optimiser layout 4K/UHD (multi-colonnes)
3. Standardiser ports (voir tableau)
4. ISO 8601 partout (dates techniques)
5. Supprimer animations décoratives
6. Configurer GitHub Pages + CI/CD
