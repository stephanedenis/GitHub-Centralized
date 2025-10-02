#!/usr/bin/env python3
"""
Analyseur de Cohérence Sémantique Cross-Domain
===============================================

Analyse la cohérence sémantique entre différents domaines:
- Traductions vs Sources originales
- Formats différents d'un même contenu  
- Versions temporelles d'un document
- Contextes culturels multiples

Objectif: Détecter invariants sémantiques et violations de cohérence.

Date: 2025-10-02
Auteur: Système Autonome PaniniFS
Version: 1.0.0
"""

import sys
import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Set, Optional, Tuple
from collections import defaultdict, Counter
from dataclasses import dataclass, asdict
import re
from difflib import SequenceMatcher
import numpy as np


@dataclass
class CoherenceViolation:
    """Violation de cohérence détectée"""
    violation_id: str
    violation_type: str
    severity: str  # 'low', 'medium', 'high', 'critical'
    domains: List[str]
    description: str
    evidence: Dict
    confidence: float
    timestamp: str


@dataclass
class SemanticInvariant:
    """Invariant sémantique validé"""
    invariant_id: str
    domains: List[str] 
    preservation_rate: float  # 0.0-1.0
    mathematical_form: Optional[str]
    validation_count: int
    counterexamples: List[Dict]


class SemanticCoherenceAnalyzer:
    """Analyseur cohérence sémantique cross-domain"""
    
    def __init__(self):
        self.domains = {}
        self.coherence_violations = []
        self.semantic_invariants = []
        self.similarity_threshold = 0.7
        
    def load_domain_data(self, domain_name: str, data_path: Path) -> bool:
        """Charge données d'un domaine spécifique"""
        try:
            with open(data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.domains[domain_name] = {
                'data': data,
                'path': data_path,
                'loaded_at': datetime.now(timezone.utc).isoformat()
            }
            
            print(f"✅ Domaine '{domain_name}' chargé: {data_path.name}")
            return True
            
        except Exception as e:
            print(f"❌ Erreur chargement domaine '{domain_name}': {e}")
            return False
    
    def auto_discover_domains(self) -> Dict[str, Path]:
        """Découverte automatique des domaines dans le workspace"""
        print("\n🔍 DÉCOUVERTE AUTOMATIQUE DOMAINES")
        print("=" * 45)
        
        current_dir = Path('.')
        domains = {}
        
        # Mapping patterns -> domaines sémantiques
        domain_patterns = {
            'translations': ['*translator*', '*translation*', '*bias*'],
            'extractions': ['*extract*', '*content*'],
            'formats': ['*multiformat*', '*format*'],
            'compressions': ['*compress*', '*benchmark*'],
            'projects': ['*project*', '*essence*'],
            'validations': ['*validation*', '*corpus*'],
            'analyses': ['*analy*', '*patterns*']
        }
        
        for domain_name, patterns in domain_patterns.items():
            domain_files = []
            for pattern in patterns:
                files = list(current_dir.glob(f"{pattern}.json"))
                domain_files.extend(files)
            
            if domain_files:
                # Prendre le plus récent pour ce domaine
                latest = max(domain_files, key=lambda f: f.stat().st_mtime)
                domains[domain_name] = latest
                print(f"  • {domain_name}: {latest.name}")
        
        return domains
    
    def analyze_cross_domain_coherence(self) -> List[CoherenceViolation]:
        """Analyse cohérence entre domaines"""
        print("\n🔍 ANALYSE COHÉRENCE CROSS-DOMAIN")
        print("=" * 45)
        
        violations = []
        domain_names = list(self.domains.keys())
        
        # Analyser toutes les paires de domaines
        for i, domain_a in enumerate(domain_names):
            for domain_b in domain_names[i+1:]:
                print(f"\n  Comparaison: {domain_a} ↔ {domain_b}")
                
                domain_violations = self._compare_domains(domain_a, domain_b)
                violations.extend(domain_violations)
        
        return violations
    
    def _compare_domains(self, domain_a: str, domain_b: str) -> List[CoherenceViolation]:
        """Compare deux domaines pour violations cohérence"""
        violations = []
        
        data_a = self.domains[domain_a]['data']
        data_b = self.domains[domain_b]['data']
        
        # 1. Cohérence temporelle
        temporal_violations = self._check_temporal_coherence(domain_a, domain_b, data_a, data_b)
        violations.extend(temporal_violations)
        
        # 2. Cohérence structurelle
        structural_violations = self._check_structural_coherence(domain_a, domain_b, data_a, data_b)
        violations.extend(structural_violations)
        
        # 3. Cohérence sémantique
        semantic_violations = self._check_semantic_coherence(domain_a, domain_b, data_a, data_b)
        violations.extend(semantic_violations)
        
        # 4. Cohérence quantitative
        quantitative_violations = self._check_quantitative_coherence(domain_a, domain_b, data_a, data_b)
        violations.extend(quantitative_violations)
        
        return violations
    
    def _check_temporal_coherence(self, domain_a: str, domain_b: str, 
                                 data_a: Dict, data_b: Dict) -> List[CoherenceViolation]:
        """Vérifie cohérence temporelle"""
        violations = []
        
        timestamp_a = data_a.get('timestamp', '')
        timestamp_b = data_b.get('timestamp', '')
        
        if timestamp_a and timestamp_b:
            try:
                time_a = datetime.fromisoformat(timestamp_a.replace('Z', '+00:00'))
                time_b = datetime.fromisoformat(timestamp_b.replace('Z', '+00:00'))
                
                time_diff = abs((time_a - time_b).total_seconds())
                
                # Si écart > 24h, c'est suspect pour des données liées
                if time_diff > 24 * 3600:
                    violation = CoherenceViolation(
                        violation_id=f"temporal_{domain_a}_{domain_b}",
                        violation_type="temporal_inconsistency",
                        severity="medium",
                        domains=[domain_a, domain_b],
                        description=f"Écart temporel important: {time_diff/3600:.1f}h",
                        evidence={
                            'timestamp_a': timestamp_a,
                            'timestamp_b': timestamp_b,
                            'time_diff_hours': time_diff/3600
                        },
                        confidence=0.8,
                        timestamp=datetime.now(timezone.utc).isoformat()
                    )
                    violations.append(violation)
                    
            except Exception as e:
                # Erreur parsing timestamps
                violation = CoherenceViolation(
                    violation_id=f"temporal_parse_{domain_a}_{domain_b}",
                    violation_type="temporal_parse_error", 
                    severity="low",
                    domains=[domain_a, domain_b],
                    description=f"Impossible de parser timestamps: {e}",
                    evidence={'error': str(e)},
                    confidence=0.9,
                    timestamp=datetime.now(timezone.utc).isoformat()
                )
                violations.append(violation)
        
        return violations
    
    def _check_structural_coherence(self, domain_a: str, domain_b: str,
                                   data_a: Dict, data_b: Dict) -> List[CoherenceViolation]:
        """Vérifie cohérence structurelle"""
        violations = []
        
        # Comparer structures JSON
        keys_a = set(data_a.keys()) if isinstance(data_a, dict) else set()
        keys_b = set(data_b.keys()) if isinstance(data_b, dict) else set()
        
        if keys_a and keys_b:
            intersection = keys_a.intersection(keys_b)
            union = keys_a.union(keys_b)
            
            similarity = len(intersection) / len(union) if union else 0.0
            
            # Si similarité structurelle très faible, c'est suspect
            if similarity < 0.1:
                violation = CoherenceViolation(
                    violation_id=f"structural_{domain_a}_{domain_b}",
                    violation_type="structural_divergence",
                    severity="high",
                    domains=[domain_a, domain_b],
                    description=f"Structures très différentes: {similarity:.2f} similarité",
                    evidence={
                        'keys_a': list(keys_a),
                        'keys_b': list(keys_b),
                        'similarity': similarity,
                        'common_keys': list(intersection)
                    },
                    confidence=0.85,
                    timestamp=datetime.now(timezone.utc).isoformat()
                )
                violations.append(violation)
        
        return violations
    
    def _check_semantic_coherence(self, domain_a: str, domain_b: str,
                                 data_a: Dict, data_b: Dict) -> List[CoherenceViolation]:
        """Vérifie cohérence sémantique"""
        violations = []
        
        # Chercher champs textuels pour comparaison sémantique
        text_fields_a = self._extract_text_fields(data_a)
        text_fields_b = self._extract_text_fields(data_b)
        
        if text_fields_a and text_fields_b:
            semantic_similarity = self._calculate_semantic_similarity(text_fields_a, text_fields_b)
            
            # Si contenu sémantiquement incohérent
            if semantic_similarity < 0.3:
                violation = CoherenceViolation(
                    violation_id=f"semantic_{domain_a}_{domain_b}",
                    violation_type="semantic_incoherence",
                    severity="medium",
                    domains=[domain_a, domain_b],
                    description=f"Faible cohérence sémantique: {semantic_similarity:.2f}",
                    evidence={
                        'semantic_similarity': semantic_similarity,
                        'sample_text_a': text_fields_a[:200],
                        'sample_text_b': text_fields_b[:200]
                    },
                    confidence=0.7,
                    timestamp=datetime.now(timezone.utc).isoformat()
                )
                violations.append(violation)
        
        return violations
    
    def _check_quantitative_coherence(self, domain_a: str, domain_b: str,
                                     data_a: Dict, data_b: Dict) -> List[CoherenceViolation]:
        """Vérifie cohérence quantitative"""
        violations = []
        
        # Chercher métriques numériques communes
        numeric_a = self._extract_numeric_metrics(data_a)
        numeric_b = self._extract_numeric_metrics(data_b)
        
        common_metrics = set(numeric_a.keys()).intersection(set(numeric_b.keys()))
        
        for metric in common_metrics:
            value_a = numeric_a[metric]
            value_b = numeric_b[metric]
            
            if value_a != 0:
                relative_diff = abs(value_a - value_b) / abs(value_a)
                
                # Si différence relative > 50%, c'est suspect
                if relative_diff > 0.5:
                    violation = CoherenceViolation(
                        violation_id=f"quantitative_{metric}_{domain_a}_{domain_b}",
                        violation_type="quantitative_divergence",
                        severity="medium",
                        domains=[domain_a, domain_b],
                        description=f"Divergence métrique '{metric}': {relative_diff:.1%}",
                        evidence={
                            'metric': metric,
                            'value_a': value_a,
                            'value_b': value_b,
                            'relative_difference': relative_diff
                        },
                        confidence=0.8,
                        timestamp=datetime.now(timezone.utc).isoformat()
                    )
                    violations.append(violation)
        
        return violations
    
    def _extract_text_fields(self, data: Dict, max_length: int = 1000) -> str:
        """Extrait champs textuels d'une structure de données"""
        texts = []
        
        def extract_recursive(obj, depth=0):
            if depth > 5:  # Éviter récursion infinie
                return
                
            if isinstance(obj, str):
                if len(obj) > 10:  # Ignorer strings courtes (IDs, etc.)
                    texts.append(obj)
            elif isinstance(obj, dict):
                for value in obj.values():
                    extract_recursive(value, depth + 1)
            elif isinstance(obj, list):
                for item in obj:
                    extract_recursive(item, depth + 1)
        
        extract_recursive(data)
        combined_text = ' '.join(texts)
        
        return combined_text[:max_length] if combined_text else ""
    
    def _extract_numeric_metrics(self, data: Dict) -> Dict[str, float]:
        """Extrait métriques numériques d'une structure"""
        metrics = {}
        
        def extract_recursive(obj, path="", depth=0):
            if depth > 5:
                return
                
            if isinstance(obj, (int, float)):
                metrics[path] = float(obj)
            elif isinstance(obj, dict):
                for key, value in obj.items():
                    new_path = f"{path}.{key}" if path else key
                    extract_recursive(value, new_path, depth + 1)
            elif isinstance(obj, list) and obj and isinstance(obj[0], (int, float)):
                # Liste de nombres -> prendre moyenne
                avg_val = sum(obj) / len(obj)
                metrics[f"{path}.avg"] = avg_val
        
        extract_recursive(data)
        return metrics
    
    def _calculate_semantic_similarity(self, text_a: str, text_b: str) -> float:
        """Calcule similarité sémantique simple entre deux textes"""
        
        if not text_a or not text_b:
            return 0.0
        
        # Normalisation basique
        text_a = re.sub(r'[^\w\s]', '', text_a.lower())
        text_b = re.sub(r'[^\w\s]', '', text_b.lower())
        
        # Similarité basée sur mots communs
        words_a = set(text_a.split())
        words_b = set(text_b.split())
        
        if not words_a or not words_b:
            return 0.0
        
        intersection = len(words_a.intersection(words_b))
        union = len(words_a.union(words_b))
        
        jaccard_similarity = intersection / union if union else 0.0
        
        # Similarité séquentielle
        sequence_similarity = SequenceMatcher(None, text_a, text_b).ratio()
        
        # Moyenne pondérée
        return 0.6 * jaccard_similarity + 0.4 * sequence_similarity
    
    def detect_semantic_invariants(self) -> List[SemanticInvariant]:
        """Détecte invariants sémantiques cross-domain"""
        print("\n🔗 DÉTECTION INVARIANTS SÉMANTIQUES")
        print("=" * 45)
        
        invariants = []
        
        # 1. Invariant de préservation temporelle
        temporal_invariant = self._detect_temporal_invariant()
        if temporal_invariant:
            invariants.append(temporal_invariant)
        
        # 2. Invariant de préservation structurelle
        structural_invariant = self._detect_structural_invariant()
        if structural_invariant:
            invariants.append(structural_invariant)
        
        # 3. Invariant de conservation sémantique
        semantic_invariant = self._detect_semantic_conservation_invariant()
        if semantic_invariant:
            invariants.append(semantic_invariant)
        
        return invariants
    
    def _detect_temporal_invariant(self) -> Optional[SemanticInvariant]:
        """Détecte invariant de préservation temporelle"""
        
        timestamps = []
        for domain_name, domain_info in self.domains.items():
            timestamp = domain_info['data'].get('timestamp')
            if timestamp:
                timestamps.append(timestamp)
        
        if len(timestamps) >= 2:
            # Calculer cohérence temporelle
            coherent_pairs = 0
            total_pairs = 0
            
            for i, ts_a in enumerate(timestamps):
                for ts_b in timestamps[i+1:]:
                    total_pairs += 1
                    try:
                        time_a = datetime.fromisoformat(ts_a.replace('Z', '+00:00'))
                        time_b = datetime.fromisoformat(ts_b.replace('Z', '+00:00'))
                        
                        time_diff = abs((time_a - time_b).total_seconds())
                        
                        # Si écart < 6h, considéré cohérent
                        if time_diff < 6 * 3600:
                            coherent_pairs += 1
                    except:
                        pass
            
            preservation_rate = coherent_pairs / total_pairs if total_pairs else 0.0
            
            if preservation_rate > 0.5:
                return SemanticInvariant(
                    invariant_id="temporal_preservation",
                    domains=list(self.domains.keys()),
                    preservation_rate=preservation_rate,
                    mathematical_form="∀ (domain_i, domain_j): |timestamp_i - timestamp_j| < δ_temporal",
                    validation_count=coherent_pairs,
                    counterexamples=[]
                )
        
        return None
    
    def _detect_structural_invariant(self) -> Optional[SemanticInvariant]:
        """Détecte invariant de préservation structurelle"""
        
        if len(self.domains) < 2:
            return None
        
        # Analyser structures communes
        all_structures = []
        for domain_name, domain_info in self.domains.items():
            data = domain_info['data']
            if isinstance(data, dict):
                all_structures.append(set(data.keys()))
        
        if len(all_structures) >= 2:
            # Calculer intersection moyenne
            total_similarity = 0.0
            pairs = 0
            
            for i, struct_a in enumerate(all_structures):
                for struct_b in all_structures[i+1:]:
                    pairs += 1
                    if struct_a or struct_b:
                        intersection = len(struct_a.intersection(struct_b))
                        union = len(struct_a.union(struct_b))
                        similarity = intersection / union if union else 0.0
                        total_similarity += similarity
            
            avg_similarity = total_similarity / pairs if pairs else 0.0
            
            if avg_similarity > 0.3:
                return SemanticInvariant(
                    invariant_id="structural_preservation",
                    domains=list(self.domains.keys()),
                    preservation_rate=avg_similarity,
                    mathematical_form="∀ (struct_i, struct_j): similarity(struct_i, struct_j) > θ_structural",
                    validation_count=pairs,
                    counterexamples=[]
                )
        
        return None
    
    def _detect_semantic_conservation_invariant(self) -> Optional[SemanticInvariant]:
        """Détecte invariant de conservation sémantique"""
        
        # Analyser cohérence sémantique globale
        semantic_coherences = []
        domain_names = list(self.domains.keys())
        
        for i, domain_a in enumerate(domain_names):
            for domain_b in domain_names[i+1:]:
                data_a = self.domains[domain_a]['data']
                data_b = self.domains[domain_b]['data']
                
                text_a = self._extract_text_fields(data_a)
                text_b = self._extract_text_fields(data_b)
                
                if text_a and text_b:
                    similarity = self._calculate_semantic_similarity(text_a, text_b)
                    semantic_coherences.append(similarity)
        
        if semantic_coherences:
            avg_coherence = sum(semantic_coherences) / len(semantic_coherences)
            
            if avg_coherence > 0.4:
                return SemanticInvariant(
                    invariant_id="semantic_conservation",
                    domains=list(self.domains.keys()),
                    preservation_rate=avg_coherence,
                    mathematical_form="∀ (content_i, content_j): semantic_similarity(content_i, content_j) > θ_semantic",
                    validation_count=len(semantic_coherences),
                    counterexamples=[]
                )
        
        return None
    
    def generate_coherence_report(self) -> Dict:
        """Génère rapport complet de cohérence"""
        
        timestamp = datetime.now(timezone.utc).isoformat()
        
        # Statistiques violations
        violation_types = Counter([v.violation_type for v in self.coherence_violations])
        severity_counts = Counter([v.severity for v in self.coherence_violations])
        
        # Statistiques invariants
        invariant_rates = [inv.preservation_rate for inv in self.semantic_invariants]
        avg_preservation = sum(invariant_rates) / len(invariant_rates) if invariant_rates else 0.0
        
        report = {
            "meta": {
                "timestamp": timestamp,
                "analyzer_version": "1.0.0",
                "domains_analyzed": len(self.domains),
                "violations_detected": len(self.coherence_violations),
                "invariants_detected": len(self.semantic_invariants)
            },
            "domains": {
                name: {
                    "file": str(info['path']),
                    "loaded_at": info['loaded_at']
                }
                for name, info in self.domains.items()
            },
            "coherence_violations": [asdict(v) for v in self.coherence_violations],
            "semantic_invariants": [asdict(inv) for inv in self.semantic_invariants],
            "statistics": {
                "violation_types": dict(violation_types),
                "severity_distribution": dict(severity_counts),
                "average_preservation_rate": avg_preservation,
                "coherence_score": max(0.0, 1.0 - len(self.coherence_violations) / max(1, len(self.domains)**2))
            },
            "recommendations": self._generate_coherence_recommendations()
        }
        
        return report
    
    def _generate_coherence_recommendations(self) -> List[str]:
        """Génère recommandations pour améliorer cohérence"""
        
        recommendations = []
        
        # Analyser patterns violations
        if self.coherence_violations:
            critical_violations = [v for v in self.coherence_violations if v.severity == 'critical']
            if critical_violations:
                recommendations.append(f"Résoudre {len(critical_violations)} violations critiques en priorité")
            
            temporal_violations = [v for v in self.coherence_violations if v.violation_type.startswith('temporal')]
            if temporal_violations:
                recommendations.append("Synchroniser les timestamps entre domaines")
            
            structural_violations = [v for v in self.coherence_violations if v.violation_type.startswith('structural')]
            if structural_violations:
                recommendations.append("Harmoniser les structures de données entre domaines")
        
        # Analyser preservation rates
        if self.semantic_invariants:
            low_preservation = [inv for inv in self.semantic_invariants if inv.preservation_rate < 0.5]
            if low_preservation:
                recommendations.append("Améliorer préservation sémantique - taux actuels insuffisants")
        
        if len(self.domains) < 3:
            recommendations.append("Ajouter plus de domaines pour analyse plus robuste")
        
        return recommendations
    
    async def run_full_coherence_analysis(self) -> Dict:
        """Exécution complète analyse cohérence"""
        
        print("\n🔍 ANALYSEUR COHÉRENCE SÉMANTIQUE - ANALYSE COMPLÈTE")
        print("=" * 65)
        
        # 1. Découverte domaines
        domain_files = self.auto_discover_domains()
        
        # 2. Chargement domaines
        print(f"\n📊 Chargement {len(domain_files)} domaines...")
        for domain_name, file_path in domain_files.items():
            self.load_domain_data(domain_name, file_path)
        
        # 3. Analyse cohérence
        print(f"\n🔍 Analyse cohérence cross-domain...")
        self.coherence_violations = self.analyze_cross_domain_coherence()
        print(f"   ⚠️  {len(self.coherence_violations)} violations détectées")
        
        # 4. Détection invariants
        self.semantic_invariants = self.detect_semantic_invariants()
        print(f"   ✅ {len(self.semantic_invariants)} invariants détectés")
        
        # 5. Génération rapport
        report = self.generate_coherence_report()
        
        # 6. Sauvegarde
        timestamp = datetime.now(timezone.utc).isoformat()
        output_file = f"semantic_coherence_analysis_{timestamp.replace(':', '-').replace('.', '-')[:19]}Z.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 Rapport sauvegardé: {output_file}")
        
        return report


