# AIS-140

中文 | [English](./README.md)

## 简介

当前项目基于 QuecPython 语言开发。

目前支持的版本为 AIS-140 (2016)。

该库的目的是提供构建车辆位置跟踪和紧急按钮的构建块。 **该库不提供完整的解决方案，因为任何实现都是特定于其预期用途的**。该库中的文档提供了有关如何最好地构建完整解决方案的指导。

**注意:**

> 要运行这些示例，需要依赖项 usocket 模块!

## 车辆定位跟踪和紧急按钮

`demo/ais_client_demo.py` 是一个车辆位置跟踪和紧急按钮演示。

```python
from usr.ais import AISClient

# Receive Server Commands Funtion.
def server_cmd(cmd, key, val):
    """This function is for receiving server commands.

    Args:
        cmd(str): SET/GET/CLR.
        key(str):
            PIP - Primary Server IP
            PPT - Primary Server Port
            SIP - Secondary Server IP
            SPT - Secondary Server Port
            EO  - Emergency OFF
            ED  - Emergency Duration
            APN - Network APN
            SL  - Speed Limit
            VN  - Vehicle Registration Number
            UR  - Update Rate
            URE - Update Rate Emergency
            URH - Update Rate Health Packet
            VID - Vendor ID
            ODM - Set Odometer
        val(str): Value of commmand key.
    """
    print("cmd[%s], key[%s], val[%s]" % (cmd, key, val))


def main():
    # Init AIS Client.
    cfg = {
        "ip": "xxx.xxx.xxx.xxx",
        "port": 9000,
    }
    ais_client = AISClient(**cfg)
    ais_client.set_callback(server_cmd)

    # Connect Server
    res = ais_client.connect()

    # Send Login Packet
    login_kwargs = {...}
    res = ais_client.send_login(**login_kwargs)
    print("ais_client.send_login() %s" % res)

    # Send Health Monitoring Packet
    hbt_kwargs = {...}
    res = ais_client.send_health_monitoring(**hbt_kwargs)
    print("ais_client.send_health_monitoring() %s" % res)

    # Send Location/Alert Information Packet
    lai_kwargs = {...}
    res = ais_client.send_loction_alert_information(**lai_kwargs)
    print("ais_client.send_loction_alert_information() %s" % res)

    # Send Emergency Packet
    meg_kwargs = {...}
    res = ais_client.send_emergency(**meg_kwargs)
    print("ais_client.send_emergency() %s" % res)

    # Disconnect Server
    res = ais_client.disconnect()
    print("ais_client.disconnect() %s" % res)
```

## 项目文件说明

```shell
|-- code
    |-- ais.py
    |-- logging.py
|-- demo
    |-- ais_client_demo.py
    |-- ais_server_demo.py
|-- docs
    |-- AIS-140 (2016).pdf
    |-- VT140-Protocol_V1._20200104.pdf
```

- `code` 该目录包含了 AIS 客户端代码。
  - `code/ais.py` 该文件包含了所有 AIS 客户端请求接口.
  - `code/logging.py` 该文件为日志模块.
- `demo` 该目录包含了 AIS 客户端样例和 AIS 服务器样例.
  - `demo/ais_client_demo.py` 该文件是一个基于 QuecPython 的 AIS 客户端样例.
  - `demo/ais_server_demo.py` 该文件是一个基于 CPython 的 AIS 服务端样例.
- `docs` 该目录包含了 AIS-140 协议相关文档.

## 如何使用

### 运行 AIS-140 服务

> 如果您有自己的 AIS-140 服务器，则可以跳过此说明。

#### 1. 安装环境

- 操作系统: Window or Linux.

- 语言: Python (Python-3.11.2).

#### 2. 配置服务器并运行样例

- 在 `demo/ais_server_demo.py` 文件中修改你的服务器端口.

```python
SERVER_PORT = 31500  # 修改为你自己的服务的端口
...

if __name__ == '__main__':
    try:
        logging.info("Start Server !")
        socket_serve = TCPServer(('', SERVER_PORT), ReceiveHandler)
        for i in range(THREAD_WORKERS_NUM):
            t = Thread(target=socket_serve.serve_forever)
            t.daemon = True
            t.start()
        socket_serve.serve_forever()
    except KeyboardInterrupt:
        socket_serve.shutdown()
        logging.info("Stop Server !")
```

- 运行 `python demo/ais_server_demo.py` 文件. 当看到交互输出 `[INFO] xxxx-xx-xxx xxx xx:xx:xx ais_server_demo.py: Start Server !`, 则服务端已经正常启动。

```shell
>>> python ais_server_demo.py
[INFO] xxxx-xx-xxx xxx xx:xx:xx ais_server_demo.py: Start Server !
```

### 运行 AIS-140 客户端

#### 1. 运行环境

您需要使用我们的 QuecPython 模块。

#### 2. 配置客户端并运行样例

- 在 `demo/ais_client_demo.py` 文件中配置服务器ip和端口。

```python
if __name__ == "__main__":
    # Init AIS Client.
    cfg = {
        "ip": "xxx.xxx.xxx.xxx",
        "port": 9000,
    }  #  Use your own server ip and port.
    ais_client = AISClient(**cfg)
    ais_client.set_callback(server_cmd)
```

- 将代码下载到 QuecPython 模块

**注意:**

> 如何下载 python 代码并在 QuecPython 模块中运行 python demo 可参考 [QuecPython 文档中心](https://python.quectel.com/doc/Getting_started/en/index.html)。

您可以将完整的 `code` 目录代码 和 `demo/ais_client_demo.py` 下载到我们的 QuecPython 模块，并运行 `ais_client_demo.py` 来测试 AIS-140 车辆位置跟踪和紧急按钮。

你可以在 QPYcom工具的交互界面看到日志 `ais_client.send_login() True.`, 则 `Login Packet` 消息报已经发送到服务器端.

**注意:**

> 您可以参考`demo/ais_client_demo.py`来编写符合业务逻辑的客户端请求。

## 用法

- [API 参考手册](./docs/zh/API参考手册.md)
- [客户端示例代码](./demo/ais_client_demo.py)
- [服务端示例代码](./demo/ais_server_demo.py)

## 贡献

我们欢迎对本项目的改进做出贡献！请按照以下步骤进行贡献：

1. Fork 此仓库。
2. 创建一个新分支（`git checkout -b feature/your-feature`）。
3. 提交您的更改（`git commit -m 'Add your feature'`）。
4. 推送到分支（`git push origin feature/your-feature`）。
5. 打开一个 Pull Request。

## 许可证

本项目使用 Apache 许可证。详细信息请参阅 [LICENSE](./LICENSE) 文件。

## 支持

如果您有任何问题或需要支持，请参阅 [QuecPython 文档](https://python.quectel.com/doc) 或在本仓库中打开一个 issue。
