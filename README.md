<!-- @format -->

# 🎤 FTNatlink - Dragon NaturallySpeaking Integration

A comprehensive Python framework for creating and managing Dragon NaturallySpeaking voice command grammars with modern addon support and development tools.

## ✨ Features

- **🐉 Dragon Integration**: Full Dragon NaturallySpeaking support with dragonfly2
- ** Grammar Management**: Load, unload, and reload voice command grammars
- **� DLL Build Tools**: Automated natlink DLL building and registration
- **🧪 Development Mode**: Test without Dragon using fake natlink runtime
- **🎨 Modern GUI**: Tabbed interface with emoji icons and activity logging
- **🌐 Multi-Language**: Support for French and English voice commands
- **📝 Notepad Integration**: Built-in example with French text insertion

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

3. **Install dependencies**
   
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup Dragon integration (optional)**
   
   For full Dragon NaturallySpeaking support:
   ```bash
   # Check system status and build requirements
   python build_natlink_dll.py --status
   
   # Build natlink DLL (requires CMake + Visual Studio)
   python build_natlink_dll.py
   ```

5. **Development mode (no Dragon required)**
   
   ```bash
   python develop_with_fake_runtime.py
   ```

### Launch the GUI

```bash
# GUI Application
python -m gui

# Development with fake runtime
python develop_with_fake_runtime.py

# Check Dragon integration status
python build_natlink_dll.py --status

# Build natlink DLL for Dragon
python build_natlink_dll.py
```

## 📂 Project Structure

```
FTNatlink/
├── __init__.py                     # Package entry point
├── build_natlink_dll.py           # 🔨 DLL build & registration tool
├── develop_with_fake_runtime.py   # 🧪 Development runtime (no Dragon)
├── requirements.txt               # 📦 Python dependencies
├── package_config.yaml           # ⚙️ Project configuration
├── core/                          # Core functionality
│   ├── __init__.py
│   ├── grammar_loader.py          # Grammar loading system
│   ├── fake_natlink_runtime.py    # Mock natlink for development
│   └── test_commands.py           # Test utilities
├── gui/                           # 🎨 GUI Application
│   ├── __init__.py                # GUI main() function
│   ├── app.py                     # Application class
│   ├── main_frame.py              # Main window
│   └── tabs/                      # Tab modules
│       ├── grammars_tab.py        # Grammar management
│       ├── addons_tab.py          # Addon installation
│       └── log_tab.py             # Activity logging
├── addon_manager/                 # 📦 Addon Management
│   ├── __init__.py
│   ├── addon_installer.py         # Addon installation
│   └── addon_packager.py          # Addon packaging
├── addons/                        # 🎤 Voice Command Addons
│   ├── notepad_addon/             # Example: Notepad control
│   │   ├── addon.json             # Addon metadata
│   │   ├── _global_mirror.py      # 🐉 Dragon grammar (dragonfly)
│   │   └── README.md
│   ├── sample_addon/              # Example: Sample commands
│   └── *.addon-natlink            # Packaged addons
├── grammars/                      # 📝 Grammar definitions
├── packages/                      # 📚 Local natlink packages
│   ├── natlink/                   # Core natlink
│   ├── natlinkcore/               # Natlink core  
│   ├── dtactions/                 # Dragon actions
│   └── dragonfly/                 # Dragonfly (Bayesian optimization)
├── tools/                         # 🔧 Utility tools
│   ├── dragon_natlink_diagnostic.py
│   ├── process_monitor.py
│   └── windows_speech.py
├── setup/                         # ⚡ Installation scripts
└── docs/                          # 📚 Documentation
```

## 🎯 Usage

### 🐉 Dragon Voice Commands (Production)

With Dragon NaturallySpeaking running:

```python
# The notepad addon provides these voice commands:
"melvin"                    # Opens Notepad with French text
"ouvre bloc note"          # French: Open Notepad  
"open notepad"             # English: Open Notepad
"lance bloc note"          # French: Launch Notepad
```

### 🧪 Development Mode (No Dragon)

Test grammars without Dragon:

```bash
python develop_with_fake_runtime.py
```

### 📋 Grammar Management (GUI)

1. Launch GUI: `python -m gui`
2. **Grammars** tab: Load/unload voice commands
3. **Log** tab: Monitor activity

### 🔨 Dragon Integration Setup

Check your system and build natlink DLL:

```bash
# Quick status check
python build_natlink_dll.py --status

# Interactive build process
python build_natlink_dll.py

# Help and options
python build_natlink_dll.py --help
```



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
- **[gui/README.md](gui/README.md)** - GUI architecture documentation

## 🔧 Technology Stack

- **Python 3.13**: Core language
- **wxPython**: GUI framework
- **dragonfly2**: Dragon speech recognition library
- **natlink**: Dragon NaturallySpeaking integration
- **natlinkcore**: Natlink core functionality
- **dtactions**: Dragon action commands

## 📋 Requirements

- Python 3.13+ (32-bit recommended for Dragon compatibility)
- wxPython 4.2.0+
- dragonfly2 0.35.0+
- natlink 5.5.8+
- Dragon NaturallySpeaking 16+ (for production use)
- CMake + Visual Studio (for DLL building)

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
