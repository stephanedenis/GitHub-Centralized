#!/usr/bin/env python3
"""
Orchestrateur Sémantique Unifié
================================

Coordonne l'exécution de tous les analyseurs sémantiques:
1. Analyseur patterns biais/styles traducteurs
2. Analyseur multiformat sémantique  
3. Moteur patterns sémantiques universels
4. Analyseur cohérence sémantique cross-domain

Séquence d'exécution optimisée avec validation croisée.

Date: 2025-10-02
Auteur: Système Autonome PaniniFS
Version: 1.0.0
"""

import sys
import json
import asyncio
import subprocess
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import time


@dataclass
class AnalyzerResult:
    """Résultat d'exécution d'un analyseur"""
    analyzer_name: str
    success: bool
    execution_time: float
    output_file: Optional[str]  # Chemin comme string
    error_message: Optional[str]
    metadata: Dict


@dataclass
class OrchestrationSummary:
    """Résumé d'orchestration complète"""
    total_analyzers: int
    successful_analyzers: int
    failed_analyzers: int
    total_execution_time: float
    output_files: List[str]  # Chemins de fichiers comme strings
    cross_validation_score: float
    unified_insights: List[str]


class SemanticOrchestrator:
    """Orchestrateur sémantique unifié"""
    
    def __init__(self):
        self.analyzer_results = []
        self.start_time = None
        self.end_time = None
        
        # Configuration analyseurs
        self.analyzers = {
            "translator_bias": {
                "script": "translator_bias_style_analyzer.py",
                "dependencies": ["translator_database_sample.json"],
                "priority": 1
            },
            "multiformat": {
                "script": "multiformat_semantic_analyzer.py", 
                "dependencies": ["extracted_content.json"],
                "priority": 2
            },
            "pattern_engine": {
                "script": "semantic_pattern_engine.py",
                "dependencies": [],  # Auto-découverte
                "priority": 3
            },
            "coherence": {
                "script": "semantic_coherence_analyzer.py",
                "dependencies": [],  # Auto-découverte
                "priority": 4
            }
        }
    
    def check_dependencies(self) -> Dict[str, bool]:
        """Vérifie disponibilité des dépendances"""
        print("\n🔍 VÉRIFICATION DÉPENDANCES")
        print("=" * 40)
        
        dependency_status = {}
        
        for analyzer_name, config in self.analyzers.items():
            all_deps_ok = True
            
            # Vérifier script principal
            script_path = Path(config["script"])
            if not script_path.exists():
                print(f"❌ Script manquant: {config['script']}")
                all_deps_ok = False
            else:
                print(f"✅ Script disponible: {config['script']}")
            
            # Vérifier dépendances
            for dep in config["dependencies"]:
                dep_path = Path(dep)
                if not dep_path.exists():
                    print(f"⚠️  Dépendance manquante: {dep} (pour {analyzer_name})")
                    # Ne pas bloquer si auto-découverte possible
                    if analyzer_name not in ["pattern_engine", "coherence"]:
                        all_deps_ok = False
                else:
                    print(f"✅ Dépendance OK: {dep}")
            
            dependency_status[analyzer_name] = all_deps_ok
        
        return dependency_status
    
    async def run_analyzer(self, analyzer_name: str, config: Dict) -> AnalyzerResult:
        """Exécute un analyseur spécifique"""
        
        print(f"\n🚀 Exécution: {analyzer_name}")
        print("-" * 30)
        
        start_time = time.time()
        
        try:
            # Construire commande
            cmd = ["python3", config["script"]]
            
            # Ajouter arguments si nécessaire
            if analyzer_name == "multiformat" and "extracted_content.json" in config["dependencies"]:
                if Path("extracted_content.json").exists():
                    cmd.append("extracted_content.json")
            
            # Exécution
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=Path.cwd()
            )
            
            stdout, stderr = await process.communicate()
            
            execution_time = time.time() - start_time
            
            if process.returncode == 0:
                print(f"✅ {analyzer_name} terminé avec succès ({execution_time:.1f}s)")
                
                # Chercher fichier de sortie
                output_file = self._find_output_file(analyzer_name)
                
                return AnalyzerResult(
                    analyzer_name=analyzer_name,
                    success=True,
                    execution_time=execution_time,
                    output_file=str(output_file) if output_file else None,
                    error_message=None,
                    metadata={
                        "stdout_lines": len(stdout.decode().splitlines()),
                        "stderr_lines": len(stderr.decode().splitlines())
                    }
                )
            else:
                error_msg = stderr.decode() if stderr else "Erreur inconnue"
                print(f"❌ {analyzer_name} a échoué: {error_msg}")
                
                return AnalyzerResult(
                    analyzer_name=analyzer_name,
                    success=False,
                    execution_time=execution_time,
                    output_file=None,
                    error_message=error_msg,
                    metadata={}
                )
                
        except Exception as e:
            execution_time = time.time() - start_time
            print(f"❌ Erreur exécution {analyzer_name}: {e}")
            
            return AnalyzerResult(
                analyzer_name=analyzer_name,
                success=False,
                execution_time=execution_time,
                output_file=None,
                error_message=str(e),
                metadata={}
            )
    
    def _find_output_file(self, analyzer_name: str) -> Optional[Path]:
        """Trouve le fichier de sortie le plus récent pour un analyseur"""
        
        # Patterns de fichiers par analyseur
        patterns = {
            "translator_bias": "*translator*bias*analysis*.json",
            "multiformat": "*multiformat*analysis*.json",
            "pattern_engine": "*semantic*patterns*analysis*.json", 
            "coherence": "*semantic*coherence*analysis*.json"
        }
        
        pattern = patterns.get(analyzer_name, f"*{analyzer_name}*.json")
        matching_files = list(Path('.').glob(pattern))
        
        if matching_files:
            # Retourner le plus récent
            return max(matching_files, key=lambda f: f.stat().st_mtime)
        
        return None
    
    def perform_cross_validation(self) -> float:
        """Effectue validation croisée des résultats"""
        print("\n🔍 VALIDATION CROISÉE RÉSULTATS")
        print("=" * 40)
        
        successful_results = [r for r in self.analyzer_results if r.success and r.output_file]
        
        if len(successful_results) < 2:
            print("⚠️  Pas assez de résultats pour validation croisée")
            return 0.0
        
        total_score = 0.0
        comparisons = 0
        
        # Comparer résultats par paires
        for i, result_a in enumerate(successful_results):
            for result_b in successful_results[i+1:]:
                score = self._compare_analyzer_outputs(Path(result_a.output_file), Path(result_b.output_file))
                total_score += score
                comparisons += 1
                
                print(f"  • {result_a.analyzer_name} ↔ {result_b.analyzer_name}: {score:.2f}")
        
        avg_score = total_score / comparisons if comparisons else 0.0
        print(f"\n📊 Score validation croisée: {avg_score:.2f}")
        
        return avg_score
    
    def _compare_analyzer_outputs(self, file_a: Path, file_b: Path) -> float:
        """Compare sorties de deux analyseurs"""
        try:
            with open(file_a, 'r', encoding='utf-8') as f:
                data_a = json.load(f)
            with open(file_b, 'r', encoding='utf-8') as f:
                data_b = json.load(f)
            
            # Comparaison structurelle simple
            keys_a = set(data_a.keys()) if isinstance(data_a, dict) else set()
            keys_b = set(data_b.keys()) if isinstance(data_b, dict) else set()
            
            if not keys_a or not keys_b:
                return 0.0
            
            intersection = len(keys_a.intersection(keys_b))
            union = len(keys_a.union(keys_b))
            
            structural_similarity = intersection / union if union else 0.0
            
            # Vérifier cohérence temporelle
            timestamp_a = data_a.get('timestamp', '')
            timestamp_b = data_b.get('timestamp', '')
            
            temporal_coherence = 0.0
            if timestamp_a and timestamp_b:
                try:
                    time_a = datetime.fromisoformat(timestamp_a.replace('Z', '+00:00'))
                    time_b = datetime.fromisoformat(timestamp_b.replace('Z', '+00:00'))
                    
                    time_diff = abs((time_a - time_b).total_seconds())
                    # Cohérence si écart < 1h
                    temporal_coherence = max(0.0, 1.0 - time_diff / 3600)
                except:
                    pass
            
            # Score combiné
            return 0.7 * structural_similarity + 0.3 * temporal_coherence
            
        except Exception as e:
            print(f"⚠️  Erreur comparaison {file_a.name} vs {file_b.name}: {e}")
            return 0.0
    
    def extract_unified_insights(self) -> List[str]:
        """Extrait insights unifiés cross-analyseurs"""
        print("\n🧠 EXTRACTION INSIGHTS UNIFIÉS")
        print("=" * 40)
        
        insights = []
        
        successful_outputs = []
        for result in self.analyzer_results:
            if result.success and result.output_file:
                try:
                    with open(result.output_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    successful_outputs.append((result.analyzer_name, data))
                except:
                    continue
        
        # Insight 1: Patterns universaux détectés
        universal_patterns_count = 0
        for analyzer_name, data in successful_outputs:
            if 'patterns' in data:
                universal_patterns = [p for p in data['patterns'] if p.get('pattern_type') == 'universal']
                universal_patterns_count += len(universal_patterns)
        
        if universal_patterns_count > 0:
            insights.append(f"Détection de {universal_patterns_count} patterns universaux cross-analyseurs")
        
        # Insight 2: Cohérence temporelle
        timestamps = []
        for analyzer_name, data in successful_outputs:
            if 'timestamp' in data:
                timestamps.append(data['timestamp'])
        
        if len(timestamps) >= 2:
            temporal_span = self._calculate_temporal_span(timestamps)
            insights.append(f"Cohérence temporelle: analyses sur {temporal_span:.1f}h")
        
        # Insight 3: Couverture domaines
        domains_covered = set()
        for analyzer_name, data in successful_outputs:
            # Extraire domaines couverts
            if 'domains' in data:
                if isinstance(data['domains'], list):
                    domains_covered.update(data['domains'])
                elif isinstance(data['domains'], dict):
                    domains_covered.update(data['domains'].keys())
        
        if domains_covered:
            insights.append(f"Couverture {len(domains_covered)} domaines: {', '.join(sorted(domains_covered))}")
        
        # Insight 4: Performance globale
        total_execution_time = sum(r.execution_time for r in self.analyzer_results)
        success_rate = len([r for r in self.analyzer_results if r.success]) / len(self.analyzer_results)
        
        insights.append(f"Performance: {success_rate:.1%} succès en {total_execution_time:.1f}s")
        
        return insights
    
    def _calculate_temporal_span(self, timestamps: List[str]) -> float:
        """Calcule étendue temporelle des analyses"""
        try:
            parsed_times = []
            for ts in timestamps:
                time_obj = datetime.fromisoformat(ts.replace('Z', '+00:00'))
                parsed_times.append(time_obj)
            
            if len(parsed_times) >= 2:
                min_time = min(parsed_times)
                max_time = max(parsed_times)
                span_seconds = (max_time - min_time).total_seconds()
                return span_seconds / 3600  # Heures
            
        except:
            pass
        
        return 0.0
    
    def generate_orchestration_report(self) -> Dict:
        """Génère rapport d'orchestration complet"""
        
        successful_results = [r for r in self.analyzer_results if r.success]
        failed_results = [r for r in self.analyzer_results if not r.success]
        
        total_time = (self.end_time - self.start_time) if self.end_time and self.start_time else 0.0
        
        cross_validation_score = self.perform_cross_validation()
        unified_insights = self.extract_unified_insights()
        
        summary = OrchestrationSummary(
            total_analyzers=len(self.analyzer_results),
            successful_analyzers=len(successful_results),
            failed_analyzers=len(failed_results),
            total_execution_time=total_time,
            output_files=[str(r.output_file) for r in successful_results if r.output_file],
            cross_validation_score=cross_validation_score,
            unified_insights=unified_insights
        )
        
        report = {
            "meta": {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "orchestrator_version": "1.0.0",
                "total_execution_time": total_time
            },
            "summary": asdict(summary),
            "analyzer_results": [asdict(r) for r in self.analyzer_results],
            "successful_outputs": [str(r.output_file) for r in successful_results if r.output_file],
            "failed_analyzers": [r.analyzer_name for r in failed_results],
            "cross_validation": {
                "score": cross_validation_score,
                "interpretation": self._interpret_validation_score(cross_validation_score)
            },
            "unified_insights": unified_insights,
            "recommendations": self._generate_orchestration_recommendations()
        }
        
        return report
    
    def _interpret_validation_score(self, score: float) -> str:
        """Interprète le score de validation croisée"""
        if score >= 0.8:
            return "Excellente cohérence entre analyseurs"
        elif score >= 0.6:
            return "Bonne cohérence avec quelques divergences"
        elif score >= 0.4:
            return "Cohérence modérée - réviser alignement"
        else:
            return "Faible cohérence - problèmes méthodologiques"
    
    def _generate_orchestration_recommendations(self) -> List[str]:
        """Génère recommandations d'amélioration"""
        
        recommendations = []
        
        success_rate = len([r for r in self.analyzer_results if r.success]) / len(self.analyzer_results) if self.analyzer_results else 0
        
        if success_rate < 0.8:
            recommendations.append("Améliorer robustesse analyseurs - taux échec élevé")
        
        if len(self.analyzer_results) < 4:
            recommendations.append("Ajouter plus d'analyseurs pour couverture complète")
        
        avg_execution_time = sum(r.execution_time for r in self.analyzer_results) / len(self.analyzer_results) if self.analyzer_results else 0
        if avg_execution_time > 30:
            recommendations.append("Optimiser performance - temps exécution élevé")
        
        output_files = [r.output_file for r in self.analyzer_results if r.success and r.output_file]
        if len(output_files) < 2:
            recommendations.append("Augmenter nombre sorties pour validation croisée")
        
        return recommendations
    
    async def run_full_orchestration(self) -> Dict:
        """Exécution complète orchestration sémantique"""
        
        print("\n🎼 ORCHESTRATEUR SÉMANTIQUE - EXÉCUTION COMPLÈTE")
        print("=" * 65)
        
        self.start_time = time.time()
        
        # 1. Vérification dépendances
        dependency_status = self.check_dependencies()
        
        # 2. Planification exécution
        executable_analyzers = [(name, config) for name, config in self.analyzers.items() 
                               if dependency_status.get(name, False)]
        
        print(f"\n📋 Planification: {len(executable_analyzers)}/{len(self.analyzers)} analyseurs exécutables")
        
        if not executable_analyzers:
            print("❌ Aucun analyseur exécutable - arrêt")
            return {}
        
        # 3. Exécution séquentielle (par priorité)
        sorted_analyzers = sorted(executable_analyzers, key=lambda x: self.analyzers[x[0]]["priority"])
        
        for analyzer_name, config in sorted_analyzers:
            result = await self.run_analyzer(analyzer_name, config)
            self.analyzer_results.append(result)
        
        self.end_time = time.time()
        
        # 4. Génération rapport final
        report = self.generate_orchestration_report()
        
        # 5. Sauvegarde
        timestamp = datetime.now(timezone.utc).isoformat()
        output_file = f"semantic_orchestration_{timestamp.replace(':', '-').replace('.', '-')[:19]}Z.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 Rapport orchestration sauvegardé: {output_file}")
        
        return report


async def main():
    """Point d'entrée principal"""
    
    orchestrator = SemanticOrchestrator()
    
    try:
        report = await orchestrator.run_full_orchestration()
        
        if report:
            print("\n📊 RÉSUMÉ ORCHESTRATION")
            print("=" * 45)
            print(f"✅ Analyseurs exécutés: {report['summary']['successful_analyzers']}/{report['summary']['total_analyzers']}")
            print(f"⏱️  Temps total: {report['summary']['total_execution_time']:.1f}s")
            print(f"📋 Fichiers générés: {len(report['summary']['output_files'])}")
            print(f"🔍 Score validation: {report['cross_validation']['score']:.2f}")
            print(f"📈 Interprétation: {report['cross_validation']['interpretation']}")
            
            if report['summary']['unified_insights']:
                print(f"\n💡 INSIGHTS UNIFIÉS:")
                for insight in report['summary']['unified_insights']:
                    print(f"   • {insight}")
        
        return True
        
    except Exception as e:
        print(f"❌ ERREUR ORCHESTRATION: {e}")
        return False


if __name__ == "__main__":
    asyncio.run(main())