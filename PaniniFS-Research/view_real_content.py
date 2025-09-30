#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VISUALISEUR DHĀTU ET THÉORIES - CONTENU RÉEL
===========================================
Affiche les détails concrets des dhātu et théories en cours,
pas juste les noms de fichiers.
"""

import json
import re
from pathlib import Path


def show_dhatu_details():
    """Afficher les détails concrets des dhātu trouvés"""
    
    # Lire le contenu extrait
    try:
        with open('extracted_content.json', 'r') as f:
            content_data = json.load(f)
    except:
        print("❌ Fichier extracted_content.json non trouvé")
        return
    
    print("🔬 DÉTAILS DHĀTU EN COURS D'ÉTUDE:")
    print("=" * 50)
    
    dhatu_found = False
    
    for filename, data in content_data.items():
        if data['dhatu_mentions']:
            print(f"\n📄 {filename}")
            for mention in data['dhatu_mentions']:
                print(f"   🔸 {mention}")
            dhatu_found = True
    
    if not dhatu_found:
        print("   ℹ️ Pas de mentions dhātu spécifiques dans les fichiers récents")
    
    print("\n" + "=" * 50)


def show_theory_details():
    """Afficher les détails des théories en développement"""
    
    try:
        with open('extracted_content.json', 'r') as f:
            content_data = json.load(f)
    except:
        return
    
    print("\n🧠 THÉORIES EN DÉVELOPPEMENT:")
    print("=" * 50)
    
    for filename, data in content_data.items():
        if data['docstrings']:
            print(f"\n📚 {filename}")
            
            for i, docstring in enumerate(data['docstrings'][:2]):  # Max 2 par fichier
                print(f"\n   📝 Théorie {i+1}:")
                
                # Nettoyer et formatter la docstring
                clean_doc = clean_docstring(docstring)
                if len(clean_doc) > 100:
                    print(f"   {clean_doc}")
                    
                    # Extraire concepts clés
                    concepts = extract_key_concepts(clean_doc)
                    if concepts:
                        print(f"   🔑 Concepts: {', '.join(concepts[:5])}")


def show_class_details():
    """Afficher les détails des classes définies"""
    
    try:
        with open('extracted_content.json', 'r') as f:
            content_data = json.load(f)
    except:
        return
    
    print("\n📚 CLASSES ET STRUCTURES DÉFINIES:")
    print("=" * 50)
    
    for filename, data in content_data.items():
        if data['class_definitions']:
            print(f"\n🏗️ {filename}")
            
            for class_def in data['class_definitions']:
                print(f"   📦 {class_def['name']}")
                if class_def['docstring']:
                    print(f"      → {class_def['docstring']}")


def show_data_structures():
    """Afficher les structures de données trouvées"""
    
    try:
        with open('extracted_content.json', 'r') as f:
            content_data = json.load(f)
    except:
        return
    
    print("\n🗃️ STRUCTURES DE DONNÉES:")
    print("=" * 50)
    
    for filename, data in content_data.items():
        if data['data_structures']:
            print(f"\n💾 {filename}")
            
            for struct in data['data_structures'][:3]:  # Max 3 par fichier
                # Nettoyer la structure
                clean_struct = ' '.join(struct.split())
                if len(clean_struct) > 50:
                    print(f"   🔹 {clean_struct[:120]}...")


def clean_docstring(docstring):
    """Nettoyer une docstring pour affichage"""
    # Enlever les caractères spéciaux de formatage
    clean = re.sub(r'[=]+', '', docstring)
    clean = re.sub(r'[-]+', '', clean)
    clean = re.sub(r'\n+', ' ', clean)
    clean = re.sub(r'\s+', ' ', clean)
    return clean.strip()


def extract_key_concepts(text):
    """Extraire les concepts clés d'un texte"""
    # Mots-clés théoriques importants
    concepts = []
    
    # Patterns pour concepts
    patterns = [
        r'\b(semantic\w*)\b',
        r'\b(universal\w*)\b',
        r'\b(panini\w*)\b',
        r'\b(information\w*)\b',
        r'\b(theory\w*)\b',
        r'\b(théorie\w*)\b',
        r'\b(foundation\w*)\b',
        r'\b(fondement\w*)\b',
        r'\b(composition\w*)\b',
        r'\b(fractal\w*)\b',
        r'\b(mapping\w*)\b',
        r'\b(domain\w*)\b',
        r'\b(autonomous\w*)\b',
        r'\b(autonome\w*)\b'
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        concepts.extend(matches)
    
    # Enlever doublons et retourner
    return list(set(concepts))


def show_active_research_focus():
    """Identifier le focus de recherche actuel"""
    
    try:
        with open('extracted_content.json', 'r') as f:
            content_data = json.load(f)
    except:
        return
    
    print("\n🎯 FOCUS DE RECHERCHE ACTUEL:")
    print("=" * 50)
    
    # Compter les mentions par thème
    themes = {
        'Sémantique/Universal': 0,
        'Systèmes Autonomes': 0,
        'Théorie Information': 0,
        'Dhātu/Linguistique': 0,
        'Infrastructure/Tech': 0
    }
    
    theme_files = {key: [] for key in themes.keys()}
    
    for filename, data in content_data.items():
        filename_lower = filename.lower()
        all_text = ' '.join(data['docstrings']).lower()
        
        # Classifier par thème
        if any(word in all_text for word in ['semantic', 'universal', 'fondement']):
            themes['Sémantique/Universal'] += 1
            theme_files['Sémantique/Universal'].append(filename)
        
        if any(word in all_text for word in ['autonome', 'autonomous', 'apprentissage']):
            themes['Systèmes Autonomes'] += 1
            theme_files['Systèmes Autonomes'].append(filename)
        
        if any(word in all_text for word in ['information', 'theory', 'théorie']):
            themes['Théorie Information'] += 1
            theme_files['Théorie Information'].append(filename)
        
        if any(word in all_text for word in ['dhatu', 'dhātu', 'linguist']):
            themes['Dhātu/Linguistique'] += 1
            theme_files['Dhātu/Linguistique'].append(filename)
        
        if any(word in filename_lower for word in ['github', 'renommeur', 'dashboard']):
            themes['Infrastructure/Tech'] += 1
            theme_files['Infrastructure/Tech'].append(filename)
    
    # Afficher résultats
    for theme, count in sorted(themes.items(), key=lambda x: x[1], reverse=True):
        if count > 0:
            print(f"\n🔸 {theme}: {count} fichier(s)")
            for filename in theme_files[theme][:3]:  # Max 3 exemples
                print(f"   • {filename}")
    
    # Identifier focus principal
    main_focus = max(themes.items(), key=lambda x: x[1])
    if main_focus[1] > 0:
        print(f"\n🎯 FOCUS PRINCIPAL: {main_focus[0]} ({main_focus[1]} fichiers)")


def main():
    """Affichage principal du contenu"""
    print("📖 VISUALISEUR CONTENU PANINI - DÉTAILS RÉELS")
    print("=" * 60)
    
    # Vérifier si le fichier d'extraction existe
    if not Path('extracted_content.json').exists():
        print("\n⚠️ Extraction du contenu requise...")
        print("📝 Exécutez d'abord: python3 extract_direct_content.py")
        return
    
    # Afficher les différentes sections
    show_active_research_focus()
    show_theory_details()
    show_class_details() 
    show_dhatu_details()
    show_data_structures()
    
    print("\n" + "=" * 60)
    print("✅ Visualisation contenu terminée")
    print("💡 Ceci montre le CONTENU réel, pas juste les noms de fichiers")


if __name__ == "__main__":
    main()