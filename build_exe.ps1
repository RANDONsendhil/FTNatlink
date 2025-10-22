# Script PowerShell pour construire FTNatlink.exe avec l'environnement virtuel local
Write-Host "🚀 Building FTNatlink.exe..." -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green

# Vérifier si l'environnement virtuel existe
if (-not (Test-Path ".venv\Scripts\Activate.ps1")) {
    Write-Host "❌ Erreur: Environnement virtuel .venv non trouvé!" -ForegroundColor Red
    Write-Host "Veuillez créer l'environnement virtuel avec: python -m venv .venv" -ForegroundColor Yellow
    pause
    exit 1
}

# Activer l'environnement virtuel
Write-Host "Activation de l'environnement virtuel..." -ForegroundColor Cyan
& .\.venv\Scripts\Activate.ps1

# Nettoyer les builds précédents
Write-Host "Nettoyage des builds précédents..." -ForegroundColor Cyan
if (Test-Path "build") { Remove-Item -Recurse -Force "build" }
if (Test-Path "dist") { Remove-Item -Recurse -Force "dist" }
if (Test-Path "FTNatlink.spec") { Remove-Item -Force "FTNatlink.spec" }

# Construire l'exécutable
Write-Host "Construction de l'exécutable..." -ForegroundColor Cyan
python build_exe.py

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ Build complete!" -ForegroundColor Green
    Write-Host "📁 Executable location: dist\FTNatlink.exe" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "❌ Build failed!" -ForegroundColor Red
}

Write-Host ""
pause