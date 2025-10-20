#!/usr/bin/env python3
"""
Simple script to test quit functionality
"""

import subprocess
import time
import psutil
import sys


def check_processes():
    """Check for running FTNatlink processes"""
    processes = []
    for proc in psutil.process_iter(["pid", "name", "cmdline"]):
        try:
            if proc.info["cmdline"] and any(
                "__init__.py" in str(arg) for arg in proc.info["cmdline"]
            ):
                processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return processes


def main():
    print("🔍 FTNatlink Process Monitor")
    print("=" * 40)

    while True:
        processes = check_processes()
        if processes:
            print(f"📊 Found {len(processes)} FTNatlink process(es):")
            for proc in processes:
                print(f"  - PID: {proc['pid']}, CMD: {' '.join(proc['cmdline'])}")
        else:
            print("✅ No FTNatlink processes running")

        print("-" * 40)
        try:
            time.sleep(5)
        except KeyboardInterrupt:
            print("\n🛑 Monitoring stopped")
            break


if __name__ == "__main__":
    main()
