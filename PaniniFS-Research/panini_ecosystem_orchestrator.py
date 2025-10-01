#!/usr/bin/env python3
"""
Panini Ecosystem Orchestrator - Configuration Complète

Orchestration multi-agent pour TOUT l'écosystème Panini :
- 15 GitHub Projects actifs
- 4 repositories (Panini, PaniniFS-Research, OntoWave, dhatu-*)
- 4 agents (Humain, Copilot, Colab Pro, Autonomous)
- Assignation optimale cross-project

Auteur: Stéphane Denis + Autonomous System
Timestamp: 2025-10-01T14:40:00Z
"""

import os
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Any
from multi_agent_orchestrator import (
    MultiAgentOrchestrator,
    AgentProfile,
    AgentType,
    Task,
    TaskType
)


class PaniniEcosystemOrchestrator(MultiAgentOrchestrator):
    """Orchestrateur spécialisé pour écosystème Panini."""
    
    def __init__(self, workspace_root: str):
        """Initialise avec projets Panini."""
        super().__init__(workspace_root)
        
        # Projets GitHub identifiés
        self.github_projects = {
            15: "Panini - Théorie Information Universelle",
            14: "OntoWave Roadmap",
            13: "PaniniFS Research Strategy 2025",
            12: "[RESEARCH] dhatu-multimodal-learning",
            11: "[RESEARCH] dhatu-linguistics-engine",
            10: "[INTERFACES] dhatu-api-gateway",
            9: "[INTERFACES] dhatu-dashboard",
            8: "[TOOLS] dhatu-evolution-simulator",
            7: "[TOOLS] dhatu-space-visualizer",
            6: "[TOOLS] dhatu-creative-generator",
            5: "[TOOLS] dhatu-pattern-analyzer",
            4: "[CORE] dhatu-gpu-accelerator",
            3: "[CORE] dhatu-web-framework",
            2: "[CORE] dhatu-corpus-manager",
            1: "[CORE] dhatu-universal-compressor"
        }
        
        # Repositories
        self.repositories = {
            "Panini": "https://github.com/stephanedenis/Panini",
            "PaniniFS-Research": "https://github.com/stephanedenis/PaniniFS-Research",
            "OntoWave": "https://github.com/stephanedenis/OntoWave",
            "dhatu-multimodal": "https://github.com/stephanedenis/dhatu-multimodal-learning"
        }
        
        # Mapping projets → repos
        self.project_to_repo = {
            15: "PaniniFS-Research",
            14: "OntoWave",
            13: "PaniniFS-Research",
            12: "dhatu-multimodal",
            11: "Panini",
            10: "Panini",
            9: "Panini",
            8: "Panini",
            7: "Panini",
            6: "Panini",
            5: "Panini",
            4: "Panini",
            3: "Panini",
            2: "Panini",
            1: "Panini"
        }
        
        # Catégories projets
        self.project_categories = {
            "CORE": [1, 2, 3, 4],        # Infrastructure fondamentale
            "TOOLS": [5, 6, 7, 8],       # Outils développement
            "INTERFACES": [9, 10],        # APIs et dashboards
            "RESEARCH": [11, 12, 13, 15], # Recherche fondamentale
            "ROADMAP": [14]               # Stratégie
        }
        
        # Initialisation tâches par projet
        self._initialize_panini_tasks()
    
    def _initialize_panini_tasks(self):
        """Crée tâches initiales pour chaque projet actif."""
        
        # PROJECT #15 - Théorie Information Universelle (ACTIF)
        self.add_task(Task(
            "panini_15_pr_improvements",
            "Améliorer compliance PRs #15-18 (symétries + patterns)",
            TaskType.REFACTORING,
            priority=9,
            requires_human_review=True
        ))
        
        self.add_task(Task(
            "panini_15_iso8601_fixes",
            "Corriger 14 violations ISO 8601 dans docs legacy",
            TaskType.REFACTORING,
            priority=7
        ))
        
        self.add_task(Task(
            "panini_15_corpus_expansion",
            "Étendre corpus multi-format à 100+ contenus",
            TaskType.DATA_ANALYSIS,
            priority=8,
            estimated_duration=7200
        ))
        
        # PROJECT #4 - GPU Accelerator (CORE)
        self.add_task(Task(
            "panini_4_gpu_dhatu_training",
            "Entraîner modèles dhātu sur GPU T4/V100",
            TaskType.ML_TRAINING,
            priority=9,
            requires_gpu=True,
            estimated_duration=3600
        ))
        
        self.add_task(Task(
            "panini_4_embeddings_multilingue",
            "Générer embeddings multilingues 10+ langues",
            TaskType.GPU_COMPUTE,
            priority=8,
            requires_gpu=True,
            estimated_duration=1800
        ))
        
        # PROJECT #2 - Corpus Manager (CORE)
        self.add_task(Task(
            "panini_2_corpus_validation",
            "Valider intégrité corpus 100k+ documents",
            TaskType.VALIDATION,
            priority=7,
            estimated_duration=300
        ))
        
        self.add_task(Task(
            "panini_2_metadata_extraction",
            "Extraire métadonnées traducteurs 100+ profils",
            TaskType.EXTRACTION,
            priority=8,
            estimated_duration=600
        ))
        
        # PROJECT #9 - Dashboard (INTERFACE)
        self.add_task(Task(
            "panini_9_dashboard_deploy",
            "Déployer dashboard GitHub Pages multi-projets",
            TaskType.DOCUMENTATION,
            priority=8,
            requires_human_review=True
        ))
        
        self.add_task(Task(
            "panini_9_realtime_metrics",
            "Implémenter métriques temps réel WebSocket",
            TaskType.REFACTORING,
            priority=6,
            estimated_duration=3600
        ))
        
        # PROJECT #11 - Linguistics Engine (RESEARCH)
        self.add_task(Task(
            "panini_11_symmetry_validation",
            "Valider symétries compose/decompose 50+ dhātu",
            TaskType.VALIDATION,
            priority=9,
            estimated_duration=1800
        ))
        
        self.add_task(Task(
            "panini_11_compression_empirical",
            "Tester compression empirique cross-lingue",
            TaskType.DATA_ANALYSIS,
            priority=8,
            requires_gpu=True,
            estimated_duration=3600
        ))
        
        # PROJECT #12 - Multimodal Learning (RESEARCH)
        self.add_task(Task(
            "panini_12_multimodal_corpus",
            "Créer corpus audio/vidéo/texte aligné",
            TaskType.DATA_ANALYSIS,
            priority=7,
            estimated_duration=7200
        ))
        
        # PROJECT #5 - Pattern Analyzer (TOOL)
        self.add_task(Task(
            "panini_5_bias_detection",
            "Détecter patterns biais culturels/temporels",
            TaskType.DATA_ANALYSIS,
            priority=7,
            estimated_duration=900
        ))
        
        # PROJECT #14 - OntoWave Roadmap (ROADMAP)
        self.add_task(Task(
            "panini_14_roadmap_update",
            "Mettre à jour roadmap Q1 2025 avec résultats",
            TaskType.DOCUMENTATION,
            priority=6,
            requires_human_review=True
        ))
    
    def assign_all_pending_tasks(self) -> Dict[str, Any]:
        """Assigne toutes les tâches pending automatiquement."""
        results = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'assigned': [],
            'failed': [],
            'summary': {}
        }
        
        pending_tasks = [
            task for task in self.tasks.values()
            if task.status == 'pending'
        ]
        
        print(f"\n🎯 Assignation automatique de {len(pending_tasks)} tâches")
        print("=" * 70)
        
        for task in pending_tasks:
            agent_id = self.assign_optimal_agent(task.task_id)
            if agent_id:
                results['assigned'].append({
                    'task_id': task.task_id,
                    'task_title': task.title,
                    'agent_id': agent_id,
                    'agent_name': self.agents[agent_id].name
                })
            else:
                results['failed'].append({
                    'task_id': task.task_id,
                    'task_title': task.title,
                    'reason': 'No capable agent available'
                })
        
        # Résumé par agent
        agent_workloads = {}
        for agent_id, agent in self.agents.items():
            agent_workloads[agent.name] = len(agent.current_tasks)
        
        results['summary'] = {
            'total_assigned': len(results['assigned']),
            'total_failed': len(results['failed']),
            'agent_workloads': agent_workloads
        }
        
        print(f"\n✅ Assignées: {len(results['assigned'])}")
        print(f"❌ Échecs: {len(results['failed'])}")
        print(f"\n📊 Charge par agent:")
        for agent_name, workload in agent_workloads.items():
            print(f"  {agent_name}: {workload} tâches")
        
        return results
    
    def generate_ecosystem_report(self) -> Dict[str, Any]:
        """Génère rapport complet écosystème Panini."""
        report = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'ecosystem': {
                'projects': len(self.github_projects),
                'repositories': len(self.repositories),
                'categories': len(self.project_categories)
            },
            'tasks': {
                'total': len(self.tasks),
                'by_status': {},
                'by_project': {},
                'by_category': {}
            },
            'agents': {},
            'recommendations': []
        }
        
        # Tasks by status
        for status in ['pending', 'assigned', 'in_progress', 'completed']:
            report['tasks']['by_status'][status] = sum(
                1 for t in self.tasks.values() if t.status == status
            )
        
        # Tasks by project (via task_id prefix panini_XX)
        for task_id, task in self.tasks.items():
            if task_id.startswith('panini_'):
                project_num = int(task_id.split('_')[1])
                project_name = self.github_projects.get(project_num, 'Unknown')
                if project_name not in report['tasks']['by_project']:
                    report['tasks']['by_project'][project_name] = 0
                report['tasks']['by_project'][project_name] += 1
        
        # Tasks by category
        for category, projects in self.project_categories.items():
            count = sum(
                1 for task_id in self.tasks
                if task_id.startswith('panini_') and
                int(task_id.split('_')[1]) in projects
            )
            report['tasks']['by_category'][category] = count
        
        # Agents
        for agent_id, agent in self.agents.items():
            report['agents'][agent.name] = {
                'workload': len(agent.current_tasks),
                'completed': agent.completed_tasks,
                'available': agent.is_available(),
                'cost_per_task': agent.cost_per_task
            }
        
        # Recommendations
        if report['tasks']['by_status']['pending'] > 5:
            report['recommendations'].append(
                f"⚠️  {report['tasks']['by_status']['pending']} tâches pending - "
                "Considérer augmenter capacité agents"
            )
        
        gpu_tasks = sum(
            1 for t in self.tasks.values()
            if t.requires_gpu and t.status in ['pending', 'assigned']
        )
        if gpu_tasks > 2:
            report['recommendations'].append(
                f"🎮 {gpu_tasks} tâches GPU waiting - "
                "Prioriser Colab Pro sessions"
            )
        
        human_review = sum(
            1 for t in self.tasks.values()
            if t.requires_human_review and t.status != 'completed'
        )
        if human_review > 0:
            report['recommendations'].append(
                f"👤 {human_review} tâches requièrent review humaine - "
                "Bloquer 30-60min pour review"
            )
        
        return report
    
    def export_ecosystem_state(self) -> Path:
        """Export état complet écosystème."""
        timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H-%M-%SZ')
        output_file = (
            self.workspace_root / 
            f'panini_ecosystem_state_{timestamp}.json'
        )
        
        state = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'ecosystem': {
                'projects': self.github_projects,
                'repositories': self.repositories,
                'project_to_repo': self.project_to_repo,
                'categories': self.project_categories
            },
            'agents': {
                agent_id: agent.to_dict()
                for agent_id, agent in self.agents.items()
            },
            'tasks': {
                task_id: task.to_dict()
                for task_id, task in self.tasks.items()
            },
            'assignments': self.assignment_log,
            'report': self.generate_ecosystem_report()
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=2, ensure_ascii=False)
        
        print(f"✅ État écosystème exporté: {output_file.name}")
        return output_file


