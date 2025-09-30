#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VISUALISEUR CONTENU PANINI - DONNÉES RÉELLES
===========================================
Affiche le CONTENU réel des travaux, pas le contenant :
- Dhātu en cours d'analyse avec détails
- Patterns linguistiques émergents
- Corpus samples et évolutions
- Concepts sémantiques développés
- Théories en construction
"""

import json
import os
from pathlib import Path
from datetime import datetime
import re


class PaniniContentViewer:
    """Visualiseur du contenu réel des travaux Panini"""
    
    def __init__(self):
        self.base_paths = [
            "/home/stephane/GitHub/Panini",
            "/home/stephane/GitHub/PaniniFS-Research"
        ]
        
    def extract_dhatu_content(self) -> dict:
        """Extraire le contenu réel des dhātu en cours"""
        dhatu_content = {
            'active_dhatu': [],
            'evolution_patterns': [],
            'semantic_mappings': [],
            'research_notes': []
        }
        
        # Chercher fichiers avec contenu dhātu
        for base_path in self.base_paths:
            if not os.path.exists(base_path):
                continue
                
            for file_path in Path(base_path).rglob("*.py"):
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        
                    # Extraire structures dhātu
                    dhatu_structures = self.parse_dhatu_structures(content, str(file_path))
                    if dhatu_structures:
                        dhatu_content['active_dhatu'].extend(dhatu_structures)
                        
                    # Extraire patterns d'évolution
                    evolution_data = self.parse_evolution_patterns(content, str(file_path))
                    if evolution_data:
                        dhatu_content['evolution_patterns'].extend(evolution_data)
                        
                    # Extraire mappings sémantiques
                    semantic_data = self.parse_semantic_mappings(content, str(file_path))
                    if semantic_data:
                        dhatu_content['semantic_mappings'].extend(semantic_data)
                        
                except Exception:
                    continue
        
        return dhatu_content
    
    def parse_dhatu_structures(self, content: str, file_path: str) -> list:
        """Parser les structures dhātu du code"""
        structures = []
        
        # Chercher définitions de dhātu
        dhatu_patterns = [
            r'class\s+(\w*[Dd]hatu\w*)\s*[:\(]([^{]*)',
            r'@dataclass.*?class\s+(\w*[Dd]hatu\w*)',
            r'(\w*dhatu\w*)\s*=\s*{([^}]+)}',
            r'"([^"]*dhatu[^"]*)":\s*{([^}]+)}'
        ]
        
        for pattern in dhatu_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE | re.DOTALL)
            for match in matches:
                structures.append({
                    'name': match.group(1),
                    'definition': match.group(2) if len(match.groups()) > 1 else '',
                    'file': os.path.basename(file_path),
                    'type': 'dhatu_structure'
                })
        
        # Chercher commentaires sur dhātu
        comment_patterns = [
            r'#.*?([dD]hatu.*?)$',
            r'"""([^"]*[dD]hatu[^"]*)"""',
            r"'''([^']*[dD]hatu[^']*)'''"
        ]
        
        for pattern in comment_patterns:
            matches = re.finditer(pattern, content, re.MULTILINE | re.DOTALL)
            for match in matches:
                comment = match.group(1).strip()
                if len(comment) > 20:  # Commentaires substantiels
                    structures.append({
                        'content': comment,
                        'file': os.path.basename(file_path),
                        'type': 'dhatu_comment'
                    })
        
        return structures
    
    def parse_evolution_patterns(self, content: str, file_path: str) -> list:
        """Parser les patterns d'évolution"""
        patterns = []
        
        # Chercher mentions d'évolution
        evolution_patterns = [
            r'evolution[^.]*\.([^,\n]+)',
            r'temporal[^.]*\.([^,\n]+)',
            r'aspect[^.]*\.([^,\n]+)',
            r'transformation[^.]*\.([^,\n]+)'
        ]
        
        for pattern in evolution_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                patterns.append({
                    'pattern': match.group(1).strip(),
                    'file': os.path.basename(file_path),
                    'context': self.get_context(content, match.start(), 100)
                })
        
        return patterns
    
    def parse_semantic_mappings(self, content: str, file_path: str) -> list:
        """Parser les mappings sémantiques"""
        mappings = []
        
        # Chercher mappings sémantiques
        mapping_patterns = [
            r'semantic[^=]*=\s*{([^}]+)}',
            r'mapping[^=]*=\s*{([^}]+)}',
            r'universal[^=]*=\s*{([^}]+)}',
            r'"semantic":\s*{([^}]+)}'
        ]
        
        for pattern in mapping_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE | re.DOTALL)
            for match in matches:
                mappings.append({
                    'mapping': match.group(1).strip(),
                    'file': os.path.basename(file_path),
                    'type': 'semantic_mapping'
                })
        
        return mappings
    
    def get_context(self, content: str, position: int, length: int = 50) -> str:
        """Obtenir le contexte autour d'une position"""
        start = max(0, position - length)
        end = min(len(content), position + length)
        return content[start:end].strip()
    
    def extract_active_theories(self) -> list:
        """Extraire les théories en cours de développement"""
        theories = []
        
        for base_path in self.base_paths:
            if not os.path.exists(base_path):
                continue
                
            for file_path in Path(base_path).rglob("*.py"):
                if any(keyword in str(file_path).lower() for keyword in 
                       ['theory', 'theorie', 'semantic', 'universal', 'foundational']):
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                        
                        # Extraire docstrings principales
                        docstring_pattern = r'"""([^"]{100,}?)"""'
                        matches = re.finditer(docstring_pattern, content, re.DOTALL)
                        
                        for match in matches:
                            theory_text = match.group(1).strip()
                            if any(keyword in theory_text.lower() for keyword in 
                                   ['theory', 'universal', 'semantic', 'panini', 'dhatu']):
                                theories.append({
                                    'file': os.path.basename(file_path),
                                    'theory': theory_text[:500] + '...' if len(theory_text) > 500 else theory_text,
                                    'concepts': self.extract_key_concepts(theory_text)
                                })
                                
                    except Exception:
                        continue
        
        return theories
    
    def extract_key_concepts(self, text: str) -> list:
        """Extraire les concepts clés d'un texte"""
        # Mots-clés conceptuels importants
        concept_patterns = [
            r'\b([A-Z][a-z]+(?:[A-Z][a-z]+)+)\b',  # CamelCase concepts
            r'\b(universal\w*)\b',
            r'\b(semantic\w*)\b', 
            r'\b(panini\w*)\b',
            r'\b(dhatu\w*)\b',
            r'\b(fractal\w*)\b',
            r'\b(composition\w*)\b',
            r'\b(information\w*)\b'
        ]
        
        concepts = set()
        for pattern in concept_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                concept = match.group(1)
                if len(concept) > 3:  # Éviter mots trop courts
                    concepts.add(concept)
        
        return list(concepts)[:10]  # Top 10 concepts
    
    def extract_corpus_samples(self) -> list:
        """Extraire des échantillons de corpus réels"""
        samples = []
        
        for base_path in self.base_paths:
            if not os.path.exists(base_path):
                continue
                
            # Chercher fichiers JSON avec contenu corpus
            for file_path in Path(base_path).rglob("*.json"):
                if any(keyword in str(file_path).lower() for keyword in 
                       ['corpus', 'collection', 'dhatu', 'analysis']):
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            data = json.load(f)
                        
                        # Extraire échantillons intéressants
                        interesting_samples = self.find_interesting_samples(data, str(file_path))
                        samples.extend(interesting_samples)
                        
                    except Exception:
                        continue
        
        return samples[:20]  # Top 20 échantillons
    
    def find_interesting_samples(self, data: dict, file_path: str) -> list:
        """Trouver les échantillons intéressants dans les données"""
        samples = []
        
        def explore_data(obj, path="", depth=0):
            if depth > 3:  # Limiter profondeur
                return
                
            if isinstance(obj, dict):
                for key, value in obj.items():
                    current_path = f"{path}.{key}" if path else key
                    
                    # Chercher contenu linguistique intéressant
                    if any(keyword in key.lower() for keyword in 
                           ['dhatu', 'root', 'semantic', 'meaning', 'definition', 'example']):
                        if isinstance(value, (str, list)) and str(value).strip():
                            samples.append({
                                'file': os.path.basename(file_path),
                                'path': current_path,
                                'content': str(value)[:200] + '...' if len(str(value)) > 200 else str(value),
                                'type': 'linguistic_data'
                            })
                    
                    explore_data(value, current_path, depth + 1)
                    
            elif isinstance(obj, list) and obj:
                # Examiner quelques éléments de la liste
                for i, item in enumerate(obj[:3]):
                    explore_data(item, f"{path}[{i}]", depth + 1)
        
        explore_data(data)
        return samples
    
    def generate_content_view(self) -> dict:
        """Générer la vue complète du contenu"""
        print("🔍 Extraction du contenu réel des travaux Panini...")
        
        content_view = {
            'timestamp': datetime.now().isoformat(),
            'dhatu_content': self.extract_dhatu_content(),
            'active_theories': self.extract_active_theories(),
            'corpus_samples': self.extract_corpus_samples(),
            'summary': {}
        }
        
        # Calculer résumé
        dhatu_count = len(content_view['dhatu_content']['active_dhatu'])
        theory_count = len(content_view['active_theories'])
        sample_count = len(content_view['corpus_samples'])
        
        content_view['summary'] = {
            'dhatu_structures_found': dhatu_count,
            'active_theories': theory_count,
            'corpus_samples': sample_count,
            'total_content_items': dhatu_count + theory_count + sample_count
        }
        
        return content_view
    
    def display_content_summary(self, content_view: dict):
        """Afficher résumé du contenu"""
        summary = content_view['summary']
        
        print(f"\n📊 CONTENU RÉEL TROUVÉ:")
        print(f"   🔬 Structures dhātu: {summary['dhatu_structures_found']}")
        print(f"   🧠 Théories actives: {summary['active_theories']}")
        print(f"   📝 Échantillons corpus: {summary['corpus_samples']}")
        print(f"   📋 Total items: {summary['total_content_items']}")
        
        # Aperçu dhātu
        if content_view['dhatu_content']['active_dhatu']:
            print(f"\n🔬 APERÇU DHĀTU:")
            for dhatu in content_view['dhatu_content']['active_dhatu'][:3]:
                if dhatu.get('name'):
                    print(f"   • {dhatu['name']} ({dhatu['file']})")
                elif dhatu.get('content'):
                    print(f"   • {dhatu['content'][:60]}... ({dhatu['file']})")
        
        # Aperçu théories
        if content_view['active_theories']:
            print(f"\n🧠 THÉORIES EN COURS:")
            for theory in content_view['active_theories'][:2]:
                print(f"   📚 {theory['file']}")
                print(f"      {theory['theory'][:100]}...")
                if theory['concepts']:
                    print(f"      Concepts: {', '.join(theory['concepts'][:3])}")
        
        # Aperçu corpus
        if content_view['corpus_samples']:
            print(f"\n📝 ÉCHANTILLONS CORPUS:")
            for sample in content_view['corpus_samples'][:3]:
                print(f"   • {sample['path']} ({sample['file']})")
                print(f"     {sample['content'][:80]}...")


def main():
    """Visualiser le contenu réel"""
    viewer = PaniniContentViewer()
    content_view = viewer.generate_content_view()
    
    # Sauvegarder
    with open('panini_content_view.json', 'w', encoding='utf-8') as f:
        json.dump(content_view, f, indent=2, ensure_ascii=False)
    
    # Afficher résumé
    viewer.display_content_summary(content_view)
    
    print(f"\n💾 Contenu détaillé sauvé dans: panini_content_view.json")
    print(f"📄 {content_view['summary']['total_content_items']} éléments de contenu extraits")


if __name__ == "__main__":
    main()