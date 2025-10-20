# Tools Directory

This folder contains utility scripts for monitoring, testing, and debugging FTNatlink.

## Files

### `simple_monitor.py`
A Windows-compatible process monitor that uses built-in Windows `tasklist` command to check for running Python processes.

**Usage:**
```bash
python tools/simple_monitor.py
```

**Features:**
- Monitors Python processes without requiring external dependencies
- Uses Windows `tasklist` command for compatibility
- Specifically designed for testing FTNatlink quit functionality
- Shows real-time process count updates

**What it does:**
- Lists all running `python.exe` processes
- Updates every 3 seconds
- Helps verify that FTNatlink properly exits when quit
- No external dependencies required

### `process_monitor.py`  
An advanced process monitor that uses `psutil` to provide detailed process information.

**Usage:**
```bash
# Requires psutil: pip install psutil
python tools/process_monitor.py
```

**Features:**
- Detailed process information including PID, command line arguments
- Specifically looks for FTNatlink processes (those running `__init__.py`)
- More detailed than simple_monitor.py but requires psutil dependency

**What it does:**
- Monitors processes by command line arguments
- Identifies FTNatlink-specific processes
- Shows PID and full command line
- Updates every 5 seconds

## Usage Examples

### Testing Application Quit Functionality
1. Start FTNatlink: `python __init__.py`
2. In another terminal, start monitoring: `python tools/simple_monitor.py`
3. Use the tray icon to quit FTNatlink
4. Verify the process disappears from the monitor

### Testing Restart Functionality  
1. Start monitoring: `python tools/simple_monitor.py`
2. Start FTNatlink: `python __init__.py`
3. Use tray icon "Restart" option
4. Verify only one process remains (no duplicates)

### Development Debugging
Use these tools during development to ensure:
- Clean application shutdown
- No zombie processes
- Proper restart behavior
- Memory leak detection

## Dependencies

### simple_monitor.py
- **No external dependencies** - uses built-in Windows commands
- Works on any Windows system with Python

### process_monitor.py  
- **Requires psutil**: `pip install psutil`
- More detailed but has dependency requirements

## Notes

- Both scripts are designed for Windows environments
- `simple_monitor.py` is recommended for most use cases (no dependencies)
- `process_monitor.py` provides more detail when psutil is available
- Both scripts can run continuously in the background during testing
- Use Ctrl+C to stop monitoring