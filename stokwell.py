#!/usr/bin/env python3
"""
StokWELL Desktop Application Launcher
This script attempts to launch the GUI version, and falls back to CLI if GUI is not available.
"""

import sys
import os

def launch_gui():
    """Attempt to launch the GUI version."""
    try:
        # Set environment for headless operation if needed
        if 'DISPLAY' not in os.environ:
            os.environ['QT_QPA_PLATFORM'] = 'offscreen'
        
        from controller import Controller
        controller = Controller()
        controller.run()
        return True
    except ImportError as e:
        print(f"GUI dependencies not available: {e}")
        return False
    except Exception as e:
        print(f"GUI launch failed: {e}")
        return False

def launch_cli():
    """Launch the CLI version."""
    try:
        from stokwell_cli import main
        main()
        return True
    except Exception as e:
        print(f"CLI launch failed: {e}")
        return False

def main():
    print("StokWELL Desktop Application")
    print("=" * 30)
    
    # Check if we should force CLI mode
    if len(sys.argv) > 1 and sys.argv[1] == '--cli':
        print("Launching in CLI mode...")
        if not launch_cli():
            print("Failed to launch CLI version.")
            sys.exit(1)
        return
    
    # Try GUI first, then fall back to CLI
    print("Attempting to launch GUI version...")
    if not launch_gui():
        print("\nGUI not available. Launching CLI version...")
        if not launch_cli():
            print("Failed to launch any version of the application.")
            sys.exit(1)

if __name__ == "__main__":
    main()

