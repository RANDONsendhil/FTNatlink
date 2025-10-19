<!-- @format -->

# Natlink Addons

This folder contains voice command addons for Natlink.

## Structure

Each addon should be in its own folder with the following structure:

```
addon_name/
├── addon.json          # Addon metadata
├── README.md           # Addon documentation
└── *.py                # Grammar files
```

## addon.json Format

```json
{
	"name": "Addon Name",
	"version": "1.0.0",
	"description": "What this addon does",
	"author": "Your Name",
	"grammars": ["grammar_file.py"],
	"dependencies": []
}
```

## Available Addons

### notepad_addon

Voice commands to open and control Notepad.

**Commands:**

- "open notepad"
- "launch notepad"
- "start notepad"

### sample_addon

Basic sample voice commands for testing.

**Commands:**

- "hello" - Triggers hello response
- "test" - Triggers test response

## Creating Your Own Addon

1. Create a new folder in `addons/`
2. Add `addon.json` with metadata
3. Create your grammar Python files
4. Add a README.md with documentation
5. Package as `.addon-natlink` (zip file) for distribution

## Installing Addons

### Method 1: Direct Copy

Copy the addon folder to the `grammars/` directory.

### Method 2: GUI Installer

1. Package your addon as a `.addon-natlink` file (zip archive)
2. Use the Natlink Grammar Manager GUI
3. Or drag-and-drop the file on main.py

### Method 3: Command Line

```bash
python main.py path/to/addon.addon-natlink
```

## Packaging Addons

To create a `.addon-natlink` package:

```bash
zip -r mygrammar.addon-natlink addon_folder/*
```

Or use the addon installer script.
