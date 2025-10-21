@echo off
echo 🚀 Building FTNatlink.exe...
echo ================================

REM Clean previous build
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "FTNatlink.spec" del "FTNatlink.spec"

REM Build executable
python build_exe.py

echo.
echo ✅ Build complete!
echo 📁 Executable location: dist\FTNatlink.exe
echo.
pause