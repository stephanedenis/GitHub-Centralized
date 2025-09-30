@copilot 

## ⚠️ CLARIFICATIONS MISSION CRITIQUES - Impact PR #13

**Date** : 2025-09-30  
**Docs mis à jour** : Commit 5179b50  
**Références** : [CLARIFICATIONS_MISSION_CRITIQUE.md](https://github.com/stephanedenis/PaniniFS-Research/blob/main/CLARIFICATIONS_MISSION_CRITIQUE.md)

### 🧬 ATOMES SÉMANTIQUES - NOUVEAU PARADIGME

**FOCUS** : Représentation sémantique **PURE**

**Objectif fondamental** :
- Modèle qui **évolue en découvrant symétries parfaites**
- **Composition ↔ Décomposition** : patterns symétriques
- Patterns deviennent **candidats universaux**

**Nouveau paradigme théorie information** :
- ❌ PAS limité au langage
- ❌ PAS limité aux données binaires
- ✅ Théorie information universelle
- ✅ Symétries compositionnelles pures

**Validation universaux** :
- Symétrie parfaite composition/décomposition
- Patterns récurrents cross-domaine
- Invariance transformation
- Généralisation au-delà linguistique

**Implications code** :
1. Détection automatique patterns symétriques
2. Tests symétrie : `compose(decompose(x)) == x`
3. Scoring candidats universaux : symétrie + récurrence + généralité
4. Pas de contrainte aux dhātu (évolution organique)

### 👥 TRADUCTEURS - QUI/QUAND pas COMBIEN

❌ **ANCIEN** : Compter nombre traducteurs  
✅ **NOUVEAU** : Métadonnées **QUI + QUAND + OÙ**

**Principe fondamental** : Traducteur = auteur de sa traduction avec interprétation propre

**Métadonnées CRITIQUES** :
```json
{
  "traducteur": "nom_traducteur",
  "epoque": "2015",
  "contexte_culturel": "France, urbain",
  "langue_source": "en",
  "langue_cible": "fr",
  "corpus": ["livre1", "livre2"],
  "biais": {
    "culturel": "description milieu/vécu",
    "temporel": "contexte époque"
  },
  "style_markers": {
    "subordinations_complexes": 0.78,
    "formalisation": "élevée"
  }
}
```

**Ce qui compte** :
- **Qui** : Identité traducteur (auteur traduction)
- **Quand** : Époque traduction (contexte temporel)
- **Où** : Contexte culturel/géographique
- **Biais** : Culturel (milieu, vécu, époque)
- **Style** : Patterns récurrents = signature traducteur

**Analyse requise** :
- Détection patterns stylistiques par traducteur
- Identification biais culturels/temporels
- Normalisation tenant compte qui/quand/où
- Séparation contenu pur vs teinte traducteur

**Implications code** :
1. Base de données traducteurs enrichie (qui/quand/où)
2. Analyse patterns stylistiques automatique
3. Détection biais par comparaison traductions même source
4. Dashboard métadonnées traducteurs (pas juste compteur)

---

**Actions requises** :
1. Implémenter détection symétries composition/décomposition
2. Enrichir DB traducteurs : qui/quand/où/biais/styles
3. Analyser patterns traducteurs (style + biais comme patterns)
