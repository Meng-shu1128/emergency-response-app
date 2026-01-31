import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import io

def get_time_range_data(alerts, time_range):
    now = datetime.now()
    
    if time_range == "today":
        start_time = now.replace(hour=0, minute=0, second=0, microsecond=0)
    elif time_range == "week":
        start_time = now - timedelta(days=7)
    elif time_range == "month":
        start_time = now - timedelta(days=30)
    else:
        return alerts
    
    filtered_alerts = []
    for alert in alerts:
        try:
            alert_time = datetime.strptime(alert['alert_time'], "%Y-%m-%d %H:%M:%S")
            if alert_time >= start_time:
                filtered_alerts.append(alert)
        except:
            continue
    
    return filtered_alerts

def create_alert_time_distribution_chart(alerts):
    if not alerts:
        return None
    
    hourly_counts = {i: 0 for i in range(24)}
    
    for alert in alerts:
        try:
            alert_time = datetime.strptime(alert['alert_time'], "%Y-%m-%d %H:%M:%S")
            hour = alert_time.hour
            hourly_counts[hour] += 1
        except:
            continue
    
    hours = list(hourly_counts.keys())
    counts = list(hourly_counts.values())
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=hours,
        y=counts,
        mode='lines+markers',
        name='警报数量',
        line=dict(color='#3366CC', width=3),
        marker=dict(size=8, color='#3366CC')
    ))
    
    fig.update_layout(
        title='24小时内警报数量时间分布',
        xaxis_title='小时',
        yaxis_title='警报数量',
        template='plotly_white',
        height=400,
        margin=dict(l=50, r=50, t=50, b=50)
    )
    
    fig.update_xaxes(
        tickmode='linear',
        tick0=0,
        dtick=2
    )
    
    return fig

def create_risk_level_pie_chart(alerts):
    if not alerts:
        return None
    
    risk_counts = {'low': 0, 'medium': 0, 'high': 0}
    
    for alert in alerts:
        risk_level = alert.get('risk_level', 'low').lower()
        if risk_level in risk_counts:
            risk_counts[risk_level] += 1
    
    labels = ['低风险', '中风险', '高风险']
    values = [risk_counts['low'], risk_counts['medium'], risk_counts['high']]
    colors = ['#66BB6A', '#FFA726', '#EF5350']
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        marker=dict(colors=colors),
        textinfo='label+percent',
        textposition='inside',
        hole=0.3
    )])
    
    fig.update_layout(
        title='风险等级分布',
        template='plotly_white',
        height=400,
        margin=dict(l=50, r=50, t=50, b=50)
    )
    
    return fig

def create_response_time_boxplot(alerts, response_logs):
    if not alerts or not response_logs:
        return None
    
    alert_response_times = {}
    
    for log in response_logs:
        alert_id = log.get('alert_id')
        action_time_str = log.get('action_time')
        
        if alert_id and action_time_str:
            try:
                action_time = datetime.strptime(action_time_str, "%Y-%m-%d %H:%M:%S")
                
                if alert_id not in alert_response_times:
                    alert_response_times[alert_id] = []
                
                alert_response_times[alert_id].append(action_time)
            except:
                continue
    
    response_times_by_risk = {'low': [], 'medium': [], 'high': []}
    
    for alert in alerts:
        alert_id = alert.get('id')
        alert_time_str = alert.get('alert_time')
        risk_level = alert.get('risk_level', 'low').lower()
        
        if alert_id in alert_response_times and alert_time_str:
            try:
                alert_time = datetime.strptime(alert_time_str, "%Y-%m-%d %H:%M:%S")
                first_response_time = min(alert_response_times[alert_id])
                response_minutes = (first_response_time - alert_time).total_seconds() / 60
                
                if risk_level in response_times_by_risk:
                    response_times_by_risk[risk_level].append(response_minutes)
            except:
                continue
    
    fig = go.Figure()
    
    risk_labels = {'low': '低风险', 'medium': '中风险', 'high': '高风险'}
    risk_colors = {'low': '#66BB6A', 'medium': '#FFA726', 'high': '#EF5350'}
    
    for risk_level, times in response_times_by_risk.items():
        if times:
            fig.add_trace(go.Box(
                y=times,
                name=risk_labels[risk_level],
                marker_color=risk_colors[risk_level],
                boxmean='sd'
            ))
    
    if fig.data:
        fig.update_layout(
            title='响应时间分布（分钟）',
            yaxis_title='响应时间（分钟）',
            template='plotly_white',
            height=400,
            margin=dict(l=50, r=50, t=50, b=50),
            showlegend=True
        )
        return fig
    
    return None