async def main():
    """Point d'entrée principal"""
    
    analyzer = SemanticCoherenceAnalyzer()
    
    try:
        report = await analyzer.run_full_coherence_analysis()
        
        print("\n📋 RÉSUMÉ COHÉRENCE")
        print("=" * 40)
        print(f"✅ Domaines analysés: {report['meta']['domains_analyzed']}")
        print(f"⚠️  Violations détectées: {report['meta']['violations_detected']}")
        print(f"✅ Invariants détectés: {report['meta']['invariants_detected']}")
        print(f"📊 Score cohérence: {report['statistics']['coherence_score']:.2f}")
        
        # Afficher violations critiques
        critical_violations = [v for v in analyzer.coherence_violations if v.severity == 'critical']
        if critical_violations:
            print(f"\n🚨 VIOLATIONS CRITIQUES ({len(critical_violations)}):")
            for violation in critical_violations:
                print(f"   • {violation.violation_id}: {violation.description}")
        
        # Afficher invariants
        if analyzer.semantic_invariants:
            print(f"\n🔗 INVARIANTS SÉMANTIQUES ({len(analyzer.semantic_invariants)}):")
            for invariant in analyzer.semantic_invariants:
                print(f"   • {invariant.invariant_id}: {invariant.preservation_rate:.2f} préservation")
        
        return True
        
    except Exception as e:
        print(f"❌ ERREUR: {e}")
        return False


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())