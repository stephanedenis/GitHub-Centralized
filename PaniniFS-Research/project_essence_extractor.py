#!/usr/bin/env python3
"""
Project Essence Extractor - Capture Vision Avant Archivage

Extrait l'essence, motivations et valeur potentielle de chaque projet
avant décision d'archivage. Crée backlog structuré pour futures réactivations.

Principe: "Rien ne se perd, tout se transforme"
Pattern: *_extractor.py (auto-approved via whitelist)

Auteur: Autonomous System
Timestamp: 2025-10-01T16:00:00Z
"""

import os
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Any, Set, Tuple


class ProjectEssenceExtractor:
    """Extracteur essence projets avant archivage."""
    
    def __init__(self, workspace_root: str):
        """Initialise l'extracteur."""
        self.workspace_root = Path(workspace_root)
        
        # Projets candidats archivage (depuis mission_alignment_analyzer)
        self.candidates = [10, 8, 7, 6, 3]
        
        # Définitions projets
        self.github_projects = self._load_github_projects()
        
        # Scan docs pour mentions
        self.project_mentions = self._scan_all_mentions()
        
        # Résultats extraction
        self.essence_report = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'projects_analyzed': [],
            'backlog_items': [],
            'preservation_recommendations': []
        }
    
    def _load_github_projects(self) -> Dict[int, Dict[str, Any]]:
        """Charge définitions projets."""
        return {
            10: {
                "name": "[INTERFACES] dhatu-api-gateway",
                "category": "INTERFACES",
                "status": "PLANIFIÉ",
                "priority": "MOYENNE"
            },
            8: {
                "name": "[TOOLS] dhatu-evolution-simulator",
                "category": "TOOLS",
                "status": "PLANIFIÉ",
                "priority": "BASSE"
            },
            7: {
                "name": "[TOOLS] dhatu-space-visualizer",
                "category": "TOOLS",
                "status": "PLANIFIÉ",
                "priority": "BASSE"
            },
            6: {
                "name": "[TOOLS] dhatu-creative-generator",
                "category": "TOOLS",
                "status": "PLANIFIÉ",
                "priority": "BASSE"
            },
            3: {
                "name": "[CORE] dhatu-web-framework",
                "category": "CORE",
                "status": "PLANIFIÉ",
                "priority": "MOYENNE"
            }
        }
    
    def _scan_all_mentions(self) -> Dict[int, List[Dict[str, Any]]]:
        """Scan tous documents pour mentions projets."""
        mentions = {proj_id: [] for proj_id in self.candidates}
        
        # Documents à scanner
        doc_patterns = [
            '*.md',
            '*.json',
            '*.py'
        ]
        
        for pattern in doc_patterns:
            for doc_path in self.workspace_root.glob(pattern):
                if doc_path.is_file() and doc_path.stat().st_size < 1_000_000:
                    try:
                        with open(doc_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        # Chercher mentions projets
                        for proj_id in self.candidates:
                            proj_name = self.github_projects[proj_id]['name']
                            
                            # Patterns recherche
                            patterns = [
                                rf'(?i)project\s*#?{proj_id}\b',
                                rf'(?i){re.escape(proj_name)}',
                                rf'(?i)dhatu[-_]' + proj_name.split('-', 2)[-1] if 'dhatu' in proj_name else ''
                            ]
                            
                            for pattern in patterns:
                                if pattern and re.search(pattern, content):
                                    # Extraire contexte (3 lignes avant/après)
                                    lines = content.split('\n')
                                    for i, line in enumerate(lines):
                                        if re.search(pattern, line):
                                            context_start = max(0, i-3)
                                            context_end = min(len(lines), i+4)
                                            context = '\n'.join(lines[context_start:context_end])
                                            
                                            mentions[proj_id].append({
                                                'file': str(doc_path.name),
                                                'line_number': i+1,
                                                'context': context[:300],
                                                'match_type': 'project_id' if f'#{proj_id}' in pattern else 'name'
                                            })
                                            break  # Une mention par fichier suffit
                    except Exception as e:
                        continue
        
        return mentions
    
    def extract_essence(self, project_id: int) -> Dict[str, Any]:
        """Extrait essence d'un projet."""
        proj_info = self.github_projects[project_id]
        proj_name = proj_info['name']
        
        print(f"\n{'='*70}")
        print(f"🔍 PROJECT #{project_id}: {proj_name}")
        print(f"{'='*70}")
        
        essence = {
            'project_id': project_id,
            'name': proj_name,
            'category': proj_info['category'],
            'original_status': proj_info['status'],
            'original_priority': proj_info['priority']
        }
        
        # 1. Inférence motivation depuis nom
        motivation = self._infer_motivation_from_name(proj_name)
        essence['inferred_motivation'] = motivation
        
        # 2. Mentions dans docs
        mentions = self.project_mentions.get(project_id, [])
        essence['mentions_count'] = len(mentions)
        essence['mentioned_in_files'] = list(set(m['file'] for m in mentions))
        
        if mentions:
            essence['sample_contexts'] = [m['context'] for m in mentions[:3]]
        
        # 3. Valeur potentielle
        potential_value = self._assess_potential_value(project_id, proj_info, mentions)
        essence['potential_value'] = potential_value
        
        # 4. Bonnes idées à préserver
        good_ideas = self._extract_good_ideas(proj_name, mentions)
        essence['good_ideas'] = good_ideas
        
        # 5. Dépendances potentielles
        dependencies = self._identify_dependencies(project_id, proj_info)
        essence['dependencies'] = dependencies
        
        # 6. Recommandation archivage
        recommendation = self._generate_archival_recommendation(
            project_id, proj_info, potential_value, mentions
        )
        essence['archival_recommendation'] = recommendation
        
        # 7. Backlog items
        backlog = self._create_backlog_items(project_id, proj_info, good_ideas)
        essence['backlog_items'] = backlog
        
        # Affichage résumé
        self._print_essence_summary(essence)
        
        return essence
    
    def _infer_motivation_from_name(self, proj_name: str) -> str:
        """Infère motivation depuis nom projet."""
        name_lower = proj_name.lower()
        
        motivations = {
            'api-gateway': "Centraliser accès APIs dhātu - Point d'entrée unifié écosystème",
            'evolution-simulator': "Simuler évolution temporelle dhātu - Visualiser transformations linguistiques",
            'space-visualizer': "Visualiser espace sémantique dhātu - Représentation géométrique multidimensionnelle",
            'creative-generator': "Générer variations créatives dhātu - Exploration espace linguistique",
            'web-framework': "Framework web complet dhātu - Infrastructure applications linguistiques"
        }
        
        for keyword, motivation in motivations.items():
            if keyword in name_lower:
                return motivation
        
        return "Motivation non documentée - Inférence impossible"
    
    def _assess_potential_value(
        self,
        project_id: int,
        proj_info: Dict[str, Any],
        mentions: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Évalue valeur potentielle projet."""
        value = {
            'strategic_alignment': 0.0,  # 0-10
            'innovation_potential': 0.0,  # 0-10
            'ecosystem_impact': 0.0,      # 0-10
            'effort_to_activate': 0.0,    # 0-10 (moins = mieux)
            'total_score': 0.0            # 0-40
        }
        
        # Strategic alignment (basé catégorie)
        category_scores = {
            'CORE': 9,
            'RESEARCH': 8,
            'INTERFACES': 7,
            'TOOLS': 5,
            'ROADMAP': 6
        }
        value['strategic_alignment'] = category_scores.get(proj_info['category'], 5)
        
        # Innovation potential (basé nom)
        name = proj_info['name'].lower()
        if 'simulator' in name or 'generator' in name:
            value['innovation_potential'] = 8  # Haute innovation
        elif 'visualizer' in name or 'gateway' in name:
            value['innovation_potential'] = 6  # Innovation moyenne
        elif 'framework' in name:
            value['innovation_potential'] = 7  # Innovation structurelle
        else:
            value['innovation_potential'] = 5
        
        # Ecosystem impact (basé mentions)
        if len(mentions) >= 5:
            value['ecosystem_impact'] = 8
        elif len(mentions) >= 2:
            value['ecosystem_impact'] = 6
        elif len(mentions) >= 1:
            value['ecosystem_impact'] = 4
        else:
            value['ecosystem_impact'] = 2
        
        # Effort to activate (inversé: moins = mieux)
        if proj_info['status'] == 'ACTIF':
            value['effort_to_activate'] = 3  # Déjà actif
        elif proj_info['category'] in ['CORE', 'RESEARCH']:
            value['effort_to_activate'] = 7  # Complexe
        else:
            value['effort_to_activate'] = 5  # Moyen
        
        # Total
        value['total_score'] = (
            value['strategic_alignment'] +
            value['innovation_potential'] +
            value['ecosystem_impact'] +
            (10 - value['effort_to_activate'])  # Inverser effort
        )
        
        return value
    
    def _extract_good_ideas(
        self,
        proj_name: str,
        mentions: List[Dict[str, Any]]
    ) -> List[str]:
        """Extrait bonnes idées du projet."""
        ideas = []
        
        # Idées depuis nom
        name_ideas = {
            'api-gateway': [
                "Point d'entrée unifié pour tous services dhātu",
                "Authentification centralisée",
                "Rate limiting et monitoring global",
                "API versioning et backward compatibility"
            ],
            'evolution-simulator': [
                "Visualiser transformations dhātu temporelles",
                "Simuler dérivations linguistiques (dhātu → mots)",
                "Prédire évolutions futures patterns",
                "Benchmarks vitesse/précision transformations"
            ],
            'space-visualizer': [
                "Représentation 3D espace sémantique dhātu",
                "Clustering visuel patterns similaires",
                "Navigation interactive géométrie linguistique",
                "Export visualisations haute résolution"
            ],
            'creative-generator': [
                "Générer variations linguistiques créatives",
                "Exploration guidée espace compositional",
                "Suggestions intelligence artificielle",
                "Mode découverte serendipité"
            ],
            'web-framework': [
                "Components réutilisables applications dhātu",
                "State management linguistique",
                "Real-time synchronization corpus",
                "Responsive design multi-devices"
            ]
        }
        
        for keyword, keyword_ideas in name_ideas.items():
            if keyword in proj_name.lower():
                ideas.extend(keyword_ideas)
        
        # Idées depuis contextes mentions
        for mention in mentions[:5]:
            context = mention.get('context', '').lower()
            
            # Extraction keywords actions
            action_keywords = [
                'visualiser', 'simuler', 'générer', 'centraliser',
                'transformer', 'explorer', 'découvrir', 'analyser'
            ]
            
            for keyword in action_keywords:
                if keyword in context:
                    # Extraire phrase contenant keyword
                    sentences = re.split(r'[.!?\n]', context)
                    for sentence in sentences:
                        if keyword in sentence.lower() and len(sentence) > 20:
                            ideas.append(sentence.strip())
                            break
        
        return list(set(ideas))  # Déduplicate
    
    def _identify_dependencies(
        self,
        project_id: int,
        proj_info: Dict[str, Any]
    ) -> Dict[str, List[int]]:
        """Identifie dépendances projet."""
        dependencies = {
            'depends_on': [],     # Ce projet dépend de...
            'required_by': []     # Ce projet est requis par...
        }
        
        # Règles dépendances logiques
        category = proj_info['category']
        
        # INTERFACES dépendent CORE
        if category == 'INTERFACES':
            dependencies['depends_on'] = [1, 2, 4]  # Compressor, Corpus, GPU
        
        # TOOLS dépendent CORE
        elif category == 'TOOLS':
            dependencies['depends_on'] = [2, 4]  # Corpus, GPU
        
        # Web framework dépend de tout CORE
        if project_id == 3:
            dependencies['depends_on'] = [1, 2, 4]
        
        # API Gateway pourrait être requis par Dashboard
        if project_id == 10:
            dependencies['required_by'] = [9]  # Dashboard
        
        return dependencies
    
    def _generate_archival_recommendation(
        self,
        project_id: int,
        proj_info: Dict[str, Any],
        potential_value: Dict[str, Any],
        mentions: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Génère recommandation archivage."""
        recommendation = {
            'decision': 'UNKNOWN',
            'confidence': 0.0,
            'rationale': [],
            'conditions_reactivation': []
        }
        
        score = potential_value['total_score']
        
        # Critères décision
        if score >= 30:
            recommendation['decision'] = 'PRESERVE'
            recommendation['confidence'] = 0.9
            recommendation['rationale'].append(
                f"Score valeur potentielle élevé ({score:.1f}/40)"
            )
        elif score >= 20:
            recommendation['decision'] = 'ARCHIVE_WITH_BACKLOG'
            recommendation['confidence'] = 0.8
            recommendation['rationale'].append(
                f"Score valeur potentielle moyen ({score:.1f}/40) - Bonnes idées à préserver"
            )
        else:
            recommendation['decision'] = 'ARCHIVE'
            recommendation['confidence'] = 0.7
            recommendation['rationale'].append(
                f"Score valeur potentielle faible ({score:.1f}/40)"
            )
        
        # Rationale additionnel
        if len(mentions) == 0:
            recommendation['rationale'].append(
                "Aucune mention dans documentation actuelle"
            )
        
        if proj_info['status'] == 'PLANIFIÉ' and proj_info['priority'] == 'BASSE':
            recommendation['rationale'].append(
                "Status PLANIFIÉ + Priority BASSE suggère non-prioritaire"
            )
        
        # Conditions réactivation
        if recommendation['decision'] in ['ARCHIVE', 'ARCHIVE_WITH_BACKLOG']:
            recommendation['conditions_reactivation'] = [
                f"Complétion projets CORE (1, 2, 4) à ≥80%",
                f"Demande explicite use case spécifique",
                f"Capacité équipe: ≥2 devs disponibles",
                f"Budget: ≥40h estimation effort"
            ]
            
            # Conditions spécifiques
            if proj_info['category'] == 'INTERFACES':
                recommendation['conditions_reactivation'].append(
                    "CORE APIs stables et documentées"
                )
            elif proj_info['category'] == 'TOOLS':
                recommendation['conditions_reactivation'].append(
                    "Corpus ≥100k validé et corpus manager opérationnel"
                )
        
        return recommendation
    
    def _create_backlog_items(
        self,
        project_id: int,
        proj_info: Dict[str, Any],
        good_ideas: List[str]
    ) -> List[Dict[str, Any]]:
        """Crée items backlog depuis bonnes idées."""
        backlog = []
        
        for i, idea in enumerate(good_ideas[:5], 1):  # Top 5
            item = {
                'id': f'backlog_{project_id}_{i:02d}',
                'title': idea[:100],
                'source_project': project_id,
                'source_project_name': proj_info['name'],
                'category': proj_info['category'],
                'priority': 'FUTURE',
                'estimated_effort': 'TBD',
                'prerequisites': self._infer_prerequisites(idea),
                'tags': self._extract_tags(idea)
            }
            backlog.append(item)
        
        return backlog
    
    def _infer_prerequisites(self, idea: str) -> List[str]:
        """Infère prérequis depuis idée."""
        prerequisites = []
        
        idea_lower = idea.lower()
        
        if 'api' in idea_lower or 'service' in idea_lower:
            prerequisites.append("CORE APIs stabilisées")
        
        if 'corpus' in idea_lower or 'données' in idea_lower:
            prerequisites.append("Corpus ≥100k validé")
        
        if 'gpu' in idea_lower or 'training' in idea_lower:
            prerequisites.append("Infrastructure GPU opérationnelle")
        
        if 'visualis' in idea_lower or '3d' in idea_lower:
            prerequisites.append("Framework visualisation choisi")
        
        if 'real-time' in idea_lower or 'synchron' in idea_lower:
            prerequisites.append("WebSocket infrastructure")
        
        return prerequisites if prerequisites else ["Aucun prérequis identifié"]
    
    def _extract_tags(self, idea: str) -> List[str]:
        """Extrait tags depuis idée."""
        tags = []
        
        idea_lower = idea.lower()
        
        tag_keywords = {
            'visualization': ['visualis', '3d', 'graph', 'chart'],
            'api': ['api', 'endpoint', 'service', 'gateway'],
            'simulation': ['simuler', 'simulation', 'prédire'],
            'generation': ['générer', 'créer', 'produire'],
            'analytics': ['analyser', 'métriques', 'benchmark'],
            'ui': ['interface', 'dashboard', 'responsive'],
            'ml': ['intelligence', 'learning', 'model'],
            'performance': ['optimis', 'performance', 'rapide']
        }
        
        for tag, keywords in tag_keywords.items():
            if any(kw in idea_lower for kw in keywords):
                tags.append(tag)
        
        return tags if tags else ['general']
    
    def _print_essence_summary(self, essence: Dict[str, Any]):
        """Affiche résumé essence."""
        print(f"\n📊 Motivation Inférée:")
        print(f"  {essence['inferred_motivation']}")
        
        print(f"\n📈 Valeur Potentielle:")
        pv = essence['potential_value']
        print(f"  Strategic Alignment: {pv['strategic_alignment']:.1f}/10")
        print(f"  Innovation Potential: {pv['innovation_potential']:.1f}/10")
        print(f"  Ecosystem Impact: {pv['ecosystem_impact']:.1f}/10")
        print(f"  Effort to Activate: {pv['effort_to_activate']:.1f}/10")
        print(f"  SCORE TOTAL: {pv['total_score']:.1f}/40")
        
        print(f"\n💡 Bonnes Idées Extraites: {len(essence['good_ideas'])}")
        for i, idea in enumerate(essence['good_ideas'][:3], 1):
            print(f"  {i}. {idea[:80]}...")
        
        print(f"\n🔗 Mentions Documentation: {essence['mentions_count']}")
        if essence['mentioned_in_files']:
            print(f"  Fichiers: {', '.join(essence['mentioned_in_files'][:3])}")
        
        print(f"\n✅ Recommandation Archivage:")
        rec = essence['archival_recommendation']
        print(f"  Décision: {rec['decision']}")
        print(f"  Confiance: {rec['confidence']*100:.0f}%")
        print(f"  Rationale:")
        for rationale in rec['rationale']:
            print(f"    - {rationale}")
        
        if rec['conditions_reactivation']:
            print(f"\n🔄 Conditions Réactivation:")
            for condition in rec['conditions_reactivation'][:3]:
                print(f"    - {condition}")
        
        print(f"\n📋 Backlog Items Créés: {len(essence['backlog_items'])}")
    
    def analyze_all_candidates(self) -> Dict[str, Any]:
        """Analyse tous candidats archivage."""
        print("\n" + "="*70)
        print("🔬 EXTRACTION ESSENCE PROJETS - AVANT ARCHIVAGE")
        print("="*70)
        print(f"\n5 projets candidats à analyser: {self.candidates}")
        
        for project_id in self.candidates:
            essence = self.extract_essence(project_id)
            self.essence_report['projects_analyzed'].append(essence)
            
            # Accumuler backlog items
            self.essence_report['backlog_items'].extend(essence['backlog_items'])
            
            # Recommandations préservation
            if essence['archival_recommendation']['decision'] == 'PRESERVE':
                self.essence_report['preservation_recommendations'].append({
                    'project_id': project_id,
                    'name': essence['name'],
                    'reason': essence['archival_recommendation']['rationale']
                })
        
        # Statistiques finales
        self._generate_final_statistics()
        
        return self.essence_report
    
    def _generate_final_statistics(self):
        """Génère statistiques finales."""
        print("\n" + "="*70)
        print("📊 STATISTIQUES FINALES EXTRACTION")
        print("="*70)
        
        total = len(self.essence_report['projects_analyzed'])
        
        # Distribution décisions
        decisions = {}
        total_score = 0
        for proj in self.essence_report['projects_analyzed']:
            decision = proj['archival_recommendation']['decision']
            decisions[decision] = decisions.get(decision, 0) + 1
            total_score += proj['potential_value']['total_score']
        
        print(f"\n📈 Distribution Décisions:")
        for decision, count in decisions.items():
            print(f"  {decision}: {count} projets")
        
        print(f"\n💡 Bonnes Idées Totales: {len(self.essence_report['backlog_items'])}")
        
        print(f"\n📋 Backlog Items par Catégorie:")
        backlog_by_category = {}
        for item in self.essence_report['backlog_items']:
            category = item['category']
            backlog_by_category[category] = backlog_by_category.get(category, 0) + 1
        
        for category, count in sorted(backlog_by_category.items()):
            print(f"  {category}: {count} items")
        
        avg_score = total_score / total if total > 0 else 0
        print(f"\n⭐ Score Potentiel Moyen: {avg_score:.1f}/40")
        
        if self.essence_report['preservation_recommendations']:
            print(f"\n⚠️  Projets À PRÉSERVER (haute valeur):")
            for rec in self.essence_report['preservation_recommendations']:
                print(f"  - Project #{rec['project_id']}: {rec['name']}")
    
    def export_report(self, output_file: Optional[Path] = None) -> Path:
        """Export rapport essence."""
        if output_file is None:
            timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H-%M-%SZ')
            output_file = (
                self.workspace_root /
                f'project_essence_extraction_{timestamp}.json'
            )
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.essence_report, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Rapport essence exporté: {output_file.name}")
        return output_file
    
    def export_backlog_markdown(self, output_file: Optional[Path] = None) -> Path:
        """Export backlog en Markdown lisible."""
        if output_file is None:
            timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H-%M-%SZ')
            output_file = (
                self.workspace_root /
                f'BACKLOG_ARCHIVED_PROJECTS_{timestamp}.md'
            )
        
        lines = [
            "# 📋 Backlog Idées - Projets Archivés",
            "",
            f"**Date**: {datetime.now(timezone.utc).strftime('%Y-%m-%d')}",
            f"**Source**: Extraction essence 5 projets archivés",
            f"**Total Items**: {len(self.essence_report['backlog_items'])}",
            "",
            "---",
            "",
            "## 🎯 Principe",
            "",
            "Ce document préserve les **bonnes idées** des projets archivés.",
            "Rien n'est perdu - ces idées peuvent être réactivées quand:",
            "- Les prérequis sont remplis",
            "- Un use case concret émerge",
            "- Les ressources sont disponibles",
            "",
            "---",
            ""
        ]
        
        # Grouper par catégorie
        by_category = {}
        for item in self.essence_report['backlog_items']:
            category = item['category']
            if category not in by_category:
                by_category[category] = []
            by_category[category].append(item)
        
        for category in sorted(by_category.keys()):
            items = by_category[category]
            lines.append(f"## 📦 {category} ({len(items)} items)")
            lines.append("")
            
            for item in items:
                lines.append(f"### {item['title']}")
                lines.append("")
                lines.append(f"**Source**: Project #{item['source_project']} - {item['source_project_name']}")
                lines.append(f"**Priority**: {item['priority']}")
                lines.append(f"**Effort**: {item['estimated_effort']}")
                lines.append("")
                
                if item['prerequisites']:
                    lines.append("**Prérequis**:")
                    for prereq in item['prerequisites']:
                        lines.append(f"- {prereq}")
                    lines.append("")
                
                if item['tags']:
                    lines.append(f"**Tags**: {', '.join(item['tags'])}")
                    lines.append("")
                
                lines.append("---")
                lines.append("")
        
        # Conditions réactivation globales
        lines.extend([
            "## 🔄 Conditions Réactivation Générales",
            "",
            "Pour réactiver un item backlog, vérifier:",
            "",
            "1. ✅ **Prérequis techniques** remplis (CORE projects opérationnels)",
            "2. ✅ **Use case concret** identifié (pas théorique)",
            "3. ✅ **Ressources disponibles** (≥40h + budget si externe)",
            "4. ✅ **Alignement stratégique** avec roadmap actuelle",
            "5. ✅ **Capacité équipe** (≥2 personnes ou agent autonome)",
            "",
            "---",
            "",
            f"*Rapport généré automatiquement par project_essence_extractor.py*"
        ])
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        
        print(f"✅ Backlog Markdown exporté: {output_file.name}")
        return output_file


def main():
    """Point d'entrée principal."""
    workspace = "/home/stephane/GitHub/PaniniFS-Research"
    
    extractor = ProjectEssenceExtractor(workspace)
    
    # Extraction complète
    report = extractor.analyze_all_candidates()
    
    # Export JSON détaillé
    json_output = extractor.export_report()
    
    # Export Markdown backlog
    md_output = extractor.export_backlog_markdown()
    
    # Résumé final
    print("\n" + "="*70)
    print("✅ EXTRACTION ESSENCE COMPLÉTÉE")
    print("="*70)
    print(f"Projets analysés: {len(report['projects_analyzed'])}")
    print(f"Backlog items: {len(report['backlog_items'])}")
    print(f"Projets à préserver: {len(report['preservation_recommendations'])}")
    print(f"\n📁 Rapports générés:")
    print(f"  - {json_output.name} (détails)")
    print(f"  - {md_output.name} (backlog)")
    
    if report['preservation_recommendations']:
        print(f"\n⚠️  ATTENTION: {len(report['preservation_recommendations'])} projets recommandés PRÉSERVATION")
        print("  Review manuelle recommandée avant archivage")


if __name__ == '__main__':
    main()
