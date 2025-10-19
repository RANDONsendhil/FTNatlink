<!-- @format -->

# 📂 Grammars Folder

## Purpose

This folder contains voice command grammar files for the Natlink system.

## Structure

```
grammars/
├── <grammar_name>.py          # Standalone grammar files
└── <addon_id>/                # Installed addon grammars
    ├── <grammar1>.py
    └── <grammar2>.py
```

## Grammar Sources

The grammar loader automatically scans **three locations**:

### 1. Direct Grammars (`grammars/*.py`)

Standalone grammar files placed directly in this folder.

**Example:**

```
grammars/
└── my_custom_grammar.py
```

**Usage:**

```python
# Create a grammar file
from fake_natlink_runtime import MockGrammar

class MyGrammar(MockGrammar):
    def __init__(self):
        super().__init__("MyGrammar")
        self.commands = {
            "hello world": self.hello
        }

    def gotResults(self, words):
        command = " ".join(words)
        if command in self.commands:
            self.commands[command]()

    def hello(self):
        print("Hello, World!")

grammar = MyGrammar()
grammar.load()
```

### 2. Installed Addons (`grammars/<addon_id>/*.py`)

Grammars installed via `.addon-natlink` packages are extracted here.

**Example:**

```
grammars/
└── notepad_control/
    ├── notepad_grammar.py
    └── clipboard_grammar.py
```

**Installation:**

- Via GUI: Addons tab → Install Addon from File
- Via CLI: `python main.py addon.addon-natlink`

### 3. Development Addons (`../addons/<addon_name>/*.py`)

Grammars in the `addons/` folder (for development).

**Example:**

```
addons/
└── notepad_addon/
    ├── addon.json
    ├── notepad_grammar.py
    └── README.md
```

**Purpose:**

- Develop addons before packaging
- Test grammars without installation
- Keep addon source code organized

## Loading Process

When you click "Load All" or call `load_grammars()`:

1. ✅ Scans `grammars/*.py` for standalone grammars
2. ✅ Scans `grammars/*/*.py` for installed addon grammars
3. ✅ Scans `addons/*/` for development addon grammars
4. ✅ Loads all found grammar files
5. ✅ Initializes grammar objects
6. ✅ Registers voice commands

## Creating Grammars

### Option 1: Standalone Grammar

Create a `.py` file directly in this folder:

```bash
# grammars/browser_control.py
from fake_natlink_runtime import MockGrammar

class BrowserGrammar(MockGrammar):
    def __init__(self):
        super().__init__("BrowserGrammar")
        self.commands = {
            "open browser": self.open_browser,
            "close browser": self.close_browser
        }

    def gotResults(self, words):
        command = " ".join(words)
        if command in self.commands:
            self.commands[command]()

    def open_browser(self):
        import webbrowser
        webbrowser.open("https://www.google.com")

    def close_browser(self):
        # Implementation here
        pass

grammar = BrowserGrammar()
grammar.load()
```

### Option 2: Addon Grammar

Create an addon in the `addons/` folder:

```bash
addons/
└── my_addon/
    ├── addon.json
    └── my_grammar.py
```

See [ADDON_INSTALL_GUIDE.md](../ADDON_INSTALL_GUIDE.md) for details.

## Grammar Naming

- Use descriptive names: `notepad_grammar.py`, not `ng.py`
- Use snake_case: `my_custom_grammar.py`
- Avoid special characters except underscore
- Don't start with `__` (reserved for Python)

## Best Practices

1. **One Grammar Per File**: Keep grammars focused and modular
2. **Clear Commands**: Use natural language for voice commands
3. **Error Handling**: Add try-except blocks for reliability
4. **Documentation**: Add docstrings to explain what the grammar does
5. **Testing**: Test grammars individually before loading all

## Troubleshooting

### Grammar Not Loading

Check the log tab for error messages:

```
❌ Error loading my_grammar: <error message>
```

Common issues:

- **Syntax errors** in Python code
- **Missing imports** (natlink, MockGrammar, etc.)
- **Duplicate grammar names**
- **Permission errors**

### Grammar Not Appearing

Make sure:

- File has `.py` extension
- File is in correct location
- Click "Refresh" in Grammars tab
- Check file doesn't start with `__`

### Commands Not Working

Verify:

- Grammar is loaded (check log)
- Commands are properly defined in `self.commands`
- `gotResults()` method is implemented
- Dragon/Windows Speech Recognition is running

## File Organization

### Recommended Structure

```
grammars/
├── README.md                    # This file
├── productivity/                # Installed addon
│   ├── email_grammar.py
│   └── calendar_grammar.py
├── navigation/                  # Installed addon
│   ├── browser_grammar.py
│   └── file_explorer_grammar.py
└── my_personal_grammar.py       # Standalone grammar
```

### Not Recommended

```
grammars/
├── g1.py                        # Unclear name
├── test.py                      # Might be confused with tests
├── __temp__.py                  # Starts with __
└── backup_old_version.py.bak    # Not a .py file
```

## Development Workflow

1. **Create** grammar in `addons/<addon_name>/`
2. **Test** using GUI (grammars load automatically)
3. **Package** using `python addon_packager.py addons/<addon_name>`
4. **Install** the `.addon-natlink` file
5. **Share** the package with others

## Commands

### List Grammars

```python
from grammar_loader import list_grammars
print(list_grammars())
```

### Load Grammars

```python
from grammar_loader import load_grammars
load_grammars()
```

### Reload After Changes

```python
from grammar_loader import reload_grammars
reload_grammars()
```

### Unload All

```python
from grammar_loader import unload_grammars
unload_grammars()
```

## See Also

- [ADDON_INSTALL_GUIDE.md](../ADDON_INSTALL_GUIDE.md) - Creating and installing addons
- [PROJECT_SETUP.md](../PROJECT_SETUP.md) - Complete project setup
- [fake_natlink_runtime.py](../fake_natlink_runtime.py) - Mock natlink for development

---

**Note**: This folder is automatically scanned on startup and when you click "Refresh" or "Load All" in the GUI.
