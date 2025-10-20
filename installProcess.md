# 📦 FTNatlink Installation Process

Complete guide for installing and setting up FTNatlink with proper version management.

# FTNatlink Installation Process Guide

## 📋 Table of Contents

1. [🎯 Quick Start (YAML-Configured Installation)](#-quick-start-yaml-configured-installation)
2. [🔧 YAML-Based Installation System (NEW!)](#-yaml-based-installation-system-new)
3. [🎯 Quick Start (Original Method)](#-quick-start-original-method)
4. [📋 Detailed Installation Steps](#-detailed-installation-steps)
5. [🔍 Verification Checklist](#-verification-checklist)
6. [⚠️ Troubleshooting](#️-troubleshooting)
7. [📂 Project Structure](#-project-structure)

## 🎯 Quick Start (YAML-Configured Installation)

```bash
# 1. Clone and setup
git clone https://github.com/RANDONsendhil/FTNatlink.git
cd FTNatlink

# 2. Create virtual environment  
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# 3. Complete YAML-configured installation (NEW!)
python manage_versions.py install-yaml

# 4. Test GUI
python -m gui
```

## 🔧 YAML-Based Installation System (NEW!)

FTNatlink now supports a complete installation system driven by `package_config.yaml`:

### Configuration-Driven Installation

All installation settings are now in `package_config.yaml` (more readable than TOML):

```yaml
# Installation process configuration
installation:
  order: ["dtactions", "natlink", "natlinkcore"]  # Installation order
  editable: true
  upgrade: false

# Dependencies organized by category
dependencies:
  core:
    - "pyyaml>=6.0"
    - "wxPython>=4.2.0"
    - "pywin32>=311"
    # ... more dependencies
  
  development:
    - "pytest>=7.1.2"
    - "black"
    - "flake8"
    # ... more dev tools
  
  documentation:
    - "sphinx"
    - "sphinx-rtd-theme"

# Custom scripts for installation and testing
scripts:
  test_installation: |
    echo "Testing FTNatlink installation..."
    python -c "import yaml; import wx; print('✅ Core dependencies working')"
    # ... more tests
```

### YAML Installation Commands

```bash
# Complete installation process from YAML config
python manage_versions.py install-yaml

# Install specific dependency groups
python manage_versions.py install-deps core
python manage_versions.py install-deps development  
python manage_versions.py install-deps documentation

# Run custom installation scripts
python manage_versions.py run-script test_installation
python manage_versions.py run-script setup_venv
```

## 🎯 Quick Start (Original Method)

```bash
# 1. Clone and setup
git clone https://github.com/RANDONsendhil/FTNatlink.git
cd FTNatlink

# 2. Create virtual environment  
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# 3. Install dependencies
pip install -r requirements.txt

# 4. Install natlink packages with version management
python manage_versions.py install

# 5. Test GUI
python -m gui
```

## 📋 Detailed Installation Steps

### 1. Prerequisites

- **Python 3.10+** (recommended)
- **Windows OS** (for Dragon NaturallySpeaking support)
- **Git** for repository management
- **Dragon NaturallySpeaking** (optional, for production use)

### 2. Repository Setup

```bash
# Clone the repository
git clone https://github.com/RANDONsendhil/FTNatlink.git
cd FTNatlink

# Verify structure
ls -la
# Should show: gui/, core/, addons/, packages/, etc.
```

### 3. Virtual Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Activate (Linux/Mac)  
source .venv/bin/activate

# Verify activation
which python  # Should point to .venv
```

### 4. Core Dependencies

```bash
# Install core dependencies
pip install -r requirements.txt

# This installs:
# - toml (configuration management)
# - wxPython (GUI framework)
# - pywin32 (Windows APIs)
# - FreeSimpleGUI (additional GUI)
# - pydebugstring (debug utilities)
# - platformdirs (platform paths)
```

### 5. Natlink Packages (Version Managed)

The natlink packages use our custom version management system:

```bash
# Show current version configuration
python manage_versions.py show

# Install all natlink packages with proper versions
python manage_versions.py install

# Or install individual packages
python manage_versions.py install-package natlink
python manage_versions.py install-package natlinkcore  
python manage_versions.py install-package dtactions
```

**What this does:**
- Reads versions from `package_config.toml`
- Substitutes `${NATLINK_VERSION}` variables in pyproject.toml
- Creates temporary copies with real versions
- Installs in editable mode for development

### 6. Verification

```bash
# Test GUI launch
python -m gui

# Expected output:
# MockGrammar 'NotepadGrammar' initialized
# 📝 Notepad Grammar initialized
# ✅ Loaded grammar: notepad_grammar (notepad_addon)
# ...

# Test natlink import
python -c "import natlink; print('✅ Natlink imported successfully')"

# Test core functionality  
python -c "from core import grammar_loader; print('✅ Core modules working')"
```

## 🔧 Version Management

### Configuration File

Edit `package_config.toml` to manage versions:

```toml
[versions]
natlink = "5.5.8"
natlinkcore = "5.4.2" 
dtactions = "1.6.4"
# ... other dependencies
```

### Version Commands

```bash
# Show current versions
python manage_versions.py show

# Update packages after version change
python manage_versions.py install

# Export environment variables
python manage_versions.py env

# Install without editable mode
python manage_versions.py install --no-editable
```

## 🛠 Development Setup

### For Core FTNatlink Development

```bash
# Already done with main installation
pip install -r requirements.txt
python manage_versions.py install
```

### For Natlink Package Development

```bash
# Additional dev tools for each package
pip install -r packages/natlink/requirements-dev.txt
pip install -r packages/natlinkcore/requirements-dev.txt  
pip install -r packages/dtactions/requirements-dev.txt

# This adds: pytest, black, flake8, mypy, sphinx
```

## 🔍 Troubleshooting

### Common Issues

#### 1. Natlink Import Error (Dragon Not Running)
```
NameError: name 'natConnect' is not defined
```
**Solution:** This is expected when Dragon NaturallySpeaking is not running. FTNatlink automatically switches to mock mode for development/testing.
- ✅ For development: Continue using mock mode
- ✅ For production: Start Dragon NaturallySpeaking first

#### 2. Version Placeholder Error
```
InvalidVersion: Version number '${NATLINK_VERSION}' does not match PEP 440 rules
```
**Solution:** Use `python manage_versions.py install` instead of direct pip install.

#### 2. Missing Dependencies
```
ModuleNotFoundError: No module named 'natlink'
```
**Solution:** Run `python manage_versions.py install` to install natlink packages.

#### 3. GUI Import Error
```
ModuleNotFoundError: No module named 'wx._core'
```
**Solution:** Reinstall wxPython: `pip install --force-reinstall wxPython`

#### 4. pywin32 Bootstrap Error
```
No module named 'pywin32_bootstrap'
```
**Solution:** This is usually harmless, but you can fix with:
```bash
python -c "import pywin32_system32"  # Test if working
# If fails, reinstall: pip install --force-reinstall pywin32
```

### Debug Steps

```bash
# 1. Check Python version
python --version  # Should be 3.10+

# 2. Check virtual environment
which python      # Should point to .venv

# 3. List installed packages
pip list | findstr natlink

# 4. Check package versions
python manage_versions.py show

# 5. Test imports individually
python -c "import natlink"
python -c "import natlinkcore" 
python -c "import dtactions"
python -c "import wx"
```

## 📁 Project Structure

```
FTNatlink/
├── 📋 requirements.txt              # Core dependencies
├── ⚙️ package_config.toml          # Version configuration
├── 🔧 manage_versions.py           # Version management script
├── 🎨 gui/                         # GUI application
├── 🔧 core/                        # Core functionality
├── 📦 addons/                      # Voice command addons
├── 📚 packages/                    # Local natlink packages
│   ├── natlink/
│   │   ├── pythonsrc/
│   │   │   └── pyproject.toml      # Uses ${NATLINK_VERSION}
│   │   └── requirements-dev.txt    # Dev dependencies
│   ├── natlinkcore/
│   │   ├── pyproject.toml          # Uses ${NATLINKCORE_VERSION}  
│   │   └── requirements-dev.txt
│   └── dtactions/
│       ├── pyproject.toml          # Uses ${DTACTIONS_VERSION}
│       └── requirements-dev.txt
└── 📖 docs/                        # Documentation
```

## 🚀 Production Deployment

### For Dragon NaturallySpeaking Use

1. **Install Dragon** NaturallySpeaking (version 13+)
2. **Follow standard installation** above
3. **Test with Dragon:**
   ```bash
   # With Dragon running
   python -c "import natlink; print(natlink.isNatSpeakRunning())"
   ```

### For Development/Testing Only

- Uses mock natlink runtime (`core/fake_natlink_runtime.py`)
- No Dragon required
- Perfect for GUI development and testing

## 📊 Installation Verification Checklist

- [ ] Python 3.10+ installed
- [ ] Virtual environment created and activated
- [ ] Core dependencies installed (`pip install -r requirements.txt`)
- [ ] Natlink packages installed (`python manage_versions.py install`)
- [ ] GUI launches successfully (`python -m gui`)
- [ ] Core application runs (`python __init__.py`)
- [ ] No import errors for natlink, natlinkcore, dtactions
- [ ] Version management working (`python manage_versions.py show`)

### Expected Runtime Behavior

**With Dragon NaturallySpeaking running:**
- ✅ Full natlink functionality available
- ✅ Real voice recognition active

**Without Dragon NaturallySpeaking:**
- ⚠️ Mock natlink runtime activates automatically
- ⚠️ Message: "Natlink not available, using mock implementation"
- ✅ GUI and development features still work
- ✅ Grammar loading simulation works for testing

## 🆘 Getting Help

1. **Check this document** for common issues
2. **Run verification commands** above
3. **Check logs** in the GUI application
4. **Verify versions** with `python manage_versions.py show`
5. **Test individual components** before full integration

## 🔄 Updating

### Update Dependencies
```bash
pip install --upgrade -r requirements.txt
```

### Update Natlink Packages
```bash
# Pull latest from git repositories
cd packages/natlink && git pull && cd ../..
cd packages/natlinkcore && git pull && cd ../..  
cd packages/dtactions && git pull && cd ../..

# Reinstall with version management
python manage_versions.py install
```

### Update Versions
```bash
# Edit package_config.toml with new versions
# Then reinstall
python manage_versions.py install
```

## ✅ Current Setup Status

Your FTNatlink project is now properly configured with:

### 📁 **Updated Files:**
- ✅ `requirements.txt` - Core dependencies with version management integration
- ✅ `package_config.toml` - Centralized version configuration
- ✅ `manage_versions.py` - Advanced version management script
- ✅ `packages/*/requirements-dev.txt` - Development dependencies for each package
- ✅ `installProcess.md` - This comprehensive installation guide

### 🛠 **Installation System:**
1. **Virtual Environment**: `.venv` properly configured
2. **Core Dependencies**: Managed via `requirements.txt`
3. **Natlink Packages**: Managed via `manage_versions.py` with variable substitution
4. **Development Tools**: Available per package via `requirements-dev.txt`

### 🎯 **Ready Commands:**
```bash
# Install core dependencies
pip install -r requirements.txt

# Install natlink packages with version management  
python manage_versions.py install

# Launch GUI application
python -m gui

# Show version configuration
python manage_versions.py show
```

---

## 📝 Notes

- **Always use version management** for natlink packages
- **Regular pip install** only handles core dependencies  
- **Editable installs** allow live development
- **Mock runtime** enables development without Dragon
- **Configuration driven** version management prevents hardcoded versions

Happy coding! 🎉