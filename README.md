<!-- @format -->

# 🎤 FTNatlink - Natlink Grammar Manager

A modern GUI application for managing Dragon NaturallySpeaking voice command grammars with addon support.

## ✨ Features

- **📋 Grammar Management**: Load, unload, and reload voice command grammars
- **📦 Addon System**: Install and package voice command addons
- **🔍 Split-View Interface**: View detailed grammar information including metadata
- **📊 Activity Logging**: Track all operations and events
- **🎨 Modern UI**: Tabbed interface with emoji icons
- **🧪 Development Mode**: Test without Dragon using mock natlink runtime

## 🚀 Quick Start

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/RANDONsendhil/FTNatlink.git
   cd FTNatlink
   ```

2. **Create virtual environment**

   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   ```

3. **Install dependencies and packages**
   
   **Recommended (handles all dependencies and natlink packages):**
   ```bash
   python setup/bootstrap_install.py
   ```
   
   **Alternative (manual installation):**
   ```bash
   pip install -r requirements.txt
   python setup/manage_versions.py install-yaml
   ```

### Launch the GUI

Multiple ways to run the application:

```bash
# Method 1: As Python package (recommended)
python -m FTNatlink

# Method 2: From package directory
cd FTNatlink
python __init__.py

# Method 3: Run gui module directly
python -m gui

# Method 4: Direct Python import
python -c "from gui import main; main()"

# Method 5: Legacy (if main.py still exists)
python main.py
```

## 📂 Project Structure

```
FTNatlink/
├── __init__.py                  # Package entry point (replaces main.py)
├── __main__.py                  # Module execution entry point
├── core/                        # Core functionality module
│   ├── __init__.py             # Core module exports
│   ├── grammar_loader.py       # Grammar loading system
│   ├── fake_natlink_runtime.py # Natlink mock for development
│   └── test_commands.py        # Test utilities
├── gui/                         # GUI module (refactored)
│   ├── __init__.py             # GUI main() function
│   ├── __main__.py             # GUI module execution
│   ├── app.py                  # Application class
│   ├── main_frame.py           # Main window frame
│   ├── README.md               # GUI documentation
│   └── tabs/                   # Tab modules
│       ├── grammars_tab.py     # Grammar management
│       ├── addons_tab.py       # Addon installation
│       └── log_tab.py          # Activity log
├── addon_manager/              # Addon management module
│   ├── __init__.py            # Module exports
│   ├── addon_installer.py     # Addon installation
│   ├── addon_packager.py      # Addon packaging
│   └── README.md              # Addon manager docs
├── addon_packager.py           # Convenience script (wrapper)
├── grammar_loader.py           # Grammar loading system
├── fake_natlink_runtime.py     # Mock natlink for development
├── test_commands.py            # Test voice commands
├── windows_speech.py           # Windows Speech Recognition
├── grammars/                   # Voice command grammars
│   ├── notepad_grammar.py      # Example: Notepad control
│   └── sample_grammar.py       # Example: Sample commands
├── addons/                     # Addon source folders
│   ├── notepad_addon/          # Example addon
│   │   ├── addon.json          # Addon metadata
│   │   ├── notepad_grammar.py  # Grammar file
│   │   └── README.md
│   └── *.addon-natlink         # Packaged addons
├── packages/                   # Local natlink packages
│   ├── natlink/                # Core natlink
│   ├── natlinkcore/            # Natlink core
│   └── dtactions/              # Dragon actions
└── docs/                       # Documentation
    ├── PROJECT_SETUP.md
    ├── ADDON_INSTALL_GUIDE.md
    └── GUI_TAB_GUIDE.md
```

## 🎯 Usage

### Grammar Management

1. Open the **Grammars** tab
2. Click **📋 Refresh** to list available grammars
3. Click any grammar to view details
4. Click **⬇️ Load All** to activate grammars

### Addon Installation

1. Open the **Addons** tab
2. Click **📦 Install Addon from File**
3. Select a `.addon-natlink` file
4. Grammars are automatically reloaded

### Create Your Own Addon

```bash
python addon_packager.py addons/your_addon
```

See [ADDON_INSTALL_GUIDE.md](ADDON_INSTALL_GUIDE.md) for details.

## 🛠️ Development

### Running Tests

```bash
python test_commands.py
```

### Mock Natlink Runtime

For development without Dragon:

```python
import fake_natlink_runtime
from grammar_loader import load_grammars

load_grammars()  # Loads with mock natlink
```

### Grammar Development

Create a new grammar in `grammars/`:

```python
from fake_natlink_runtime import MockGrammar

class MyGrammar(MockGrammar):
    def __init__(self):
        super().__init__("MyGrammar")
        self.commands = {
            "open browser": self.open_browser,
        }

    def gotResults(self, words):
        command = " ".join(words)
        if command in self.commands:
            self.commands[command]()

    def open_browser(self):
        print("Opening browser...")

grammar = MyGrammar()
grammar.load()
```

## 📚 Documentation

- **[PROJECT_SETUP.md](PROJECT_SETUP.md)** - Complete setup guide
- **[GUI_TAB_GUIDE.md](GUI_TAB_GUIDE.md)** - GUI usage instructions
- **[ADDON_INSTALL_GUIDE.md](ADDON_INSTALL_GUIDE.md)** - Addon creation and installation
- **[gui/README.md](gui/README.md)** - GUI architecture documentation

## 🔧 Technology Stack

- **Python 3.12**: Core language
- **wxPython**: GUI framework
- **natlink**: Dragon NaturallySpeaking integration
- **natlinkcore**: Natlink core functionality
- **dtactions**: Dragon action commands

## 📋 Requirements

- Python 3.12+
- wxPython 4.2.0+
- natlink 5.5.8+
- Dragon NaturallySpeaking (for production use)

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

See LICENSE file for details.

## 👤 Author

**Sendhil RANDON**

## 🙏 Acknowledgments

- Dragon NaturallySpeaking team
- Natlink community
- wxPython developers
