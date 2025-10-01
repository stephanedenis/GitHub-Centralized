#!/usr/bin/env python3
"""
Analyseur Comparatif Multi-Format
==================================

Compare contenu sémantique extrait depuis différents formats (TXT, PDF, EPUB, MP3).
Identifie universaux (patterns identiques cross-format) vs contextuels (spécifiques format).

Validation: Intégrité 100% sur universaux ou FAIL.

Conform ité:
    - ISO 8601 timestamps
    - Pattern: *_analyzer.py (auto-approuvé via autonomous_wrapper.py)
    - Read-only: true (pas de modification fichiers)
    
Usage:
    python3 multiformat_semantic_analyzer.py <extraction1.json> <extraction2.json> ...
    python3 autonomous_wrapper.py multiformat_semantic_analyzer.py txt_extract.json pdf_extract.json

Auteur: Stéphane Denis (via système zéro-approbation)
Date: 2025-10-01
Version: 1.0
"""

import sys
import json
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Set
from collections import Counter
import re


class MultiFormatSemanticAnalyzer:
    """Analyseur comparatif contenu multi-format"""
    
    def __init__(self):
        self.extractions = []
        
    def load_extraction(self, json_path: Path) -> Dict:
        """Charge fichier extraction JSON"""
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
            
    def analyze(self, extraction_paths: List[Path]) -> Dict:
        """
        Analyse comparative extractions multi-format
        
        Args:
            extraction_paths: Liste chemins JSON extractions
            
        Returns:
            dict avec universaux, contextuels, metrics, timestamp
        """
        # Chargement toutes extractions
        for path in extraction_paths:
            try:
                extraction = self.load_extraction(path)
                if extraction.get("success"):
                    self.extractions.append(extraction)
                else:
                    print(f"⚠️  Skipping failed extraction: {path}")
            except Exception as e:
                print(f"❌ Error loading {path}: {e}")
                
        if len(self.extractions) < 2:
            return self._error_result("Need at least 2 successful extractions")
            
        # Analyse comparative
        universals = self._identify_universals()
        contextuals = self._identify_contextuals()
        cross_format_metrics = self._compute_cross_format_metrics()
        integrity_validation = self._validate_cross_format_integrity()
        
        return {
            "success": True,
            "num_formats_compared": len(self.extractions),
            "formats": [e["format"] for e in self.extractions],
            "universals": universals,
            "contextuals": contextuals,
            "cross_format_metrics": cross_format_metrics,
            "integrity_validation": integrity_validation,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
    def _identify_universals(self) -> Dict:
        """Identifie patterns universels (identiques tous formats)"""
        # Extraction mots tous formats
        all_words = []
        for extraction in self.extractions:
            content = extraction.get("content", "")
            words = set(re.findall(r'\b\w+\b', content.lower()))
            all_words.append(words)
            
        # Intersection: mots présents dans TOUS formats
        if all_words:
            universal_words = set.intersection(*all_words)
        else:
            universal_words = set()
            
        # Dhātu candidats universels
        all_dhatu = []
        for extraction in self.extractions:
            sem = extraction.get("semantic_analysis", {})
            dhatu = set(sem.get("dhatu_candidates", []))
            all_dhatu.append(dhatu)
            
        if all_dhatu:
            universal_dhatu = set.intersection(*all_dhatu)
        else:
            universal_dhatu = set()
            
        # Concepts universels
        all_concepts = []
        for extraction in self.extractions:
            sem = extraction.get("semantic_analysis", {})
            concepts = set(sem.get("concepts_detected", []))
            all_concepts.append(concepts)
            
        if all_concepts:
            universal_concepts = set.intersection(*all_concepts)
        else:
            universal_concepts = set()
            
        return {
            "universal_words": sorted(list(universal_words))[:50],  # Top 50
            "universal_words_count": len(universal_words),
            "universal_dhatu": sorted(list(universal_dhatu)),
            "universal_dhatu_count": len(universal_dhatu),
            "universal_concepts": sorted(list(universal_concepts)),
            "universal_concepts_count": len(universal_concepts),
            "recurrence_rate": round(len(universal_words) / len(set.union(*all_words)) if all_words else 0, 3)
        }
        
    def _identify_contextuals(self) -> Dict:
        """Identifie patterns contextuels (spécifiques à formats)"""
        contextual_by_format = {}
        
        # Pour chaque format
        for extraction in self.extractions:
            format_name = extraction["format"]
            content = extraction.get("content", "")
            words = set(re.findall(r'\b\w+\b', content.lower()))
            
            # Mots présents dans ce format uniquement
            other_extractions = [e for e in self.extractions if e["format"] != format_name]
            other_words = []
            for e in other_extractions:
                c = e.get("content", "")
                other_words.append(set(re.findall(r'\b\w+\b', c.lower())))
                
            if other_words:
                unique_words = words - set.union(*other_words)
            else:
                unique_words = words
                
            contextual_by_format[format_name] = {
                "unique_words": sorted(list(unique_words))[:20],  # Top 20
                "unique_words_count": len(unique_words),
                "format_specific_features": self._extract_format_features(extraction)
            }
            
        return contextual_by_format
        
    def _extract_format_features(self, extraction: Dict) -> List[str]:
        """Extrait features spécifiques au format"""
        features = []
        format_name = extraction["format"]
        
        if format_name == "PDF":
            features.append(f"Pages: {extraction.get('metadata', {}).get('num_pages', 0)}")
            pdf_meta = extraction.get('metadata', {}).get('pdf_metadata', {})
            if pdf_meta:
                features.append(f"PDF metadata: {len(pdf_meta)} fields")
                
        elif format_name == "TXT":
            features.append(f"Encoding: {extraction.get('metadata', {}).get('encoding', 'unknown')}")
            features.append(f"Line endings: {extraction.get('metadata', {}).get('line_endings', 'unknown')}")
            
        elif format_name == "EPUB":
            features.append("HTML structured content")
            features.append("Navigation TOC")
            
        elif format_name == "MP3":
            features.append("Audio transcription")
            features.append("Prosody information")
            
        return features
        
    def _compute_cross_format_metrics(self) -> Dict:
        """Calcule métriques comparatives cross-format"""
        metrics = {}
        
        # Longueurs contenu
        content_lengths = [e.get("content_length_chars", 0) for e in self.extractions]
        metrics["content_length_mean"] = round(sum(content_lengths) / len(content_lengths))
        metrics["content_length_variance"] = round(max(content_lengths) - min(content_lengths))
        metrics["content_length_consistency"] = round(1 - (metrics["content_length_variance"] / metrics["content_length_mean"]), 3) if metrics["content_length_mean"] > 0 else 0
        
        # Richesse vocabulaire
        vocab_richness = [
            e.get("semantic_analysis", {}).get("vocabulary_richness", 0)
            for e in self.extractions
        ]
        metrics["vocabulary_richness_mean"] = round(sum(vocab_richness) / len(vocab_richness), 3)
        
        # Mots total
        total_words = [
            e.get("semantic_analysis", {}).get("total_words", 0)
            for e in self.extractions
        ]
        metrics["total_words_mean"] = round(sum(total_words) / len(total_words))
        metrics["total_words_variance"] = round(max(total_words) - min(total_words))
        
        return metrics
        
    def _validate_cross_format_integrity(self) -> Dict:
        """Valide intégrité cross-format"""
        # Vérifier que tous formats ont intégrité 100%
        all_valid = all(
            e.get("integrity", {}).get("integrity_percentage", 0) == 100.0
            for e in self.extractions
        )
        
        # Hashes contenus
        hashes = {}
        for extraction in self.extractions:
            format_name = extraction["format"]
            integrity = extraction.get("integrity", {})
            
            # Essayer différents noms hash
            hash_val = (
                integrity.get("sha256") or
                integrity.get("content_sha256") or
                "unknown"
            )
            hashes[format_name] = hash_val
            
        # Vérifier si hashes identiques (contenu EXACTEMENT identique)
        unique_hashes = set(h for h in hashes.values() if h != "unknown")
        content_identical = len(unique_hashes) == 1 if unique_hashes else False
        
        return {
            "all_formats_valid": all_valid,
            "content_hashes": hashes,
            "content_exactly_identical": content_identical,
            "integrity_percentage": 100.0 if all_valid else 0.0,
            "validation_status": "PASS" if all_valid else "FAIL"
        }
        
    def _error_result(self, error_msg: str) -> Dict:
        """Résultat erreur standardisé"""
        return {
            "success": False,
            "error": error_msg,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
    def export_json(self, result: Dict, output_path: Path = None):
        """Exporte résultats en JSON"""
        if output_path is None:
            timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H-%M-%SZ')
            output_path = Path(f"multiformat_analysis_{timestamp}.json")
            
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
            
        return output_path


def main():
    """Point d'entrée CLI"""
    if len(sys.argv) < 3:
        print("Usage: python3 multiformat_semantic_analyzer.py <extract1.json> <extract2.json> ...")
        print("\nExemple:")
        print("  python3 multiformat_semantic_analyzer.py txt_extract.json pdf_extract.json")
        print("\nAuto-approved via autonomous_wrapper.py:")
        print("  python3 autonomous_wrapper.py multiformat_semantic_analyzer.py txt.json pdf.json")
        sys.exit(1)
        
    extraction_paths = [Path(p) for p in sys.argv[1:]]
    
    # Analyse
    analyzer = MultiFormatSemanticAnalyzer()
    result = analyzer.analyze(extraction_paths)
    
    # Export JSON
    if result["success"]:
        output_file = analyzer.export_json(result)
        
        # Affichage résumé
        print("=" * 70)
        print("✅ ANALYSE MULTI-FORMAT RÉUSSIE")
        print("=" * 70)
        print(f"Formats comparés: {result['num_formats_compared']}")
        print(f"Liste: {', '.join(result['formats'])}")
        
        print(f"\n🌐 UNIVERSAUX (Cross-Format)")
        univ = result['universals']
        print(f"  - Mots universels: {univ['universal_words_count']}")
        print(f"  - Dhātu universels: {univ['universal_dhatu_count']}")
        print(f"  - Concepts universels: {univ['universal_concepts_count']}")
        print(f"  - Taux récurrence: {univ['recurrence_rate']}")
        
        print(f"\n🔸 CONTEXTUELS (Format-Specific)")
        for format_name, ctx in result['contextuals'].items():
            print(f"  - {format_name}: {ctx['unique_words_count']} mots uniques")
            
        print(f"\n📊 MÉTRIQUES CROSS-FORMAT")
        metrics = result['cross_format_metrics']
        print(f"  - Longueur moyenne: {metrics['content_length_mean']} chars")
        print(f"  - Consistency: {metrics['content_length_consistency']}")
        print(f"  - Richesse vocab: {metrics['vocabulary_richness_mean']}")
        
        print(f"\n✅ VALIDATION INTÉGRITÉ")
        integ = result['integrity_validation']
        print(f"  - Tous formats valides: {integ['all_formats_valid']}")
        print(f"  - Contenu identique: {integ['content_exactly_identical']}")
        print(f"  - Status: {integ['validation_status']}")
        print(f"  - Intégrité: {integ['integrity_percentage']}%")
        
        print(f"\n💾 Export: {output_file}")
        print(f"Timestamp: {result['timestamp']}")
        print("=" * 70)
    else:
        print("❌ ANALYSE ÉCHOUÉE")
        print(f"Erreur: {result['error']}")
        sys.exit(1)


if __name__ == "__main__":
    main()
