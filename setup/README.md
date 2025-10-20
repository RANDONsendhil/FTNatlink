# Setup Scripts

This folder contains installation and version management scripts for FTNatlink.

## Files

### `bootstrap_install.py`
Bootstrap installation script that handles the chicken-and-egg problem where manage_versions.py needs PyYAML to run but PyYAML isn't installed in fresh virtual environments.

**Usage:**
```bash
python setup/bootstrap_install.py
```

**What it does:**
- Checks if PyYAML is installed
- Installs PyYAML if missing
- Fixes pip if broken in fresh virtual environments
- Runs the main installation process via manage_versions.py

### `manage_versions.py`
Main package version management and installation automation script.

**Usage:**
```bash
# Complete installation using YAML configuration
python setup/manage_versions.py install-yaml

# Install specific dependency groups
python setup/manage_versions.py install-deps core
python setup/manage_versions.py install-deps development
python setup/manage_versions.py install-deps documentation

# Run installation test
python setup/manage_versions.py run-script test_installation

# Show version information
python setup/manage_versions.py show

# Export environment variables
python setup/manage_versions.py env
```

**Features:**
- Manages versions for natlink packages from package_config.yaml
- Provides environment variables and installation helpers
- Supports variable substitution in configuration
- Handles both editable and non-editable installations
- Automated dependency management

## Installation Process

### Quick Start (Recommended)
```bash
# From project root directory
python setup/bootstrap_install.py
```

### Manual Installation
```bash
# From project root directory
pip install pyyaml
python setup/manage_versions.py install-yaml
```

## Configuration

Both scripts read from `../package_config.yaml` (relative to the setup directory) which contains:
- Package versions
- Dependency groups
- Installation scripts
- Environment variables

## Notes

- Run all commands from the project root directory
- The scripts automatically handle path resolution
- Both scripts work together to provide a robust installation system
- `bootstrap_install.py` is the safest entry point for fresh environments