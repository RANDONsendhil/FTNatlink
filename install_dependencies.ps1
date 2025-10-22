# Script PowerShell pour installer les dépendances FTNatlink
Write-Host "📦 Installation des dépendances FTNatlink..." -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green

# Vérifier si l'environnement virtuel existe
if (-not (Test-Path ".venv\Scripts\python.exe")) {
    Write-Host "❌ Erreur: Environnement virtuel .venv non trouvé!" -ForegroundColor Red
    Write-Host "Création de l'environnement virtuel..." -ForegroundColor Yellow
    
    python -m venv .venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Échec de création de l'environnement virtuel" -ForegroundColor Red
        pause
        exit 1
    }
    Write-Host "✅ Environnement virtuel créé avec succès" -ForegroundColor Green
}

# Activer l'environnement virtuel
Write-Host "Activation de l'environnement virtuel..." -ForegroundColor Cyan
& .\.venv\Scripts\Activate.ps1

# Mettre à jour pip
Write-Host "Mise à jour de pip..." -ForegroundColor Cyan
& .\.venv\Scripts\python -m pip install --upgrade pip

# Installer les dépendances
Write-Host "Installation des dépendances depuis requirements.txt..." -ForegroundColor Cyan
& .\.venv\Scripts\python -m pip install -r requirements.txt

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Erreur lors de l'installation des dépendances" -ForegroundColor Red
    pause
    exit 1
}

# Installer les packages natlink
Write-Host "Installation des packages natlink..." -ForegroundColor Cyan
& .\.venv\Scripts\python setup/manage_versions.py install

Write-Host ""
Write-Host "✅ Installation terminée !" -ForegroundColor Green
Write-Host "🚀 Pour lancer l'application : .venv\Scripts\python -m gui" -ForegroundColor Green
Write-Host "🔨 Pour construire l'exécutable : .\build_exe.ps1" -ForegroundColor Green
Write-Host ""
pause