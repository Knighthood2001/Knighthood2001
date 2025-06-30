import requests
import json
from datetime import datetime, timedelta
import time
"""
获取pypi中昨天的下载量，包含镜像源和非镜像源
"""
def get_mirror_lastday_download(package_name):
    """获取包含镜像源的最近一天下载量"""
    try:
        url = f"https://pypistats.org/api/packages/{package_name}/overall?mirrors=true"
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # 检查请求是否成功
        
        data = response.json()
        items = data.get("data", [])
        
        if not items:
            return {
                "package_name": package_name,
                "last_day": None,
                "download": 0
            }
        
        # 找到最新日期的记录
        latest_item = max(items, key=lambda x: x["date"])
        
        return {
            "package_name": package_name,
            "last_day": latest_item["date"],
            "download": latest_item["downloads"]
        }
    
    except Exception as e:
        print(f"获取{package_name}镜像数据失败: {e}")
        return {
            "package_name": package_name,
            "last_day": None,
            "download": 0
        }

def get_without_mirror_lastday_download(package_name):
    """获取不包含镜像源的最近一天下载量"""
    try:
        url = f"https://pypistats.org/api/packages/{package_name}/recent"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        last_day_downloads = data.get("data", {}).get("last_day", 0)
        
        # 计算实际日期（通常是昨天）
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        
        return {
            "package_name": package_name,
            "last_day": yesterday,
            "download": last_day_downloads
        }
    
    except Exception as e:
        print(f"获取{package_name}非镜像数据失败: {e}")
        return {
            "package_name": package_name,
            "last_day": None,
            "download": 0
        }

def get_lastday_download(package_name):
    """获取总下载量（镜像+非镜像）"""
    # 获取镜像和非镜像数据
    mirror_data = get_mirror_lastday_download(package_name)
    without_mirror_data = get_without_mirror_lastday_download(package_name)
    
    # 合并数据
    return {
        "package_name": package_name,
        "last_day": mirror_data["last_day"],  # 使用镜像数据的日期（更准确）
        "download": mirror_data["download"] + without_mirror_data["download"]
    }

# 示例使用
if __name__ == "__main__":
    package_list = ["ros-pointcloud-recorder", "tree2json", "tree2proj"]
    for pkg in package_list:
        time.sleep(1)
        result = get_lastday_download(pkg)
        print(json.dumps(result, indent=2))
