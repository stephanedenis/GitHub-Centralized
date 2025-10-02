"""
🌳 Dhātu Semantic Graph - Graphe sémantique pur + fonctions

Graphe dhātu séparé des fonctions morphologie/syntaxe/lexical.

Basé sur décisions architecturales:
- Graphe sémantique pur (dhātu uniquement)
- Fonctions généralisables séparées (morphology, syntax, lexical)
- Propagation par similarité vectorielle

Auteur: Système Autonome
Date: 2025-10-01
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import json


@dataclass
class DhatuNode:
    """Nœud dhātu (racine Sanskrit)."""
    id: str
    root: str  # Ex: √kṛ
    meaning: str
    embedding: List[float] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DhatuSemanticGraph:
    """
    Graphe sémantique pur (dhātu uniquement).
    
    Pas de morphologie/syntaxe/lexical ici.
    """
    nodes: Dict[str, DhatuNode] = field(default_factory=dict)
    edges: Dict[str, List[str]] = field(default_factory=dict)
    
    def add_node(self, node: DhatuNode) -> str:
        """Ajoute nœud dhātu."""
        self.nodes[node.id] = node
        self.edges[node.id] = []
        return node.id
    
    def add_edge(self, from_id: str, to_id: str) -> None:
        """Ajoute arête entre dhātu."""
        if from_id in self.edges:
            if to_id not in self.edges[from_id]:
                self.edges[from_id].append(to_id)
    
    def get_neighbors(self, node_id: str) -> List[DhatuNode]:
        """Retourne voisins d'un dhātu."""
        if node_id not in self.edges:
            return []
        return [
            self.nodes[nid] for nid in self.edges[node_id]
            if nid in self.nodes
        ]
    
    def find_similar(
        self,
        embedding: List[float],
        top_k: int = 5,
        threshold: float = 0.7
    ) -> List[DhatuNode]:
        """
        Trouve dhātu similaires par cosine similarity.
        
        Pour propagation sémantique.
        """
        import math
        
        def cosine_similarity(a: List[float], b: List[float]) -> float:
            dot = sum(x * y for x, y in zip(a, b))
            norm_a = math.sqrt(sum(x**2 for x in a))
            norm_b = math.sqrt(sum(y**2 for y in b))
            return dot / (norm_a * norm_b) if norm_a and norm_b else 0.0
        
        # Calcule similarités
        similarities = []
        for node in self.nodes.values():
            if not node.embedding:
                continue
            sim = cosine_similarity(embedding, node.embedding)
            if sim >= threshold:
                similarities.append((node, sim))
        
        # Trie et retourne top_k
        similarities.sort(key=lambda x: x[1], reverse=True)
        return [node for node, _ in similarities[:top_k]]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'nodes': {
                nid: {
                    'id': n.id,
                    'root': n.root,
                    'meaning': n.meaning,
                    'embedding': n.embedding[:5] if n.embedding else [],
                    'metadata': n.metadata
                }
                for nid, n in self.nodes.items()
            },
            'edges': self.edges
        }


# ================================================
# Fonctions séparées (généralisables)
# ================================================


class MorphologyFunctions:
    """Fonctions morphologie (séparées du graphe)."""
    
    @staticmethod
    def inflect(dhatu: DhatuNode, features: Dict[str, str]) -> str:
        """
        Inflexion morphologique.
        
        features: {tense, person, number, mood, voice}
        """
        # Mock implementation
        root = dhatu.root.replace('√', '')
        tense = features.get('tense', 'present')
        person = features.get('person', '3')
        
        # Simple heuristic
        if tense == 'present':
            if person == '3':
                return f"{root}ati"
        elif tense == 'past':
            return f"a{root}at"
        
        return root
    
    @staticmethod
    def derive(dhatu: DhatuNode, affix: str) -> str:
        """Dérivation (kṛt/taddhita)."""
        root = dhatu.root.replace('√', '')
        return f"{root}{affix}"


