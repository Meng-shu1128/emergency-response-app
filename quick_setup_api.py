"""
快速API配置脚本
用于快速配置应急响应系统的API密钥
"""

import os
import sys

def print_header():
    print("=" * 60)
    print("        应急响应系统 - API快速配置工具")
    print("=" * 60)
    print()

def print_menu():
    print("请选择要配置的API：")
    print("  1. 地图API密钥 (MAP_API_KEY)")
    print("  2. 天气API密钥 (WEATHER_API_KEY)")
    print("  3. 短信API密钥 (SMS_API_KEY)")
    print("  4. 通知API密钥 (NOTIFICATION_API_KEY)")
    print("  5. 全部配置")
    print("  6. 查看当前配置")
    print("  7. 退出")
    print()

def get_env_file_path():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, '.env')

def read_env_file():
    env_file = get_env_file_path()
    if not os.path.exists(env_file):
        print(f"错误：找不到 .env 文件：{env_file}")
        return None
    
    config = {}
    with open(env_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                config[key.strip()] = value.strip()
    
    return config

def write_env_file(config):
    env_file = get_env_file_path()
    
    with open(env_file, 'w', encoding='utf-8') as f:
        f.write("# 应急响应系统 - 环境变量配置\n")
        f.write("# \n")
        f.write("# 重要提示：\n")
        f.write("# 1. 此文件包含敏感的API密钥，请勿提交到版本控制系统\n")
        f.write("# 2. 参考 API_CONFIG_GUIDE.md 获取详细的API密钥获取指南\n")
        f.write("# 3. 配置完成后，在系统设置页面点击\"保存并重新加载\"使配置生效\n")
        f.write("\n")
        f.write("# ============================================\n")
        f.write("# 地图API配置 (MAP_API_KEY)\n")
        f.write("# ============================================\n")
        f.write("MAP_API_KEY=" + config.get('MAP_API_KEY', 'your_map_api_key_here') + "\n")
        f.write("\n")
        f.write("# ============================================\n")
        f.write("# 天气API配置 (WEATHER_API_KEY)\n")
        f.write("# ============================================\n")
        f.write("WEATHER_API_KEY=" + config.get('WEATHER_API_KEY', 'your_weather_api_key_here') + "\n")
        f.write("\n")
        f.write("# ============================================\n")
        f.write("# 短信API配置 (SMS_API_KEY)\n")
        f.write("# ============================================\n")
        f.write("SMS_API_KEY=" + config.get('SMS_API_KEY', 'your_sms_api_key_here') + "\n")
        f.write("\n")
        f.write("# ============================================\n")
        f.write("# 通知API配置 (NOTIFICATION_API_KEY)\n")
        f.write("# ============================================\n")
        f.write("NOTIFICATION_API_KEY=" + config.get('NOTIFICATION_API_KEY', 'your_notification_api_key_here') + "\n")
        f.write("\n")
        f.write("# ============================================\n")
        f.write("# 测试配置（可选）\n")
        f.write("# ============================================\n")
        f.write("TEST_API_KEY=''\n")
        f.write("\n")
        f.write("# ============================================\n")
        f.write("# 批量配置示例（可选）\n")
        f.write("# ============================================\n")
        f.write("BATCH_KEY_1='batch_value_1'\n")
        f.write("BATCH_KEY_2='batch_value_2'\n")
    
    print(f"✅ 配置已保存到：{env_file}")

def show_current_config():
    config = read_env_file()
    if config is None:
        return
    
    print("\n当前配置：")
    print("-" * 60)
    
    keys = ['MAP_API_KEY', 'WEATHER_API_KEY', 'SMS_API_KEY', 'NOTIFICATION_API_KEY']
    names = {
        'MAP_API_KEY': '地图API密钥',
        'WEATHER_API_KEY': '天气API密钥',
        'SMS_API_KEY': '短信API密钥',
        'NOTIFICATION_API_KEY': '通知API密钥'
    }
    
    for key in keys:
        value = config.get(key, '未配置')
        if value.startswith('your_') or value == '':
            status = "❌ 未配置"
        else:
            status = "✅ 已配置"
        print(f"{names[key]}: {status}")
        if not value.startswith('your_') and value != '':
            print(f"  值: {value[:20]}..." if len(value) > 20 else f"  值: {value}")
    
    print("-" * 60)
    print()

def configure_api_key(key_name, display_name):
    config = read_env_file()
    if config is None:
        return
    
    print(f"\n配置 {display_name}")
    print("-" * 60)
    
    current_value = config.get(key_name, '未配置')
    if not current_value.startswith('your_') and current_value != '':
        print(f"当前值: {current_value}")
    
    print(f"\n请输入新的 {display_name} (留空保持不变):")
    new_value = input().strip()
    
    if new_value:
        config[key_name] = new_value
        write_env_file(config)
        print(f"✅ {display_name} 已更新")
    else:
        print("ℹ️ 保持不变")
    
    print()

def main():
    print_header()
    
    print("欢迎使用API快速配置工具！")
    print("此工具将帮助您快速配置应急响应系统的API密钥。")
    print()
    
    config = read_env_file()
    if config is None:
        return
    
    while True:
        print_menu()
        choice = input("请输入选项 (1-7): ").strip()
        
        if choice == '1':
            configure_api_key('MAP_API_KEY', '地图API密钥')
        elif choice == '2':
            configure_api_key('WEATHER_API_KEY', '天气API密钥')
        elif choice == '3':
            configure_api_key('SMS_API_KEY', '短信API密钥')
        elif choice == '4':
            configure_api_key('NOTIFICATION_API_KEY', '通知API密钥')
        elif choice == '5':
            print("\n配置所有API密钥")
            print("-" * 60)
            
            map_key = input("请输入地图API密钥: ").strip()
            weather_key = input("请输入天气API密钥: ").strip()
            sms_key = input("请输入短信API密钥: ").strip()
            notification_key = input("请输入通知API密钥: ").strip()
            
            if map_key:
                config['MAP_API_KEY'] = map_key
            if weather_key:
                config['WEATHER_API_KEY'] = weather_key
            if sms_key:
                config['SMS_API_KEY'] = sms_key
            if notification_key:
                config['NOTIFICATION_API_KEY'] = notification_key
            
            write_env_file(config)
            print("✅ 所有API密钥已更新")
            print()
        elif choice == '6':
            show_current_config()
        elif choice == '7':
            print("\n感谢使用！")
            print("💡 提示：配置完成后，请在系统设置页面点击\"保存并重新加载\"使配置生效")
            break
        else:
            print("❌ 无效选项，请重新输入")
            print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n操作已取消")
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        sys.exit(1)
