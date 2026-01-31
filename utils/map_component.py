import streamlit as st
import folium
from streamlit_folium import st_folium
from typing import List, Dict, Optional
import hashlib

RISK_LEVEL_COLORS = {
    'low': 'green',
    'medium': 'orange',
    'high': 'red'
}

RISK_LEVEL_ICONS = {
    'low': 'info-sign',
    'medium': 'exclamation-sign',
    'high': 'fire'
}

def _get_alerts_hash(alerts: List[Dict]) -> str:
    alert_str = str(sorted([(a.get('id', 0), a.get('status', ''), a.get('risk_level', '')) for a in alerts]))
    return hashlib.md5(alert_str.encode()).hexdigest()

@st.cache_data(ttl=300)
def create_alert_map(
    alerts: List[Dict],
    center_lat: float = 39.9042,
    center_lng: float = 116.4074,
    zoom: int = 10,
    height: int = 500,
    show_layer_control: bool = True
) -> folium.Map:
    m = folium.Map(
        location=[center_lat, center_lng],
        zoom_start=zoom,
        control_scale=True
    )
    
    folium.TileLayer('OpenStreetMap').add_to(m)
    
    if show_layer_control:
        folium.LayerControl().add_to(m)
    
    if alerts:
        for alert in alerts:
            if alert.get('location_lat') and alert.get('location_lng'):
                lat = alert['location_lat']
                lng = alert['location_lng']
                risk_level = alert.get('risk_level', 'medium').lower()
                
                color = RISK_LEVEL_COLORS.get(risk_level, 'blue')
                
                popup_content = f"""
                <div style="min-width: 200px;">
                    <h4>求助 #{alert.get('id', 'N/A')}</h4>
                    <p><b>用户:</b> {alert.get('user_name', 'N/A')}</p>
                    <p><b>电话:</b> {alert.get('user_phone', 'N/A')}</p>
                    <p><b>时间:</b> {alert.get('alert_time', 'N/A')}</p>
                    <p><b>地址:</b> {alert.get('user_address', 'N/A')}</p>
                    <p><b>风险等级:</b> {risk_level.upper()}</p>
                    <p><b>描述:</b> {alert.get('description', '无') or '无'}</p>
                    <p><b>状态:</b> {alert.get('status', 'N/A')}</p>
                </div>
                """
                
                folium.Marker(
                    location=[lat, lng],
                    popup=folium.Popup(popup_content, max_width=300),
                    icon=folium.Icon(color=color, icon=RISK_LEVEL_ICONS.get(risk_level, 'info-sign'))
                ).add_to(m)
    
    return m

def display_alert_map(
    alerts: List[Dict],
    center_lat: float = 39.9042,
    center_lng: float = 116.4074,
    zoom: int = 10,
    height: int = 500,
    show_layer_control: bool = True,
    show_pending_only: bool = False,
    show_risk_filter: bool = True
):
    filtered_alerts = alerts
    
    if show_pending_only:
        filtered_alerts = [a for a in alerts if a.get('status') == 'pending']
    
    if show_risk_filter:
        with st.expander("🎯 风险等级筛选", expanded=False):
            risk_levels = ['low', 'medium', 'high']
            selected_risks = []
            for risk in risk_levels:
                if st.checkbox(f"{'🟢' if risk == 'low' else '🟡' if risk == 'medium' else '🔴'} {risk.upper()} 风险", value=True, key=f"risk_filter_{risk}"):
                    selected_risks.append(risk)
            
            if selected_risks:
                filtered_alerts = [a for a in filtered_alerts if a.get('risk_level', '').lower() in selected_risks]
            else:
                filtered_alerts = []
    
    st.subheader("🗺️ 求助地图")
    
    if filtered_alerts:
        col1, col2 = st.columns([3, 1])
        
        with col2:
            st.markdown("### 图例")
            st.markdown("🔴 高风险")
            st.markdown("🟡 中风险")
            st.markdown("🟢 低风险")
            
            st.markdown("---")
            st.markdown(f"**显示点数**: {len(filtered_alerts)}")
        
        with col1:
            if filtered_alerts:
                center_lat = filtered_alerts[0].get('location_lat', center_lat)
                center_lng = filtered_alerts[0].get('location_lng', center_lng)
            
            with st.spinner("正在加载地图..."):
                m = create_alert_map(
                    alerts=filtered_alerts,
                    center_lat=center_lat,
                    center_lng=center_lng,
                    zoom=zoom,
                    height=height,
                    show_layer_control=show_layer_control
                )
                
                st_folium(m, width='100%', height=height, key=f"map_{_get_alerts_hash(filtered_alerts)}")
    else:
        st.info("没有符合条件的求助记录可显示")

def create_single_alert_map(
    alert: Dict,
    height: int = 400
) -> folium.Map:
    if alert.get('location_lat') and alert.get('location_lng'):
        lat = alert['location_lat']
        lng = alert['location_lng']
    else:
        lat = 39.9042
        lng = 116.4074
    
    m = folium.Map(
        location=[lat, lng],
        zoom_start=15,
        control_scale=True
    )
    
    folium.TileLayer('OpenStreetMap').add_to(m)
    
    risk_level = alert.get('risk_level', 'medium').lower()
    color = RISK_LEVEL_COLORS.get(risk_level, 'blue')
    
    popup_content = f"""
    <div style="min-width: 200px;">
        <h4>求助 #{alert.get('id', 'N/A')}</h4>
        <p><b>用户:</b> {alert.get('user_name', 'N/A')}</p>
        <p><b>电话:</b> {alert.get('user_phone', 'N/A')}</p>
        <p><b>时间:</b> {alert.get('alert_time', 'N/A')}</p>
        <p><b>地址:</b> {alert.get('user_address', 'N/A')}</p>
        <p><b>风险等级:</b> {risk_level.upper()}</p>
        <p><b>描述:</b> {alert.get('description', '无') or '无'}</p>
        <p><b>状态:</b> {alert.get('status', 'N/A')}</p>
    </div>
    """
    
    folium.Marker(
        location=[lat, lng],
        popup=folium.Popup(popup_content, max_width=300),
        icon=folium.Icon(color=color, icon=RISK_LEVEL_ICONS.get(risk_level, 'info-sign'))
    ).add_to(m)
    
    return m
