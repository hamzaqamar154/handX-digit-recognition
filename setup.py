"""
Setup script for handwriting recognition project.
"""
from setuptools import setup, find_packages

setup(
    name="handwriting-recognition-ml",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "tensorflow>=2.13.0",
        "streamlit>=1.28.0",
        "fastapi>=0.104.0",
        "uvicorn[standard]>=0.24.0",
        "pillow>=10.0.0",
        "numpy>=1.24.0",
        "pandas>=2.0.0",
        "matplotlib>=3.7.0",
        "scikit-learn>=1.3.0",
    ],
)

