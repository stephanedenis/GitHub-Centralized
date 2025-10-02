"""
🗜️ Mock Compressor - Compresseur MVP complet

Compresseur utilisant tous les composants MVP.

Pipeline:
1. Analyse texte → Représentation sémantique
2. Extraction graphe dhātu
3. Application fonctions (morpho/syntax/lexical)
4. Génération guide bytecode
5. Sérialisation complète

Auteur: Système Autonome
Date: 2025-10-01
"""

import json
from typing import Dict, Any, Optional

from semantic_representation import (
    SemanticRepresentation,
    SemanticUnitType,
    RelationType
)
from dhatu_graph import (
    DhatuSemanticGraph,
    DhatuNode,
    MorphologyFunctions,
    SyntaxFunctions,
    LexicalFunctions
)
from guide_bytecode import GuideBytecode


class MockCompressor:
    """
    Compresseur MVP intégrant tous composants.
    
    Workflow:
    - compress(): texte → (sémantique, dhātu, guide)
    - decompress(): (sémantique, dhātu, guide) → texte
    """
    
    def __init__(self):
        self.dhatu_graph = DhatuSemanticGraph()
        self._init_dhatu_graph()
    
    def _init_dhatu_graph(self) -> None:
        """Initialise graphe dhātu avec racines de base."""
        dhatus = [
            ('d1', '√kṛ', 'to do, make'),
            ('d2', '√gam', 'to go'),
            ('d3', '√bhū', 'to become, be'),
            ('d4', '√vac', 'to speak, say'),
            ('d5', '√dā', 'to give'),
            ('d6', '√jñā', 'to know, conquer'),
        ]
        
        for id_, root, meaning in dhatus:
            node = DhatuNode(
                id=id_,
                root=root,
                meaning=meaning,
                embedding=[0.5]*768  # Mock embedding
            )
            self.dhatu_graph.add_node(node)
    
    def compress(self, text: str, language: str = 'fr') -> Dict[str, Any]:
        """
        Compresse texte en représentation sémantique + guide.
        
        Args:
            text: Texte source
            language: Langue source
        
        Returns:
            Dict avec 'semantic', 'guide', 'stats'
        """
        # 1. Analyse texte → Représentation sémantique
        sem_repr = self._analyze_text(text, language)
        
        # 2. Génère guide restitution
        guide = self._generate_guide(text, sem_repr)
        
        # 3. Stats
        original_bytes = len(text.encode('utf-8'))
        semantic_bytes = len(json.dumps(sem_repr.to_dict()))
        guide_bytes = len(guide)
        total_bytes = semantic_bytes + guide_bytes
        
        ratio = (1 - total_bytes / original_bytes) * 100
        
        return {
            'semantic': sem_repr.to_dict(),
            'guide': guide.serialize().hex(),
            'dhatu_count': len(sem_repr.graph.nodes),
            'stats': {
                'original_size': original_bytes,
                'semantic_size': semantic_bytes,
                'guide_size': guide_bytes,
                'total_size': total_bytes,
                'compression_ratio': round(ratio, 2)
            }
        }
    
    def decompress(
        self,
        semantic_dict: Dict[str, Any],
        guide_hex: str
    ) -> str:
        """
        Décompresse représentation sémantique + guide → texte.
        
        Args:
            semantic_dict: Représentation sémantique (dict)
            guide_hex: Guide bytecode (hex string)
        
        Returns:
            Texte restitué
        """
        # 1. Parse représentation sémantique
        # (simplified: just reconstruct from sequence)
        sequence = semantic_dict['sequence']
        
        # 2. Reconstruit texte de base
        text_parts = []
        for unit in sequence:
            value = unit['value']
            text_parts.append(str(value))
        
        text = ' '.join(text_parts)
        
        # 3. Applique guide restitution
        guide_bytes = bytes.fromhex(guide_hex)
        guide = GuideBytecode.deserialize(guide_bytes)
        
        # Apply operations (simplified)
        for op in guide.parse_operations():
            # Mock: just log operations
            pass
        
        return text
    
    def _analyze_text(
        self,
        text: str,
        language: str
    ) -> SemanticRepresentation:
        """Analyse texte → représentation sémantique."""
        sem_repr = SemanticRepresentation(
            metadata={'language': language, 'source': 'mock_analyzer'}
        )
        
        # Mock analysis: split words, map to dhātu
        words = text.split()
        
        # Simple mapping (mock)
        word_to_dhatu = {
            'fait': '√kṛ',
            'va': '√gam',
            'devient': '√bhū',
            'dit': '√vac',
            'donne': '√dā',
            'sait': '√jñā',
            'roi': 'entity:roi',
            'royaume': 'entity:royaume'
        }
        
        for word in words:
            word_lower = word.lower().strip('.,!?')
            
            if word_lower in word_to_dhatu:
                value = word_to_dhatu[word_lower]
                
                if value.startswith('√'):
                    unit_type = SemanticUnitType.DHATU
                elif value.startswith('entity:'):
                    unit_type = SemanticUnitType.ENTITY
                    value = value.replace('entity:', '')
                else:
                    unit_type = SemanticUnitType.CONCEPT
                
                sem_repr.add_unit(unit_type, value)
            else:
                # Unknown word → pattern
                sem_repr.add_unit(SemanticUnitType.PATTERN, word)
        
        # Add relations (mock: sequential dependencies)
        for i in range(len(sem_repr.sequence) - 1):
            current = sem_repr.sequence[i]
            next_unit = sem_repr.sequence[i + 1]
            
            if current.type == SemanticUnitType.ENTITY and \
               next_unit.type == SemanticUnitType.DHATU:
                sem_repr.add_relation(
                    current,
                    next_unit,
                    RelationType.AGENT
                )
        
        return sem_repr
    
    def _generate_guide(
        self,
        original_text: str,
        sem_repr: SemanticRepresentation
    ) -> GuideBytecode:
        """Génère guide restitution."""
        guide = GuideBytecode()
        
        # Mock: add some operations
        # (real version would compute delta between generic and original)
        
        # Example: replace generic with original form
        guide.add_replace(position=0, old_len=4, new_text="Le")
        
        # Example: disambiguate polysemy
        if len(sem_repr.graph.nodes) > 0:
            node_id = list(sem_repr.graph.nodes.keys())[0]
            guide.add_disambiguate(node_id=node_id, choice=1)
        
        return guide
    
    def validate_compression(
        self,
        text: str,
        language: str = 'fr'
    ) -> Dict[str, Any]:
        """Valide compression-décompression (round-trip)."""
        # Compress
        compressed = self.compress(text, language)
        
        # Decompress
        restored = self.decompress(
            compressed['semantic'],
            compressed['guide']
        )
        
        # Compare
        original_words = set(text.lower().split())
        restored_words = set(restored.lower().split())
        
        word_overlap = len(original_words & restored_words)
        word_coverage = word_overlap / len(original_words) * 100
        
        return {
            'original': text,
            'restored': restored,
            'compression_stats': compressed['stats'],
            'validation': {
                'word_coverage': round(word_coverage, 2),
                'lossless': word_coverage == 100.0
            }
        }


