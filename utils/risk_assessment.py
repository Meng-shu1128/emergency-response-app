import math
from datetime import datetime, time
from typing import Dict, List, Tuple

class RiskAssessment:
    def __init__(self):
        self.base_risk = 0
        self.risk_factors = []
        self.risk_level = "low"
        self.suggestions = []
        
        self.river_locations = [
            {"name": "永定河", "lat": 39.9100, "lng": 116.4000},
            {"name": "潮白河", "lat": 39.8900, "lng": 116.4200},
            {"name": "北运河", "lat": 39.9200, "lng": 116.3800},
            {"name": "拒马河", "lat": 39.8800, "lng": 116.4500}
        ]
        
        self.weather_risk_map = {
            "晴": 0,
            "多云": 0,
            "阴": 0,
            "小雨": 1,
            "中雨": 1,
            "大雨": 1,
            "暴雨": 1,
            "雷阵雨": 1,
            "雪": 1,
            "大雾": 1,
            "沙尘暴": 1
        }
        
        self.suggestion_rules = {
            "night": "夜间出行请携带照明设备，避免单独行动",
            "near_river": "请远离河道边缘，注意防滑",
            "bad_weather": "恶劣天气请减少外出，注意保暖防滑",
            "high_risk": "建议立即联系家人或救援人员",
            "medium_risk": "请保持警惕，随时准备求助",
            "low_risk": "注意安全，保持通讯畅通"
        }
    
    def calculate_distance(self, lat1: float, lng1: float, lat2: float, lng2: float) -> float:
        R = 6371000
        
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lng = math.radians(lng2 - lng1)
        
        a = math.sin(delta_lat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lng / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        return R * c
    
    def is_night_time(self, current_time: datetime) -> bool:
        night_start = time(22, 0)
        night_end = time(6, 0)
        
        time_only = current_time.time()
        
        if night_start <= time_only or time_only <= night_end:
            return True
        return False
    
    def is_near_river(self, lat: float, lng: float, threshold: float = 100) -> Tuple[bool, str]:
        for river in self.river_locations:
            distance = self.calculate_distance(lat, lng, river["lat"], river["lng"])
            if distance <= threshold:
                return True, river["name"]
        return False, ""
    
    def get_weather_risk(self, weather: str) -> int:
        return self.weather_risk_map.get(weather, 0)
    
    def assess_risk(self, lat: float, lng: float, current_time: datetime = None, weather: str = "晴") -> Dict:
        if current_time is None:
            current_time = datetime.now()
        
        self.base_risk = 0
        self.risk_factors = []
        self.suggestions = []
        
        is_night = self.is_night_time(current_time)
        if is_night:
            self.base_risk += 1
            self.risk_factors.append({
                "factor": "夜间时段",
                "description": f"当前时间 {current_time.strftime('%H:%M')} 处于夜间时段（22:00-06:00）",
                "risk_increase": 1
            })
            self.suggestions.append(self.suggestion_rules["night"])
        
        near_river, river_name = self.is_near_river(lat, lng)
        if near_river:
            self.base_risk += 2
            self.risk_factors.append({
                "factor": "靠近河流",
                "description": f"距离 {river_name} 100米范围内",
                "risk_increase": 2
            })
            self.suggestions.append(self.suggestion_rules["near_river"])
        
        weather_risk = self.get_weather_risk(weather)
        if weather_risk > 0:
            self.base_risk += weather_risk
            self.risk_factors.append({
                "factor": "恶劣天气",
                "description": f"当前天气为 {weather}",
                "risk_increase": weather_risk
            })
            self.suggestions.append(self.suggestion_rules["bad_weather"])
        
        if self.base_risk >= 3:
            self.risk_level = "high"
            self.suggestions.append(self.suggestion_rules["high_risk"])
        elif self.base_risk >= 2:
            self.risk_level = "medium"
            self.suggestions.append(self.suggestion_rules["medium_risk"])
        else:
            self.risk_level = "low"
            self.suggestions.append(self.suggestion_rules["low_risk"])
        
        return {
            "risk_level": self.risk_level,
            "risk_score": self.base_risk,
            "risk_factors": self.risk_factors,
            "suggestions": list(set(self.suggestions)),
            "assessment_time": current_time.strftime("%Y-%m-%d %H:%M:%S"),
            "location": {"lat": lat, "lng": lng},
            "weather": weather
        }
    
    def batch_assess(self, locations: List[Dict], weather: str = "晴") -> List[Dict]:
        results = []
        for loc in locations:
            lat = loc.get("lat")
            lng = loc.get("lng")
            time_str = loc.get("time")
            
            if time_str:
                try:
                    current_time = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
                except:
                    current_time = datetime.now()
            else:
                current_time = datetime.now()
            
            result = self.assess_risk(lat, lng, current_time, weather)
            result["location_id"] = loc.get("id", "")
            results.append(result)
        
        return results
    
    def add_river_location(self, name: str, lat: float, lng: float):
        self.river_locations.append({
            "name": name,
            "lat": lat,
            "lng": lng
        })
    
    def add_weather_risk(self, weather: str, risk_level: int):
        self.weather_risk_map[weather] = risk_level
    
    def add_suggestion_rule(self, rule_key: str, suggestion: str):
        self.suggestion_rules[rule_key] = suggestion

def show_risk_assessment_ui():
    st.subheader("🎯 风险评估工具")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        lat = st.number_input("纬度", value=39.9042, format="%.6f", key="risk_lat")
    
    with col2:
        lng = st.number_input("经度", value=116.4074, format="%.6f", key="risk_lng")
    
    with col3:
        weather_options = ["晴", "多云", "阴", "小雨", "中雨", "大雨", "暴雨", "雷阵雨", "雪", "大雾", "沙尘暴"]
        weather = st.selectbox("天气状况", options=weather_options, index=0, key="risk_weather")
    
    time_input = st.text_input("时间（格式：YYYY-MM-DD HH:MM:SS，留空使用当前时间）", placeholder="2024-01-01 23:30:00", key="risk_time")
    
    if st.button("🔍 评估风险", type="primary", key="risk_assess_btn"):
        try:
            if time_input:
                current_time = datetime.strptime(time_input, "%Y-%m-%d %H:%M:%S")
            else:
                current_time = datetime.now()
            
            assessor = RiskAssessment()
            result = assessor.assess_risk(lat, lng, current_time, weather)
            
            st.markdown("---")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                risk_emoji = {
                    "low": "🟢",
                    "medium": "🟡",
                    "high": "🔴"
                }
                st.metric("风险等级", f"{risk_emoji.get(result['risk_level'], '⚪')} {result['risk_level'].upper()}")
            
            with col2:
                st.metric("风险评分", result['risk_score'])
            
            with col3:
                st.metric("评估时间", current_time.strftime("%H:%M:%S"))
            
            st.markdown("---")
            
            if result['risk_factors']:
                st.markdown("### 📊 风险因素分析")
                for factor in result['risk_factors']:
                    with st.container():
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.write(f"**{factor['factor']}**: {factor['description']}")
                        with col2:
                            st.caption(f"+{factor['risk_increase']} 分")
                        st.markdown("---")
            else:
                st.info("未检测到明显风险因素")
            
            st.markdown("---")
            
            if result['suggestions']:
                st.markdown("### 💡 建议措施")
                for i, suggestion in enumerate(result['suggestions'], 1):
                    st.write(f"{i}. {suggestion}")
            
            st.markdown("---")
            
            with st.expander("📋 详细评估信息"):
                st.json(result)
        
        except Exception as e:
            st.error(f"评估失败: {str(e)}")

def get_risk_level_from_assessment(lat: float, lng: float, weather: str = "晴") -> str:
    assessor = RiskAssessment()
    result = assessor.assess_risk(lat, lng, datetime.now(), weather)
    return result['risk_level']
