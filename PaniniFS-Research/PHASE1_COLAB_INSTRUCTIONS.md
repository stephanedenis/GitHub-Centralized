# 🎮 Colab Pro - Training GPU Dhātu Models

**Tâche**: `panini_4_gpu_dhatu_training`  
**Duration**: 1h  
**Priority**: P9 (CRITIQUE)  
**GPU**: T4 ou V100

---

## 🚀 Quick Start

### 1. Ouvrir Colab Pro

```
https://colab.research.google.com/
```

### 2. Activer GPU

- Runtime → Change runtime type → GPU (T4 ou V100)

### 3. Notebook Template

```python
# Dhātu GPU Training - Session 2025-10-01

import torch
import numpy as np
from datetime import datetime

# Vérifier GPU disponible
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f'Device: {device}')
if torch.cuda.is_available():
    print(f'GPU: {torch.cuda.get_device_name(0)}')

# TODO: Charger données dhātu
# TODO: Définir modèle
# TODO: Training loop
# TODO: Sauvegarder checkpoints
```

### 4. Monitoring

- Vérifier training curves
- Sauvegarder checkpoints réguliers (every 10 epochs)
- Noter métriques finales (accuracy, loss)

---

## 📊 Deliverables

- [ ] Modèles entraînés (checkpoints .pt)
- [ ] Training curves (loss/accuracy plots)
- [ ] Temps entraînement total
- [ ] Métriques finales (rapport JSON)

---

**Démarrer maintenant en arrière-plan** 🎮