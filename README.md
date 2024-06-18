# AIS-140

[中文](./README_ZH.md) | English

## Introduction

This is based on QuecPython.

Currently AIS-140 (2016) is supported.

The purpose of this library is to provide the building blocks to construct a vehicle location tracking and emergency button. **The library does not provide a completed solution, as any implementation is specific for its intended use**. The documents in this library should be inspected, as these documents provided guidance on how best to build a complete solution.

**Note:**

> To run these examples the dependency usocket is required!

## Vehicle Location Tracking and Emergency Button

The `demo/ais_client_demo.py` is a Vehicle Location Tracking and Emergency Button demo.

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

## Project Files Description

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

- `code` floder is incloud AIS client codes.
  - `code/ais.py` is incloud all ais client requests interface.
  - `code/logging.py` is log module.
- `demo` floder is incloud AIS client demo and AIS server demo.
  - `demo/ais_client_demo.py` is an AIS client demo base on QuecPython.
  - `demo/ais_server_demo.py` is an AIS server demo base on CPython.
- `docs` floder is incloud AIS-140 protocal documents.

## How To Use

### Running AIS-140 Server

> If you have your own AIS-140 server, you can skip this instruction.

#### 1. Install environments

- Operating System: Window or Linux.

- Language: Python (Python-3.11.2).

#### 2. Config server and running demo

- Change your server port in `demo/ais_server_demo.py`.

```python
SERVER_PORT = 31500  # Change this port value for your own server port.
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

- Running `python demo/ais_server_demo.py`. When output `[INFO] xxxx-xx-xxx xxx xx:xx:xx ais_server_demo.py: Start Server !`, the server is started.

```shell
>>> python ais_server_demo.py
[INFO] xxxx-xx-xxx xxx xx:xx:xx ais_server_demo.py: Start Server !
```

### Running AIS-140 Client

#### 1. Running environment

You need to use our QuecPython module.

#### 2. Config client and running demo

- Config your server host and port in `demo/ais_client_demo.py`

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

- Download code to QuecPython module

**Note:**

> You can find documents in [QuecPython Document Center](https://python.quectel.com/doc/Getting_started/en/index.html) for how to download python code and running python demo in our QuecPython module

You can download full `code` floder and `demo/ais_client_demo.py` to our QuecPython module and run `ais_client_demo.py` to test AIS-140 Vehicle Location Tracking and Emergency Button.

You can see log `ais_client.send_login() True.` in our QPYcom REPL, than the `Login Packet` message is sented to server.

**Note:**

> You can refer to `demo/ais_client_demo.py` to write client requests that conform to business logic.

## Usage

- [API Reference Manual](./docs/en/API_Reference.md)
- [Client Example Code](./demo/ais_client_demo.py)
- [Server Example Code](./demo/ais_server_demo.py)

## Contribution

We welcome contributions to improve this project! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m 'Add your feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a Pull Request.

## License

This project is licensed under the Apache License. See the [LICENSE](./LICENSE) file for details.

## Support

If you have any questions or need support, please refer to the [QuecPython documentation](https://python.quectel.com/doc/en) or open an issue in this repository.
