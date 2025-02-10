from pathlib import Path
import streamlit as st
import sys

# Add the src directory to Python path
src_path = str(Path(__file__).parent.parent / 'src')
if src_path not in sys.path:
    sys.path.append(src_path)

# Import the main app
from app import main

def handler(request, response):
    return main() 