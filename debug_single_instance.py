#!/usr/bin/env python3
"""
Debug script to test single instance detection step by step
"""

import sys
import os

sys.path.insert(0, ".")

from core.single_instance import SingleInstanceManager
import psutil


def debug_processes():
    """Debug what processes are being detected"""
    print("=== DEBUGGING SINGLE INSTANCE DETECTION ===")

    current_pid = os.getpid()
    print(f"Current script PID: {current_pid}")
    print()

    print("=== ALL PYTHON PROCESSES ===")
    for process in psutil.process_iter(["pid", "name", "cmdline"]):
        try:
            info = process.info
            pid = info.get("pid")
            name = (info.get("name") or "").lower()
            cmdline = info.get("cmdline") or []

            if name == "python.exe" or name == "python":
                cmdline_str = " ".join(map(str, cmdline))
                print(f"PID {pid}: {cmdline_str}")

                # Check if this would trigger our detection
                joined = cmdline_str.lower()
                if "__init__.py" in joined and "ftnatlink" in joined:
                    print(f"  ⚠️  WOULD BE DETECTED BY OLD LOGIC")

                if (
                    "__init__.py" in joined
                    and "ftnatlink" in joined
                    and "ftnatlink\\__init__.py" in joined
                    and "vscode" not in joined
                    and "lsp_server" not in joined
                ):
                    print(f"  🚨 DETECTED BY NEW LOGIC")
                print()
        except Exception as e:
            pass

    print("=== TESTING SINGLE INSTANCE MANAGER ===")
    sim = SingleInstanceManager()
    result = sim.is_already_running()
    print(f"SingleInstanceManager.is_already_running(): {result}")

    # Test each method individually
    print("\n=== TESTING INDIVIDUAL METHODS ===")

    # Method 1: psutil
    try:
        psutil_result = sim._check_processes_psutil()
        print(f"_check_processes_psutil(): {psutil_result}")
    except Exception as e:
        print(f"_check_processes_psutil() ERROR: {e}")

    # Method 2: tasklist
    try:
        tasklist_result = sim._check_processes_tasklist()
        print(f"_check_processes_tasklist(): {tasklist_result}")
    except Exception as e:
        print(f"_check_processes_tasklist() ERROR: {e}")

    # Method 3: lock file
    try:
        lockfile_result = sim._check_lock_file()
        print(f"_check_lock_file(): {lockfile_result}")
    except Exception as e:
        print(f"_check_lock_file() ERROR: {e}")


if __name__ == "__main__":
    debug_processes()
