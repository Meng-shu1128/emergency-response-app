import streamlit as st
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.database import get_users, get_alerts, generate_mock_data
from utils.config_manager import get_config_manager, reload_config

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
        
        st.info("在此页面配置API密钥，将自动保存到 .env 文件")
        
        config_manager = get_config_manager()
        config_status = config_manager.get_config_status()
        
        st.markdown("### 当前配置")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**地图API密钥**")
            if config_status['MAP_API_KEY']['configured']:
                if config_status['MAP_API_KEY']['valid']:
                    st.success("✅ 已配置")
                else:
                    st.warning("⚠️ 配置无效")
                st.code(config_status['MAP_API_KEY']['value'])
            else:
                st.warning("⚠️ 未配置")
            
            st.markdown("**天气API密钥**")
            if config_status['WEATHER_API_KEY']['configured']:
                if config_status['WEATHER_API_KEY']['valid']:
                    st.success("✅ 已配置")
                else:
                    st.warning("⚠️ 配置无效")
                st.code(config_status['WEATHER_API_KEY']['value'])
            else:
                st.warning("⚠️ 未配置")
        
        with col2:
            st.markdown("**短信API密钥**")
            if config_status['SMS_API_KEY']['configured']:
                if config_status['SMS_API_KEY']['valid']:
                    st.success("✅ 已配置")
                else:
                    st.warning("⚠️ 配置无效")
                st.code(config_status['SMS_API_KEY']['value'])
            else:
                st.warning("⚠️ 未配置")
            
            st.markdown("**通知API密钥**")
            if config_status['NOTIFICATION_API_KEY']['configured']:
                if config_status['NOTIFICATION_API_KEY']['valid']:
                    st.success("✅ 已配置")
                else:
                    st.warning("⚠️ 配置无效")
                st.code(config_status['NOTIFICATION_API_KEY']['value'])
            else:
                st.warning("⚠️ 未配置")
        
        st.markdown("---")
        st.markdown("### 更新配置")
        
        with st.form("api_config"):
            st.markdown("输入新的API密钥（留空则保持不变）")
            
            new_map_api_key = st.text_input(
                "地图API密钥", 
                type="password", 
                placeholder="留空保持不变",
                help="用于地图显示和位置服务"
            )
            
            new_weather_api_key = st.text_input(
                "天气API密钥", 
                type="password", 
                placeholder="留空保持不变",
                help="用于获取天气信息进行风险评估"
            )
            
            new_sms_api_key = st.text_input(
                "短信API密钥", 
                type="password", 
                placeholder="留空保持不变",
                help="用于发送紧急通知短信"
            )
            
            new_notification_api_key = st.text_input(
                "通知API密钥", 
                type="password", 
                placeholder="留空保持不变",
                help="用于APP推送通知"
            )
            
            submitted = st.form_submit_button("保存并重新加载", type="primary")
            
            if submitted:
                changes_made = False
                validation_errors = []
                
                if new_map_api_key:
                    is_valid, message = config_manager.validate_api_key('MAP_API_KEY', new_map_api_key)
                    if is_valid:
                        config_manager.set('MAP_API_KEY', new_map_api_key)
                        changes_made = True
                    else:
                        validation_errors.append(f"地图API密钥: {message}")
                
                if new_weather_api_key:
                    is_valid, message = config_manager.validate_api_key('WEATHER_API_KEY', new_weather_api_key)
                    if is_valid:
                        config_manager.set('WEATHER_API_KEY', new_weather_api_key)
                        changes_made = True
                    else:
                        validation_errors.append(f"天气API密钥: {message}")
                
                if new_sms_api_key:
                    is_valid, message = config_manager.validate_api_key('SMS_API_KEY', new_sms_api_key)
                    if is_valid:
                        config_manager.set('SMS_API_KEY', new_sms_api_key)
                        changes_made = True
                    else:
                        validation_errors.append(f"短信API密钥: {message}")
                
                if new_notification_api_key:
                    is_valid, message = config_manager.validate_api_key('NOTIFICATION_API_KEY', new_notification_api_key)
                    if is_valid:
                        config_manager.set('NOTIFICATION_API_KEY', new_notification_api_key)
                        changes_made = True
                    else:
                        validation_errors.append(f"通知API密钥: {message}")
                
                if validation_errors:
                    st.error("❌ 配置验证失败：")
                    for error in validation_errors:
                        st.error(f"  - {error}")
                elif changes_made:
                    st.success("✅ 配置已更新，请重启应用！")
                    st.info("💡 点击下方按钮重启应用使新配置生效")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("🔄 立即重启应用", type="primary"):
                            reload_config()
                            st.session_state.rerun = True
                            rerun()
                    with col2:
                        if st.button("📋 查看当前配置"):
                            st.json(config_manager.get_masked_config())
                else:
                    st.warning("⚠️ 没有检测到任何更改")
    
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
            alerts_result = get_alerts()
            
            alerts = alerts_result.get('data', []) if isinstance(alerts_result, dict) else alerts_result
            
            st.metric("用户总数", len(users))
            st.metric("求助记录总数", len(alerts))
            
            if alerts:
                pending = len([a for a in alerts if isinstance(a, dict) and a.get('status') == 'pending'])
                resolved = len([a for a in alerts if isinstance(a, dict) and a.get('status') == 'resolved'])
                
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
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🎲 生成模拟数据", type="primary"):
                st.warning("此操作将生成模拟数据用于演示！")
                if st.checkbox("我确认要生成模拟数据"):
                    with st.spinner("正在生成模拟数据..."):
                        result = generate_mock_data()
                    
                    st.success(f"✅ 模拟数据生成成功！")
                    st.info(f"  - 生成用户: {result['users']} 个")
                    st.info(f"  - 生成历史警报: {result['alerts']} 条")
                    st.info(f"  - 生成今日警报: {result['today_alerts']} 条")
                    st.info(f"  - 总计警报: {result['total_alerts']} 条")
                    st.info("💡 请刷新页面查看数据")
                    
                    if st.button("🔄 立即刷新"):
                        st.session_state.rerun = True
                        rerun()
        
        with col2:
            if st.button("🗑️ 清空所有数据", type="secondary"):
                st.error("此操作将删除所有数据，请谨慎操作！")
                if st.checkbox("我确认要清空所有数据"):
                    from utils.database import init_database
                    init_database()
                    st.success("数据库已重置！")
                    st.session_state.rerun = True
                    rerun()
