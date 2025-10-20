#!/usr/bin/env python3
"""
Simple script to test quit functionality using Windows tasklist
"""

import subprocess
import time


def check_python_processes():
    """Check for running Python processes using Windows tasklist"""
    try:
        result = subprocess.run(
            ["tasklist", "/FI", "IMAGENAME eq python.exe", "/FO", "CSV"],
            capture_output=True,
            text=True,
        )
        lines = result.stdout.strip().split("\n")
        if len(lines) > 1:  # More than just header
            return lines[1:]  # Return process lines
        return []
    except Exception as e:
        print(f"Error checking processes: {e}")
        return []


def main():
    print("🔍 Python Process Monitor (for FTNatlink testing)")
    print("=" * 50)
    print("Instructions:")
    print("1. Start FTNatlink in another terminal")
    print("2. Watch this monitor to see the process")
    print("3. Use the tray icon 'Quit' option")
    print("4. Verify the process disappears from this monitor")
    print("5. Press Ctrl+C to stop monitoring")
    print("=" * 50)

    while True:
        processes = check_python_processes()
        if processes:
            print(f"📊 Found {len(processes)} Python process(es):")
            for proc in processes:
                # Clean up CSV format
                proc_clean = proc.replace('"', "")
                print(f"  - {proc_clean}")
        else:
            print("✅ No Python processes running")

        print("-" * 30)
        try:
            time.sleep(3)
        except KeyboardInterrupt:
            print("\n🛑 Monitoring stopped")
            break


if __name__ == "__main__":
    main()
