# 🛠️ Scripts de Développement FTNatlink

Ce dossier contient des scripts pour faciliter le développement et la construction de FTNatlink.

## 📦 Installation des Dépendances

### Windows Batch
```cmd
install_dependencies.bat
```

### PowerShell  
```powershell
.\install_dependencies.ps1
```

Ces scripts :
- Créent l'environnement virtuel `.venv` si nécessaire
- Installent toutes les dépendances depuis `requirements.txt`
- Installent les packages natlink via `setup/manage_versions.py`

## 🔨 Construction de l'Exécutable

### Windows Batch
```cmd
build_exe.bat
```

### PowerShell
```powershell
.\build_exe.ps1
```

Ces scripts :
- Utilisent automatiquement l'environnement virtuel local
- Nettoient les builds précédents
- Construisent `FTNatlink.exe` dans le dossier `dist/`

## 🚀 Lancement de l'Application

### Mode Développement
```cmd
.venv\Scripts\python -m gui
```

### Avec Addon
```cmd
.venv\Scripts\python -m gui addons/mon_addon.natlink-addon
```

## 📂 Structure des Environnements

```
FTNatlink/
├── .venv/                     # Environnement virtuel local
├── requirements.txt           # Dépendances Python
├── install_dependencies.*     # Scripts d'installation
├── build_exe.*               # Scripts de construction
└── dist/                     # Exécutables compilés
    └── FTNatlink.exe
```

## ✅ Avantages de cette Approche

- **Isolation** : Chaque projet a ses propres dépendances
- **Reproductibilité** : Versions exactes dans `requirements.txt`
- **Simplicité** : Un script pour installer, un pour construire
- **Stabilité** : Pas de conflits avec l'installation Python globale

## 🔧 Dépannage

### Erreur d'environnement virtuel
```cmd
# Supprimer et recréer l'environnement
rmdir /s .venv
python -m venv .venv
.\install_dependencies.bat
```

### Erreur de construction
```cmd
# Nettoyer et recommencer
rmdir /s build dist
del FTNatlink.spec
.\build_exe.bat
```