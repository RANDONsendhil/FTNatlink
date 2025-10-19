<!-- @format -->

# Installing Addons via GUI

## 🎯 Overview

The Natlink Grammar Manager GUI provides an easy way to install voice command addons from `.addon-natlink` files on your system.

## 📦 Installing an Addon

### Method 1: Using the GUI Button

1. **Launch the Grammar Manager**

   ```powershell
   python main.py
   ```

2. **Click "📦 Install Addon" button**

   - This opens a file browser dialog

3. **Select your `.addon-natlink` file**

   - Browse to where you saved the addon file
   - Select the file (e.g., `Notepad_Control_Addon.addon-natlink`)
   - Click "Open"

4. **Wait for Installation**

   - The addon will be extracted
   - Grammars will be automatically reloaded
   - A success message will appear

5. **Verify Installation**
   - Click "📋 List Grammars" to see the new grammar
   - The log will show all available grammars

### Method 2: Command Line

```powershell
python main.py path/to/addon.addon-natlink
```

### Method 3: Drag and Drop

Drag a `.addon-natlink` file onto `main.py` in Windows Explorer.

## 🔍 What Happens During Installation

1. ✅ Addon file is validated
2. ✅ Contents are extracted to `grammars/` folder
3. ✅ Grammar files are copied
4. ✅ Grammars are automatically reloaded
5. ✅ New voice commands are active

## 📋 GUI Features

### Buttons Available:

- **📋 List Grammars** - Shows all available grammar files
- **⬇️ Load Grammars** - Loads all grammars from the grammars folder
- **♻️ Reload Grammars** - Unloads and reloads all grammars (useful after editing)
- **⬆️ Unload Grammars** - Unloads all currently active grammars
- **📦 Install Addon** - Opens file browser to select and install `.addon-natlink` files

### Log Output:

The log window shows:

- Installation progress
- Success/error messages
- Grammar loading status
- Available grammars list

## 🛠️ Creating Addons to Install

### 1. Create Your Addon

```
my_addon/
├── addon.json
├── my_grammar.py
└── README.md
```

### 2. Package It

```powershell
python addon_packager.py addons/my_addon
```

This creates `My_Addon.addon-natlink`

### 3. Distribute

Share the `.addon-natlink` file with others!

## 📁 Where Are Addons Installed?

Addons are extracted to:

```
FTNatlink/grammars/
```

Each grammar file from the addon is copied here and automatically loaded.

## 🔧 Troubleshooting

### "File not found" error

- Make sure the `.addon-natlink` file exists
- Check the file path is correct

### "Failed to install addon" error

- Ensure the addon has a valid `addon.json`
- Check that grammar files are valid Python files
- Look at the log output for specific error messages

### Addon installed but not working

- Click "♻️ Reload Grammars" to refresh
- Check the log for loading errors
- Verify the grammar file syntax

## ✨ Example Workflow

1. Download `Notepad_Control_Addon.addon-natlink`
2. Run `python main.py`
3. Click "📦 Install Addon"
4. Select the downloaded file
5. Wait for "Installation Complete" message
6. Say "open notepad" to test!

## 🎤 Using Installed Commands

After installation:

- Commands are immediately active
- No restart needed
- Just start speaking the commands!

## 🗑️ Uninstalling Addons

To remove an addon:

1. Go to the `grammars/` folder
2. Delete the grammar files you don't want
3. Click "♻️ Reload Grammars" in the GUI

## 💡 Tips

- Keep your `.addon-natlink` files organized in a folder
- You can reinstall addons to update them
- Test addons with `test_commands.py` before installing
- Share addons with coworkers for consistent voice commands
