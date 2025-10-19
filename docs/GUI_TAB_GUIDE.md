<!-- @format -->

# 🎨 Natlink GUI - Tab Interface Guide

## 📑 Overview

The Natlink Grammar Manager now uses a modern tabbed interface for better organization and easier navigation.

## 🗂️ Tabs

### 1. 📋 Grammars Tab

**Purpose:** Manage voice command grammars

**Layout:**

- **Left Panel** - Grammar list and management buttons
- **Right Panel** - Detailed information about selected grammar

**Features:**

- **Grammar List** - Shows all available grammar files
- **Split-View Details** - Click any grammar to see its details
- **📋 Refresh** - Updates the grammar list
- **⬇️ Load All** - Loads all grammars from the grammars folder
- **♻️ Reload All** - Unloads and reloads all grammars (useful after editing)
- **⬆️ Unload All** - Unloads all currently active grammars

**Grammar Details Display:**
When you select a grammar from the list, the right panel shows:

- 📄 File name and location
- 📏 File size
- 📝 Description (from module docstring)
- 🔷 Class names and their methods
- 🎤 Voice commands defined in the grammar

**Usage:**

1. Click "📋 Refresh" to see available grammars
2. Click any grammar to view its details in the right panel
3. Click "⬇️ Load All" to activate grammars
4. Click "♻️ Reload All" after editing grammar files
5. Drag the divider between panels to adjust the view

### 2. 📦 Addons Tab

**Purpose:** Install and manage addon packages

**Features:**

- **Instructions** - How to use addons
- **📦 Install Addon from File** - Browse and install .addon-natlink files
- **Packaging Info** - How to create your own addons

**Usage:**

1. Click "📦 Install Addon from File"
2. Browse to select a .addon-natlink file
3. Wait for installation to complete
4. Grammars are automatically reloaded

**Benefits:**

- Easy addon installation
- No need to manually copy files
- Automatic grammar activation
- Share addons with colleagues

### 3. 📄 Log Tab

**Purpose:** View activity and debug messages

**Features:**

- **Activity Log** - Shows all operations and messages
- **🗑️ Clear Log** - Clears the log output
- **Auto-scroll** - Always shows latest messages

**What's Logged:**

- Grammar loading/unloading operations
- Addon installation progress
- Success/error messages
- System notifications

## 🎯 Workflow Examples

### Installing an Addon

1. **Switch to 📦 Addons tab**
2. **Click "📦 Install Addon from File"**
3. **Select your .addon-natlink file**
4. **Switch to 📄 Log tab** to see installation progress
5. **Switch to 📋 Grammars tab** to verify installation

### Managing Grammars

1. **Go to 📋 Grammars tab**
2. **Click "📋 Refresh List"** to see available grammars
3. **Make changes to grammar files** (edit in VS Code)
4. **Click "♻️ Reload All"** to apply changes
5. **Check 📄 Log tab** for any errors

### Debugging

1. **Open 📄 Log tab**
2. **Perform actions** in other tabs
3. **Watch log messages** for errors or warnings
4. **Use "🗑️ Clear Log"** to start fresh

## 🎨 Visual Layout

```
┌─────────────────────────────────────────┐
│  Natlink Grammar Manager                │
├─────────────────────────────────────────┤
│ [📋 Grammars] [📦 Addons] [📄 Log]     │
├─────────────────────────────────────────┤
│                                          │
│  Tab Content Area                        │
│                                          │
│  (Changes based on selected tab)        │
│                                          │
│                                          │
│                                          │
└─────────────────────────────────────────┘
```

## ✨ Benefits of Tab Interface

### Better Organization

- ✅ Related functions grouped together
- ✅ Less cluttered interface
- ✅ Easy to find features

### Improved Workflow

- ✅ Switch between tasks easily
- ✅ Keep log visible while working
- ✅ Clear separation of concerns

### Enhanced Usability

- ✅ Larger working area per tab
- ✅ More space for content
- ✅ Cleaner, modern look

## 🔧 Keyboard Shortcuts

- **Ctrl+Tab** - Next tab
- **Ctrl+Shift+Tab** - Previous tab
- **Alt+F4** - Close window

## 💡 Tips

- **Keep Log Tab Open** - Switch between tabs while watching logs
- **Refresh Often** - Click "📋 Refresh List" after changes
- **Check Logs** - Always check the log tab after operations
- **Clean Interface** - Use "🗑️ Clear Log" to reduce clutter

## 🎓 Quick Reference

| Task              | Tab         | Button                     |
| ----------------- | ----------- | -------------------------- |
| See grammars      | 📋 Grammars | 📋 Refresh List            |
| Load grammars     | 📋 Grammars | ⬇️ Load All                |
| Reload after edit | 📋 Grammars | ♻️ Reload All              |
| Install addon     | 📦 Addons   | 📦 Install Addon from File |
| Check status      | 📄 Log      | (view messages)            |
| Clear messages    | 📄 Log      | 🗑️ Clear Log               |

## 🚀 Getting Started

1. **Launch GUI**: `python main.py`
2. **Go to 📋 Grammars tab**
3. **Click "📋 Refresh List"** to see available grammars
4. **Click "⬇️ Load All"** to activate voice commands
5. **Switch to 📄 Log tab** to see results

You're ready to use voice commands! 🎤
