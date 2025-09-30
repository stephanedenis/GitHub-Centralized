#!/usr/bin/env python3
"""
POC - Détection Symétries Composition/Décomposition
====================================================

Nouveau paradigme théorie information universelle:
- Focus: Représentation sémantique PURE
- Objectif: Découvrir symétries parfaites composition ↔ décomposition
- Test fondamental: compose(decompose(x)) == x

Date: 2025-09-30
Conformité: ISO 8601, clarifications mission
"""

from datetime import datetime, timezone
from typing import Any, List, Dict, Tuple, Optional
import json
import hashlib


class SymmetryPattern:
    """Représente un pattern de symétrie composition/décomposition"""
    
    def __init__(self, pattern_id: str, description: str):
        self.pattern_id = pattern_id
        self.description = description
        self.discovered_at = datetime.now(timezone.utc).isoformat()
        self.symmetry_score = 0.0  # 1.0 = symétrie parfaite
        self.recurrence_count = 0
        self.cross_domain_validated = False
        
    def to_dict(self) -> Dict:
        return {
            "pattern_id": self.pattern_id,
            "description": self.description,
            "discovered_at": self.discovered_at,
            "symmetry_score": self.symmetry_score,
            "recurrence_count": self.recurrence_count,
            "cross_domain_validated": self.cross_domain_validated,
            "is_universal_candidate": self.is_universal_candidate()
        }
    
    def is_universal_candidate(self) -> bool:
        """Un pattern est candidat universel si symétrie parfaite + récurrence + cross-domain"""
        return (
            self.symmetry_score >= 0.99 and  # Symétrie quasi-parfaite
            self.recurrence_count >= 3 and    # Récurrent
            self.cross_domain_validated       # Validé cross-domaine
        )


class SymmetryDetector:
    """
    Détecteur de symétries composition/décomposition
    
    Principe:
    1. Décomposer objet en composants
    2. Recomposer à partir des composants
    3. Vérifier identité: original == recomposé
    4. Scorer symétrie: hash_match + semantic_match
    """
    
    def __init__(self):
        self.discovered_patterns: List[SymmetryPattern] = []
        self.symmetry_log: List[Dict] = []
        
    def compose(self, components: List[Any]) -> Any:
        """
        Composition: components → objet
        
        Version POC: simple concaténation
        Production: règles composition sophistiquées
        """
        if not components:
            return None
            
        # POC: concaténation string
        if all(isinstance(c, str) for c in components):
            return "".join(components)
        
        # POC: list composition
        return components
    
    def decompose(self, obj: Any) -> List[Any]:
        """
        Décomposition: objet → components
        
        Version POC: découpage simple
        Production: analyse sémantique profonde
        """
        if obj is None:
            return []
        
        # POC: string → caractères
        if isinstance(obj, str):
            # Décomposition par mots (plus sémantique que caractères)
            if " " in obj:
                return obj.split()
            return list(obj)
        
        # POC: déjà une liste
        if isinstance(obj, list):
            return obj
        
        # Fallback: objet unique
        return [obj]
    
    def test_symmetry(self, original: Any) -> Tuple[bool, float]:
        """
        Test symétrie fondamental: compose(decompose(x)) == x
        
        Returns:
            (is_symmetric, symmetry_score)
            - is_symmetric: True si symétrie parfaite
            - symmetry_score: 0.0-1.0 (1.0 = parfait)
        """
        # Décomposition
        components = self.decompose(original)
        
        # Recomposition
        reconstructed = self.compose(components)
        
        # Test identité stricte
        is_identical = (original == reconstructed)
        
        # Score symétrie (hash + semantic)
        if is_identical:
            symmetry_score = 1.0
        else:
            # Similarité partielle (hash comparison)
            orig_hash = hashlib.sha256(str(original).encode()).hexdigest()
            recon_hash = hashlib.sha256(str(reconstructed).encode()).hexdigest()
            
            # Hamming distance sur hashs (approximation)
            matching_chars = sum(
                1 for a, b in zip(orig_hash, recon_hash) if a == b
            )
            symmetry_score = matching_chars / len(orig_hash)
        
        # Log tentative
        self.symmetry_log.append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "original": str(original)[:100],
            "components": [str(c)[:50] for c in components[:5]],
            "reconstructed": str(reconstructed)[:100],
            "is_symmetric": is_identical,
            "symmetry_score": symmetry_score
        })
        
        return is_identical, symmetry_score
    
    def discover_patterns(self, dataset: List[Any]) -> List[SymmetryPattern]:
        """
        Découverte automatique patterns symétriques dans dataset
        
        Processus:
        1. Tester symétrie sur chaque élément
        2. Identifier patterns récurrents
        3. Valider cross-domaine
        4. Scorer candidats universaux
        """
        print(f"\n🔬 Découverte patterns symétriques...")
        print(f"   Dataset: {len(dataset)} éléments")
        print(f"   Timestamp: {datetime.now(timezone.utc).isoformat()}\n")
        
        symmetry_results = []
        
        for idx, item in enumerate(dataset):
            is_sym, score = self.test_symmetry(item)
            symmetry_results.append({
                "item": item,
                "symmetric": is_sym,
                "score": score
            })
            
            if is_sym:
                print(f"   ✅ Symétrie parfaite: {str(item)[:50]}...")
            elif score > 0.9:
                print(f"   ⚠️  Symétrie partielle ({score:.2%}): {str(item)[:50]}...")
        
        # Identifier patterns récurrents
        perfect_symmetries = [r for r in symmetry_results if r["symmetric"]]
        partial_symmetries = [r for r in symmetry_results if r["score"] > 0.9 and not r["symmetric"]]
        
        print(f"\n📊 Résultats:")
        print(f"   Symétries parfaites: {len(perfect_symmetries)}/{len(dataset)} ({len(perfect_symmetries)/len(dataset)*100:.1f}%)")
        print(f"   Symétries partielles (>90%): {len(partial_symmetries)}")
        
        # Créer pattern pour symétries parfaites
        if perfect_symmetries:
            pattern = SymmetryPattern(
                pattern_id=f"pattern_{datetime.now(timezone.utc).timestamp()}",
                description=f"Symétrie composition/décomposition sur {len(perfect_symmetries)} items"
            )
            pattern.symmetry_score = 1.0
            pattern.recurrence_count = len(perfect_symmetries)
            # TODO: valider cross-domain avec dataset multi-domaine
            
            self.discovered_patterns.append(pattern)
            print(f"\n🎯 Pattern découvert: {pattern.pattern_id}")
            print(f"   Candidat universel: {pattern.is_universal_candidate()}")
        
        return self.discovered_patterns
    
    def export_results(self, filepath: str = "symmetry_detection_results.json"):
        """Exporter résultats en JSON (ISO 8601 conforme)"""
        results = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "total_tests": len(self.symmetry_log),
            "discovered_patterns": [p.to_dict() for p in self.discovered_patterns],
            "symmetry_log": self.symmetry_log[-20:]  # Derniers 20 tests
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Résultats exportés: {filepath}")
        return filepath


