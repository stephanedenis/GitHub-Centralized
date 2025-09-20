#!/usr/bin/env python3
"""
Database Tools - Opérations SQLite Réutilisables
================================================

Remplace toutes les commandes SQLite ad-hoc que j'ai créées:
- sqlite3 db "SELECT ..." → database.query()
- sqlite3 db ".tables" → database.list_tables()
- Rapports SQLite → database.generate_report()
"""

import sqlite3
import json
from pathlib import Path
from typing import List, Dict, Any, Optional, Union


class DatabaseTools:
    """Outils SQLite réutilisables"""
    
    def __init__(self):
        self.workspace_root = Path("/home/stephane/GitHub/PaniniFS-Research")
        self.web_dir = self.workspace_root / "web"
        
    def connect(self, db_path: Union[str, Path]) -> sqlite3.Connection:
        """Connexion SQLite avec gestion erreurs"""
        if isinstance(db_path, str):
            db_path = Path(db_path)
            
        if not db_path.is_absolute():
            db_path = self.web_dir / db_path
            
        return sqlite3.connect(str(db_path))
        
    def query(self, db_path: Union[str, Path], sql: str, 
              params: tuple = None) -> List[Dict[str, Any]]:
        """Exécution query avec résultats structurés"""
        try:
            with self.connect(db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                if params:
                    cursor.execute(sql, params)
                else:
                    cursor.execute(sql)
                    
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
                
        except sqlite3.Error as e:
            print(f"❌ Erreur SQLite: {e}")
            return []
            
    def list_tables(self, db_path: Union[str, Path]) -> List[str]:
        """Liste des tables (remplace .tables)"""
        tables = self.query(db_path, 
            "SELECT name FROM sqlite_master WHERE type='table'")
        return [table['name'] for table in tables]
        
    def table_info(self, db_path: Union[str, Path], 
                   table_name: str) -> List[Dict[str, Any]]:
        """Info structure table (remplace .schema)"""
        return self.query(db_path, f"PRAGMA table_info({table_name})")
        
    def count_records(self, db_path: Union[str, Path], 
                      table_name: str) -> int:
        """Compte enregistrements table"""
        result = self.query(db_path, f"SELECT COUNT(*) as count FROM {table_name}")
        return result[0]['count'] if result else 0
        
    def table_stats(self, db_path: Union[str, Path], 
                    table_name: str) -> Dict[str, Any]:
        """Statistiques complètes table"""
        info = self.table_info(db_path, table_name)
        count = self.count_records(db_path, table_name)
        
        return {
            'name': table_name,
            'columns': len(info),
            'records': count,
            'schema': info
        }
        
    def database_overview(self, db_path: Union[str, Path]) -> Dict[str, Any]:
        """Vue d'ensemble base de données"""
        tables = self.list_tables(db_path)
        overview = {
            'path': str(db_path),
            'tables_count': len(tables),
            'tables': {}
        }
        
        total_records = 0
        for table in tables:
            stats = self.table_stats(db_path, table)
            overview['tables'][table] = stats
            total_records += stats['records']
            
        overview['total_records'] = total_records
        return overview
        
    # ======== QUERIES SPÉCIFIQUES PROJET ========
    
    def corpus_stats(self, db_path: str = "real_corpus_analysis.db") -> Dict[str, Any]:
        """Statistiques corpus (remplace queries repetées)"""
        queries = {
            'total_docs': "SELECT COUNT(*) as count FROM real_corpus",
            'by_source': "SELECT source, COUNT(*) as count FROM real_corpus GROUP BY source ORDER BY count DESC",
            'by_language': "SELECT language, COUNT(*) as count FROM real_corpus GROUP BY language ORDER BY count DESC",
            'by_category': "SELECT category, COUNT(*) as count FROM real_corpus WHERE category IS NOT NULL GROUP BY category"
        }
        
        stats = {}
        for key, sql in queries.items():
            stats[key] = self.query(db_path, sql)
            
        return stats
        
    def dhatu_stats(self, db_path: str = "real_dhatu_analysis.db") -> Dict[str, Any]:
        """Statistiques dhātu (remplace queries repetées)"""
        queries = {
            'total_atoms': "SELECT COUNT(*) as count FROM real_dhatu_atoms",
            'total_patterns': "SELECT COUNT(*) as count FROM real_dhatu_patterns",
            'top_atoms': "SELECT form, frequency FROM real_dhatu_atoms ORDER BY frequency DESC LIMIT 10",
            'atoms_by_length': "SELECT LENGTH(form) as length, COUNT(*) as count FROM real_dhatu_atoms GROUP BY LENGTH(form) ORDER BY length"
        }
        
        stats = {}
        for key, sql in queries.items():
            stats[key] = self.query(db_path, sql)
            
        return stats
        
    def validation_check(self, 
                        corpus_db: str = "real_corpus_analysis.db",
                        dhatu_db: str = "real_dhatu_analysis.db") -> Dict[str, Any]:
        """Validation automatique (remplace validation répétée)"""
        checks = {
            'corpus_docs': self.query(corpus_db, "SELECT COUNT(*) as count FROM real_corpus")[0]['count'],
            'dhatu_atoms': self.query(dhatu_db, "SELECT COUNT(*) as count FROM real_dhatu_atoms")[0]['count'],
            'dhatu_patterns': self.query(dhatu_db, "SELECT COUNT(*) as count FROM real_dhatu_patterns")[0]['count'],
            'languages': len(self.query(corpus_db, "SELECT DISTINCT language FROM real_corpus"))
        }
        
        # Critères validation
        validation = {
            'corpus_docs_ok': 400 <= checks['corpus_docs'] <= 600,
            'dhatu_atoms_ok': 2000 <= checks['dhatu_atoms'] <= 3500,
            'dhatu_patterns_ok': 80 <= checks['dhatu_patterns'] <= 150,
            'languages_ok': checks['languages'] >= 8
        }
        
        return {
            'checks': checks,
            'validation': validation,
            'all_passed': all(validation.values())
        }
        
    def generate_report(self, output_file: str = None) -> Dict[str, Any]:
        """Génère rapport complet bases de données"""
        report = {
            'corpus': self.corpus_stats(),
            'dhatu': self.dhatu_stats(),
            'validation': self.validation_check()
        }
        
        if output_file:
            output_path = self.web_dir / output_file
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            print(f"📄 Rapport sauvegardé: {output_path}")
            
        return report
        
    def execute_script(self, db_path: Union[str, Path], 
                      script_path: Union[str, Path]) -> bool:
        """Exécution script SQL depuis fichier"""
        try:
            with open(script_path, 'r', encoding='utf-8') as f:
                script = f.read()
                
            with self.connect(db_path) as conn:
                conn.executescript(script)
                
            print(f"✅ Script exécuté: {script_path}")
            return True
            
        except Exception as e:
            print(f"❌ Erreur script: {e}")
            return False


def main():
    """Test du module database_tools"""
    tools = DatabaseTools()
    
    print("🧪 TEST DATABASE TOOLS")
    print("=" * 30)
    
    # Test bases projet
    corpus_db = "real_corpus_analysis.db"
    dhatu_db = "real_dhatu_analysis.db"
    
    if Path(tools.web_dir / corpus_db).exists():
        print(f"\n📊 ANALYSE CORPUS")
        stats = tools.corpus_stats()
        if stats['total_docs']:
            print(f"Documents: {stats['total_docs'][0]['count']}")
            print("Sources:")
            for source in stats['by_source'][:3]:
                print(f"  - {source['source']}: {source['count']}")
    
    if Path(tools.web_dir / dhatu_db).exists():
        print(f"\n⚛️  ANALYSE DHĀTU")
        stats = tools.dhatu_stats()
        if stats['total_atoms']:
            print(f"Atomes: {stats['total_atoms'][0]['count']}")
            print(f"Patterns: {stats['total_patterns'][0]['count']}")
    
    # Test validation
    print(f"\n✅ VALIDATION")
    validation = tools.validation_check()
    for key, passed in validation['validation'].items():
        icon = "✅" if passed else "❌"
        print(f"  {icon} {key}: {passed}")
    
    return 0


if __name__ == "__main__":
    main()