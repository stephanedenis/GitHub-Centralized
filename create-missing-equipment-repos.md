# Create Missing Equipment Repositories on GitHub

## 🚀 Repositories to Create

### equipment-router
```bash
# 1. Create on GitHub: https://github.com/new
#    Repository name: equipment-router
#    Description: Router/Internet Box Management (192.168.0.1)
#    Visibility: Public

# 2. Push local repository:
cd /home/stephane/GitHub/equipment-router
git remote add origin git@github.com:stephanedenis/equipment-router.git
git branch -M main
git push -u origin main

# 3. Add as submodule (run after all repos are created):
cd /home/stephane/GitHub
git submodule add git@github.com:stephanedenis/equipment-router.git projects/equipment/equipment-router
```

### equipment-mystery
```bash
# 1. Create on GitHub: https://github.com/new
#    Repository name: equipment-mystery
#    Description: Mystery Device Investigation (192.168.0.104)
#    Visibility: Public

# 2. Push local repository:
cd /home/stephane/GitHub/equipment-mystery
git remote add origin git@github.com:stephanedenis/equipment-mystery.git
git branch -M main
git push -u origin main

# 3. Add as submodule (run after all repos are created):
cd /home/stephane/GitHub
git submodule add git@github.com:stephanedenis/equipment-mystery.git projects/equipment/equipment-mystery
```

## 🔗 Complete Equipment Setup

After creating all repositories, run:

```bash
cd /home/stephane/GitHub
python3 equipment-hauru/reorganize-equipment.py
```

This will add all equipment repositories as submodules in the centralized GitHub structure.
