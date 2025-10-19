<!-- @format -->

# Core Module

The `core/` module contains the fundamental functionality for FTNatlink, including grammar loading, natlink runtime mocking, and testing utilities.

## 📁 Module Contents

### `grammar_loader.py`

**Purpose**: Load and manage voice command grammars from multiple locations

**Key Functions**:

- `load_grammars()` - Load all grammars from grammars/, grammars/_/, and addons/_/
- `list_grammars()` - List all available grammars
- `unload_grammars()` - Unload all active grammars
- `reload_grammars()` - Reload all grammars

**Grammar Locations**:

1. `grammars/*.py` - Root-level grammar files
2. `grammars/*/*.py` - Nested grammar folders
3. `addons/*/*.py` - Addon-provided grammars

**Usage**:

```python
from core import load_grammars, list_grammars

# Load all grammars
load_grammars()

# List loaded grammars
grammars = list_grammars()
print(grammars)  # ['notepad_grammar', 'sample_grammar']
```

### `fake_natlink_runtime.py`

**Purpose**: Mock natlink runtime for development without Dragon NaturallySpeaking

**Key Components**:

- `MockGrammar` - Mock grammar base class
- `natlinkmain` - Mock natlinkmain module with GrammarBase

**Why It Exists**:

- Allows development and testing without Dragon NaturallySpeaking installed
- Provides same API as real natlink for compatibility
- Enables GUI and grammar testing in any environment

**Usage**:

```python
from core.fake_natlink_runtime import natlinkmain

class MyGrammar(natlinkmain.GrammarBase):
    def __init__(self):
        super().__init__(name="MyGrammar")
        # Your grammar initialization
```

### `test_commands.py`

**Purpose**: Test utilities for voice commands and grammar functionality

**Usage**:

```python
cd F:\PROJECT_FT_NATLINK\FTNatlink\core
python test_commands.py
```

This will:

- Load all grammars
- Test grammar initialization
- Verify grammar loading from all locations

## 🔧 Integration

The core module is integrated throughout FTNatlink:

### GUI Integration

```python
# gui/app.py
from core.grammar_loader import load_grammars

# gui/tabs/grammars_tab.py
from core.grammar_loader import list_grammars, reload_grammars

# gui/tabs/addons_tab.py
from core.grammar_loader import reload_grammars
```

### Grammar Files

```python
# addons/*/grammar.py
from core.fake_natlink_runtime import natlinkmain

class MyGrammar(natlinkmain.GrammarBase):
    # Your grammar implementation
```

## 📦 Module Structure

```
core/
├── __init__.py                 # Module exports
├── grammar_loader.py           # Grammar loading system
├── fake_natlink_runtime.py     # Natlink mock
├── test_commands.py            # Test utilities
└── README.md                   # This file
```

## 🚀 Development Workflow

### Adding New Grammar Loaders

If you need to add new grammar loading logic:

1. Edit `grammar_loader.py`
2. Add your function
3. Export it in `core/__init__.py`
4. Import it where needed: `from core import your_function`

### Extending Mock Runtime

If you need to add more natlink functionality:

1. Edit `fake_natlink_runtime.py`
2. Add methods to `MockGrammar` or `natlinkmain`
3. Test with `test_commands.py`

## 🧪 Testing

Test the core module:

```bash
# Test grammar loading
cd core
python test_commands.py

# Or from project root
python -m core.test_commands
```

## 📚 Related Documentation

- **Grammar Loading Architecture**: `docs/GRAMMAR_ARCHITECTURE.md`
- **Addon System**: `addon_manager/README.md`
- **GUI Integration**: `gui/README.md`

## 🔑 Key Design Decisions

1. **Centralized Grammar Loading**: All grammar loading logic in one place
2. **Mock Runtime**: Development without Dragon dependency
3. **Multi-location Support**: Flexible grammar organization (root, nested, addons)
4. **Clean API**: Simple imports via `core` module

## 💡 Tips

- **Import Pattern**: Always use `from core import ...` for consistency
- **Path Setup**: Grammar files add project root to `sys.path` before importing
- **Mock vs Real**: The mock runtime has the same API as real natlink
- **Testing**: Use `test_commands.py` to verify grammar loading

---

**Last Updated**: October 19, 2025  
**Module Version**: 1.0  
**Part of**: FTNatlink Project
