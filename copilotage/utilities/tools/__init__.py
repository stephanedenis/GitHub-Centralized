"""
PaniniFS Research Toolkit - Modules Réutilisables
================================================

Ce package contient tous les outils réutilisables pour éviter
les commandes ad-hoc et non réutilisables dans le chat.

Modules disponibles:
- system_tools: Opérations système (processes, ports, filesystem)
- database_tools: Opérations SQLite (queries, stats, reports)
- web_tools: HTTP calls, API, serveurs
- analytics_tools: Métriques, performance, bottlenecks
- reporting_tools: Génération rapports standardisés
"""

__version__ = "1.0.0"
__author__ = "PaniniFS Research Team"

# Import des outils principaux
from .system_tools import SystemTools
from .database_tools import DatabaseTools
from .web_tools import WebTools
from .analytics_tools import AnalyticsTools
from .reporting_tools import ReportingTools

# Instance globale réutilisable
system = SystemTools()
database = DatabaseTools()
web = WebTools()
analytics = AnalyticsTools()
reporting = ReportingTools()

__all__ = [
    'SystemTools', 'DatabaseTools', 'WebTools', 
    'AnalyticsTools', 'ReportingTools',
    'system', 'database', 'web', 'analytics', 'reporting'
]