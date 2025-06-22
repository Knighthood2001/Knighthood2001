import requests
import os
import json
from datetime import datetime

def get_pypi_stats(package_name):
    """通过PyPI Stats API获取下载数据"""
    # 近期下载量（天/周/月）
    recent_url = f"https://pypistats.org/api/packages/{package_name}/recent"
    recent_response = requests.get(recent_url)
    recent_data = recent_response.json()
    
    # 整体下载量（最近30天）
    overall_url = f"https://pypistats.org/api/packages/{package_name}/overall"
    overall_response = requests.get(overall_url)
    overall_data = overall_response.json()
    
    return {
        "package": package_name,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "recent_downloads": recent_data.get("data", {}),
        "overall_downloads": overall_data.get("data", [])[:30]  # 取最近30天
    }

if __name__ == "__main__":
    package_name = os.environ.get("PYPACKAGE_NAME")
    if not package_name:
        print("❌ 未设置PYPACKAGE_NAME环境变量")
        exit(1)
    
    try:
        stats = get_pypi_stats(package_name)
        with open("stats.json", "w", encoding="utf-8") as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)
        print(f"✅ 成功获取{package_name}的下载数据")
    except Exception as e:
        print(f"❌ 获取数据失败: {str(e)}")
        exit(1)
