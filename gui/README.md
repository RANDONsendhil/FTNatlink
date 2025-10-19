<!-- @format -->

# 🎨 GUI Module Documentation

## 📂 Structure

```
gui/
├── __init__.py          # Main entry point - contains main() function
├── __main__.py          # Module execution entry point (python -m gui)
├── app.py               # Application class (NatlinkApp)
├── main_frame.py        # Main window frame (GrammarManagerFrame)
└── tabs/
    ├── __init__.py      # Tab module exports
    ├── grammars_tab.py  # Grammars management tab with split-view
    ├── addons_tab.py    # Addon installation tab
    └── log_tab.py       # Activity log tab
```

## 🚀 Usage

### Launch the GUI

**Method 1: Via main.py (Recommended)**

```bash
python main.py
```

**Method 2: As a Python module**

```bash
python -m gui
```

**Method 3: Programmatically**

```python
from gui import main
main()
```

**Method 4: Direct app instance**

```python
from gui import NatlinkApp
import wx
app = NatlinkApp()
app.MainLoop()
```

## 📋 Module Overview

### `__init__.py`

- **Purpose**: Entry point for the GUI module
- **Exports**: `main()`, `NatlinkApp`
- **Function**: `main()` - Launches the application

### `app.py`

- **Purpose**: Main application class
- **Class**: `NatlinkApp(wx.App)`
- **Features**:
  - Handles command-line arguments for addon installation
  - Loads all grammars on startup
  - Creates and displays main frame

### `main_frame.py`

- **Purpose**: Main window container
- **Class**: `GrammarManagerFrame(wx.Frame)`
- **Features**:
  - Creates tabbed interface with wx.Notebook
  - Manages tabs (Grammars, Addons, Log)
  - Provides `log_msg()` method for logging

### `tabs/grammars_tab.py`

- **Purpose**: Grammar management interface
- **Function**: `create_grammars_tab(parent, frame)`
- **Features**:
  - Split-view layout (list + details)
  - Grammar list with emoji icons
  - Detailed grammar information display
  - Addon metadata integration
  - Buttons: Refresh, Load All, Reload All, Unload All
- **Event Handlers**:
  - `on_grammar_selected(event, frame)` - Display grammar details
  - `on_list(event, frame)` - Refresh grammar list
  - `on_load(event, frame)` - Load all grammars
  - `on_reload(event, frame)` - Reload all grammars
  - `on_unload(event, frame)` - Unload all grammars

### `tabs/addons_tab.py`

- **Purpose**: Addon installation interface
- **Function**: `create_addons_tab(parent, frame)`
- **Features**:
  - File browser for .addon-natlink files
  - Installation with progress feedback
  - Automatic grammar reload after installation
- **Event Handlers**:
  - `on_install(event, frame)` - Open file dialog and install addon

### `tabs/log_tab.py`

- **Purpose**: Activity logging interface
- **Function**: `create_log_tab(parent, frame)`
- **Features**:
  - Multiline readonly text display
  - Clear button to reset log
  - Auto-scroll to bottom

## 🔧 Architecture

### Tab Creation Pattern

Each tab follows this pattern:

```python
def create_<tab_name>_tab(parent, frame):
    """Create the tab panel"""
    panel = wx.Panel(parent)

    # Create widgets
    # ...

    # Bind events with frame reference
    button.Bind(wx.EVT_BUTTON, lambda e: on_<action>(e, frame))

    # Layout
    sizer = wx.BoxSizer(wx.VERTICAL)
    # ...
    panel.SetSizer(sizer)

    return panel

def on_<action>(event, frame):
    """Event handler with frame reference"""
    # Access frame methods/attributes
    frame.log_msg("Action performed")
```

### Event Handling

Events are handled by standalone functions that receive the `frame` parameter, allowing them to:

- Access frame attributes (e.g., `frame.grammar_list`)
- Call frame methods (e.g., `frame.log_msg()`)
- Update UI components

### Communication Between Modules

- **Frame → Tabs**: Frame instance passed to tab creation functions
- **Tabs → Frame**: Event handlers receive frame reference
- **Tabs → Core**: Import functions from parent modules (grammar_loader, addon_installer)

## 📊 Data Flow

```
main.py
  ↓
gui/__init__.py::main()
  ↓
gui/app.py::NatlinkApp
  ↓ (creates)
gui/main_frame.py::GrammarManagerFrame
  ↓ (creates tabs)
gui/tabs/*_tab.py::create_*_tab()
  ↓ (user interaction)
Event Handlers → Core Functions
  ↓
grammar_loader.py / addon_installer.py
```

## 🎯 Design Principles

1. **Separation of Concerns**: GUI code separated from business logic
2. **Modularity**: Each tab is a separate module
3. **Reusability**: Tab functions can be used independently
4. **Maintainability**: Clear structure makes updates easier
5. **Testability**: Core logic can be tested without GUI

## 🔄 Future Enhancements

Potential improvements:

- [ ] Move event handlers into class methods for better encapsulation
- [ ] Create base tab class for common functionality
- [ ] Add configuration dialog
- [ ] Implement drag-and-drop for addon installation
- [ ] Add grammar editor functionality
- [ ] Create syntax highlighting for grammar code
- [ ] Add search/filter for grammar list
- [ ] Implement keyboard shortcuts

## 📝 Notes

- All tab creation functions return a `wx.Panel` instance
- Frame reference is passed to enable cross-tab communication
- Path handling uses `pathlib.Path` for cross-platform compatibility
- Emojis used for visual enhancement (📋 📦 📄 etc.)
