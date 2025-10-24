# PowerShell script to launch FTNatlink with virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Green
& .\.venv\Scripts\Activate.ps1
Write-Host "Running FTNatlink with 32-bit Python..." -ForegroundColor Green
python __init__.py
Write-Host "Press any key to continue..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")