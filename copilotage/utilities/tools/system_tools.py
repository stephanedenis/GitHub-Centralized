#!/usr/bin/env python3
"""
System Tools - Opérations Système Réutilisables
===============================================

Remplace toutes les commandes ad-hoc system que j'ai créées:
- echo "..." → system.print_section()
- ps aux | grep → system.find_processes() 
- pkill -f → system.kill_processes()
- lsof -i → system.check_ports()
- find . -name → system.find_files()
- ls -la → system.list_files()
- du -sh → system.get_disk_usage()
"""

import os
import subprocess
import psutil
import time
from pathlib import Path
from typing import List, Dict, Optional, Any


class SystemTools:
    """Outils système réutilisables"""
    
    def __init__(self):
        self.workspace_root = Path("/home/stephane/GitHub/PaniniFS-Research")
        
    def print_section(self, title: str, subtitle: str = "", emoji: str = "📊"):
        """Remplace echo avec formatage standardisé"""
        print(f"\n{emoji} {title.upper()}")
        if subtitle:
            print(f"{subtitle}")
        print("=" * len(title))
        
    def print_subsection(self, title: str, emoji: str = "🔍"):
        """Sous-section standardisée"""
        print(f"\n{emoji} {title}")
        print("-" * len(title))
        
    def find_processes(self, pattern: str) -> List[Dict[str, Any]]:
        """Remplace ps aux | grep pattern"""
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'cpu_percent', 'memory_percent']):
            try:
                cmdline = ' '.join(proc.info['cmdline'] or [])
                if pattern.lower() in cmdline.lower() or pattern.lower() in proc.info['name'].lower():
                    processes.append({
                        'pid': proc.info['pid'],
                        'name': proc.info['name'],
                        'cmdline': cmdline,
                        'cpu': proc.info['cpu_percent'],
                        'memory': proc.info['memory_percent']
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return processes
        
    def kill_processes(self, pattern: str, force: bool = False) -> int:
        """Remplace pkill -f pattern"""
        killed = 0
        processes = self.find_processes(pattern)
        
        for proc_info in processes:
            try:
                proc = psutil.Process(proc_info['pid'])
                if force:
                    proc.kill()
                else:
                    proc.terminate()
                killed += 1
                print(f"✅ Processus terminé: {proc_info['name']} (PID: {proc_info['pid']})")
            except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                print(f"❌ Impossible de terminer PID {proc_info['pid']}: {e}")
                
        return killed
        
    def check_ports(self, ports: List[int] = None) -> Dict[int, Dict[str, Any]]:
        """Remplace lsof -i :PORT"""
        if ports is None:
            ports = [8081, 8082, 8083, 8084, 8085, 8097]
            
        port_status = {}
        
        for port in ports:
            port_status[port] = {
                'status': 'free',
                'process': None,
                'pid': None
            }
            
        # Vérifier connexions réseau
        for conn in psutil.net_connections():
            if conn.laddr and conn.laddr.port in ports:
                try:
                    proc = psutil.Process(conn.pid) if conn.pid else None
                    port_status[conn.laddr.port] = {
                        'status': 'occupied',
                        'process': proc.name() if proc else 'unknown',
                        'pid': conn.pid,
                        'state': conn.status
                    }
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    port_status[conn.laddr.port]['status'] = 'occupied'
                    
        return port_status
        
    def find_files(self, pattern: str, directory: str = None, max_results: int = 100) -> List[Path]:
        """Remplace find . -name pattern"""
        if directory is None:
            directory = self.workspace_root
        
        directory = Path(directory)
        files = []
        
        try:
            for file_path in directory.rglob(pattern):
                if len(files) >= max_results:
                    break
                if file_path.is_file():
                    files.append(file_path)
        except PermissionError:
            pass
            
        return files
        
    def list_files(self, directory: str = None, show_hidden: bool = False) -> List[Dict[str, Any]]:
        """Remplace ls -la avec formatage structuré"""
        if directory is None:
            directory = self.workspace_root
            
        directory = Path(directory)
        files_info = []
        
        try:
            for item in directory.iterdir():
                if not show_hidden and item.name.startswith('.'):
                    continue
                    
                stat_info = item.stat()
                files_info.append({
                    'name': item.name,
                    'type': 'directory' if item.is_dir() else 'file',
                    'size': stat_info.st_size,
                    'modified': time.ctime(stat_info.st_mtime),
                    'permissions': oct(stat_info.st_mode)[-3:],
                    'path': str(item)
                })
        except PermissionError:
            pass
            
        return files_info
        
    def get_disk_usage(self, path: str = None) -> Dict[str, int]:
        """Remplace du -sh avec résultats structurés"""
        if path is None:
            path = self.workspace_root
            
        usage = psutil.disk_usage(path)
        return {
            'total': usage.total,
            'used': usage.used,
            'free': usage.free,
            'percent': (usage.used / usage.total) * 100
        }
        
    def get_system_resources(self) -> Dict[str, Any]:
        """Info système complète réutilisable"""
        return {
            'cpu': {
                'percent': psutil.cpu_percent(interval=1),
                'count': psutil.cpu_count(),
                'freq': psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None
            },
            'memory': {
                'total': psutil.virtual_memory().total,
                'available': psutil.virtual_memory().available,
                'percent': psutil.virtual_memory().percent,
                'used': psutil.virtual_memory().used
            },
            'disk': self.get_disk_usage(),
            'uptime': time.time() - psutil.boot_time()
        }
        
    def run_command_safe(self, command: str, timeout: int = 30) -> Dict[str, Any]:
        """Exécution commande sécurisée avec gestion erreurs"""
        try:
            result = subprocess.run(
                command.split(), 
                capture_output=True, 
                text=True, 
                timeout=timeout,
                cwd=self.workspace_root
            )
            return {
                'success': result.returncode == 0,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode
            }
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': f'Command timeout after {timeout}s',
                'returncode': -1
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'returncode': -1
            }


def main():
    """Test du module system_tools"""
    tools = SystemTools()
    
    tools.print_section("TEST SYSTEM TOOLS", "Module de remplacement commandes ad-hoc", "🧪")
    
    # Test processes
    tools.print_subsection("Processus Python actifs")
    processes = tools.find_processes("python")
    for proc in processes[:5]:
        print(f"  PID {proc['pid']}: {proc['name']} - CPU: {proc['cpu']}%")
    
    # Test ports
    tools.print_subsection("État des ports dashboard")
    ports = tools.check_ports()
    for port, info in ports.items():
        status_icon = "🔴" if info['status'] == 'occupied' else "🟢"
        print(f"  {status_icon} Port {port}: {info['status']}")
        if info['process']:
            print(f"     Processus: {info['process']} (PID: {info['pid']})")
    
    # Test ressources système
    tools.print_subsection("Ressources système")
    resources = tools.get_system_resources()
    print(f"  🖥️  CPU: {resources['cpu']['percent']:.1f}% ({resources['cpu']['count']} cores)")
    print(f"  💾 RAM: {resources['memory']['percent']:.1f}% ({resources['memory']['used']//1024//1024//1024}GB/{resources['memory']['total']//1024//1024//1024}GB)")
    print(f"  💿 Disk: {resources['disk']['percent']:.1f}%")
    
    return 0


if __name__ == "__main__":
    main()