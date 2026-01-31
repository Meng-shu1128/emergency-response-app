import sys
import os
sys.path.append(os.getcwd())

from utils.database import generate_mock_data, get_users, get_alerts

print("正在生成模拟数据...")
result = generate_mock_data()

print("\n✅ 模拟数据生成成功！")
print(f"  - 生成用户: {result['users']} 个")
print(f"  - 生成历史警报: {result['alerts']} 条")
print(f"  - 生成今日警报: {result['today_alerts']} 条")
print(f"  - 总计警报: {result['total_alerts']} 条")

users = get_users()
alerts_result = get_alerts()
alerts = alerts_result.get('data', []) if isinstance(alerts_result, dict) else alerts_result

print(f"\n数据库统计：")
print(f"  - 用户总数: {len(users)}")
print(f"  - 警报总数: {len(alerts)}")

if users:
    print(f"\n用户列表：")
    for user in users:
        print(f"  - {user['name']} ({user['phone']})")

if alerts:
    print(f"\n最近5条警报：")
    for alert in alerts[-5:]:
        status = alert['status']
        print(f"  - ID: {alert['id']}, 状态: {status}")

print("\n🎉 完成！请访问 http://localhost:8501 查看应用")
