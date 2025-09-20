#!/usr/bin/env python3
"""
Web Tools - HTTP et API Réutilisables
=====================================

Remplace toutes les commandes curl et serveurs HTTP ad-hoc:
- curl http://localhost:8081/api/metrics → web.get_api()
- curl -I → web.check_endpoint()
- Serveurs HTTP temporaires → web.start_server()
"""

import requests
import json
import socket
import time
from typing import Dict, Any, Optional, List
from pathlib import Path
import threading
import http.server
import socketserver


class WebTools:
    """Outils web et API réutilisables"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.timeout = 30
        self.running_servers = []
        
    def check_endpoint(self, url: str, method: str = 'HEAD') -> Dict[str, Any]:
        """Remplace curl -I (vérification endpoint)"""
        try:
            if method.upper() == 'HEAD':
                response = self.session.head(url)
            else:
                response = self.session.get(url)
                
            return {
                'success': True,
                'status_code': response.status_code,
                'headers': dict(response.headers),
                'accessible': response.status_code < 400,
                'response_time': response.elapsed.total_seconds()
            }
            
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': str(e),
                'accessible': False
            }
            
    def get_api(self, url: str, params: Dict = None) -> Dict[str, Any]:
        """Remplace curl API calls avec parsing JSON"""
        try:
            response = self.session.get(url, params=params)
            
            result = {
                'success': response.status_code < 400,
                'status_code': response.status_code,
                'headers': dict(response.headers),
                'response_time': response.elapsed.total_seconds()
            }
            
            # Tentative parsing JSON
            try:
                result['data'] = response.json()
                result['content_type'] = 'json'
            except ValueError:
                result['data'] = response.text
                result['content_type'] = 'text'
                
            return result
            
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': str(e)
            }
            
    def post_api(self, url: str, data: Dict = None, 
                 json_data: Dict = None) -> Dict[str, Any]:
        """POST API avec gestion JSON"""
        try:
            if json_data:
                response = self.session.post(url, json=json_data)
            else:
                response = self.session.post(url, data=data)
                
            result = {
                'success': response.status_code < 400,
                'status_code': response.status_code,
                'response_time': response.elapsed.total_seconds()
            }
            
            try:
                result['data'] = response.json()
            except ValueError:
                result['data'] = response.text
                
            return result
            
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': str(e)
            }
            
    def check_port_available(self, port: int, host: str = 'localhost') -> bool:
        """Vérifier si port disponible"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                result = s.connect_ex((host, port))
                return result != 0  # Port libre si connexion échoue
        except Exception:
            return False
            
    def find_free_port(self, start_port: int = 8080, 
                       end_port: int = 8090) -> Optional[int]:
        """Trouver port libre dans range"""
        for port in range(start_port, end_port + 1):
            if self.check_port_available(port):
                return port
        return None
        
    def start_simple_server(self, directory: str, port: int = None) -> Dict[str, Any]:
        """Serveur HTTP simple pour fichiers statiques"""
        if port is None:
            port = self.find_free_port()
            
        if port is None:
            return {'success': False, 'error': 'No free port found'}
            
        directory = Path(directory)
        if not directory.exists():
            return {'success': False, 'error': f'Directory not found: {directory}'}
            
        def run_server():
            class Handler(http.server.SimpleHTTPRequestHandler):
                def __init__(self, *args, **kwargs):
                    super().__init__(*args, directory=str(directory), **kwargs)
                    
            with socketserver.TCPServer(("", port), Handler) as httpd:
                self.running_servers.append({'port': port, 'httpd': httpd})
                httpd.serve_forever()
                
        thread = threading.Thread(target=run_server, daemon=True)
        thread.start()
        
        # Attendre que serveur démarre
        time.sleep(1)
        
        return {
            'success': True,
            'port': port,
            'url': f'http://localhost:{port}',
            'directory': str(directory)
        }
        
    def stop_all_servers(self):
        """Arrêter tous les serveurs démarrés"""
        for server_info in self.running_servers:
            try:
                server_info['httpd'].shutdown()
            except Exception:
                pass
        self.running_servers.clear()
        
    # ======== APIS SPÉCIFIQUES PROJET ========
    
    def check_dashboard_apis(self, ports: List[int] = None) -> Dict[int, Dict[str, Any]]:
        """Vérifier APIs dashboard projet"""
        if ports is None:
            ports = [8081, 8082, 8083, 8084, 8085]
            
        results = {}
        
        for port in ports:
            base_url = f"http://localhost:{port}"
            
            # Endpoints communs à tester
            endpoints = {
                'root': base_url,
                'metrics': f"{base_url}/api/metrics",
                'status': f"{base_url}/api/status",
                'health': f"{base_url}/health"
            }
            
            port_results = {'port': port, 'endpoints': {}}
            
            for name, url in endpoints.items():
                check = self.check_endpoint(url, method='GET')
                port_results['endpoints'][name] = {
                    'accessible': check.get('accessible', False),
                    'status_code': check.get('status_code'),
                    'error': check.get('error')
                }
                
            # Marquer port comme actif si au moins un endpoint répond
            port_results['active'] = any(
                ep['accessible'] for ep in port_results['endpoints'].values()
            )
            
            results[port] = port_results
            
        return results
        
    def get_dhatu_metrics(self, port: int = 8081) -> Dict[str, Any]:
        """Récupérer métriques dhātu spécifiques"""
        endpoints = [
            f"http://localhost:{port}/api/metrics",
            f"http://localhost:{port}/api/dhatu",
            f"http://localhost:{port}/api/performance"
        ]
        
        metrics = {}
        
        for url in endpoints:
            result = self.get_api(url)
            if result['success'] and result.get('content_type') == 'json':
                # Extraire métriques utiles
                data = result['data']
                if 'cpu' in data:
                    metrics['cpu'] = data['cpu']
                if 'dhatu_pipeline' in data:
                    metrics['dhatu_pipeline'] = data['dhatu_pipeline']
                if 'performance' in data:
                    metrics['performance'] = data['performance']
                    
        return metrics
        
    def batch_health_check(self, urls: List[str]) -> Dict[str, Dict[str, Any]]:
        """Vérification santé multiple URLs"""
        results = {}
        
        for url in urls:
            results[url] = self.check_endpoint(url)
            
        return results


