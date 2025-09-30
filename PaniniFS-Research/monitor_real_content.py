#!/usr/bin/env python3
"""
DASHBOARD PANINI RÉEL - MONITORING DU CONTENU ACTUEL
==================================================
Dashboard qui affiche le vrai contenu en cours de traitement
"""

import json
import os
import time
import glob
from pathlib import Path
from datetime import datetime
import subprocess
import re

class PaniniRealContentMonitor:
    def __init__(self):
        self.workspace_root = Path.cwd()
        self.last_check = {}
        self.active_files = []
        self.current_content = {}
        
    def scan_active_files(self):
        """Scanner les fichiers réellement modifiés récemment"""
        active_files = []
        now = time.time()
        
        # Fichiers JSON de données
        json_patterns = [
            "*.json",
            "corpus_*.json", 
            "analyse_*.json",
            "dictionnaire_*.json",
            "dhatu_*.json"
        ]
        
        # Python files actifs
        py_patterns = [
            "*autonomous*.py",
            "*analyse*.py", 
            "*corpus*.py",
            "*dhatu*.py"
        ]
        
        for pattern in json_patterns + py_patterns:
            for file_path in glob.glob(str(self.workspace_root / pattern)):
                file_stat = os.stat(file_path)
                # Modifié dans les dernières 24h
                if now - file_stat.st_mtime < 86400:
                    active_files.append({
                        'path': file_path,
                        'name': os.path.basename(file_path),
                        'modified': datetime.fromtimestamp(file_stat.st_mtime),
                        'size': file_stat.st_size,
                        'type': 'json' if file_path.endswith('.json') else 'python'
                    })
        
        # Trier par dernière modification
        active_files.sort(key=lambda x: x['modified'], reverse=True)
        return active_files[:20]  # Top 20
    
    def read_json_content(self, file_path):
        """Lire le contenu JSON et extraire les infos importantes"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            analysis = {
                'file': os.path.basename(file_path),
                'structure': type(data).__name__,
                'size': len(data) if isinstance(data, (list, dict)) else 1,
                'content_preview': self.analyze_json_structure(data),
                'last_modified': datetime.fromtimestamp(os.path.getmtime(file_path))
            }
            return analysis
        except Exception as e:
            return {'file': os.path.basename(file_path), 'error': str(e)}
    
    def analyze_json_structure(self, data):
        """Analyser la structure du JSON pour comprendre le contenu"""
        if isinstance(data, dict):
            keys = list(data.keys())[:10]  # Premières 10 clés
            analysis = {
                'type': 'dictionary',
                'keys_count': len(data),
                'sample_keys': keys,
                'content_type': self.detect_content_type(data)
            }
            
            # Analyser le contenu spécifique
            if 'dhatu' in str(data).lower():
                analysis['domain'] = 'dhatu_analysis'
                analysis['dhatu_count'] = self.count_dhatu_entries(data)
            elif 'corpus' in str(data).lower():
                analysis['domain'] = 'corpus_data'
                analysis['entries'] = len(data) if isinstance(data, list) else len(data.get('entries', []))
            elif 'analyse' in str(data).lower():
                analysis['domain'] = 'analysis_results'
                analysis['results'] = self.extract_analysis_results(data)
                
            return analysis
            
        elif isinstance(data, list):
            return {
                'type': 'list',
                'length': len(data),
                'sample_items': data[:3] if data else [],
                'item_types': list(set(type(item).__name__ for item in data[:10]))
            }
        
        return {'type': type(data).__name__, 'value': str(data)[:100]}
    
    def detect_content_type(self, data):
        """Détecter le type de contenu basé sur les clés"""
        if isinstance(data, dict):
            keys_str = ' '.join(str(k).lower() for k in data.keys())
            if any(word in keys_str for word in ['dhatu', 'sanskrit', 'root']):
                return 'linguistic_data'
            elif any(word in keys_str for word in ['corpus', 'text', 'document']):
                return 'corpus_data'
            elif any(word in keys_str for word in ['analyse', 'result', 'discovery']):
                return 'analysis_results'
            elif any(word in keys_str for word in ['molecule', 'semantic', 'pattern']):
                return 'semantic_analysis'
        return 'unknown'
    
    def count_dhatu_entries(self, data):
        """Compter les entrées dhātu"""
        count = 0
        def count_recursive(obj):
            nonlocal count
            if isinstance(obj, dict):
                for key, value in obj.items():
                    if 'dhatu' in str(key).lower():
                        count += 1
                    count_recursive(value)
            elif isinstance(obj, list):
                for item in obj:
                    count_recursive(item)
        count_recursive(data)
        return count
    
    def extract_analysis_results(self, data):
        """Extraire les résultats d'analyse"""
        results = {}
        if isinstance(data, dict):
            for key, value in data.items():
                if any(word in str(key).lower() for word in ['result', 'analyse', 'discovery', 'pattern']):
                    if isinstance(value, (list, dict)):
                        results[key] = len(value) if isinstance(value, list) else len(value)
                    else:
                        results[key] = str(value)[:50]
        return results
    
    def check_running_processes(self):
        """Vérifier les processus Python Panini en cours"""
        try:
            result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
            processes = []
            for line in result.stdout.split('\n'):
                if 'python' in line and any(keyword in line for keyword in 
                    ['panini', 'autonomous', 'corpus', 'dhatu', 'analyse']):
                    processes.append({
                        'command': ' '.join(line.split()[10:]),
                        'pid': line.split()[1],
                        'cpu': line.split()[2],
                        'memory': line.split()[3]
                    })
            return processes
        except:
            return []
    
    def get_recent_log_entries(self):
        """Récupérer les entrées de log récentes"""
        log_files = glob.glob('*.log') + glob.glob('**//*.log', recursive=True)
        recent_logs = []
        
        for log_file in log_files:
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()[-10:]  # 10 dernières lignes
                    for line in lines:
                        if line.strip():
                            recent_logs.append({
                                'file': os.path.basename(log_file),
                                'content': line.strip(),
                                'timestamp': datetime.now()  # Approximation
                            })
            except:
                continue
        
        return recent_logs[-20:]  # 20 plus récentes
    
    def generate_dashboard_data(self):
        """Générer toutes les données pour le dashboard"""
        return {
            'timestamp': datetime.now().isoformat(),
            'active_files': self.scan_active_files(),
            'json_content': [self.read_json_content(f['path']) for f in self.scan_active_files() if f['type'] == 'json'],
            'running_processes': self.check_running_processes(),
            'recent_logs': self.get_recent_log_entries(),
            'workspace_stats': {
                'total_json_files': len(glob.glob('*.json')),
                'total_py_files': len(glob.glob('*.py')),
                'total_log_files': len(glob.glob('*.log')),
                'workspace_size': sum(os.path.getsize(f) for f in glob.glob('*') if os.path.isfile(f))
            }
        }

