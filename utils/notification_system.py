import streamlit as st
import threading
import queue
import time
import logging
from datetime import datetime
from typing import Dict, List, Optional
import heapq

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def rerun():
    if 'rerun' not in st.session_state:
        st.session_state.rerun = False
    
    if st.session_state.rerun:
        st.session_state.rerun = False
        st.experimental_rerun()

class Notification:
    def __init__(self, id: int, recipient: str, message: str, priority: str = "low", 
                 notification_type: str = "sms", retry_count: int = 0, max_retries: int = 3):
        self.id = id
        self.recipient = recipient
        self.message = message
        self.priority = priority
        self.notification_type = notification_type
        self.retry_count = retry_count
        self.max_retries = max_retries
        self.created_at = datetime.now()
        self.last_retry_at = None
        self.status = "pending"
        self.error_message = None
        
    def __lt__(self, other):
        priority_order = {"high": 0, "medium": 1, "low": 2}
        return priority_order.get(self.priority, 2) < priority_order.get(other.priority, 2)

class NotificationChannel:
    def __init__(self, name: str):
        self.name = name
        self.sent_count = 0
        self.failed_count = 0
        self.logs = []
    
    def send(self, notification: Notification) -> bool:
        raise NotImplementedError("Subclasses must implement send method")
    
    def log(self, notification: Notification, success: bool, error_message: str = None):
        log_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "channel": self.name,
            "notification_id": notification.id,
            "recipient": notification.recipient,
            "message": notification.message,
            "priority": notification.priority,
            "success": success,
            "error": error_message
        }
        self.logs.append(log_entry)
        
        if success:
            self.sent_count += 1
            logger.info(f"[{self.name}] Success: ID={notification.id}, Recipient={notification.recipient}")
        else:
            self.failed_count += 1
            logger.error(f"[{self.name}] Failed: ID={notification.id}, Error={error_message}")

class SMSChannel(NotificationChannel):
    def __init__(self):
        super().__init__("SMS")
        self.simulation_delay = 0.5
    
    def send(self, notification: Notification) -> bool:
        try:
            time.sleep(self.simulation_delay)
            
            if len(notification.recipient) < 3:
                raise ValueError("Invalid phone number")
            
            self.log(notification, True)
            return True
        
        except Exception as e:
            self.log(notification, False, str(e))
            return False

class VoiceCallChannel(NotificationChannel):
    def __init__(self):
        super().__init__("VoiceCall")
        self.simulation_delay = 1.0
        self.call_records = []
    
    def send(self, notification: Notification) -> bool:
        try:
            time.sleep(self.simulation_delay)
            
            if len(notification.recipient) < 3:
                raise ValueError("Invalid phone number")
            
            call_record = {
                "call_id": f"CALL_{notification.id}_{int(time.time())}",
                "recipient": notification.recipient,
                "message": notification.message,
                "call_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "duration": 30,
                "status": "connected"
            }
            self.call_records.append(call_record)
            
            self.log(notification, True)
            return True
        
        except Exception as e:
            self.log(notification, False, str(e))
            return False

class AppPushChannel(NotificationChannel):
    def __init__(self):
        super().__init__("AppPush")
        self.simulation_delay = 0.3
        self.push_notifications = []
    
    def send(self, notification: Notification) -> bool:
        try:
            time.sleep(self.simulation_delay)
            
            if not notification.recipient:
                raise ValueError("Invalid recipient")
            
            push_record = {
                "push_id": f"PUSH_{notification.id}_{int(time.time())}",
                "recipient": notification.recipient,
                "title": "紧急通知",
                "message": notification.message,
                "push_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "read": False
            }
            self.push_notifications.append(push_record)
            
            self.log(notification, True)
            return True
        
        except Exception as e:
            self.log(notification, False, str(e))
            return False

