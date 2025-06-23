import requests
import os
import re
import json
from datetime import datetime
import time

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
            "total": total_downloads
        }
    except Exception as e:
        print(f"获取{package_name}数据失败: {str(e)}")
        return {
            "package": package_name,
            "last_day": 0,
            "total": 0
        }

def update_readme(package_list):
    """更新README.md中的下载统计部分"""
    # 获取所有包的统计数据
    all_stats = []
    total_last_day = 0
    total_all = 0
    
    for pkg in package_list:
        time.sleep(1)  # 避免频繁请求
        stats = get_package_downloads(pkg)
        all_stats.append(stats)
        total_last_day += stats["last_day"]
        total_all += stats["total"]
        print(f"{pkg}的一天下载量：{stats['last_day']}     总共下载量：{stats['total']}")
    
    # 生成统计内容
    stats_content = "### Python Package Download Stats\n\n"
    for stats in all_stats:
        stats_content += f"- **{stats['package']}**\n  - Last 24 hours: {stats['last_day']} downloads\n  - Total downloads: {stats['total']} downloads\n\n"
    
    stats_content += f"- **Total**\n  - Last 24 hours: {total_last_day} downloads\n  - Total downloads: {total_all} downloads\n"
    stats_content += f"- Data update time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    # 读取并更新README
    try:
        with open("README.md", "r", encoding="utf-8") as f:
            readme = f.read()
        
        # 使用标记替换统计部分
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
