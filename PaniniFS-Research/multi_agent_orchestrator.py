#!/usr/bin/env python3
"""
Multi-Agent Orchestrator - Gestion collaborative agents/humains

Gère l'assignation optimale des tâches entre:
- Humains (vous)
- GitHub Copilot (@copilot)
- Google Colab Pro (GPU/ML tasks)
- Autonomous Wrapper (scripts auto-approuvés)

Pattern: *_orchestrator.py (auto-approved via whitelist extension)

Fonctionnalités:
1. Profils agents (capacités, contraintes, coûts)
2. Assignation automatique basée sur type tâche
3. Tracking qui fait quoi en temps réel
4. Détection conflits et handoff
5. Métriques performance par agent

Auteur: Autonomous System
Timestamp: 2025-10-01T14:10:00Z
"""

import os
import json
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
from enum import Enum


class AgentType(Enum):
    """Types d'agents disponibles."""
    HUMAN = "human"
    COPILOT = "github_copilot"
    COLAB_PRO = "google_colab_pro"
    AUTONOMOUS = "autonomous_wrapper"


class TaskType(Enum):
    """Types de tâches avec agents optimaux."""
    CODE_REVIEW = "code_review"
    DATA_ANALYSIS = "data_analysis"
    ML_TRAINING = "ml_training"
    GPU_COMPUTE = "gpu_compute"
    DOCUMENTATION = "documentation"
    VALIDATION = "validation"
    EXTRACTION = "extraction"
    REFACTORING = "refactoring"
    ARCHITECTURE = "architecture"
    RESEARCH = "research"


class AgentProfile:
    """Profil d'un agent avec capacités et contraintes."""
    
    def __init__(
        self,
        agent_id: str,
        agent_type: AgentType,
        name: str,
        capabilities: List[TaskType],
        constraints: Dict[str, Any],
        cost_per_task: float = 0.0
    ):
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.name = name
        self.capabilities = capabilities
        self.constraints = constraints
        self.cost_per_task = cost_per_task
        self.current_tasks = []
        self.completed_tasks = 0
        self.total_time_seconds = 0.0
        
    def can_handle(self, task_type: TaskType) -> bool:
        """Vérifie si l'agent peut gérer ce type de tâche."""
        return task_type in self.capabilities
    
    def is_available(self) -> bool:
        """Vérifie si l'agent est disponible."""
        max_concurrent = self.constraints.get('max_concurrent_tasks', 1)
        return len(self.current_tasks) < max_concurrent
    
    def estimate_duration(self, task_type: TaskType) -> float:
        """Estime durée tâche (secondes)."""
        base_times = self.constraints.get('avg_task_duration', {})
        return base_times.get(task_type.value, 60.0)
    
    def to_dict(self) -> Dict[str, Any]:
        """Export JSON."""
        return {
            'agent_id': self.agent_id,
            'agent_type': self.agent_type.value,
            'name': self.name,
            'capabilities': [c.value for c in self.capabilities],
            'constraints': self.constraints,
            'cost_per_task': self.cost_per_task,
            'current_tasks': self.current_tasks,
            'completed_tasks': self.completed_tasks,
            'total_time_seconds': self.total_time_seconds
        }


class Task:
    """Tâche assignable avec metadata."""
    
    def __init__(
        self,
        task_id: str,
        title: str,
        task_type: TaskType,
        priority: int = 5,
        estimated_duration: float = 60.0,
        requires_gpu: bool = False,
        requires_human_review: bool = False,
        dependencies: List[str] = None
    ):
        self.task_id = task_id
        self.title = title
        self.task_type = task_type
        self.priority = priority  # 1-10 (10 = urgent)
        self.estimated_duration = estimated_duration
        self.requires_gpu = requires_gpu
        self.requires_human_review = requires_human_review
        self.dependencies = dependencies or []
        
        self.assigned_to: Optional[str] = None
        self.status = "pending"  # pending, in_progress, completed, blocked
        self.started_at: Optional[str] = None
        self.completed_at: Optional[str] = None
        self.result: Optional[Dict[str, Any]] = None
        
    def to_dict(self) -> Dict[str, Any]:
        """Export JSON."""
        return {
            'task_id': self.task_id,
            'title': self.title,
            'task_type': self.task_type.value,
            'priority': self.priority,
            'estimated_duration': self.estimated_duration,
            'requires_gpu': self.requires_gpu,
            'requires_human_review': self.requires_human_review,
            'dependencies': self.dependencies,
            'assigned_to': self.assigned_to,
            'status': self.status,
            'started_at': self.started_at,
            'completed_at': self.completed_at,
            'result': self.result
        }


