<!-- @format -->

# 📦 Addon Manager Module

## Purpose

The addon_manager module handles all addon-related functionality including installation, packaging, and management of Natlink voice command addons.

## Structure

```
addon_manager/
├── __init__.py           # Module exports
├── addon_installer.py    # Addon installation functionality
└── addon_packager.py     # Addon packaging functionality
```

## Components

### 1. addon_installer.py

**Purpose**: Install `.addon-natlink` packages into the grammars folder.

**Main Function**: `install_addon(addon_path)`

**Process**:

1. Extract `.addon-natlink` zip file
2. Read `addon.json` metadata
3. Move grammars to `grammars/<addon_id>/`
4. Store metadata in `installed_addons/`

**Usage**:

```python
from addon_manager import install_addon

install_addon("path/to/addon.addon-natlink")
```

**Features**:

- ✅ Validates addon structure
- ✅ Checks for addon.json
- ✅ Creates addon directory
- ✅ Stores metadata
- ✅ Handles errors gracefully

---

### 2. addon_packager.py

**Purpose**: Package addon folders into distributable `.addon-natlink` files.

**Main Function**: `package_addon(addon_folder, output_file=None)`

**Process**:

1. Read `addon.json` metadata
2. Create zip file with `.addon-natlink` extension
3. Include all files except `.addon-natlink` files
4. Generate in `addons/` folder by default

**Usage via Script**:

```bash
python addon_packager.py addons/my_addon
```

**Usage via Import**:

```python
from addon_manager import package_addon

package_addon("addons/my_addon")
```

**Features**:

- ✅ Reads addon metadata
- ✅ Creates zip archive
- ✅ Shows file list
- ✅ Displays package size
- ✅ Lists available addons if no argument

---

## Usage Examples

### Installing an Addon

**Via GUI:**

1. Open GUI → Addons tab
2. Click "📦 Install Addon from File"
3. Select `.addon-natlink` file
4. Grammars automatically reloaded

**Via Code:**

```python
from addon_manager import install_addon
from grammar_loader import reload_grammars

install_addon("downloads/my_addon.addon-natlink")
reload_grammars()
```

**Via Command Line:**

```bash
python __init__.py my_addon.addon-natlink
```

---

### Packaging an Addon

**Via Command Line (Recommended):**

```bash
python addon_packager.py addons/notepad_addon
```

**Via Code:**

```python
from addon_manager import package_addon

success = package_addon("addons/notepad_addon")
if success:
    print("Package created!")
```

**Output:**

```
📦 Packaging addon from: addons\notepad_addon
📋 Addon: Notepad Control Addon v1.0.0
📝 Creating package: addons\Notepad_Control_Addon.addon-natlink

   ✅ Added: addon.json
   ✅ Added: notepad_grammar.py
   ✅ Added: README.md

🎉 Package created: addons\Notepad_Control_Addon.addon-natlink
   Size: 2048 bytes
```

---

## API Reference

### install_addon(addon_path)

Install an addon from a `.addon-natlink` file.

**Parameters:**

- `addon_path` (str | Path): Path to `.addon-natlink` file

**Returns:** None

**Raises:**

- `FileNotFoundError`: If addon file doesn't exist
- `ValueError`: If addon.json is missing or invalid

**Example:**

```python
from addon_manager import install_addon

try:
    install_addon("my_addon.addon-natlink")
    print("Installed successfully!")
except FileNotFoundError:
    print("Addon file not found")
except ValueError as e:
    print(f"Invalid addon: {e}")
```

---

### package_addon(addon_folder, output_file=None)

Package an addon folder into a `.addon-natlink` file.

**Parameters:**

- `addon_folder` (str | Path): Path to addon folder
- `output_file` (str | Path, optional): Output file path (auto-generated if None)

**Returns:** bool - True if successful

**Raises:**

- `FileNotFoundError`: If addon folder doesn't exist
- `ValueError`: If addon.json is missing or invalid