def calculate_metrics(alerts, response_logs):
    metrics = {
        'total_alerts': len(alerts),
        'pending_alerts': 0,
        'processing_alerts': 0,
        'resolved_alerts': 0,
        'high_risk_alerts': 0,
        'avg_response_time': 0,
        'response_rate': 0
    }
    
    if not alerts:
        return metrics
    
    for alert in alerts:
        status = alert.get('status', 'pending')
        risk_level = alert.get('risk_level', 'low').lower()
        
        if status == 'pending':
            metrics['pending_alerts'] += 1
        elif status == 'processing':
            metrics['processing_alerts'] += 1
        elif status == 'resolved':
            metrics['resolved_alerts'] += 1
        
        if risk_level == 'high':
            metrics['high_risk_alerts'] += 1
    
    if alerts and response_logs:
        alert_response_times = {}
        
        for log in response_logs:
            alert_id = log.get('alert_id')
            action_time_str = log.get('action_time')
            
            if alert_id and action_time_str:
                try:
                    action_time = datetime.strptime(action_time_str, "%Y-%m-%d %H:%M:%S")
                    
                    if alert_id not in alert_response_times:
                        alert_response_times[alert_id] = []
                    
                    alert_response_times[alert_id].append(action_time)
                except:
                    continue
        
        response_times = []
        
        for alert in alerts:
            alert_id = alert.get('id')
            alert_time_str = alert.get('alert_time')
            
            if alert_id in alert_response_times and alert_time_str:
                try:
                    alert_time = datetime.strptime(alert_time_str, "%Y-%m-%d %H:%M:%S")
                    first_response_time = min(alert_response_times[alert_id])
                    response_minutes = (first_response_time - alert_time).total_seconds() / 60
                    response_times.append(response_minutes)
                except:
                    continue
        
        if response_times:
            metrics['avg_response_time'] = round(sum(response_times) / len(response_times), 2)
        
        metrics['response_rate'] = round(len(alert_response_times) / len(alerts) * 100, 1)
    
    return metrics

def export_to_csv(data, filename):
    df = pd.DataFrame(data)
    csv = df.to_csv(index=False, encoding='utf-8-sig')
    st.download_button(
        label="📥 导出CSV",
        data=csv,
        file_name=filename,
        mime="text/csv"
    )

def show_dashboard_analytics(alerts, response_logs):
    st.subheader("📈 应急响应数据看板")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        time_range = st.selectbox(
            "时间范围",
            options=["today", "week", "month", "all"],
            format_func=lambda x: {
                "today": "今天",
                "week": "本周",
                "month": "本月",
                "all": "全部"
            }.get(x, x),
            index=0,
            key="analytics_time_range"
        )
    
    with col2:
        show_export = st.checkbox("显示导出按钮", value=True, key="analytics_show_export")
    
    with col3:
        auto_refresh = st.checkbox("自动刷新", value=False, key="analytics_auto_refresh")
    
    if auto_refresh:
        st.rerun()
    
    filtered_alerts = get_time_range_data(alerts, time_range)
    
    metrics = calculate_metrics(filtered_alerts, response_logs)
    
    st.markdown("---")
    
    st.markdown("### 📊 关键指标")
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        st.metric("总警报数", metrics['total_alerts'])
    
    with col2:
        st.metric("待处理", metrics['pending_alerts'], delta_color="inverse")
    
    with col3:
        st.metric("处理中", metrics['processing_alerts'])
    
    with col4:
        st.metric("已解决", metrics['resolved_alerts'], delta_color="normal")
    
    with col5:
        st.metric("高风险", metrics['high_risk_alerts'], delta_color="inverse")
    
    with col6:
        st.metric("响应率", f"{metrics['response_rate']}%")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("平均响应时间", f"{metrics['avg_response_time']}分钟")
    
    with col2:
        if time_range == "today":
            st.metric("时间范围", "今天")
        elif time_range == "week":
            st.metric("时间范围", "本周")
        elif time_range == "month":
            st.metric("时间范围", "本月")
        else:
            st.metric("时间范围", "全部")
    
    st.markdown("---")
    
    tab1, tab2, tab3 = st.tabs(["📈 时间分布", "🥧 风险分布", "📦 响应时间"])
    
    with tab1:
        st.markdown("### 24小时内警报数量时间分布")
        
        time_chart = create_alert_time_distribution_chart(filtered_alerts)
        
        if time_chart:
            st.plotly_chart(time_chart, use_container_width=True)
            
            if show_export and filtered_alerts:
                export_to_csv(filtered_alerts, f"alert_time_distribution_{time_range}.csv")
        else:
            st.info("暂无数据")
    
    with tab2:
        st.markdown("### 风险等级分布")
        
        risk_chart = create_risk_level_pie_chart(filtered_alerts)
        
        if risk_chart:
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.plotly_chart(risk_chart, use_container_width=True)
            
            with col2:
                st.markdown("#### 统计摘要")
                
                risk_counts = {'low': 0, 'medium': 0, 'high': 0}
                
                for alert in filtered_alerts:
                    risk_level = alert.get('risk_level', 'low').lower()
                    if risk_level in risk_counts:
                        risk_counts[risk_level] += 1
                
                st.metric("低风险", risk_counts['low'])
                st.metric("中风险", risk_counts['medium'])
                st.metric("高风险", risk_counts['high'])
            
            if show_export and filtered_alerts:
                export_to_csv(filtered_alerts, f"risk_level_distribution_{time_range}.csv")
        else:
            st.info("暂无数据")
    
    with tab3:
        st.markdown("### 响应时间分布")
        
        response_chart = create_response_time_boxplot(filtered_alerts, response_logs)
        
        if response_chart:
            st.plotly_chart(response_chart, use_container_width=True)
            
            if show_export and filtered_alerts:
                export_to_csv(filtered_alerts, f"response_time_{time_range}.csv")
        else:
            st.info("暂无数据")
    
    st.markdown("---")
    
    with st.expander("📋 详细数据"):
        if filtered_alerts:
            df = pd.DataFrame(filtered_alerts)
            st.dataframe(df, use_container_width=True)
            
            if show_export:
                export_to_csv(filtered_alerts, f"alerts_detail_{time_range}.csv")
        else:
            st.info("暂无数据")
