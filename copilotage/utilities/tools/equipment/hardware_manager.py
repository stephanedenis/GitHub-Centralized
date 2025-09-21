"""
Equipment Management Tools - Hardware Detection
==============================================

Outils centralisés pour détection et gestion du matériel
Remplace les commandes bash ad-hoc par des fonctions Python réutilisables
"""

import os
import subprocess
import platform
import psutil
import json
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

class HardwareManager:
    """Gestionnaire centralisé pour détection et monitoring matériel"""
    
    def __init__(self):
        self.hostname = platform.node()
        self.architecture = platform.machine()
        
    def get_cpu_info(self) -> Dict[str, Any]:
        """Détection complète du CPU"""
        try:
            # Informations via psutil
            cpu_count_logical = psutil.cpu_count(logical=True)
            cpu_count_physical = psutil.cpu_count(logical=False)
            cpu_freq = psutil.cpu_freq()
            
            # Informations via /proc/cpuinfo
            cpu_model = "Unknown"
            cpu_cache = "Unknown"
            
            try:
                with open('/proc/cpuinfo', 'r') as f:
                    for line in f:
                        if 'model name' in line:
                            cpu_model = line.split(':')[1].strip()
                            break
                        
                # Cache L3 via lscpu si disponible
                result = subprocess.run(['lscpu'], capture_output=True, text=True)
                if result.returncode == 0:
                    for line in result.stdout.split('\n'):
                        if 'L3 cache' in line:
                            cpu_cache = line.split(':')[1].strip()
                            break
            except Exception:
                pass
                
            return {
                'model': cpu_model,
                'architecture': self.architecture,
                'cores_logical': cpu_count_logical,
                'cores_physical': cpu_count_physical,
                'frequency_current': cpu_freq.current if cpu_freq else None,
                'frequency_max': cpu_freq.max if cpu_freq else None,
                'cache_l3': cpu_cache
            }
        except Exception as e:
            return {'error': str(e)}
    
    def get_memory_info(self) -> Dict[str, Any]:
        """Détection complète de la mémoire"""
        try:
            memory = psutil.virtual_memory()
            swap = psutil.swap_memory()
            
            return {
                'total_bytes': memory.total,
                'total_human': self._bytes_to_human(memory.total),
                'available_bytes': memory.available,
                'available_human': self._bytes_to_human(memory.available),
                'used_bytes': memory.used,
                'used_human': self._bytes_to_human(memory.used),
                'percent_used': memory.percent,
                'swap_total': swap.total,
                'swap_used': swap.used,
                'swap_percent': swap.percent
            }
        except Exception as e:
            return {'error': str(e)}
    
    def get_gpu_info(self) -> Dict[str, Any]:
        """Détection GPU via lspci"""
        try:
            result = subprocess.run(['lspci'], capture_output=True, text=True)
            if result.returncode != 0:
                return {'error': 'lspci not available'}
            
            gpu_lines = [line for line in result.stdout.split('\n') 
                        if 'VGA' in line or 'Display' in line or '3D' in line]
            
            gpus = []
            for line in gpu_lines:
                if ':' in line:
                    gpu_info = line.split(':', 2)[-1].strip()
                    gpus.append(gpu_info)
            
            # Détection driver
            driver = "unknown"
            try:
                lsmod_result = subprocess.run(['lsmod'], capture_output=True, text=True)
                if 'nvidia' in lsmod_result.stdout:
                    driver = "nvidia"
                elif 'amdgpu' in lsmod_result.stdout:
                    driver = "amdgpu"
                elif 'radeon' in lsmod_result.stdout:
                    driver = "radeon"
                elif 'i915' in lsmod_result.stdout:
                    driver = "intel"
            except Exception:
                pass
            
            return {
                'primary': gpus[0] if gpus else "No GPU detected",
                'all_gpus': gpus,
                'driver': driver
            }
        except Exception as e:
            return {'error': str(e)}
    
    def get_storage_info(self) -> Dict[str, Any]:
        """Détection des périphériques de stockage"""
        try:
            # Disques via psutil
            disk_partitions = psutil.disk_partitions()
            
            devices = []
            for partition in disk_partitions:
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    devices.append({
                        'device': partition.device,
                        'mountpoint': partition.mountpoint,
                        'fstype': partition.fstype,
                        'total_bytes': usage.total,
                        'total_human': self._bytes_to_human(usage.total),
                        'used_bytes': usage.used,
                        'used_human': self._bytes_to_human(usage.used),
                        'free_bytes': usage.free,
                        'free_human': self._bytes_to_human(usage.free),
                        'percent_used': round((usage.used / usage.total) * 100, 1)
                    })
                except Exception:
                    continue
            
            # Informations additionnelles via lsblk
            try:
                result = subprocess.run(['lsblk', '-d', '-o', 'NAME,SIZE,TYPE'], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    lsblk_info = []
                    for line in result.stdout.split('\n')[1:]:  # Skip header
                        if line.strip():
                            parts = line.split()
                            if len(parts) >= 3 and parts[2] == 'disk':
                                lsblk_info.append(f"{parts[0]}: {parts[1]}")
                else:
                    lsblk_info = []
            except Exception:
                lsblk_info = []
            
            return {
                'partitions': devices,
                'raw_devices': lsblk_info
            }
        except Exception as e:
            return {'error': str(e)}
    
    def get_network_info(self) -> Dict[str, Any]:
        """Détection des interfaces réseau"""
        try:
            interfaces = psutil.net_if_addrs()
            stats = psutil.net_if_stats()
            
            network_info = []
            for interface, addresses in interfaces.items():
                if interface == 'lo':  # Skip loopback
                    continue
                    
                interface_info = {
                    'name': interface,
                    'addresses': [],
                    'is_up': stats[interface].isup if interface in stats else False,
                    'speed': stats[interface].speed if interface in stats else None
                }
                
                for addr in addresses:
                    if addr.family == 2:  # IPv4
                        interface_info['addresses'].append({
                            'type': 'IPv4',
                            'address': addr.address,
                            'netmask': addr.netmask
                        })
                    elif addr.family == 10:  # IPv6
                        interface_info['addresses'].append({
                            'type': 'IPv6', 
                            'address': addr.address
                        })
                
                network_info.append(interface_info)
            
            return {
                'interfaces': network_info,
                'active_interfaces': [iface for iface in network_info if iface['is_up']]
            }
        except Exception as e:
            return {'error': str(e)}
    
    def get_usb_info(self) -> Dict[str, Any]:
        """Détection des périphériques USB"""
        try:
            result = subprocess.run(['lsusb'], capture_output=True, text=True)
            if result.returncode != 0:
                return {'error': 'lsusb not available'}
            
            devices = []
            for line in result.stdout.split('\n'):
                if line.strip() and 'Bus' in line:
                    devices.append(line.strip())
            
            return {
                'count': len(devices),
                'devices': devices
            }
        except Exception as e:
            return {'error': str(e)}
    
    def get_thermal_info(self) -> Dict[str, Any]:
        """Détection des capteurs de température"""
        try:
            if not psutil.sensors_temperatures():
                # Fallback to sensors command
                result = subprocess.run(['sensors'], capture_output=True, text=True)
                if result.returncode != 0:
                    return {'sensors': [], 'count': 0}
                
                sensors = []
                for line in result.stdout.split('\n'):
                    if '°C' in line:
                        sensors.append(line.strip())
                
                return {
                    'count': len(sensors),
                    'sensors': sensors,
                    'method': 'sensors_command'
                }
            else:
                temps = psutil.sensors_temperatures()
                sensors = []
                for name, entries in temps.items():
                    for entry in entries:
                        sensors.append({
                            'sensor': f"{name}_{entry.label or 'temp'}",
                            'current': entry.current,
                            'high': entry.high,
                            'critical': entry.critical
                        })
                
                return {
                    'count': len(sensors),
                    'sensors': sensors,
                    'method': 'psutil'
                }
        except Exception as e:
            return {'error': str(e)}
    
    def get_complete_hardware_inventory(self) -> Dict[str, Any]:
        """Inventaire complet du matériel"""
        return {
            'system': {
                'hostname': self.hostname,
                'architecture': self.architecture,
                'scan_time': datetime.now().isoformat()
            },
            'cpu': self.get_cpu_info(),
            'memory': self.get_memory_info(),
            'gpu': self.get_gpu_info(),
            'storage': self.get_storage_info(),
            'network': self.get_network_info(),
            'usb': self.get_usb_info(),
            'thermal': self.get_thermal_info()
        }
    
    def save_inventory_yaml(self, filepath: str) -> bool:
        """Sauvegarde l'inventaire en YAML"""
        try:
            inventory = self.get_complete_hardware_inventory()
            with open(filepath, 'w') as f:
                yaml.dump(inventory, f, default_flow_style=False, indent=2)
            return True
        except Exception as e:
            print(f"Error saving inventory: {e}")
            return False
    
    def _bytes_to_human(self, bytes_value: int) -> str:
        """Conversion bytes vers format lisible"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_value < 1024.0:
                return f"{bytes_value:.1f}{unit}"
            bytes_value /= 1024.0
        return f"{bytes_value:.1f}PB"