# Example usage
if __name__ == "__main__":
    compressor = MockCompressor()
    
    # Test texts
    texts = [
        "Le roi fait la guerre",
        "Le sage dit la vérité",
        "L'homme devient libre"
    ]
    
    print("=" * 60)
    print("MOCK COMPRESSOR - Tests MVP")
    print("=" * 60)
    
    for text in texts:
        print(f"\n📝 Original: {text}")
        
        # Validate compression
        result = compressor.validate_compression(text)
        
        print(f"🗜️  Compressed:")
        print(f"   - Dhātu nodes: {result['compression_stats']['semantic_size']} bytes")
        print(f"   - Guide: {result['compression_stats']['guide_size']} bytes")
        print(f"   - Total: {result['compression_stats']['total_size']} bytes")
        print(f"   - Ratio: {result['compression_stats']['compression_ratio']}%")
        
        print(f"📤 Restored: {result['restored']}")
        print(f"✅ Word coverage: {result['validation']['word_coverage']}%")
    
    # Full compression example
    print("\n" + "=" * 60)
    print("DETAILED COMPRESSION EXAMPLE")
    print("=" * 60)
    
    text = "Le roi conquiert le royaume"
    compressed = compressor.compress(text, 'fr')
    
    print(f"\n📝 Original text: {text}")
    print(f"📊 Stats:")
    for key, value in compressed['stats'].items():
        print(f"   {key}: {value}")
    
    print(f"\n🌳 Semantic graph:")
    print(json.dumps(
        compressed['semantic']['graph'],
        indent=2,
        ensure_ascii=False
    ))
    
    print(f"\n🔢 Guide (first 100 hex chars):")
    print(compressed['guide'][:100] + "...")
