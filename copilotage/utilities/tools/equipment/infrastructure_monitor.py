"""
Equipment Management Tools - Infrastructure Monitoring
====================================================

Outils centralisés pour monitoring et surveillance d'infrastructure
Remplace les scripts bash ad-hoc par des fonctions Python réutilisables
"""

import os
import subprocess
import psutil
import time
import json
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from dataclasses import dataclass

@dataclass
class HealthThresholds:
    """Seuils pour monitoring santé système"""
    cpu_warning: float = 70.0
    cpu_critical: float = 85.0
    memory_warning: float = 80.0
    memory_critical: float = 90.0
    disk_warning: float = 80.0
    disk_critical: float = 90.0
    temp_warning: float = 65.0
    temp_critical: float = 75.0

class InfrastructureMonitor:
    """Monitoring centralisé pour infrastructure équipement"""
    
    def __init__(self, thresholds: Optional[HealthThresholds] = None):
        self.thresholds = thresholds or HealthThresholds()
        self.hostname = os.uname().nodename
        
    def check_cpu_health(self) -> Dict[str, Any]:
        """Vérification santé CPU"""
        try:
            # CPU usage over 5 seconds for more accurate reading
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            load_avg = os.getloadavg()
            
            # Determine status
            if cpu_percent >= self.thresholds.cpu_critical:
                status = "CRITICAL"
                color = "🔴"
            elif cpu_percent >= self.thresholds.cpu_warning:
                status = "WARNING"
                color = "🟡"
            else:
                status = "OK"
                color = "🟢"
            
            # Top processes
            top_processes = []
            for proc in sorted(psutil.process_iter(['pid', 'name', 'cpu_percent']), 
                             key=lambda x: x.info['cpu_percent'] or 0, reverse=True)[:5]:
                try:
                    top_processes.append({
                        'pid': proc.info['pid'],
                        'name': proc.info['name'],
                        'cpu_percent': proc.info['cpu_percent'] or 0
                    })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            return {
                'status': status,
                'color': color,
                'cpu_percent': cpu_percent,
                'cpu_count': cpu_count,
                'load_avg_1m': load_avg[0],
                'load_avg_5m': load_avg[1], 
                'load_avg_15m': load_avg[2],
                'top_processes': top_processes,
                'thresholds': {
                    'warning': self.thresholds.cpu_warning,
                    'critical': self.thresholds.cpu_critical
                }
            }
        except Exception as e:
            return {'status': 'ERROR', 'error': str(e)}
    
    def check_memory_health(self) -> Dict[str, Any]:
        """Vérification santé mémoire"""
        try:
            memory = psutil.virtual_memory()
            swap = psutil.swap_memory()
            
            # Determine status
            if memory.percent >= self.thresholds.memory_critical:
                status = "CRITICAL"
                color = "🔴"
            elif memory.percent >= self.thresholds.memory_warning:
                status = "WARNING"
                color = "🟡"
            else:
                status = "OK"
                color = "🟢"
            
            # Top memory consumers
            top_processes = []
            for proc in sorted(psutil.process_iter(['pid', 'name', 'memory_percent']), 
                             key=lambda x: x.info['memory_percent'] or 0, reverse=True)[:5]:
                try:
                    top_processes.append({
                        'pid': proc.info['pid'],
                        'name': proc.info['name'],
                        'memory_percent': round(proc.info['memory_percent'] or 0, 1)
                    })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            return {
                'status': status,
                'color': color,
                'total_gb': round(memory.total / (1024**3), 1),
                'used_gb': round(memory.used / (1024**3), 1),
                'available_gb': round(memory.available / (1024**3), 1),
                'percent_used': memory.percent,
                'swap_percent': swap.percent,
                'top_processes': top_processes,
                'thresholds': {
                    'warning': self.thresholds.memory_warning,
                    'critical': self.thresholds.memory_critical
                }
            }
        except Exception as e:
            return {'status': 'ERROR', 'error': str(e)}
    
    def check_disk_health(self) -> Dict[str, Any]:
        """Vérification santé disques"""
        try:
            partitions = psutil.disk_partitions()
            disk_info = []
            overall_status = "OK"
            overall_color = "🟢"
            
            for partition in partitions:
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    percent_used = (usage.used / usage.total) * 100
                    
                    # Determine status for this partition
                    if percent_used >= self.thresholds.disk_critical:
                        status = "CRITICAL"
                        color = "🔴"
                        overall_status = "CRITICAL"
                        overall_color = "🔴"
                    elif percent_used >= self.thresholds.disk_warning:
                        status = "WARNING"
                        color = "🟡"
                        if overall_status == "OK":
                            overall_status = "WARNING"
                            overall_color = "🟡"
                    else:
                        status = "OK"
                        color = "🟢"
                    
                    disk_info.append({
                        'device': partition.device,
                        'mountpoint': partition.mountpoint,
                        'fstype': partition.fstype,
                        'total_gb': round(usage.total / (1024**3), 1),
                        'used_gb': round(usage.used / (1024**3), 1),
                        'free_gb': round(usage.free / (1024**3), 1),
                        'percent_used': round(percent_used, 1),
                        'status': status,
                        'color': color
                    })
                except Exception:
                    continue
            
            return {
                'status': overall_status,
                'color': overall_color,
                'partitions': disk_info,
                'thresholds': {
                    'warning': self.thresholds.disk_warning,
                    'critical': self.thresholds.disk_critical
                }
            }
        except Exception as e:
            return {'status': 'ERROR', 'error': str(e)}
    
    def check_temperature_health(self) -> Dict[str, Any]:
        """Vérification santé température"""
        try:
            # Try psutil first
            temps = psutil.sensors_temperatures()
            if temps:
                temp_info = []
                overall_status = "OK"
                overall_color = "🟢"
                max_temp = 0
                
                for name, entries in temps.items():
                    for entry in entries:
                        current_temp = entry.current
                        max_temp = max(max_temp, current_temp)
                        
                        # Determine status
                        if current_temp >= self.thresholds.temp_critical:
                            status = "CRITICAL"
                            color = "🔴"
                            overall_status = "CRITICAL"
                            overall_color = "🔴"
                        elif current_temp >= self.thresholds.temp_warning:
                            status = "WARNING"
                            color = "🟡"
                            if overall_status == "OK":
                                overall_status = "WARNING"
                                overall_color = "🟡"
                        else:
                            status = "OK"
                            color = "🟢"
                        
                        temp_info.append({
                            'sensor': f"{name}_{entry.label or 'temp'}",
                            'current': current_temp,
                            'high': entry.high,
                            'critical': entry.critical,
                            'status': status,
                            'color': color
                        })
                
                return {
                    'status': overall_status,
                    'color': overall_color,
                    'max_temperature': max_temp,
                    'sensors': temp_info,
                    'method': 'psutil',
                    'thresholds': {
                        'warning': self.thresholds.temp_warning,
                        'critical': self.thresholds.temp_critical
                    }
                }
            
            # Fallback to sensors command
            try:
                result = subprocess.run(['sensors'], capture_output=True, text=True)
                if result.returncode == 0:
                    sensors_data = []
                    for line in result.stdout.split('\n'):
                        if '°C' in line:
                            sensors_data.append(line.strip())
                    
                    return {
                        'status': 'OK',
                        'color': '🟢',
                        'sensors_raw': sensors_data,
                        'method': 'sensors_command',
                        'note': 'Could not parse detailed temperature data'
                    }
            except Exception:
                pass
            
            return {
                'status': 'UNKNOWN',
                'color': '⚫',
                'error': 'No temperature sensors available'
            }
            
        except Exception as e:
            return {'status': 'ERROR', 'error': str(e)}
    
    def check_network_health(self) -> Dict[str, Any]:
        """Vérification santé réseau"""
        try:
            interfaces = psutil.net_if_addrs()
            stats = psutil.net_if_stats()
            io_counters = psutil.net_io_counters(pernic=True)
            
            network_info = []
            active_count = 0
            
            for interface, addresses in interfaces.items():
                if interface == 'lo':  # Skip loopback
                    continue
                
                is_up = stats[interface].isup if interface in stats else False
                if is_up:
                    active_count += 1
                
                # Get IP addresses
                ipv4_addrs = []
                ipv6_addrs = []
                for addr in addresses:
                    if addr.family == 2:  # IPv4
                        ipv4_addrs.append(addr.address)
                    elif addr.family == 10:  # IPv6
                        ipv6_addrs.append(addr.address)
                
                # Network I/O stats
                io_stats = {}
                if interface in io_counters:
                    io = io_counters[interface]
                    io_stats = {
                        'bytes_sent': io.bytes_sent,
                        'bytes_recv': io.bytes_recv,
                        'packets_sent': io.packets_sent,
                        'packets_recv': io.packets_recv,
                        'errors_in': io.errin,
                        'errors_out': io.errout
                    }
                
                network_info.append({
                    'interface': interface,
                    'is_up': is_up,
                    'ipv4_addresses': ipv4_addrs,
                    'ipv6_addresses': ipv6_addrs,
                    'speed': stats[interface].speed if interface in stats else None,
                    'io_stats': io_stats,
                    'status': '🟢 UP' if is_up else '🔴 DOWN'
                })
            
            return {
                'status': 'OK' if active_count > 0 else 'WARNING',
                'color': '🟢' if active_count > 0 else '🟡',
                'active_interfaces': active_count,
                'total_interfaces': len(network_info),
                'interfaces': network_info
            }
        except Exception as e:
            return {'status': 'ERROR', 'error': str(e)}
    
    def check_services_health(self) -> Dict[str, Any]:
        """Vérification santé services système"""
        try:
            # Critical services to monitor
            critical_services = ['ssh', 'NetworkManager', 'systemd-logind']
            
            service_status = []
            failed_count = 0
            critical_down = 0
            
            for service in critical_services:
                try:
                    result = subprocess.run(['systemctl', 'is-active', service], 
                                          capture_output=True, text=True)
                    is_active = result.stdout.strip() == 'active'
                    
                    service_status.append({
                        'service': service,
                        'status': 'active' if is_active else 'inactive',
                        'color': '🟢' if is_active else '🔴',
                        'critical': True
                    })
                    
                    if not is_active:
                        critical_down += 1
                        
                except Exception:
                    service_status.append({
                        'service': service,
                        'status': 'unknown',
                        'color': '⚫',
                        'critical': True
                    })
                    critical_down += 1
            
            # Check for failed services
            try:
                result = subprocess.run(['systemctl', '--failed', '--no-legend'], 
                                      capture_output=True, text=True)
                failed_services = [line.split()[0] for line in result.stdout.split('\n') 
                                 if line.strip()]
                failed_count = len(failed_services)
            except Exception:
                failed_services = []
                failed_count = 0
            
            # Overall status
            if critical_down > 0:
                overall_status = "CRITICAL"
                overall_color = "🔴"
            elif failed_count > 0:
                overall_status = "WARNING"
                overall_color = "🟡"
            else:
                overall_status = "OK"
                overall_color = "🟢"
            
            return {
                'status': overall_status,
                'color': overall_color,
                'critical_services': service_status,
                'failed_count': failed_count,
                'failed_services': failed_services,
                'critical_down': critical_down
            }
        except Exception as e:
            return {'status': 'ERROR', 'error': str(e)}
    
    def get_system_uptime(self) -> Dict[str, Any]:
        """Informations uptime système"""
        try:
            boot_time = psutil.boot_time()
            uptime_seconds = time.time() - boot_time
            
            # Convert to human readable
            days = int(uptime_seconds // 86400)
            hours = int((uptime_seconds % 86400) // 3600)
            minutes = int((uptime_seconds % 3600) // 60)
            
            uptime_str = f"{days}d {hours}h {minutes}m"
            
            return {
                'uptime_seconds': int(uptime_seconds),
                'uptime_human': uptime_str,
                'boot_time': datetime.fromtimestamp(boot_time).isoformat()
            }
        except Exception as e:
            return {'error': str(e)}
    
    def generate_health_report(self) -> Dict[str, Any]:
        """Rapport complet de santé système"""
        report = {
            'hostname': self.hostname,
            'timestamp': datetime.now().isoformat(),
            'uptime': self.get_system_uptime(),
            'cpu': self.check_cpu_health(),
            'memory': self.check_memory_health(),
            'disk': self.check_disk_health(),
            'temperature': self.check_temperature_health(),
            'network': self.check_network_health(),
            'services': self.check_services_health()
        }
        
        # Overall system status
        statuses = [report[key].get('status', 'UNKNOWN') for key in 
                   ['cpu', 'memory', 'disk', 'temperature', 'network', 'services']]
        
        if 'CRITICAL' in statuses:
            report['overall_status'] = 'CRITICAL'
            report['overall_color'] = '🔴'
        elif 'WARNING' in statuses:
            report['overall_status'] = 'WARNING'
            report['overall_color'] = '🟡'
        elif 'ERROR' in statuses:
            report['overall_status'] = 'ERROR'
            report['overall_color'] = '⚫'
        else:
            report['overall_status'] = 'OK'
            report['overall_color'] = '🟢'
        
        return report
    
    def save_health_report(self, filepath: str) -> bool:
        """Sauvegarde le rapport de santé"""
        try:
            report = self.generate_health_report()
            with open(filepath, 'w') as f:
                yaml.dump(report, f, default_flow_style=False, indent=2)
            return True
        except Exception as e:
            print(f"Error saving health report: {e}")
            return False