import streamlit as st
import random
import time
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.database import get_users, create_alert

VILLAGE_BOUNDARIES = {
    'village_1': {
        'name': '东村',
        'lat_range': (39.90, 39.92),
        'lng_range': (116.40, 116.42)
    },
    'village_2': {
        'name': '西村',
        'lat_range': (39.88, 39.90),
        'lng_range': (116.38, 116.40)
    },
    'village_3': {
        'name': '南村',
        'lat_range': (39.86, 39.88),
        'lng_range': (116.40, 116.42)
    },
    'village_4': {
        'name': '北村',
        'lat_range': (39.92, 39.94),
        'lng_range': (116.38, 116.40)
    }
}

ALERT_DESCRIPTIONS = [
    '老人跌倒需要帮助',
    '突发疾病需要急救',
    '家中失火',
    '发现可疑人员',
    '迷路需要帮助',
    '突发心脏病',
    '燃气泄漏',
    '触电事故',
    '突发晕厥'
]

RISK_LEVELS = ['low', 'medium', 'high']

def generate_random_location():
    village_key = random.choice(list(VILLAGE_BOUNDARIES.keys()))
    village = VILLAGE_BOUNDARIES[village_key]
    
    lat = random.uniform(village['lat_range'][0], village['lat_range'][1])
    lng = random.uniform(village['lng_range'][0], village['lng_range'][1])
    
    return {
        'lat': round(lat, 6),
        'lng': round(lng, 6),
        'village': village['name']
    }

def generate_random_alert():
    users = get_users()
    
    if not users:
        return None
    
    user = random.choice(users)
    location = generate_random_location()
    risk_level = random.choice(RISK_LEVELS)
    description = random.choice(ALERT_DESCRIPTIONS)
    
    alert_id = create_alert(
        user_id=user['id'],
        location_lat=location['lat'],
        location_lng=location['lng'],
        risk_level=risk_level,
        description=description
    )
    
    return {
        'id': alert_id,
        'user_name': user['name'],
        'user_phone': user['phone'],
        'location': location,
        'risk_level': risk_level,
        'description': description,
        'village': location['village']
    }

def run_alert_simulation(interval_seconds=30):
    if "simulation_running" not in st.session_state:
        st.session_state.simulation_running = False
    
    if "simulation_logs" not in st.session_state:
        st.session_state.simulation_logs = []
    
    st.subheader("🔄 实时警报模拟")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        start_button = st.button("▶️ 开始模拟", type="primary", disabled=st.session_state.simulation_running)
    
    with col2:
        stop_button = st.button("⏹️ 停止模拟", type="secondary", disabled=not st.session_state.simulation_running)
    
    st.markdown("---")
    
    if start_button:
        st.session_state.simulation_running = True
        st.session_state.simulation_logs = []
        st.success("模拟已启动！每30秒生成一条随机警报。")
        st.rerun()
    
    if stop_button:
        st.session_state.simulation_running = False
        st.warning("模拟已停止！")
        st.rerun()
    
    if st.session_state.simulation_running:
        status_container = st.empty()
        log_container = st.empty()
        
        status_container.info("🟢 模拟运行中...")
        
        while st.session_state.simulation_running:
            alert = generate_random_alert()
            
            if alert:
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                log_entry = {
                    'timestamp': timestamp,
                    'alert': alert
                }
                st.session_state.simulation_logs.insert(0, log_entry)
                
                if len(st.session_state.simulation_logs) > 10:
                    st.session_state.simulation_logs.pop()
                
                with log_container.container():
                    st.subheader("### 📋 模拟日志")
                    
                    for log in st.session_state.simulation_logs:
                        alert_data = log['alert']
                        risk_emoji = {
                            'low': '🟢',
                            'medium': '🟡',
                            'high': '🔴'
                        }
                        
                        with st.container():
                            col1, col2 = st.columns([3, 1])
                            with col1:
                                st.markdown(f"""
                                **{log['timestamp']}** - {risk_emoji.get(alert_data['risk_level'], '🔵')} {alert_data['risk_level'].upper()} 风险
                                - **用户**: {alert_data['user_name']}
                                - **位置**: {alert_data['village']} ({alert_data['location']['lat']}, {alert_data['location']['lng']})
                                - **描述**: {alert_data['description']}
                                """)
                            with col2:
                                st.markdown(f"#{alert_data['id']}")
                            st.markdown("---")
                    
                    st.markdown(f"**已生成 {len(st.session_state.simulation_logs)} 条警报记录**")
            
            time.sleep(interval_seconds)
            
            if not st.session_state.simulation_running:
                break
        
        status_container.warning("⏹️ 模拟已停止")
    else:
        st.info("点击 '开始模拟' 按钮启动实时警报生成")
        
        if st.session_state.simulation_logs:
            st.markdown("---")
            st.subheader("### 📋 上次模拟日志")
            
            for log in st.session_state.simulation_logs:
                alert_data = log['alert']
                risk_emoji = {
                    'low': '🟢',
                    'medium': '🟡',
                    'high': '🔴'
                }
                
                with st.container():
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"""
                        **{log['timestamp']}** - {risk_emoji.get(alert_data['risk_level'], '🔵')} {alert_data['risk_level'].upper()} 风险
                        - **用户**: {alert_data['user_name']}
                        - **位置**: {alert_data['village']} ({alert_data['location']['lat']}, {alert_data['location']['lng']})
                        - **描述**: {alert_data['description']}
                        """)
                    with col2:
                        st.markdown(f"#{alert_data['id']}")
                    st.markdown("---")
            
            st.markdown(f"**共 {len(st.session_state.simulation_logs)} 条记录**")
