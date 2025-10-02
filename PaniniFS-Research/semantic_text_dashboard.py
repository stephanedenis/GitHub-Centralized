#!/usr/bin/env python3
"""
Dashboard Sémantique Unifié - Version Text
==========================================

Dashboard textuel des analyses sémantiques sans dépendances matplotlib.

Date: 2025-10-02
Auteur: Système Autonome PaniniFS
Version: 1.0.0
"""

import json
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Any
from collections import Counter, defaultdict


class SemanticTextDashboard:
    """Dashboard sémantique textuel"""
    
    def __init__(self):
        self.orchestration_data = None
        self.pattern_data = None
        self.coherence_data = None
        self.translator_data = None
        
    def load_latest_orchestration(self) -> bool:
        """Charge le dernier rapport d'orchestration"""
        orchestration_files = list(Path('.').glob('*semantic_orchestration*.json'))
        
        if not orchestration_files:
            print("❌ Aucun rapport d'orchestration trouvé")
            return False
        
        latest = max(orchestration_files, key=lambda f: f.stat().st_mtime)
        
        try:
            with open(latest, 'r', encoding='utf-8') as f:
                self.orchestration_data = json.load(f)
            print(f"✅ Orchestration chargée: {latest.name}")
            return True
        except Exception as e:
            print(f"❌ Erreur chargement orchestration: {e}")
            return False
    
    def load_supporting_data(self):
        """Charge données de support des autres analyseurs"""
        
        # Patterns sémantiques
        pattern_files = list(Path('.').glob('*semantic_patterns_analysis*.json'))
        if pattern_files:
            latest_pattern = max(pattern_files, key=lambda f: f.stat().st_mtime)
            try:
                with open(latest_pattern, 'r', encoding='utf-8') as f:
                    self.pattern_data = json.load(f)
                print(f"✅ Patterns chargés: {latest_pattern.name}")
            except:
                pass
        
        # Cohérence sémantique
        coherence_files = list(Path('.').glob('*semantic_coherence_analysis*.json'))
        if coherence_files:
            latest_coherence = max(coherence_files, key=lambda f: f.stat().st_mtime)
            try:
                with open(latest_coherence, 'r', encoding='utf-8') as f:
                    self.coherence_data = json.load(f)
                print(f"✅ Cohérence chargée: {latest_coherence.name}")
            except:
                pass
        
        # Biais traducteurs
        translator_files = list(Path('.').glob('*translator_bias*.json'))
        if translator_files:
            latest_translator = max(translator_files, key=lambda f: f.stat().st_mtime)
            try:
                with open(latest_translator, 'r', encoding='utf-8') as f:
                    self.translator_data = json.load(f)
                print(f"✅ Biais traducteurs chargés: {latest_translator.name}")
            except:
                pass
    
    def display_orchestration_overview(self):
        """Affiche vue d'ensemble orchestration"""
        
        print("\n" + "="*60)
        print("📊 VUE D'ENSEMBLE ORCHESTRATION")
        print("="*60)
        
        if not self.orchestration_data:
            print("❌ Aucune donnée d'orchestration disponible")
            return
        
        summary = self.orchestration_data['summary']
        
        print(f"🔄 Analyseurs:")
        print(f"   • Total: {summary['total_analyzers']}")
        print(f"   • Succès: {summary['successful_analyzers']} ({summary['successful_analyzers']/summary['total_analyzers']*100:.1f}%)")
        print(f"   • Échecs: {summary['failed_analyzers']} ({summary['failed_analyzers']/summary['total_analyzers']*100:.1f}%)")
        
        print(f"\n⏱️  Performance:")
        print(f"   • Temps total: {summary['total_execution_time']:.2f}s")
        print(f"   • Fichiers générés: {len(summary['output_files'])}")
        
        print(f"\n🔍 Validation croisée:")
        print(f"   • Score: {summary['cross_validation_score']:.3f}")
        
        # Détails par analyseur
        print(f"\n📋 DÉTAILS ANALYSEURS:")
        print("-"*40)
        
        analyzer_results = self.orchestration_data.get('analyzer_results', [])
        for result in analyzer_results:
            status = "✅" if result['success'] else "❌"
            print(f"{status} {result['analyzer_name']:<20} {result['execution_time']:.2f}s")
            if not result['success'] and result.get('error_message'):
                print(f"    Erreur: {result['error_message'][:80]}...")
        
        # Insights
        insights = summary.get('unified_insights', [])
        if insights:
            print(f"\n💡 INSIGHTS UNIFIÉS:")
            for insight in insights:
                print(f"   • {insight}")
    
    def display_patterns_analysis(self):
        """Affiche analyse patterns"""
        
        print("\n" + "="*60)
        print("🧠 ANALYSE PATTERNS SÉMANTIQUES")
        print("="*60)
        
        if not self.pattern_data:
            print("❌ Aucune donnée de patterns disponible")
            return
        
        patterns = self.pattern_data.get('patterns', [])
        invariants = self.pattern_data.get('universal_invariants', [])
        
        print(f"📊 STATISTIQUES GÉNÉRALES:")
        print(f"   • Patterns détectés: {len(patterns)}")
        print(f"   • Invariants universels: {len(invariants)}")
        print(f"   • Analyseurs sources: {self.pattern_data['meta']['analyzers_count']}")
        
        # Patterns par type
        if patterns:
            pattern_types = [p['pattern_type'] for p in patterns]
            type_counts = Counter(pattern_types)
            
            print(f"\n🏷️  PATTERNS PAR TYPE:")
            for pattern_type, count in type_counts.items():
                print(f"   • {pattern_type.capitalize()}: {count}")
            
            # Patterns universaux
            universal_patterns = [p for p in patterns if p['pattern_type'] == 'universal']
            if universal_patterns:
                print(f"\n🌟 PATTERNS UNIVERSAUX ({len(universal_patterns)}):")
                for pattern in universal_patterns:
                    print(f"   • {pattern['pattern_id']}")
                    print(f"     Force: {pattern['strength']:.3f} | Confiance: {pattern['confidence']:.3f}")
                    print(f"     Sources: {', '.join(pattern['sources'])}")
        
        # Invariants universels
        if invariants:
            print(f"\n🔗 INVARIANTS UNIVERSELS ({len(invariants)}):")
            for invariant in invariants:
                print(f"   • {invariant['invariant_id']}")
                print(f"     Description: {invariant['description']}")
                print(f"     Score universalité: {invariant['universality_score']:.3f}")
                if invariant.get('mathematical_form'):
                    print(f"     Forme: {invariant['mathematical_form']}")
    
    def display_coherence_analysis(self):
        """Affiche analyse cohérence"""
        
        print("\n" + "="*60)
        print("🔍 ANALYSE COHÉRENCE SÉMANTIQUE")
        print("="*60)
        
        if not self.coherence_data:
            print("❌ Aucune donnée de cohérence disponible")
            return
        
        stats = self.coherence_data.get('statistics', {})
        violations = self.coherence_data.get('coherence_violations', [])
        invariants = self.coherence_data.get('semantic_invariants', [])
        domains = self.coherence_data.get('domains', {})
        
        print(f"📊 STATISTIQUES GÉNÉRALES:")
        print(f"   • Domaines analysés: {len(domains)}")
        print(f"   • Violations détectées: {len(violations)}")
        print(f"   • Invariants détectés: {len(invariants)}")
        print(f"   • Score cohérence: {stats.get('coherence_score', 0):.3f}")
        
        # Domaines
        print(f"\n🏷️  DOMAINES ANALYSÉS:")
        for domain_name, domain_info in domains.items():
            print(f"   • {domain_name}: {domain_info['file']}")
        
        # Violations par type
        if violations:
            violation_types = [v['violation_type'] for v in violations]
            type_counts = Counter(violation_types)
            
            print(f"\n⚠️  VIOLATIONS PAR TYPE:")
            for vtype, count in type_counts.items():
                print(f"   • {vtype}: {count}")
            
            # Violations par sévérité
            severities = [v['severity'] for v in violations]
            severity_counts = Counter(severities)
            
            print(f"\n🚨 VIOLATIONS PAR SÉVÉRITÉ:")
            severity_order = ['critical', 'high', 'medium', 'low']
            for severity in severity_order:
                if severity in severity_counts:
                    count = severity_counts[severity]
                    emoji = {'critical': '🔴', 'high': '🟠', 'medium': '🟡', 'low': '🟢'}[severity]
                    print(f"   {emoji} {severity.capitalize()}: {count}")
            
            # Top violations
            print(f"\n🔍 TOP VIOLATIONS:")
            sorted_violations = sorted(violations, key=lambda v: v['confidence'], reverse=True)[:5]
            for i, violation in enumerate(sorted_violations, 1):
                print(f"   {i}. {violation['violation_type']} ({violation['severity']})")
                print(f"      Domaines: {', '.join(violation['domains'])}")
                print(f"      Description: {violation['description']}")
                print(f"      Confiance: {violation['confidence']:.3f}")
    
    def display_translator_analysis(self):
        """Affiche analyse traducteurs"""
        
        print("\n" + "="*60)
        print("👥 ANALYSE BIAIS TRADUCTEURS")
        print("="*60)
        
        if not self.translator_data:
            print("❌ Aucune donnée de traducteurs disponible")
            return
        
        print(f"📊 STATISTIQUES GÉNÉRALES:")
        print(f"   • Traducteurs analysés: {self.translator_data.get('traducteurs_analyses', 0)}")
        
        # Patterns culturels
        cultural_patterns = self.translator_data.get('patterns_culturels', {})
        if cultural_patterns:
            print(f"\n🌍 PATTERNS CULTURELS ({len(cultural_patterns)}):")
            for pattern_name, translators in cultural_patterns.items():
                print(f"   • {pattern_name}: {len(translators)} traducteur(s)")
                if len(translators) <= 3:  # Afficher noms si peu
                    print(f"     Traducteurs: {', '.join(translators)}")
        
        # Patterns temporels
        temporal_patterns = self.translator_data.get('patterns_temporels', {})
        if temporal_patterns:
            print(f"\n⏰ PATTERNS TEMPORELS ({len(temporal_patterns)}):")
            for pattern_name, translators in temporal_patterns.items():
                print(f"   • {pattern_name}: {len(translators)} traducteur(s)")
        
        # Signatures stylistiques
        style_signatures = self.translator_data.get('signatures_stylistiques', {})
        if style_signatures:
            print(f"\n✍️  SIGNATURES STYLISTIQUES ({len(style_signatures)}):")
            for signature_name, translators in style_signatures.items():
                print(f"   • {signature_name}: {len(translators)} traducteur(s)")
        
        # Universaux vs contextuels
        universaux = self.translator_data.get('universaux', {})
        contextuels = self.translator_data.get('contextuels', {})
        
        if universaux or contextuels:
            print(f"\n🌐 UNIVERSAUX vs CONTEXTUELS:")
            print(f"   • Patterns universaux: {len(universaux)}")
            print(f"   • Patterns contextuels: {len(contextuels)}")
            
            if universaux:
                print(f"\n🔗 CANDIDATS UNIVERSAUX:")
                for pattern_name, info in universaux.items():
                    print(f"   • {pattern_name}: validation sur {info.get('count', 0)} traducteur(s)")
    
    def generate_executive_summary(self) -> Dict:
        """Génère résumé exécutif"""
        
        timestamp = datetime.now(timezone.utc).isoformat()
        
        # Métriques clés
        total_patterns = 0
        universal_patterns = 0
        total_violations = 0
        critical_violations = 0
        coherence_score = 0.0
        success_rate = 0.0
        
        if self.pattern_data:
            patterns = self.pattern_data.get('patterns', [])
            total_patterns = len(patterns)
            universal_patterns = len([p for p in patterns if p.get('pattern_type') == 'universal'])
        
        if self.coherence_data:
            violations = self.coherence_data.get('coherence_violations', [])
            total_violations = len(violations)
            critical_violations = len([v for v in violations if v.get('severity') == 'critical'])
            coherence_score = self.coherence_data.get('statistics', {}).get('coherence_score', 0.0)
        
        if self.orchestration_data:
            summary = self.orchestration_data['summary']
            success_rate = summary['successful_analyzers'] / summary['total_analyzers']
        
        # Score global
        global_score = self._calculate_global_score()
        
        # Recommandations
        recommendations = self._generate_recommendations()
        
        # Insights clés
        key_insights = self._extract_key_insights()
        
        summary = {
            "meta": {
                "timestamp": timestamp,
                "dashboard_version": "1.0.0 (text)",
                "analysis_scope": "semantic_ecosystem"
            },
            "executive_summary": {
                "global_semantic_score": global_score,
                "analyzer_success_rate": success_rate,
                "patterns_detected": total_patterns,
                "universal_patterns": universal_patterns,
                "coherence_violations": total_violations,
                "critical_violations": critical_violations,
                "coherence_score": coherence_score
            },
            "key_insights": key_insights,
            "recommendations": recommendations,
            "data_completeness": {
                "orchestration": self.orchestration_data is not None,
                "patterns": self.pattern_data is not None,
                "coherence": self.coherence_data is not None,
                "translators": self.translator_data is not None
            }
        }
        
        return summary
    
    def _calculate_global_score(self) -> float:
        """Calcule score global"""
        
        scores = []
        
        # Score orchestration
        if self.orchestration_data:
            summary = self.orchestration_data['summary']
            success_rate = summary['successful_analyzers'] / summary['total_analyzers']
            scores.append(success_rate)
        
        # Score patterns (ratio universaux)
        if self.pattern_data:
            patterns = self.pattern_data.get('patterns', [])
            if patterns:
                universal_count = len([p for p in patterns if p.get('pattern_type') == 'universal'])
                universal_ratio = universal_count / len(patterns)
                scores.append(universal_ratio)
        
        # Score cohérence
        if self.coherence_data:
            coherence_score = self.coherence_data.get('statistics', {}).get('coherence_score', 0.0)
            scores.append(coherence_score)
        
        return sum(scores) / len(scores) if scores else 0.0
    
    def _generate_recommendations(self) -> List[str]:
        """Génère recommandations"""
        
        recommendations = []
        
        # Recommandations orchestration
        if self.orchestration_data:
            failed_analyzers = [r for r in self.orchestration_data.get('analyzer_results', []) if not r['success']]
            if failed_analyzers:
                recommendations.append(f"Réparer {len(failed_analyzers)} analyseurs défaillants")
        
        # Recommandations cohérence
        if self.coherence_data:
            violations = self.coherence_data.get('coherence_violations', [])
            critical = [v for v in violations if v.get('severity') == 'critical']
            if critical:
                recommendations.append(f"Résoudre d'urgence {len(critical)} violations critiques")
        
        # Recommandations patterns
        if self.pattern_data:
            patterns = self.pattern_data.get('patterns', [])
            universal_patterns = [p for p in patterns if p.get('pattern_type') == 'universal']
            if len(universal_patterns) == 0:
                recommendations.append("Aucun pattern universel détecté - réviser méthodologie")
        
        global_score = self._calculate_global_score()
        if global_score < 0.5:
            recommendations.append("Score global faible - audit complet recommandé")
        
        return recommendations
    
    def _extract_key_insights(self) -> List[str]:
        """Extrait insights clés"""
        
        insights = []
        
        # Insight patterns
        if self.pattern_data:
            patterns = self.pattern_data.get('patterns', [])
            universal_patterns = [p for p in patterns if p.get('pattern_type') == 'universal']
            if universal_patterns:
                insights.append(f"Base solide: {len(universal_patterns)} patterns universaux validés")
        
        # Insight cohérence
        if self.coherence_data:
            domains_count = len(self.coherence_data.get('domains', {}))
            insights.append(f"Analyse cohérence cross-domain sur {domains_count} domaines")
        
        # Insight performance
        if self.orchestration_data:
            exec_time = self.orchestration_data['summary']['total_execution_time']
            if exec_time < 1.0:
                insights.append("Performance excellente: analyse complète sous 1 seconde")
        
        # Insight traducteurs
        if self.translator_data:
            cultural_patterns = self.translator_data.get('patterns_culturels', {})
            universaux = [p for p, translators in cultural_patterns.items() 
                         if len(translators) >= self.translator_data.get('traducteurs_analyses', 1)]
            if universaux:
                insights.append(f"Biais culturels universels confirmés: {len(universaux)} patterns")
        
        return insights
    
    def run_full_dashboard(self) -> bool:
        """Génère dashboard complet"""
        
        print("\n📊 DASHBOARD SÉMANTIQUE TEXTUEL - GÉNÉRATION COMPLÈTE")
        print("=" * 70)
        
        # 1. Chargement données
        if not self.load_latest_orchestration():
            return False
        
        self.load_supporting_data()
        
        # 2. Affichage sections
        self.display_orchestration_overview()
        self.display_patterns_analysis()
        self.display_coherence_analysis()
        self.display_translator_analysis()
        
        # 3. Résumé exécutif
        print("\n" + "="*70)
        print("📋 RÉSUMÉ EXÉCUTIF")
        print("="*70)
        
        summary = self.generate_executive_summary()
        
        exec_summary = summary['executive_summary']
        print(f"🎯 Score Global Sémantique: {exec_summary['global_semantic_score']:.3f}")
        print(f"✅ Taux succès analyseurs: {exec_summary['analyzer_success_rate']:.1%}")
        print(f"🧠 Patterns détectés: {exec_summary['patterns_detected']} (dont {exec_summary['universal_patterns']} universaux)")
        print(f"🔍 Score cohérence: {exec_summary['coherence_score']:.3f}")
        print(f"⚠️  Violations: {exec_summary['coherence_violations']} (dont {exec_summary['critical_violations']} critiques)")
        
        # Insights clés
        print(f"\n💡 INSIGHTS CLÉS:")
        for insight in summary['key_insights']:
            print(f"   • {insight}")
        
        # Recommandations
        print(f"\n📋 RECOMMANDATIONS:")
        for recommendation in summary['recommendations']:
            print(f"   • {recommendation}")
        
        # 4. Sauvegarde rapport
        timestamp = datetime.now(timezone.utc).isoformat()
        summary_file = f"semantic_dashboard_summary_{timestamp.replace(':', '-').replace('.', '-')[:19]}Z.json"
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 Rapport sauvegardé: {summary_file}")
        
        return True


def main():
    """Point d'entrée principal"""
    
    dashboard = SemanticTextDashboard()
    
    try:
        success = dashboard.run_full_dashboard()
        
        if success:
            print(f"\n✅ DASHBOARD SÉMANTIQUE TERMINÉ AVEC SUCCÈS")
            print("="*50)
            
            global_score = dashboard._calculate_global_score()
            
            if global_score > 0.8:
                print("🌟 Excellent - Écosystème sémantique très robuste")
            elif global_score > 0.6:
                print("✅ Bon - Écosystème sémantique fonctionnel")
            elif global_score > 0.4:
                print("⚠️  Moyen - Améliorations nécessaires")
            else:
                print("🚨 Faible - Révision majeure requise")
        
        return success
        
    except Exception as e:
        print(f"❌ ERREUR DASHBOARD: {e}")
        return False


if __name__ == "__main__":
    main()