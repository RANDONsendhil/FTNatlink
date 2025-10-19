<!-- @format -->

# 📝 Migration Note: main.py → **init**.py

## What Changed?

The project has been restructured to use proper Python package conventions:

- **Old**: `main.py` as the entry point
- **New**: `__init__.py` and `__main__.py` as package entry points

## Why?

1. **Python Best Practices**: Using `__init__.py` and `__main__.py` is the standard way to make a Python package executable
2. **Cleaner Structure**: FTNatlink is now a proper Python package
3. **More Flexibility**: Can be executed in multiple ways
4. **Professional**: Follows conventions used by major Python projects

## Impact

### ✅ What Still Works

All existing functionality works exactly the same. Only the launch method has changed.

### 🔄 How to Update

#### Before (with main.py)

```bash
cd FTNatlink
python main.py
```

#### After (with **init**.py)

```bash
# Method 1: From parent directory (recommended)
python -m FTNatlink

# Method 2: From FTNatlink directory
python __init__.py

# Method 3: GUI module directly
cd FTNatlink
python -m gui
```

### 📋 Update Your Scripts

If you have scripts or shortcuts that use `python main.py`, update them:

**Batch Files (.bat):**

```batch
# Old
python main.py

# New
python -m FTNatlink
```

**PowerShell (.ps1):**

```powershell
# Old
python main.py

# New
python -m FTNatlink
```

**Shell Scripts (.sh):**

```bash
# Old
python main.py

# New
python -m FTNatlink
```

### 🔗 Desktop Shortcuts

Update your desktop shortcuts:

**Windows:**

- Target: `python.exe -m FTNatlink`
- Start in: `F:\PROJECT_FT_NATLINK`

**Linux/Mac:**

- Command: `python -m FTNatlink`
- Working Directory: `~/PROJECT_FT_NATLINK`

## File Changes

### New Files

1. **`__init__.py`** (root)

   - Main package entry point
   - Imports and exports `main()` function
   - Can be executed directly: `python __init__.py`

2. **`__main__.py`** (root)
   - Module execution entry point
   - Enables: `python -m FTNatlink`
   - Standard Python pattern

### Modified Files

- `main.py` - **Can be removed** (replaced by `__init__.py`)
- `README.md` - Updated launch instructions
- `LAUNCH_METHODS.md` - Updated all examples
- `gui/__init__.py` - Already supports module execution
- `gui/__main__.py` - Already exists for `python -m gui`

## Benefits

### 1. Standard Python Package

```bash
# Install as package (future feature)
pip install -e .

# Run from anywhere
python -m FTNatlink
```

### 2. Clear Package Hierarchy

```
FTNatlink/          # Package root
├── __init__.py     # Package entry
├── __main__.py     # Module execution
├── gui/            # GUI subpackage
│   ├── __init__.py
│   └── __main__.py
└── ...
```

### 3. Multiple Entry Points

```bash
# Whole package
python -m FTNatlink

# Just GUI
python -m gui

# Specific module
python -m grammar_loader
```

## Backward Compatibility

### Option 1: Keep main.py (Deprecated)

If you want to keep backward compatibility, you can keep `main.py`:

```python
# main.py (deprecated)
"""
Legacy entry point - use 'python -m FTNatlink' instead
"""
import warnings
warnings.warn(
    "main.py is deprecated. Use 'python -m FTNatlink' instead.",
    DeprecationWarning
)

from gui import main
if __name__ == "__main__":
    main()
```

### Option 2: Remove main.py (Recommended)

Simply delete `main.py` and update all references to use the new methods.

## Testing

Verify the migration worked:

```bash
# Test package execution
python -m FTNatlink
# Should launch the GUI

# Test direct execution
cd FTNatlink
python __init__.py
# Should launch the GUI

# Test GUI module
python -m gui
# Should launch the GUI

# Test imports
python -c "from gui import main; print('OK')"
# Should print: OK
```

## Troubleshooting

### Error: "No module named FTNatlink"

**Solution**: Make sure you're running from the parent directory:

```bash
cd F:\PROJECT_FT_NATLINK
python -m FTNatlink
```

### Error: "No module named gui"

**Solution**: Virtual environment not activated:

```bash
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
```

### GUI doesn't start

**Solution**: Check if packages are installed:

```bash
pip install -r requirements.txt
```

## Rollback

If you need to rollback to `main.py`:

1. Rename `__init__.py` to `__init__.py.bak`
2. Create new `main.py`:
   ```python
   from gui import main
   if __name__ == "__main__":
       main()
   ```
3. Update your shortcuts back to `python main.py`

## Questions?

See documentation:

- [README.md](README.md) - Main documentation
- [LAUNCH_METHODS.md](LAUNCH_METHODS.md) - All launch methods
- [gui/README.md](gui/README.md) - GUI architecture

## Summary

✅ **Recommended Action**: Remove `main.py` and use `python -m FTNatlink`  
✅ **Migration Effort**: Low - just update launch commands  
✅ **Breaking Changes**: None - all functionality preserved  
✅ **Benefits**: Professional structure, follows Python standards

---

**Migration Date**: October 19, 2025  
**Project**: FTNatlink - Natlink Grammar Manager
