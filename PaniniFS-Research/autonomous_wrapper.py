#!/usr/bin/env python3
"""
Wrapper Autonome pour Exécution Scripts Python
================================================

Exécute scripts Python pré-approuvés avec validation et logging automatique.
Compatible GitHub Copilot Coding Agent pour réduire approbations manuelles.

Usage:
    python3 autonomous_wrapper.py <script_name> [args...]

Exemples:
    python3 autonomous_wrapper.py translator_metadata_extractor.py
    python3 autonomous_wrapper.py symmetry_detector_poc.py --verbose
    python3 autonomous_wrapper.py scan_real_panini_data.py corpus.json

Conformité:
    - ISO 8601: Tous timestamps
    - Whitelist: .github/copilot-approved-scripts.json
    - Logging: autonomous_execution.log (JSON)
    - Safety: Constraints validation automatique

Auteur: Stéphane Denis
Date: 2025-10-01
Version: 1.0
"""

import subprocess
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple
import time
import re


class AutonomousScriptRunner:
    """
    Exécuteur autonome scripts Python pré-approuvés
    
    Valide scripts contre whitelist, exécute avec timeout,
    log résultats format JSON ISO 8601.
    """
    
    def __init__(self, project_root: Optional[Path] = None):
        """
        Initialize runner
        
        Args:
            project_root: Racine projet (défaut: parent de ce script)
        """
        self.project_root = project_root or Path(__file__).parent
        self.whitelist_path = self.project_root / ".github" / "copilot-approved-scripts.json"
        self.log_file = self.project_root / "autonomous_execution.log"
        
        # Charger whitelist
        self.whitelist = self._load_whitelist()
        
    def _load_whitelist(self) -> dict:
        """Charge whitelist scripts approuvés"""
        if not self.whitelist_path.exists():
            print(f"⚠️  Whitelist not found: {self.whitelist_path}", file=sys.stderr)
            print("Using default patterns only", file=sys.stderr)
            return {
                "approved_patterns": {
                    "extractors": {"pattern": "**/*_extractor.py"},
                    "analyzers": {"pattern": "**/*_analyzer.py"},
                    "validators": {"pattern": "**/*_validator.py"},
                    "scanners": {"pattern": "scan_*.py"}
                }
            }
            
        try:
            with open(self.whitelist_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"❌ Whitelist JSON invalid: {e}", file=sys.stderr)
            sys.exit(1)
            
    def _matches_pattern(self, script_path: Path, pattern: str) -> bool:
        """
        Vérifie si script match pattern glob
        
        Args:
            script_path: Chemin script
            pattern: Pattern glob (e.g., "**/*_analyzer.py")
            
        Returns:
            True si match
        """
        # Conversion pattern glob vers regex simple
        pattern_re = pattern.replace("**/*", ".*").replace("*", "[^/]*")
        pattern_re = f"^{pattern_re}$"
        
        return bool(re.match(pattern_re, str(script_path.name)))
        
    def is_approved(self, script_path: Path) -> Tuple[bool, Optional[str]]:
        """
        Vérifie si script pré-approuvé
        
        Args:
            script_path: Chemin script à valider
            
        Returns:
            (approved: bool, category: Optional[str])
        """
        approved_patterns = self.whitelist.get("approved_patterns", {})
        
        for category, config in approved_patterns.items():
            pattern = config.get("pattern", "")
            if self._matches_pattern(script_path, pattern):
                return True, category
                
        return False, None
        
    def _validate_constraints(
        self, 
        script_path: Path, 
        category: str,
        args: Optional[List[str]]
    ) -> Tuple[bool, Optional[str]]:
        """
        Valide contraintes catégorie script
        
        Args:
            script_path: Chemin script
            category: Catégorie (extractors, analyzers, etc.)
            args: Arguments ligne commande
            
        Returns:
            (valid: bool, error_message: Optional[str])
        """
        constraints = self.whitelist.get("approved_patterns", {}).get(category, {}).get("constraints", {})
        
        # Vérifier args requis
        required_args = constraints.get("required_args", [])
        if required_args and not args:
            return False, f"Script requires args: {required_args}"
            
        # Vérifier read-only si applicable
        is_read_only = constraints.get("read_only", False)
        if is_read_only:
            # TODO: Analyse statique pour vérifier absence écritures
            pass
            
        return True, None
        
    def run_script(
        self, 
        script_name: str, 
        args: Optional[List[str]] = None,
        verbose: bool = False
    ) -> Dict:
        """
        Exécute script pré-approuvé avec logging
        
        Args:
            script_name: Nom script (relatif ou absolu)
            args: Arguments optionnels
            verbose: Mode verbeux
            
        Returns:
            dict avec stdout, stderr, returncode, timestamp, etc.
        """
        start_time = time.time()
        script_path = self.project_root / script_name
        
        # Validation existence
        if not script_path.exists():
            return self._error_result(
                f"Script not found: {script_name}",
                script_name,
                args,
                start_time
            )
            
        # Validation approbation
        is_approved, category = self.is_approved(script_path)
        if not is_approved:
            return self._error_result(
                f"Script not in approved whitelist: {script_name}",
                script_name,
                args,
                start_time
            )
            
        if verbose:
            print(f"✅ Script approved: {category}")
            
        # Validation contraintes
        constraints_valid, constraint_error = self._validate_constraints(
            script_path, 
            category, 
            args
        )
        if not constraints_valid:
            return self._error_result(
                f"Constraint violation: {constraint_error}",
                script_name,
                args,
                start_time
            )
            
        # Récupérer timeout
        constraints = self.whitelist.get("approved_patterns", {}).get(category, {}).get("constraints", {})
        timeout = constraints.get("max_execution_time_seconds", 600)
        
        # Construction commande
        cmd = ["python3", str(script_path)]
        if args:
            cmd.extend(args)
            
        if verbose:
            print(f"🚀 Executing: {' '.join(cmd)}")
            print(f"⏱️  Timeout: {timeout}s")
            
        # Exécution avec timeout
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=self.project_root
            )
            
            execution_time = time.time() - start_time
            
            output = {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
                "script": script_name,
                "category": category,
                "args": args or [],
                "execution_time_seconds": round(execution_time, 3),
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            
            # Log résultat
            self._log_execution(output)
            
            if verbose:
                status = "✅" if output["success"] else "❌"
                print(f"{status} Execution completed in {execution_time:.2f}s")
            
            return output
            
        except subprocess.TimeoutExpired:
            execution_time = time.time() - start_time
            return self._error_result(
                f"Script timeout after {timeout}s",
                script_name,
                args,
                start_time,
                category=category
            )
        except Exception as e:
            return self._error_result(
                f"Execution error: {str(e)}",
                script_name,
                args,
                start_time,
                category=category
            )
            
    def _error_result(
        self,
        error_msg: str,
        script_name: str,
        args: Optional[List[str]],
        start_time: float,
        category: Optional[str] = None
    ) -> Dict:
        """Génère résultat erreur standardisé"""
        execution_time = time.time() - start_time
        
        result = {
            "success": False,
            "error": error_msg,
            "script": script_name,
            "category": category,
            "args": args or [],
            "execution_time_seconds": round(execution_time, 3),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        self._log_execution(result)
        return result
            
    def _log_execution(self, result: Dict):
        """
        Log exécution dans fichier JSON
        
        Args:
            result: Résultat exécution
        """
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(result, ensure_ascii=False) + "\n")
        except Exception as e:
            print(f"⚠️  Logging failed: {e}", file=sys.stderr)


def main():
    """Point d'entrée CLI"""
    parser = argparse.ArgumentParser(
        description="Wrapper autonome exécution scripts Python pré-approuvés",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
  %(prog)s translator_metadata_extractor.py
  %(prog)s symmetry_detector_poc.py --verbose
  %(prog)s scan_real_panini_data.py corpus.json

Scripts approuvés définis dans:
  .github/copilot-approved-scripts.json
        """
    )
    
    parser.add_argument(
        "script_name",
        help="Nom script Python à exécuter (relatif au projet)"
    )
    
    parser.add_argument(
        "script_args",
        nargs="*",
        help="Arguments optionnels pour le script"
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Mode verbeux"
    )
    
    parser.add_argument(
        "--project-root",
        type=Path,
        help="Racine projet (défaut: répertoire courant)"
    )
    
    args = parser.parse_args()
    
    # Initialiser runner
    runner = AutonomousScriptRunner(project_root=args.project_root)
    
    # Exécuter script
    result = runner.run_script(
        args.script_name,
        args.script_args if args.script_args else None,
        verbose=args.verbose
    )
    
    # Afficher résultat
    if args.verbose or not result["success"]:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        # Mode silencieux : juste stdout du script
        print(result.get("stdout", ""), end="")
        
    # Exit code
    sys.exit(0 if result["success"] else 1)


if __name__ == "__main__":
    main()
