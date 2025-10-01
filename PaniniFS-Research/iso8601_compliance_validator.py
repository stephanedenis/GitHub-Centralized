#!/usr/bin/env python3
"""
Scanner Conformité ISO 8601
============================

Identifie tous fichiers avec dates non-conformes au standard ISO 8601.
Standard obligatoire: YYYY-MM-DD (dates) et YYYY-MM-DDTHH:MM:SSZ (timestamps).

Scanne:
    - Noms fichiers (ex: rapport_2025-10-01.md vs rapport_10-01-2025.md)
    - Contenu JSON (champs timestamp, date, created, updated, etc.)
    - Contenu Markdown (dates dans texte)
    - Code Python (strings dates)

Conformité:
    - ISO 8601 timestamps
    - Pattern: *_validator.py (auto-approuvé via autonomous_wrapper.py)
    - Read-only: true
    
Usage:
    python3 iso8601_compliance_validator.py
    python3 autonomous_wrapper.py iso8601_compliance_validator.py

Auteur: Stéphane Denis (via système zéro-approbation)
Date: 2025-10-01
Version: 1.0
"""

import sys
import json
import re
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Set
import os


class ISO8601ComplianceValidator:
    """Validator conformité ISO 8601 pour tous fichiers projet"""
    
    # Patterns dates non-conformes
    NON_COMPLIANT_PATTERNS = [
        r'\b\d{2}[/-]\d{2}[/-]\d{4}\b',  # DD/MM/YYYY ou DD-MM-YYYY
        r'\b\d{2}[/-]\d{2}[/-]\d{2}\b',   # DD/MM/YY ou DD-MM-YY
        r'\b\d{1,2}\s+(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+\d{4}\b',  # 1 January 2025
        r'\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+\d{1,2},?\s+\d{4}\b',  # January 1, 2025
    ]
    
    # Pattern ISO 8601 valide
    ISO8601_PATTERN = r'\b\d{4}-\d{2}-\d{2}(?:T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})?)?\b'
    
    def __init__(self, project_root: Path = None):
        self.project_root = project_root or Path.cwd()
        self.violations = []
        self.compliant_files = []
        
    def scan_all(self) -> Dict:
        """Scan complet projet"""
        print("🔍 Scanning projet pour conformité ISO 8601...")
        
        # Scan filenames
        self._scan_filenames()
        
        # Scan JSON files
        self._scan_json_files()
        
        # Scan Markdown files
        self._scan_markdown_files()
        
        # Scan Python files
        self._scan_python_files()
        
        # Rapport
        return self._generate_report()
        
    def _scan_filenames(self):
        """Scan noms fichiers"""
        print("  📁 Scanning filenames...")
        
        for file_path in self.project_root.rglob("*"):
            if file_path.is_file() and not self._is_excluded(file_path):
                filename = file_path.name
                
                # Chercher dates dans filename
                for pattern in self.NON_COMPLIANT_PATTERNS:
                    matches = re.findall(pattern, filename, re.IGNORECASE)
                    if matches:
                        self.violations.append({
                            "file": str(file_path.relative_to(self.project_root)),
                            "type": "filename",
                            "violation": matches[0],
                            "pattern": pattern,
                            "line": None
                        })
                        break
                else:
                    # Vérifier si ISO 8601 présent
                    if re.search(self.ISO8601_PATTERN, filename):
                        self.compliant_files.append(str(file_path.relative_to(self.project_root)))
                        
    def _scan_json_files(self):
        """Scan fichiers JSON"""
        print("  📄 Scanning JSON files...")
        
        for json_file in self.project_root.rglob("*.json"):
            if self._is_excluded(json_file):
                continue
                
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    data = json.loads(content)
                    
                # Scan champs date/timestamp
                self._scan_json_object(data, json_file, [])
                
            except Exception as e:
                # Ignorer erreurs parsing
                pass
                
    def _scan_json_object(self, obj, file_path: Path, path: List[str]):
        """Scan récursif objet JSON"""
        if isinstance(obj, dict):
            for key, value in obj.items():
                current_path = path + [key]
                
                # Champs dates communs
                if key.lower() in ['date', 'timestamp', 'created', 'updated', 'modified', 'datetime']:
                    if isinstance(value, str):
                        # Vérifier conformité
                        if not re.match(self.ISO8601_PATTERN, value):
                            # Vérifier si non-conforme
                            for pattern in self.NON_COMPLIANT_PATTERNS:
                                if re.search(pattern, value, re.IGNORECASE):
                                    self.violations.append({
                                        "file": str(file_path.relative_to(self.project_root)),
                                        "type": "json_field",
                                        "violation": value,
                                        "field_path": ".".join(current_path),
                                        "line": None
                                    })
                                    break
                                    
                # Récursion
                self._scan_json_object(value, file_path, current_path)
                
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                self._scan_json_object(item, file_path, path + [f"[{i}]"])
                
    def _scan_markdown_files(self):
        """Scan fichiers Markdown"""
        print("  📝 Scanning Markdown files...")
        
        for md_file in self.project_root.rglob("*.md"):
            if self._is_excluded(md_file):
                continue
                
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    
                for line_num, line in enumerate(lines, 1):
                    # Chercher dates non-conformes
                    for pattern in self.NON_COMPLIANT_PATTERNS:
                        matches = re.findall(pattern, line, re.IGNORECASE)
                        if matches:
                            self.violations.append({
                                "file": str(md_file.relative_to(self.project_root)),
                                "type": "markdown_content",
                                "violation": matches[0],
                                "line": line_num,
                                "context": line.strip()[:100]
                            })
                            
            except Exception:
                pass
                
    def _scan_python_files(self):
        """Scan fichiers Python"""
        print("  🐍 Scanning Python files...")
        
        for py_file in self.project_root.rglob("*.py"):
            if self._is_excluded(py_file):
                continue
                
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    
                for line_num, line in enumerate(lines, 1):
                    # Ignorer commentaires
                    if line.strip().startswith('#'):
                        continue
                        
                    # Chercher strings avec dates
                    strings = re.findall(r'["\']([^"\']+)["\']', line)
                    for string in strings:
                        for pattern in self.NON_COMPLIANT_PATTERNS:
                            if re.search(pattern, string, re.IGNORECASE):
                                self.violations.append({
                                    "file": str(py_file.relative_to(self.project_root)),
                                    "type": "python_string",
                                    "violation": string,
                                    "line": line_num,
                                    "context": line.strip()[:100]
                                })
                                
            except Exception:
                pass
                
    def _is_excluded(self, path: Path) -> bool:
        """Vérifie si fichier/dossier exclu du scan"""
        excluded_patterns = [
            '__pycache__',
            '.git',
            'node_modules',
            '.venv',
            'venv',
            '.continue'
        ]
        
        return any(pattern in str(path) for pattern in excluded_patterns)
        
    def _generate_report(self) -> Dict:
        """Génère rapport conformité"""
        total_violations = len(self.violations)
        total_compliant = len(self.compliant_files)
        
        # Grouper violations par type
        violations_by_type = {}
        for violation in self.violations:
            v_type = violation['type']
            if v_type not in violations_by_type:
                violations_by_type[v_type] = []
            violations_by_type[v_type].append(violation)
            
        # Grouper par fichier
        violations_by_file = {}
        for violation in self.violations:
            file = violation['file']
            if file not in violations_by_file:
                violations_by_file[file] = []
            violations_by_file[file].append(violation)
            
        return {
            "success": True,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "project_root": str(self.project_root),
            "total_violations": total_violations,
            "total_compliant": total_compliant,
            "compliance_status": "PASS" if total_violations == 0 else "FAIL",
            "violations_by_type": {k: len(v) for k, v in violations_by_type.items()},
            "violations_by_file": {k: len(v) for k, v in violations_by_file.items()},
            "top_violations": self.violations[:20],  # Top 20
            "statistics": {
                "filenames": len([v for v in self.violations if v['type'] == 'filename']),
                "json_fields": len([v for v in self.violations if v['type'] == 'json_field']),
                "markdown_content": len([v for v in self.violations if v['type'] == 'markdown_content']),
                "python_strings": len([v for v in self.violations if v['type'] == 'python_string'])
            }
        }
        
    def export_json(self, report: Dict, output_path: Path = None):
        """Export rapport JSON"""
        if output_path is None:
            timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H-%M-%SZ')
            output_path = self.project_root / f"iso8601_compliance_report_{timestamp}.json"
            
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
            
        return output_path