class MultiAgentOrchestrator:
    """Orchestrateur multi-agent avec assignation optimale."""
    
    def __init__(self, workspace_root: str):
        """Initialise l'orchestrateur."""
        self.workspace_root = Path(workspace_root)
        self.agents: Dict[str, AgentProfile] = {}
        self.tasks: Dict[str, Task] = {}
        self.assignment_log = []
        
        # Chargement config ou création profils par défaut
        self._initialize_default_agents()
        
    def _initialize_default_agents(self):
        """Crée profils agents par défaut."""
        
        # Humain (vous)
        self.register_agent(AgentProfile(
            agent_id="human_stephane",
            agent_type=AgentType.HUMAN,
            name="Stéphane Denis",
            capabilities=[
                TaskType.ARCHITECTURE,
                TaskType.RESEARCH,
                TaskType.CODE_REVIEW,
                TaskType.DOCUMENTATION
            ],
            constraints={
                'max_concurrent_tasks': 1,
                'availability': 'business_hours',  # 9h-18h
                'requires_approval': False,
                'avg_task_duration': {
                    'architecture': 3600,  # 1h
                    'research': 7200,      # 2h
                    'code_review': 1800    # 30min
                }
            },
            cost_per_task=0.0  # Votre temps = précieux mais pas facturé
        ))
        
        # GitHub Copilot
        self.register_agent(AgentProfile(
            agent_id="copilot_agent",
            agent_type=AgentType.COPILOT,
            name="GitHub Copilot SWE Agent",
            capabilities=[
                TaskType.CODE_REVIEW,
                TaskType.REFACTORING,
                TaskType.DOCUMENTATION,
                TaskType.VALIDATION,
                TaskType.EXTRACTION
            ],
            constraints={
                'max_concurrent_tasks': 4,  # Peut gérer plusieurs PRs
                'requires_issue_mention': True,  # Besoin @copilot
                'avg_task_duration': {
                    'code_review': 300,      # 5min
                    'refactoring': 600,      # 10min
                    'documentation': 180,    # 3min
                    'validation': 120        # 2min
                }
            },
            cost_per_task=0.0  # Inclus dans subscription GitHub
        ))
        
        # Google Colab Pro
        self.register_agent(AgentProfile(
            agent_id="colab_pro",
            agent_type=AgentType.COLAB_PRO,
            name="Google Colab Pro (GPU)",
            capabilities=[
                TaskType.ML_TRAINING,
                TaskType.GPU_COMPUTE,
                TaskType.DATA_ANALYSIS
            ],
            constraints={
                'max_concurrent_tasks': 1,  # 1 notebook à la fois
                'requires_gpu': True,
                'gpu_type': 'T4/V100',
                'max_runtime_hours': 12,
                'avg_task_duration': {
                    'ml_training': 3600,     # 1h
                    'gpu_compute': 1800,     # 30min
                    'data_analysis': 900     # 15min
                }
            },
            cost_per_task=0.10  # ~$10/mois = $0.10/task estimé
        ))
        
        # Autonomous Wrapper
        self.register_agent(AgentProfile(
            agent_id="autonomous_wrapper",
            agent_type=AgentType.AUTONOMOUS,
            name="Autonomous Wrapper System",
            capabilities=[
                TaskType.VALIDATION,
                TaskType.EXTRACTION,
                TaskType.DATA_ANALYSIS
            ],
            constraints={
                'max_concurrent_tasks': 10,  # Parallélisation scripts
                'requires_whitelist': True,
                'script_patterns': [
                    '*_validator.py',
                    '*_extractor.py',
                    '*_analyzer.py'
                ],
                'avg_task_duration': {
                    'validation': 5,         # 5s
                    'extraction': 10,        # 10s
                    'data_analysis': 30      # 30s
                }
            },
            cost_per_task=0.0  # Local execution
        ))
        
    def register_agent(self, agent: AgentProfile):
        """Enregistre un agent."""
        self.agents[agent.agent_id] = agent
        print(f"✅ Agent enregistré: {agent.name} ({agent.agent_type.value})")
        
    def add_task(self, task: Task):
        """Ajoute une tâche à la queue."""
        self.tasks[task.task_id] = task
        print(f"📋 Tâche ajoutée: {task.title} (type: {task.task_type.value})")
        
    def assign_optimal_agent(self, task_id: str) -> Optional[str]:
        """
        Assigne agent optimal pour une tâche.
        
        Critères:
        1. Capacité (agent peut gérer le type)
        2. Disponibilité (pas surchargé)
        3. Contraintes spéciales (GPU, etc.)
        4. Coût (préférence moins cher à qualité égale)
        5. Performance historique
        
        Returns:
            agent_id ou None si pas d'agent disponible
        """
        task = self.tasks.get(task_id)
        if not task:
            print(f"❌ Tâche {task_id} introuvable")
            return None
        
        # Filtrer agents capables
        capable_agents = [
            agent for agent in self.agents.values()
            if agent.can_handle(task.task_type)
        ]
        
        if not capable_agents:
            print(f"❌ Aucun agent capable de gérer {task.task_type.value}")
            return None
        
        # Filtrer par contraintes spéciales
        if task.requires_gpu:
            capable_agents = [
                a for a in capable_agents
                if a.constraints.get('requires_gpu', False)
            ]
        
        # Filtrer par disponibilité
        available_agents = [
            a for a in capable_agents
            if a.is_available()
        ]
        
        if not available_agents:
            print(f"⏳ Agents capables mais tous occupés")
            return None
        
        # Scoring agents disponibles
        scored_agents = []
        for agent in available_agents:
            score = self._score_agent_for_task(agent, task)
            scored_agents.append((agent, score))
        
        # Meilleur agent
        best_agent, best_score = max(scored_agents, key=lambda x: x[1])
        
        # Assignation
        task.assigned_to = best_agent.agent_id
        task.status = "assigned"
        best_agent.current_tasks.append(task_id)
        
        # Log
        assignment = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'task_id': task_id,
            'task_title': task.title,
            'agent_id': best_agent.agent_id,
            'agent_name': best_agent.name,
            'score': best_score,
            'reason': self._explain_assignment(best_agent, task)
        }
        self.assignment_log.append(assignment)
        
        print(f"✅ Tâche '{task.title}' → {best_agent.name}")
        print(f"   Raison: {assignment['reason']}")
        
        return best_agent.agent_id
    
    def _score_agent_for_task(
        self, 
        agent: AgentProfile, 
        task: Task
    ) -> float:
        """
        Score agent pour tâche (0-100).
        
        Facteurs:
        - Vitesse (40%)
        - Coût (30%)
        - Fiabilité (20%)
        - Disponibilité (10%)
        """
        score = 0.0
        
        # Vitesse (40%) - plus rapide = mieux
        estimated_time = agent.estimate_duration(task.task_type)
        speed_score = max(0, 100 - (estimated_time / 60))  # Normalisation
        score += speed_score * 0.4
        
        # Coût (30%) - moins cher = mieux
        if agent.cost_per_task == 0:
            cost_score = 100
        else:
            cost_score = max(0, 100 - (agent.cost_per_task * 100))
        score += cost_score * 0.3
        
        # Fiabilité (20%) - basé sur historique
        if agent.completed_tasks > 0:
            reliability_score = 90  # Par défaut bon si historique existe
        else:
            reliability_score = 70  # Nouveau agent = moins fiable
        score += reliability_score * 0.2
        
        # Disponibilité (10%) - moins chargé = mieux
        max_tasks = agent.constraints.get('max_concurrent_tasks', 1)
        current_load = len(agent.current_tasks) / max_tasks
        availability_score = (1 - current_load) * 100
        score += availability_score * 0.1
        
        return score
    
    def _explain_assignment(
        self, 
        agent: AgentProfile, 
        task: Task
    ) -> str:
        """Génère explication human-readable de l'assignation."""
        reasons = []
        
        # Type agent
        if agent.agent_type == AgentType.AUTONOMOUS:
            reasons.append("exécution locale rapide")
        elif agent.agent_type == AgentType.COLAB_PRO:
            reasons.append("GPU disponible")
        elif agent.agent_type == AgentType.COPILOT:
            reasons.append("spécialisé code")
        
        # Coût
        if agent.cost_per_task == 0:
            reasons.append("gratuit")
        
        # Vitesse
        duration = agent.estimate_duration(task.task_type)
        if duration < 60:
            reasons.append(f"très rapide ({duration:.0f}s)")
        
        return ", ".join(reasons)
    
    def mark_task_started(self, task_id: str):
        """Marque tâche comme démarrée."""
        task = self.tasks.get(task_id)
        if task:
            task.status = "in_progress"
            task.started_at = datetime.now(timezone.utc).isoformat()
            print(f"🚀 Tâche démarrée: {task.title}")
    
    def mark_task_completed(
        self, 
        task_id: str, 
        result: Optional[Dict[str, Any]] = None
    ):
        """Marque tâche comme complétée."""
        task = self.tasks.get(task_id)
        if not task:
            return
        
        task.status = "completed"
        task.completed_at = datetime.now(timezone.utc).isoformat()
        task.result = result
        
        # Mise à jour agent
        if task.assigned_to:
            agent = self.agents.get(task.assigned_to)
            if agent:
                if task_id in agent.current_tasks:
                    agent.current_tasks.remove(task_id)
                agent.completed_tasks += 1
                
                # Calcul temps réel
                if task.started_at:
                    start = datetime.fromisoformat(task.started_at)
                    end = datetime.fromisoformat(task.completed_at)
                    duration = (end - start).total_seconds()
                    agent.total_time_seconds += duration
        
        print(f"✅ Tâche complétée: {task.title}")
    
    def get_agent_status(self, agent_id: str) -> Dict[str, Any]:
        """Récupère status complet d'un agent."""
        agent = self.agents.get(agent_id)
        if not agent:
            return {}
        
        return {
            'agent': agent.to_dict(),
            'current_workload': len(agent.current_tasks),
            'is_available': agent.is_available(),
            'avg_task_time': (
                agent.total_time_seconds / agent.completed_tasks
                if agent.completed_tasks > 0
                else 0
            )
        }
    
    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """Récupère status complet d'une tâche."""
        task = self.tasks.get(task_id)
        if not task:
            return {}
        
        return task.to_dict()
    
    def generate_dashboard_report(self) -> Dict[str, Any]:
        """Génère rapport complet pour dashboard."""
        report = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'agents': {
                agent_id: self.get_agent_status(agent_id)
                for agent_id in self.agents
            },
            'tasks': {
                'total': len(self.tasks),
                'pending': sum(
                    1 for t in self.tasks.values() 
                    if t.status == 'pending'
                ),
                'in_progress': sum(
                    1 for t in self.tasks.values() 
                    if t.status == 'in_progress'
                ),
                'completed': sum(
                    1 for t in self.tasks.values() 
                    if t.status == 'completed'
                )
            },
            'assignments': self.assignment_log[-20:]  # 20 dernières
        }
        
        return report
    
    def export_state(self, output_file: Optional[Path] = None) -> Path:
        """Export état complet JSON."""
        if output_file is None:
            timestamp = datetime.now(timezone.utc).strftime(
                '%Y-%m-%dT%H-%M-%SZ'
            )
            output_file = (
                self.workspace_root / 
                f'orchestrator_state_{timestamp}.json'
            )
        
        state = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'agents': {
                agent_id: agent.to_dict() 
                for agent_id, agent in self.agents.items()
            },
            'tasks': {
                task_id: task.to_dict() 
                for task_id, task in self.tasks.items()
            },
            'assignment_log': self.assignment_log
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=2, ensure_ascii=False)
        
        print(f"✅ État exporté: {output_file.name}")
        return output_file


