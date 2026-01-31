import streamlit as st
import sys
import os
import re
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.database import add_user, create_alert, get_user_by_id
from utils.voice_player import show_voice_player, play_soothing_message
from utils.risk_assessment import RiskAssessment, show_risk_assessment_ui
from utils.notification_system import show_notification_system_ui, send_emergency_notification


def validate_phone(phone):
    if not phone:
        return False, "电话号码不能为空"
    
    if not phone.isdigit():
        return False, "电话号码必须为数字"
    
    if len(phone) != 11:
        return False, "电话号码必须为11位"
    
    if not phone.startswith('1'):
        return False, "电话号码必须以1开头"
    
    return True, "验证通过"


def validate_user_form(name, phone, emergency_contact):
    errors = []
    
    if not name or not name.strip():
        errors.append("姓名不能为空")
    
    is_valid, message = validate_phone(phone)
    if not is_valid:
        errors.append(message)
    
    if emergency_contact and emergency_contact.strip():
        is_valid, message = validate_phone(emergency_contact)
        if not is_valid:
            errors.append(f"紧急联系人{message}")
        
        if emergency_contact == phone:
            errors.append("紧急联系人电话不能与本人电话相同")
    
    return len(errors) == 0, errors


def validate_alert_form(description):
    errors = []
    
    if not description or not description.strip():
        errors.append("紧急情况描述不能为空")
    
    return len(errors) == 0, errors

def show_elderly_page():
    st.title("👴 老人端模拟界面")
    st.markdown("---")
    
    if "elderly_user_id" not in st.session_state:
        st.session_state.elderly_user_id = None
    
    if "elderly_quick_help" not in st.session_state:
        st.session_state.elderly_quick_help = None
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📝 用户信息")
        with st.form("user_form"):
            name = st.text_input("姓名", placeholder="请输入姓名")
            phone = st.text_input("电话", placeholder="请输入电话号码")
            address = st.text_input("地址", placeholder="请输入家庭地址")
            emergency_contact = st.text_input("紧急联系人", placeholder="请输入紧急联系人电话")
            
            if st.form_submit_button("注册/更新用户信息", type="primary"):
                is_valid, errors = validate_user_form(name, phone, emergency_contact)
                
                if is_valid:
                    user_id = add_user(name, phone, address, emergency_contact)
                    st.session_state.elderly_user_id = user_id
                    st.success(f"用户信息已保存！用户ID: {user_id}")
                    st.balloons()
                else:
                    st.error("❌ 表单验证失败：")
                    for error in errors:
                        st.error(f"  - {error}")
    
    with col2:
        st.subheader("🚨 发起紧急求助")
        
        if st.session_state.elderly_user_id:
            with st.spinner("正在加载用户信息..."):
                user = get_user_by_id(st.session_state.elderly_user_id)
            if user:
                st.info(f"当前用户: {user['name']} ({user['phone']})")
        
        weather_options = ["晴", "多云", "阴", "小雨", "中雨", "大雨", "暴雨", "雷阵雨", "雪", "大雾", "沙尘暴"]
        weather = st.selectbox("当前天气", options=weather_options, index=0, key="elderly_weather")
        
        col_lat, col_lng = st.columns(2)
        with col_lat:
            location_lat = st.number_input("纬度", value=39.9042, format="%.6f", key="elderly_lat")
        with col_lng:
            location_lng = st.number_input("经度", value=116.4074, format="%.6f", key="elderly_lng")
        
        quick_help_description = st.session_state.elderly_quick_help if st.session_state.elderly_quick_help else ""
        
        with st.form("alert_form"):
            description = st.text_area(
                "紧急情况描述", 
                value=quick_help_description,
                placeholder="请描述您遇到的紧急情况...",
                key="elderly_description"
            )
            risk_level = st.selectbox("风险等级", ["低", "中", "高"], index=1)
            
            if st.form_submit_button("🆘 发送紧急求助", type="primary"):
                if st.session_state.elderly_user_id:
                    is_valid, errors = validate_alert_form(description)
                    
                    if is_valid:
                        alert_id = create_alert(
                            user_id=st.session_state.elderly_user_id,
                            location_lat=location_lat,
                            location_lng=location_lng,
                            risk_level=risk_level.lower(),
                            description=description
                        )
                        st.success(f"紧急求助已发送！求助ID: {alert_id}")
                        st.balloons()
                        st.session_state.elderly_quick_help = None
                    else:
                        st.error("❌ 表单验证失败：")
                        for error in errors:
                            st.error(f"  - {error}")
                else:
                    st.error("❌ 请先注册用户信息！")
        
        st.markdown("---")
        st.subheader("🎯 自动风险评估")
        
        assessor = RiskAssessment()
        result = assessor.assess_risk(location_lat, location_lng, None, weather)
        
        risk_emoji = {
            "low": "🟢",
            "medium": "🟡",
            "high": "🔴"
        }
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("评估风险等级", f"{risk_emoji.get(result['risk_level'], '⚪')} {result['risk_level'].upper()}")
        
        with col2:
            st.metric("风险评分", result['risk_score'])
        
        with col3:
            st.metric("天气", weather)
        
        if result['risk_factors']:
            st.markdown("### 风险因素")
            for factor in result['risk_factors']:
                st.write(f"- {factor['factor']}: {factor['description']}")
        
        if result['suggestions']:
            st.markdown("### 建议措施")
            for suggestion in result['suggestions']:
                st.write(f"• {suggestion}")
    
    st.markdown("---")
    st.subheader("📱 快捷求助按钮")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🏥 医疗急救", use_container_width=True, type="primary"):
            st.session_state.elderly_quick_help = "医疗急救需要"
            st.success("已选择医疗急救，请点击下方发送按钮")
    
    with col2:
        if st.button("🔥 火灾报警", use_container_width=True, type="primary"):
            st.session_state.elderly_quick_help = "火灾报警需要"
            st.success("已选择火灾报警，请点击下方发送按钮")
    
    with col3:
        if st.button("👮 治安求助", use_container_width=True, type="primary"):
            st.session_state.elderly_quick_help = "治安求助需要"
            st.success("已选择治安求助，请点击下方发送按钮")
    
    st.markdown("---")
    
    tab1, tab2, tab3, tab4 = st.tabs(["🔊 语音安抚", "📝 自定义语音", "🎯 风险评估", "📢 通知系统"])
    
    with tab1:
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
    
    with tab2:
        custom_text = st.text_area("输入自定义安抚语音", placeholder="请输入要播放的安抚语音文本...", height=150)
        if custom_text:
            show_voice_player(custom_text=custom_text)
    
    with tab3:
        show_risk_assessment_ui()
    
    with tab4:
        show_notification_system_ui()
