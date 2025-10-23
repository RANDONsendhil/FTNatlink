# Script to help install ATL for Visual Studio 2019 Build Tools

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "ATL Installation Helper for VS 2019" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Visual Studio Installer exists
$installerPath = "C:\Program Files (x86)\Microsoft Visual Studio\Installer\vs_installer.exe"

if (Test-Path $installerPath) {
    Write-Host "Visual Studio Installer found" -ForegroundColor Green
    Write-Host ""
    Write-Host "Opening Visual Studio Installer..." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "STEPS TO FOLLOW:" -ForegroundColor Cyan
    Write-Host "1. Find 'Visual Studio Build Tools 2019' in the list" -ForegroundColor White
    Write-Host "2. Click the 'Modify' button" -ForegroundColor White
    Write-Host "3. Go to 'Individual components' tab" -ForegroundColor White
    Write-Host "4. Search for 'ATL'" -ForegroundColor White
    Write-Host "5. Check: 'C++ ATL for latest v142 build tools (x86 & x64)'" -ForegroundColor White
    Write-Host "6. Click 'Modify' to install" -ForegroundColor White
    Write-Host ""
    Write-Host "Press any key to open the installer..." -ForegroundColor Yellow
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    
    # Launch Visual Studio Installer
    Start-Process $installerPath
    
    Write-Host ""
    Write-Host "After installing ATL, run this command to rebuild natlink:" -ForegroundColor Green
    Write-Host "  Remove-Item packages\natlink\build -Recurse -Force; .\build_natlink.bat" -ForegroundColor Yellow
    Write-Host ""
    
} else {
    Write-Host "Visual Studio Installer not found at:" -ForegroundColor Red
    Write-Host "  $installerPath" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please download and install Visual Studio Build Tools 2019 from:" -ForegroundColor Yellow
    Write-Host "  https://visualstudio.microsoft.com/downloads/" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "For detailed instructions, see: install_atl.md" -ForegroundColor Cyan
