"""
Standalone training script that can be run directly.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.train import train_model

if __name__ == "__main__":
    train_model()

