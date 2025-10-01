#!/usr/bin/env python3
"""
Extracteur Métadonnées Traducteurs - Mode Autonome
===================================================

Mission: Analyser corpus existant pour identifier métadonnées traducteurs
Focus: QUI/QUAND/OÙ >> nombre (principe clarifications 2025-09-30)

Objectifs:
1. Scanner tous fichiers corpus disponibles
2. Extraire métadonnées: qui, quand, où, contexte
3. Identifier patterns biais culturels/temporels
4. Détecter signatures stylistiques

Date: 2025-09-30
Conformité: ISO 8601, clarifications mission
"""

from datetime import datetime, timezone
from pathlib import Path
import json
import re
from typing import Dict, List, Optional, Any
from collections import defaultdict


class TranslatorMetadata:
    """Métadonnées traducteur selon clarifications mission"""
    
    def __init__(self, name: str):
        self.name = name
        self.translations: List[Dict] = []
        self.epoch: Optional[str] = None  # Époque traduction
        self.cultural_context: Optional[str] = None  # Contexte culturel
        self.source_lang: Optional[str] = None
        self.target_lang: Optional[str] = None
        self.corpus: List[str] = []
        self.style_markers: Dict[str, Any] = {}
        self.bias_indicators: Dict[str, Any] = {}
        
    def to_dict(self) -> Dict:
        return {
            "qui": self.name,
            "quand": self.epoch,
            "ou": self.cultural_context,
            "langue_source": self.source_lang,
            "langue_cible": self.target_lang,
            "corpus": self.corpus,
            "nombre_traductions": len(self.translations),
            "style_markers": self.style_markers,
            "biais": self.bias_indicators
        }


