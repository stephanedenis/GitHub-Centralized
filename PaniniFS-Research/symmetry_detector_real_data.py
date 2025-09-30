#!/usr/bin/env python3
"""
POC v2 - Détection Symétries sur Données Réelles Panini
========================================================

Test sur données réelles du projet pour découvrir patterns symétriques.
Focus: Représentation sémantique PURE + théorie information universelle

Date: 2025-09-30
"""

from symmetry_detector_poc import SymmetryDetector, SymmetryPattern
from datetime import datetime, timezone
import json
from pathlib import Path


def load_real_panini_data():
    """Charger données réelles Panini"""
    print("📂 Chargement données réelles Panini...")
    
    data_files = [
        "panini_real_data.json",
        "extracted_content.json",
        "dashboard_real_data.json"
    ]
    
    loaded_data = {}
    for filename in data_files:
        filepath = Path(filename)
        if filepath.exists():
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    loaded_data[filename] = json.load(f)
                print(f"   ✅ {filename}: {len(str(loaded_data[filename]))} chars")
            except Exception as e:
                print(f"   ⚠️  {filename}: Erreur - {e}")
    
    return loaded_data


def extract_test_dataset(panini_data: dict) -> list:
    """Extraire dataset test depuis données Panini"""
    print("\n🔍 Extraction dataset test...")
    
    dataset = []
    
    # Extraire fichiers réels
    if "panini_real_data.json" in panini_data:
        data = panini_data["panini_real_data.json"]
        
        # Noms fichiers
        if "real_files" in data:
            for file_info in data["real_files"][:20]:  # 20 premiers
                if "name" in file_info:
                    dataset.append(file_info["name"])
        
        # Types fichiers
        if "scan_summary" in data and "file_types" in data["scan_summary"]:
            for file_type in data["scan_summary"]["file_types"].keys():
                dataset.append(file_type)
    
    # Extraire contenu sémantique
    if "extracted_content.json" in panini_data:
        content = panini_data["extracted_content.json"]
        if isinstance(content, dict):
            for key, value in list(content.items())[:10]:
                if isinstance(value, str) and len(value) < 200:
                    dataset.append(value)
                elif isinstance(value, dict) and "content" in value:
                    if isinstance(value["content"], str) and len(value["content"]) < 200:
                        dataset.append(value["content"])
    
    print(f"   Dataset extrait: {len(dataset)} éléments")
    return dataset


def test_semantic_atoms(detector: SymmetryDetector):
    """Test spécifique: atomes sémantiques comme concepts décomposables"""
    print("\n" + "="*70)
    print("🧬 TEST ATOMES SÉMANTIQUES")
    print("="*70)
    
    # Hypothèse: concepts complexes = composition atomes simples
    concepts = [
        # Concepts simples (devraient être symétriques)
        "run",
        "eat",
        "think",
        
        # Concepts composés (test composition)
        "running fast",
        "eating food",
        "thinking deeply",
        
        # Structures plus complexes
        "universal semantic atoms",
        "composition decomposition symmetry",
        "information theory paradigm"
    ]
    
    patterns = detector.discover_patterns(concepts)
    
    print(f"\n📊 Atomes sémantiques:")
    print(f"   Symétries détectées: {len([p for p in patterns if p.symmetry_score >= 0.99])}")
    
    return patterns


def test_cross_domain_validation(detector: SymmetryDetector):
    """Test validation cross-domaine: patterns dans domaines différents"""
    print("\n" + "="*70)
    print("🌐 TEST VALIDATION CROSS-DOMAINE")
    print("="*70)
    
    # Dataset multi-domaine
    datasets = {
        "linguistic": ["word", "sentence", "grammar", "syntax"],
        "numeric": ["123", "456", "789"],
        "symbolic": ["@", "#", "$"],
        "mixed": ["abc123", "test@domain", "file_name.json"]
    }
    
    cross_domain_patterns = []
    
    for domain_name, domain_data in datasets.items():
        print(f"\n   🔬 Domaine: {domain_name}")
        patterns = detector.discover_patterns(domain_data)
        
        if patterns:
            for p in patterns:
                p.cross_domain_validated = True
                cross_domain_patterns.append((domain_name, p))
    
    print(f"\n📊 Patterns cross-domaine:")
    print(f"   Total domaines testés: {len(datasets)}")
    print(f"   Patterns validés: {len(cross_domain_patterns)}")
    
    return cross_domain_patterns


