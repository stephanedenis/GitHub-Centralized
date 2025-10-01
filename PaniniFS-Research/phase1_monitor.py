#!/usr/bin/env python3
"""
Phase 1 Monitor - Surveillance Rendement en Temps Réel

Monitore progression Phase 1 CORE:
- Détection automatique tâches complétées
- Calcul taux completion en temps réel
- Alertes si retard détecté
- Dashboard ASCII live

Pattern: *_monitor.py (auto-approved via whitelist)

Auteur: Autonomous System
Timestamp: 2025-10-01T17:45:00Z
"""

import json
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Dict, List, Optional


class Phase1Monitor:
    """Moniteur temps réel Phase 1 CORE."""
    
    def __init__(self, workspace_root: str):
        """Initialise le moniteur."""
        self.workspace_root = Path(workspace_root)
        self.session_log_path = self.workspace_root / 'phase1_session_log.json'
        
        # Charger session
        with open(self.session_log_path, 'r') as f:
            self.session = json.load(f)
        
        self.start_time = datetime.fromisoformat(
            self.session['start_time']
        )
        
        # Critères détection completion
        self.completion_indicators = {
            'human_architecture': {
                'file': 'COMPRESSOR_ARCHITECTURE_v1.md',
                'min_lines': 100,
                'keywords': ['API', 'architecture', 'algorithme'],
                'weight': 2.0  # Tâche CRITIQUE
            },
            'colab_training': {
                'files': [
                    'dhatu_training_checkpoints/',
                    'training_metrics.json'
                ],
                'keywords': ['checkpoint', 'loss', 'accuracy'],
                'weight': 2.0  # Tâche CRITIQUE
            },
            'autonomous_validation': {
                'file': 'compression_validation_results.json',
                'min_tests': 100,
                'keywords': ['compose', 'decompose', 'integrity'],
                'weight': 1.0
            },
            'autonomous_benchmarks': {
                'file': 'compression_benchmarks.json',
                'keywords': ['gzip', 'bzip2', 'ratio', 'speed'],
                'weight': 1.0
            },
            'autonomous_metadata': {
                'file': 'translators_metadata.json',
                'min_entries': 100,
                'keywords': ['WHO', 'WHEN', 'WHERE'],
                'weight': 1.0
            }
        }
        
        self.total_weight = sum(
            ind['weight'] for ind in self.completion_indicators.values()
        )
    
    def check_task_completion(self, task_id: str, indicator: Dict) -> Dict:
        """Vérifie si une tâche est complétée."""
        result = {
            'task_id': task_id,
            'status': 'NOT_STARTED',
            'completion_percent': 0,
            'evidence': [],
            'missing': []
        }
        
        # Vérifier fichier(s)
        files_to_check = []
        if 'file' in indicator:
            files_to_check = [indicator['file']]
        elif 'files' in indicator:
            files_to_check = indicator['files']
        
        files_found = []
        for file_pattern in files_to_check:
            file_path = self.workspace_root / file_pattern
            
            # Support dossiers
            if file_pattern.endswith('/'):
                if file_path.exists() and file_path.is_dir():
                    # Compter fichiers dans dossier
                    count = len(list(file_path.iterdir()))
                    if count > 0:
                        files_found.append(f"{file_pattern} ({count} files)")
                        result['evidence'].append(
                            f"Dossier {file_pattern}: {count} fichiers"
                        )
                else:
                    result['missing'].append(f"Dossier {file_pattern}")
            else:
                if file_path.exists():
                    files_found.append(file_pattern)
                    
                    # Vérifier contenu si fichier texte
                    if file_path.suffix in ['.md', '.json', '.txt', '.py']:
                        try:
                            content = file_path.read_text()
                            lines = len(content.split('\n'))
                            
                            # Vérifier min_lines
                            if 'min_lines' in indicator:
                                if lines >= indicator['min_lines']:
                                    result['evidence'].append(
                                        f"{file_pattern}: {lines} lignes"
                                    )
                                else:
                                    result['missing'].append(
                                        f"{file_pattern}: "
                                        f"{lines}/{indicator['min_lines']} lignes"
                                    )
                            
                            # Vérifier keywords
                            if 'keywords' in indicator:
                                found_keywords = [
                                    kw for kw in indicator['keywords']
                                    if kw.lower() in content.lower()
                                ]
                                if found_keywords:
                                    result['evidence'].append(
                                        f"Keywords: {', '.join(found_keywords)}"
                                    )
                                
                                missing_keywords = [
                                    kw for kw in indicator['keywords']
                                    if kw.lower() not in content.lower()
                                ]
                                if missing_keywords:
                                    result['missing'].append(
                                        f"Keywords manquants: "
                                        f"{', '.join(missing_keywords)}"
                                    )
                            
                            # Vérifier min_entries pour JSON
                            if file_path.suffix == '.json' and 'min_entries' in indicator:
                                try:
                                    data = json.loads(content)
                                    if isinstance(data, list):
                                        count = len(data)
                                    elif isinstance(data, dict):
                                        count = len(data.keys())
                                    else:
                                        count = 0
                                    
                                    if count >= indicator['min_entries']:
                                        result['evidence'].append(
                                            f"{count} entrées"
                                        )
                                    else:
                                        result['missing'].append(
                                            f"{count}/{indicator['min_entries']} entrées"
                                        )
                                except json.JSONDecodeError:
                                    result['missing'].append(
                                        f"{file_pattern}: JSON invalide"
                                    )
                        
                        except Exception as e:
                            result['missing'].append(
                                f"{file_pattern}: erreur lecture ({e})"
                            )
                else:
                    result['missing'].append(f"Fichier {file_pattern}")
        
        # Calculer completion
        if not result['missing']:
            result['status'] = 'COMPLETED'
            result['completion_percent'] = 100
        elif result['evidence']:
            result['status'] = 'IN_PROGRESS'
            # Heuristique: % basé sur ratio evidence/total_checks
            total_checks = len(files_to_check)
            if 'keywords' in indicator:
                total_checks += len(indicator['keywords'])
            if 'min_lines' in indicator:
                total_checks += 1
            if 'min_entries' in indicator:
                total_checks += 1
            
            result['completion_percent'] = int(
                (len(result['evidence']) / total_checks) * 100
            )
        else:
            result['status'] = 'NOT_STARTED'
            result['completion_percent'] = 0
        
        return result
    
    def calculate_overall_progress(self) -> Dict:
        """Calcule progression globale Phase 1."""
        task_results = {}
        weighted_sum = 0.0
        
        for task_id, indicator in self.completion_indicators.items():
            result = self.check_task_completion(task_id, indicator)
            task_results[task_id] = result
            
            # Contribution pondérée
            contribution = (
                result['completion_percent'] / 100.0
            ) * indicator['weight']
            weighted_sum += contribution
        
        overall_percent = (weighted_sum / self.total_weight) * 100
        
        # Temps écoulé
        now = datetime.now(timezone.utc)
        elapsed = now - self.start_time
        elapsed_hours = elapsed.total_seconds() / 3600
        
        # Estimation completion
        target_end = self.start_time + timedelta(hours=2)
        remaining = target_end - now
        remaining_minutes = max(0, remaining.total_seconds() / 60)
        
        # Statut global
        if overall_percent >= 37:
            status = 'ON_TRACK'
        elif overall_percent >= 20:
            status = 'ACCEPTABLE'
        elif elapsed_hours >= 1.5:
            status = 'AT_RISK'
        else:
            status = 'STARTING'
        
        return {
            'overall_percent': round(overall_percent, 1),
            'status': status,
            'elapsed_hours': round(elapsed_hours, 2),
            'remaining_minutes': int(remaining_minutes),
            'task_results': task_results,
            'timestamp': now.isoformat()
        }
    
    def display_dashboard(self, progress: Dict):
        """Affiche dashboard ASCII."""
        print("\n" + "="*70)
        print("📊 PHASE 1 CORE - MONITORING TEMPS RÉEL")
        print("="*70)
        
        now = datetime.fromisoformat(progress['timestamp'])
        print(f"\n⏰ {now.strftime('%Y-%m-%d %H:%M:%S UTC')}")
        print(f"⏱️  Elapsed: {progress['elapsed_hours']:.2f}h")
        print(f"⏳ Remaining: {progress['remaining_minutes']}min")
        
        # Barre progression globale
        percent = progress['overall_percent']
        bar_length = 40
        filled = int((percent / 100) * bar_length)
        bar = '█' * filled + '░' * (bar_length - filled)
        
        print(f"\n📈 PROGRESSION GLOBALE: {percent}%")
        print(f"[{bar}]")
        
        # Statut
        status_icons = {
            'ON_TRACK': '✅',
            'ACCEPTABLE': '🟡',
            'AT_RISK': '⚠️',
            'STARTING': '🔵'
        }
        icon = status_icons.get(progress['status'], '❓')
        print(f"\n{icon} Statut: {progress['status']}")
        
        # Détail tâches
        print(f"\n📋 DÉTAIL TÂCHES:")
        
        task_names = {
            'human_architecture': '👤 Architecture compresseur (P9)',
            'colab_training': '🎮 Training GPU dhātu (P9)',
            'autonomous_validation': '🤖 Validation algo (P8)',
            'autonomous_benchmarks': '🤖 Benchmarks compression (P8)',
            'autonomous_metadata': '🤖 Extraction metadata (P8)'
        }
        
        for task_id, result in progress['task_results'].items():
            name = task_names.get(task_id, task_id)
            status = result['status']
            percent = result['completion_percent']
            
            status_icon = {
                'COMPLETED': '✅',
                'IN_PROGRESS': '🔄',
                'NOT_STARTED': '⏸️'
            }.get(status, '❓')
            
            print(f"\n{status_icon} {name}")
            print(f"   Status: {status} ({percent}%)")
            
            if result['evidence']:
                print(f"   ✓ Evidence:")
                for evidence in result['evidence'][:3]:  # Max 3 items
                    print(f"      - {evidence}")
            
            if result['missing']:
                print(f"   ✗ Missing:")
                for missing in result['missing'][:3]:  # Max 3 items
                    print(f"      - {missing}")
        
        # Target
        print(f"\n🎯 TARGET PHASE 1: 37-50% (3-4 tâches)")
        if percent >= 50:
            print(f"   🎉 EXCELLENT: {percent}% ≥ 50%")
        elif percent >= 37:
            print(f"   ✅ SUCCESS: {percent}% ≥ 37%")
        elif percent >= 20:
            print(f"   🟡 EN COURS: {percent}% (besoin accélérer)")
        else:
            print(f"   ⚠️  DÉMARRAGE: {percent}% (temps pour progresser)")
        
        print("\n" + "="*70)
    
    def export_progress_report(self, progress: Dict):
        """Export rapport progression."""
        report_path = self.workspace_root / 'phase1_progress_report.json'
        
        # Charger historique
        history = []
        if report_path.exists():
            with open(report_path, 'r') as f:
                data = json.load(f)
                history = data.get('history', [])
        
        # Ajouter snapshot actuel
        history.append({
            'timestamp': progress['timestamp'],
            'overall_percent': progress['overall_percent'],
            'status': progress['status'],
            'elapsed_hours': progress['elapsed_hours'],
            'task_completions': {
                task_id: {
                    'status': result['status'],
                    'percent': result['completion_percent']
                }
                for task_id, result in progress['task_results'].items()
            }
        })
        
        # Sauvegarder
        report = {
            'phase': 'PHASE_1_CORE',
            'start_time': self.session['start_time'],
            'current_progress': progress,
            'history': history
        }
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        return report_path
    
    def monitor_loop(self, interval_seconds: int = 300, iterations: Optional[int] = None):
        """Boucle monitoring continue."""
        iteration = 0
        
        print("\n🔍 Démarrage monitoring Phase 1...")
        print(f"⏱️  Interval: {interval_seconds}s ({interval_seconds//60}min)")
        if iterations:
            print(f"🔢 Iterations: {iterations}")
        else:
            print(f"♾️  Iterations: infini (Ctrl+C pour arrêter)")
        
        try:
            while True:
                if iterations and iteration >= iterations:
                    break
                
                # Check progression
                progress = self.calculate_overall_progress()
                
                # Display
                self.display_dashboard(progress)
                
                # Export
                report_path = self.export_progress_report(progress)
                print(f"\n💾 Rapport sauvegardé: {report_path.name}")
                
                # Alertes
                if progress['status'] == 'AT_RISK':
                    print(f"\n⚠️  ALERTE: Phase 1 à risque!")
                    print(f"   Action recommandée: Vérifier blocages")
                
                if progress['overall_percent'] >= 37:
                    print(f"\n🎉 MILESTONE ATTEINT: ≥37%")
                    if progress['overall_percent'] >= 50:
                        print(f"   🏆 DÉPASSEMENT TARGET: {progress['overall_percent']}%")
                
                # Prochain check
                if iterations is None or iteration < iterations - 1:
                    next_check = datetime.now(timezone.utc) + timedelta(
                        seconds=interval_seconds
                    )
                    print(f"\n⏭️  Prochain check: {next_check.strftime('%H:%M:%S UTC')}")
                    time.sleep(interval_seconds)
                
                iteration += 1
        
        except KeyboardInterrupt:
            print(f"\n\n⏹️  Monitoring arrêté par utilisateur")
            print(f"📊 Total iterations: {iteration}")


def main():
    """Point d'entrée principal."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Monitor Phase 1 CORE progression'
    )
    parser.add_argument(
        '--interval',
        type=int,
        default=300,
        help='Interval entre checks (secondes, défaut: 300 = 5min)'
    )
    parser.add_argument(
        '--iterations',
        type=int,
        default=None,
        help='Nombre iterations (défaut: infini)'
    )
    parser.add_argument(
        '--once',
        action='store_true',
        help='Check une seule fois (équivalent --iterations 1)'
    )
    
    args = parser.parse_args()
    
    workspace = "/home/stephane/GitHub/PaniniFS-Research"
    monitor = Phase1Monitor(workspace)
    
    if args.once:
        iterations = 1
    else:
        iterations = args.iterations
    
    monitor.monitor_loop(
        interval_seconds=args.interval,
        iterations=iterations
    )


if __name__ == '__main__':
    main()
