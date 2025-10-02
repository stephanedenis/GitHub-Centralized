"""
📐 Semantic Representation - Structures données

Représentation sémantique hybride (séquence + graphe).

Basé sur décisions architecturales:
- Séquence: Ordre textuel préservé
- Graphe: Relations sémantiques riches
- Unités: Dhātu, patterns, concepts, idiomes

Auteur: Système Autonome
Date: 2025-10-01
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from enum import Enum


class SemanticUnitType(Enum):
    """Types d'unités sémantiques."""
    DHATU = "dhatu"
    PATTERN = "pattern"
    CONCEPT = "concept"
    IDIOM = "idiom"
    ENTITY = "entity"


class RelationType(Enum):
    """Types de relations sémantiques."""
    AGENT = "AGENT"  # Sujet acteur
    PATIENT = "PATIENT"  # Objet patient
    INSTRUMENT = "INSTRUMENT"  # Moyen
    MANNER = "MANNER"  # Manière
    CAUSE = "CAUSE"  # Cause
    PURPOSE = "PURPOSE"  # But
    LOCATION = "LOCATION"  # Lieu
    TIME = "TIME"  # Temps


@dataclass
class SemanticUnit:
    """Unité sémantique atomique."""
    id: str
    type: SemanticUnitType
    value: Any
    position: int  # Position dans séquence
    graph_node_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'type': self.type.value,
            'value': str(self.value),
            'position': self.position,
            'graph_node_id': self.graph_node_id,
            'metadata': self.metadata
        }


@dataclass
class SemanticNode:
    """Nœud du graphe sémantique."""
    id: str
    type: SemanticUnitType
    value: Any
    attributes: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'type': self.type.value,
            'value': str(self.value),
            'attributes': self.attributes
        }


@dataclass
class SemanticEdge:
    """Arête du graphe sémantique."""
    from_id: str
    to_id: str
    relation: RelationType
    weight: float = 1.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'from': self.from_id,
            'to': self.to_id,
            'relation': self.relation.value,
            'weight': self.weight
        }


@dataclass
class SemanticGraph:
    """Graphe conceptuel pour relations sémantiques."""
    nodes: Dict[str, SemanticNode] = field(default_factory=dict)
    edges: List[SemanticEdge] = field(default_factory=list)
    
    def add_node(self, node: SemanticNode) -> str:
        """Ajoute nœud et retourne ID."""
        self.nodes[node.id] = node
        return node.id
    
    def add_edge(
        self, 
        from_id: str, 
        to_id: str, 
        relation: RelationType,
        weight: float = 1.0
    ) -> None:
        """Ajoute relation entre nœuds."""
        self.edges.append(SemanticEdge(from_id, to_id, relation, weight))
    
    def get_neighbors(self, node_id: str) -> List[str]:
        """Retourne voisins d'un nœud."""
        return [
            edge.to_id for edge in self.edges 
            if edge.from_id == node_id
        ]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'nodes': {nid: n.to_dict() for nid, n in self.nodes.items()},
            'edges': [e.to_dict() for e in self.edges]
        }


@dataclass
class SemanticRepresentation:
    """
    Représentation sémantique hybride complète.
    
    Combine:
    - Séquence: Préserve ordre textuel
    - Graphe: Relations sémantiques profondes
    """
    sequence: List[SemanticUnit] = field(default_factory=list)
    graph: SemanticGraph = field(default_factory=SemanticGraph)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def add_unit(
        self, 
        unit_type: SemanticUnitType,
        value: Any,
        create_node: bool = True
    ) -> SemanticUnit:
        """Ajoute unité sémantique."""
        unit_id = f"u{len(self.sequence)}"
        position = len(self.sequence)
        
        node_id = None
        if create_node:
            node = SemanticNode(
                id=f"n{len(self.graph.nodes)}",
                type=unit_type,
                value=value
            )
            node_id = self.graph.add_node(node)
        
        unit = SemanticUnit(
            id=unit_id,
            type=unit_type,
            value=value,
            position=position,
            graph_node_id=node_id
        )
        
        self.sequence.append(unit)
        return unit
    
    def add_relation(
        self, 
        from_unit: SemanticUnit,
        to_unit: SemanticUnit,
        relation: RelationType
    ) -> None:
        """Ajoute relation entre unités."""
        if from_unit.graph_node_id and to_unit.graph_node_id:
            self.graph.add_edge(
                from_unit.graph_node_id,
                to_unit.graph_node_id,
                relation
            )
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'sequence': [u.to_dict() for u in self.sequence],
            'graph': self.graph.to_dict(),
            'metadata': self.metadata
        }
    
    def __len__(self) -> int:
        return len(self.sequence)


# Example usage
if __name__ == "__main__":
    # Create semantic representation
    sem_repr = SemanticRepresentation()
    
    # Add units (example: "Le roi conquiert le royaume")
    roi = sem_repr.add_unit(
        SemanticUnitType.ENTITY, 
        "roi"
    )
    
    conquiert = sem_repr.add_unit(
        SemanticUnitType.DHATU,
        "√jñā"  # conquer/know
    )
    
    royaume = sem_repr.add_unit(
        SemanticUnitType.ENTITY,
        "royaume"
    )
    
    # Add relations
    sem_repr.add_relation(roi, conquiert, RelationType.AGENT)
    sem_repr.add_relation(conquiert, royaume, RelationType.PATIENT)
    
    # Print
    import json
    print(json.dumps(sem_repr.to_dict(), indent=2, ensure_ascii=False))
