import requests
import os
import json
from datetime import datetime

import requests
import os
import re
import json
from datetime import datetime
import time
from pathlib import Path

def get_package_downloads(package_name):
    """获取单个包的最近1天下载量和总下载量"""
    try:
        # 最近1天下载量
        recent_url = f"https://pypistats.org/api/packages/{package_name}/recent"
        recent_response = requests.get(recent_url, timeout=10)
        recent_data = recent_response.json()
        last_day = recent_data.get("data", {}).get("last_day", 0)
        
        # 总下载量（通过整体接口获取所有时间数据的总和）
        overall_url = f"https://pypistats.org/api/packages/{package_name}/overall"
        overall_response = requests.get(overall_url, timeout=10)
        overall_data = overall_response.json()
        total_downloads = sum(item["downloads"] for item in overall_data.get("data", []))
        
        return {
            "package": package_name,
            "last_day": last_day,
            "pypi_total": total_downloads  # # 明确表示这是 PyPI 接口的 180 天总和
        }
    except Exception as e:
        print(f"获取{package_name}数据失败: {str(e)}")
        return {
            "package": package_name,
            "last_day": 0,
            "pypi_total": 0
        }

if __name__ == "__main__":
    package_name = "tree2proj"
    stats = get_package_downloads(package_name)
    print(stats)

