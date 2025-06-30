import requests
import os
import re
import json
from datetime import datetime
import time
from pathlib import Path
from get_pypi_lastday_download import *


def get_package_downloads(package_name):
    """获取单个包的最近1天下载量和总下载量"""
    try:
        # 获取最近一天下载量（包含镜像和非镜像）
        last_day_data = get_lastday_download(package_name)
        
        # 获取总下载量（最近180天，包含镜像源）
        overall_url = f"https://pypistats.org/api/packages/{package_name}/overall"
        overall_response = requests.get(overall_url, timeout=10)
        overall_response.raise_for_status()  # 检查请求是否成功
        
        overall_data = overall_response.json()
        total_downloads = sum(item["downloads"] for item in overall_data.get("data", []))
        
        # 将总下载量合并到last_day_data中
        last_day_data["pypi_total"] = total_downloads
        
        return last_day_data
    
    except Exception as e:
        print(f"获取{package_name}数据失败: {str(e)}")
        return {
            "package_name": package_name,
            "last_day": None,
            "download": 0,
            "pypi_total": 0
        }


if __name__ == "__main__":
    package_list = ["ros-pointcloud-recorder", "tree2json", "tree2proj"]
    for pkg in package_list:
        time.sleep(1)
        result = get_package_downloads(pkg)
        print(json.dumps(result, indent=2))
        print(f"{pkg}的一天下载量：{result['download']}     总共下载量：{result['pypi_total']}")
