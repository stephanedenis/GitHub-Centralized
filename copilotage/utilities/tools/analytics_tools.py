#!/usr/bin/env python3
"""
Analytics Tools - Métriques et Performance Réutilisables
========================================================

Remplace les analyses de performance ad-hoc répétitives:
- Analyse bottlenecks → analytics.analyze_bottlenecks()
- Métriques système → analytics.collect_metrics()
- Tests performance → analytics.run_performance_test()
"""

import time
import psutil
import sqlite3
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
import threading
from collections import defaultdict


class AnalyticsTools:
    """Outils analytics et performance réutilisables"""
    
    def __init__(self):
        self.workspace_root = Path("/home/stephane/GitHub/PaniniFS-Research")
        self.web_dir = self.workspace_root / "web"
        self.metrics_history = []
        self.performance_data = defaultdict(list)
        
    def collect_system_metrics(self) -> Dict[str, Any]:
        """Collecte métriques système standardisée"""
        timestamp = time.time()
        
        # CPU
        cpu_percent = psutil.cpu_percent(interval=0.1)
        cpu_count = psutil.cpu_count()
        cpu_freq = psutil.cpu_freq()
        
        # Mémoire
        memory = psutil.virtual_memory()
        
        # Disque
        disk = psutil.disk_usage(self.workspace_root)
        
        # Processus Python actifs
        python_processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                if 'python' in proc.info['name'].lower():
                    python_processes.append({
                        'pid': proc.info['pid'],
                        'cpu': proc.info['cpu_percent'],
                        'memory': proc.info['memory_percent']
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
                
        metrics = {
            'timestamp': timestamp,
            'datetime': datetime.fromtimestamp(timestamp).isoformat(),
            'cpu': {
                'percent': cpu_percent,
                'count': cpu_count,
                'frequency': cpu_freq.current if cpu_freq else None
            },
            'memory': {
                'total': memory.total,
                'available': memory.available,
                'percent': memory.percent,
                'used': memory.used
            },
            'disk': {
                'total': disk.total,
                'used': disk.used,
                'free': disk.free,
                'percent': (disk.used / disk.total) * 100
            },
            'processes': {
                'python_count': len(python_processes),
                'python_cpu_total': sum(p['cpu'] for p in python_processes),
                'python_memory_total': sum(p['memory'] for p in python_processes)
            }
        }
        
        self.metrics_history.append(metrics)
        return metrics
        
    def analyze_dhatu_performance(self, 
                                 db_path: str = "real_dhatu_analysis.db") -> Dict[str, Any]:
        """Analyse performance pipeline dhātu"""
        db_full_path = self.web_dir / db_path
        
        if not db_full_path.exists():
            return {'error': f'Database not found: {db_path}'}
            
        try:
            with sqlite3.connect(str(db_full_path)) as conn:
                cursor = conn.cursor()
                
                # Statistiques de base
                cursor.execute("SELECT COUNT(*) FROM real_dhatu_atoms")
                total_atoms = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM real_dhatu_patterns")
                total_patterns = cursor.fetchone()[0]
                
                # Distribution longueurs atomes
                cursor.execute("""
                    SELECT LENGTH(form) as length, COUNT(*) as count 
                    FROM real_dhatu_atoms 
                    GROUP BY LENGTH(form) 
                    ORDER BY length
                """)
                length_distribution = cursor.fetchall()
                
                # Top atomes par fréquence
                cursor.execute("""
                    SELECT form, frequency 
                    FROM real_dhatu_atoms 
                    ORDER BY frequency DESC 
                    LIMIT 10
                """)
                top_atoms = cursor.fetchall()
                
                return {
                    'total_atoms': total_atoms,
                    'total_patterns': total_patterns,
                    'atoms_per_pattern': total_atoms / total_patterns if total_patterns > 0 else 0,
                    'length_distribution': dict(length_distribution),
                    'top_atoms': [{'form': form, 'frequency': freq} for form, freq in top_atoms],
                    'efficiency_score': self._calculate_efficiency_score(total_atoms, total_patterns)
                }
                
        except sqlite3.Error as e:
            return {'error': f'Database error: {e}'}
            
    def _calculate_efficiency_score(self, atoms: int, patterns: int) -> float:
        """Score d'efficacité pipeline (0-100)"""
        if atoms == 0 or patterns == 0:
            return 0.0
            
        # Facteurs d'efficacité
        atom_factor = min(atoms / 2500, 1.0) * 40  # Max 40 points pour 2500+ atomes
        pattern_factor = min(patterns / 100, 1.0) * 30  # Max 30 points pour 100+ patterns
        ratio_factor = min(atoms / patterns / 20, 1.0) * 30  # Max 30 points pour ratio 20+
        
        return atom_factor + pattern_factor + ratio_factor
        
    def detect_bottlenecks(self, duration: int = 60) -> Dict[str, Any]:
        """Détection bottlenecks système sur période"""
        print(f"🔍 Analyse bottlenecks ({duration}s)...")
        
        start_time = time.time()
        samples = []
        
        while time.time() - start_time < duration:
            sample = self.collect_system_metrics()
            samples.append(sample)
            time.sleep(1)
            
        # Analyse des échantillons
        cpu_values = [s['cpu']['percent'] for s in samples]
        memory_values = [s['memory']['percent'] for s in samples]
        
        analysis = {
            'duration': duration,
            'samples_count': len(samples),
            'cpu': {
                'avg': sum(cpu_values) / len(cpu_values),
                'max': max(cpu_values),
                'min': min(cpu_values),
                'bottleneck': max(cpu_values) > 80
            },
            'memory': {
                'avg': sum(memory_values) / len(memory_values),
                'max': max(memory_values),
                'min': min(memory_values),
                'bottleneck': max(memory_values) > 85
            },
            'bottlenecks_detected': [],
            'recommendations': []
        }
        
        # Détection bottlenecks
        if analysis['cpu']['bottleneck']:
            analysis['bottlenecks_detected'].append({
                'type': 'cpu',
                'severity': 'high' if analysis['cpu']['max'] > 90 else 'medium',
                'description': f"CPU usage peaked at {analysis['cpu']['max']:.1f}%"
            })
            analysis['recommendations'].append("Consider reducing CPU-intensive operations")
            
        if analysis['memory']['bottleneck']:
            analysis['bottlenecks_detected'].append({
                'type': 'memory',
                'severity': 'high' if analysis['memory']['max'] > 95 else 'medium',
                'description': f"Memory usage peaked at {analysis['memory']['max']:.1f}%"
            })
            analysis['recommendations'].append("Consider optimizing memory usage")
            
        # Score santé global
        cpu_health = 100 - analysis['cpu']['avg']
        memory_health = 100 - analysis['memory']['avg']
        analysis['health_score'] = (cpu_health + memory_health) / 2
        
        return analysis
        
    def benchmark_dhatu_processing(self, test_duration: int = 30) -> Dict[str, Any]:
        """Benchmark traitement dhātu"""
        print(f"⚡ Benchmark dhātu processing ({test_duration}s)...")
        
        start_time = time.time()
        start_metrics = self.collect_system_metrics()
        
        # Simulation charge dhātu (remplace vrai traitement)
        operations = 0
        while time.time() - start_time < test_duration:
            # Simulation opération dhātu
            dummy_text = "lorem ipsum " * 100
            atoms = dummy_text.split()  # Simulation extraction atomes
            patterns = [atom[:3] for atom in atoms[:10]]  # Simulation patterns
            operations += len(atoms) + len(patterns)
            
            if operations % 1000 == 0:
                time.sleep(0.001)  # Micro-pause pour réalisme
                
        end_metrics = self.collect_system_metrics()
        end_time = time.time()
        
        duration = end_time - start_time
        throughput = operations / duration
        
        return {
            'duration': duration,
            'operations_total': operations,
            'throughput_ops_per_sec': throughput,
            'throughput_ops_per_min': throughput * 60,
            'cpu_delta': end_metrics['cpu']['percent'] - start_metrics['cpu']['percent'],
            'memory_delta': end_metrics['memory']['percent'] - start_metrics['memory']['percent'],
            'efficiency_rating': self._rate_efficiency(throughput)
        }
        
    def _rate_efficiency(self, throughput: float) -> str:
        """Rating efficacité basé sur throughput"""
        if throughput > 10000:
            return "excellent"
        elif throughput > 5000:
            return "good"
        elif throughput > 1000:
            return "average"
        else:
            return "poor"
            
    def generate_performance_report(self) -> Dict[str, Any]:
        """Rapport performance complet"""
        current_metrics = self.collect_system_metrics()
        dhatu_perf = self.analyze_dhatu_performance()
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'system_status': {
                'cpu_usage': current_metrics['cpu']['percent'],
                'memory_usage': current_metrics['memory']['percent'],
                'disk_usage': current_metrics['disk']['percent'],
                'python_processes': current_metrics['processes']['python_count']
            },
            'dhatu_pipeline': dhatu_perf,
            'health_indicators': {
                'cpu_healthy': current_metrics['cpu']['percent'] < 80,
                'memory_healthy': current_metrics['memory']['percent'] < 85,
                'disk_healthy': current_metrics['disk']['percent'] < 90,
                'pipeline_efficient': dhatu_perf.get('efficiency_score', 0) > 70
            },
            'metrics_history_length': len(self.metrics_history)
        }
        
        # Score santé global
        health_checks = list(report['health_indicators'].values())
        report['overall_health_score'] = (sum(health_checks) / len(health_checks)) * 100
        
        return report
        
    def save_metrics(self, filename: str = None) -> str:
        """Sauvegarde métriques collectées"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"metrics_{timestamp}.json"
            
        filepath = self.web_dir / filename
        
        data = {
            'metadata': {
                'created': datetime.now().isoformat(),
                'samples_count': len(self.metrics_history),
                'workspace': str(self.workspace_root)
            },
            'metrics': self.metrics_history,
            'performance_data': dict(self.performance_data)
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
        return str(filepath)


def main():
    """Test du module analytics_tools"""
    analytics = AnalyticsTools()
    
    print("🧪 TEST ANALYTICS TOOLS")
    print("=" * 30)
    
    # Test métriques système
    print("\n📊 MÉTRIQUES SYSTÈME")
    metrics = analytics.collect_system_metrics()
    print(f"CPU: {metrics['cpu']['percent']:.1f}%")
    print(f"Memory: {metrics['memory']['percent']:.1f}%")
    print(f"Python processes: {metrics['processes']['python_count']}")
    
    # Test performance dhātu
    print("\n⚛️  PERFORMANCE DHĀTU")
    dhatu_perf = analytics.analyze_dhatu_performance()
    if 'error' not in dhatu_perf:
        print(f"Total atoms: {dhatu_perf['total_atoms']}")
        print(f"Total patterns: {dhatu_perf['total_patterns']}")
        print(f"Efficiency score: {dhatu_perf['efficiency_score']:.1f}/100")
    else:
        print(f"⚠️  {dhatu_perf['error']}")
    
    # Test benchmark rapide
    print("\n⚡ BENCHMARK RAPIDE (5s)")
    benchmark = analytics.benchmark_dhatu_processing(5)
    print(f"Throughput: {benchmark['throughput_ops_per_sec']:.0f} ops/sec")
    print(f"Efficiency: {benchmark['efficiency_rating']}")
    
    # Rapport global
    print("\n📈 RAPPORT PERFORMANCE")
    report = analytics.generate_performance_report()
    print(f"Overall health: {report['overall_health_score']:.1f}%")
    
    return 0


if __name__ == "__main__":
    main()