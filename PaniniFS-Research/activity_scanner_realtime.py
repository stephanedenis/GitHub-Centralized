#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SCANNER ACTIVITÉ TEMPS RÉEL - SUJETS DU MOMENT
==============================================
Capture les vraies activités en cours pour dashboard dynamique :
- Fichiers modifiés récemment avec contenu analysé
- Processus actifs avec progression
- Logs en temps réel avec extraction concepts
- Patterns émergents et sujets chauds
- Évolutions dhātu et données en mouvement
"""

import os
import json
import subprocess
import logging
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import time
import re


class RealTimeActivityScanner:
    """Scanner d'activité temps réel pour capturer ce qui bouge vraiment"""
    
    def __init__(self):
        self.base_paths = [
            "/home/stephane/GitHub/Panini",
            "/home/stephane/GitHub/PaniniFS", 
            "/home/stephane/GitHub/PaniniFS-Research"
        ]
        self.hot_topics = []
        self.activity_threshold_hours = 24  # Activité récente = 24h
        
    def scan_recent_modifications(self) -> Dict[str, Any]:
        """Scanner les modifications récentes avec analyse de contenu"""
        recent_files = []
        cutoff_time = datetime.now() - timedelta(hours=self.activity_threshold_hours)
        
        for base_path in self.base_paths:
            if not os.path.exists(base_path):
                continue
                
            # Fichiers modifiés récemment
            cmd = f"find {base_path} -type f -mtime -1 -name '*.py' -o -name '*.json' -o -name '*.md'"
            try:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                files = result.stdout.strip().split('\n') if result.stdout.strip() else []
                
                for file_path in files:
                    if not file_path:
                        continue
                        
                    try:
                        stat = os.stat(file_path)
                        mod_time = datetime.fromtimestamp(stat.st_mtime)
                        
                        if mod_time > cutoff_time:
                            content_analysis = self.analyze_file_content(file_path)
                            recent_files.append({
                                'path': file_path,
                                'name': os.path.basename(file_path),
                                'modified': mod_time.isoformat(),
                                'size': stat.st_size,
                                'type': self.classify_file_type(file_path),
                                'content_analysis': content_analysis,
                                'activity_score': self.calculate_activity_score(content_analysis)
                            })
                    except Exception as e:
                        continue
                        
            except Exception as e:
                continue
        
        # Trier par score d'activité
        recent_files.sort(key=lambda x: x['activity_score'], reverse=True)
        return {
            'recent_modifications': recent_files[:20],  # Top 20
            'total_active_files': len(recent_files),
            'scan_time': datetime.now().isoformat()
        }
    
    def analyze_file_content(self, file_path: str) -> Dict[str, Any]:
        """Analyser le contenu pour identifier les sujets actifs"""
        analysis = {
            'hot_keywords': [],
            'concepts': [],
            'research_topics': [],
            'dhatu_references': 0,
            'activity_indicators': []
        }
        
        try:
            # Lire début et fin du fichier pour analyse rapide
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read(5000)  # Premier 5KB
                
            # Mots-clés chauds
            hot_patterns = [
                r'(dhatu|dhātu)',
                r'(sémantique|semantic)',
                r'(recherche|research)',
                r'(autonome|autonomous)',
                r'(théorie|theory)',
                r'(information|universal)',
                r'(panini|Panini)',
                r'(corpus|collection)',
                r'(analyse|analysis)',
                r'(évolution|evolution)'
            ]
            
            for pattern in hot_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                if matches:
                    analysis['hot_keywords'].extend(matches)
            
            # Concepts spécifiques
            concept_patterns = [
                r'class\s+(\w+)',
                r'def\s+(\w+)',
                r'"([^"]*(?:dhatu|semantic|universal)[^"]*)"',
                r'#.*?(TODO|FIXME|NOTE|BUG).*',
                r'@dataclass.*?class\s+(\w+)'
            ]
            
            for pattern in concept_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                analysis['concepts'].extend([m if isinstance(m, str) else m[0] for m in matches])
            
            # Indicateurs d'activité
            if 'in_progress' in content.lower():
                analysis['activity_indicators'].append('work_in_progress')
            if any(word in content.lower() for word in ['développement', 'development', 'en cours']):
                analysis['activity_indicators'].append('active_development')
            if 'TODO' in content:
                analysis['activity_indicators'].append('has_todos')
            if any(word in content.lower() for word in ['autonome', 'autonomous', 'auto']):
                analysis['activity_indicators'].append('autonomous_system')
                
            analysis['dhatu_references'] = len(re.findall(r'dhatu|dhātu', content, re.IGNORECASE))
            
        except Exception as e:
            analysis['error'] = str(e)
            
        return analysis
    
    def classify_file_type(self, file_path: str) -> str:
        """Classifier le type de fichier pour l'activité"""
        name = os.path.basename(file_path).lower()
        
        if 'dhatu' in name:
            return 'dhatu_work'
        elif 'semantic' in name or 'semantique' in name:
            return 'semantic_research'
        elif 'recherche' in name or 'research' in name:
            return 'research_active'
        elif 'autonome' in name or 'autonomous' in name:
            return 'autonomous_system'
        elif 'corpus' in name or 'collection' in name:
            return 'corpus_work'
        elif 'analyse' in name or 'analysis' in name:
            return 'analysis_work'
        elif name.endswith('.py'):
            return 'python_code'
        elif name.endswith('.json'):
            return 'data_file'
        elif name.endswith('.md'):
            return 'documentation'
        else:
            return 'other'
    
    def calculate_activity_score(self, content_analysis: Dict[str, Any]) -> float:
        """Calculer un score d'activité basé sur le contenu"""
        score = 0.0
        
        # Bonus pour les mots-clés chauds
        score += len(content_analysis.get('hot_keywords', [])) * 0.5
        
        # Bonus pour les références dhātu
        score += content_analysis.get('dhatu_references', 0) * 1.0
        
        # Bonus pour les indicateurs d'activité
        score += len(content_analysis.get('activity_indicators', [])) * 2.0
        
        # Bonus pour les concepts
        score += len(content_analysis.get('concepts', [])) * 0.3
        
        return min(score, 10.0)  # Cap à 10
    
    def scan_active_processes(self) -> Dict[str, Any]:
        """Scanner les processus actifs liés aux travaux"""
        active_processes = []
        
        try:
            # Chercher processus Python avec patterns pertinents
            cmd = "ps aux | grep -E 'python.*panini|python.*dhatu|python.*corpus|python.*research' | grep -v grep"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            for line in result.stdout.strip().split('\n'):
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 11:
                        process_info = {
                            'pid': parts[1],
                            'cpu': parts[2],
                            'mem': parts[3],
                            'command': ' '.join(parts[10:]),
                            'activity_type': self.classify_process_activity(' '.join(parts[10:]))
                        }
                        active_processes.append(process_info)
                        
        except Exception as e:
            pass
        
        return {
            'active_processes': active_processes,
            'process_count': len(active_processes),
            'scan_time': datetime.now().isoformat()
        }
    
    def classify_process_activity(self, command: str) -> str:
        """Classifier l'activité du processus"""
        command_lower = command.lower()
        
        if 'dhatu' in command_lower:
            return 'dhatu_processing'
        elif 'corpus' in command_lower:
            return 'corpus_collection'
        elif 'research' in command_lower or 'recherche' in command_lower:
            return 'research_active'
        elif 'semantic' in command_lower:
            return 'semantic_analysis'
        elif 'autonomous' in command_lower or 'autonome' in command_lower:
            return 'autonomous_work'
        else:
            return 'general_python'
    
    def extract_hot_topics(self, recent_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extraire les sujets chauds du moment"""
        topics = {}
        
        # Analyser les fichiers récents
        for file_info in recent_data.get('recent_modifications', []):
            content = file_info.get('content_analysis', {})
            
            # Compter les occurrences de concepts
            for keyword in content.get('hot_keywords', []):
                if keyword.lower() not in topics:
                    topics[keyword.lower()] = {
                        'name': keyword,
                        'frequency': 0,
                        'files': [],
                        'activity_score': 0
                    }
                topics[keyword.lower()]['frequency'] += 1
                topics[keyword.lower()]['files'].append(file_info['name'])
                topics[keyword.lower()]['activity_score'] += file_info.get('activity_score', 0)
        
        # Convertir en liste triée par activité
        hot_topics = []
        for topic_data in topics.values():
            if topic_data['frequency'] > 1:  # Seulement sujets récurrents
                hot_topics.append(topic_data)
        
        hot_topics.sort(key=lambda x: x['activity_score'], reverse=True)
        return hot_topics[:10]  # Top 10
    
    def scan_log_activity(self) -> Dict[str, Any]:
        """Scanner l'activité dans les logs récents"""
        log_activity = []
        
        for base_path in self.base_paths:
            log_dir = Path(base_path) / "logs"
            if log_dir.exists():
                try:
                    # Chercher logs récents
                    for log_file in log_dir.glob("*.log"):
                        if log_file.stat().st_mtime > (datetime.now() - timedelta(hours=24)).timestamp():
                            # Lire les dernières lignes
                            try:
                                result = subprocess.run(
                                    f"tail -n 20 {log_file}", 
                                    shell=True, capture_output=True, text=True
                                )
                                if result.stdout:
                                    log_activity.append({
                                        'log_file': str(log_file),
                                        'name': log_file.name,
                                        'recent_lines': result.stdout.strip().split('\n')[-5:],  # 5 dernières
                                        'activity_detected': self.detect_log_activity(result.stdout)
                                    })
                            except Exception:
                                continue
                except Exception:
                    continue
        
        return {
            'log_activity': log_activity,
            'active_logs': len(log_activity),
            'scan_time': datetime.now().isoformat()
        }
    
    def detect_log_activity(self, log_content: str) -> List[str]:
        """Détecter l'activité dans le contenu des logs"""
        indicators = []
        
        if 'progress' in log_content.lower():
            indicators.append('progress_tracking')
        if any(word in log_content.lower() for word in ['error', 'warning', 'exception']):
            indicators.append('issues_detected')
        if 'completed' in log_content.lower():
            indicators.append('tasks_completed')
        if any(word in log_content.lower() for word in ['start', 'begin', 'init']):
            indicators.append('processes_starting')
        if re.search(r'\d+%|\d+/\d+', log_content):
            indicators.append('numerical_progress')
            
        return indicators
    
    def generate_activity_dashboard_data(self) -> Dict[str, Any]:
        """Générer les données pour le dashboard d'activité"""
        print("🔍 Scanning real-time activity...")
        
        # Scanner toutes les activités
        recent_mods = self.scan_recent_modifications()
        active_procs = self.scan_active_processes()
        log_activity = self.scan_log_activity()
        hot_topics = self.extract_hot_topics(recent_mods)
        
        dashboard_data = {
            'timestamp': datetime.now().isoformat(),
            'activity_summary': {
                'active_files': recent_mods['total_active_files'],
                'running_processes': active_procs['process_count'],
                'active_logs': log_activity['active_logs'],
                'hot_topics_count': len(hot_topics)
            },
            'hot_topics': hot_topics,
            'recent_work': recent_mods['recent_modifications'][:10],  # Top 10
            'active_processes': active_procs['active_processes'],
            'log_streams': log_activity['log_activity'],
            'activity_focus': self.identify_activity_focus(recent_mods, hot_topics)
        }
        
        return dashboard_data
    
    def identify_activity_focus(self, recent_mods: Dict, hot_topics: List) -> Dict[str, Any]:
        """Identifier le focus principal d'activité"""
        focus_areas = {}
        
        # Analyser par type de fichier
        for file_info in recent_mods.get('recent_modifications', []):
            file_type = file_info.get('type', 'unknown')
            if file_type not in focus_areas:
                focus_areas[file_type] = {
                    'name': file_type,
                    'file_count': 0,
                    'total_activity_score': 0,
                    'key_files': []
                }
            focus_areas[file_type]['file_count'] += 1
            focus_areas[file_type]['total_activity_score'] += file_info.get('activity_score', 0)
            focus_areas[file_type]['key_files'].append(file_info['name'])
        
        # Identifier le focus principal
        main_focus = max(focus_areas.values(), key=lambda x: x['total_activity_score']) if focus_areas else None
        
        return {
            'main_focus': main_focus,
            'focus_areas': list(focus_areas.values()),
            'recommendation': self.generate_focus_recommendation(main_focus, hot_topics)
        }
    
    def generate_focus_recommendation(self, main_focus: Dict, hot_topics: List) -> str:
        """Générer une recommandation basée sur l'activité"""
        if not main_focus:
            return "Aucune activité significative détectée"
        
        focus_type = main_focus['name']
        
        recommendations = {
            'dhatu_work': "🔬 Focus sur l'analyse dhātu - Évolution des racines verbales active",
            'semantic_research': "🧠 Recherche sémantique intensive - Patterns émergents détectés", 
            'research_active': "📚 Recherche active - Nouvelle théorie en développement",
            'autonomous_system': "🤖 Systèmes autonomes - Processus d'apprentissage en cours",
            'corpus_work': "📊 Travail sur corpus - Collection et analyse de données",
            'analysis_work': "📈 Analyses en cours - Résultats en production"
        }
        
        return recommendations.get(focus_type, f"📋 Activité {focus_type} détectée")


def main():
    """Scanner l'activité temps réel"""
    scanner = RealTimeActivityScanner()
    dashboard_data = scanner.generate_activity_dashboard_data()
    
    # Sauvegarder les données
    output_file = 'activity_dashboard_data.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(dashboard_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Activity data saved to {output_file}")
    
    # Afficher résumé
    summary = dashboard_data['activity_summary']
    print(f"\n📊 ACTIVITÉ TEMPS RÉEL:")
    print(f"   📁 Fichiers actifs: {summary['active_files']}")
    print(f"   🔄 Processus: {summary['running_processes']}")
    print(f"   📝 Logs actifs: {summary['active_logs']}")
    print(f"   🔥 Sujets chauds: {summary['hot_topics_count']}")
    
    if dashboard_data['activity_focus']['main_focus']:
        focus = dashboard_data['activity_focus']['main_focus']
        print(f"\n🎯 FOCUS PRINCIPAL: {focus['name']} ({focus['file_count']} fichiers)")
        print(f"   💡 {dashboard_data['activity_focus']['recommendation']}")
    
    # Top sujets chauds
    if dashboard_data['hot_topics']:
        print(f"\n🔥 SUJETS DU MOMENT:")
        for topic in dashboard_data['hot_topics'][:5]:
            print(f"   🌟 {topic['name']} (score: {topic['activity_score']:.1f})")


if __name__ == "__main__":
    main()