import streamlit as st
import os
from dotenv import load_dotenv
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.database import init_database

load_dotenv()

st.set_page_config(
    page_title="应急响应系统",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded"
)

init_database()

PAGES = {
    "老人端模拟": {
        "icon": "👴",
        "file": "pages/elderly_page.py"
    },
    "后台仪表盘": {
        "icon": "📊",
        "file": "pages/dashboard.py"
    },
    "知识库管理": {
        "icon": "📚",
        "file": "pages/knowledge_base.py"
    },
    "系统设置": {
        "icon": "⚙️",
        "file": "pages/settings.py"
    }
}

def render_sidebar():
    with st.sidebar:
        st.title("🚨 应急响应系统")
        st.markdown("---")
        
        for page_name, page_info in PAGES.items():
            icon = page_info["icon"]
            if st.button(f"{icon} {page_name}", key=f"nav_{page_name}", use_container_width=True):
                st.session_state.current_page = page_name
        
        st.markdown("---")
        st.caption("© 2026 应急响应系统")

def main():
    if "current_page" not in st.session_state:
        st.session_state.current_page = "后台仪表盘"
    
    render_sidebar()
    
    current_page = st.session_state.current_page
    
    if current_page == "老人端模拟":
        from pages.elderly_page import show_elderly_page
        show_elderly_page()
    elif current_page == "后台仪表盘":
        from pages.dashboard import show_dashboard
        show_dashboard()
    elif current_page == "知识库管理":
        from pages.knowledge_base import show_knowledge_base
        show_knowledge_base()
    elif current_page == "系统设置":
        from pages.settings import show_settings
        show_settings()

if __name__ == "__main__":
    main()
