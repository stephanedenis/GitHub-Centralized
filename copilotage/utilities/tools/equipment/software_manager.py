"""
Equipment Management Tools - Software Detection
==============================================

Outils centralisés pour détection et gestion des logiciels
Remplace les commandes bash ad-hoc par des fonctions Python réutilisables
"""

import os
import subprocess
import platform
import shutil
import json
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

class SoftwareManager:
    """Gestionnaire centralisé pour détection et monitoring logiciels"""
    
    def __init__(self):
        self.hostname = platform.node()
        self.home_path = Path.home()
        
    def get_os_info(self) -> Dict[str, Any]:
        """Informations système d'exploitation"""
        try:
            # Informations de base
            os_info = {
                'system': platform.system(),
                'architecture': platform.machine(),
                'kernel': platform.release(),
                'python_version': platform.python_version()
            }
            
            # Distribution Linux
            try:
                with open('/etc/os-release', 'r') as f:
                    os_release = {}
                    for line in f:
                        if '=' in line:
                            key, value = line.strip().split('=', 1)
                            os_release[key] = value.strip('"')
                    os_info['distribution'] = os_release.get('PRETTY_NAME', 'Unknown')
                    os_info['version_id'] = os_release.get('VERSION_ID', 'Unknown')
            except Exception:
                os_info['distribution'] = 'Unknown'
                os_info['version_id'] = 'Unknown'
            
            # Desktop environment
            desktop_env = (os.environ.get('XDG_CURRENT_DESKTOP') or 
                          os.environ.get('DESKTOP_SESSION') or 
                          'Unknown')
            os_info['desktop_environment'] = desktop_env
            
            return os_info
        except Exception as e:
            return {'error': str(e)}
    
    def get_development_tools(self) -> Dict[str, Any]:
        """Détection des outils de développement"""
        tools = {}
        
        # Git
        tools['git'] = self._get_version_info('git', '--version')
        
        # GitHub CLI
        tools['github_cli'] = self._get_version_info('gh', '--version')
        
        # Python
        tools['python'] = {
            'version': platform.python_version(),
            'executable': shutil.which('python3') or shutil.which('python'),
            'pip_version': self._get_pip_version()
        }
        
        # Node.js et npm
        tools['node'] = self._get_version_info('node', '--version')
        tools['npm'] = self._get_version_info('npm', '--version')
        
        # Docker
        tools['docker'] = self._get_version_info('docker', '--version')
        
        # Autres outils communs
        tools['code'] = self._get_version_info('code', '--version')
        tools['make'] = self._get_version_info('make', '--version')
        tools['gcc'] = self._get_version_info('gcc', '--version')
        
        return tools
    
    def get_system_packages(self) -> Dict[str, Any]:
        """Détection des packages système"""
        packages = {}
        
        # Détection du gestionnaire de packages
        if shutil.which('zypper'):
            packages['manager'] = 'zypper'
            packages['count'] = self._count_zypper_packages()
        elif shutil.which('apt'):
            packages['manager'] = 'apt'
            packages['count'] = self._count_apt_packages()
        elif shutil.which('yum'):
            packages['manager'] = 'yum'
            packages['count'] = self._count_yum_packages()
        elif shutil.which('pacman'):
            packages['manager'] = 'pacman'
            packages['count'] = self._count_pacman_packages()
        else:
            packages['manager'] = 'unknown'
            packages['count'] = 0
        
        return packages
    
    def get_user_applications(self) -> Dict[str, Any]:
        """Détection des applications utilisateur"""
        apps = {}
        
        # Navigateurs
        apps['firefox'] = self._get_version_info('firefox', '--version')
        apps['chrome'] = self._get_version_info('google-chrome', '--version')
        apps['chromium'] = self._get_version_info('chromium', '--version')
        
        # Éditeurs
        apps['vim'] = self._get_version_info('vim', '--version')
        apps['nano'] = self._get_version_info('nano', '--version')
        apps['emacs'] = self._get_version_info('emacs', '--version')
        
        # Outils système
        apps['htop'] = self._get_version_info('htop', '--version')
        apps['tree'] = self._get_version_info('tree', '--version')
        apps['curl'] = self._get_version_info('curl', '--version')
        apps['wget'] = self._get_version_info('wget', '--version')
        
        return apps
    
    def get_services_info(self) -> Dict[str, Any]:
        """Information sur les services système"""
        try:
            # Services actifs
            result = subprocess.run(['systemctl', 'list-units', '--type=service', '--state=active', '--no-legend'], 
                                  capture_output=True, text=True)
            active_count = len([line for line in result.stdout.split('\n') if line.strip()])
            
            # Services échoués
            result = subprocess.run(['systemctl', '--failed', '--no-legend'], 
                                  capture_output=True, text=True)
            failed_services = [line.split()[0] for line in result.stdout.split('\n') if line.strip()]
            
            return {
                'active_count': active_count,
                'failed_count': len(failed_services),
                'failed_services': failed_services
            }
        except Exception as e:
            return {'error': str(e)}
    
    def get_github_repositories(self) -> Dict[str, Any]:
        """Détection des dépôts GitHub dans ~/GitHub"""
        try:
            github_dir = self.home_path / 'GitHub'
            if not github_dir.exists():
                return {'count': 0, 'repositories': []}
            
            repos = []
            for item in github_dir.iterdir():
                if item.is_dir() and not item.name.startswith('.'):
                    git_dir = item / '.git'
                    if git_dir.exists():
                        repos.append({
                            'name': item.name,
                            'path': str(item),
                            'is_git': True
                        })
                    else:
                        repos.append({
                            'name': item.name,
                            'path': str(item),
                            'is_git': False
                        })
            
            return {
                'count': len(repos),
                'git_repos': len([r for r in repos if r['is_git']]),
                'repositories': repos
            }
        except Exception as e:
            return {'error': str(e)}
    
    def get_python_environments(self) -> Dict[str, Any]:
        """Détection des environnements Python"""
        try:
            envs = {}
            
            # Conda environments
            try:
                result = subprocess.run(['conda', 'env', 'list'], capture_output=True, text=True)
                if result.returncode == 0:
                    conda_envs = []
                    for line in result.stdout.split('\n'):
                        if line.strip() and not line.startswith('#'):
                            env_name = line.split()[0]
                            if env_name != 'base':
                                conda_envs.append(env_name)
                    envs['conda'] = conda_envs
            except Exception:
                envs['conda'] = []
            
            # Virtual environments
            venv_dirs = [
                self.home_path / '.virtualenvs',
                self.home_path / 'venv',
                self.home_path / 'virtualenvs'
            ]
            
            venvs = []
            for venv_dir in venv_dirs:
                if venv_dir.exists():
                    for item in venv_dir.iterdir():
                        if item.is_dir():
                            venvs.append(item.name)
            
            envs['virtualenv'] = venvs
            
            return envs
        except Exception as e:
            return {'error': str(e)}
    
    def get_complete_software_inventory(self) -> Dict[str, Any]:
        """Inventaire complet des logiciels"""
        return {
            'system': {
                'hostname': self.hostname,
                'scan_time': datetime.now().isoformat()
            },
            'os': self.get_os_info(),
            'development': self.get_development_tools(),
            'packages': self.get_system_packages(),
            'applications': self.get_user_applications(),
            'services': self.get_services_info(),
            'repositories': self.get_github_repositories(),
            'python_environments': self.get_python_environments()
        }
    
    def save_inventory_yaml(self, filepath: str) -> bool:
        """Sauvegarde l'inventaire en YAML"""
        try:
            inventory = self.get_complete_software_inventory()
            with open(filepath, 'w') as f:
                yaml.dump(inventory, f, default_flow_style=False, indent=2)
            return True
        except Exception as e:
            print(f"Error saving software inventory: {e}")
            return False
    
    def _get_version_info(self, command: str, version_flag: str = '--version') -> Dict[str, Any]:
        """Obtient les informations de version d'une commande"""
        try:
            if not shutil.which(command):
                return {'installed': False, 'version': None}
            
            result = subprocess.run([command, version_flag], capture_output=True, text=True)
            if result.returncode == 0:
                version_output = result.stdout.strip().split('\n')[0]
                return {
                    'installed': True,
                    'version': version_output,
                    'executable': shutil.which(command)
                }
            else:
                return {'installed': True, 'version': 'Unknown', 'executable': shutil.which(command)}
        except Exception:
            return {'installed': False, 'version': None}
    
    def _get_pip_version(self) -> Optional[str]:
        """Version de pip"""
        try:
            result = subprocess.run(['pip', '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip()
            return None
        except Exception:
            return None
    
    def _count_zypper_packages(self) -> int:
        """Compte les packages zypper installés"""
        try:
            result = subprocess.run(['zypper', 'search', '--installed-only'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                return len([line for line in result.stdout.split('\n') if line.startswith('i ')])
            return 0
        except Exception:
            return 0
    
    def _count_apt_packages(self) -> int:
        """Compte les packages apt installés"""
        try:
            result = subprocess.run(['dpkg', '--get-selections'], capture_output=True, text=True)
            if result.returncode == 0:
                return len([line for line in result.stdout.split('\n') 
                           if line.strip() and 'install' in line])
            return 0
        except Exception:
            return 0
    
    def _count_yum_packages(self) -> int:
        """Compte les packages yum installés"""
        try:
            result = subprocess.run(['yum', 'list', 'installed'], capture_output=True, text=True)
            if result.returncode == 0:
                return len(result.stdout.split('\n')) - 1  # Minus header
            return 0
        except Exception:
            return 0
    
    def _count_pacman_packages(self) -> int:
        """Compte les packages pacman installés"""
        try:
            result = subprocess.run(['pacman', '-Q'], capture_output=True, text=True)
            if result.returncode == 0:
                return len(result.stdout.split('\n')) - 1
            return 0
        except Exception:
            return 0