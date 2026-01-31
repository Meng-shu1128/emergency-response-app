import streamlit as st
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.database import get_users, get_alerts

def rerun():
    if 'rerun' not in st.session_state:
        st.session_state.rerun = False
    
    if st.session_state.rerun:
        st.session_state.rerun = False
        st.experimental_rerun()

def show_settings():
    st.title("⚙️ 系统设置")
    st.markdown("---")
    
    tab1, tab2, tab3 = st.tabs(["🔑 API配置", "👥 用户管理", "🗑️ 数据管理"])
    
    with tab1:
        st.subheader("API密钥配置")
        
        st.info("请在项目根目录的 .env 文件中配置以下API密钥")
        
        with st.form("api_config"):
            api_key = st.text_input("主API密钥", type="password", placeholder="your_api_key_here")
            map_api_key = st.text_input("地图API密钥", type="password", placeholder="your_map_api_key_here")
            sms_api_key = st.text_input("短信API密钥", type="password", placeholder="your_sms_api_key_here")
            notification_api_key = st.text_input("通知API密钥", type="password", placeholder="your_notification_api_key_here")
            
            if st.form_submit_button("保存配置"):
                st.warning("请直接编辑 .env 文件来保存配置")
                st.code(f"""API_KEY={api_key}
MAP_API_KEY={map_api_key}
SMS_API_KEY={sms_api_key}
NOTIFICATION_API_KEY={notification_api_key}""")
        
        st.markdown("---")
        st.markdown("### 当前环境变量")
        st.code(os.getenv('API_KEY', '未设置'))
        st.code(os.getenv('MAP_API_KEY', '未设置'))
        st.code(os.getenv('SMS_API_KEY', '未设置'))
        st.code(os.getenv('NOTIFICATION_API_KEY', '未设置'))
    
    with tab2:
        st.subheader("用户管理")
        
        users = get_users()
        
        if users:
            st.dataframe(
                users,
                column_config={
                    "id": "ID",
                    "name": "姓名",
                    "phone": "电话",
                    "address": "地址",
                    "emergency_contact": "紧急联系人",
                    "created_at": "创建时间"
                },
                use_container_width=True,
                hide_index=True
            )
            
            st.markdown(f"**总计**: {len(users)} 位用户")
        else:
            st.info("暂无用户")
    
    with tab3:
        st.subheader("数据管理")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 数据统计")
            users = get_users()
            alerts = get_alerts()
            
            st.metric("用户总数", len(users))
            st.metric("求助记录总数", len(alerts))
            
            if alerts:
                pending = len([a for a in alerts if a['status'] == 'pending'])
                resolved = len([a for a in alerts if a['status'] == 'resolved'])
                
                st.metric("待处理求助", pending)
                st.metric("已解决求助", resolved)
        
        with col2:
            st.markdown("### 数据导出")
            
            export_format = st.selectbox("导出格式", ["CSV", "JSON"])
            
            if st.button("导出用户数据"):
                if users:
                    if export_format == "CSV":
                        import pandas as pd
                        df = pd.DataFrame(users)
                        csv = df.to_csv(index=False)
                        st.download_button(
                            label="下载用户数据 (CSV)",
                            data=csv,
                            file_name="users_export.csv",
                            mime="text/csv"
                        )
                    else:
                        import json
                        json_data = json.dumps(users, ensure_ascii=False, indent=2)
                        st.download_button(
                            label="下载用户数据 (JSON)",
                            data=json_data,
                            file_name="users_export.json",
                            mime="application/json"
                        )
                else:
                    st.warning("暂无用户数据可导出")
            
            if st.button("导出求助数据"):
                if alerts:
                    if export_format == "CSV":
                        import pandas as pd
                        df = pd.DataFrame(alerts)
                        csv = df.to_csv(index=False)
                        st.download_button(
                            label="下载求助数据 (CSV)",
                            data=csv,
                            file_name="alerts_export.csv",
                            mime="text/csv"
                        )
                    else:
                        import json
                        json_data = json.dumps(alerts, ensure_ascii=False, indent=2)
                        st.download_button(
                            label="下载求助数据 (JSON)",
                            data=json_data,
                            file_name="alerts_export.json",
                            mime="application/json"
                        )
                else:
                    st.warning("暂无求助数据可导出")
        
        st.markdown("---")
        st.warning("⚠️ 危险操作区域")
        
        if st.button("清空所有数据", type="secondary"):
            st.error("此操作将删除所有数据，请谨慎操作！")
            if st.checkbox("我确认要清空所有数据"):
                from utils.database import init_database
                init_database()
                st.success("数据库已重置！")
                st.session_state.rerun = True
                rerun()
