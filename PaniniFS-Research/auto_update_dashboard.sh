#!/bin/bash
# Auto-update Phase 1 progress report to GitHub
# Lance en arrière-plan, push toutes les 5min

cd /home/stephane/GitHub/PaniniFS-Research

echo "🔄 Démarrage auto-updater GitHub Pages..."
echo "📊 Push phase1_progress_report.json toutes les 5min"
echo ""

# Fonction push
push_report() {
    # Check si fichier modifié
    if git diff --quiet phase1_progress_report.json; then
        echo "[$(date '+%H:%M:%S')] Pas de changement"
        return
    fi
    
    echo "[$(date '+%H:%M:%S')] 📤 Push nouveau rapport..."
    
    git add phase1_progress_report.json
    git commit -m "📊 Update Phase 1 progress - $(date '+%Y-%m-%d %H:%M UTC')" --quiet
    git push origin main --quiet 2>&1 | head -3
    
    echo "[$(date '+%H:%M:%S')] ✅ Rapport poussé"
}

# Loop 24 iterations (2h, toutes les 5min)
for i in {1..24}; do
    push_report
    
    if [ $i -lt 24 ]; then
        echo "[$(date '+%H:%M:%S')] ⏳ Prochain push dans 5min..."
        sleep 300
    fi
done

echo ""
echo "✅ Auto-updater terminé (2h complétées)"
