#!/bin/bash
# Deploy Phase 1 Dashboard to GitHub Pages

cd /home/stephane/GitHub/PaniniFS-Research

echo "🌐 Déploiement Dashboard Phase 1 vers GitHub Pages..."
echo ""

# Vérifier que docs/ existe
if [ ! -d "docs" ]; then
    echo "❌ Dossier docs/ introuvable"
    exit 1
fi

# Vérifier dashboard
if [ ! -f "docs/phase1_dashboard.html" ]; then
    echo "❌ Dashboard introuvable: docs/phase1_dashboard.html"
    exit 1
fi

# Créer index.html redirect si besoin
if [ ! -f "docs/index.html" ]; then
    echo "📝 Création index.html redirect..."
    cat > docs/index.html << 'EOF'
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="0; url=phase1_dashboard.html">
    <title>Phase 1 Dashboard - Redirect</title>
</head>
<body>
    <p>Redirection vers <a href="phase1_dashboard.html">Phase 1 Dashboard</a>...</p>
</body>
</html>
EOF
fi

# Commit
echo "💾 Commit dashboard..."
git add docs/phase1_dashboard.html docs/index.html phase1_progress_report.json

git commit -m "🌐 Deploy Phase 1 Dashboard - GitHub Pages

Dashboard web monitoring temps réel:
- Interface responsive moderne
- Auto-refresh 30s
- Progression pondérée visuelle
- Détail 5 tâches avec status
- Stats temps écoulé/restant

URL (après activation GitHub Pages):
https://stephanedenis.github.io/GitHub-Centralized/PaniniFS-Research/docs/phase1_dashboard.html

Features:
- 📊 Barre progression animée
- 🚦 Status badges (STARTING/ACCEPTABLE/ON_TRACK/AT_RISK)
- ✅ Detection automatique completion
- 🔄 Auto-refresh 30s
- 📱 Mobile responsive

Data source: phase1_progress_report.json (via raw.githubusercontent.com)"

# Push
echo "📤 Push vers GitHub..."
git push origin main

echo ""
echo "✅ Dashboard déployé!"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📋 PROCHAINES ÉTAPES:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "1. Activer GitHub Pages (si pas déjà fait):"
echo "   → https://github.com/stephanedenis/GitHub-Centralized/settings/pages"
echo "   → Source: Deploy from a branch"
echo "   → Branch: main"
echo "   → Folder: /docs"
echo "   → Save"
echo ""
echo "2. Attendre déploiement (1-2min)"
echo ""
echo "3. Accéder dashboard:"
echo "   → https://stephanedenis.github.io/GitHub-Centralized/PaniniFS-Research/docs/phase1_dashboard.html"
echo ""
echo "4. Pour que dashboard fonctionne:"
echo "   → Commit régulier phase1_progress_report.json"
echo "   → Monitoring auto fait déjà ça toutes les 5min"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "💡 Tips:"
echo "   - Dashboard se refresh auto toutes les 30s"
echo "   - Données via raw.githubusercontent.com"
echo "   - Fonctionne sur mobile/tablet/desktop"
echo ""
