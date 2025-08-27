#!/usr/bin/env python3
"""
Simple pytest runner for the Financial Analysis Bot.
"""
import subprocess
import sys
import os

def main():
    """Run pytest with common configurations."""
    # Change to project root directory
    project_root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_root)
    
    # Build pytest command
    cmd = [sys.executable, '-m', 'pytest']
    
    # Add any command line arguments passed to this script
    if len(sys.argv) > 1:
        cmd.extend(sys.argv[1:])
    
    print(f"Running: {' '.join(cmd)}")
    
    # Run pytest
    try:
        result = subprocess.run(cmd)
        sys.exit(result.returncode)
    except KeyboardInterrupt:
        print("\nTest run interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error running pytest: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()