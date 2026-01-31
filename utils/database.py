import sqlite3
import os
import streamlit as st
from datetime import datetime
from typing import List, Dict, Optional

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'emergency_response.db')

def init_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            address TEXT,
            emergency_contact TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            alert_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            location_lat REAL,
            location_lng REAL,
            status TEXT DEFAULT 'pending',
            risk_level TEXT DEFAULT 'medium',
            description TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS response_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            alert_id INTEGER NOT NULL,
            responder TEXT NOT NULL,
            action_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            action_type TEXT NOT NULL,
            notes TEXT,
            FOREIGN KEY (alert_id) REFERENCES alerts (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def add_user(name: str, phone: str, address: str = None, emergency_contact: str = None) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO users (name, phone, address, emergency_contact) VALUES (?, ?, ?, ?)',
        (name, phone, address, emergency_contact)
    )
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    return user_id

@st.cache_data(ttl=300)
def get_users() -> List[Dict]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users ORDER BY created_at DESC')
    users = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return users

@st.cache_data(ttl=300)
def get_user_by_id(user_id: int) -> Optional[Dict]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    return dict(user) if user else None

def create_alert(user_id: int, location_lat: float = None, location_lng: float = None, 
                 risk_level: str = 'medium', description: str = None) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO alerts (user_id, location_lat, location_lng, risk_level, description) VALUES (?, ?, ?, ?, ?)',
        (user_id, location_lat, location_lng, risk_level, description)
    )
    conn.commit()
    alert_id = cursor.lastrowid
    conn.close()
    return alert_id

@st.cache_data(ttl=60)
def get_alerts(status: str = None, page: int = 1, page_size: int = 50) -> Dict:
    conn = get_connection()
    cursor = conn.cursor()
    
    offset = (page - 1) * page_size
    
    if status:
        cursor.execute('SELECT * FROM alerts WHERE status = ? ORDER BY alert_time DESC LIMIT ? OFFSET ?', (status, page_size, offset))
    else:
        cursor.execute('SELECT * FROM alerts ORDER BY alert_time DESC LIMIT ? OFFSET ?', (page_size, offset))
    alerts = [dict(row) for row in cursor.fetchall()]
    
    if status:
        cursor.execute('SELECT COUNT(*) FROM alerts WHERE status = ?', (status,))
    else:
        cursor.execute('SELECT COUNT(*) FROM alerts')
    total_count = cursor.fetchone()[0]
    
    conn.close()
    
    return {
        'data': alerts,
        'total': total_count,
        'page': page,
        'page_size': page_size,
        'total_pages': (total_count + page_size - 1) // page_size
    }

@st.cache_data(ttl=60)
def get_alert_by_id(alert_id: int) -> Optional[Dict]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM alerts WHERE id = ?', (alert_id,))
    alert = cursor.fetchone()
    conn.close()
    return dict(alert) if alert else None

