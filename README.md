

在OpenLookeng上执行POC测试
<https://docs.mesalab.cn/display/DataVirtualizationEngine-




### 目录结构

```
- install.sh         # 依赖安装脚本 （基于新疆环境,python2.7）
- run.sh             # 测试脚本
- require
> log 日志目录
  - install.log      # 安装日志
  - ch-result.log    # ClickHouse运行统计日志
  - ol-result.log    # OpenLookeng运行统计日志
  - ch-*.json        # ClickHouse单次执行详细结果
  - ol-*.json        # OpenLookeng单次执行详细结果
> src
  - auto-ol.json     # OpenLookeng测试语句
  - poc-ch.json      # ClickHouse测试语句
  - config           # 配置文件
  - openlookeng_driver.py  #openlookeng驱动文件
  - run.py           # python自动化测试脚本
  - convert_sql.py   # 根据poc-ch.json生成openlookeng语法的测试集
> whl                # 离线安装包目录
  - clickhouse_driver-0.1.2-cp27-cp27m-manylinux1_x86_64.whl
  - clickhouse_driver-0.1.2-cp27-cp27mu-manylinux1_x86_64.whl
  - clickhouse_driver-0.2.1-cp35-cp35m-manylinux1_x86_64.whl
  - requests_toolbelt-0.9.1-py2.py3-none-any.whl
```

## Todo

- csv文件下载失败
- 结果的行数统计