# 如何更新pypi包
在update_pypi_stats.yml中
```shell
env:
# 替换为你的包名，用逗号分隔
PYPI_PACKAGES: "ros-pointcloud-recorder,tree2json,tree2proj,auto-model-monitor"
GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```
将你需要更新的包名替换到`PYPI_PACKAGES`中，并用逗号分隔。

然后你就可以git push上传，上传后会自动触发workflow，更新你的数据，数据会更新到`Knighthood2001/assets/pypi_stats.json`中。