**Example:**

```python
from addon_manager import package_addon

# Auto-generate output filename
if package_addon("addons/my_addon"):
    print("Success!")

# Custom output path
package_addon(
    "addons/my_addon",
    "releases/my_addon_v1.0.0.addon-natlink"
)
```

---

## Directory Structure

### Before Installation

```
FTNatlink/
├── addon_manager/
│   ├── addon_installer.py
│   └── addon_packager.py
├── addons/
│   └── my_addon/
│       ├── addon.json
│       └── my_grammar.py
└── grammars/
    └── (empty or existing grammars)
```

### After Packaging

```
FTNatlink/
├── addon_manager/
├── addons/
│   ├── my_addon/
│   │   ├── addon.json
│   │   └── my_grammar.py
│   └── My_Addon.addon-natlink  ← Created package
└── grammars/
```

### After Installation

```
FTNatlink/
├── addon_manager/
├── addons/
│   └── My_Addon.addon-natlink
├── grammars/
│   └── my_addon_id/  ← Installed here
│       └── my_grammar.py
└── installed_addons/
    └── my_addon_id.json  ← Metadata stored
```

---

## Integration Points

### With grammar_loader

```python
from addon_manager import install_addon
from grammar_loader import reload_grammars

# Install and reload
install_addon("addon.addon-natlink")
reload_grammars()  # Load new grammars
```

### With GUI

```python
# gui/app.py
from addon_manager import install_addon

# Handle command-line addon installation
if addon_file.suffix == ".addon-natlink":
    install_addon(addon_file)
```

```python
# gui/tabs/addons_tab.py
from addon_manager import install_addon

def on_install(event, frame):
    # File dialog → install_addon → reload
    install_addon(selected_file)
    reload_grammars()
```

---

## Error Handling

### Common Errors

**1. Addon File Not Found**

```python
FileNotFoundError: Addon not found: path/to/addon.addon-natlink
```

**Solution**: Check file path is correct

**2. Invalid Addon Structure**

```python
ValueError: Invalid addon: missing addon.json
```

**Solution**: Ensure addon.json exists in the addon folder

**3. Corrupted Zip File**

```python
zipfile.BadZipFile: File is not a zip file
```

**Solution**: Repackage the addon or download again

---

## Best Practices

### For Addon Developers

1. **Always include addon.json**:

   ```json
   {
   	"name": "My Addon",
   	"version": "1.0.0",
   	"description": "Description here",
   	"author": "Your Name",
   	"grammars": ["my_grammar.py"],
   	"dependencies": []
   }
   ```

2. **Test before packaging**:

   ```bash
   # Test in addons/ folder first
   python -m gui
   # Then package
   python addon_packager.py addons/my_addon
   ```

3. **Use semantic versioning**: 1.0.0, 1.0.1, 1.1.0, 2.0.0

4. **Document your grammars**: Add README.md and docstrings

### For Users

1. **Always from trusted sources**: Only install addons from trusted developers

2. **Backup before installing**: Save your grammars folder

3. **Check metadata**: Verify addon name, version, author

4. **Test in isolation**: Install one addon at a time

---

## Future Enhancements

Potential improvements:

- [ ] Addon versioning and updates
- [ ] Dependency resolution
- [ ] Digital signatures for security
- [ ] Addon repository/marketplace
- [ ] Auto-update functionality
- [ ] Addon categories/tags
- [ ] User reviews and ratings
- [ ] Rollback functionality

---

## See Also

- **[ADDON_INSTALL_GUIDE.md](../docs/ADDON_INSTALL_GUIDE.md)** - Complete addon guide
- **[grammar_loader.py](../grammar_loader.py)** - Grammar loading system
- **[addons/README.md](../addons/README.md)** - Addon folder info

---

**Module**: addon_manager  
**Version**: 1.0.0  
**Status**: ✅ Production Ready
