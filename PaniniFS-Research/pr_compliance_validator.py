#!/usr/bin/env python3
"""
PR Compliance Validator for Mission Clarifications

Valide la conformité des Pull Requests GitHub (#15-18) avec les 8 clarifications
de la mission "Théorie Information Universelle".

Pattern: *_validator.py (auto-approved via whitelist)

CLARIFICATIONS À VÉRIFIER:
1. Dashboard Scope: Écosystème Panini complet (pas seulement tools)
2. Integrity Validation: Binaire 100% ou FAIL (pas de seuils flous)
3. Symmetries: Compose/Decompose fondamental (pas seulement identité)
4. Translators: QUI/QUAND > number (pas seulement counting)
5. Translators Patterns: Bias+Style=Patterns (pas isolation)
6. Standards ISO 8601: Timestamps obligatoires (pas formats libres)
7. Standards Modular: Sections indépendantes (pas monolithique)
8. Standards UHD: Animations utiles seulement (pas decoration)

Auteur: Autonomous Wrapper System
Timestamp: 2025-10-01T13:41:00Z
"""

import os
import sys
import json
import re
import subprocess
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
from pathlib import Path


class PRComplianceValidator:
    """Validator pour conformité PRs avec clarifications mission."""
    
    def __init__(self, workspace_root: str):
        """Initialise le validator."""
        self.workspace_root = Path(workspace_root)
        self.prs = [15, 16, 17, 18]
        self.clarifications = {
            'dashboard_scope': {
                'keywords': ['écosystème', 'panini', 'complet', 'tous', 'tools'],
                'anti_keywords': ['seulement', 'uniquement', 'tools only'],
                'weight': 0.15
            },
            'integrity_binary': {
                'keywords': ['100%', 'binaire', 'FAIL', 'SUCCESS', 'boolean'],
                'anti_keywords': ['seuil', 'threshold', '80%', '90%', 'partial'],
                'weight': 0.15
            },
            'symmetries_compose': {
                'keywords': ['compose', 'decompose', 'fondamental', 'fundamental'],
                'anti_keywords': ['identité', 'identity only', 'simple'],
                'weight': 0.15
            },
            'translators_qui_quand': {
                'keywords': ['QUI', 'QUAND', 'qui/quand', 'semantic', 'context'],
                'anti_keywords': ['number only', 'counting', 'numeric'],
                'weight': 0.15
            },
            'translators_patterns': {
                'keywords': ['bias', 'style', 'patterns', 'combination', 'combo'],
                'anti_keywords': ['isolation', 'separate', 'independent'],
                'weight': 0.10
            },
            'iso8601_mandatory': {
                'keywords': ['ISO 8601', 'YYYY-MM-DD', 'timestamp', 'datetime'],
                'anti_keywords': ['libre', 'flexible', 'format libre'],
                'weight': 0.10
            },
            'standards_modular': {
                'keywords': ['modular', 'modulaire', 'sections', 'independent'],
                'anti_keywords': ['monolithique', 'monolithic', 'single block'],
                'weight': 0.10
            },
            'standards_uhd_functional': {
                'keywords': ['UHD', '4K', 'animations utiles', 'functional'],
                'anti_keywords': ['decoration', 'decorative', 'bling'],
                'weight': 0.10
            }
        }
        
        self.results = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'prs_analyzed': [],
            'overall_compliance': 0.0,
            'status': 'PENDING'
        }
    
    def validate_all_prs(self) -> Dict[str, Any]:
        """Valide tous les PRs spécifiés."""
        print(f"\n🔍 PR Compliance Validator - Mission Clarifications")
        print(f"=" * 70)
        print(f"PRs à analyser: {', '.join(f'#{pr}' for pr in self.prs)}")
        print(f"Clarifications: {len(self.clarifications)}")
        print()
        
        for pr_number in self.prs:
            pr_result = self._validate_pr(pr_number)
            self.results['prs_analyzed'].append(pr_result)
        
        # Calcul compliance globale
        if self.results['prs_analyzed']:
            total_scores = [pr['compliance_score'] 
                           for pr in self.results['prs_analyzed']]
            self.results['overall_compliance'] = sum(total_scores) / len(total_scores)
        
        # Détermination status
        if self.results['overall_compliance'] >= 0.90:
            self.results['status'] = 'EXCELLENT'
        elif self.results['overall_compliance'] >= 0.75:
            self.results['status'] = 'GOOD'
        elif self.results['overall_compliance'] >= 0.60:
            self.results['status'] = 'PARTIAL'
        else:
            self.results['status'] = 'NEEDS_IMPROVEMENT'
        
        self._print_summary()
        return self.results
    
    def _validate_pr(self, pr_number: int) -> Dict[str, Any]:
        """Valide un PR individuel."""
        print(f"\n📋 Analysing PR #{pr_number}")
        print(f"-" * 70)
        
        pr_result = {
            'pr_number': pr_number,
            'title': '',
            'description': '',
            'files_changed': [],
            'clarifications': {},
            'compliance_score': 0.0,
            'status': 'PENDING',
            'recommendations': []
        }
        
        # Récupération PR info via gh CLI
        pr_info = self._get_pr_info(pr_number)
        if not pr_info:
            pr_result['status'] = 'NOT_FOUND'
            pr_result['recommendations'].append(
                f"PR #{pr_number} not found or not accessible"
            )
            print(f"⚠️  PR #{pr_number} not found")
            return pr_result
        
        pr_result['title'] = pr_info.get('title', '')
        pr_result['description'] = pr_info.get('body', '')
        
        # Récupération diff
        pr_diff = self._get_pr_diff(pr_number)
        if pr_diff:
            pr_result['files_changed'] = self._extract_changed_files(pr_diff)
        
        # Analyse conformité pour chaque clarification
        full_content = f"{pr_result['title']}\n{pr_result['description']}\n{pr_diff}"
        
        for clarif_name, clarif_config in self.clarifications.items():
            score = self._analyze_clarification(full_content, clarif_config)
            pr_result['clarifications'][clarif_name] = {
                'score': score,
                'weight': clarif_config['weight'],
                'weighted_score': score * clarif_config['weight']
            }
        
        # Calcul score global PR
        weighted_scores = [c['weighted_score'] 
                          for c in pr_result['clarifications'].values()]
        pr_result['compliance_score'] = sum(weighted_scores)
        
        # Status PR
        if pr_result['compliance_score'] >= 0.90:
            pr_result['status'] = 'EXCELLENT'
        elif pr_result['compliance_score'] >= 0.75:
            pr_result['status'] = 'GOOD'
        elif pr_result['compliance_score'] >= 0.60:
            pr_result['status'] = 'PARTIAL'
        else:
            pr_result['status'] = 'NEEDS_IMPROVEMENT'
        
        # Recommandations
        for clarif_name, clarif_data in pr_result['clarifications'].items():
            if clarif_data['score'] < 0.7:
                pr_result['recommendations'].append(
                    f"Low compliance for {clarif_name}: "
                    f"{clarif_data['score']:.1%}"
                )
        
        print(f"✓ Compliance: {pr_result['compliance_score']:.1%}")
        print(f"✓ Status: {pr_result['status']}")
        
        return pr_result
    
    def _get_pr_info(self, pr_number: int) -> Optional[Dict[str, Any]]:
        """Récupère info PR via gh CLI."""
        try:
            cmd = [
                'gh', 'pr', 'view', str(pr_number),
                '--json', 'title,body,state,number',
                '--repo', 'stephanedenis/Panini'
            ]
            
            result = subprocess.run(
                cmd,
                cwd=self.workspace_root,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                return json.loads(result.stdout)
            
            return None
            
        except (subprocess.TimeoutExpired, json.JSONDecodeError, Exception) as e:
            print(f"⚠️  Error fetching PR info: {e}")
            return None
    
    def _get_pr_diff(self, pr_number: int) -> str:
        """Récupère diff du PR via gh CLI."""
        try:
            cmd = [
                'gh', 'pr', 'diff', str(pr_number),
                '--repo', 'stephanedenis/Panini'
            ]
            
            result = subprocess.run(
                cmd,
                cwd=self.workspace_root,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                return result.stdout
            
            return ""
            
        except (subprocess.TimeoutExpired, Exception) as e:
            print(f"⚠️  Error fetching PR diff: {e}")
            return ""
    
    def _extract_changed_files(self, diff: str) -> List[str]:
        """Extrait liste fichiers modifiés du diff."""
        files = []
        for line in diff.split('\n'):
            if line.startswith('diff --git'):
                # Format: diff --git a/file b/file
                match = re.search(r'b/(.+)$', line)
                if match:
                    files.append(match.group(1))
        
        return files
    
    def _analyze_clarification(
        self, 
        content: str, 
        config: Dict[str, Any]
    ) -> float:
        """Analyse conformité pour une clarification."""
        content_lower = content.lower()
        
        # Comptage keywords positifs
        positive_count = sum(
            1 for kw in config['keywords']
            if kw.lower() in content_lower
        )
        
        # Comptage anti-keywords (pénalité)
        negative_count = sum(
            1 for akw in config['anti_keywords']
            if akw.lower() in content_lower
        )
        
        # Score = (positifs - négatifs) / total possible positifs
        max_positive = len(config['keywords'])
        
        if max_positive == 0:
            return 0.5  # Neutral si pas de keywords
        
        raw_score = (positive_count - negative_count) / max_positive
        
        # Normalisation [0, 1]
        return max(0.0, min(1.0, (raw_score + 1) / 2))
    
    def _print_summary(self):
        """Affiche résumé des résultats."""
        print(f"\n" + "=" * 70)
        print(f"📊 RÉSUMÉ CONFORMITÉ")
        print(f"=" * 70)
        print(f"PRs analysés: {len(self.results['prs_analyzed'])}")
        print(f"Compliance globale: {self.results['overall_compliance']:.1%}")
        print(f"Status: {self.results['status']}")
        print()
        
        print(f"DÉTAILS PAR PR:")
        for pr in self.results['prs_analyzed']:
            print(f"  PR #{pr['pr_number']}: {pr['compliance_score']:.1%} "
                  f"({pr['status']})")
            
            if pr['recommendations']:
                print(f"    Recommandations:")
                for rec in pr['recommendations'][:3]:  # Max 3
                    print(f"      - {rec}")
        
        print()
    
    def export_results(self, output_dir: Optional[Path] = None) -> Path:
        """Export résultats JSON."""
        if output_dir is None:
            output_dir = self.workspace_root
        
        timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H-%M-%SZ')
        output_file = output_dir / f'pr_compliance_report_{timestamp}.json'
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Rapport exporté: {output_file.name}")
        return output_file


def main():
    """Point d'entrée principal."""
    # Détection workspace
    workspace_root = os.getcwd()
    
    if '--workspace' in sys.argv:
        idx = sys.argv.index('--workspace')
        workspace_root = sys.argv[idx + 1]
    
    print(f"Workspace: {workspace_root}")
    
    # Validation
    validator = PRComplianceValidator(workspace_root)
    results = validator.validate_all_prs()
    
    # Export
    output_file = validator.export_results()
    
    # Exit code basé sur status
    if results['status'] in ['EXCELLENT', 'GOOD']:
        print(f"\n✅ STATUS: {results['status']}")
        sys.exit(0)
    elif results['status'] == 'PARTIAL':
        print(f"\n⚠️  STATUS: {results['status']}")
        sys.exit(1)
    else:
        print(f"\n❌ STATUS: {results['status']}")
        sys.exit(1)


if __name__ == '__main__':
    main()
