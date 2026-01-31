import streamlit as st
import os
import sys
from streamlit.web import bootstrap

def main():
    os.environ["STREAMLIT_SERVER_PORT"] = "9000"
    os.environ["STREAMLIT_SERVER_ADDRESS"] = "0.0.0.0"
    
    sys.path.insert(0, os.path.dirname(__file__))
    
    from main import main as app_main
    app_main()

if __name__ == "__main__":
    main()
