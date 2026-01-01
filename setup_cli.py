# setup_cli.py - Install CLI tool as system command
#!/usr/bin/env python3

import os
import sys
import shutil

def install_cli():
    """Install CLI tool as system command"""
    print("Python OS Simulator CLI Installer")
    print("=" * 50)
    
    # Check OS
    if sys.platform == "win32":
        install_windows()
    elif sys.platform == "linux" or sys.platform == "darwin":
        install_unix()
    else:
        print(f"Unsupported platform: {sys.platform}")
        
def install_windows():
    """Install CLI on Windows"""
    print("Installing for Windows...")
    
    # Create batch file
    batch_content = '''@echo off
python "%~dp0os_cli.py" %*
'''
    
    # Write batch file
    with open('pos.bat', 'w') as f:
        f.write(batch_content)
        
    # Add to PATH
    current_dir = os.path.abspath('.')
    print(f"\nCreated 'pos.bat' in {current_dir}")
    print("\nTo use the CLI:")
    print(f"1. Add {current_dir} to your PATH")
    print("2. Run commands like: pos --help")
    print("\nOr run directly: python os_cli.py --help")
    
def install_unix():
    """Install CLI on Unix/Linux/macOS"""
    print("Installing for Unix/Linux/macOS...")
    
    # Create shell script
    script_content = '''#!/bin/bash
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
python "$SCRIPT_DIR/os_cli.py" "$@"
'''
    
    # Write script
    with open('pos', 'w') as f:
        f.write(script_content)
        
    # Make executable
    os.chmod('pos', 0o755)
    
    current_dir = os.path.abspath('.')
    print(f"\nCreated 'pos' executable in {current_dir}")
    print("\nTo use the CLI:")
    print(f"1. Add to PATH: export PATH=\"$PATH:{current_dir}\"")
    print("2. Run commands like: pos --help")
    print("\nOr run directly: python os_cli.py --help")

if __name__ == "__main__":
    install_cli()