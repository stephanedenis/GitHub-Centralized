#!/usr/bin/env python3
"""
Backlog Reviewer - Évaluation Interactive Items Archivés

Review méthodique des 20 bonnes idées préservées:
- Scoring interactif par critères
- Priorisation intelligente
- Génération plan réactivation
- Export décisions pour traçabilité

Usage: python3 backlog_reviewer.py

Pattern: *_reviewer.py (auto-approved via whitelist)

Auteur: Autonomous System
Timestamp: 2025-10-01T16:00:00Z
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Any


class BacklogReviewer:
    """Review interactif backlog items."""
    
    def __init__(self, workspace_root: str):
        """Initialise le reviewer."""
        self.workspace_root = Path(workspace_root)
        
        # Charger extraction essence
        essence_files = list(
            self.workspace_root.glob('project_essence_extraction_*.json')
        )
        if not essence_files:
            raise FileNotFoundError(
                "Aucun fichier project_essence_extraction_*.json trouvé"
            )
        
        latest_essence = max(essence_files, key=lambda p: p.stat().st_mtime)
        with open(latest_essence, 'r', encoding='utf-8') as f:
            self.essence_data = json.load(f)
        
        self.backlog_items = self.essence_data.get('backlog_items', [])
        
        # Résultats review
        self.review_results = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'total_items': len(self.backlog_items),
            'items_reviewed': [],
            'prioritization': {
                'high': [],
                'medium': [],
                'low': [],
                'deferred': []
            },
            'reactivation_candidates': [],
            'statistics': {}
        }
    
    def analyze_prerequisites_status(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """Analyse statut prérequis item."""
        prereqs = item.get('prerequisites', [])
        
        # Statut CORE projects (base pour beaucoup de prereqs)
        core_status = {
            'project_1_compressor': 'IN_PROGRESS',  # 4 nouvelles tâches
            'project_2_corpus': 'IN_PROGRESS',      # Tâches actives
            'project_4_gpu': 'IN_PROGRESS',         # Tâches GPU actives
            'apis_stable': 'NOT_STARTED',
            'corpus_100k': 'IN_PROGRESS',           # Validation en cours
            'gpu_infra': 'OPERATIONAL',             # Colab Pro ready
            'websocket': 'NOT_STARTED',
            'visualization_framework': 'NOT_STARTED'
        }
        
        status = {
            'all_met': False,
            'count_met': 0,
            'count_total': len(prereqs),
            'details': []
        }
        
        if status['count_total'] == 0:
            status['all_met'] = True
            return status
        
        for prereq in prereqs:
            prereq_lower = prereq.lower()
            met = False
            reason = ''
            
            if 'core apis' in prereq_lower:
                met = core_status['apis_stable'] == 'OPERATIONAL'
                reason = 'CORE APIs pas encore stables'
            elif 'corpus' in prereq_lower and '100k' in prereq_lower:
                met = core_status['corpus_100k'] == 'COMPLETED'
                reason = 'Corpus 100k validation en cours'
            elif 'gpu' in prereq_lower or 'infrastructure gpu' in prereq_lower:
                met = core_status['gpu_infra'] == 'OPERATIONAL'
                reason = 'Infrastructure GPU opérationnelle (Colab Pro)'
            elif 'websocket' in prereq_lower:
                met = core_status['websocket'] == 'OPERATIONAL'
                reason = 'WebSocket infrastructure pas démarrée'
            elif 'visualis' in prereq_lower or 'framework' in prereq_lower:
                met = core_status['visualization_framework'] == 'OPERATIONAL'
                reason = 'Framework visualisation pas choisi'
            elif 'aucun' in prereq_lower:
                met = True
                reason = 'Aucun prérequis'
            
            status['details'].append({
                'prerequisite': prereq,
                'met': met,
                'reason': reason
            })
            
            if met:
                status['count_met'] += 1
        
        status['all_met'] = status['count_met'] == status['count_total']
        
        return status
    
    def score_item_value(self, item: Dict[str, Any]) -> Dict[str, float]:
        """Score valeur item (0-100)."""
        scores = {
            'innovation': 0.0,
            'strategic_fit': 0.0,
            'effort_low': 0.0,
            'prerequisites_met': 0.0,
            'total': 0.0
        }
        
        # Innovation (basé tags et title)
        title = item.get('title', '').lower()
        tags = item.get('tags', [])
        
        if 'simulation' in tags or 'ml' in tags:
            scores['innovation'] = 25.0  # Très innovant
        elif 'visualization' in tags or 'generation' in tags:
            scores['innovation'] = 20.0  # Innovant
        elif 'api' in tags or 'analytics' in tags:
            scores['innovation'] = 15.0  # Utile
        else:
            scores['innovation'] = 10.0  # Standard
        
        # Strategic fit (basé catégorie)
        category = item.get('category', '')
        if category == 'CORE':
            scores['strategic_fit'] = 25.0  # Très stratégique
        elif category == 'RESEARCH':
            scores['strategic_fit'] = 20.0  # Stratégique
        elif category == 'INTERFACES':
            scores['strategic_fit'] = 15.0  # Important
        else:
            scores['strategic_fit'] = 10.0  # Nice to have
        
        # Effort (inversé: moins d'effort = plus de score)
        # Basé sur estimated_effort (TBD = assume moyen)
        scores['effort_low'] = 15.0  # TBD = assume effort moyen
        
        # Prerequisites met
        prereq_status = self.analyze_prerequisites_status(item)
        if prereq_status['all_met']:
            scores['prerequisites_met'] = 35.0
        elif prereq_status['count_met'] > 0:
            ratio = prereq_status['count_met'] / prereq_status['count_total']
            scores['prerequisites_met'] = 35.0 * ratio
        else:
            scores['prerequisites_met'] = 0.0
        
        scores['total'] = sum([
            scores['innovation'],
            scores['strategic_fit'],
            scores['effort_low'],
            scores['prerequisites_met']
        ])
        
        return scores
    
    def generate_item_report(self, item: Dict[str, Any], index: int) -> str:
        """Génère rapport détaillé item."""
        lines = []
        
        lines.append(f"\n{'='*70}")
        lines.append(f"📋 ITEM #{index+1}/20")
        lines.append(f"{'='*70}")
        
        lines.append(f"\n**Titre**: {item['title']}")
        lines.append(f"**Source**: Project #{item['source_project']} - {item['source_project_name']}")
        lines.append(f"**Catégorie**: {item['category']}")
        lines.append(f"**Tags**: {', '.join(item['tags'])}")
        
        # Prérequis
        lines.append(f"\n**Prérequis**:")
        prereq_status = self.analyze_prerequisites_status(item)
        lines.append(f"  Status: {prereq_status['count_met']}/{prereq_status['count_total']} remplis")
        
        for detail in prereq_status['details']:
            status_icon = '✅' if detail['met'] else '❌'
            lines.append(f"  {status_icon} {detail['prerequisite']}")
            if not detail['met'] and detail['reason']:
                lines.append(f"     → {detail['reason']}")
        
        # Scoring
        scores = self.score_item_value(item)
        lines.append(f"\n**Scoring Valeur** (sur 100):")
        lines.append(f"  Innovation: {scores['innovation']:.0f}/25")
        lines.append(f"  Strategic Fit: {scores['strategic_fit']:.0f}/25")
        lines.append(f"  Effort faible: {scores['effort_low']:.0f}/15")
        lines.append(f"  Prérequis remplis: {scores['prerequisites_met']:.0f}/35")
        lines.append(f"  TOTAL: {scores['total']:.0f}/100")
        
        # Recommandation
        lines.append(f"\n**Recommandation**:")
        if scores['total'] >= 75:
            lines.append(f"  🟢 HIGH PRIORITY - Réactivation recommandée immédiatement")
        elif scores['total'] >= 50:
            lines.append(f"  🟡 MEDIUM PRIORITY - Réactivation après CORE complété")
        elif scores['total'] >= 25:
            lines.append(f"  🟠 LOW PRIORITY - Réactivation Q1 2026 si ressources")
        else:
            lines.append(f"  ⚪ DEFERRED - Reporter à review ultérieure")
        
        return '\n'.join(lines)
    
    def review_all_items(self) -> Dict[str, Any]:
        """Review automatique tous items."""
        print("\n🔍 REVIEW BACKLOG AUTOMATIQUE - 20 ITEMS")
        print("="*70)
        
        for i, item in enumerate(self.backlog_items):
            # Rapport item
            report = self.generate_item_report(item, i)
            print(report)
            
            # Scoring
            scores = self.score_item_value(item)
            prereq_status = self.analyze_prerequisites_status(item)
            
            # Classification
            priority = None
            if scores['total'] >= 75:
                priority = 'high'
                self.review_results['reactivation_candidates'].append(item['id'])
            elif scores['total'] >= 50:
                priority = 'medium'
            elif scores['total'] >= 25:
                priority = 'low'
            else:
                priority = 'deferred'
            
            self.review_results['prioritization'][priority].append(item['id'])
            
            # Enregistrer review
            self.review_results['items_reviewed'].append({
                'item_id': item['id'],
                'title': item['title'],
                'source_project': item['source_project'],
                'category': item['category'],
                'scores': scores,
                'prerequisites_status': prereq_status,
                'priority': priority
            })
        
        # Statistiques
        self._generate_statistics()
        
        return self.review_results
    
    def _generate_statistics(self):
        """Génère statistiques review."""
        stats = {
            'by_priority': {
                'high': len(self.review_results['prioritization']['high']),
                'medium': len(self.review_results['prioritization']['medium']),
                'low': len(self.review_results['prioritization']['low']),
                'deferred': len(self.review_results['prioritization']['deferred'])
            },
            'by_category': {},
            'prerequisites_analysis': {
                'all_met': 0,
                'partial': 0,
                'none_met': 0
            },
            'reactivation_ready': len(self.review_results['reactivation_candidates'])
        }
        
        # Par catégorie
        for item_review in self.review_results['items_reviewed']:
            category = item_review['category']
            stats['by_category'][category] = stats['by_category'].get(category, 0) + 1
            
            # Prérequis
            prereq_status = item_review['prerequisites_status']
            if prereq_status['all_met']:
                stats['prerequisites_analysis']['all_met'] += 1
            elif prereq_status['count_met'] > 0:
                stats['prerequisites_analysis']['partial'] += 1
            else:
                stats['prerequisites_analysis']['none_met'] += 1
        
        self.review_results['statistics'] = stats
        
        print("\n" + "="*70)
        print("📊 STATISTIQUES REVIEW")
        print("="*70)
        
        print(f"\n**Priorisation**:")
        print(f"  🟢 HIGH: {stats['by_priority']['high']} items")
        print(f"  🟡 MEDIUM: {stats['by_priority']['medium']} items")
        print(f"  🟠 LOW: {stats['by_priority']['low']} items")
        print(f"  ⚪ DEFERRED: {stats['by_priority']['deferred']} items")
        
        print(f"\n**Par Catégorie**:")
        for category, count in sorted(stats['by_category'].items()):
            print(f"  {category}: {count} items")
        
        print(f"\n**Prérequis**:")
        print(f"  ✅ Tous remplis: {stats['prerequisites_analysis']['all_met']} items")
        print(f"  ⚠️  Partiels: {stats['prerequisites_analysis']['partial']} items")
        print(f"  ❌ Aucun rempli: {stats['prerequisites_analysis']['none_met']} items")
        
        print(f"\n**Recommandation Réactivation**:")
        print(f"  🚀 {stats['reactivation_ready']} items prêts réactivation immédiate")
    
    def generate_reactivation_plan(self) -> str:
        """Génère plan réactivation pour items HIGH priority."""
        lines = [
            "# 🚀 Plan Réactivation Backlog - Items HIGH Priority",
            "",
            f"**Date**: {datetime.now(timezone.utc).strftime('%Y-%m-%d')}",
            f"**Items analysés**: {self.review_results['total_items']}",
            f"**Items HIGH priority**: {len(self.review_results['prioritization']['high'])}",
            "",
            "---",
            "",
            "## 🎯 Critères Réactivation",
            "",
            "Items classés HIGH priority (score ≥75/100) basé sur:",
            "- ✅ Innovation (25 points max)",
            "- ✅ Strategic Fit (25 points max)",
            "- ✅ Effort faible (15 points max)",
            "- ✅ Prérequis remplis (35 points max)",
            "",
            "---",
            ""
        ]
        
        high_priority_ids = self.review_results['prioritization']['high']
        
        if not high_priority_ids:
            lines.extend([
                "## ⚠️ Aucun Item HIGH Priority",
                "",
                "Aucun item n'atteint le seuil 75/100 actuellement.",
                "**Recommandation**: Compléter projets CORE (1, 2, 4) d'abord.",
                "",
                "Une fois CORE ≥80% complété, re-review backlog pour items MEDIUM."
            ])
        else:
            lines.append(f"## 📋 Items HIGH Priority ({len(high_priority_ids)})")
            lines.append("")
            
            for item_id in high_priority_ids:
                # Trouver item review
                item_review = next(
                    (ir for ir in self.review_results['items_reviewed']
                     if ir['item_id'] == item_id),
                    None
                )
                
                if item_review:
                    lines.append(f"### {item_id}")
                    lines.append("")
                    lines.append(f"**Titre**: {item_review['title']}")
                    lines.append(f"**Source**: Project #{item_review['source_project']}")
                    lines.append(f"**Catégorie**: {item_review['category']}")
                    lines.append(f"**Score Total**: {item_review['scores']['total']:.0f}/100")
                    lines.append("")
                    
                    prereq = item_review['prerequisites_status']
                    lines.append("**Prérequis**:")
                    for detail in prereq['details']:
                        status = '✅' if detail['met'] else '❌'
                        lines.append(f"- {status} {detail['prerequisite']}")
                    lines.append("")
                    
                    lines.append("**Action**:")
                    lines.append(f"1. Créer GitHub Issue pour cet item")
                    lines.append(f"2. Assigner à agent optimal")
                    lines.append(f"3. Estimer effort détaillé")
                    lines.append(f"4. Ajouter au sprint actuel si capacité disponible")
                    lines.append("")
                    lines.append("---")
                    lines.append("")
        
        return '\n'.join(lines)
    
    def export_results(self) -> Path:
        """Export résultats review."""
        timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H-%M-%SZ')
        
        # JSON détaillé
        json_file = (
            self.workspace_root /
            f'backlog_review_results_{timestamp}.json'
        )
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(self.review_results, f, indent=2, ensure_ascii=False)
        
        # Markdown plan réactivation
        md_file = (
            self.workspace_root /
            f'BACKLOG_REACTIVATION_PLAN_{timestamp}.md'
        )
        plan = self.generate_reactivation_plan()
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(plan)
        
        print(f"\n✅ Résultats exportés:")
        print(f"  - {json_file.name}")
        print(f"  - {md_file.name}")
        
        return json_file


def main():
    """Point d'entrée principal."""
    workspace = "/home/stephane/GitHub/PaniniFS-Research"
    
    reviewer = BacklogReviewer(workspace)
    
    # Review automatique
    results = reviewer.review_all_items()
    
    # Export
    reviewer.export_results()
    
    # Résumé final
    print("\n" + "="*70)
    print("✅ REVIEW BACKLOG COMPLÉTÉ")
    print("="*70)
    print(f"Items HIGH priority: {len(results['prioritization']['high'])}")
    print(f"Items MEDIUM priority: {len(results['prioritization']['medium'])}")
    print(f"Items LOW priority: {len(results['prioritization']['low'])}")
    print(f"Items DEFERRED: {len(results['prioritization']['deferred'])}")
    print(f"\nRecommandation: Voir BACKLOG_REACTIVATION_PLAN_*.md")


if __name__ == '__main__':
    main()
