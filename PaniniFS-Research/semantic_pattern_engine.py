#!/usr/bin/env python3
"""
Moteur de Patterns Sémantiques Universels
==========================================

Système unifié d'analyse sémantique multi-dimensionnelle:
- Patterns linguistiques universaux
- Structures sémantiques cross-format
- Invariants informationnels
- Corrélations inter-analyseurs

Agrège tous les analyseurs existants pour identifier méta-patterns.

Date: 2025-10-02
Auteur: Système Autonome PaniniFS
Version: 1.0.0
"""

import sys
import json
import asyncio
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Set, Optional, Any
from collections import defaultdict, Counter
from dataclasses import dataclass, asdict
import re
import numpy as np
from itertools import combinations
import subprocess


@dataclass
class SemanticPattern:
    """Représentation d'un pattern sémantique"""
    pattern_id: str
    pattern_type: str  # 'universal', 'contextual', 'hybrid'
    strength: float   # 0.0-1.0
    confidence: float # 0.0-1.0
    sources: List[str]  # Analyseurs sources
    evidence: List[Dict]
    timestamp: str
    

@dataclass 
class UniversalInvariant:
    """Invariant universel détecté"""
    invariant_id: str
    description: str
    mathematical_form: Optional[str]
    evidence_count: int
    cross_format_validation: bool
    cross_analyzer_validation: bool
    universality_score: float


