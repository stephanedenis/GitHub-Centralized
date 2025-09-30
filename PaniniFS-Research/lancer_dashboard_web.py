#!/usr/bin/env python3
"""
PANINI DASHBOARD WEB - SERVEUR DE DÉVELOPPEMENT
============================================
Serveur HTTP simple pour lancer le dashboard web sémantique
"""

import http.server
import socketserver
import webbrowser
import os
import sys
from pathlib import Path


class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Headers CORS pour développement
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def log_message(self, format, *args):
        # Log personnalisé
        print(f"🌐 {self.address_string()} - {format % args}")


def main():
    # Configuration
    PORT = 8889  # Port différent pour éviter conflit
    DASHBOARD_FILE = "dashboard_real_panini.html"
    
    print("🧠 PANINI DASHBOARD WEB - SERVEUR DE DÉVELOPPEMENT")
    print("=" * 55)
    
    # Vérifier que le fichier dashboard existe
    if not os.path.exists(DASHBOARD_FILE):
        print(f"❌ Erreur: {DASHBOARD_FILE} non trouvé!")
        print(f"📁 Répertoire actuel: {os.getcwd()}")
        print("📋 Fichiers disponibles:")
        for file in os.listdir('.'):
            if file.endswith('.html'):
                print(f"   - {file}")
        sys.exit(1)
    
    # Changer vers le répertoire du script
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print(f"📂 Répertoire de travail: {os.getcwd()}")
    print(f"📄 Dashboard: {DASHBOARD_FILE}")
    print(f"🌐 Port: {PORT}")
    print()
    
    try:
        # Démarrer le serveur
        with socketserver.TCPServer(("", PORT), 
                                  CustomHTTPRequestHandler) as httpd:
            print(f"🚀 Serveur démarré sur http://localhost:{PORT}")
            dashboard_url = f"http://localhost:{PORT}/{DASHBOARD_FILE}"
            print(f"🔗 Dashboard accessible: {dashboard_url}")
            print()
            print("📊 FONCTIONNALITÉS DU DASHBOARD:")
            print("   🔬 Hypothèses sémantiques en temps réel")
            print("   ⚡ Découvertes Panini live")
            print("   🌟 Métriques universaux animées")
            print("   🕸️  Réseau conceptuel interactif")
            print("   📖 Analyse de contenu sémantique")
            print()
            print("⏹️  Ctrl+C pour arrêter le serveur")
            print("=" * 55)
            
            # Ouvrir automatiquement le navigateur
            try:
                url = dashboard_url
                print(f"🌐 Ouverture automatique: {url}")
                webbrowser.open(url)
            except Exception as e:
                error_msg = f"⚠️  Impossible d'ouvrir le navigateur: {e}"
                print(error_msg)
                manual_msg = f"🔗 Ouvrez manuellement: {dashboard_url}"
                print(manual_msg)
            
            print()
            print("🔄 Serveur en attente de connexions...")
            print()
            
            # Servir les requêtes
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n🛑 Arrêt du serveur demandé")
    except OSError as e:
        if e.errno == 98:  # Port déjà utilisé
            print(f"❌ Erreur: Port {PORT} déjà utilisé!")
            print("💡 Solutions:")
            print("   - Changer le port dans le script")
            print(f"   - Arrêter le processus utilisant le port {PORT}")
            print(f"   - Utiliser: sudo lsof -i :{PORT}")
        else:
            print(f"❌ Erreur réseau: {e}")
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
    
    print("\n✅ Serveur arrêté proprement")
    print("🧠 Dashboard Panini fermé")


if __name__ == "__main__":
    main()