def update_alert_status(alert_id: int, status: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE alerts SET status = ? WHERE id = ?', (status, alert_id))
    conn.commit()
    conn.close()

def add_response_log(alert_id: int, responder: str, action_type: str, notes: str = None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO response_logs (alert_id, responder, action_type, notes) VALUES (?, ?, ?, ?)',
        (alert_id, responder, action_type, notes)
    )
    conn.commit()
    conn.close()

@st.cache_data(ttl=120)
def get_response_logs(alert_id: int) -> List[Dict]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM response_logs WHERE alert_id = ? ORDER BY action_time ASC', (alert_id,))
    logs = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return logs

@st.cache_data(ttl=60)
def get_alerts_with_details(page: int = 1, page_size: int = 50) -> Dict:
    conn = get_connection()
    cursor = conn.cursor()
    
    offset = (page - 1) * page_size
    
    cursor.execute('''
        SELECT a.*, u.name as user_name, u.phone as user_phone, u.address as user_address
        FROM alerts a
        JOIN users u ON a.user_id = u.id
        ORDER BY a.alert_time DESC
        LIMIT ? OFFSET ?
    ''', (page_size, offset))
    alerts = [dict(row) for row in cursor.fetchall()]
    
    cursor.execute('SELECT COUNT(*) FROM alerts')
    total_count = cursor.fetchone()[0]
    
    conn.close()
    
    return {
        'data': alerts,
        'total': total_count,
        'page': page,
        'page_size': page_size,
        'total_pages': (total_count + page_size - 1) // page_size
    }

@st.cache_data(ttl=30)
def get_statistics():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM users')
    total_users = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM alerts')
    total_alerts = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM alerts WHERE status = "pending"')
    pending_alerts = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM alerts WHERE status = "resolved"')
    resolved_alerts = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM alerts WHERE risk_level = "high"')
    high_risk_alerts = cursor.fetchone()[0]
    
    conn.close()
    
    return {
        'total_users': total_users,
        'total_alerts': total_alerts,
        'pending_alerts': pending_alerts,
        'resolved_alerts': resolved_alerts,
        'high_risk_alerts': high_risk_alerts
    }

def generate_mock_users(count: int = 5):
    conn = get_connection()
    cursor = conn.cursor()
    
    mock_users = [
        ("张三", "13812345678", "北京市朝阳区建国路88号", "13912345678"),
        ("李四", "13812345679", "北京市海淀区中关村大街1号", "13912345679"),
        ("王五", "13812345680", "北京市西城区金融街35号", "13912345680"),
        ("赵六", "13812345681", "北京市东城区王府井大街1号", "13912345681"),
        ("孙七", "13812345682", "北京市丰台区南三环西路3号", "13912345682"),
    ]
    
    user_ids = []
    for i in range(min(count, len(mock_users))):
        name, phone, address, emergency_contact = mock_users[i]
        
        cursor.execute('''
            INSERT INTO users (name, phone, address, emergency_contact)
            VALUES (?, ?, ?, ?)
        ''', (name, phone, address, emergency_contact))
        
        user_id = cursor.lastrowid
        user_ids.append(user_id)
    
    conn.commit()
    conn.close()
    
    return user_ids

def generate_mock_alerts(user_ids: List[int], count: int = 10):
    if not user_ids:
        return []
    
    conn = get_connection()
    cursor = conn.cursor()
    
    import random
    from datetime import timedelta
    
    statuses = ["pending", "processing", "resolved"]
    risk_levels = ["low", "medium", "high"]
    descriptions = [
        "老人在家中跌倒，需要紧急救助",
        "突发心脏病，请求医疗急救",
        "家中发生火灾，请求消防支援",
        "发现可疑人员，请求治安协助",
        "老人感到身体不适，需要医疗检查",
        "忘记服药，需要提醒",
        "家中燃气泄漏，请求紧急处理",
        "老人走失，请求协助寻找",
        "突发高血压，需要医疗救助",
        "家中水管破裂，请求维修"
    ]
    
    alert_ids = []
    for i in range(count):
        user_id = random.choice(user_ids)
        status = random.choice(statuses)
        risk_level = random.choice(risk_levels)
        description = random.choice(descriptions)
        
        base_lat = 39.9042
        base_lng = 116.4074
        location_lat = base_lat + random.uniform(-0.1, 0.1)
        location_lng = base_lng + random.uniform(-0.1, 0.1)
        
        alert_time = datetime.now() - timedelta(days=random.randint(1, 30))
        
        cursor.execute('''
            INSERT INTO alerts (user_id, alert_time, location_lat, location_lng, status, risk_level, description)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, alert_time, location_lat, location_lng, status, risk_level, description))
        
        alert_id = cursor.lastrowid
        alert_ids.append(alert_id)
    
    conn.commit()
    conn.close()
    
    return alert_ids

def generate_mock_today_alerts(user_ids: List[int], count: int = 3):
    if not user_ids:
        return []
    
    conn = get_connection()
    cursor = conn.cursor()
    
    import random
    from datetime import timedelta
    
    statuses = ["pending", "processing"]
    risk_levels = ["medium", "high"]
    descriptions = [
        "老人在家中跌倒，请求紧急救助",
        "突发心脏病，请求医疗急救",
        "家中发生火灾，请求消防支援"
    ]
    
    alert_ids = []
    for i in range(count):
        user_id = random.choice(user_ids)
        status = random.choice(statuses)
        risk_level = random.choice(risk_levels)
        description = random.choice(descriptions)
        
        base_lat = 39.9042
        base_lng = 116.4074
        location_lat = base_lat + random.uniform(-0.05, 0.05)
        location_lng = base_lng + random.uniform(-0.05, 0.05)
        
        alert_time = datetime.now() - timedelta(hours=random.randint(0, 23))
        
        cursor.execute('''
            INSERT INTO alerts (user_id, alert_time, location_lat, location_lng, status, risk_level, description)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, alert_time, location_lat, location_lng, status, risk_level, description))
        
        alert_id = cursor.lastrowid
        alert_ids.append(alert_id)
    
    conn.commit()
    conn.close()
    
    return alert_ids

def generate_mock_data():
    user_count = 5
    alert_count = 10
    today_alert_count = 3
    
    user_ids = generate_mock_users(user_count)
    alert_ids = generate_mock_alerts(user_ids, alert_count)
    today_alert_ids = generate_mock_today_alerts(user_ids, today_alert_count)
    
    return {
        'users': len(user_ids),
        'alerts': len(alert_ids),
        'today_alerts': len(today_alert_ids),
        'total_alerts': len(alert_ids) + len(today_alert_ids)
    }
