import requests
import os
import re
import json
from datetime import datetime
import time
from pathlib import Path

from pypi_download import get_package_downloads

# def get_package_downloads(package_name):
#     """获取单个包的最近1天下载量和总下载量"""
#     try:
#         # 最近1天下载量，这个只会得到非镜像的下载次数
#         recent_url = f"https://pypistats.org/api/packages/{package_name}/recent"
#         recent_response = requests.get(recent_url, timeout=10)
#         recent_data = recent_response.json()
#         last_day = recent_data.get("data", {}).get("last_day", 0)
        
#         # 总下载量（通过整体接口获取所有时间数据的总和）
#         overall_url = f"https://pypistats.org/api/packages/{package_name}/overall"
#         overall_response = requests.get(overall_url, timeout=10)
#         overall_data = overall_response.json()
#         total_downloads = sum(item["downloads"] for item in overall_data.get("data", []))
        
#         return {
#             "package": package_name,
#             "last_day": last_day,
#             "pypi_total": total_downloads  # # 明确表示这是 PyPI 接口的 180 天总和
#         }
#     except Exception as e:
#         print(f"获取{package_name}数据失败: {str(e)}")
#         return {
#             "package": package_name,
#             "last_day": 0,
#             "pypi_total": 0
#         }

def load_historical_data():
    """加载历史数据文件"""
    file_path = Path("./assets/pypi_stats.json")
    if file_path.exists():
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_historical_data(data):
    """保存历史数据文件"""
    with open("./assets/pypi_stats.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

# 更加美观
def update_readme(package_list):
    """更新 README 和历史数据"""
    historical_data = load_historical_data()
    all_stats = []
    total_last_day = 0
    total_all = 0

    for pkg in package_list:
        time.sleep(1)
        stats = get_package_downloads(pkg)
        print(f"{pkg}的一天下载量：{stats['download']}     总共下载量：{stats['pypi_total']}")
        
        # 更新历史数据（累加每日下载量）
        if pkg not in historical_data:
            historical_data[pkg] = {
                "last_update": "", 
                "total": stats["pypi_total"],
                "daily_data": {}  
            }
        
        today = datetime.now().strftime("%Y-%m-%d")
        if historical_data[pkg]["last_update"] != today:
            historical_data[pkg]["total"] += stats["download"]
            historical_data[pkg]["last_update"] = today
            historical_data[pkg]["daily_data"][today] = stats["download"]
        
        stats["historical_total"] = historical_data[pkg]["total"]
        all_stats.append(stats)
        total_last_day += stats["download"]
        total_all += stats["historical_total"]

    # 保存历史数据
    save_historical_data(historical_data)

    # 生成精美的表格内容
    stats_content = """
<h3>PyPI Download Statistics</h3>
<table>
  <thead align="center">
    <tr border: none;>
      <td><b>📦 Package</b></td>
      <td><b>📊 Last 24h</b></td>
      <td><b>📈 Total</b></td>
    </tr>
  </thead>
  <tbody>"""
    
    for stats in all_stats:
        stats_content += f"""
    <tr>
      <td><a href="https://pypi.org/project/{stats['package']}/"><b>{stats['package']}</b></a></td>
      <td align="center">{stats['download']}</td>
      <td align="center">{stats['historical_total']:,}</td>
    </tr>"""
    
    stats_content += f"""
    <tr>
      <td><b>Total</b></td>
      <td align="center">{total_last_day}</td>
      <td align="center">{total_all:,}</td>
    </tr>
  </tbody>
</table>
<p align="right"><sub>Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</sub></p>
"""

    try:
        # 更新 README.md
        with open("README.md", "r", encoding="utf-8") as f:
            readme = f.read()
        
        updated_readme = re.sub(
            r"<!-- PYPI_STATS:Start -->.*?<!-- PYPI_STATS:End -->",
            f"<!-- PYPI_STATS:Start -->\n{stats_content}\n<!-- PYPI_STATS:End -->",
            readme,
            flags=re.DOTALL
        )
        
        with open("README.md", "w", encoding="utf-8") as f:
            f.write(updated_readme)
        print("✅ README更新成功")
    except Exception as e:
        print(f"❌ 更新README失败: {str(e)}")
if __name__ == "__main__":
    print("---------- 更新PyPI下载统计 ----------")
    # 从环境变量获取包列表，多个包用逗号分隔
    package_list = os.environ.get("PYPI_PACKAGES", "").split(",")
    if not package_list or package_list[0] == "":
        print("❌ 未设置包列表，请设置PYPI_PACKAGES环境变量")
        exit(1)
    
    print(f"正在获取 {', '.join(package_list)} 的下载数据...")
    update_readme(package_list)
    print("---------- 更新完成 ----------")
