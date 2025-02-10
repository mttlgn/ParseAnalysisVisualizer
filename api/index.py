from pathlib import Path
import streamlit as st
import sys
import os
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
import uvicorn

# Add the src directory to Python path
src_path = str(Path(__file__).parent.parent / 'src')
if src_path not in sys.path:
    sys.path.append(src_path)

# Import the main app
from app import main

# Configure Streamlit for Edge deployment
st.set_page_config(
    layout="wide",
    page_title="WoW Raid Analysis",
    initial_sidebar_state="collapsed"
)

# Optimize for Edge
st.cache_data.clear()
st.cache_resource.clear()
os.environ['STREAMLIT_SERVER_HEADLESS'] = 'true'
os.environ['STREAMLIT_SERVER_FILE_WATCHER_TYPE'] = 'none'

async def app(request):
    try:
        return await main()
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

# Create ASGI app
routes = [Route("/", app)]
app = Starlette(routes=routes)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 