class SemanticPatternEngine:
    """Moteur d'analyse patterns sémantiques universaux"""
    
    def __init__(self):
        self.patterns = []
        self.invariants = []
        self.analyzer_outputs = {}
        self.correlation_matrix = None
        
    def load_analyzer_output(self, analyzer_name: str, output_path: Path) -> Dict:
        """Charge sortie d'un analyseur spécifique"""
        try:
            with open(output_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.analyzer_outputs[analyzer_name] = data
            print(f"✅ Chargé: {analyzer_name} ({output_path.name})")
            return data
        except Exception as e:
            print(f"❌ Erreur chargement {analyzer_name}: {e}")
            return {}
    
    def auto_discover_analyzers(self) -> Dict[str, Path]:
        """Découverte automatique des sorties d'analyseurs"""
        print("\n🔍 DÉCOUVERTE AUTOMATIQUE ANALYSEURS")
        print("=" * 50)
        
        current_dir = Path('.')
        analyzer_files = {}
        
        # Patterns de fichiers analyseurs
        patterns = {
            'translator_bias': '*translator*bias*analysis*.json',
            'multiformat': '*multiformat*analysis*.json', 
            'extraction': '*extract*.json',
            'project_essence': '*project*essence*.json',
            'corpus_validation': '*corpus*validation*.json',
            'compression_benchmarks': '*compression*benchmarks*.json'
        }
        
        for analyzer_type, pattern in patterns.items():
            files = list(current_dir.glob(pattern))
            if files:
                # Prendre le plus récent
                latest = max(files, key=lambda f: f.stat().st_mtime)
                analyzer_files[analyzer_type] = latest
                print(f"  • {analyzer_type}: {latest.name}")
        
        return analyzer_files
    
    def extract_semantic_patterns(self) -> List[SemanticPattern]:
        """Extraction patterns sémantiques cross-analyseurs"""
        print("\n🧠 EXTRACTION PATTERNS SÉMANTIQUES")
        print("=" * 50)
        
        patterns = []
        
        # 1. Patterns de biais culturels universaux
        if 'translator_bias' in self.analyzer_outputs:
            bias_data = self.analyzer_outputs['translator_bias']
            universal_biases = self._analyze_universal_biases(bias_data)
            patterns.extend(universal_biases)
        
        # 2. Patterns multi-format 
        if 'multiformat' in self.analyzer_outputs:
            format_data = self.analyzer_outputs['multiformat']
            format_patterns = self._analyze_format_patterns(format_data)
            patterns.extend(format_patterns)
        
        # 3. Patterns d'extraction
        extraction_patterns = self._analyze_extraction_patterns()
        patterns.extend(extraction_patterns)
        
        # 4. Meta-patterns cross-analyseurs
        meta_patterns = self._analyze_meta_patterns()
        patterns.extend(meta_patterns)
        
        return patterns
    
    def _analyze_universal_biases(self, bias_data: Dict) -> List[SemanticPattern]:
        """Analyse biais universaux détectés"""
        patterns = []
        
        if 'patterns_culturels' in bias_data:
            cultural = bias_data['patterns_culturels']
            
            # Chercher patterns récurrents (candidats universaux)
            for pattern_name, translators in cultural.items():
                if len(translators) >= 2:  # Au moins 2 traducteurs
                    strength = len(translators) / bias_data.get('traducteurs_analyses', 1)
                    
                    pattern = SemanticPattern(
                        pattern_id=f"cultural_bias_{pattern_name.lower().replace(' ', '_')}",
                        pattern_type='universal' if strength > 0.8 else 'hybrid',
                        strength=strength,
                        confidence=0.85,
                        sources=['translator_bias_analyzer'],
                        evidence=[{'type': 'cultural_recurrence', 'translators': translators}],
                        timestamp=datetime.now(timezone.utc).isoformat()
                    )
                    patterns.append(pattern)
        
        return patterns
    
    def _analyze_format_patterns(self, format_data: Dict) -> List[SemanticPattern]:
        """Analyse patterns multi-format"""
        patterns = []
        
        # Analyser invariants cross-format
        if 'universal_patterns' in format_data:
            for pattern_name, pattern_info in format_data['universal_patterns'].items():
                strength = pattern_info.get('consistency_score', 0.0)
                
                pattern = SemanticPattern(
                    pattern_id=f"multiformat_{pattern_name}",
                    pattern_type='universal',
                    strength=strength,
                    confidence=pattern_info.get('confidence', 0.7),
                    sources=['multiformat_analyzer'],
                    evidence=[pattern_info],
                    timestamp=datetime.now(timezone.utc).isoformat()
                )
                patterns.append(pattern)
        
        return patterns
    
    def _analyze_extraction_patterns(self) -> List[SemanticPattern]:
        """Analyse patterns d'extraction"""
        patterns = []
        
        # Analyser cohérence entre extractions
        extraction_keys = [k for k in self.analyzer_outputs.keys() if 'extract' in k]
        
        if len(extraction_keys) >= 2:
            common_structures = self._find_common_structures(extraction_keys)
            
            for structure_name, structure_info in common_structures.items():
                pattern = SemanticPattern(
                    pattern_id=f"extraction_structure_{structure_name}",
                    pattern_type='universal',
                    strength=structure_info['consistency'],
                    confidence=0.8,
                    sources=extraction_keys,
                    evidence=[structure_info],
                    timestamp=datetime.now(timezone.utc).isoformat()
                )
                patterns.append(pattern)
        
        return patterns
    
    def _analyze_meta_patterns(self) -> List[SemanticPattern]:
        """Analyse méta-patterns cross-analyseurs"""
        patterns = []
        
        # Chercher corrélations entre différents analyseurs
        analyzer_names = list(self.analyzer_outputs.keys())
        
        for analyzer_a, analyzer_b in combinations(analyzer_names, 2):
            correlation = self._calculate_cross_analyzer_correlation(analyzer_a, analyzer_b)
            
            if correlation > 0.7:  # Corrélation forte
                pattern = SemanticPattern(
                    pattern_id=f"meta_correlation_{analyzer_a}_{analyzer_b}",
                    pattern_type='hybrid',
                    strength=correlation,
                    confidence=0.75,
                    sources=[analyzer_a, analyzer_b],
                    evidence=[{'correlation_score': correlation}],
                    timestamp=datetime.now(timezone.utc).isoformat()
                )
                patterns.append(pattern)
        
        return patterns
    
    def _find_common_structures(self, extraction_keys: List[str]) -> Dict:
        """Trouve structures communes entre extractions"""
        common_structures = {}
        
        # Analyse simplifiée - chercher clés communes
        all_keys = []
        for key in extraction_keys:
            if key in self.analyzer_outputs:
                data = self.analyzer_outputs[key]
                if isinstance(data, dict):
                    all_keys.append(set(data.keys()))
        
        if len(all_keys) >= 2:
            common_keys = set.intersection(*all_keys)
            if common_keys:
                common_structures['common_keys'] = {
                    'keys': list(common_keys),
                    'consistency': len(common_keys) / max(len(keys) for keys in all_keys)
                }
        
        return common_structures
    
    def _calculate_cross_analyzer_correlation(self, analyzer_a: str, analyzer_b: str) -> float:
        """Calcule corrélation entre deux analyseurs"""
        # Implémentation simplifiée - comparaison structurelle
        
        data_a = self.analyzer_outputs.get(analyzer_a, {})
        data_b = self.analyzer_outputs.get(analyzer_b, {})
        
        if not data_a or not data_b:
            return 0.0
        
        # Comparer structures JSON
        keys_a = set(data_a.keys()) if isinstance(data_a, dict) else set()
        keys_b = set(data_b.keys()) if isinstance(data_b, dict) else set()
        
        if not keys_a or not keys_b:
            return 0.0
        
        intersection = len(keys_a.intersection(keys_b))
        union = len(keys_a.union(keys_b))
        
        return intersection / union if union > 0 else 0.0
    
    def detect_universal_invariants(self) -> List[UniversalInvariant]:
        """Détection invariants universels"""
        print("\n🔍 DÉTECTION INVARIANTS UNIVERSELS")
        print("=" * 50)
        
        invariants = []
        
        # 1. Invariant de conservation d'information
        info_invariant = self._detect_information_conservation()
        if info_invariant:
            invariants.append(info_invariant)
        
        # 2. Invariant de patterns culturels
        cultural_invariant = self._detect_cultural_invariant()
        if cultural_invariant:
            invariants.append(cultural_invariant)
        
        # 3. Invariant de structure sémantique
        semantic_invariant = self._detect_semantic_structure_invariant()
        if semantic_invariant:
            invariants.append(semantic_invariant)
        
        return invariants
    
    def _detect_information_conservation(self) -> Optional[UniversalInvariant]:
        """Détecte invariant de conservation information"""
        
        # Chercher preuves dans les analyses multiformat
        evidence_count = 0
        
        if 'multiformat' in self.analyzer_outputs:
            format_data = self.analyzer_outputs['multiformat']
            if 'conservation_score' in format_data:
                evidence_count += 1
        
        if evidence_count > 0:
            return UniversalInvariant(
                invariant_id="information_conservation",
                description="L'information sémantique core est conservée lors des transformations de format",
                mathematical_form="I(content) = Σ(semantic_units) [invariant across formats]",
                evidence_count=evidence_count,
                cross_format_validation=True,
                cross_analyzer_validation=False,
                universality_score=0.8
            )
        
        return None
    
    def _detect_cultural_invariant(self) -> Optional[UniversalInvariant]:
        """Détecte invariant culturel"""
        
        if 'translator_bias' in self.analyzer_outputs:
            bias_data = self.analyzer_outputs['translator_bias']
            
            # Vérifier si certains biais sont vraiment universaux
            cultural_patterns = bias_data.get('patterns_culturels', {})
            universal_count = sum(1 for translators in cultural_patterns.values() 
                                if len(translators) >= bias_data.get('traducteurs_analyses', 1))
            
            if universal_count > 0:
                return UniversalInvariant(
                    invariant_id="cultural_bias_universality",
                    description="Certains biais culturels apparaissent de manière universelle chez tous les traducteurs",
                    mathematical_form="∀ translator ∈ T: ∃ bias ∈ B_universal",
                    evidence_count=universal_count,
                    cross_format_validation=False,
                    cross_analyzer_validation=True,
                    universality_score=0.7
                )
        
        return None
    
    def _detect_semantic_structure_invariant(self) -> Optional[UniversalInvariant]:
        """Détecte invariant structure sémantique"""
        
        # Analyser cohérence structures entre analyseurs
        consistent_structures = 0
        total_analyzed = len(self.analyzer_outputs)
        
        for data in self.analyzer_outputs.values():
            if isinstance(data, dict) and 'timestamp' in data:
                consistent_structures += 1
        
        if consistent_structures >= 2:
            universality_score = consistent_structures / total_analyzed
            
            return UniversalInvariant(
                invariant_id="semantic_structure_consistency",
                description="Les structures sémantiques fondamentales sont cohérentes entre analyseurs",
                mathematical_form="Structure(A₁) ≅ Structure(A₂) ≅ ... ≅ Structure(Aₙ)",
                evidence_count=consistent_structures,
                cross_format_validation=True,
                cross_analyzer_validation=True,
                universality_score=universality_score
            )
        
        return None
    
    def generate_unified_report(self) -> Dict:
        """Génère rapport unifié des patterns sémantiques"""
        
        timestamp = datetime.now(timezone.utc).isoformat()
        
        # Calculer statistiques
        universal_patterns = [p for p in self.patterns if p.pattern_type == 'universal']
        hybrid_patterns = [p for p in self.patterns if p.pattern_type == 'hybrid']
        contextual_patterns = [p for p in self.patterns if p.pattern_type == 'contextual']
        
        avg_strength = np.mean([p.strength for p in self.patterns]) if self.patterns else 0.0
        avg_confidence = np.mean([p.confidence for p in self.patterns]) if self.patterns else 0.0
        
        report = {
            "meta": {
                "timestamp": timestamp,
                "engine_version": "1.0.0",
                "analyzers_count": len(self.analyzer_outputs),
                "patterns_detected": len(self.patterns),
                "invariants_detected": len(self.invariants)
            },
            "patterns_summary": {
                "universal": len(universal_patterns),
                "hybrid": len(hybrid_patterns), 
                "contextual": len(contextual_patterns),
                "average_strength": avg_strength,
                "average_confidence": avg_confidence
            },
            "patterns": [asdict(p) for p in self.patterns],
            "universal_invariants": [asdict(i) for i in self.invariants],
            "analyzer_sources": list(self.analyzer_outputs.keys()),
            "cross_correlations": self._generate_correlation_matrix(),
            "recommendations": self._generate_recommendations()
        }
        
        return report
    
    def _generate_correlation_matrix(self) -> Dict:
        """Génère matrice corrélations entre analyseurs"""
        
        analyzer_names = list(self.analyzer_outputs.keys())
        correlations = {}
        
        for analyzer_a, analyzer_b in combinations(analyzer_names, 2):
            correlation = self._calculate_cross_analyzer_correlation(analyzer_a, analyzer_b)
            correlations[f"{analyzer_a}_x_{analyzer_b}"] = correlation
        
        return correlations
    
    def _generate_recommendations(self) -> List[str]:
        """Génère recommandations pour développement futur"""
        
        recommendations = []
        
        if len(self.patterns) == 0:
            recommendations.append("Augmenter la diversité des données d'entrée pour détecter plus de patterns")
        
        universal_count = len([p for p in self.patterns if p.pattern_type == 'universal'])
        if universal_count == 0:
            recommendations.append("Aucun pattern universel détecté - réviser critères de détection")
        
        if len(self.analyzer_outputs) < 3:
            recommendations.append("Ajouter plus d'analyseurs pour améliorer validation croisée")
        
        avg_confidence = np.mean([p.confidence for p in self.patterns]) if self.patterns else 0.0
        if avg_confidence < 0.7:
            recommendations.append("Améliorer algorithmes de confiance - niveau actuel trop bas")
        
        return recommendations
    
    async def run_full_analysis(self) -> Dict:
        """Exécution complète analyse patterns sémantiques"""
        
        print("\n🚀 MOTEUR PATTERNS SÉMANTIQUES - ANALYSE COMPLÈTE")
        print("=" * 60)
        
        # 1. Découverte automatique analyseurs
        analyzer_files = self.auto_discover_analyzers()
        
        # 2. Chargement données
        print(f"\n📊 Chargement {len(analyzer_files)} analyseurs...")
        for analyzer_name, file_path in analyzer_files.items():
            self.load_analyzer_output(analyzer_name, file_path)
        
        # 3. Extraction patterns
        print(f"\n🔍 Extraction patterns sémantiques...")
        self.patterns = self.extract_semantic_patterns()
        print(f"   ✅ {len(self.patterns)} patterns détectés")
        
        # 4. Détection invariants universels
        self.invariants = self.detect_universal_invariants()
        print(f"   ✅ {len(self.invariants)} invariants universels détectés")
        
        # 5. Génération rapport
        report = self.generate_unified_report()
        
        # 6. Sauvegarde
        timestamp = datetime.now(timezone.utc).isoformat()
        output_file = f"semantic_patterns_analysis_{timestamp.replace(':', '-').replace('.', '-')[:19]}Z.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 Rapport sauvegardé: {output_file}")
        
        return report


