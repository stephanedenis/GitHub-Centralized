#!/usr/bin/env python3
"""
Analyseur Patterns Biais/Styles Traducteurs
============================================

Analyse automatique patterns biais culturels/temporels et signatures stylistiques.
Focus: Style + biais = patterns identifiables

Date: 2025-09-30
"""

from datetime import datetime, timezone
import json
from typing import Dict, List
from collections import defaultdict


class BiasPatternAnalyzer:
    """Analyseur patterns biais et styles traducteurs"""
    
    def __init__(self, translator_db_path: str = "translator_database_sample.json"):
        with open(translator_db_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.translators = data['traducteurs']
        self.patterns = defaultdict(list)
        
    def analyze_cultural_bias_patterns(self) -> Dict:
        """Identifier patterns biais culturels récurrents"""
        print("\n🌍 ANALYSE BIAIS CULTURELS")
        print("=" * 60)
        
        cultural_patterns = defaultdict(list)
        
        for translator in self.translators:
            qui = translator['qui']
            ou = translator.get('ou', '')
            biais = translator.get('biais', {})
            
            # Extraire composantes géographiques/culturelles
            if 'France' in ou or 'Paris' in ou:
                cultural_patterns['Occidental/Français'].append(qui)
            if 'Espagne' in ou or 'Madrid' in ou:
                cultural_patterns['Occidental/Ibérique'].append(qui)
            if 'Inde' in ou or 'India' in ou:
                cultural_patterns['Oriental/Indien'].append(qui)
            
            # Analyser types biais
            for bias_type, bias_desc in biais.items():
                cultural_patterns[f"Type:{bias_type}"].append(qui)
        
        print("\nPatterns culturels détectés:")
        for pattern, translators in cultural_patterns.items():
            print(f"   • {pattern}: {len(translators)} traducteur(s)")
            for t in translators:
                print(f"      - {t}")
        
        return dict(cultural_patterns)
    
    def analyze_temporal_bias_patterns(self) -> Dict:
        """Identifier patterns biais temporels"""
        print("\n⏰ ANALYSE BIAIS TEMPORELS")
        print("=" * 60)
        
        temporal_patterns = defaultdict(list)
        
        for translator in self.translators:
            qui = translator['qui']
            quand = translator.get('quand', '')
            biais = translator.get('biais', {})
            
            # Extraire période
            if '-' in quand:
                start, end = quand.split('-')
                start_year = int(start)
                
                if start_year < 2000:
                    temporal_patterns['Pré-2000'].append(qui)
                elif start_year < 2010:
                    temporal_patterns['2000-2010'].append(qui)
                else:
                    temporal_patterns['Post-2010'].append(qui)
            
            # Analyser biais temporel spécifique
            temporal_bias = biais.get('temporel', '')
            if temporal_bias:
                temporal_patterns[f"Biais:{temporal_bias[:40]}"].append(qui)
        
        print("\nPatterns temporels détectés:")
        for pattern, translators in temporal_patterns.items():
            print(f"   • {pattern}: {len(translators)} traducteur(s)")
        
        return dict(temporal_patterns)
    
    def analyze_style_signature_patterns(self) -> Dict:
        """Identifier signatures stylistiques"""
        print("\n✍️  ANALYSE SIGNATURES STYLISTIQUES")
        print("=" * 60)
        
        style_signatures = defaultdict(list)
        
        for translator in self.translators:
            qui = translator['qui']
            style_markers = translator.get('style_markers', {})
            
            # Analyser niveau formalisation
            formalisation = style_markers.get('formalisation', '')
            if 'élevée' in formalisation or 'très' in formalisation:
                style_signatures['Formalisation élevée'].append(qui)
            elif 'moyenne' in formalisation:
                style_signatures['Formalisation moyenne'].append(qui)
            
            # Analyser subordinations
            sub_ratio = style_markers.get('subordinations_complexes', 0)
            if sub_ratio > 0.7:
                style_signatures['Style complexe (sub>0.7)'].append(qui)
            elif sub_ratio < 0.5:
                style_signatures['Style simple (sub<0.5)'].append(qui)
            
            # Patterns spécifiques
            for key, value in style_markers.items():
                if isinstance(value, str) and len(value) > 0:
                    style_signatures[f"Pattern:{key}"].append(qui)
        
        print("\nSignatures stylistiques détectées:")
        for signature, translators in style_signatures.items():
            print(f"   • {signature}: {len(translators)} traducteur(s)")
        
        return dict(style_signatures)
    
    def cross_reference_patterns(self) -> Dict:
        """Cross-référencer patterns biais + styles"""
        print("\n🔗 CROSS-RÉFÉRENCEMENT PATTERNS")
        print("=" * 60)
        
        cross_refs = []
        
        for translator in self.translators:
            qui = translator['qui']
            ou = translator.get('ou', '')
            quand = translator.get('quand', '')
            biais = translator.get('biais', {})
            style = translator.get('style_markers', {})
            
            # Créer profil combiné
            profile = {
                "traducteur": qui,
                "contexte_geo": ou.split(',')[0] if ',' in ou else ou,
                "periode": quand,
                "biais_dominants": [k for k, v in biais.items()],
                "style_caracteristiques": [
                    f"{k}:{v}" for k, v in style.items() 
                    if isinstance(v, (int, float, str)) and str(v)
                ][:3]
            }
            
            cross_refs.append(profile)
        
        print("\nProfils cross-référencés:")
        for profile in cross_refs:
            print(f"\n   Traducteur: {profile['traducteur']}")
            print(f"   - Contexte: {profile['contexte_geo']} ({profile['periode']})")
            print(f"   - Biais: {', '.join(profile['biais_dominants'])}")
            print(f"   - Style: {', '.join(profile['style_caracteristiques'][:2])}")
        
        return {"profiles": cross_refs}
    
    def identify_universal_vs_contextual(self) -> Dict:
        """Identifier éléments universels vs contextuels"""
        print("\n🌐 UNIVERSAUX vs CONTEXTUELS")
        print("=" * 60)
        
        # Compter récurrences
        all_bias_types = []
        all_style_markers = []
        
        for translator in self.translators:
            biais = translator.get('biais', {})
            style = translator.get('style_markers', {})
            
            all_bias_types.extend(biais.keys())
            all_style_markers.extend(style.keys())
        
        # Récurrents = potentiellement universaux
        from collections import Counter
        bias_freq = Counter(all_bias_types)
        style_freq = Counter(all_style_markers)
        
        universal_candidates = {
            "biais_recurrents": [
                (k, v) for k, v in bias_freq.items() 
                if v >= len(self.translators) * 0.6  # 60% traducteurs
            ],
            "style_recurrents": [
                (k, v) for k, v in style_freq.items()
                if v >= len(self.translators) * 0.6
            ]
        }
        
        contextual = {
            "biais_uniques": [k for k, v in bias_freq.items() if v == 1],
            "style_uniques": [k for k, v in style_freq.items() if v == 1]
        }
        
        print("\n✅ Patterns récurrents (candidats universaux):")
        for k, v in universal_candidates["biais_recurrents"]:
            print(f"   • Biais '{k}': {v}/{len(self.translators)} traducteurs")
        for k, v in universal_candidates["style_recurrents"]:
            print(f"   • Style '{k}': {v}/{len(self.translators)} traducteurs")
        
        print("\n🔸 Patterns contextuels (spécifiques):")
        print(f"   • Biais uniques: {len(contextual['biais_uniques'])}")
        print(f"   • Styles uniques: {len(contextual['style_uniques'])}")
        
        return {
            "universal_candidates": universal_candidates,
            "contextual": contextual
        }
    
    def export_analysis(self, filepath: str = "translator_bias_style_analysis.json"):
        """Exporter analyse complète"""
        analysis = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "traducteurs_analyses": len(self.translators),
            "patterns_culturels": self.analyze_cultural_bias_patterns(),
            "patterns_temporels": self.analyze_temporal_bias_patterns(),
            "signatures_stylistiques": self.analyze_style_signature_patterns(),
            "cross_references": self.cross_reference_patterns(),
            "universaux_vs_contextuels": self.identify_universal_vs_contextual()
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Analyse exportée: {filepath}")
        return analysis


def main():
    """Analyse autonome patterns biais/styles"""
    print("=" * 70)
    print("🔬 ANALYSE PATTERNS BIAIS/STYLES TRADUCTEURS")
    print("=" * 70)
    print(f"Timestamp: {datetime.now(timezone.utc).isoformat()}\n")
    
    analyzer = BiasPatternAnalyzer()
    
    print(f"Traducteurs chargés: {len(analyzer.translators)}")
    
    # Analyse complète
    analysis = analyzer.export_analysis()
    
    # Résumé
    print("\n" + "=" * 70)
    print("📊 RÉSUMÉ ANALYSE")
    print("=" * 70)
    
    print(f"\n✅ Traducteurs analysés: {len(analyzer.translators)}")
    print(f"✅ Patterns culturels: {len(analysis['patterns_culturels'])} détectés")
    print(f"✅ Patterns temporels: {len(analysis['patterns_temporels'])} détectés")
    print(f"✅ Signatures stylistiques: {len(analysis['signatures_stylistiques'])} détectées")
    
    universal = analysis['universaux_vs_contextuels']['universal_candidates']
    print(f"\n🎯 Candidats universaux:")
    print(f"   • Biais récurrents: {len(universal['biais_recurrents'])}")
    print(f"   • Styles récurrents: {len(universal['style_recurrents'])}")
    
    print(f"\n✅ Analyse terminée!")
    print(f"   Fichier: translator_bias_style_analysis.json")
    print(f"   Timestamp: {datetime.now(timezone.utc).isoformat()}")


if __name__ == "__main__":
    main()
