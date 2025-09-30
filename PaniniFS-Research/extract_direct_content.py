#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EXTRACTEUR CONTENU DIRECT - DONNÉES DHĀTU
=========================================
Extrait directement le contenu des fichiers récents pour voir
les vraies données linguistiques, pas le contenant.
"""

import os
import json
from pathlib import Path
from datetime import datetime, timedelta


def extract_real_content():
    """Extraire le contenu réel récent"""
    print("🔍 Extraction contenu réel des travaux...")
    
    # Fichiers modifiés récemment
    recent_files = []
    base_paths = ["/home/stephane/GitHub/Panini", "/home/stephane/GitHub/PaniniFS-Research"]
    
    for base_path in base_paths:
        if not os.path.exists(base_path):
            continue
        
        # Chercher fichiers modifiés dans les 24h
        cutoff = datetime.now() - timedelta(hours=24)
        
        for file_path in Path(base_path).rglob("*.py"):
            try:
                if datetime.fromtimestamp(file_path.stat().st_mtime) > cutoff:
                    recent_files.append(str(file_path))
            except:
                continue
    
    print(f"📁 {len(recent_files)} fichiers récents trouvés")
    
    # Analyser contenu
    content_analysis = {}
    
    for file_path in recent_files[:10]:  # Top 10
        print(f"\n📄 CONTENU: {os.path.basename(file_path)}")
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Extraire éléments intéressants
            analysis = analyze_file_content(content)
            
            if analysis['has_content']:
                content_analysis[os.path.basename(file_path)] = analysis
                display_content_summary(analysis)
                
        except Exception as e:
            print(f"   ❌ Erreur lecture: {e}")
    
    return content_analysis


def analyze_file_content(content: str) -> dict:
    """Analyser le contenu d'un fichier"""
    analysis = {
        'has_content': False,
        'dhatu_mentions': [],
        'class_definitions': [],
        'docstrings': [],
        'data_structures': [],
        'theoretical_concepts': []
    }
    
    lines = content.split('\n')
    
    # Chercher mentions dhātu
    for i, line in enumerate(lines):
        if 'dhatu' in line.lower() or 'dhātu' in line.lower():
            context = ' '.join(lines[max(0, i-1):i+2]).strip()
            if len(context) > 20:
                analysis['dhatu_mentions'].append(context[:150])
                analysis['has_content'] = True
    
    # Chercher définitions de classes avec contenu substantiel
    for i, line in enumerate(lines):
        if line.strip().startswith('class ') and ':' in line:
            class_name = line.split('class ')[1].split('(')[0].split(':')[0].strip()
            # Chercher docstring de la classe
            for j in range(i+1, min(i+10, len(lines))):
                if '"""' in lines[j] or "'''" in lines[j]:
                    docstring_start = j
                    docstring_lines = []
                    in_docstring = True
                    quote_type = '"""' if '"""' in lines[j] else "'''"
                    
                    # Si docstring commence et finit sur la même ligne
                    if lines[j].count(quote_type) >= 2:
                        docstring = lines[j].split(quote_type)[1]
                        if len(docstring.strip()) > 30:
                            analysis['class_definitions'].append({
                                'name': class_name,
                                'docstring': docstring.strip()[:200]
                            })
                            analysis['has_content'] = True
                    else:
                        # Docstring multi-lignes
                        for k in range(j+1, min(j+20, len(lines))):
                            if quote_type in lines[k]:
                                docstring = '\n'.join(lines[j+1:k]).strip()
                                if len(docstring) > 30:
                                    analysis['class_definitions'].append({
                                        'name': class_name,
                                        'docstring': docstring[:200]
                                    })
                                    analysis['has_content'] = True
                                break
                    break
    
    # Chercher structures de données intéressantes
    for i, line in enumerate(lines):
        if any(keyword in line.lower() for keyword in ['semantic', 'universal', 'theory', 'mapping']):
            if '=' in line and ('{' in line or '[' in line):
                context = ' '.join(lines[i:min(i+3, len(lines))]).strip()
                if len(context) > 30:
                    analysis['data_structures'].append(context[:150])
                    analysis['has_content'] = True
    
    # Chercher concepts théoriques dans les docstrings
    in_docstring = False
    docstring_content = []
    quote_type = None
    
    for line in lines:
        if not in_docstring and ('"""' in line or "'''" in line):
            quote_type = '"""' if '"""' in line else "'''"
            in_docstring = True
            # Vérifier si docstring commence et finit sur la même ligne
            if line.count(quote_type) >= 2:
                docstring_text = line.split(quote_type)[1]
                if len(docstring_text.strip()) > 50:
                    analysis['docstrings'].append(docstring_text.strip()[:300])
                    analysis['has_content'] = True
                in_docstring = False
            else:
                docstring_content = [line.split(quote_type)[1] if quote_type in line else '']
        elif in_docstring:
            if quote_type in line:
                docstring_content.append(line.split(quote_type)[0])
                full_docstring = '\n'.join(docstring_content).strip()
                if len(full_docstring) > 50:
                    analysis['docstrings'].append(full_docstring[:300])
                    analysis['has_content'] = True
                in_docstring = False
                docstring_content = []
            else:
                docstring_content.append(line)
    
    return analysis


def display_content_summary(analysis: dict):
    """Afficher résumé du contenu"""
    
    if analysis['dhatu_mentions']:
        print("   🔬 DHĀTU TROUVÉS:")
        for mention in analysis['dhatu_mentions'][:2]:
            print(f"      • {mention}")
    
    if analysis['class_definitions']:
        print("   📚 CLASSES DÉFINIES:")
        for class_def in analysis['class_definitions'][:2]:
            print(f"      • {class_def['name']}: {class_def['docstring'][:80]}...")
    
    if analysis['docstrings']:
        print("   📝 THÉORIES/CONCEPTS:")
        for docstring in analysis['docstrings'][:1]:
            print(f"      • {docstring[:100]}...")
    
    if analysis['data_structures']:
        print("   🗃️ STRUCTURES DONNÉES:")
        for struct in analysis['data_structures'][:2]:
            print(f"      • {struct}")


def main():
    """Extraction principale"""
    content_data = extract_real_content()
    
    print(f"\n📊 RÉSUMÉ CONTENU EXTRAIT:")
    print(f"   📁 Fichiers avec contenu: {len(content_data)}")
    
    total_dhatu = sum(len(data['dhatu_mentions']) for data in content_data.values())
    total_classes = sum(len(data['class_definitions']) for data in content_data.values())
    total_theories = sum(len(data['docstrings']) for data in content_data.values())
    
    print(f"   🔬 Mentions dhātu: {total_dhatu}")
    print(f"   📚 Classes définies: {total_classes}")
    print(f"   🧠 Théories/concepts: {total_theories}")
    
    # Sauvegarder
    with open('extracted_content.json', 'w', encoding='utf-8') as f:
        json.dump(content_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Contenu sauvé dans: extracted_content.json")


if __name__ == "__main__":
    main()