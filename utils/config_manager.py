import os
from dotenv import dotenv_values, set_key, load_dotenv
import re


class ConfigManager:
    
    def __init__(self, env_file=None):
        if env_file is None:
            env_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
        
        self.env_file = env_file
        self.load()
    
    def load(self):
        load_dotenv(self.env_file)
        self._config = dotenv_values(self.env_file)
        return self._config
    
    def get(self, key, default=None):
        return self._config.get(key, default)
    
    def get_all(self):
        return self._config.copy()
    
    def set(self, key, value):
        set_key(self.env_file, key, value)
        self._config[key] = value
        return True
    
    def set_multiple(self, config_dict):
        for key, value in config_dict.items():
            if value:
                self.set(key, value)
        return True
    
    def delete(self, key):
        set_key(self.env_file, key, '')
        if key in self._config:
            del self._config[key]
        return True
    
    def is_configured(self, key):
        value = self.get(key)
        return value and value != f'your_{key.lower()}_here'
    
    def mask_value(self, value, visible_chars=4, mask_char='*'):
        if not value or len(value) <= visible_chars:
            return value
        
        return value[:visible_chars] + mask_char * (len(value) - visible_chars)
    
    def get_masked_config(self, visible_chars=4):
        masked = {}
        for key, value in self._config.items():
            masked[key] = self.mask_value(value, visible_chars)
        return masked
    
    def validate_api_key(self, key_name, value):
        if not value or not value.strip():
            return False, "API密钥不能为空"
        
        if value.startswith('your_') and value.endswith('_here'):
            return False, "请使用实际的API密钥，不要使用默认值"
        
        min_length = 16
        if len(value) < min_length:
            return False, f"API密钥长度至少需要{min_length}个字符"
        
        if key_name == 'MAP_API_KEY':
            return self._validate_map_api_key(value)
        elif key_name == 'WEATHER_API_KEY':
            return self._validate_weather_api_key(value)
        elif key_name == 'SMS_API_KEY':
            return self._validate_sms_api_key(value)
        elif key_name == 'NOTIFICATION_API_KEY':
            return self._validate_notification_api_key(value)
        
        return True, "验证通过"
    
    def _validate_map_api_key(self, value):
        if re.match(r'^[A-Za-z0-9_-]{20,}$', value):
            return True, "验证通过"
        return False, "地图API密钥格式不正确，应为字母、数字、下划线或连字符，长度至少20个字符"
    
    def _validate_weather_api_key(self, value):
        if re.match(r'^[A-Za-z0-9_-]{16,}$', value):
            return True, "验证通过"
        return False, "天气API密钥格式不正确，应为字母、数字、下划线或连字符，长度至少16个字符"
    
    def _validate_sms_api_key(self, value):
        if re.match(r'^[A-Za-z0-9_-]{20,}$', value):
            return True, "验证通过"
        return False, "短信API密钥格式不正确，应为字母、数字、下划线或连字符，长度至少20个字符"
    
    def _validate_notification_api_key(self, value):
        if re.match(r'^[A-Za-z0-9_-]{16,}$', value):
            return True, "验证通过"
        return False, "通知API密钥格式不正确，应为字母、数字、下划线或连字符，长度至少16个字符"
    
    def validate_all(self):
        results = {}
        for key, value in self._config.items():
            is_valid, message = self.validate_api_key(key, value)
            results[key] = {
                'is_valid': is_valid,
                'message': message,
                'is_configured': self.is_configured(key)
            }
        return results
    
    def get_config_status(self):
        status = {}
        for key, value in self._config.items():
            is_configured = self.is_configured(key)
            is_valid, message = self.validate_api_key(key, value)
            
            status[key] = {
                'configured': is_configured,
                'valid': is_valid,
                'message': message,
                'value': self.mask_value(value) if is_configured else None
            }
        return status
    
    def backup(self):
        backup_file = self.env_file + '.backup'
        import shutil
        shutil.copy2(self.env_file, backup_file)
        return backup_file
    
    def restore(self):
        backup_file = self.env_file + '.backup'
        if os.path.exists(backup_file):
            import shutil
            shutil.copy2(backup_file, self.env_file)
            self.load()
            return True
        return False


_config_manager = None


def get_config_manager():
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager


def reload_config():
    global _config_manager
    _config_manager = ConfigManager()
    return _config_manager
