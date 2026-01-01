# quick_start.py - Interactive CLI tutorial
#!/usr/bin/env python3

def quick_start():
    """Interactive CLI quick start guide"""
    print("Python OS Simulator CLI - Quick Start Guide")
    print("=" * 60)
    
    print("\nWelcome to the Python OS Simulator CLI!")
    print("\nThis tool allows you to manage the OS Simulator from")
    print("your system terminal/command prompt.")
    
    input("\nPress Enter to continue...")
    
    print("\n" + "=" * 60)
    print("INSTALLATION")
    print("=" * 60)
    
    print("\n1. Make sure you're in the OS Simulator directory")
    print("2. Run the setup script:")
    print("   python setup_cli.py")
    print("\nThis will create a 'pos' command for easy access.")
    
    input("\nPress Enter to continue...")
    
    print("\n" + "=" * 60)
    print("BASIC COMMANDS")
    print("=" * 60)
    
    print("\nTry these commands to get started:")
    print("""
  pos --help                    # Show all commands
  pos status                    # Check system status
  pos user --list               # List all users
  pos reset-system              # Reset system (triggers setup)
  pos reset-settings            # Reset to default settings
    """)
    
    input("\nPress Enter to continue...")
    
    print("\n" + "=" * 60)
    print("USER MANAGEMENT")
    print("=" * 60)
    
    print("\nManaging users:")
    print("""
  pos user --add bob            # Add user 'bob'
  pos user --delete bob         # Delete user 'bob'
  pos user --reset-password admin  # Reset admin password
    """)
    
    input("\nPress Enter to continue...")
    
    print("\n" + "=" * 60)
    print("BACKUP & RESTORE")
    print("=" * 60)
    
    print("\nBackup your system:")
    print("""
  pos backup --output my_backup.db
  pos restore --input my_backup.db
    """)
    
    print("\n" + "=" * 60)
    print("GETTING HELP")
    print("=" * 60)
    
    print("\nFor detailed help on any command:")
    print("  pos [command] --help")
    print("\nExample: pos user --help")
    
    print("\n" + "=" * 60)
    print("ENJOY!")
    print("=" * 60)
    print("\nThe CLI tool gives you complete control over your")
    print("Python OS Simulator from the command line!")
    
if __name__ == "__main__":
    quick_start()