#!/bin/bash
# Phase 1 Auto-Monitor - Surveillance continue en arrière-plan
# Lance monitoring toutes les 5min pendant 2h

cd /home/stephane/GitHub/PaniniFS-Research

echo "🔍 Démarrage monitoring automatique Phase 1..."
echo "⏱️  Durée: 2h (checks toutes les 5min)"
echo "📊 Logs: phase1_monitoring.log"
echo ""

# 2h = 120min, check toutes les 5min = 24 iterations max
python3 phase1_monitor.py --interval 300 --iterations 24 >> phase1_monitoring.log 2>&1 &

MONITOR_PID=$!
echo "✅ Monitor lancé en arrière-plan (PID: $MONITOR_PID)"
echo "📝 Suivre logs: tail -f phase1_monitoring.log"
echo "⏹️  Arrêter: kill $MONITOR_PID"
echo ""
echo "💡 Commandes utiles:"
echo "   - Voir état actuel: python3 phase1_monitor.py --once"
echo "   - Voir logs live: tail -f phase1_monitoring.log"
echo "   - Voir rapport: cat phase1_progress_report.json"
echo ""
