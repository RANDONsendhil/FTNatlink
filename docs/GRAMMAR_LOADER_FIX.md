<!-- @format -->

# 🔧 Fix: Grammar Loading from Addons

## Problem

Grammars in the `addons/` folder were not being loaded by the application.

## Root Cause

The `grammar_loader.py` was only scanning the `grammars/` folder for `.py` files in the root directory. It was not checking:

1. Subdirectories in `grammars/` (installed addons)
2. The `addons/` folder (development addons)

## Solution

Updated `grammar_loader.py` to scan **three locations**:

### 1. Direct Grammars (`grammars/*.py`)

```python
for file in GRAMMAR_DIR.glob("*.py"):
    if not file.name.startswith("__"):
        _load_grammar_file(file)
```

### 2. Installed Addon Grammars (`grammars/*/*.py`)

```python
for subdir in GRAMMAR_DIR.iterdir():
    if subdir.is_dir():
        for file in subdir.glob("*.py"):
            if not file.name.startswith("__"):
                _load_grammar_file(file)
```

### 3. Development Addon Grammars (`addons/*/*.py`)

```python
if ADDON_DIR.exists():
    for addon_folder in ADDON_DIR.iterdir():
        if addon_folder.is_dir():
            addon_json = addon_folder / "addon.json"
            if addon_json.exists():
                for file in addon_folder.glob("*.py"):
                    if not file.name.startswith("__"):
                        _load_grammar_file(file)
```

## Changes Made

### File: `grammar_loader.py`

#### Added:

- `ADDON_DIR` constant pointing to `addons/` folder
- `_load_grammar_file()` helper function for loading individual files
- Directory scanning for subdirectories in `grammars/`
- Directory scanning for addon folders in `addons/`
- Better error messages showing grammar location

#### Updated:

- `load_grammars()` - Now scans all three locations
- `list_grammars()` - Returns grammars from all sources
- Added automatic directory creation if `grammars/` doesn't exist

### File: `grammars/README.md` (NEW)

- Complete documentation for the grammars folder
- Explanation of all three grammar sources
- Examples and best practices
- Troubleshooting guide

## Testing

After the fix, grammars are successfully loaded:

```
✅ Loaded grammar: notepad_grammar (notepad_addon)
✅ Loaded grammar: sample_grammar (sample_addon)
```

## Benefits

### ✅ Development Workflow

- Can develop grammars directly in `addons/` folder
- No need to install addon packages for testing
- Changes reflected immediately on reload

### ✅ Organized Structure

```
addons/
├── notepad_addon/           # Development addon
│   ├── addon.json
│   └── notepad_grammar.py   # ✅ Now loaded!
└── sample_addon/            # Development addon
    ├── addon.json
    └── sample_grammar.py    # ✅ Now loaded!

grammars/
├── my_grammar.py            # ✅ Standalone grammar
└── installed_addon/         # ✅ Installed addon
    └── addon_grammar.py     # ✅ Now loaded!
```

### ✅ Flexibility

- Standalone grammars in `grammars/`
- Development addons in `addons/`
- Installed addons in `grammars/<addon_id>/`
- All automatically discovered and loaded

## Usage

### For Users

Just use the GUI - grammars from all locations load automatically:

1. Open GUI
2. Go to Grammars tab
3. Click "Refresh" - sees all grammars
4. Click "Load All" - loads all grammars

### For Developers

**Develop in `addons/` folder:**

```bash
addons/
└── my_new_addon/
    ├── addon.json
    └── my_grammar.py
```

**Test immediately:**

```bash
python -m gui
# Click "Refresh" then "Load All"
```

**Package when ready:**

```bash
python addon_packager.py addons/my_new_addon
```

## Example Output

```
PS F:\PROJECT_FT_NATLINK\FTNatlink> python -m gui
MockGrammar 'NotepadGrammar' initialized
📝 Notepad Grammar initialized
✅ Loaded grammar: notepad_grammar (notepad_addon)
MockGrammar 'SampleGrammar' initialized
🎤 Sample Grammar initialized
✅ Loaded grammar: sample_grammar (sample_addon)
```

Notice:

- Grammar name shown
- Source folder shown in parentheses
- Both addons loaded successfully

## Migration

No migration needed! The fix is backward compatible:

- ✅ Existing standalone grammars still work
- ✅ Existing installed addons still work
- ✅ New development addons now work

## Future Enhancements

Potential improvements:

1. **Priority Loading**: Load in specific order (grammars → installed → dev)
2. **Dependency Resolution**: Handle grammar dependencies
3. **Lazy Loading**: Load grammars on-demand
4. **Hot Reload**: Watch for file changes and auto-reload
5. **Grammar Registry**: Track loaded grammars with metadata

## Summary

✅ **Problem**: Addons folder grammars not loading  
✅ **Solution**: Updated grammar_loader.py to scan addons/  
✅ **Result**: All grammars now load from all three locations  
✅ **Impact**: Better development workflow, no breaking changes

---

**Fixed**: October 19, 2025  
**File**: grammar_loader.py  
**Issue**: Addons not being scanned  
**Status**: ✅ Resolved and Tested
