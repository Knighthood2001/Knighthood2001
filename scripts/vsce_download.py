import json
import time

from vsce_downloads import get_extension_stats


def get_extension_downloads(extension_id):
    """获取单个 VS Code 扩展的下载统计。"""
    try:
        stats = get_extension_stats(extension_id)
        return {
            "success": True,
            "extension": extension_id,
            "vscode_download": int(stats.get("vscode_download", 0) or 0),
            "vsix_download": int(stats.get("vsix_download", 0) or 0),
            "total_install": int(stats.get("total_install", 0) or 0),
        }
    except Exception as e:
        print(f"获取{extension_id}数据失败: {str(e)}")
        return {
            "success": False,
            "extension": extension_id,
            "vscode_download": 0,
            "vsix_download": 0,
            "total_install": 0,
        }


if __name__ == "__main__":
    vsce_list = [
        "knighthood2001.urdf-formatting",
        "knighthood2001.ros-quick-runner",
        "knighthood2001.ros2-quick-runner",
        "knighthood2001.md-translator",
    ]
    for pkg in vsce_list:
        time.sleep(1)
        result = get_extension_downloads(pkg)
        print(json.dumps(result, indent=2))
        print(f"{pkg}总共下载量：{result['total_install']}")
