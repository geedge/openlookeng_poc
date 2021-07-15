# POC测试-xj

在OpenLookeng上执行POC测试
<https://docs.mesalab.cn/pages/viewpage.action?pageId=19860345>

### 目录结构

```
- install.sh         # 依赖安装脚本 （基于新疆环境,python2.7）
- run.sh             # 测试脚本
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
  - clickhouse_driver-0.1.2-cp27-cp27mu-manylinux1_x86_64.whl
  - clickhouse_driver-0.2.1-cp35-cp35m-manylinux1_x86_64.whl
  - requests_toolbelt-0.9.1-py2.py3-none-any.whl
```

## 安装依赖
Python 2环境
```
pip install ./whl/clickhouse_driver-0.1.2-cp27-cp27mu-manylinux1_x86_64.whl
pip install ./whl/requests_toolbelt-0.9.1-py2.py3-none-any.whl
```

Python 3环境
```
pip install ./whl/clickhouse_driver-0.2.1-cp35-cp35m-manylinux1_x86_64.whl
pip install ./whl/requests_toolbelt-0.9.1-py2.py3-none-any.whl
```

## 执行方式
```
./run.sh
```
等待执行完成后，将自动生成`log.tgz`压缩包，为各种日志的打包


## Todo

- 结果的行数统计