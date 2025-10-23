@echo off
REM Build natlink DLL with proper Visual Studio environment

echo Setting up Visual Studio 2019 Build Tools environment...
call "C:\Program Files (x86)\Microsoft Visual Studio\2019\BuildTools\VC\Auxiliary\Build\vcvarsall.bat" x86

echo.
echo Building natlink DLL...
cd /d "%~dp0"
cd packages\natlink

if not exist build mkdir build
cd build

echo Running CMake...
cmake -G "Visual Studio 16 2019" -A Win32 -DPYTHON_EXECUTABLE="%~dp0.venv\Scripts\python.exe" ..

echo.
echo Building with MSBuild...
cmake --build . --config Release

echo.
echo Build complete!
echo Looking for _natlink_core.pyd...
dir /s /b _natlink_core.pyd

pause
