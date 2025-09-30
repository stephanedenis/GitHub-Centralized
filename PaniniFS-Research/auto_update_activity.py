#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AUTO-UPDATER DASHBOARD ACTIVITÉ
==============================
Met à jour automatiquement les données d'activité pour le dashboard focalisé.
Lance le scanner d'activité en boucle pour capturer les changements en temps réel.
"""

import time
import subprocess
import sys
from datetime import datetime
import json


def update_activity_data():
    """Mettre à jour les données d'activité"""
    try:
        print(f"🔄 {datetime.now().strftime('%H:%M:%S')} - Mise à jour activité...")
        result = subprocess.run([sys.executable, 'activity_scanner_realtime.py'], 
                               capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ {datetime.now().strftime('%H:%M:%S')} - Données mises à jour")
            return True
        else:
            print(f"❌ {datetime.now().strftime('%H:%M:%S')} - Erreur: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {datetime.now().strftime('%H:%M:%S')} - Exception: {e}")
        return False


def main():
    """Boucle principale de mise à jour"""
    print("🚀 Démarrage auto-updater dashboard activité")
    print("📊 Mise à jour toutes les 10 secondes")
    print("🛑 Ctrl+C pour arrêter\n")
    
    try:
        while True:
            update_activity_data()
            time.sleep(10)  # Mise à jour toutes les 10 secondes
            
    except KeyboardInterrupt:
        print(f"\n🛑 {datetime.now().strftime('%H:%M:%S')} - Arrêt demandé")
        print("📊 Auto-updater arrêté")


if __name__ == "__main__":
    main()