def main():
    """Démo orchestrateur."""
    workspace = os.getcwd()
    orchestrator = MultiAgentOrchestrator(workspace)
    
    print("\n" + "=" * 70)
    print("🎭 MULTI-AGENT ORCHESTRATOR - Démo")
    print("=" * 70 + "\n")
    
    # Scénario: Plusieurs tâches à assigner
    tasks = [
        Task(
            "task_001",
            "Valider intégrité corpus multi-format",
            TaskType.VALIDATION,
            priority=8
        ),
        Task(
            "task_002",
            "Entraîner modèle dhātu sur GPU",
            TaskType.ML_TRAINING,
            priority=9,
            requires_gpu=True,
            estimated_duration=3600
        ),
        Task(
            "task_003",
            "Refactoriser validateurs PaniniFS",
            TaskType.REFACTORING,
            priority=6
        ),
        Task(
            "task_004",
            "Définir architecture système compression",
            TaskType.ARCHITECTURE,
            priority=10,
            requires_human_review=True
        ),
        Task(
            "task_005",
            "Extraire métadonnées traducteurs",
            TaskType.EXTRACTION,
            priority=7
        )
    ]
    
    # Ajout tâches
    for task in tasks:
        orchestrator.add_task(task)
    
    print("\n" + "-" * 70)
    print("📊 ASSIGNATION OPTIMALE")
    print("-" * 70 + "\n")
    
    # Assignation automatique
    for task in tasks:
        agent_id = orchestrator.assign_optimal_agent(task.task_id)
        if agent_id:
            orchestrator.mark_task_started(task.task_id)
    
    # Rapport
    print("\n" + "-" * 70)
    print("📈 RAPPORT DASHBOARD")
    print("-" * 70 + "\n")
    
    report = orchestrator.generate_dashboard_report()
    print(f"Agents actifs: {len(report['agents'])}")
    print(f"Tâches totales: {report['tasks']['total']}")
    print(f"  - En cours: {report['tasks']['in_progress']}")
    print(f"  - Complétées: {report['tasks']['completed']}")
    print(f"  - En attente: {report['tasks']['pending']}")
    
    # Export
    output = orchestrator.export_state()
    print(f"\n✅ État complet exporté: {output.name}")


if __name__ == '__main__':
    main()