def main():
    """Test du module web_tools"""
    tools = WebTools()
    
    print("🧪 TEST WEB TOOLS")
    print("=" * 30)
    
    # Test ports dashboard
    print("\n🌐 CHECK DASHBOARD APIS")
    dashboard_status = tools.check_dashboard_apis()
    
    active_ports = []
    for port, info in dashboard_status.items():
        status_icon = "🟢" if info['active'] else "🔴"
        print(f"  {status_icon} Port {port}: {'ACTIVE' if info['active'] else 'INACTIVE'}")
        
        if info['active']:
            active_ports.append(port)
            # Montrer endpoints actifs
            for endpoint, data in info['endpoints'].items():
                if data['accessible']:
                    print(f"     ✅ {endpoint}: HTTP {data['status_code']}")
    
    # Test métriques si dashboard actif
    if active_ports:
        print(f"\n📊 MÉTRIQUES DHĀTU (Port {active_ports[0]})")
        metrics = tools.get_dhatu_metrics(active_ports[0])
        
        if 'cpu' in metrics:
            print(f"  CPU Usage: {metrics['cpu'].get('overall_usage', 'N/A')}")
        if 'dhatu_pipeline' in metrics:
            pipeline = metrics['dhatu_pipeline']
            print(f"  Atoms processed: {pipeline.get('atoms_processed', 'N/A')}")
    
    # Test port disponible
    print(f"\n🔍 RECHERCHE PORT LIBRE")
    free_port = tools.find_free_port(8090, 8099)
    if free_port:
        print(f"  ✅ Port libre trouvé: {free_port}")
    else:
        print(f"  ❌ Aucun port libre dans range 8090-8099")
    
    return 0


if __name__ == "__main__":
    main()