#!/usr/bin/env python3
"""
COPILOTAGE DATE VALIDATOR - ISO 8601 ENFORCEMENT
==============================================
Utilitaire pour valider et corriger les formats de dates selon les règles de copilotage
"""

import json
import os
import re
import glob
from datetime import datetime, timezone
from pathlib import Path
import dateutil.parser

class DateFormatValidator:
    def __init__(self):
        self.iso_date_pattern = re.compile(
            r'\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}:\d{2}(\.\d{3})?Z?)?'
        )
        self.non_iso_patterns = [
            re.compile(r'\d{2}/\d{2}/\d{4}'),  # MM/DD/YYYY ou DD/MM/YYYY
            re.compile(r'\d{2}-\d{2}-\d{4}'),  # MM-DD-YYYY ou DD-MM-YYYY
            re.compile(r'\d{4}/\d{2}/\d{2}'),  # YYYY/MM/DD
        ]
        self.violations = []
        
    def validate_filename(self, file_path):
        """Valider le format de date dans un nom de fichier"""
        filename = os.path.basename(file_path)
        
        # Chercher des dates dans le nom de fichier
        date_matches = re.findall(r'\d{4}[-/]\d{2}[-/]\d{2}', filename)
        
        violations = []
        for match in date_matches:
            if '-' in match:
                # Format YYYY-MM-DD (correct)
                continue
            else:
                # Format avec / (incorrect)
                violations.append({
                    'type': 'filename_date_format',
                    'file': file_path,
                    'violation': match,
                    'suggested_fix': match.replace('/', '-'),
                    'severity': 'HIGH'
                })
        
        return violations
    
    def validate_json_dates(self, file_path):
        """Valider les dates dans un fichier JSON"""
        violations = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            def check_recursive(obj, path=""):
                if isinstance(obj, dict):
                    for key, value in obj.items():
                        current_path = f"{path}.{key}" if path else key
                        
                        # Vérifier si c'est un champ de date
                        if any(date_field in key.lower() for date_field in [
                            'date', 'time', 'timestamp', 'created', 'modified', 'updated'
                        ]):
                            if isinstance(value, str):
                                if not self.is_iso_format(value):
                                    violations.append({
                                        'type': 'json_date_format',
                                        'file': file_path,
                                        'field': current_path,
                                        'violation': value,
                                        'suggested_fix': self.convert_to_iso(value),
                                        'severity': 'HIGH'
                                    })
                        
                        # Récursion
                        check_recursive(value, current_path)
                        
                elif isinstance(obj, list):
                    for i, item in enumerate(obj):
                        check_recursive(item, f"{path}[{i}]")
            
            check_recursive(data)
            
        except Exception as e:
            violations.append({
                'type': 'json_parse_error',
                'file': file_path,
                'error': str(e),
                'severity': 'MEDIUM'
            })
        
        return violations
    
    def validate_log_timestamps(self, file_path):
        """Valider les timestamps dans un fichier log"""
        violations = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            for line_num, line in enumerate(lines, 1):
                # Chercher des timestamps au début de ligne
                timestamp_match = re.match(r'^\[([^\]]+)\]', line.strip())
                if timestamp_match:
                    timestamp = timestamp_match.group(1)
                    if not self.is_iso_format(timestamp):
                        violations.append({
                            'type': 'log_timestamp_format',
                            'file': file_path,
                            'line': line_num,
                            'violation': timestamp,
                            'suggested_fix': self.convert_to_iso(timestamp),
                            'severity': 'MEDIUM'
                        })
        
        except Exception as e:
            violations.append({
                'type': 'log_parse_error',
                'file': file_path,
                'error': str(e),
                'severity': 'LOW'
            })
        
        return violations
    
    def is_iso_format(self, date_string):
        """Vérifier si une chaîne est au format ISO 8601"""
        try:
            # Tentative de parsing strict ISO
            if 'T' in date_string:
                # Format datetime
                return bool(re.match(
                    r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{3})?Z?$', 
                    date_string
                ))
            else:
                # Format date seulement
                return bool(re.match(r'^\d{4}-\d{2}-\d{2}$', date_string))
        except:
            return False
    
    def convert_to_iso(self, date_string):
        """Convertir une date vers le format ISO 8601"""
        try:
            # Tentative de parsing avec dateutil
            parsed_date = dateutil.parser.parse(date_string)
            
            # Si pas de timezone, ajouter UTC
            if parsed_date.tzinfo is None:
                parsed_date = parsed_date.replace(tzinfo=timezone.utc)
            
            return parsed_date.isoformat()
        except:
            # Si la conversion échoue, retourner la date actuelle ISO
            return datetime.now(timezone.utc).isoformat()
    
    def scan_workspace(self, workspace_path="."):
        """Scanner tout le workspace pour les violations de format de date"""
        print("🔍 SCAN COPILOTAGE - VALIDATION DATES ISO 8601")
        print("=" * 60)
        
        all_violations = []
        
        # Scanner les fichiers JSON
        json_files = glob.glob(os.path.join(workspace_path, "**/*.json"), recursive=True)
        print(f"📄 Scan {len(json_files)} fichiers JSON...")
        
        for json_file in json_files:
            # Valider nom de fichier
            filename_violations = self.validate_filename(json_file)
            all_violations.extend(filename_violations)
            
            # Valider contenu JSON
            json_violations = self.validate_json_dates(json_file)
            all_violations.extend(json_violations)
        
        # Scanner les fichiers log
        log_files = glob.glob(os.path.join(workspace_path, "**/*.log"), recursive=True)
        print(f"📝 Scan {len(log_files)} fichiers log...")
        
        for log_file in log_files:
            log_violations = self.validate_log_timestamps(log_file)
            all_violations.extend(log_violations)
        
        # Scanner les fichiers Python pour les dates hardcodées
        py_files = glob.glob(os.path.join(workspace_path, "**/*.py"), recursive=True)
        print(f"🐍 Scan {len(py_files)} fichiers Python...")
        
        for py_file in py_files:
            filename_violations = self.validate_filename(py_file)
            all_violations.extend(filename_violations)
        
        return all_violations
    
    def generate_compliance_report(self, violations):
        """Générer un rapport de conformité"""
        report = {
            'scan_timestamp': datetime.now(timezone.utc).isoformat(),
            'total_violations': len(violations),
            'severity_summary': {
                'HIGH': len([v for v in violations if v.get('severity') == 'HIGH']),
                'MEDIUM': len([v for v in violations if v.get('severity') == 'MEDIUM']),
                'LOW': len([v for v in violations if v.get('severity') == 'LOW'])
            },
            'violation_types': {
                'filename_date_format': len([v for v in violations if v.get('type') == 'filename_date_format']),
                'json_date_format': len([v for v in violations if v.get('type') == 'json_date_format']),
                'log_timestamp_format': len([v for v in violations if v.get('type') == 'log_timestamp_format'])
            },
            'violations': violations
        }
        
        # Sauvegarder le rapport
        report_file = f"copilotage_date_compliance_{datetime.now(timezone.utc).strftime('%Y-%m-%dT%H-%M-%SZ')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        return report, report_file