def main():
    """Démo orchestrateur écosystème Panini."""
    workspace = "/home/stephane/GitHub/PaniniFS-Research"
    
    print("\n" + "=" * 70)
    print("🌐 PANINI ECOSYSTEM ORCHESTRATOR")
    print("=" * 70 + "\n")
    
    orchestrator = PaniniEcosystemOrchestrator(workspace)
    
    print(f"📊 Écosystème chargé:")
    print(f"  - {len(orchestrator.github_projects)} GitHub Projects")
    print(f"  - {len(orchestrator.repositories)} Repositories")
    print(f"  - {len(orchestrator.tasks)} Tâches initiales")
    print(f"  - {len(orchestrator.agents)} Agents disponibles")
    
    # Assignation automatique
    print("\n" + "-" * 70)
    results = orchestrator.assign_all_pending_tasks()
    
    # Rapport écosystème
    print("\n" + "-" * 70)
    print("📈 RAPPORT ÉCOSYSTÈME PANINI")
    print("-" * 70 + "\n")
    
    report = orchestrator.generate_ecosystem_report()
    
    print(f"Projets: {report['ecosystem']['projects']}")
    print(f"Repositories: {report['ecosystem']['repositories']}")
    print(f"\nTâches par status:")
    for status, count in report['tasks']['by_status'].items():
        print(f"  {status}: {count}")
    
    print(f"\nTâches par catégorie:")
    for category, count in report['tasks']['by_category'].items():
        print(f"  {category}: {count}")
    
    if report['recommendations']:
        print(f"\n💡 Recommandations:")
        for rec in report['recommendations']:
            print(f"  {rec}")
    
    # Export
    print("\n" + "-" * 70)
    output = orchestrator.export_ecosystem_state()
    
    print(f"\n✅ Orchestrateur écosystème Panini prêt !")
    print(f"📊 Utilisez le rapport pour prioriser votre travail")


if __name__ == '__main__':
    main()