class NotificationSystem:
    def __init__(self):
        self.channels = {
            "sms": SMSChannel(),
            "voice": VoiceCallChannel(),
            "app": AppPushChannel()
        }
        self.priority_queue = []
        self.low_priority_queue = queue.Queue()
        self.notification_counter = 0
        self.is_running = False
        self.worker_thread = None
        self.retry_queue = []
        self.retry_interval = 300
        self.lock = threading.Lock()
        
        if "notification_logs" not in st.session_state:
            st.session_state.notification_logs = []
        
        if "push_notifications" not in st.session_state:
            st.session_state.push_notifications = []
    
    def add_notification(self, recipient: str, message: str, priority: str = "low", 
                      notification_type: str = "sms") -> int:
        with self.lock:
            self.notification_counter += 1
            notification_id = self.notification_counter
        
        notification = Notification(
            id=notification_id,
            recipient=recipient,
            message=message,
            priority=priority,
            notification_type=notification_type
        )
        
        if priority == "high":
            heapq.heappush(self.priority_queue, notification)
        else:
            self.low_priority_queue.put(notification)
        
        logger.info(f"Notification added: ID={notification_id}, Priority={priority}, Type={notification_type}")
        
        return notification_id
    
    def send_notification(self, notification: Notification) -> bool:
        channel = self.channels.get(notification.notification_type)
        
        if not channel:
            logger.error(f"Unknown channel: {notification.notification_type}")
            return False
        
        success = channel.send(notification)
        
        if success:
            notification.status = "sent"
            self._update_session_state(notification, success)
        else:
            notification.status = "failed"
            notification.error_message = "Send failed"
            self._update_session_state(notification, success)
        
        return success
    
    def _update_session_state(self, notification: Notification, success: bool):
        log_entry = {
            "id": notification.id,
            "recipient": notification.recipient,
            "message": notification.message,
            "type": notification.notification_type,
            "priority": notification.priority,
            "status": "sent" if success else "failed",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        st.session_state.notification_logs.insert(0, log_entry)
        
        if len(st.session_state.notification_logs) > 100:
            st.session_state.notification_logs.pop()
        
        if notification.notification_type == "app" and success:
            push_entry = {
                "title": "紧急通知",
                "message": notification.message,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "priority": notification.priority
            }
            st.session_state.push_notifications.insert(0, push_entry)
            
            if len(st.session_state.push_notifications) > 20:
                st.session_state.push_notifications.pop()
    
    def process_high_priority(self):
        while self.priority_queue:
            notification = heapq.heappop(self.priority_queue)
            success = self.send_notification(notification)
            
            if not success and notification.retry_count < notification.max_retries:
                notification.retry_count += 1
                notification.last_retry_at = datetime.now()
                self.retry_queue.append(notification)
                logger.warning(f"Notification {notification.id} will retry in {self.retry_interval} seconds")
    
    def process_low_priority(self):
        batch_size = 5
        batch = []
        
        while len(batch) < batch_size and not self.low_priority_queue.empty():
            try:
                notification = self.low_priority_queue.get_nowait()
                batch.append(notification)
            except queue.Empty:
                break
        
        for notification in batch:
            success = self.send_notification(notification)
            
            if not success and notification.retry_count < notification.max_retries:
                notification.retry_count += 1
                notification.last_retry_at = datetime.now()
                self.retry_queue.append(notification)
                logger.warning(f"Notification {notification.id} will retry in {self.retry_interval} seconds")
    
    def process_retries(self):
        now = datetime.now()
        remaining_retries = []
        
        for notification in self.retry_queue:
            if notification.last_retry_at:
                time_since_retry = (now - notification.last_retry_at).total_seconds()
                
                if time_since_retry >= self.retry_interval:
                    success = self.send_notification(notification)
                    
                    if not success and notification.retry_count < notification.max_retries:
                        notification.retry_count += 1
                        notification.last_retry_at = datetime.now()
                        remaining_retries.append(notification)
                        logger.warning(f"Notification {notification.id} retry {notification.retry_count}/{notification.max_retries}")
                else:
                    remaining_retries.append(notification)
        
        self.retry_queue = remaining_retries
    
    def start(self):
        if self.is_running:
            return
        
        self.is_running = True
        self.worker_thread = threading.Thread(target=self._worker_loop, daemon=True)
        self.worker_thread.start()
        logger.info("Notification system started")
    
    def stop(self):
        self.is_running = False
        if self.worker_thread:
            self.worker_thread.join(timeout=2)
        logger.info("Notification system stopped")
    
    def _worker_loop(self):
        while self.is_running:
            self.process_high_priority()
            self.process_low_priority()
            self.process_retries()
            time.sleep(1)
    
    def get_statistics(self) -> Dict:
        total_sent = sum(channel.sent_count for channel in self.channels.values())
        total_failed = sum(channel.failed_count for channel in self.channels.values())
        
        return {
            "total_sent": total_sent,
            "total_failed": total_failed,
            "pending_high": len(self.priority_queue),
            "pending_low": self.low_priority_queue.qsize(),
            "retrying": len(self.retry_queue),
            "channels": {
                name: {
                    "sent": channel.sent_count,
                    "failed": channel.failed_count
                }
                for name, channel in self.channels.items()
            }
        }

def show_notification_system_ui():
    st.subheader("📢 多通道通知系统")
    
    if "notification_system" not in st.session_state:
        st.session_state.notification_system = NotificationSystem()
        st.session_state.notification_system.start()
    
    notification_system = st.session_state.notification_system
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        recipient = st.text_input("接收者", placeholder="手机号或用户ID", key="notify_recipient")
    
    with col2:
        notification_type = st.selectbox(
            "通知类型",
            options=["sms", "voice", "app"],
            format_func=lambda x: {
                "sms": "短信",
                "voice": "语音呼叫",
                "app": "APP推送"
            }.get(x, x),
            index=0,
            key="notify_type"
        )
    
    with col3:
        priority = st.selectbox(
            "优先级",
            options=["high", "medium", "low"],
            format_func=lambda x: {
                "high": "高优先级",
                "medium": "中优先级",
                "low": "低优先级"
            }.get(x, x),
            index=2,
            key="notify_priority"
        )
    
    message = st.text_area("通知内容", placeholder="请输入通知内容...", height=100, key="notify_message")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📤 发送通知", type="primary", key="send_notify"):
            if recipient and message:
                notification_id = notification_system.add_notification(
                    recipient=recipient,
                    message=message,
                    priority=priority,
                    notification_type=notification_type
                )
                st.success(f"通知已添加到队列！ID: {notification_id}")
                st.session_state.rerun = True
                rerun()
            else:
                st.error("请填写接收者和通知内容！")
    
    with col2:
        if st.button("🔄 刷新统计", key="refresh_notify_stats"):
            st.session_state.rerun = True
            rerun()
    
    with col3:
        if st.button("🧹 清空日志", key="clear_notify_logs"):
            st.session_state.notification_logs = []
            st.session_state.push_notifications = []
            st.session_state.rerun = True
            rerun()
    
    st.markdown("---")
    
    stats = notification_system.get_statistics()
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("已发送", stats['total_sent'])
    
    with col2:
        st.metric("发送失败", stats['total_failed'], delta_color="inverse")
    
    with col3:
        st.metric("高优先级队列", stats['pending_high'])
    
    with col4:
        st.metric("低优先级队列", stats['pending_low'])
    
    with col5:
        st.metric("重试队列", stats['retrying'])
    
    st.markdown("---")
    
    tab1, tab2, tab3 = st.tabs(["📋 通知日志", "📱 APP推送", "📊 通道统计"])
    
    with tab1:
        st.subheader("通知发送日志")
        
        if st.session_state.notification_logs:
            for log in st.session_state.notification_logs[:20]:
                with st.container():
                    status_emoji = {
                        "sent": "✅",
                        "failed": "❌"
                    }
                    type_badge = {
                        "sms": "📱 短信",
                        "voice": "📞 语音",
                        "app": "🔔 APP"
                    }
                    priority_badge = {
                        "high": "🔴 高",
                        "medium": "🟡 中",
                        "low": "🟢 低"
                    }
                    
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.markdown(f"""
                        {status_emoji.get(log['status'], '⚪')} **ID: {log['id']}** - {type_badge.get(log['type'], log['type'])}
                        - **接收者**: {log['recipient']}
                        - **优先级**: {priority_badge.get(log['priority'], log['priority'])}
                        - **消息**: {log['message'][:50]}...
                        - **时间**: {log['timestamp']}
                        """)
                    with col2:
                        st.caption(log['timestamp'])
                    st.markdown("---")
        else:
            st.info("暂无通知日志")
    
    with tab2:
        st.subheader("APP推送通知")
        
        if st.session_state.push_notifications:
            for push in st.session_state.push_notifications:
                with st.container():
                    priority_emoji = {
                        "high": "🔴",
                        "medium": "🟡",
                        "low": "🟢"
                    }
                    
                    st.markdown(f"""
                    {priority_emoji.get(push['priority'], '⚪')} **{push['title']}**
                    - **消息**: {push['message']}
                    - **时间优先级**: {push['priority']}
                    - **时间**: {push['timestamp']}
                    """)
                    st.markdown("---")
        else:
            st.info("暂无APP推送通知")
    
    with tab3:
        st.subheader("通道统计")
        
        for channel_name, channel_stats in stats['channels'].items():
            channel_badge = {
                "sms": "📱 短信通道",
                "voice": "📞 语音通道",
                "app": "🔔 APP通道"
            }
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"### {channel_badge.get(channel_name, channel_name)}")
            
            with col2:
                st.metric("发送成功", channel_stats['sent'])
            
            with col3:
                st.metric("发送失败", channel_stats['failed'], delta_color="inverse")
            
            st.markdown("---")

def send_emergency_notification(recipient: str, message: str, notification_type: str = "sms"):
    if "notification_system" not in st.session_state:
        st.session_state.notification_system = NotificationSystem()
        st.session_state.notification_system.start()
    
    notification_system = st.session_state.notification_system
    
    notification_id = notification_system.add_notification(
        recipient=recipient,
        message=message,
        priority="high",
        notification_type=notification_type
    )
    
    return notification_id