def main():
    """Test POC avec données exemple"""
    print("="*70)
    print("🧬 POC - Détection Symétries Composition/Décomposition")
    print("="*70)
    
    detector = SymmetryDetector()
    
    # Dataset test 1: Strings simples (devrait être symétrique)
    print("\n### Test 1: Strings simples")
    dataset1 = [
        "hello world",
        "composition test",
        "semantic atoms",
        "universal theory",
        "panini research"
    ]
    
    patterns1 = detector.discover_patterns(dataset1)
    
    # Dataset test 2: Structures complexes
    print("\n" + "="*70)
    print("\n### Test 2: Structures mixtes")
    dataset2 = [
        ["atom1", "atom2", "atom3"],
        ["compose", "decompose"],
        "single_string",
        ["nested", ["structure"]],
        "another test"
    ]
    
    patterns2 = detector.discover_patterns(dataset2)
    
    # Export résultats
    detector.export_results()
    
    # Résumé final
    print("\n" + "="*70)
    print("📋 RÉSUMÉ FINAL")
    print("="*70)
    print(f"Total patterns découverts: {len(detector.discovered_patterns)}")
    print(f"Candidats universaux: {sum(1 for p in detector.discovered_patterns if p.is_universal_candidate())}")
    print(f"Tests symétrie effectués: {len(detector.symmetry_log)}")
    
    universal_candidates = [p for p in detector.discovered_patterns if p.is_universal_candidate()]
    if universal_candidates:
        print("\n🎯 CANDIDATS UNIVERSAUX DÉTECTÉS:")
        for p in universal_candidates:
            print(f"   - {p.pattern_id}: {p.description}")
            print(f"     Score: {p.symmetry_score:.2%}, Récurrence: {p.recurrence_count}")
    else:
        print("\n⚠️  Aucun candidat universel (critères: symétrie ≥99%, récurrence ≥3, cross-domain validé)")
    
    print("\n✅ POC terminé!")
    print(f"   Timestamp: {datetime.now(timezone.utc).isoformat()}")


if __name__ == "__main__":
    main()
