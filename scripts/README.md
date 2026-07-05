# 如何更新下载统计
在update_stats.yml中
```shell
env:
  # 替换为你的包名，用逗号分隔
  PYPI_PACKAGES: "ros-pointcloud-recorder,tree2json,tree2proj,auto-model-monitor"
  # 替换为你的 VS Code 扩展 ID，用逗号分隔
  VSCE_EXTENSIONS: "knighthood2001.urdf-formatting,knighthood2001.ros-quick-runner"
  GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```
将你需要更新的 PyPI 包名替换到`PYPI_PACKAGES`中，将 VS Code 扩展 ID 替换到`VSCE_EXTENSIONS`中，并用逗号分隔。

然后你就可以git push上传，上传后会自动触发workflow，更新你的数据，数据会更新到`Knighthood2001/assets/pypi_stats.json`和`Knighthood2001/assets/vsce_stats.json`中。
