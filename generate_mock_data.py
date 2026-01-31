"""
快速生成模拟数据脚本
用于快速生成应急响应系统的模拟数据
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.database import generate_mock_data, get_users, get_alerts

def print_header():
    print("=" * 60)
    print("        应急响应系统 - 模拟数据生成工具")
    print("=" * 60)
    print()

def main():
    print_header()
    
    print("此工具将为应急响应系统生成模拟数据，包括：")
    print("  - 5个模拟老人用户")
    print("  - 10条模拟历史警报记录")
    print("  - 3条模拟今日警报")
    print()
    
    confirm = input("确认要生成模拟数据吗？(y/n): ").strip().lower()
    
    if confirm != 'y':
        print("操作已取消")
        return
    
    print()
    print("正在生成模拟数据...")
    print("-" * 60)
    
    try:
        result = generate_mock_data()
        
        print("✅ 模拟数据生成成功！")
        print()
        print("生成统计：")
        print(f"  - 生成用户: {result['users']} 个")
        print(f"  - 生成历史警报: {result['alerts']} 条")
        print(f"  - 生成今日警报: {result['today_alerts']} 条")
        print(f"  - 总计警报: {result['total_alerts']} 条")
        print()
        
        print("-" * 60)
        print()
        print("正在验证数据...")
        
        users = get_users()
        alerts_result = get_alerts()
        alerts = alerts_result.get('data', []) if isinstance(alerts_result, dict) else alerts_result
        
        print(f"✅ 数据库中现有用户: {len(users)} 个")
        print(f"✅ 数据库中现有警报: {len(alerts)} 条")
        print()
        
        if users:
            print("用户列表：")
            for user in users:
                print(f"  - ID: {user['id']}, 姓名: {user['name']}, 电话: {user['phone']}")
            print()
        
        if alerts:
            print("警报列表（最近5条）：")
            for alert in alerts[-5:]:
                status_badge = {
                    'pending': '⏳ 待处理',
                    'processing': '🔄 处理中',
                    'resolved': '✅ 已解决'
                }
                status = status_badge.get(alert['status'], alert['status'])
                print(f"  - ID: {alert['id']}, 用户: {alert.get('user_name', 'N/A')}, 状态: {status}")
            print()
        
        print("=" * 60)
        print("🎉 模拟数据生成完成！")
        print("=" * 60)
        print()
        print("💡 提示：")
        print("  1. 打开浏览器访问应用: http://localhost:8501")
        print("  2. 查看'📊 后台仪表盘'查看数据统计")
        print("  3. 查看'👴 老人端模拟界面'测试用户功能")
        print()
        
    except Exception as e:
        print(f"❌ 生成模拟数据时出错: {e}")
        import sys
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n操作已取消")
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        sys.exit(1)
