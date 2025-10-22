@echo off
echo 📦 Installation des dépendances FTNatlink...
echo ============================================

REM Vérifier si l'environnement virtuel existe
if not exist ".venv\Scripts\python.exe" (
    echo ❌ Erreur: Environnement virtuel .venv non trouvé!
    echo Création de l'environnement virtuel...
    python -m venv .venv
    if errorlevel 1 (
        echo ❌ Échec de création de l'environnement virtuel
        pause
        exit /b 1
    )
    echo ✅ Environnement virtuel créé avec succès
)

REM Activer l'environnement virtuel
echo Activation de l'environnement virtuel...
call .venv\Scripts\activate.bat

REM Mettre à jour pip
echo Mise à jour de pip...
.venv\Scripts\python -m pip install --upgrade pip

REM Installer les dépendances
echo Installation des dépendances depuis requirements.txt...
.venv\Scripts\python -m pip install -r requirements.txt

if errorlevel 1 (
    echo ❌ Erreur lors de l'installation des dépendances
    pause
    exit /b 1
)

REM Installer les packages natlink
echo Installation des packages natlink...
.venv\Scripts\python setup/manage_versions.py install

echo.
echo ✅ Installation terminée !
echo 🚀 Pour lancer l'application : .venv\Scripts\python -m gui
echo 🔨 Pour construire l'exécutable : build_exe.bat
echo.
pause