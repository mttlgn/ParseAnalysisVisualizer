from pathlib import Path
import streamlit as st
import sys
import os

# Add the src directory to Python path
src_path = str(Path(__file__).parent.parent / 'src')
if src_path not in sys.path:
    sys.path.append(src_path)

# Import the main app
from app import main

# Configure Streamlit for minimal resource usage
st.set_page_config(
    layout="wide",
    page_title="WoW Raid Analysis",
    initial_sidebar_state="collapsed"
)

# Disable file uploaders and other heavy features
st.cache_data.clear()
st.cache_resource.clear()

def handler(request, response):
    try:
        # Set environment variables for optimization
        os.environ['STREAMLIT_SERVER_HEADLESS'] = 'true'
        os.environ['STREAMLIT_SERVER_FILE_WATCHER_TYPE'] = 'none'
        
        return main()
    except Exception as e:
        return {
            "statusCode": 500,
            "body": str(e)
        } 