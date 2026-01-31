import streamlit as st
import pandas as pd
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.database import get_alerts_with_details, get_statistics, update_alert_status, add_response_log, get_response_logs
from utils.map_component import display_alert_map, create_single_alert_map
from utils.alert_simulator import run_alert_simulation
from utils.voice_player import show_voice_player
from utils.risk_assessment import RiskAssessment, show_risk_assessment_ui
from utils.dashboard_analytics import show_dashboard_analytics
from utils.notification_system import show_notification_system_ui, send_emergency_notification
from streamlit_folium import st_folium

def rerun():
    if 'rerun' not in st.session_state:
        st.session_state.rerun = False
    
    if st.session_state.rerun:
        st.session_state.rerun = False
        st.experimental_rerun()

@st.cache_data(ttl=30)
def _load_dashboard_stats():
    return get_statistics()

def show_dashboard():
    st.title("📊 后台仪表盘")
    st.markdown("---")
    
    with st.spinner("正在加载统计数据..."):
        stats = _load_dashboard_stats()
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("总用户数", stats['total_users'])
    
    with col2:
        st.metric("总求助数", stats['total_alerts'])
    
    with col3:
        st.metric("待处理", stats['pending_alerts'], delta_color="inverse")
    
    with col4:
        st.metric("已解决", stats['resolved_alerts'], delta_color="normal")
    
    with col5:
        st.metric("高风险", stats['high_risk_alerts'], delta_color="inverse")
    
    st.markdown("---")
    
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(["🗺️ 求助地图", "📋 求助列表", "📝 响应日志", "🔄 实时模拟", "🔊 语音安抚", "🎯 风险评估", "📈 数据看板", "📢 通知系统"])
    
    with tab1:
        with st.spinner("正在加载地图数据..."):
            alerts_result = get_alerts_with_details(page=1, page_size=100)
            alerts = alerts_result['data']
        
        display_alert_map(
            alerts=alerts,
            center_lat=39.9042,
            center_lng=116.4074,
            zoom=10,
            height=500,
            show_layer_control=True,
            show_pending_only=False,
            show_risk_filter=True
        )
    
    with tab2:
        st.subheader("求助列表")
        
        if "alerts_page" not in st.session_state:
            st.session_state.alerts_page = 1
        
        if "alerts_page_size" not in st.session_state:
            st.session_state.alerts_page_size = 10
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            status_filter = st.multiselect(
                "筛选状态",
                options=["pending", "processing", "resolved"],
                default=["pending", "processing", "resolved"],
                key="alert_status_filter"
            )
        
        with col2:
            page_size = st.selectbox(
                "每页显示",
                options=[5, 10, 20, 50],
                index=1,
                key="alert_page_size_select"
            )
            st.session_state.alerts_page_size = page_size
        
        with col3:
            st.caption(f"当前页: {st.session_state.alerts_page}")
        
        alerts_result = get_alerts_with_details(page=st.session_state.alerts_page, page_size=st.session_state.alerts_page_size)
        alerts = alerts_result['data']
        
        if alerts:
            df = pd.DataFrame(alerts)
            
            if status_filter:
                df = df[df['status'].isin(status_filter)]
            
            if not df.empty:
                for idx, alert in df.iterrows():
                    with st.expander(f"求助 #{alert['id']} - {alert['user_name']} - {alert['alert_time']}", expanded=alert['status'] == 'pending'):
                        col1, col2 = st.columns([2, 1])
                        
                        with col1:
                            st.write(f"**用户**: {alert['user_name']}")
                            st.write(f"**电话**: {alert['user_phone']}")
                            st.write(f"**地址**: {alert['user_address']}")
                            st.write(f"**位置**: {alert['location_lat']}, {alert['location_lng']}")
                            st.write(f"**描述**: {alert['description'] or '无'}")
                            
                            risk_badge = {
                                'low': '🟢 低风险',
                                'medium': '🟡 中风险',
                                'high': '🔴 高风险'
                            }
                            st.write(f"**风险等级**: {risk_badge.get(alert['risk_level'], alert['risk_level'])}")
                            
                            if alert.get('location_lat') and alert.get('location_lng'):
                                st.markdown("---")
                                st.markdown("#### 位置地图")
                                m = create_single_alert_map(alert, height=300)
                                st_folium(m, width='100%', height=300)
                        
                        with col2:
                            status_badge = {
                                'pending': '⏳ 待处理',
                                'processing': '🔄 处理中',
                                'resolved': '✅ 已解决'
                            }
                            st.write(f"**状态**: {status_badge.get(alert['status'], alert['status'])}")
                            
                            if alert['status'] == 'pending':
                                if st.button("开始处理", key=f"process_{alert['id']}", use_container_width=True):
                                    update_alert_status(alert['id'], 'processing')
                                    add_response_log(alert['id'], '系统', '状态更新', '求助开始处理')
                                    st.session_state.rerun = True
                                    rerun()
                            
                            if alert['status'] == 'processing':
                                if st.button("标记为已解决", key=f"resolve_{alert['id']}", use_container_width=True):
                                    update_alert_status(alert['id'], 'resolved')
                                    add_response_log(alert['id'], '系统', '状态更新', '求助已解决')
                                    st.session_state.rerun = True
                                    rerun()
                            
                            with st.form(f"response_form_{alert['id']}"):
                                responder = st.text_input("响应人员", placeholder="请输入姓名")
                                action_type = st.selectbox("操作类型", ["电话联系", "现场处理", "派遣救援", "其他"])
                                notes = st.text_area("备注", placeholder="请输入操作备注...")
                                
                                if st.form_submit_button("添加响应记录", use_container_width=True):
                                    if responder:
                                        add_response_log(alert['id'], responder, action_type, notes)
                                        st.success("响应记录已添加！")
                                        st.session_state.rerun = True
                                        rerun()
                                    else:
                                        st.error("请输入响应人员姓名！")
                
                st.markdown("---")
                
                st.markdown(f"共 {alerts_result['total']} 条记录，第 {alerts_result['page']} / {alerts_result['total_pages']} 页")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("⬅️ 上一页", disabled=alerts_result['page'] <= 1, key="alert_prev_page"):
                        st.session_state.alerts_page -= 1
                        st.session_state.rerun = True
                        rerun()
                
                with col2:
                    st.write(f"第 {alerts_result['page']} 页 / 共 {alerts_result['total_pages']} 页")
                
                with col3:
                    if st.button("➡️ 下一页", disabled=alerts_result['page'] >= alerts_result['total_pages'], key="alert_next_page"):
                        st.session_state.alerts_page += 1
                        st.session_state.rerun = True
                        rerun()
            else:
                st.info("没有符合条件的求助记录")
        else:
            st.info("暂无求助记录")
    
    with tab3:
        st.subheader("响应日志")
        
        alert_options = get_alerts_with_details(page=1, page_size=1000)['data']
        
        selected_alert_id = st.selectbox(
            "选择求助记录查看日志",
            options=[alert['id'] for alert in alert_options],
            format_func=lambda x: f"求助 #{x}"
        )
        
        if selected_alert_id:
            logs = get_response_logs(selected_alert_id)
            
            if logs:
                for log in logs:
                    with st.container():
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.write(f"**{log['action_time']}** - {log['responder']} - {log['action_type']}")
                            if log['notes']:
                                st.write(f"备注: {log['notes']}")
                        with col2:
                            st.caption(log['action_time'])
                        st.markdown("---")
            else:
                st.info("该求助暂无响应记录")
    
    with tab4:
        run_alert_simulation(interval_seconds=30)
    
    with tab5:
        st.subheader("🔊 语音安抚播放器")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 预设安抚语音")
            alert_type = st.selectbox(
                "选择警报类型",
                options=["general", "fall", "medical", "fire"],
                format_func=lambda x: {
                    "general": "一般求助",
                    "fall": "跌倒求助",
                    "medical": "医疗急救",
                    "fire": "火灾报警"
                }.get(x, x),
                index=0
            )
            show_voice_player(alert_type=alert_type)
        
        with col2:
            st.markdown("### 自定义安抚语音")
            custom_text = st.text_area("输入自定义安抚语音", placeholder="请输入要播放的安抚语音文本...", height=150, key="dashboard_custom_text")
            if custom_text:
                show_voice_player(custom_text=custom_text)
            else:
                st.info("输入文本后显示播放器")
    
    with tab6:
        show_risk_assessment_ui()
    
    with tab7:
        alerts = get_alerts_with_details()
        all_response_logs = []
        
        for alert in alerts:
            logs = get_response_logs(alert['id'])
            all_response_logs.extend(logs)
        
        show_dashboard_analytics(alerts, all_response_logs)
    
    with tab8:
        show_notification_system_ui()
