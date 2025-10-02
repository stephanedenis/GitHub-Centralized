#!/usr/bin/env python3
"""
Dashboard Sémantique Unifié - Visualisation Insights
====================================================

Agrège tous les résultats d'analyses sémantiques pour créer
un dashboard unifié avec visualisations et métriques clés.

Date: 2025-10-02
Auteur: Système Autonome PaniniFS
Version: 1.0.0
"""

import json
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Any
import numpy as np
from collections import Counter, defaultdict


class SemanticDashboard:
    """Dashboard sémantique unifié"""
    
    def __init__(self):
        self.orchestration_data = None
        self.pattern_data = None
        self.coherence_data = None
        self.translator_data = None
        
        # Configuration style
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
        
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
    
    def create_orchestration_overview(self) -> plt.Figure:
        """Crée vue d'ensemble orchestration"""
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('📊 Dashboard Sémantique - Vue d\'ensemble', fontsize=16, fontweight='bold')
        
        # 1. Statut analyseurs
        if self.orchestration_data:
            summary = self.orchestration_data['summary']
            
            labels = ['Succès', 'Échecs']
            sizes = [summary['successful_analyzers'], summary['failed_analyzers']]
            colors = ['#2ecc71', '#e74c3c']
            
            ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
            ax1.set_title('Statut Analyseurs')
            
            # 2. Temps d'exécution par analyseur
            analyzer_results = self.orchestration_data.get('analyzer_results', [])
            if analyzer_results:
                names = [r['analyzer_name'] for r in analyzer_results]
                times = [r['execution_time'] for r in analyzer_results]
                
                bars = ax2.bar(names, times)
                ax2.set_title('Temps d\'exécution (s)')
                ax2.set_xlabel('Analyseurs')
                ax2.set_ylabel('Temps (s)')
                ax2.tick_params(axis='x', rotation=45)
                
                # Colorier selon succès/échec
                for i, result in enumerate(analyzer_results):
                    bars[i].set_color('#2ecc71' if result['success'] else '#e74c3c')
        
        # 3. Patterns détectés
        if self.pattern_data:
            patterns = self.pattern_data.get('patterns', [])
            pattern_types = [p['pattern_type'] for p in patterns]
            type_counts = Counter(pattern_types)
            
            if type_counts:
                ax3.bar(type_counts.keys(), type_counts.values())
                ax3.set_title('Patterns par Type')
                ax3.set_xlabel('Type de Pattern')
                ax3.set_ylabel('Nombre')
        
        # 4. Score cohérence
        if self.coherence_data:
            coherence_score = self.coherence_data.get('statistics', {}).get('coherence_score', 0)
            
            # Gauge simple
            angles = np.linspace(0, np.pi, 100)
            values = np.ones_like(angles) * 0.8
            
            ax4.plot(angles, values, 'k-', linewidth=2)
            ax4.fill_between(angles, 0, values, alpha=0.3)
            
            # Position du score
            score_angle = coherence_score * np.pi
            ax4.plot([score_angle, score_angle], [0, 0.8], 'r-', linewidth=4)
            
            ax4.set_ylim(0, 1)
            ax4.set_xlim(0, np.pi)
            ax4.set_title(f'Score Cohérence: {coherence_score:.2f}')
            ax4.set_xticks([0, np.pi/2, np.pi])
            ax4.set_xticklabels(['0', '0.5', '1.0'])
            ax4.set_yticks([])
        
        plt.tight_layout()
        return fig
    
    def create_patterns_analysis(self) -> plt.Figure:
        """Analyse détaillée des patterns"""
        
        if not self.pattern_data:
            return None
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('🧠 Analyse Patterns Sémantiques', fontsize=16, fontweight='bold')
        
        patterns = self.pattern_data.get('patterns', [])
        
        if patterns:
            # 1. Distribution force patterns
            strengths = [p['strength'] for p in patterns]
            ax1.hist(strengths, bins=10, alpha=0.7, color='skyblue', edgecolor='black')
            ax1.set_title('Distribution Force Patterns')
            ax1.set_xlabel('Force')
            ax1.set_ylabel('Nombre de Patterns')
            ax1.axvline(np.mean(strengths), color='red', linestyle='--', label=f'Moyenne: {np.mean(strengths):.2f}')
            ax1.legend()
            
            # 2. Confiance vs Force
            confidences = [p['confidence'] for p in patterns]
            ax2.scatter(strengths, confidences, alpha=0.7)
            ax2.set_title('Confiance vs Force')
            ax2.set_xlabel('Force')
            ax2.set_ylabel('Confiance')
            
            # Ligne de régression
            if len(strengths) > 1:
                z = np.polyfit(strengths, confidences, 1)
                p = np.poly1d(z)
                ax2.plot(strengths, p(strengths), "r--", alpha=0.8)
        
        # 3. Sources patterns
        if patterns:
            all_sources = []
            for p in patterns:
                all_sources.extend(p.get('sources', []))
            
            source_counts = Counter(all_sources)
            
            if source_counts:
                ax3.bar(source_counts.keys(), source_counts.values())
                ax3.set_title('Contribution par Source')
                ax3.set_xlabel('Analyseur Source')
                ax3.set_ylabel('Nombre de Patterns')
                ax3.tick_params(axis='x', rotation=45)
        
        # 4. Invariants universels
        invariants = self.pattern_data.get('universal_invariants', [])
        if invariants:
            scores = [inv['universality_score'] for inv in invariants]
            names = [inv['invariant_id'][:20] + '...' if len(inv['invariant_id']) > 20 else inv['invariant_id'] for inv in invariants]
            
            bars = ax4.barh(names, scores)
            ax4.set_title('Scores Universalité Invariants')
            ax4.set_xlabel('Score Universalité')
            
            # Colorier selon score
            for i, score in enumerate(scores):
                if score > 0.8:
                    bars[i].set_color('#2ecc71')  # Vert
                elif score > 0.6:
                    bars[i].set_color('#f39c12')  # Orange
                else:
                    bars[i].set_color('#e74c3c')  # Rouge
        
        plt.tight_layout()
        return fig
    
    def create_coherence_analysis(self) -> plt.Figure:
        """Analyse détaillée cohérence"""
        
        if not self.coherence_data:
            return None
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('🔍 Analyse Cohérence Sémantique', fontsize=16, fontweight='bold')
        
        # 1. Distribution violations par type
        violations = self.coherence_data.get('coherence_violations', [])
        if violations:
            violation_types = [v['violation_type'] for v in violations]
            type_counts = Counter(violation_types)
            
            ax1.bar(type_counts.keys(), type_counts.values())
            ax1.set_title('Violations par Type')
            ax1.set_xlabel('Type de Violation')
            ax1.set_ylabel('Nombre')
            ax1.tick_params(axis='x', rotation=45)
        
        # 2. Sévérité violations
        if violations:
            severities = [v['severity'] for v in violations]
            severity_counts = Counter(severities)
            
            colors_map = {'low': '#2ecc71', 'medium': '#f39c12', 'high': '#e74c3c', 'critical': '#8e44ad'}
            colors = [colors_map.get(sev, '#95a5a6') for sev in severity_counts.keys()]
            
            ax2.pie(severity_counts.values(), labels=severity_counts.keys(), colors=colors, autopct='%1.1f%%')
            ax2.set_title('Distribution Sévérité')
        
        # 3. Violations par domaine
        if violations:
            domain_violations = defaultdict(int)
            for v in violations:
                for domain in v.get('domains', []):
                    domain_violations[domain] += 1
            
            if domain_violations:
                ax3.bar(domain_violations.keys(), domain_violations.values())
                ax3.set_title('Violations par Domaine')
                ax3.set_xlabel('Domaine')
                ax3.set_ylabel('Nombre de Violations')
                ax3.tick_params(axis='x', rotation=45)
        
        # 4. Confiance violations
        if violations:
            confidences = [v['confidence'] for v in violations]
            ax4.hist(confidences, bins=10, alpha=0.7, color='lightcoral', edgecolor='black')
            ax4.set_title('Distribution Confiance Violations')
            ax4.set_xlabel('Confiance')
            ax4.set_ylabel('Nombre de Violations')
            ax4.axvline(np.mean(confidences), color='blue', linestyle='--', label=f'Moyenne: {np.mean(confidences):.2f}')
            ax4.legend()
        
        plt.tight_layout()
        return fig
    
    def create_translator_bias_analysis(self) -> plt.Figure:
        """Analyse biais traducteurs"""
        
        if not self.translator_data:
            return None
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('👥 Analyse Biais Traducteurs', fontsize=16, fontweight='bold')
        
        # 1. Patterns culturels
        cultural_patterns = self.translator_data.get('patterns_culturels', {})
        if cultural_patterns:
            pattern_names = list(cultural_patterns.keys())
            pattern_counts = [len(translators) for translators in cultural_patterns.values()]
            
            ax1.barh(pattern_names, pattern_counts)
            ax1.set_title('Patterns Culturels')
            ax1.set_xlabel('Nombre de Traducteurs')
        
        # 2. Patterns temporels
        temporal_patterns = self.translator_data.get('patterns_temporels', {})
        if temporal_patterns:
            pattern_names = list(temporal_patterns.keys())
            pattern_counts = [len(translators) for translators in temporal_patterns.values()]
            
            ax2.bar(pattern_names, pattern_counts)
            ax2.set_title('Patterns Temporels')
            ax2.set_ylabel('Nombre de Traducteurs')
            ax2.tick_params(axis='x', rotation=45)
        
        # 3. Signatures stylistiques
        style_signatures = self.translator_data.get('signatures_stylistiques', {})
        if style_signatures:
            signature_names = list(style_signatures.keys())
            signature_counts = [len(translators) for translators in style_signatures.values()]
            
            ax3.pie(signature_counts, labels=signature_names, autopct='%1.1f%%')
            ax3.set_title('Signatures Stylistiques')
        
        # 4. Universaux vs Contextuels
        universaux = self.translator_data.get('universaux', {})
        contextuels = self.translator_data.get('contextuels', {})
        
        categories = ['Universaux', 'Contextuels']
        counts = [len(universaux), len(contextuels)]
        
        ax4.bar(categories, counts, color=['#3498db', '#e67e22'])
        ax4.set_title('Universaux vs Contextuels')
        ax4.set_ylabel('Nombre de Patterns')
        
        plt.tight_layout()
        return fig
    
    def generate_summary_report(self) -> Dict:
        """Génère rapport de synthèse"""
        
        timestamp = datetime.now(timezone.utc).isoformat()
        
        # Métriques clés
        total_patterns = 0
        total_invariants = 0
        total_violations = 0
        coherence_score = 0.0
        
        if self.pattern_data:
            total_patterns = len(self.pattern_data.get('patterns', []))
            total_invariants = len(self.pattern_data.get('universal_invariants', []))
        
        if self.coherence_data:
            total_violations = len(self.coherence_data.get('coherence_violations', []))
            coherence_score = self.coherence_data.get('statistics', {}).get('coherence_score', 0.0)
        
        # Performance orchestration
        success_rate = 0.0
        total_time = 0.0
        if self.orchestration_data:
            summary = self.orchestration_data['summary']
            success_rate = summary['successful_analyzers'] / summary['total_analyzers']
            total_time = summary['total_execution_time']
        
        # Score global sémantique
        semantic_score = self._calculate_global_semantic_score()
        
        report = {
            "meta": {
                "timestamp": timestamp,
                "dashboard_version": "1.0.0"
            },
            "key_metrics": {
                "total_patterns_detected": total_patterns,
                "universal_invariants": total_invariants,
                "coherence_violations": total_violations,
                "coherence_score": coherence_score,
                "analyzer_success_rate": success_rate,
                "total_execution_time": total_time,
                "global_semantic_score": semantic_score
            },
            "data_sources": {
                "orchestration_loaded": self.orchestration_data is not None,
                "patterns_loaded": self.pattern_data is not None,
                "coherence_loaded": self.coherence_data is not None,
                "translator_loaded": self.translator_data is not None
            },
            "recommendations": self._generate_dashboard_recommendations(),
            "insights": self._extract_key_insights()
        }
        
        return report
    
    def _calculate_global_semantic_score(self) -> float:
        """Calcule score sémantique global"""
        
        scores = []
        
        # Score patterns (force moyenne)
        if self.pattern_data:
            patterns = self.pattern_data.get('patterns', [])
            if patterns:
                avg_strength = sum(p['strength'] for p in patterns) / len(patterns)
                scores.append(avg_strength)
        
        # Score cohérence
        if self.coherence_data:
            coherence_score = self.coherence_data.get('statistics', {}).get('coherence_score', 0.0)
            scores.append(coherence_score)
        
        # Score orchestration (taux succès)
        if self.orchestration_data:
            summary = self.orchestration_data['summary']
            success_rate = summary['successful_analyzers'] / summary['total_analyzers']
            scores.append(success_rate)
        
        return sum(scores) / len(scores) if scores else 0.0
    
    def _generate_dashboard_recommendations(self) -> List[str]:
        """Génère recommandations dashboard"""
        
        recommendations = []
        
        global_score = self._calculate_global_semantic_score()
        
        if global_score < 0.5:
            recommendations.append("Score sémantique global faible - réviser méthodologie")
        
        if self.coherence_data:
            violations = self.coherence_data.get('coherence_violations', [])
            critical_violations = [v for v in violations if v.get('severity') == 'critical']
            if critical_violations:
                recommendations.append(f"Résoudre {len(critical_violations)} violations critiques")
        
        if self.orchestration_data:
            failed_analyzers = len([r for r in self.orchestration_data.get('analyzer_results', []) if not r['success']])
            if failed_analyzers > 0:
                recommendations.append(f"Réparer {failed_analyzers} analyseurs défaillants")
        
        return recommendations
    
    def _extract_key_insights(self) -> List[str]:
        """Extrait insights clés"""
        
        insights = []
        
        # Insight patterns
        if self.pattern_data:
            universal_patterns = [p for p in self.pattern_data.get('patterns', []) if p.get('pattern_type') == 'universal']
            if universal_patterns:
                insights.append(f"{len(universal_patterns)} patterns universaux validés - base solide")
        
        # Insight cohérence
        if self.coherence_data:
            domains_count = len(self.coherence_data.get('domains', {}))
            insights.append(f"Analyse cohérence sur {domains_count} domaines sémantiques")
        
        # Insight performance
        if self.orchestration_data:
            total_time = self.orchestration_data['summary']['total_execution_time']
            if total_time < 1.0:
                insights.append("Performance excellente - analyse sous 1 seconde")
        
        return insights
    
    def run_full_dashboard(self) -> bool:
        """Génère dashboard complet"""
        
        print("\n📊 DASHBOARD SÉMANTIQUE - GÉNÉRATION COMPLÈTE")
        print("=" * 55)
        
        # 1. Chargement données
        if not self.load_latest_orchestration():
            return False
        
        self.load_supporting_data()
        
        # 2. Génération visualisations
        print("\n🎨 Génération visualisations...")
        
        # Vue d'ensemble
        fig1 = self.create_orchestration_overview()
        if fig1:
            fig1.savefig('semantic_dashboard_overview.png', dpi=300, bbox_inches='tight')
            print("✅ Vue d'ensemble sauvegardée")
            plt.close(fig1)
        
        # Patterns
        fig2 = self.create_patterns_analysis()
        if fig2:
            fig2.savefig('semantic_dashboard_patterns.png', dpi=300, bbox_inches='tight')
            print("✅ Analyse patterns sauvegardée")
            plt.close(fig2)
        
        # Cohérence
        fig3 = self.create_coherence_analysis()
        if fig3:
            fig3.savefig('semantic_dashboard_coherence.png', dpi=300, bbox_inches='tight')
            print("✅ Analyse cohérence sauvegardée")
            plt.close(fig3)
        
        # Traducteurs
        fig4 = self.create_translator_bias_analysis()
        if fig4:
            fig4.savefig('semantic_dashboard_translators.png', dpi=300, bbox_inches='tight')
            print("✅ Analyse traducteurs sauvegardée")
            plt.close(fig4)
        
        # 3. Rapport synthèse
        summary_report = self.generate_summary_report()
        
        timestamp = datetime.now(timezone.utc).isoformat()
        summary_file = f"semantic_dashboard_summary_{timestamp.replace(':', '-').replace('.', '-')[:19]}Z.json"
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary_report, f, ensure_ascii=False, indent=2)
        
        print(f"💾 Rapport synthèse: {summary_file}")
        
        return True


def main():
    """Point d'entrée principal"""
    
    dashboard = SemanticDashboard()
    
    try:
        success = dashboard.run_full_dashboard()
        
        if success:
            print("\n📈 DASHBOARD SÉMANTIQUE TERMINÉ")
            print("=" * 40)
            print("✅ Visualisations générées:")
            print("   • semantic_dashboard_overview.png")
            print("   • semantic_dashboard_patterns.png") 
            print("   • semantic_dashboard_coherence.png")
            print("   • semantic_dashboard_translators.png")
            print("✅ Rapport synthèse généré")
            
            # Afficher métriques clés
            if dashboard.orchestration_data or dashboard.pattern_data or dashboard.coherence_data:
                global_score = dashboard._calculate_global_semantic_score()
                print(f"\n🎯 Score Sémantique Global: {global_score:.2f}")
                
                insights = dashboard._extract_key_insights()
                if insights:
                    print("\n💡 Insights Clés:")
                    for insight in insights:
                        print(f"   • {insight}")
        
        return success
        
    except Exception as e:
        print(f"❌ ERREUR DASHBOARD: {e}")
        return False


if __name__ == "__main__":
    main()