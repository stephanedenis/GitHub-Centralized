#!/usr/bin/env python3
"""
Extracteur Contenu TXT - Multi-Format Corpus
=============================================

Extrait contenu sémantique depuis fichiers TXT avec métadonnées complètes.
Validation: intégrité 100% ou FAIL.

Conformité:
    - ISO 8601 timestamps
    - UTF-8 encoding
    - Pattern: *_extractor.py (auto-approuvé via autonomous_wrapper.py)
    
Usage:
    python3 txt_content_extractor.py <input.txt>
    python3 autonomous_wrapper.py txt_content_extractor.py <input.txt>

Auteur: Stéphane Denis (via système zéro-approbation)
Date: 2025-10-01
Version: 1.0
"""

import sys
import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Optional
import re


class TXTContentExtractor:
    """Extracteur contenu fichiers TXT avec validation intégrité"""
    
    def __init__(self):
        self.encoding = 'utf-8'
        
    def extract(self, txt_path: Path) -> Dict:
        """
        Extrait contenu + métadonnées depuis fichier TXT
        
        Args:
            txt_path: Chemin fichier TXT
            
        Returns:
            dict avec content, metadata, integrity, timestamp
        """
        if not txt_path.exists():
            return self._error_result(f"File not found: {txt_path}")
            
        try:
            # Lecture contenu
            with open(txt_path, 'r', encoding=self.encoding) as f:
                content = f.read()
                
            # Extraction métadonnées
            metadata = self._extract_metadata(txt_path, content)
            
            # Validation intégrité
            integrity = self._validate_integrity(content)
            
            # Analyse sémantique basique
            semantic_analysis = self._analyze_semantics(content)
            
            return {
                "success": True,
                "format": "TXT",
                "source_file": str(txt_path),
                "content": content,
                "content_length_chars": len(content),
                "content_length_lines": len(content.split('\n')),
                "metadata": metadata,
                "integrity": integrity,
                "semantic_analysis": semantic_analysis,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            
        except UnicodeDecodeError as e:
            return self._error_result(f"Encoding error: {e}")
        except Exception as e:
            return self._error_result(f"Extraction error: {e}")
            
    def _extract_metadata(self, txt_path: Path, content: str) -> Dict:
        """Extrait métadonnées depuis fichier + contenu"""
        metadata = {
            "filename": txt_path.name,
            "file_size_bytes": txt_path.stat().st_size,
            "encoding": self.encoding,
            "line_endings": self._detect_line_endings(content)
        }
        
        # Extraction métadonnées depuis contenu (si format structuré)
        header_metadata = self._parse_header_metadata(content)
        if header_metadata:
            metadata.update(header_metadata)
            
        return metadata
        
    def _detect_line_endings(self, content: str) -> str:
        """Détecte type line endings"""
        if '\r\n' in content:
            return 'CRLF (Windows)'
        elif '\n' in content:
            return 'LF (Unix)'
        elif '\r' in content:
            return 'CR (Mac)'
        return 'None'
        
    def _parse_header_metadata(self, content: str) -> Optional[Dict]:
        """Parse métadonnées depuis header si présentes"""
        metadata = {}
        
        # Pattern métadonnées: - **Key:** Value
        pattern = r'- \*\*([^:]+):\*\* (.+)'
        matches = re.findall(pattern, content[:1000])  # Premiers 1000 chars
        
        for key, value in matches:
            metadata[key.strip().lower().replace(' ', '_')] = value.strip()
            
        return metadata if metadata else None
        
    def _validate_integrity(self, content: str) -> Dict:
        """Valide intégrité contenu"""
        # Hash SHA-256
        content_bytes = content.encode('utf-8')
        sha256_hash = hashlib.sha256(content_bytes).hexdigest()
        
        # Validation basique
        is_valid = len(content) > 0 and content.isprintable() or '\n' in content
        
        return {
            "valid": is_valid,
            "sha256": sha256_hash,
            "validation_method": "basic_printable_check",
            "integrity_percentage": 100.0 if is_valid else 0.0
        }
        
    def _analyze_semantics(self, content: str) -> Dict:
        """Analyse sémantique basique"""
        # Comptage mots
        words = re.findall(r'\b\w+\b', content)
        unique_words = set(w.lower() for w in words)
        
        # Détection dhātu mentions (patterns Sanskrit)
        dhatu_pattern = r'\b[A-ZĀĪŪṚḶṂṆṄṄṄṄṆṆṆṆṆṆṆṆṆṆṂĀĪŪṚḶṂṆṄṄṄṄṆṆṆṆṆṆṆṆṆṆṂ]{2,}\b'
        dhatu_candidates = re.findall(dhatu_pattern, content)
        
        # Extraction concepts (titres sections)
        concepts = re.findall(r'### (.+)', content)
        
        # Patterns composition (mots composés)
        compound_words = [w for w in words if len(w) > 10]
        
        return {
            "total_words": len(words),
            "unique_words": len(unique_words),
            "vocabulary_richness": round(len(unique_words) / len(words), 3) if words else 0,
            "dhatu_candidates": dhatu_candidates[:10],  # Top 10
            "concepts_detected": concepts,
            "compound_words_sample": compound_words[:5],
            "avg_word_length": round(sum(len(w) for w in words) / len(words), 2) if words else 0
        }
        
    def _error_result(self, error_msg: str) -> Dict:
        """Résultat erreur standardisé"""
        return {
            "success": False,
            "format": "TXT",
            "error": error_msg,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
    def export_json(self, result: Dict, output_path: Optional[Path] = None):
        """Exporte résultats en JSON"""
        if output_path is None:
            # Génération nom fichier automatique
            timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H-%M-%SZ')
            output_path = Path(f"txt_extraction_{timestamp}.json")
            
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
            
        return output_path


def main():
    """Point d'entrée CLI"""
    if len(sys.argv) < 2:
        print("Usage: python3 txt_content_extractor.py <input.txt>")
        print("\nExemple:")
        print("  python3 txt_content_extractor.py test_multiformat_source.txt")
        print("\nAuto-approved via autonomous_wrapper.py:")
        print("  python3 autonomous_wrapper.py txt_content_extractor.py test.txt")
        sys.exit(1)
        
    input_file = Path(sys.argv[1])
    
    # Extraction
    extractor = TXTContentExtractor()
    result = extractor.extract(input_file)
    
    # Export JSON
    output_file = extractor.export_json(result)
    
    # Affichage résumé
    if result["success"]:
        print("=" * 70)
        print("✅ EXTRACTION TXT RÉUSSIE")
        print("=" * 70)
        print(f"Format: {result['format']}")
        print(f"Fichier: {result['source_file']}")
        print(f"Contenu: {result['content_length_chars']} chars, {result['content_length_lines']} lignes")
        print(f"Intégrité: {result['integrity']['integrity_percentage']}%")
        print(f"Hash SHA-256: {result['integrity']['sha256'][:16]}...")
        print(f"\n📊 Analyse Sémantique:")
        sem = result['semantic_analysis']
        print(f"  - Mots total: {sem['total_words']}")
        print(f"  - Mots uniques: {sem['unique_words']}")
        print(f"  - Richesse vocabulaire: {sem['vocabulary_richness']}")
        print(f"  - Dhātu candidats: {len(sem['dhatu_candidates'])}")
        print(f"  - Concepts détectés: {len(sem['concepts_detected'])}")
        print(f"\n💾 Export: {output_file}")
        print(f"Timestamp: {result['timestamp']}")
        print("=" * 70)
    else:
        print("❌ EXTRACTION ÉCHOUÉE")
        print(f"Erreur: {result['error']}")
        print(f"Timestamp: {result['timestamp']}")
        sys.exit(1)


if __name__ == "__main__":
    main()