class TranslatorExtractor:
    """Extracteur métadonnées traducteurs depuis corpus"""
    
    def __init__(self):
        self.translators: Dict[str, TranslatorMetadata] = {}
        self.corpus_files: List[Path] = []
        self.extraction_log: List[Dict] = []
        
    def scan_corpus_files(self, directory: str = ".") -> List[Path]:
        """Scanner fichiers corpus disponibles"""
        print(f"🔍 Scan corpus dans: {directory}")
        
        patterns = [
            "*corpus*.json",
            "*traduction*.json", 
            "*translation*.json",
            "*multilingu*.json",
            "*content*.json"
        ]
        
        found_files = []
        for pattern in patterns:
            found_files.extend(Path(directory).glob(pattern))
        
        # Chercher aussi dans sous-dossiers
        for pattern in patterns:
            found_files.extend(Path(directory).glob(f"**/{pattern}"))
        
        self.corpus_files = list(set(found_files))[:50]  # Max 50 fichiers
        
        print(f"   Fichiers trouvés: {len(self.corpus_files)}")
        for f in self.corpus_files[:10]:
            print(f"      • {f.name}")
        if len(self.corpus_files) > 10:
            print(f"      ... et {len(self.corpus_files) - 10} autres")
        
        return self.corpus_files
    
    def extract_from_filename(self, filepath: Path) -> Optional[Dict]:
        """Extraire indices depuis nom fichier"""
        filename = filepath.stem
        
        # Patterns dates ISO 8601 dans nom fichier
        date_pattern = r'(\d{4}[-_]\d{2}[-_]\d{2})'
        dates = re.findall(date_pattern, filename)
        
        # Patterns langues (codes ISO 639)
        lang_pattern = r'[_\-](en|fr|de|es|it|pt|ru|zh|ja|ar)[_\-]'
        langs = re.findall(lang_pattern, filename.lower())
        
        # Patterns traduction
        trans_patterns = [
            r'trad(?:uction|uctor)?[_\-](\w+)',
            r'translator[_\-](\w+)',
            r'by[_\-](\w+)',
            r'trans[_\-](\w+)'
        ]
        
        translator_hints = []
        for pattern in trans_patterns:
            matches = re.findall(pattern, filename.lower())
            translator_hints.extend(matches)
        
        if dates or langs or translator_hints:
            return {
                "source": "filename",
                "dates": dates,
                "languages": langs,
                "translator_hints": translator_hints
            }
        return None
    
    def extract_from_json_content(self, filepath: Path) -> List[Dict]:
        """Extraire métadonnées depuis contenu JSON"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            findings = []
            
            # Patterns clés métadonnées
            metadata_keys = [
                'translator', 'traducteur', 'author', 'auteur',
                'translation', 'traduction', 'translated_by',
                'epoch', 'epoque', 'date', 'year', 'annee',
                'context', 'contexte', 'location', 'lieu',
                'source_lang', 'target_lang', 'langue_source', 'langue_cible'
            ]
            
            def recursive_search(obj, path="root"):
                """Recherche récursive métadonnées"""
                if isinstance(obj, dict):
                    for key, value in obj.items():
                        key_lower = key.lower()
                        
                        # Vérifier si clé correspond à métadonnée
                        for meta_key in metadata_keys:
                            if meta_key in key_lower:
                                findings.append({
                                    "path": f"{path}.{key}",
                                    "key": key,
                                    "value": str(value)[:200],
                                    "type": type(value).__name__
                                })
                        
                        # Récursion
                        recursive_search(value, f"{path}.{key}")
                
                elif isinstance(obj, list) and len(obj) < 100:
                    for i, item in enumerate(obj[:20]):  # Max 20 items
                        recursive_search(item, f"{path}[{i}]")
            
            recursive_search(data)
            return findings
            
        except Exception as e:
            self.extraction_log.append({
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "file": str(filepath),
                "error": str(e)
            })
            return []
    
    def analyze_style_markers(self, text: str) -> Dict:
        """Analyser patterns stylistiques texte"""
        if not text or len(text) < 50:
            return {}
        
        # Métriques basiques
        words = text.split()
        sentences = text.count('.') + text.count('!') + text.count('?')
        
        markers = {
            "longueur_mots_moyenne": len(' '.join(words)) / max(len(words), 1),
            "phrases_complexes": text.count(',') / max(sentences, 1),
            "formalisation": "élevée" if any(w in text.lower() for w in ['néanmoins', 'toutefois', 'ainsi']) else "standard"
        }
        
        # Subordinations
        subordinations = len(re.findall(r'\bque\b|\bqui\b|\bdont\b', text.lower()))
        markers["subordinations_ratio"] = subordinations / max(len(words), 1)
        
        return markers
    
    def process_all_corpus(self):
        """Traiter tous fichiers corpus"""
        print(f"\n📊 Traitement corpus...")
        print(f"   Timestamp: {datetime.now(timezone.utc).isoformat()}\n")
        
        total_findings = 0
        
        for filepath in self.corpus_files:
            print(f"   Analyse: {filepath.name}")
            
            # Extraction nom fichier
            filename_data = self.extract_from_filename(filepath)
            if filename_data:
                print(f"      Indices filename: {len(filename_data.get('dates', []))} dates, "
                      f"{len(filename_data.get('languages', []))} langues")
                total_findings += 1
            
            # Extraction contenu
            content_findings = self.extract_from_json_content(filepath)
            if content_findings:
                print(f"      Métadonnées trouvées: {len(content_findings)}")
                total_findings += len(content_findings)
                
                # Créer/mettre à jour traducteurs
                for finding in content_findings:
                    if 'translator' in finding['key'].lower() or 'traducteur' in finding['key'].lower():
                        name = finding['value']
                        if name not in self.translators:
                            self.translators[name] = TranslatorMetadata(name)
                        self.translators[name].corpus.append(str(filepath.name))
        
        print(f"\n   Total indices trouvés: {total_findings}")
        print(f"   Traducteurs identifiés: {len(self.translators)}")
    
    def generate_report(self) -> Dict:
        """Générer rapport extraction"""
        report = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "scan_summary": {
                "fichiers_scannes": len(self.corpus_files),
                "traducteurs_identifies": len(self.translators),
                "total_findings": len(self.extraction_log)
            },
            "traducteurs": {
                name: meta.to_dict() 
                for name, meta in self.translators.items()
            },
            "fichiers_corpus": [str(f) for f in self.corpus_files],
            "extraction_log": self.extraction_log[-50:]  # Derniers 50
        }
        return report
    
    def export_results(self, filepath: str = "translator_metadata_extraction.json"):
        """Exporter résultats"""
        report = self.generate_report()
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"\n�� Résultats exportés: {filepath}")
        return filepath


def create_sample_translator_database():
    """Créer base données exemple traducteurs"""
    print("\n📚 Création base données exemple traducteurs...")
    
    sample_translators = [
        {
            "qui": "Jean Dupont",
            "quand": "1985-2010",
            "ou": "France, Paris, milieu universitaire",
            "langue_source": "en",
            "langue_cible": "fr",
            "corpus": ["Bhagavad Gita", "Upanishads", "Yoga Sutras"],
            "biais": {
                "culturel": "Occidentalisation concepts orientaux",
                "temporel": "Post-structuralisme français années 80",
                "académique": "Formalisation excessive, vocabulaire technique"
            },
            "style_markers": {
                "subordinations_complexes": 0.78,
                "formalisation": "très élevée",
                "vocabulaire_spécialisé": "sanskrit translitéré systématiquement",
                "notes_explicatives": "nombreuses (ratio 1:3)"
            }
        },
        {
            "qui": "Maria González",
            "quand": "2015-2020",
            "ou": "Espagne, Madrid, traductrice indépendante",
            "langue_source": "sa",
            "langue_cible": "es",
            "corpus": ["Mahabharata", "Ramayana excerpts"],
            "biais": {
                "culturel": "Catholicisme ibérique influence interprétation",
                "temporel": "Sensibilité contemporaine genre/inclusion",
                "personnel": "Accent sur aspects dévotionnels"
            },
            "style_markers": {
                "subordinations_complexes": 0.45,
                "formalisation": "moyenne",
                "accessibilité": "grand public",
                "adaptation_culturelle": "forte (équivalents chrétiens)"
            }
        },
        {
            "qui": "राज शर्मा (Raj Sharma)",
            "quand": "2010-2025",
            "ou": "Inde, Varanasi, pandit traditionnel",
            "langue_source": "sa",
            "langue_cible": "hi",
            "corpus": ["Vedas", "Brahma Sutras", "Dhatu Patha"],
            "biais": {
                "culturel": "Tradition védique orthodoxe",
                "temporel": "Perspective traditionnelle intemporelle",
                "religieux": "Cadre hindou brahmanique strict"
            },
            "style_markers": {
                "subordinations_complexes": 0.92,
                "formalisation": "extrêmement élevée",
                "références_scripturaires": "systématiques",
                "commentaires_classiques": "intégrés (Shankara, etc.)"
            }
        }
    ]
    
    output = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "description": "Base données exemple traducteurs (QUI/QUAND/OÙ + biais/styles)",
        "principe": "Traducteur = auteur avec interprétation propre",
        "focus": "Métadonnées > nombre",
        "traducteurs": sample_translators
    }
    
    with open("translator_database_sample.json", 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"   ✅ Base exemple créée: translator_database_sample.json")
    print(f"   Traducteurs exemple: {len(sample_translators)}")
    
    return sample_translators


def main():
    """Extraction autonome métadonnées traducteurs"""
    print("=" * 70)
    print("🔍 EXTRACTION MÉTADONNÉES TRADUCTEURS - MODE AUTONOME")
    print("=" * 70)
    print(f"Timestamp: {datetime.now(timezone.utc).isoformat()}\n")
    
    extractor = TranslatorExtractor()
    
    # 1. Scanner corpus
    corpus_files = extractor.scan_corpus_files()
    
    if not corpus_files:
        print("\n⚠️  Aucun fichier corpus trouvé")
        print("   Création base données exemple à la place...")
        create_sample_translator_database()
    else:
        # 2. Traiter corpus
        extractor.process_all_corpus()
        
        # 3. Exporter résultats
        extractor.export_results()
        
        # 4. Créer aussi base exemple
        create_sample_translator_database()
    
    # 5. Résumé final
    print("\n" + "=" * 70)
    print("📋 RÉSUMÉ EXTRACTION")
    print("=" * 70)
    
    if extractor.translators:
        print(f"\n✅ Traducteurs identifiés: {len(extractor.translators)}")
        for name, meta in list(extractor.translators.items())[:5]:
            print(f"\n   Traducteur: {name}")
            print(f"   - Corpus: {len(meta.corpus)} fichiers")
            if meta.epoch:
                print(f"   - Époque: {meta.epoch}")
            if meta.cultural_context:
                print(f"   - Contexte: {meta.cultural_context}")
    else:
        print("\n⚠️  Aucun traducteur dans corpus existant")
        print("   (Base exemple créée avec 3 traducteurs)")
    
    print(f"\n✅ Extraction terminée!")
    print(f"   Fichiers exportés:")
    print(f"   - translator_metadata_extraction.json")
    print(f"   - translator_database_sample.json")
    print(f"\n   Timestamp: {datetime.now(timezone.utc).isoformat()}")


if __name__ == "__main__":
    main()
