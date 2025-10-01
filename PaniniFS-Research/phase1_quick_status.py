#!/usr/bin/env python3
"""
Phase 1 Quick Status - Check rapide rendement

Affiche résumé ultra-condensé de l'état Phase 1.
Usage: python3 phase1_quick_status.py

Auteur: Autonomous System
Timestamp: 2025-10-01T18:10:00Z
"""

import json
from pathlib import Path
from datetime import datetime, timezone


def main():
    """Check rapide état Phase 1."""
    workspace = Path("/home/stephane/GitHub/PaniniFS-Research")
    report_path = workspace / 'phase1_progress_report.json'
    
    print("\n" + "="*50)
    print("⚡ PHASE 1 CORE - QUICK STATUS")
    print("="*50)
    
    if not report_path.exists():
        print("\n❌ Pas encore de données monitoring")
        print("   → Lancer: ./start_phase1_monitoring.sh")
        return
    
    # Charger dernier rapport
    with open(report_path, 'r') as f:
        data = json.load(f)
    
    progress = data['current_progress']
    
    # Temps
    now = datetime.now(timezone.utc)
    last_check = datetime.fromisoformat(progress['timestamp'])
    age_minutes = int((now - last_check).total_seconds() / 60)
    
    print(f"\n⏰ Dernier check: il y a {age_minutes}min")
    print(f"⏱️  Elapsed: {progress['elapsed_hours']:.1f}h")
    print(f"⏳ Remaining: {progress['remaining_minutes']}min")
    
    # Progression
    percent = progress['overall_percent']
    status = progress['status']
    
    status_icons = {
        'ON_TRACK': '✅',
        'ACCEPTABLE': '🟡',
        'AT_RISK': '⚠️',
        'STARTING': '🔵'
    }
    icon = status_icons.get(status, '❓')
    
    print(f"\n{icon} {percent}% [{status}]")
    
    # Barre mini
    bar_length = 20
    filled = int((percent / 100) * bar_length)
    bar = '█' * filled + '░' * (bar_length - filled)
    print(f"[{bar}] Target: 37-50%")
    
    # Tâches
    print(f"\n📋 Tâches:")
    
    task_results = progress['task_results']
    
    completed = sum(
        1 for r in task_results.values()
        if r['status'] == 'COMPLETED'
    )
    in_progress = sum(
        1 for r in task_results.values()
        if r['status'] == 'IN_PROGRESS'
    )
    not_started = sum(
        1 for r in task_results.values()
        if r['status'] == 'NOT_STARTED'
    )
    
    print(f"   ✅ {completed} complétées")
    print(f"   🔄 {in_progress} en cours")
    print(f"   ⏸️  {not_started} pas démarrées")
    
    # Détail rapide
    for task_id, result in task_results.items():
        if result['status'] in ['COMPLETED', 'IN_PROGRESS']:
            task_names = {
                'human_architecture': '👤 Archi',
                'colab_training': '🎮 GPU',
                'autonomous_validation': '🤖 Valid',
                'autonomous_benchmarks': '🤖 Bench',
                'autonomous_metadata': '🤖 Meta'
            }
            name = task_names.get(task_id, task_id[:10])
            status_icon = '✅' if result['status'] == 'COMPLETED' else '🔄'
            print(f"   {status_icon} {name}: {result['completion_percent']}%")
    
    # Recommendation
    print(f"\n💡 Recommandation:")
    if percent >= 50:
        print(f"   🎉 Excellent rendement! Continue!")
    elif percent >= 37:
        print(f"   ✅ Target atteint! Phase 1 réussie")
    elif percent >= 20 and progress['remaining_minutes'] > 30:
        print(f"   🟡 Bon rythme, continuer travail")
    elif percent < 20 and progress['remaining_minutes'] < 30:
        print(f"   ⚠️  Accélérer ou accepter Phase 1 partielle")
    else:
        print(f"   🔵 Début normal, temps disponible")
    
    print(f"\n" + "="*50)
    print(f"\n📊 Détails: cat phase1_progress_report.json")
    print(f"🔍 Monitoring: tail -f phase1_monitoring.log\n")


if __name__ == '__main__':
    main()