def main():
    validator = DateFormatValidator()
    
    # Scanner le workspace
    violations = validator.scan_workspace()
    
    # Générer le rapport
    report, report_file = validator.generate_compliance_report(violations)
    
    print(f"\n📊 RAPPORT DE CONFORMITÉ DATES ISO")
    print("=" * 50)
    print(f"🔍 Total violations: {report['total_violations']}")
    print(f"🚨 Sévérité HIGH: {report['severity_summary']['HIGH']}")
    print(f"⚠️  Sévérité MEDIUM: {report['severity_summary']['MEDIUM']}")
    print(f"ℹ️  Sévérité LOW: {report['severity_summary']['LOW']}")
    
    print(f"\n📋 Types de violations:")
    for vtype, count in report['violation_types'].items():
        print(f"   {vtype}: {count}")
    
    if violations:
        print(f"\n🔍 DÉTAILS VIOLATIONS (Top 10):")
        for violation in violations[:10]:
            print(f"   ❌ {violation['type']}: {violation['file']}")
            print(f"      Problème: {violation['violation']}")
            if 'suggested_fix' in violation:
                print(f"      Solution: {violation['suggested_fix']}")
            print()
    
    print(f"📄 Rapport complet sauvé: {report_file}")

if __name__ == "__main__":
    main()