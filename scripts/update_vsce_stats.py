import json
import os
import re
import time
from datetime import datetime, timedelta
from pathlib import Path

from vsce_download import get_extension_downloads


STATS_FILE = Path("./assets/vsce_stats.json")
SNAPSHOT_RETENTION_DAYS = 14


def load_historical_data():
    """加载 VS Code 扩展历史数据文件。"""
    if STATS_FILE.exists():
        with open(STATS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_historical_data(data):
    """保存 VS Code 扩展历史数据文件。"""
    STATS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STATS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def parse_snapshot_time(snapshot):
    try:
        return datetime.fromisoformat(snapshot["time"])
    except (KeyError, TypeError, ValueError):
        return None


def get_last_24h_downloads(history, current_total, now):
    cutoff = now - timedelta(hours=24)
    baseline = None
    baseline_time = None

    for snapshot in history.get("snapshots", []):
        snapshot_time = parse_snapshot_time(snapshot)
        if snapshot_time is None or snapshot_time > cutoff:
            continue

        if baseline_time is None or snapshot_time > baseline_time:
            baseline = snapshot
            baseline_time = snapshot_time

    if baseline is None:
        return 0

    return max(current_total - int(baseline.get("total", 0)), 0)


def prune_snapshots(snapshots, now):
    retention_start = now - timedelta(days=SNAPSHOT_RETENTION_DAYS)
    pruned = []

    for snapshot in snapshots:
        snapshot_time = parse_snapshot_time(snapshot)
        if snapshot_time is None or snapshot_time < retention_start:
            continue
        pruned.append(snapshot)

    return pruned


def update_readme(extension_list):
    """更新 README 和 VS Code 扩展历史数据。"""
    historical_data = load_historical_data()
    all_stats = []
    failed_extensions = []
    total_last_24h = 0
    total_all = 0
    now = datetime.now()
    today = now.strftime("%Y-%m-%d")

    for extension_id in extension_list:
        time.sleep(1)
        stats = get_extension_downloads(extension_id)
        if not stats.get("success", False):
            failed_extensions.append(extension_id)
            continue

        current_total = stats["total_install"]

        if extension_id not in historical_data:
            historical_data[extension_id] = {
                "last_update": "",
                "total": current_total,
                "daily_data": {},
                "snapshots": [],
            }

        extension_history = historical_data[extension_id]
        extension_history.setdefault("daily_data", {})
        extension_history.setdefault("snapshots", [])

        last_24h_downloads = get_last_24h_downloads(
            extension_history,
            current_total,
            now,
        )

        extension_history["daily_data"][today] = last_24h_downloads
        extension_history["last_update"] = today
        extension_history["total"] = current_total
        extension_history["snapshots"].append(
            {
                "time": now.isoformat(timespec="seconds"),
                "total": current_total,
            }
        )
        extension_history["snapshots"] = prune_snapshots(
            extension_history["snapshots"],
            now,
        )

        stats["last_24h_downloads"] = last_24h_downloads
        all_stats.append(stats)
        total_last_24h += last_24h_downloads
        total_all += current_total

        print(
            f"{extension_id}近24小时下载量：{last_24h_downloads}     "
            f"总共下载量：{current_total}"
        )

    if failed_extensions:
        raise RuntimeError(
            "以下 VS Code 扩展统计获取失败，已中止更新: "
            + ", ".join(failed_extensions)
        )

    save_historical_data(historical_data)

    stats_content = """
<h3>Vscode Extension Statistics</h3>
<table>
  <thead align="center">
    <tr border: none;>
      <td><b>🧩 Extension</b></td>
      <td><b>📊 Last 24h</b></td>
      <td><b>📥 Total</b></td>
    </tr>
  </thead>
  <tbody>"""

    for stats in all_stats:
        extension_id = stats["extension"]
        extension_name = extension_id.split(".", 1)[1] if "." in extension_id else extension_id
        stats_content += f"""
    <tr>
      <td><a href="https://marketplace.visualstudio.com/items?itemName={extension_id}"><b>{extension_name}</b></a></td>
      <td align="center">{stats['last_24h_downloads']}</td>
      <td align="center">{stats['total_install']:,}</td>
    </tr>"""

    stats_content += f"""
    <tr>
      <td><b>Total</b></td>
      <td align="center">{total_last_24h}</td>
      <td align="center">{total_all:,}</td>
    </tr>
  </tbody>
</table>
"""

    try:
        with open("README.md", "r", encoding="utf-8") as f:
            readme = f.read()

        updated_readme = re.sub(
            r"<!-- VSCE_STATS:Start -->.*?<!-- VSCE_STATS:End -->",
            f"<!-- VSCE_STATS:Start -->\n{stats_content}\n<!-- VSCE_STATS:End -->",
            readme,
            flags=re.DOTALL,
        )

        with open("README.md", "w", encoding="utf-8") as f:
            f.write(updated_readme)
        print("✅ README更新成功")
    except Exception as e:
        print(f"❌ 更新README失败: {str(e)}")
        raise


if __name__ == "__main__":
    print("---------- 更新VS Code扩展下载统计 ----------")
    extension_list = [
        extension.strip()
        for extension in os.environ.get("VSCE_EXTENSIONS", "").split(",")
        if extension.strip()
    ]
    if not extension_list:
        print("❌ 未设置扩展列表，请设置VSCE_EXTENSIONS环境变量")
        exit(1)

    print(f"正在获取 {', '.join(extension_list)} 的下载数据...")
    update_readme(extension_list)
    print("---------- 更新完成 ----------")
