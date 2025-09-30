#!/usr/bin/env python3
"""
DASHBOARD PANINI RÉEL - SCANNER DES VRAIS FICHIERS DE DONNÉES
==========================================================
Dashboard qui lit les vrais fichiers mentionnés dans le contexte initial
"""

import json
import os
import time
import glob
from pathlib import Path
from datetime import datetime, timezone  # Conformité copilotage: timezone UTC
import subprocess
import re

class PaniniRealDataScanner:
    def __init__(self):
        # Scanner les répertoires réels mentionnés dans le contexte
        self.scan_paths = [
            "/home/stephane/GitHub/PaniniFS-Research",
            ".",  # Répertoire actuel
            "../",  # Répertoire parent
        ]
        
        # Fichiers réels mentionnés dans le contexte initial du workspace
        self.real_files_mentioned = [
            "corpus_multilingue_dev.json",
            "corpus_prescolaire.json", 
            "corpus_scientifique.json",
            "corpus_complet_unifie.json",
            "dictionnaire_dhatu_mot_exhaustif.json",
            "dhatu_aspectuels_complete.json",
            "dhatu_aspectual_evolution_results.json",
            "analyse_molecules_semantiques_conte.json",
            "analyse_20250922_085336_en.json",
            "analyse_20250922_085336_fr.json",
            "analyse_onomastique_20250922_090407_en.json",
            "analyse_onomastique_20250922_090407_fr.json",
            "integration_molecules_ultimate.json",
            "demo_accomplishments.json",
            "detailed_failure_analysis.json",
            "etat_gestionnaire_arriere_plan.json",
            "grand_corpus_collection.log",
            "gestionnaire_arriere_plan.log",
            "autonomous_processor.log"
        ]
        
        self.current_analysis = {}
        
    def find_real_files(self):
        """Scanner pour trouver les vrais fichiers de données"""
        found_files = []
        
        # Scanner les patterns de fichiers
        file_patterns = [
            "*.json",
            "*.log", 
            "*corpus*.json",
            "*dhatu*.json", 
            "*analyse*.json",
            "*molecules*.json",
            "*onomastique*.json"
        ]
        
        for scan_path in self.scan_paths:
            for pattern in file_patterns:
                search_pattern = os.path.join(scan_path, "**", pattern)
                for file_path in glob.glob(search_pattern, recursive=True):
                    if os.path.isfile(file_path):
                        file_info = self.analyze_file(file_path)
                        if file_info:
                            found_files.append(file_info)
        
        # Éliminer les doublons
        unique_files = {}
        for file_info in found_files:
            key = file_info['name']
            if key not in unique_files or file_info['modified'] > unique_files[key]['modified']:
                unique_files[key] = file_info
        
        return list(unique_files.values())
    
    def analyze_file(self, file_path):
        """Analyser un fichier individuellement"""
        try:
            file_stat = os.stat(file_path)
            file_info = {
                'path': file_path,
                'name': os.path.basename(file_path),
                'size': file_stat.st_size,
                'modified': datetime.fromtimestamp(file_stat.st_mtime, tz=timezone.utc).isoformat(),  # ISO avec timezone
                'type': self.detect_file_type(file_path),
                'content_summary': None
            }
            
            # Analyser le contenu selon le type
            if file_path.endswith('.json'):
                file_info['content_summary'] = self.analyze_json_file(file_path)
            elif file_path.endswith('.log'):
                file_info['content_summary'] = self.analyze_log_file(file_path)
            elif file_path.endswith('.py'):
                file_info['content_summary'] = self.analyze_python_file(file_path)
            
            return file_info
        
        except Exception as e:
            return {
                'path': file_path,
                'name': os.path.basename(file_path),
                'error': str(e)
            }
    
    def detect_file_type(self, file_path):
        """Détecter le type de contenu du fichier"""
        name = os.path.basename(file_path).lower()
        
        if 'corpus' in name:
            return 'corpus_data'
        elif 'dhatu' in name:
            return 'dhatu_analysis'
        elif 'analyse' in name:
            return 'analysis_results'
        elif 'molecules' in name:
            return 'semantic_molecules'
        elif 'onomastique' in name:
            return 'onomastic_analysis'
        elif name.endswith('.log'):
            return 'log_file'
        elif name.endswith('.py'):
            return 'python_script'
        else:
            return 'data_file'
    
    def analyze_json_file(self, file_path):
        """Analyser le contenu d'un fichier JSON"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            summary = {
                'structure': type(data).__name__,
                'size': len(data) if isinstance(data, (list, dict)) else 1,
                'key_concepts': [],
                'data_points': {}
            }
            
            # Analyser la structure pour extraire les concepts clés
            if isinstance(data, dict):
                # Compter les entrées importantes
                for key, value in data.items():
                    key_lower = str(key).lower()
                    if any(concept in key_lower for concept in ['dhatu', 'sanskrit', 'root']):
                        summary['data_points']['dhatu_entries'] = len(value) if isinstance(value, list) else 1
                    elif any(concept in key_lower for concept in ['corpus', 'text', 'documents']):
                        summary['data_points']['corpus_size'] = len(value) if isinstance(value, list) else 1
                    elif any(concept in key_lower for concept in ['analyse', 'results', 'discoveries']):
                        summary['data_points']['analysis_results'] = len(value) if isinstance(value, list) else 1
                    elif any(concept in key_lower for concept in ['molecules', 'semantic']):
                        summary['data_points']['semantic_molecules'] = len(value) if isinstance(value, list) else 1
                
                # Extraire un échantillon de clés importantes
                important_keys = [k for k in data.keys() if any(concept in str(k).lower() 
                    for concept in ['dhatu', 'corpus', 'analyse', 'molecules', 'universaux', 'pattern'])]
                summary['key_concepts'] = important_keys[:10]
                
            elif isinstance(data, list):
                summary['data_points']['total_items'] = len(data)
                if data:
                    # Analyser le premier élément pour comprendre la structure
                    first_item = data[0]
                    if isinstance(first_item, dict):
                        summary['key_concepts'] = list(first_item.keys())[:5]
            
            return summary
            
        except Exception as e:
            return {'error': f"Erreur lecture JSON: {str(e)}"}
    
    def analyze_log_file(self, file_path):
        """Analyser le contenu d'un fichier log"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            summary = {
                'total_lines': len(lines),
                'recent_entries': [],
                'error_count': 0,
                'info_count': 0,
                'activity_summary': []
            }
            
            # Analyser les dernières lignes pour l'activité récente
            for line in lines[-20:]:  # 20 dernières lignes
                line = line.strip()
                if line:
                    summary['recent_entries'].append({
                        'content': line[:100],  # Premier 100 chars
                        'timestamp': 'extracted' if any(char.isdigit() for char in line[:20]) else 'unknown'
                    })
                    
                    # Compter les types de messages
                    if any(keyword in line.lower() for keyword in ['error', 'erreur', 'failed']):
                        summary['error_count'] += 1
                    elif any(keyword in line.lower() for keyword in ['info', 'success', 'completed']):
                        summary['info_count'] += 1
            
            return summary
            
        except Exception as e:
            return {'error': f"Erreur lecture log: {str(e)}"}
    
    def analyze_python_file(self, file_path):
        """Analyser un fichier Python pour identifier sa fonction"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            summary = {
                'lines': len(content.split('\n')),
                'functions': len(re.findall(r'def\s+(\w+)', content)),
                'classes': len(re.findall(r'class\s+(\w+)', content)),
                'purpose': 'unknown',
                'key_concepts': []
            }
            
            # Identifier le but du script
            content_lower = content.lower()
            if any(keyword in content_lower for keyword in ['autonomous', 'autonome']):
                summary['purpose'] = 'autonomous_system'
            elif any(keyword in content_lower for keyword in ['corpus', 'collection']):
                summary['purpose'] = 'corpus_processing'
            elif any(keyword in content_lower for keyword in ['dhatu', 'sanskrit']):
                summary['purpose'] = 'dhatu_analysis'
            elif any(keyword in content_lower for keyword in ['analyse', 'analysis']):
                summary['purpose'] = 'data_analysis'
            
            # Extraire les concepts clés depuis les commentaires et docstrings
            concepts = re.findall(r'(?:dhatu|corpus|analyse|molecules|universaux|panini)', content_lower)
            summary['key_concepts'] = list(set(concepts))[:10]
            
            return summary
            
        except Exception as e:
            return {'error': f"Erreur lecture Python: {str(e)}"}
    
    def get_system_status(self):
        """État du système et processus actifs"""
        try:
            result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
            panini_processes = []
            
            for line in result.stdout.split('\n'):
                if any(keyword in line.lower() for keyword in ['panini', 'autonomous', 'corpus', 'dhatu']):
                    if 'python' in line:
                        panini_processes.append({
                            'command': ' '.join(line.split()[10:])[:80],
                            'cpu': line.split()[2] if len(line.split()) > 2 else '0',
                            'memory': line.split()[3] if len(line.split()) > 3 else '0'
                        })
            
            return {
                'active_processes': panini_processes,
                'total_processes': len(panini_processes)
            }
        except:
            return {'active_processes': [], 'total_processes': 0}
    
    def generate_real_dashboard_data(self):
        """Générer toutes les données réelles pour le dashboard"""
        print("🔍 Scanner des fichiers réels...")
        files = self.find_real_files()
        
        print("🔄 Analyse état système...")
        system_status = self.get_system_status()
        
        dashboard_data = {
            'timestamp': datetime.now(timezone.utc).isoformat(),  # Conformité copilotage ISO
            'scan_summary': {
                'total_files_found': len(files),
                'file_types': {},
                'total_size': sum(f.get('size', 0) for f in files),
                'most_recent': max([f['modified'] for f in files if 'modified' in f], default=datetime.now(timezone.utc).isoformat()) if files else datetime.now(timezone.utc).isoformat()
            },
            'real_files': files,
            'system_status': system_status,
            'content_analysis': {
                'corpus_files': [f for f in files if f.get('type') == 'corpus_data'],
                'dhatu_files': [f for f in files if f.get('type') == 'dhatu_analysis'],
                'analysis_files': [f for f in files if f.get('type') == 'analysis_results'],
                'log_files': [f for f in files if f.get('type') == 'log_file']
            }
        }
        
        # Compter les types de fichiers
        for file_info in files:
            file_type = file_info.get('type', 'unknown')
            dashboard_data['scan_summary']['file_types'][file_type] = \
                dashboard_data['scan_summary']['file_types'].get(file_type, 0) + 1
        
        return dashboard_data

def main():
    scanner = PaniniRealDataScanner()
    
    print("🧠 PANINI REAL DATA SCANNER")
    print("=" * 50)
    
    # Générer les données réelles
    real_data = scanner.generate_real_dashboard_data()
    
    # Sauvegarder
    with open('panini_real_data.json', 'w', encoding='utf-8') as f:
        json.dump(real_data, f, indent=2, default=str, ensure_ascii=False)
    
    print(f"\n✅ SCAN COMPLÉTÉ")
    print(f"📁 Fichiers trouvés: {real_data['scan_summary']['total_files_found']}")
    print(f"💾 Taille totale: {real_data['scan_summary']['total_size']:,} bytes")
    print(f"🔄 Processus actifs: {real_data['system_status']['total_processes']}")
    
    print(f"\n📊 TYPES DE FICHIERS:")
    for file_type, count in real_data['scan_summary']['file_types'].items():
        print(f"   {file_type}: {count} fichiers")
    
    print(f"\n📄 FICHIERS DE DONNÉES RÉELS:")
    for file_info in real_data['real_files'][:15]:  # Top 15
        if 'error' not in file_info:
            size_kb = file_info['size'] / 1024
            # file_info['modified'] est déjà une chaîne ISO, pas besoin de strftime
            modified_str = file_info['modified'][:16].replace('T', ' ')  # Format lisible
            print(f"   📄 {file_info['name']} ({size_kb:.1f}KB) - {modified_str}")
            if file_info.get('content_summary') and 'data_points' in file_info['content_summary']:
                for key, value in file_info['content_summary']['data_points'].items():
                    print(f"      🔹 {key}: {value}")

if __name__ == "__main__":
    main()