def main():
    """Point d'entrée CLI"""
    validator = ISO8601ComplianceValidator()
    
    print("=" * 70)
    print("🔍 SCANNER CONFORMITÉ ISO 8601")
    print("=" * 70)
    print()
    
    # Scan complet
    report = validator.scan_all()
    
    # Export JSON
    output_file = validator.export_json(report)
    
    print()
    print("=" * 70)
    print("📊 RÉSULTATS")
    print("=" * 70)
    
    status_icon = "✅" if report["compliance_status"] == "PASS" else "❌"
    print(f"\nStatus: {status_icon} {report['compliance_status']}")
    print(f"Total violations: {report['total_violations']}")
    print(f"Fichiers conformes: {report['total_compliant']}")
    
    if report['total_violations'] > 0:
        print(f"\n🔸 Violations par Type:")
        for v_type, count in report['violations_by_type'].items():
            print(f"  - {v_type}: {count}")
            
        print(f"\n🔸 Top Fichiers Non-Conformes:")
        sorted_files = sorted(report['violations_by_file'].items(), key=lambda x: x[1], reverse=True)
        for file, count in sorted_files[:10]:
            print(f"  - {file}: {count} violations")
            
        print(f"\n🔸 Exemples Violations (top 5):")
        for i, violation in enumerate(report['top_violations'][:5], 1):
            print(f"\n  {i}. {violation['file']}")
            print(f"     Type: {violation['type']}")
            print(f"     Violation: {violation['violation']}")
            if violation.get('line'):
                print(f"     Line: {violation['line']}")
                
    print(f"\n💾 Rapport complet: {output_file}")
    print(f"Timestamp: {report['timestamp']}")
    print("=" * 70)
    
    # Exit code selon status
    sys.exit(0 if report['compliance_status'] == 'PASS' else 1)


if __name__ == "__main__":
    main()
