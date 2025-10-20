# FTNatlink Grammar Loading Guide

## Overview
FTNatlink now automatically loads grammars on application startup and provides convenient management features through the system tray.

## Features

### 🚀 Automatic Grammar Loading
- Grammars are automatically loaded when the application starts
- No need to manually load grammars through the GUI
- Loaded grammars are active immediately and ready for voice commands

### 📋 System Tray Menu
Right-click the FTNatlink tray icon to access:

1. **Show Status** - Displays current application status and loaded grammars
2. **GUI Grammar Manager** - Opens the graphical interface for grammar management
3. **Reload Grammars** - Reloads all grammars without restarting the app
4. **Restart** - Restarts the entire application
5. **Quit** - Properly shuts down the application

### 🔄 Grammar Reload
- Use "Reload Grammars" to refresh grammar definitions without restarting
- Useful during development when modifying grammar files
- Shows confirmation dialog with reload results

## Startup Process

1. **Application Launch**: `python __init__.py`
2. **Grammar Loading**: Automatically scans and loads available grammars
3. **Tray Icon**: Creates system tray icon with menu options
4. **Background Service**: Runs continuously in the background
5. **Ready**: Grammars are active and ready for voice commands

## Console Output

When starting the application, you'll see:
```
🔄 Loading grammars on startup...
✅ Loaded grammar: notepad_grammar (notepad_addon)
✅ Loaded grammar: sample_grammar (sample_addon)
📊 Total grammars loaded: 2
```

## Benefits

- **Faster Workflow**: Grammars are ready immediately on startup
- **Better Development**: Reload grammars without full restart
- **Status Monitoring**: Easy way to check what grammars are loaded
- **Clean Shutdown**: Proper application exit with resource cleanup

## Usage Examples

### Development Workflow
1. Start FTNatlink: `python __init__.py`
2. Modify a grammar file
3. Right-click tray icon → "Reload Grammars"
4. Test your changes immediately

### Daily Use
1. Start FTNatlink once
2. Grammars are automatically loaded and active
3. Use voice commands immediately
4. Check status via tray menu if needed