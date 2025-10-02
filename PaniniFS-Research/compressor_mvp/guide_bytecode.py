"""
🔢 Guide Bytecode - Format compression guide

Guide de restitution en bytecode ultra-compact.

Basé sur décisions architecturales:
- Opcodes optimisés (replace, insert, delete, disambiguate, specify)
- Format binaire compact (struct packing)
- Minimal par design

Auteur: Système Autonome
Date: 2025-10-01
"""

import struct
from enum import IntEnum
from dataclasses import dataclass
from typing import List, Tuple


class GuideOpcode(IntEnum):
    """Opcodes pour guide restitution."""
    
    # Deltas textuels
    REPLACE = 0x01
    INSERT = 0x02
    DELETE = 0x03
    
    # Patches sémantiques
    DISAMBIGUATE = 0x10
    SPECIFY = 0x11
    
    # Marqueurs contextuels
    CONTEXT_START = 0x20
    CONTEXT_END = 0x21


@dataclass
class GuideOperation:
    """Opération guide."""
    opcode: GuideOpcode
    data: bytes


class GuideBytecode:
    """Guide de restitution en bytecode compact."""
    
    def __init__(self, version: int = 1):
        self.version = version
        self.operations: bytes = b''
    
    def add_replace(
        self, 
        position: int, 
        old_len: int, 
        new_text: str
    ) -> None:
        """Ajoute opération REPLACE."""
        # Format: [opcode:1][position:2][old_len:1][new_text:variable][null:1]
        op = struct.pack(
            'BHB',
            GuideOpcode.REPLACE,
            position & 0xFFFF,  # Max 65535
            old_len & 0xFF  # Max 255
        )
        op += new_text.encode('utf-8')
        op += b'\x00'  # Null terminator
        self.operations += op
    
    def add_insert(self, position: int, text: str) -> None:
        """Ajoute opération INSERT."""
        # Format: [opcode:1][position:2][text:variable][null:1]
        op = struct.pack(
            'BH',
            GuideOpcode.INSERT,
            position & 0xFFFF
        )
        op += text.encode('utf-8')
        op += b'\x00'
        self.operations += op
    
    def add_delete(self, position: int, length: int) -> None:
        """Ajoute opération DELETE."""
        # Format: [opcode:1][position:2][length:1]
        op = struct.pack(
            'BHB',
            GuideOpcode.DELETE,
            position & 0xFFFF,
            length & 0xFF
        )
        self.operations += op
    
    def add_disambiguate(self, node_id: str, choice: int) -> None:
        """Ajoute patch disambiguation."""
        # Format: [opcode:1][choice:1][node_hash:2]
        node_hash = hash(node_id) & 0xFFFF
        op = struct.pack(
            'BBH',
            GuideOpcode.DISAMBIGUATE,
            choice & 0xFF,
            node_hash
        )
        self.operations += op
    
    def add_specify(self, node_id: str, specification: str) -> None:
        """Ajoute patch specification."""
        # Format: [opcode:1][node_hash:2][spec:variable][null:1]
        node_hash = hash(node_id) & 0xFFFF
        op = struct.pack(
            'BH',
            GuideOpcode.SPECIFY,
            node_hash
        )
        op += specification.encode('utf-8')
        op += b'\x00'
        self.operations += op
    
    def serialize(self) -> bytes:
        """Sérialise guide en bytes."""
        # Header: [version:1][op_length_high:1][op_length_low:1] = 3 bytes
        op_len = len(self.operations)
        header = struct.pack(
            'BBB',  # 3 bytes unpacked
            self.version,
            (op_len >> 8) & 0xFF,  # high byte
            op_len & 0xFF  # low byte
        )
        return header + self.operations
    
    @classmethod
    def deserialize(cls, data: bytes) -> 'GuideBytecode':
        """Désérialise guide depuis bytes."""
        # Parse header (3 bytes)
        version, op_len_high, op_len_low = struct.unpack('BBB', data[:3])
        op_length = (op_len_high << 8) | op_len_low
        operations = data[3:3+op_length]
        
        guide = cls(version=version)
        guide.operations = operations
        return guide
    
    def parse_operations(self) -> List[GuideOperation]:
        """Parse operations depuis bytecode."""
        ops = []
        offset = 0
        
        while offset < len(self.operations):
            opcode = GuideOpcode(self.operations[offset])
            
            if opcode == GuideOpcode.REPLACE:
                # Read position, old_len, new_text
                position, old_len = struct.unpack_from('HB', self.operations, offset + 1)
                offset += 4
                # Find null terminator
                null_pos = self.operations.find(b'\x00', offset)
                new_text = self.operations[offset:null_pos].decode('utf-8')
                offset = null_pos + 1
                ops.append(GuideOperation(opcode, (position, old_len, new_text)))
            
            elif opcode == GuideOpcode.INSERT:
                position = struct.unpack_from('H', self.operations, offset + 1)[0]
                offset += 3
                null_pos = self.operations.find(b'\x00', offset)
                text = self.operations[offset:null_pos].decode('utf-8')
                offset = null_pos + 1
                ops.append(GuideOperation(opcode, (position, text)))
            
            elif opcode == GuideOpcode.DELETE:
                position, length = struct.unpack_from('HB', self.operations, offset + 1)
                offset += 4
                ops.append(GuideOperation(opcode, (position, length)))
            
            elif opcode in [GuideOpcode.DISAMBIGUATE, GuideOpcode.SPECIFY]:
                # Skip for now
                offset += 4
            
            else:
                break  # Unknown opcode
        
        return ops
    
    def __len__(self) -> int:
        """Taille totale guide (header + operations)."""
        return 3 + len(self.operations)


# Example usage
if __name__ == "__main__":
    guide = GuideBytecode()
    
    # Add operations
    guide.add_replace(position=7, old_len=8, new_text="conquiert")
    guide.add_disambiguate(node_id='n2', choice=2)
    guide.add_insert(position=30, text=" avec bravoure")
    guide.add_delete(position=50, length=5)
    
    # Serialize
    bytecode = guide.serialize()
    print(f"Guide size: {len(bytecode)} bytes")
    print(f"Operations: {len(guide.operations)} bytes")
    
    # Deserialize
    restored = GuideBytecode.deserialize(bytecode)
    print(f"Restored operations: {len(restored.operations)} bytes")
    
    # Parse
    ops = restored.parse_operations()
    print(f"Parsed {len(ops)} operations:")
    for op in ops:
        print(f"  {op.opcode.name}: {op.data}")