def main():
    monitor = PaniniRealContentMonitor()
    
    print("🧠 PANINI REAL CONTENT MONITOR")
    print("=" * 50)
    print("📊 Génération des données réelles...")
    
    data = monitor.generate_dashboard_data()
    
    # Sauvegarder les données pour le dashboard web
    with open('dashboard_real_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, default=str, ensure_ascii=False)
    
    print(f"✅ Données générées: {len(data['active_files'])} fichiers actifs")
    print(f"📁 Contenu JSON: {len(data['json_content'])} fichiers analysés")
    print(f"🔄 Processus: {len(data['running_processes'])} en cours")
    print(f"📝 Logs: {len(data['recent_logs'])} entrées récentes")
    print("\n📄 Fichiers actifs récents:")
    
    for file_info in data['active_files'][:10]:
        print(f"   📄 {file_info['name']} - {file_info['modified'].strftime('%H:%M:%S')} ({file_info['size']} bytes)")
    
    print("\n🔍 Contenu JSON analysé:")
    for content in data['json_content'][:5]:
        if 'error' not in content:
            print(f"   📊 {content['file']} - {content['content_preview']['type']} ({content['size']} items)")
            if 'domain' in content['content_preview']:
                print(f"      🎯 Domaine: {content['content_preview']['domain']}")

if __name__ == "__main__":
    main()