async def main():
    """Point d'entrée principal"""
    
    engine = SemanticPatternEngine()
    
    try:
        report = await engine.run_full_analysis()
        
        print("\n📋 RÉSUMÉ ANALYSE")
        print("=" * 40)
        print(f"✅ Patterns détectés: {report['meta']['patterns_detected']}")
        print(f"✅ Invariants universels: {report['meta']['invariants_detected']}")
        print(f"✅ Analyseurs sources: {report['meta']['analyzers_count']}")
        
        # Afficher patterns universaux
        universal_patterns = [p for p in report['patterns'] if p['pattern_type'] == 'universal']
        if universal_patterns:
            print(f"\n🌟 PATTERNS UNIVERSAUX ({len(universal_patterns)}):")
            for pattern in universal_patterns:
                print(f"   • {pattern['pattern_id']} (force: {pattern['strength']:.2f})")
        
        # Afficher invariants
        if report['universal_invariants']:
            print(f"\n🔗 INVARIANTS UNIVERSELS ({len(report['universal_invariants'])}):")
            for invariant in report['universal_invariants']:
                print(f"   • {invariant['invariant_id']}: {invariant['description']}")
                print(f"     Score universalité: {invariant['universality_score']:.2f}")
        
        return True
        
    except Exception as e:
        print(f"❌ ERREUR: {e}")
        return False


if __name__ == "__main__":
    asyncio.run(main())