def analyze_symmetry_quality(detector: SymmetryDetector):
    """Analyser qualité symétries détectées"""
    print("\n" + "="*70)
    print("📈 ANALYSE QUALITÉ SYMÉTRIES")
    print("="*70)
    
    if not detector.symmetry_log:
        print("   ⚠️  Aucune donnée à analyser")
        return
    
    # Statistiques
    total_tests = len(detector.symmetry_log)
    perfect = sum(1 for test in detector.symmetry_log if test["is_symmetric"])
    high_score = sum(1 for test in detector.symmetry_log if test["symmetry_score"] > 0.95)
    medium_score = sum(1 for test in detector.symmetry_log if 0.80 <= test["symmetry_score"] <= 0.95)
    low_score = sum(1 for test in detector.symmetry_log if test["symmetry_score"] < 0.80)
    
    avg_score = sum(test["symmetry_score"] for test in detector.symmetry_log) / total_tests
    
    print(f"\n   Total tests: {total_tests}")
    print(f"   Symétries parfaites (100%): {perfect} ({perfect/total_tests*100:.1f}%)")
    print(f"   Score élevé (>95%): {high_score} ({high_score/total_tests*100:.1f}%)")
    print(f"   Score moyen (80-95%): {medium_score} ({medium_score/total_tests*100:.1f}%)")
    print(f"   Score faible (<80%): {low_score} ({low_score/total_tests*100:.1f}%)")
    print(f"   Score moyen global: {avg_score:.2%}")
    
    # Identifier patterns récurrents d'échec
    failed_tests = [t for t in detector.symmetry_log if not t["is_symmetric"]]
    if failed_tests:
        print(f"\n   ⚠️  Échecs symétrie: {len(failed_tests)}")
        print(f"   Exemples échecs:")
        for test in failed_tests[:3]:
            print(f"      - Original: {test['original'][:50]}...")
            print(f"        Reconstruit: {test['reconstructed'][:50]}...")
            print(f"        Score: {test['symmetry_score']:.2%}")


def main():
    """Test POC v2 sur données réelles"""
    print("="*70)
    print("🧬 POC v2 - Symétries sur Données Réelles Panini")
    print("="*70)
    print(f"Timestamp: {datetime.now(timezone.utc).isoformat()}\n")
    
    detector = SymmetryDetector()
    
    # 1. Charger données réelles
    panini_data = load_real_panini_data()
    
    if not panini_data:
        print("⚠️  Aucune donnée réelle trouvée, utilisation données test")
        dataset = ["test1", "test2", "test3"]
    else:
        dataset = extract_test_dataset(panini_data)
    
    # 2. Test sur données réelles
    print("\n" + "="*70)
    print("📊 TEST DONNÉES RÉELLES PANINI")
    print("="*70)
    patterns_real = detector.discover_patterns(dataset)
    
    # 3. Test atomes sémantiques
    patterns_atoms = test_semantic_atoms(detector)
    
    # 4. Test cross-domaine
    cross_domain = test_cross_domain_validation(detector)
    
    # 5. Analyse qualité
    analyze_symmetry_quality(detector)
    
    # 6. Export résultats
    output_file = "symmetry_detection_real_panini_data.json"
    detector.export_results(output_file)
    
    # 7. Résumé final
    print("\n" + "="*70)
    print("📋 RÉSUMÉ FINAL - POC v2")
    print("="*70)
    
    all_patterns = detector.discovered_patterns
    universal_candidates = [p for p in all_patterns if p.is_universal_candidate()]
    
    print(f"\nPatterns découverts: {len(all_patterns)}")
    print(f"Candidats universaux: {len(universal_candidates)}")
    print(f"Tests effectués: {len(detector.symmetry_log)}")
    print(f"Validation cross-domaine: {len(cross_domain)} patterns")
    
    if universal_candidates:
        print("\n🎯 CANDIDATS UNIVERSAUX:")
        for p in universal_candidates:
            print(f"\n   Pattern: {p.pattern_id}")
            print(f"   - Description: {p.description}")
            print(f"   - Score symétrie: {p.symmetry_score:.2%}")
            print(f"   - Récurrence: {p.recurrence_count}")
            print(f"   - Cross-domaine: {'✅' if p.cross_domain_validated else '❌'}")
    else:
        print("\n⏳ Aucun candidat universel encore")
        print("   Critères requis:")
        print("   - Symétrie ≥ 99%")
        print("   - Récurrence ≥ 3")
        print("   - Validation cross-domaine")
    
    print(f"\n✅ POC v2 terminé!")
    print(f"   Résultats: {output_file}")
    print(f"   Timestamp: {datetime.now(timezone.utc).isoformat()}")


if __name__ == "__main__":
    main()