class SyntaxFunctions:
    """Fonctions syntaxe (séparées du graphe)."""
    
    @staticmethod
    def kāraka_assign(
        verb: DhatuNode,
        arguments: Dict[str, Any]
    ) -> Dict[str, str]:
        """
        Assigne kāraka (rôles sémantiques).
        
        kāraka: kartṛ (agent), karman (patient), karaṇa (instrument)
        """
        roles = {}
        
        if 'subject' in arguments:
            roles['kartṛ'] = arguments['subject']
        if 'object' in arguments:
            roles['karman'] = arguments['object']
        if 'instrument' in arguments:
            roles['karaṇa'] = arguments['instrument']
        
        return roles
    
    @staticmethod
    def vibhakti_select(role: str, noun: str) -> str:
        """
        Sélectionne vibhakti (case) pour rôle.
        
        kartṛ → nominative, karman → accusative, etc.
        """
        case_map = {
            'kartṛ': 'nominative',
            'karman': 'accusative',
            'karaṇa': 'instrumental'
        }
        return case_map.get(role, 'nominative')


class LexicalFunctions:
    """Fonctions lexicales (séparées du graphe)."""
    
    @staticmethod
    def lexicalize(dhatu: DhatuNode, language: str) -> str:
        """Lexicalisation vers langue cible."""
        # Mock translation dictionary
        translations = {
            'fr': {
                '√kṛ': 'faire',
                '√gam': 'aller',
                '√bhū': 'devenir'
            },
            'en': {
                '√kṛ': 'do',
                '√gam': 'go',
                '√bhū': 'become'
            }
        }
        
        lang_dict = translations.get(language, {})
        return lang_dict.get(dhatu.root, dhatu.root)
    
    @staticmethod
    def disambiguate_polysemy(
        dhatu: DhatuNode,
        context: List[DhatuNode]
    ) -> str:
        """Résout polysémie via contexte."""
        # Mock: return first sense
        return dhatu.meaning.split(',')[0].strip()


# Example usage
if __name__ == "__main__":
    # Create graph
    graph = DhatuSemanticGraph()
    
    # Add dhātu nodes
    kr = DhatuNode(
        id='d1',
        root='√kṛ',
        meaning='to do, make',
        embedding=[0.5, 0.3, 0.8] + [0.0]*765
    )
    graph.add_node(kr)
    
    gam = DhatuNode(
        id='d2',
        root='√gam',
        meaning='to go',
        embedding=[0.4, 0.6, 0.2] + [0.0]*765
    )
    graph.add_node(gam)
    
    bhu = DhatuNode(
        id='d3',
        root='√bhū',
        meaning='to become, be',
        embedding=[0.6, 0.2, 0.7] + [0.0]*765
    )
    graph.add_node(bhu)
    
    # Add relations
    graph.add_edge('d1', 'd2')
    graph.add_edge('d1', 'd3')
    
    # Test functions
    morph = MorphologyFunctions()
    print(f"Inflect √kṛ (present, 3): {morph.inflect(kr, {'tense': 'present'})}")
    print(f"Derive √kṛ + -aka: {morph.derive(kr, 'aka')}")
    
    syntax = SyntaxFunctions()
    roles = syntax.kāraka_assign(kr, {'subject': 'rāja', 'object': 'rājya'})
    print(f"Kāraka roles: {roles}")
    
    lex = LexicalFunctions()
    print(f"Lexicalize √kṛ to French: {lex.lexicalize(kr, 'fr')}")
    
    # Search similar
    query_embedding = [0.55, 0.25, 0.75] + [0.0]*765
    similar = graph.find_similar(query_embedding, top_k=2, threshold=0.5)
    print(f"Similar dhātu: {[n.root for n in similar]}")
    
    # Export
    print(json.dumps(graph.to_dict(), indent=2, ensure_ascii=False))
