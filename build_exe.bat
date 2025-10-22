@echo off
echo 🚀 Building FTNatlink.exe...
echo ================================

REM Vérifier si l'environnement virtuel existe
if not exist ".venv\Scripts\python.exe" (
    echo ❌ Erreur: Environnement virtuel .venv non trouvé!
    echo Veuillez créer l'environnement virtuel avec: python -m venv .venv
    pause
    exit /b 1
)

REM Activer l'environnement virtuel et construire
echo Utilisation de l'environnement virtuel local...
call .venv\Scripts\activate.bat

REM Clean previous build
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "FTNatlink.spec" del "FTNatlink.spec"

REM Build executable avec l'environnement virtuel
echo Construction de l'exécutable...
.venv\Scripts\python build_exe.py

echo.
echo ✅ Build complete!
echo 📁 Executable location: dist\FTNatlink.exe
echo.
pause