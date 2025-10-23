# Installing ATL for Visual Studio 2019 Build Tools

## Why ATL is needed
The natlink C++ core requires ATL (Active Template Library) to compile. The error `'atlbase.h' : No such file or directory` indicates ATL is not installed.

## Installation Steps

### Method 1: Using Visual Studio Installer GUI

1. **Open Visual Studio Installer**
   - Search for "Visual Studio Installer" in Windows Start Menu
   - Or run: `"C:\Program Files (x86)\Microsoft Visual Studio\Installer\vs_installer.exe"`

2. **Modify Build Tools 2019**
   - Find "Visual Studio Build Tools 2019" in the list
   - Click the "Modify" button

3. **Install ATL Components**
   - Go to the **"Individual components"** tab
   - Search for "ATL" in the search box
   - Check these components:
     - ✅ **C++ ATL for latest v142 build tools (x86 & x64)**
     - ✅ **C++ MFC for latest v142 build tools (x86 & x64)** (optional but recommended)
   
4. **Apply Changes**
   - Click "Modify" button at bottom right
   - Wait for installation to complete (may take 5-10 minutes)

### Method 2: Using Command Line (Alternative)

Run PowerShell as Administrator and execute:

```powershell
# Path to Visual Studio Installer
$installerPath = "C:\Program Files (x86)\Microsoft Visual Studio\Installer\vs_installer.exe"

# Run installer to modify Build Tools with ATL component
& $installerPath modify --installPath "C:\Program Files (x86)\Microsoft Visual Studio\2019\BuildTools" --add Microsoft.VisualStudio.Component.VC.ATL --quiet --norestart
```

## After Installation

Once ATL is installed, rebuild natlink:

```powershell
Remove-Item -Path "packages\natlink\build" -Recurse -Force -ErrorAction SilentlyContinue
.\build_natlink.bat
```

## Verification

After building, check if the DLL was created:

```powershell
Get-ChildItem -Path "packages\natlink\build" -Recurse -Filter "_natlink_core*.pyd"
```

## What ATL Provides

- **atlbase.h**: Core ATL header with COM wrapper classes
- **COM Support**: Helper classes for Component Object Model
- **Windows Integration**: Required for Dragon NaturallySpeaking COM interface

## Alternative: Pre-built Binary

If you prefer not to install ATL, you could:
1. Use Python 3.11 or 3.12 (32-bit) which have pre-built natlink wheels
2. Download pre-built binaries from: https://github.com/dictation-toolbox/natlink/releases
3. Contact natlink maintainers for Python 3.13 32-bit builds
