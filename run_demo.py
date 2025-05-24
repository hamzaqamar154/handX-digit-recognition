"""
Standalone demo script that can be run directly.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.main import main
import argparse

if __name__ == "__main__":
    # Override sys.argv for demo
    sys.argv = ["run_demo.py", "--demo"]
    main()

