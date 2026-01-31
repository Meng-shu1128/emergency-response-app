import streamlit as st
import threading
import queue
import time
import pyttsx3

SOOTHING_MESSAGES = {
    'fall': [
        "请不要惊慌，我们已经收到您的求助信息，救援人员正在赶来的路上。",
        "请保持冷静，不要随意移动，我们会尽快为您提供帮助。",
        "您已经成功发出求助信号，请耐心等待救援人员的到来。"
    ],
    'medical': [
        "医疗救援团队已收到您的求助，正在紧急赶往您的位置。",
        "请不要紧张，保持呼吸平稳，我们的医护人员很快就到。",
        "您的求救信号已确认，医疗援助正在途中。"
    ],
    'fire': [
        "请立即远离火源，我们已经通知消防部门前往救援。",
        "请保持冷静，寻找安全出口，消防人员正在赶来。",
        "您的火警求助已收到，请确保自身安全，救援马上就到。"
    ],
    'general': [
        "请保持冷静，我们已经收到您的求助信息，正在为您安排援助。",
        "不要担心，帮助正在路上，请耐心等待。",
        "您的求助信号已成功发送，我们尽快与您联系。"
    ]
}

def rerun():
    if 'rerun' not in st.session_state:
        st.session_state.rerun = False
    
    if st.session_state.rerun:
        st.session_state.rerun = False
        st.experimental_rerun()

class VoicePlayer:
    def __init__(self):
        self.engine = None
        self.is_playing = False
        self.is_paused = False
        self.playback_thread = None
        self.text_queue = queue.Queue()
        self.current_text = ""
        self.rate = 200
        self.volume = 1.0
        self._init_engine()
    
    def _init_engine(self):
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', self.rate)
            self.engine.setProperty('volume', self.volume)
        except Exception as e:
            st.error(f"语音引擎初始化失败: {str(e)}")
    
    def set_rate(self, rate):
        self.rate = rate
        if self.engine:
            self.engine.setProperty('rate', rate)
    
    def set_volume(self, volume):
        self.volume = volume
        if self.engine:
            self.engine.setProperty('volume', volume)
    
    def play_text(self, text):
        if not text:
            return
        
        self.current_text = text
        self.is_paused = False
        
        if self.playback_thread and self.playback_thread.is_alive():
            self.text_queue.put(text)
        else:
            self.is_playing = True
            self.playback_thread = threading.Thread(target=self._play_thread, args=(text,))
            self.playback_thread.daemon = True
            self.playback_thread.start()
    
    def _play_thread(self, text):
        try:
            if self.engine:
                self.engine.say(text)
                self.engine.runAndWait()
            
            while not self.text_queue.empty():
                next_text = self.text_queue.get()
                if self.engine:
                    self.engine.say(next_text)
                    self.engine.runAndWait()
        
        except Exception as e:
            st.error(f"语音播放错误: {str(e)}")
        
        finally:
            self.is_playing = False
    
    def stop(self):
        self.is_playing = False
        self.is_paused = False
        self.text_queue.queue.clear()
        
        if self.engine:
            try:
                self.engine.stop()
            except:
                pass
    
    def pause(self):
        if self.engine and self.is_playing:
            try:
                self.engine.stop()
                self.is_paused = True
            except:
                pass
    
    def resume(self):
        if self.is_paused and self.current_text:
            self.is_paused = False
            self.playback_thread = threading.Thread(target=self._play_thread, args=(self.current_text,))
            self.playback_thread.daemon = True
            self.playback_thread.start()

def get_soothing_messages(alert_type=None):
    if alert_type and alert_type.lower() in SOOTHING_MESSAGES:
        return SOOTHING_MESSAGES[alert_type.lower()]
    return SOOTHING_MESSAGES['general']

def show_voice_player(alert_type=None, custom_text=None):
    if 'voice_player' not in st.session_state:
        st.session_state.voice_player = VoicePlayer()
    
    if 'voice_player_text' not in st.session_state:
        st.session_state.voice_player_text = ""
    
    if 'voice_player_status' not in st.session_state:
        st.session_state.voice_player_status = "就绪"
    
    player = st.session_state.voice_player
    
    st.subheader("🔊 语音安抚播放器")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if custom_text:
            text_input = st.text_area("自定义语音文本", value=custom_text, height=100, key="voice_custom_text")
        else:
            messages = get_soothing_messages(alert_type)
            selected_message = st.selectbox(
                "选择安抚语音",
                options=messages,
                index=0,
                key="voice_message_select"
            )
            text_input = st.text_area("语音文本", value=selected_message, height=100, key="voice_text_input")
    
    with col2:
        rate = st.slider("语速", min_value=50, max_value=400, value=200, step=10, key="voice_rate")
        player.set_rate(rate)
        
        volume = st.slider("音量", min_value=0.0, max_value=1.0, value=1.0, step=0.1, key="voice_volume")
        player.set_volume(volume)
    
    st.markdown("---")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("▶️ 播放", type="primary", key="voice_play", disabled=player.is_playing and not player.is_paused):
            st.session_state.voice_player_text = text_input
            player.play_text(text_input)
            st.session_state.voice_player_status = "播放中"
            st.session_state.rerun = True
            rerun()
    
    with col2:
        if st.button("⏸️ 暂停", key="voice_pause", disabled=not player.is_playing or player.is_paused):
            player.pause()
            st.session_state.voice_player_status = "已暂停"
            st.session_state.rerun = True
            rerun()
    
    with col3:
        if st.button("▶️ 继续", key="voice_resume", disabled=not player.is_paused):
            player.resume()
            st.session_state.voice_player = player
            st.session_state.voice_player_status = "播放中"
            st.session_state.rerun = True
            rerun()
    
    with col4:
        if st.button("⏹️ 停止", type="secondary", key="voice_stop", disabled=not player.is_playing):
            player.stop()
            st.session_state.voice_player_status = "已停止"
            st.session_state.rerun = True
            rerun()
    
    st.markdown("---")
    
    status_color = {
        "就绪": "🟢",
        "播放中": "🔵",
        "已暂停": "🟡",
        "已停止": "🔴"
    }
    
    st.info(f"{status_color.get(st.session_state.voice_player_status, '⚪')} 状态: {st.session_state.voice_player_status}")
    
    if st.session_state.voice_player_text:
        st.caption(f"当前文本: {st.session_state.voice_player_text[:100]}...")
    
    if player.playback_thread and player.playback_thread.is_alive():
        st.session_state.voice_player_status = "播放中"
    elif player.is_paused:
        st.session_state.voice_player_status = "已暂停"
    elif player.is_playing:
        st.session_state.voice_player_status = "已停止"
        player.is_playing = False
    else:
        st.session_state.voice_player_status = "就绪"

def play_soothing_message(alert_type, message_index=0):
    messages = get_soothing_messages(alert_type)
    
    if messages and 0 <= message_index < len(messages):
        text = messages[message_index]
        
        if 'voice_player' not in st.session_state:
            st.session_state.voice_player = VoicePlayer()
        
        player = st.session_state.voice_player
        player.play_text(text)
        
        return text
    
    return None
