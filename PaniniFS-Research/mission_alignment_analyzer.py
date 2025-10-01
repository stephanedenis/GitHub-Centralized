#!/usr/bin/env python3
"""
Mission Alignment Analyzer - Audit Cohérence Écosystème Panini

Analyse l'alignement et la cohérence entre:
- GitHub Projects actifs
- PRs en cours
- Tâches orchestrateur
- Documentation mission
- Vision/Stratégie actuelle

Détecte:
- Projets obsolètes (vestiges anciennes versions)
- Incohérences objectifs
- Duplications efforts
- Gaps stratégiques
- Conflits priorités

Pattern: *_analyzer.py (auto-approved via whitelist)

Auteur: Autonomous System
Timestamp: 2025-10-01T15:00:00Z
"""

import os
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Any, Set, Tuple


class MissionAlignmentAnalyzer:
    """Analyseur alignement missions écosystème Panini."""
    
    def __init__(self, workspace_root: str):
        """Initialise l'analyseur."""
        self.workspace_root = Path(workspace_root)
        
        # Scan documents stratégiques
        self.strategic_docs = self._scan_strategic_documents()
        
        # Parse GitHub Projects
        self.github_projects = self._load_github_projects()
        
        # Parse orchestrateur tasks
        self.orchestrator_tasks = self._load_orchestrator_tasks()
        
        # Parse PRs actifs
        self.active_prs = self._scan_active_prs()
        
        # Résultats analyse
        self.alignment_report = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'status': 'ANALYZING',
            'issues': [],
            'recommendations': [],
            'coherence_score': 0.0
        }
    
    def _scan_strategic_documents(self) -> Dict[str, Any]:
        """Scan documents stratégiques pour extraire vision actuelle."""
        docs = {}
        
        # Documents clés à analyser
        key_docs = [
            'README_MISSION_PANINI.md',
            'STRATEGIE_RAFFINEE_PLAN_TRAVAIL.md',
            'CLARIFICATIONS_MISSION_CRITIQUE.md',
            'SYNTHESE_CLARIFICATIONS_INTEGREES.md',
            'SESSION_COMPLETE_SYNTHESE_EXECUTIVE.md',
            'PANINI_ECOSYSTEM_ORCHESTRATOR_GUIDE.md'
        ]
        
        for doc_name in key_docs:
            doc_path = self.workspace_root / doc_name
            if doc_path.exists():
                docs[doc_name] = self._parse_strategic_doc(doc_path)
        
        return docs
    
    def _parse_strategic_doc(self, doc_path: Path) -> Dict[str, Any]:
        """Parse un document stratégique."""
        with open(doc_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extraction dates (détection obsolescence)
        dates = re.findall(r'\*\*Date\*\*\s*:\s*(\d{4}-\d{2}-\d{2})', content)
        
        # Extraction objectifs (headers avec verbes action)
        objectives = re.findall(
            r'(?:##|###)\s+(?:✅|❌|⚠️|🎯)?\s*(.+?)(?:\n|$)',
            content
        )
        
        # Extraction métriques success
        metrics = re.findall(
            r'(?:Métriques?|Success|Target|Objectif)\s*[:\-]\s*(.+?)(?:\n|$)',
            content,
            re.IGNORECASE
        )
        
        # Extraction projets mentionnés
        projects_mentioned = re.findall(
            r'(?:Project|Projet)\s*#?(\d+)',
            content,
            re.IGNORECASE
        )
        
        # Extraction warnings/deprecated
        warnings = re.findall(
            r'(?:⚠️|ATTENTION|WARNING|OBSOLETE|DEPRECATED)(.+?)(?:\n|$)',
            content,
            re.IGNORECASE
        )
        
        return {
            'path': str(doc_path),
            'size': len(content),
            'dates': dates,
            'objectives': objectives[:10],  # Top 10
            'metrics': metrics[:5],
            'projects_mentioned': list(set(projects_mentioned)),
            'warnings': warnings,
            'last_modified': datetime.fromtimestamp(
                doc_path.stat().st_mtime
            ).isoformat()
        }
    
    def _load_github_projects(self) -> Dict[int, Dict[str, Any]]:
        """Charge définitions GitHub Projects."""
        # Depuis panini_ecosystem_orchestrator.py
        return {
            15: {
                "name": "Panini - Théorie Information Universelle",
                "status": "ACTIF",
                "category": "RESEARCH",
                "priority": "CRITIQUE"
            },
            14: {
                "name": "OntoWave Roadmap",
                "status": "ACTIF",
                "category": "ROADMAP",
                "priority": "STRATÉGIQUE"
            },
            13: {
                "name": "PaniniFS Research Strategy 2025",
                "status": "ACTIF",
                "category": "RESEARCH",
                "priority": "HAUTE"
            },
            12: {
                "name": "[RESEARCH] dhatu-multimodal-learning",
                "status": "PLANIFIÉ",
                "category": "RESEARCH",
                "priority": "MOYENNE"
            },
            11: {
                "name": "[RESEARCH] dhatu-linguistics-engine",
                "status": "ACTIF",
                "category": "RESEARCH",
                "priority": "HAUTE"
            },
            10: {
                "name": "[INTERFACES] dhatu-api-gateway",
                "status": "PLANIFIÉ",
                "category": "INTERFACES",
                "priority": "MOYENNE"
            },
            9: {
                "name": "[INTERFACES] dhatu-dashboard",
                "status": "ACTIF",
                "category": "INTERFACES",
                "priority": "HAUTE"
            },
            8: {
                "name": "[TOOLS] dhatu-evolution-simulator",
                "status": "PLANIFIÉ",
                "category": "TOOLS",
                "priority": "BASSE"
            },
            7: {
                "name": "[TOOLS] dhatu-space-visualizer",
                "status": "PLANIFIÉ",
                "category": "TOOLS",
                "priority": "BASSE"
            },
            6: {
                "name": "[TOOLS] dhatu-creative-generator",
                "status": "PLANIFIÉ",
                "category": "TOOLS",
                "priority": "BASSE"
            },
            5: {
                "name": "[TOOLS] dhatu-pattern-analyzer",
                "status": "PLANIFIÉ",
                "category": "TOOLS",
                "priority": "MOYENNE"
            },
            4: {
                "name": "[CORE] dhatu-gpu-accelerator",
                "status": "ACTIF",
                "category": "CORE",
                "priority": "HAUTE"
            },
            3: {
                "name": "[CORE] dhatu-web-framework",
                "status": "PLANIFIÉ",
                "category": "CORE",
                "priority": "MOYENNE"
            },
            2: {
                "name": "[CORE] dhatu-corpus-manager",
                "status": "ACTIF",
                "category": "CORE",
                "priority": "HAUTE"
            },
            1: {
                "name": "[CORE] dhatu-universal-compressor",
                "status": "ACTIF",
                "category": "CORE",
                "priority": "CRITIQUE"
            }
        }
    
    def _load_orchestrator_tasks(self) -> Dict[str, Dict[str, Any]]:
        """Charge tâches orchestrateur."""
        # Parse panini_ecosystem_state_*.json le plus récent
        state_files = list(self.workspace_root.glob('panini_ecosystem_state_*.json'))
        
        if not state_files:
            return {}
        
        latest_state = max(state_files, key=lambda p: p.stat().st_mtime)
        
        with open(latest_state, 'r', encoding='utf-8') as f:
            state = json.load(f)
        
        return state.get('tasks', {})
    
    def _scan_active_prs(self) -> List[Dict[str, Any]]:
        """Scan PRs actifs depuis documents."""
        prs = []
        
        # Parse SYNTHESE_CLARIFICATIONS_INTEGREES.md
        synthese_path = self.workspace_root / 'SYNTHESE_CLARIFICATIONS_INTEGREES.md'
        if synthese_path.exists():
            with open(synthese_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract PR info
            pr_matches = re.findall(
                r'PR\s*#(\d+)[^\n]*?\n[^\n]*?(.+?)(?:\n\n|\Z)',
                content,
                re.DOTALL
            )
            
            for pr_num, description in pr_matches:
                prs.append({
                    'number': int(pr_num),
                    'description': description.strip()[:100]
                })
        
        return prs
    
    def analyze_alignment(self) -> Dict[str, Any]:
        """Analyse alignement complet."""
        print("\n🔍 ANALYSE ALIGNEMENT MISSIONS PANINI")
        print("=" * 70)
        
        # 1. Détection projets obsolètes
        self._detect_obsolete_projects()
        
        # 2. Analyse cohérence objectifs
        self._analyze_objectives_coherence()
        
        # 3. Détection duplications
        self._detect_duplications()
        
        # 4. Gaps stratégiques
        self._identify_strategic_gaps()
        
        # 5. Conflits priorités
        self._detect_priority_conflicts()
        
        # 6. Score cohérence global
        self._compute_coherence_score()
        
        # 7. Recommandations
        self._generate_recommendations()
        
        self.alignment_report['status'] = 'COMPLETED'
        
        return self.alignment_report
    
    def _detect_obsolete_projects(self):
        """Détecte projets potentiellement obsolètes."""
        print("\n📊 1. Détection Projets Obsolètes")
        print("-" * 70)
        
        obsolete_candidates = []
        
        # Critères obsolescence
        for proj_id, proj_info in self.github_projects.items():
            issues = []
            
            # Status PLANIFIÉ + Priority BASSE = potentiellement obsolète
            if (proj_info['status'] == 'PLANIFIÉ' and 
                proj_info['priority'] == 'BASSE'):
                issues.append("Status PLANIFIÉ + Priority BASSE")
            
            # Pas de tâches orchestrateur associées
            has_tasks = any(
                f"panini_{proj_id}_" in task_id
                for task_id in self.orchestrator_tasks
            )
            if not has_tasks and proj_info['status'] == 'PLANIFIÉ':
                issues.append("Aucune tâche orchestrateur")
            
            # Pas mentionné dans docs stratégiques récents
            mentioned = any(
                str(proj_id) in doc['projects_mentioned']
                for doc in self.strategic_docs.values()
            )
            if not mentioned and proj_info['status'] == 'PLANIFIÉ':
                issues.append("Non mentionné docs stratégiques")
            
            if issues:
                obsolete_candidates.append({
                    'project_id': proj_id,
                    'name': proj_info['name'],
                    'issues': issues,
                    'severity': 'HIGH' if len(issues) >= 2 else 'MEDIUM'
                })
        
        if obsolete_candidates:
            self.alignment_report['issues'].append({
                'type': 'OBSOLETE_PROJECTS',
                'count': len(obsolete_candidates),
                'details': obsolete_candidates
            })
            
            print(f"⚠️  {len(obsolete_candidates)} projets potentiellement obsolètes:")
            for candidate in obsolete_candidates:
                print(f"  - Project #{candidate['project_id']}: {candidate['name']}")
                for issue in candidate['issues']:
                    print(f"    • {issue}")
        else:
            print("✅ Aucun projet obsolète détecté")
    
    def _analyze_objectives_coherence(self):
        """Analyse cohérence objectifs entre documents."""
        print("\n📊 2. Cohérence Objectifs")
        print("-" * 70)
        
        # Extraction objectifs de tous les docs
        all_objectives = []
        for doc_name, doc_data in self.strategic_docs.items():
            for obj in doc_data['objectives']:
                all_objectives.append({
                    'source': doc_name,
                    'text': obj,
                    'date': doc_data['dates'][0] if doc_data['dates'] else 'UNKNOWN'
                })
        
        # Détection contradictions (keywords opposés)
        contradictions = []
        opposite_pairs = [
            ('100%', 'seuil'),
            ('binaire', 'pourcentage'),
            ('compose/decompose', 'identité'),
            ('QUI/QUAND', 'number'),
            ('écosystème', 'seulement')
        ]
        
        for obj1 in all_objectives:
            for obj2 in all_objectives:
                if obj1['source'] != obj2['source']:
                    for keyword1, keyword2 in opposite_pairs:
                        if (keyword1.lower() in obj1['text'].lower() and
                            keyword2.lower() in obj2['text'].lower()):
                            contradictions.append({
                                'doc1': obj1['source'],
                                'doc2': obj2['source'],
                                'conflict': f"{keyword1} vs {keyword2}",
                                'severity': 'MEDIUM'
                            })
        
        if contradictions:
            self.alignment_report['issues'].append({
                'type': 'OBJECTIVE_CONTRADICTIONS',
                'count': len(contradictions),
                'details': contradictions[:5]  # Top 5
            })
            print(f"⚠️  {len(contradictions)} contradictions potentielles détectées")
        else:
            print("✅ Objectifs cohérents entre documents")
    
    def _detect_duplications(self):
        """Détecte duplications efforts."""
        print("\n📊 3. Duplications Efforts")
        print("-" * 70)
        
        duplications = []
        
        # Analyse tâches similaires
        task_themes = {}
        for task_id, task_data in self.orchestrator_tasks.items():
            # Extract theme (keywords principaux)
            title = task_data.get('title', '').lower()
            
            for keyword in ['validation', 'extraction', 'dashboard', 
                           'corpus', 'training', 'embeddings']:
                if keyword in title:
                    if keyword not in task_themes:
                        task_themes[keyword] = []
                    task_themes[keyword].append(task_id)
        
        # Duplication si 3+ tâches même thème
        for theme, task_ids in task_themes.items():
            if len(task_ids) >= 3:
                duplications.append({
                    'theme': theme,
                    'task_count': len(task_ids),
                    'task_ids': task_ids,
                    'severity': 'MEDIUM'
                })
        
        if duplications:
            self.alignment_report['issues'].append({
                'type': 'EFFORT_DUPLICATIONS',
                'count': len(duplications),
                'details': duplications
            })
            print(f"⚠️  {len(duplications)} potentielles duplications:")
            for dup in duplications:
                print(f"  - Thème '{dup['theme']}': {dup['task_count']} tâches")
        else:
            print("✅ Aucune duplication majeure détectée")
    
    def _identify_strategic_gaps(self):
        """Identifie gaps stratégiques."""
        print("\n📊 4. Gaps Stratégiques")
        print("-" * 70)
        
        gaps = []
        
        # Projets ACTIF sans tâches
        for proj_id, proj_info in self.github_projects.items():
            if proj_info['status'] == 'ACTIF':
                has_tasks = any(
                    f"panini_{proj_id}_" in task_id
                    for task_id in self.orchestrator_tasks
                )
                if not has_tasks:
                    gaps.append({
                        'type': 'MISSING_TASKS',
                        'project_id': proj_id,
                        'project_name': proj_info['name'],
                        'severity': 'HIGH' if proj_info['priority'] == 'CRITIQUE' else 'MEDIUM'
                    })
        
        # Catégories sous-représentées
        category_tasks = {}
        for task_id in self.orchestrator_tasks:
            if task_id.startswith('panini_'):
                proj_id = int(task_id.split('_')[1])
                category = self.github_projects[proj_id]['category']
                category_tasks[category] = category_tasks.get(category, 0) + 1
        
        # CORE devrait avoir le plus de tâches
        if category_tasks.get('CORE', 0) < category_tasks.get('TOOLS', 0):
            gaps.append({
                'type': 'CATEGORY_IMBALANCE',
                'issue': 'TOOLS > CORE tasks (inversé)',
                'severity': 'HIGH'
            })
        
        if gaps:
            self.alignment_report['issues'].append({
                'type': 'STRATEGIC_GAPS',
                'count': len(gaps),
                'details': gaps
            })
            print(f"⚠️  {len(gaps)} gaps stratégiques identifiés")
        else:
            print("✅ Couverture stratégique complète")
    
    def _detect_priority_conflicts(self):
        """Détecte conflits priorités."""
        print("\n📊 5. Conflits Priorités")
        print("-" * 70)
        
        conflicts = []
        
        # Projets CRITIQUE sans tâches high priority
        for proj_id, proj_info in self.github_projects.items():
            if proj_info['priority'] == 'CRITIQUE':
                high_priority_tasks = [
                    task_id for task_id, task_data in self.orchestrator_tasks.items()
                    if f"panini_{proj_id}_" in task_id and
                    task_data.get('priority', 0) >= 8
                ]
                if not high_priority_tasks:
                    conflicts.append({
                        'type': 'PRIORITY_MISMATCH',
                        'project_id': proj_id,
                        'project_name': proj_info['name'],
                        'issue': 'Project CRITIQUE mais aucune tâche priority ≥8',
                        'severity': 'HIGH'
                    })
        
        if conflicts:
            self.alignment_report['issues'].append({
                'type': 'PRIORITY_CONFLICTS',
                'count': len(conflicts),
                'details': conflicts
            })
            print(f"⚠️  {len(conflicts)} conflits priorités")
        else:
            print("✅ Priorités cohérentes")
    
    def _compute_coherence_score(self):
        """Calcule score cohérence global."""
        print("\n📊 6. Score Cohérence Global")
        print("-" * 70)
        
        # Score basé sur issues détectées
        total_issues = len(self.alignment_report['issues'])
        
        # Pondération par severity
        severity_weights = {'HIGH': 3, 'MEDIUM': 2, 'LOW': 1}
        weighted_issues = 0
        
        for issue_group in self.alignment_report['issues']:
            for detail in issue_group.get('details', []):
                severity = detail.get('severity', 'MEDIUM')
                weighted_issues += severity_weights[severity]
        
        # Score sur 100 (100 = parfait, 0 = chaos)
        max_expected_issues = 20  # Projection
        score = max(0, 100 - (weighted_issues / max_expected_issues) * 100)
        
        self.alignment_report['coherence_score'] = score
        
        if score >= 90:
            status = "EXCELLENT ✅"
        elif score >= 75:
            status = "BON ✅"
        elif score >= 60:
            status = "ACCEPTABLE ⚠️"
        else:
            status = "BESOIN REFACTORING ❌"
        
        print(f"Score: {score:.1f}/100 - {status}")
        print(f"Issues totales: {total_issues}")
        print(f"Issues pondérées: {weighted_issues}")
    
    def _generate_recommendations(self):
        """Génère recommandations."""
        print("\n📊 7. Recommandations")
        print("-" * 70)
        
        recommendations = []
        
        # Basé sur issues détectées
        for issue_group in self.alignment_report['issues']:
            issue_type = issue_group['type']
            
            if issue_type == 'OBSOLETE_PROJECTS':
                recommendations.append({
                    'priority': 'HIGH',
                    'action': 'ARCHIVE_PROJECTS',
                    'description': f"Archiver {issue_group['count']} projets obsolètes",
                    'projects': [d['project_id'] for d in issue_group['details']]
                })
            
            elif issue_type == 'STRATEGIC_GAPS':
                recommendations.append({
                    'priority': 'HIGH',
                    'action': 'ADD_TASKS',
                    'description': f"Créer tâches pour {issue_group['count']} gaps",
                    'details': issue_group['details']
                })
            
            elif issue_type == 'PRIORITY_CONFLICTS':
                recommendations.append({
                    'priority': 'HIGH',
                    'action': 'ADJUST_PRIORITIES',
                    'description': f"Corriger {issue_group['count']} conflits priorités"
                })
            
            elif issue_type == 'EFFORT_DUPLICATIONS':
                recommendations.append({
                    'priority': 'MEDIUM',
                    'action': 'CONSOLIDATE_TASKS',
                    'description': f"Consolider {issue_group['count']} duplications"
                })
        
        # Recommandations générales
        if self.alignment_report['coherence_score'] < 75:
            recommendations.append({
                'priority': 'CRITICAL',
                'action': 'STRATEGIC_REVIEW',
                'description': 'Session review stratégique complète recommandée'
            })
        
        self.alignment_report['recommendations'] = recommendations
        
        if recommendations:
            print(f"\n💡 {len(recommendations)} recommandations:")
            for rec in recommendations:
                print(f"  [{rec['priority']}] {rec['action']}: {rec['description']}")
        else:
            print("✅ Aucune action requise - alignement optimal")
    
    def export_report(self, output_file: Optional[Path] = None) -> Path:
        """Export rapport alignement."""
        if output_file is None:
            timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H-%M-%SZ')
            output_file = (
                self.workspace_root /
                f'mission_alignment_report_{timestamp}.json'
            )
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.alignment_report, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Rapport exporté: {output_file.name}")
        return output_file


def main():
    """Point d'entrée principal."""
    workspace = "/home/stephane/GitHub/PaniniFS-Research"
    
    analyzer = MissionAlignmentAnalyzer(workspace)
    
    # Analyse complète
    report = analyzer.analyze_alignment()
    
    # Export
    output = analyzer.export_report()
    
    # Résumé final
    print("\n" + "=" * 70)
    print(f"📊 RÉSUMÉ ANALYSE ALIGNEMENT")
    print("=" * 70)
    print(f"Score cohérence: {report['coherence_score']:.1f}/100")
    print(f"Issues détectées: {len(report['issues'])}")
    print(f"Recommandations: {len(report['recommendations'])}")
    
    if report['coherence_score'] >= 75:
        print(f"\n✅ Alignement satisfaisant - Prêt à activer ressources")
    else:
        print(f"\n⚠️  Alignement insuffisant - Review recommandée avant activation")


if __name__ == '__main__':
    main()
