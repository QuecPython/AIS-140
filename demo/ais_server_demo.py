# Copyright (c) Quectel Wireless Solution, Co., Ltd.All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
@file      : ais_server_demo.py
@author    : Jack Sun (jack.sun@quectel.com)
@brief     : <Description>
@version   : v1.0.0
@date      : 2024-04-29 14:41:35
@copyright : Copyright (c) 2024
"""

import time
import logging
from threading import Thread
from socketserver import BaseRequestHandler, TCPServer

BUF_SIZE = 1024
SERVER_PORT = 31500
THREAD_WORKERS_NUM = 10
CMDS = [
    "SET PIP:example.com",
    "SET PPT:8011",
    "SET SIP:example.com",
    "SET SPT:8011",
    "SET EO",
    "SET ED:50",
    "SET APN:CMNET",
    "SET SL:120",
    "SET VN:666",
    "SET UR:10",
    "SET URE:20",
    "SET URH:5",
    "SET VID:ISTARTEK",
    "SET ODM:123"
]


# 自定义的日志
logging.basicConfig(
    level=logging.DEBUG,
    format='[%(levelname)s] %(asctime)s %(filename)s: %(message)s',
    datefmt='%Y-%m-%d %A %H:%M:%S',
    # filename='socket.log',
    filemode='a',
)


class ReceiveHandler(BaseRequestHandler):
    def setup(self):
        logging.info("Connect from: " + str(self.client_address))

    def handle(self):
        try:
            while True:
                msg = self.request.recv(BUF_SIZE)
                if msg:
                    logging.debug("RECIVE msg %s" % msg)
                    if msg.startswith(b"$,EPB,"):
                        for cmd in CMDS:
                            logging.debug("SEND cmd %s" % cmd)
                            self.request.sendall(cmd.encode())
                            time.sleep(1)
                else:
                    break
        except Exception as e:
            logging.warning('Exception is: ' + str(e))

    def finish(self):
        logging.info("Disconnect from: " + str(self.client_address))


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
