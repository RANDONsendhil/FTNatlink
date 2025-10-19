<!-- @format -->

# 🎯 Natlink Development Environment - Complete Setup

## 📁 Project Structure

```
FTNatlink/
├── .venv/                          # Python virtual environment
├── packages/                       # Natlink core packages (editable installs)
│   ├── dtactions/
│   ├── natlink/
│   └── natlinkcore/
├── addons/                         # Addon source folders
│   ├── notepad_addon/             # Notepad control addon
│   │   ├── addon.json
│   │   ├── notepad_grammar.py
│   │   └── README.md
│   ├── sample_addon/              # Sample testing addon
│   │   ├── addon.json
│   │   ├── sample_grammar.py
│   │   └── addon.json
│   └── README.md                  # Addons documentation
├── grammars/                      # Active grammar files
│   ├── notepad_grammar.py
│   └── sample_grammar.py
├── installed_addons/              # Installed addon packages
├── main.py                        # Main GUI application
├── addon_packager.py              # Package addons into .addon-natlink
├── addon_installer.py             # Install .addon-natlink packages
├── grammar_loader.py              # Load/unload grammars
├── fake_natlink_runtime.py        # Mock natlink for testing
├── test_commands.py               # Test voice commands
├── windows_speech.py              # Windows speech recognition
└── requirements.txt               # Python dependencies

```

## 🚀 Quick Start

### 1. Activate Virtual Environment

```powershell
.venv\Scripts\activate
```

### 2. Run the GUI

```powershell
python main.py
```

### 3. Test Commands

```powershell
python test_commands.py
```

## 📦 Working with Addons

### Create an Addon

1. Create folder in `addons/`
2. Add `addon.json` with metadata
3. Create your grammar `.py` files
4. Add documentation in `README.md`

### Package an Addon

```powershell
python addon_packager.py addons/your_addon
```

### Install an Addon

```powershell
# Method 1: Via GUI
python main.py
# Then use the GUI to install

# Method 2: Command line
python main.py path/to/addon.addon-natlink
```

## 🎤 Available Voice Commands

### Notepad Addon

- "open notepad"
- "launch notepad"
- "start notepad"

### Sample Addon

- "hello" - Test greeting
- "test" - Test command

## 🛠️ Development Workflow

### At Home (Testing)

1. Use Windows Speech Recognition for testing
2. Develop and test grammars without Dragon
3. Package addons for distribution

### At Work (Production)

1. Same code works with Dragon NaturallySpeaking
2. Better speech recognition accuracy
3. Full natlink functionality

## 📝 Creating a New Grammar

```python
from fake_natlink_runtime import natlinkmain
import subprocess

class MyGrammar(natlinkmain.GrammarBase):
    def __init__(self):
        super().__init__(name="MyGrammar")
        self.commands = {
            "my command": self.my_action,
        }

    def my_action(self):
        # Do something
        print("Command executed!")

    def gotResults(self, words, fullResults):
        recognized = ' '.join(words).lower()
        for command, action in self.commands.items():
            if command in recognized:
                action()
                return

grammar = MyGrammar()
```

## 🔧 Useful Scripts

- **main.py** - GUI for managing grammars
- **test_commands.py** - Test grammars without speech
- **addon_packager.py** - Package addons for distribution
- **grammar_loader.py** - Load/reload/unload grammars

## 📚 Key Features

✅ Virtual environment setup
✅ Mock natlink runtime for development
✅ GUI for grammar management
✅ Addon packaging system
✅ Test suite for commands
✅ Windows Speech Recognition integration
✅ Ready for Dragon NaturallySpeaking at work

## 🎓 Next Steps

1. Create custom grammars in `addons/`
2. Test with `test_commands.py`
3. Package with `addon_packager.py`
4. Deploy at work with Dragon

## 💡 Tips

- Grammars in `grammars/` are loaded automatically
- Addons in `addons/` are source code (not installed)
- Use GUI to reload grammars after editing
- Test locally, deploy at work seamlessly
