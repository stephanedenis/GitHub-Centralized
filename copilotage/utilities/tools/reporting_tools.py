#!/usr/bin/env python3
"""
Reporting Tools - Génération Rapports Réutilisables
===================================================

Remplace la génération ad-hoc de rapports texte:
- echo "RAPPORT..." → reporting.generate_section_report()
- Rapports formatés → reporting.create_formatted_report()
- Tableaux de données → reporting.create_data_table()
"""

import json
import sqlite3
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime
import textwrap


class ReportingTools:
    """Outils génération rapports réutilisables"""
    
    def __init__(self):
        self.workspace_root = Path("/home/stephane/GitHub/PaniniFS-Research")
        self.web_dir = self.workspace_root / "web"
        
    def format_section(self, title: str, content: str = "", 
                      emoji: str = "📊", level: int = 1) -> str:
        """Formatage section standardisé"""
        if level == 1:
            separator = "=" * len(title)
            return f"\n{emoji} {title.upper()}\n{separator}\n{content}\n"
        elif level == 2:
            separator = "-" * len(title)
            return f"\n{emoji} {title}\n{separator}\n{content}\n"
        else:
            return f"\n{emoji} {title}:\n{content}\n"
            
    def format_data_table(self, data: List[Dict], 
                         columns: List[str] = None,
                         max_width: int = 80) -> str:
        """Formatage tableau de données"""
        if not data:
            return "Aucune donnée disponible"
            
        if columns is None:
            columns = list(data[0].keys())
            
        # Calcul largeurs colonnes
        col_widths = {}
        for col in columns:
            max_len = len(col)
            for row in data:
                value_len = len(str(row.get(col, "")))
                max_len = max(max_len, value_len)
            col_widths[col] = min(max_len, max_width // len(columns))
            
        # Génération tableau
        lines = []
        
        # En-tête
        header = " | ".join(col.ljust(col_widths[col]) for col in columns)
        lines.append(header)
        lines.append("-" * len(header))
        
        # Données
        for row in data:
            row_str = " | ".join(
                str(row.get(col, "")).ljust(col_widths[col]) 
                for col in columns
            )
            lines.append(row_str)
            
        return "\n".join(lines)
        
    def format_metrics(self, metrics: Dict[str, Any]) -> str:
        """Formatage métriques système"""
        sections = []
        
        if 'cpu' in metrics:
            cpu = metrics['cpu']
            sections.append(
                f"🖥️  CPU: {cpu.get('percent', 'N/A'):.1f}% "
                f"({cpu.get('count', 'N/A')} cores)"
            )
            
        if 'memory' in metrics:
            memory = metrics['memory']
            total_gb = memory.get('total', 0) // 1024 // 1024 // 1024
            used_gb = memory.get('used', 0) // 1024 // 1024 // 1024
            sections.append(
                f"💾 RAM: {memory.get('percent', 'N/A'):.1f}% "
                f"({used_gb}GB/{total_gb}GB)"
            )
            
        if 'disk' in metrics:
            disk = metrics['disk']
            sections.append(
                f"💿 Disk: {disk.get('percent', 'N/A'):.1f}%"
            )
            
        return "\n".join(f"  {section}" for section in sections)
        
    def create_corpus_report(self, db_path: str = "real_corpus_analysis.db") -> str:
        """Rapport corpus standardisé"""
        report_sections = []
        
        db_full_path = self.web_dir / db_path
        if not db_full_path.exists():
            return self.format_section(
                "ERREUR CORPUS", 
                f"Base de données non trouvée: {db_path}",
                "❌"
            )
            
        try:
            with sqlite3.connect(str(db_full_path)) as conn:
                cursor = conn.cursor()
                
                # Statistiques générales
                cursor.execute("SELECT COUNT(*) FROM real_corpus")
                total_docs = cursor.fetchone()[0]
                
                report_sections.append(
                    self.format_section(
                        "STATISTIQUES CORPUS",
                        f"📄 Documents totaux: {total_docs:,}",
                        "📚"
                    )
                )
                
                # Par source
                cursor.execute("""
                    SELECT source, COUNT(*) as count 
                    FROM real_corpus 
                    GROUP BY source 
                    ORDER BY count DESC
                """)
                sources = cursor.fetchall()
                
                source_lines = []
                for source, count in sources:
                    source_lines.append(f"  • {source}: {count:,} documents")
                    
                report_sections.append(
                    self.format_section(
                        "RÉPARTITION PAR SOURCE",
                        "\n".join(source_lines),
                        "🌐",
                        2
                    )
                )
                
                # Par langue
                cursor.execute("""
                    SELECT language, COUNT(*) as count 
                    FROM real_corpus 
                    GROUP BY language 
                    ORDER BY count DESC
                """)
                languages = cursor.fetchall()
                
                lang_lines = []
                for lang, count in languages:
                    lang_lines.append(f"  • {lang}: {count:,} documents")
                    
                report_sections.append(
                    self.format_section(
                        "COUVERTURE LINGUISTIQUE",
                        "\n".join(lang_lines),
                        "🌍",
                        2
                    )
                )
                
        except sqlite3.Error as e:
            report_sections.append(
                self.format_section(
                    "ERREUR DATABASE",
                    f"Erreur SQLite: {e}",
                    "❌"
                )
            )
            
        return "".join(report_sections)
        
    def create_dhatu_report(self, db_path: str = "real_dhatu_analysis.db") -> str:
        """Rapport dhātu standardisé"""
        report_sections = []
        
        db_full_path = self.web_dir / db_path
        if not db_full_path.exists():
            return self.format_section(
                "ERREUR DHĀTU",
                f"Base de données non trouvée: {db_path}",
                "❌"
            )
            
        try:
            with sqlite3.connect(str(db_full_path)) as conn:
                cursor = conn.cursor()
                
                # Statistiques générales
                cursor.execute("SELECT COUNT(*) FROM real_dhatu_atoms")
                total_atoms = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM real_dhatu_patterns")
                total_patterns = cursor.fetchone()[0]
                
                ratio = total_atoms / total_patterns if total_patterns > 0 else 0
                
                stats_content = f"""📊 Atomes dhātu extraits: {total_atoms:,}
📊 Patterns identifiés: {total_patterns:,}
📊 Ratio atomes/patterns: {ratio:.1f}"""
                
                report_sections.append(
                    self.format_section(
                        "ANALYSE DHĀTU",
                        stats_content,
                        "⚛️"
                    )
                )
                
                # Top atomes
                cursor.execute("""
                    SELECT form, frequency 
                    FROM real_dhatu_atoms 
                    ORDER BY frequency DESC 
                    LIMIT 10
                """)
                top_atoms = cursor.fetchall()
                
                atom_lines = []
                for i, (form, freq) in enumerate(top_atoms, 1):
                    atom_lines.append(f"  {i:2d}. {form} (fréq: {freq})")
                    
                report_sections.append(
                    self.format_section(
                        "TOP ATOMES DHĀTU",
                        "\n".join(atom_lines),
                        "🔝",
                        2
                    )
                )
                
                # Distribution longueurs
                cursor.execute("""
                    SELECT LENGTH(form) as length, COUNT(*) as count
                    FROM real_dhatu_atoms 
                    GROUP BY LENGTH(form) 
                    ORDER BY length
                """)
                lengths = cursor.fetchall()
                
                length_lines = []
                for length, count in lengths:
                    percent = (count / total_atoms) * 100 if total_atoms > 0 else 0
                    length_lines.append(f"  • {length} caractères: {count:,} ({percent:.1f}%)")
                    
                report_sections.append(
                    self.format_section(
                        "DISTRIBUTION LONGUEURS",
                        "\n".join(length_lines),
                        "📏",
                        2
                    )
                )
                
        except sqlite3.Error as e:
            report_sections.append(
                self.format_section(
                    "ERREUR DATABASE",
                    f"Erreur SQLite: {e}",
                    "❌"
                )
            )
            
        return "".join(report_sections)
        
    def create_validation_report(self) -> str:
        """Rapport validation standardisé"""
        from database_tools import DatabaseTools
        
        db_tools = DatabaseTools()
        validation = db_tools.validation_check()
        
        report_sections = []
        
        # Métriques validation
        checks = validation['checks']
        metrics_content = f"""📄 Documents corpus: {checks['corpus_docs']:,}
⚛️  Atomes dhātu: {checks['dhatu_atoms']:,}
📊 Patterns dhātu: {checks['dhatu_patterns']:,}
🌍 Langues couvertes: {checks['languages']}"""
        
        report_sections.append(
            self.format_section(
                "MÉTRIQUES VALIDATION",
                metrics_content,
                "📊"
            )
        )
        
        # Résultats validation
        validation_results = validation['validation']
        result_lines = []
        
        for key, passed in validation_results.items():
            icon = "✅" if passed else "❌"
            name = key.replace('_', ' ').title()
            result_lines.append(f"  {icon} {name}")
            
        success_rate = sum(validation_results.values()) / len(validation_results) * 100
        result_lines.append(f"\n🎯 Taux de réussite: {success_rate:.1f}%")
        
        report_sections.append(
            self.format_section(
                "RÉSULTATS VALIDATION",
                "\n".join(result_lines),
                "✅" if validation['all_passed'] else "❌",
                2
            )
        )
        
        return "".join(report_sections)
        
    def create_complete_report(self, output_file: str = None) -> str:
        """Rapport complet projet"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        report_parts = [
            self.format_section(
                "RAPPORT COMPLET PANINI-FS DHĀTU",
                f"Généré le: {timestamp}",
                "📋"
            ),
            self.create_corpus_report(),
            self.create_dhatu_report(),
            self.create_validation_report()
        ]
        
        complete_report = "".join(report_parts)
        
        if output_file:
            output_path = self.web_dir / output_file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(complete_report)
            print(f"📄 Rapport complet sauvegardé: {output_path}")
            
        return complete_report


def main():
    """Test du module reporting_tools"""
    reporting = ReportingTools()
    
    print("🧪 TEST REPORTING TOOLS")
    print("=" * 30)
    
    # Test formatage section
    print(reporting.format_section("Test Section", "Contenu de test", "🧪"))
    
    # Test tableau
    test_data = [
        {'name': 'Python', 'count': 42, 'status': 'active'},
        {'name': 'SQLite', 'count': 15, 'status': 'ready'},
        {'name': 'HTTP', 'count': 8, 'status': 'pending'}
    ]
    
    print("📊 TEST TABLEAU:")
    print(reporting.format_data_table(test_data))
    
    # Test rapports
    print("\n📋 GÉNÉRATION RAPPORTS...")
    
    # Rapport validation (fonctionne toujours)
    validation_report = reporting.create_validation_report()
    print("✅ Rapport validation généré")
    
    # Autres rapports si BDD existent
    if (Path(reporting.web_dir) / "real_corpus_analysis.db").exists():
        corpus_report = reporting.create_corpus_report()
        print("✅ Rapport corpus généré")
        
    if (Path(reporting.web_dir) / "real_dhatu_analysis.db").exists():
        dhatu_report = reporting.create_dhatu_report()
        print("✅ Rapport dhātu généré")
    
    return 0


if __name__ == "__main__":
    main()