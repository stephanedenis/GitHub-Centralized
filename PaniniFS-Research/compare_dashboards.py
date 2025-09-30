#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
COMPARATEUR DASHBOARDS PANINI
============================
Ouvre les deux dashboards pour comparaison :
- Ancien dashboard statique (modèle complet)
- Nouveau dashboard dynamique (activité focalisée)
"""

import webbrowser
import time


def main():
    """Ouvrir les dashboards pour comparaison"""
    print("🔗 Ouverture dashboards Panini pour comparaison...\n")
    
    # URLs des dashboards
    dashboard_static = "http://localhost:8889/dashboard_real_panini.html"
    dashboard_dynamic = "http://localhost:8889/dashboard_activity_focused.html"
    
    print(f"📊 Dashboard STATIQUE (ancien):")
    print(f"   {dashboard_static}")
    print(f"   → Modèle complet, tous les panels, mise à jour 30s")
    
    print(f"\n🔥 Dashboard DYNAMIQUE (nouveau):")
    print(f"   {dashboard_dynamic}")
    print(f"   → Focus activité, panels minimisés, mise à jour 10s")
    
    # Ouvrir automatiquement si demandé
    response = input("\n🌐 Ouvrir automatiquement dans le navigateur ? (y/n): ")
    
    if response.lower() in ['y', 'yes', 'oui', 'o']:
        print("\n🚀 Ouverture dashboards...")
        webbrowser.open(dashboard_static)
        time.sleep(2)
        webbrowser.open(dashboard_dynamic)
        print("✅ Dashboards ouverts dans le navigateur")
    
    print(f"\n📋 Pour comparaison manuelle :")
    print(f"   1. Ouvrez les deux URLs ci-dessus")
    print(f"   2. Comparez l'information visible")
    print(f"   3. Observez la fréquence de mise à jour")
    print(f"   4. Notez la hiérarchisation de l'information")


if __name__ == "__main__":
    main()