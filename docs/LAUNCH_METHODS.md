<!-- @format -->

# 🚀 Launch Methods Quick Reference

## Overview

FTNatlink can be launched in multiple ways to suit different use cases.

## Available Methods

### 1. Package Execution (Recommended)

```bash
# From parent directory
python -m FTNatlink

# Or from within FTNatlink directory
python __init__.py
```

**Use when:**

- Running the application normally
- Following Python best practices
- Working with the package as a whole
- Creating desktop shortcuts

**Benefits:**

- Standard Python package pattern
- Clean and professional
- Works from any directory

---

### 2. GUI Module Execution

```bash
# From FTNatlink directory
python -m gui
```

**Use when:**

- Running just the GUI component
- Testing GUI changes
- Developing GUI features
- Part of automated scripts

**Benefits:**

- Direct GUI module access
- Explicit about what's being executed
- Good for development

---

### 3. Programmatic Launch

```python
from gui import main
main()
```

**Use when:**

- Embedding in another Python script
- Creating custom launchers
- Adding initialization code
- Testing and development

**Example:**

```python
# custom_launcher.py
import logging
logging.basicConfig(level=logging.DEBUG)

from gui import main
main()
```

---

### 4. Direct App Instance

```python
from gui import NatlinkApp
import wx

app = NatlinkApp()
app.MainLoop()
```

**Use when:**

- Need fine control over wx.App lifecycle
- Creating custom app variants
- Advanced integration scenarios
- Testing specific app behaviors

**Example:**

```python
# test_app.py
from gui import NatlinkApp
import wx

# Create app but don't start immediately
app = NatlinkApp()

# Do custom initialization
# ...

# Start the app
app.MainLoop()
```

---

### 5. One-Liner Command

```bash
python -c "from gui import main; main()"
```

**Use when:**

- Quick testing
- Shell scripts
- Command-line automation
- Remote execution

---

### 6. With Addon Installation (Command Line)

```bash
python main.py path/to/addon.addon-natlink
```

**Use when:**

- Installing addon from command line
- Batch addon installation
- File association setup
- Double-click .addon-natlink files

**How it works:**

- Automatically installs the addon
- Loads all grammars
- Starts the GUI

---

## Desktop Shortcuts

### Windows

Create a `.bat` file:

```batch
@echo off
cd /d "F:\PROJECT_FT_NATLINK"
call FTNatlink\.venv\Scripts\activate
python -m FTNatlink
pause
```

Or PowerShell `.ps1`:

```powershell
Set-Location "F:\PROJECT_FT_NATLINK"
.\FTNatlink\.venv\Scripts\Activate.ps1
python -m FTNatlink
```

### Linux/Mac

Create a shell script:

```bash
#!/bin/bash
cd ~/PROJECT_FT_NATLINK
source FTNatlink/.venv/bin/activate
python -m FTNatlink
```

Make it executable:

```bash
chmod +x launch_ftnatlink.sh
./launch_ftnatlink.sh
```

---

## Development Shortcuts

### Test Grammar Loading

```python
python -c "from grammar_loader import load_grammars; load_grammars()"
```

### Package an Addon

```bash
python addon_packager.py addons/my_addon
```

### Test Commands Without GUI

```bash
python test_commands.py
```

---

## File Associations (Windows)

### Associate .addon-natlink files

1. Right-click a `.addon-natlink` file
2. Select "Open with" → "Choose another app"
3. Browse to `main.py` or create a `.bat` launcher
4. Check "Always use this app"

**Launcher script (`install_addon.bat`):**

```batch
@echo off
cd /d "F:\PROJECT_FT_NATLINK\FTNatlink"
call .venv\Scripts\activate
python main.py "%1"
```

---

## Advanced Integration

### Run in Background (No Console)

Create `main.pyw` (Windows):

```python
from gui import main
main()
```

Run with `pythonw`:

```bash
pythonw main.pyw
```

### System Tray Integration

```python
# system_tray_launcher.py
import wx
from gui import NatlinkApp

class TrayApp(NatlinkApp):
    def OnInit(self):
        # Add system tray icon
        # ...
        return super().OnInit()

if __name__ == "__main__":
    app = TrayApp()
    app.MainLoop()
```

---

## Troubleshooting

### GUI doesn't start

```bash
# Check Python version
python --version  # Should be 3.12+

# Check wxPython
python -c "import wx; print(wx.version())"

# Check imports
python -c "from gui import main; print('OK')"
```

### Module not found

```bash
# Ensure virtual environment is activated
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Reinstall dependencies
pip install -r requirements.txt
```

### Grammars not loading

```bash
# Check grammars folder
dir grammars  # Windows
ls grammars   # Linux/Mac

# Test grammar loader
python -c "from grammar_loader import list_grammars; print(list_grammars())"
```

---

## Comparison Table

| Method                 | Simplicity | Flexibility | Use Case     |
| ---------------------- | ---------- | ----------- | ------------ |
| `python -m FTNatlink`  | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐    | Daily use    |
| `python __init__.py`   | ⭐⭐⭐⭐⭐ | ⭐⭐⭐      | Quick launch |
| `python -m gui`        | ⭐⭐⭐⭐   | ⭐⭐⭐⭐    | Development  |
| `from gui import main` | ⭐⭐⭐     | ⭐⭐⭐⭐⭐  | Integration  |
| Direct app instance    | ⭐⭐       | ⭐⭐⭐⭐⭐  | Advanced     |
| One-liner              | ⭐⭐⭐⭐   | ⭐⭐        | Quick test   |
| With addon arg         | ⭐⭐⭐⭐   | ⭐⭐⭐⭐    | Installation |

---

## Best Practices

1. **For users**: Use `python -m FTNatlink` - it's professional and follows Python standards
2. **For developers**: Use `python -m gui` - direct GUI module access
3. **For scripts**: Import and call `main()` - most flexible
4. **For testing**: Use one-liners or direct instances - quick feedback
5. **For quick launch**: Use `python __init__.py` from within the directory

---

## Next Steps

- Set up desktop shortcut
- Configure file associations
- Create custom launcher scripts
- Test different launch methods

**See also:**

- [README.md](README.md) - Main documentation
- [gui/README.md](gui/README.md) - GUI architecture
- [PROJECT_SETUP.md](PROJECT_SETUP.md) - Setup guide
