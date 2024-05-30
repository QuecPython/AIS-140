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
@file      : ais.py
@author    : Jack Sun (jack.sun@quectel.com)
@brief     : <Description>
@version   : v1.0.0
@date      : 2024-04-29 09:39:01
@copyright : Copyright (c) 2024
"""

import ure
import sys
import utime
import _thread
import usocket
from utils import crc32
from usr import logging

logger = logging.getLogger(__name__)


def checksum(data):
    data = data if isinstance(data, bytes) else str(data).encode()
    csum = 0
    for i in data:
        csum ^= i
    return hex(csum)[2:].upper()


def crc32_checksum(data):
    data = data if isinstance(data, bytes) else str(data).encode()
    csum = 0xFFFFFFFF
    try:
        csum = crc32().update(csum, data)
    except Exception:
        return None
    return hex(csum)[2:].upper()


class StrEnum:
    pass


class PacketTypes(StrEnum):
    NormalReport = "NR"
    EmergencyAlert = "EA"
    TemperAlert = "TA"
    HealthPacket = "HP"
    IgnitionOn = "IN"
    IgnitionOff = "IF"
    VehicleBatteryDisconnected = "BD"
    VehicleBatteryReconnected = "BR"
    InternalBatteryLow = "BL"
    HarshBreaking = "HB"
    HarshAcceleration = "HA"
    RashTurning = "RT"
    SOSEmergencyButtonWireDisconnect = "WD"
    OverspeedAlert = "OS"


class AlertID(StrEnum):
    LocationUpdate = "01"
    LocationUpdateHistory = "02"
    Mainsoff = "03"
    LowBattery = "04"
    LowBatteryremoved = "05"
    MainsOn = "06"
    IgnitionOn = "07"
    IgnitionOff = "08"
    TemperAlert = "09"
    EmergencyOn = "10"
    EmergencyOff = "11"
    OTAAlert = "12"
    HarshBreaking = "13"
    HarshAcceleration = "14"
    RashTurning = "15"
    WireDisconnect = "16"
    Overspeed = "17"


class TCPUDPBase:
    """This class is TCP/UDP base module."""

    def __init__(self, ip=None, port=None, domain=None, method="TCP", timeout=600, keep_alive=0):
        """
        Args:
            ip: server ip address (default: {None})
            port: server port (default: {None})
            domain: server domain (default: {None})
            method: TCP or UDP (default: {"TCP"})
        """
        self.__ip = ip
        self.__port = port
        self.__domain = domain
        self.__addr = None
        self.__method = method
        self.__socket = None
        self.__socket_args = []
        self.__timeout = timeout
        self.__keep_alive = keep_alive
        self.__socket_lock = _thread.allocate_lock()
        self.__conn_tag = 0
        self.__tid = None
        self.__callback = print
        self.__stack_size = 0x2000

    def __init_addr(self):
        """Get ip and port from domain.

        Raises:
            ValueError: Domain DNS parsing falied.
        """
        if self.__domain is not None and self.__domain:
            if self.__port is None:
                self.__port == 8883 if self.__domain.startswith("https://") else 1883
            try:
                addr_info = usocket.getaddrinfo(self.__domain, self.__port)
                self.__ip = addr_info[0][-1][0]
            except Exception as e:
                sys.print_exception(e)
                raise ValueError("Domain %s DNS parsing error. %s" % (self.__domain, str(e)))
        self.__addr = (self.__ip, self.__port)

    def __init_socket(self):
        """Init socket by ip, port and method

        Raises:
            ValueError: ip or domain or method is illegal.
        """
        if self.__check_ipv4():
            socket_af = usocket.AF_INET
        elif self.__check_ipv6():
            socket_af = usocket.AF_INET6
        else:
            raise ValueError("Args ip %s is illegal!" % self.__ip)

        if self.__method == 'TCP':
            socket_type = usocket.SOCK_STREAM
            socket_proto = usocket.IPPROTO_TCP
        elif self.__method == 'UDP':
            socket_type = usocket.SOCK_DGRAM
            socket_proto = usocket.IPPROTO_UDP
        else:
            raise ValueError("Args method is TCP or UDP, not %s" % self.__method)
        self.__socket_args = (socket_af, socket_type, socket_proto)

    def __check_ipv4(self):
        """Check ip is ipv4.

        Returns:
            bool: True - ip is ipv4, False - ip is not ipv4
        """
        self.__ipv4_item = r"(25[0-5]|2[0-4]\d|[01]?\d\d?)"
        self.__ipv4_regex = r"^{item}\.{item}\.{item}\.{item}$".format(item=self.__ipv4_item)
        if self.__ip.find(":") == -1:
            ipv4_re = ure.search(self.__ipv4_regex, self.__ip)
            if ipv4_re:
                if ipv4_re.group(0) == self.__ip:
                    return True
        return False

    def __check_ipv6(self):
        """Check ip is ipv6.

        Returns:
            bool: True - ip is ipv6, False - ip is not ipv6
        """
        self.__ipv6_code = r"[0-9a-fA-F]"
        ipv6_item_format = [self.__ipv6_code * i for i in range(1, 5)]
        self.__ipv6_item = r"{}|{}|{}|{}".format(*ipv6_item_format)

        if self.ip.startswith("::") or ure.search(self.__ipv6_item + ":", self.__ip):
            return True
        else:
            return False

    def __connect(self):
        """Socket connect when method is TCP

        Returns:
            bool: True - success, False - falied
        """
        with self.__socket_lock:
            self.__init_addr()
            self.__init_socket()
            if self.__socket_args:
                try:
                    logger.debug("self.__socket_args %s" % str(self.__socket_args))
                    self.__socket = usocket.socket(*self.__socket_args)
                    if self.__method == 'TCP':
                        logger.debug("self.__addr %s" % str(self.__addr))
                        self.__socket.connect(self.__addr)
                        if 1 <= self.__keep_alive <= 120:
                            self.__socket.setsockopt(usocket.SOL_SOCKET, usocket.TCP_KEEPALIVE, self.__keep_alive)
                    return True
                except Exception as e:
                    sys.print_exception(e)
            return False

    def __disconnect(self):
        """Socket disconnect

        Returns:
            bool: True - success, False - falied
        """
        with self.__socket_lock:
            if self.__socket is not None:
                try:
                    self.__socket.close()
                    self.__socket = None
                    return True
                except Exception as e:
                    sys.print_exception(e)
                    return False
            else:
                return True

    def __send(self, data):
        """Send data by socket.

        Args:
            data(bytes): byte stream

        Returns:
            bool: True - success, False - falied.
        """
        with self.__socket_lock:
            if self.__socket is not None:
                try:
                    if self.__method == "TCP":
                        write_data_num = self.__socket.write(data)
                        return (write_data_num == len(data))
                    elif self.__method == "UDP":
                        send_data_num = self.__socket.sendto(data, self.__addr)
                        return (send_data_num == len(data))
                except Exception as e:
                    sys.print_exception(e)
            return False

    def __read(self, bufsize=1024):
        """Read data by socket.

        Args:
            bufsize(int): read data size.

        Returns:
            bytes: read data info
        """
        logger.debug("start read")
        data = b""
        if self.__socket is not None:
            while True:
                read_data = b""
                try:
                    self.__socket.settimeout(0.5 if data else self.__timeout)
                    read_data = self.__socket.recv(bufsize)
                    logger.debug("read_data: %s" % read_data)
                except Exception as e:
                    if e.args[0] != 110:
                        sys.print_exception(e)
                        logger.error("%s read falied. error: %s" % (self.__method, repr(e)))
                data += read_data if read_data else b""
                if not read_data or len(data) >= bufsize:
                    break

        return data

    def __wait_msg(self):
        _msg = b""
        while self.__conn_tag:
            if self.status() != 0:
                if self.status() != 1:
                    self.__disconnect()
                    self.__connect()
                logger.error("%s connection status is %s" % (self.__method, self.status()))
                utime.sleep(1)
                continue
            _msg += self.__read()
            if not _msg:
                continue
            _msg = self.parse(_msg)

    def __downlink_thread_start(self):
        """This function starts a thread to read the data sent by the server"""
        if self.__tid is None or (self.__tid and not _thread.threadIsRunning(self.__tid)):
            _thread.stack_size(self.__stack_size)
            self.__tid = _thread.start_new_thread(self.__wait_msg, ())

    def __downlink_thread_stop(self):
        """This function stop the thread that read the data sent by the server"""
        if self.__tid:
            _cnt = 0
            while _thread.threadIsRunning(self.__tid) and _cnt < 300:
                utime.sleep_ms(10)
                _cnt += 1
            if _thread.threadIsRunning(self.__tid):
                _thread.stop_thread(self.__tid)
            self.__tid = None

    def parse(self, msg):
        if callable(self.__callback):
            self.__callback("Receive msg %s" % repr(msg))
        else:
            logger.info("Receive msg %s" % repr(msg))

        return b""

    def status(self):
        """Get socket connection status

        Returns:
            [int]:
                -1: Error
                 0: Connected
                 1: Connecting
                 2: Disconnect
        """
        _status = -1
        if self.__socket is not None:
            try:
                if self.__method == "TCP":
                    socket_sta = self.__socket.getsocketsta()
                    if socket_sta in range(4):
                        # Connecting
                        _status = 1
                    elif socket_sta == 4:
                        # Connected
                        _status = 0
                    elif socket_sta in range(5, 11):
                        # Disconnect
                        _status = 2
                elif self.__method == "UDP":
                    _status = 0
            except Exception as e:
                sys.print_exception(e)

        return _status

    def set_callback(self, callback):
        if callable(callback):
            self.__callback = callback
            return True
        return False

    def connect(self):
        """Connect server and start downlink thread for server

        Returns:
            bool: True - success, False - failed
        """
        if self.__conn_tag == 0:
            if self.__connect():
                self.__conn_tag = 1
                self.__downlink_thread_start()
                return True
        return False

    def disconnect(self):
        """Disconnect server, than stop downlink thread and heart beat timer

        Returns:
            bool: True - success, False - failed
        """
        if self.__conn_tag == 1:
            self.__conn_tag = 0
            self.__socket.settimeout(0.1)
            self.__downlink_thread_stop()
            return self.__disconnect()
        return True


class AISClient(TCPUDPBase):

    def __init__(self, ip=None, port=None, domain=None, method="TCP", timeout=600, keep_alive=0):
        super().__init__(ip=ip, port=port, domain=domain, method=method, timeout=timeout, keep_alive=keep_alive)
        self.fn = None
        self.__cmd_regex = r"(SET|GET|CLR)\s([A-Z]+):?(.*)"

    def __send_msg(self, msg, timeout=10):
        res = False
        last_ack_size = self.__socket.getsendacksize()
        if self.__send(msg):
            logger.debug("__send msg: %s" % msg)
            if timeout > 0:
                run_time = 0
                # logger.debug("run_time %s, last_ack_size %s, now_ack_size %s" % (run_time, last_ack_size, self.__socket.getsendacksize()))
                while (run_time < timeout * 1000) and (self.__socket.getsendacksize() - last_ack_size) < len(msg):
                    utime.sleep_ms(10)
                    run_time += 10
                    # logger.debug("run_time %s, last_ack_size %s, now_ack_size %s" % (run_time, last_ack_size, self.__socket.getsendacksize()))
                res = (self.__socket.getsendacksize() - last_ack_size) == len(msg)
            else:
                res = True
        return res

    def _frame_number(self):
        try:
            if not self.fn:
                self.fn = iter(range(1, 999999))
            _fn = next(self.fn)
            return "{:06d}".format(_fn)
        except Exception:
            self.fn = None
            return self._frame_number()

    def parse(self, msg):
        msg = msg.decode()
        while msg:
            rematch = ure.match(self.__cmd_regex, msg)
            if rematch:
                total_cmd, cmd_type, cmd_key, cmd_val = [rematch.group(i) for i in range(4)]
                if msg != total_cmd:
                    sindex = msg.find(total_cmd)
                    msg = msg[0:sindex] + msg[sindex + len(total_cmd):]
                else:
                    msg = ""
                if callable(self.__callback):
                    self.__callback(*(cmd_type, cmd_key, cmd_val))
            else:
                break
        msg = msg.encode()
        return msg

    def send_login(self, vender_id, device_name, imei, firmware_version, protocal_version, latitude,
                   latitude_dir, longitude, longtiude_dir):
        kwgs = {
            "vender_id": vender_id,
            "device_name": device_name,
            "imei": imei,
            "firmware_version": firmware_version,
            "protocal_version": protocal_version,
            "latitude": latitude,
            "latitude_dir": latitude_dir,
            "longitude": longitude,
            "longtiude_dir": longtiude_dir
        }
        msg = "$,LGN,{vender_id},{device_name},{imei},{firmware_version},{protocal_version}," \
              "{latitude},{latitude_dir},{longitude},{longtiude_dir}*".format(**kwgs)
        return self.__send_msg(msg)

    def send_heart_beat(self, vender_id, firmware_version, imei, battery_percentage,
                        Low_battery_threshold_value, memory_percentage,
                        data_update_rate_when_ignition_on, data_update_rate_when_ignition_off,
                        digital_io_status, analog_io_status):
        kwgs = {
            "vender_id": vender_id,
            "firmware_version": firmware_version,
            "imei": imei,
            "battery_percentage": battery_percentage,
            "Low_battery_threshold_value": Low_battery_threshold_value,
            "memory_percentage": memory_percentage,
            "data_update_rate_when_ignition_on": data_update_rate_when_ignition_on,
            "data_update_rate_when_ignition_off": data_update_rate_when_ignition_off,
            "digital_io_status": digital_io_status,
            "analog_io_status": analog_io_status
        }
        msg = "$,HBT,{vender_id},{firmware_version},{imei},{battery_percentage}," \
              "{Low_battery_threshold_value},{memory_percentage},{data_update_rate_when_ignition_on}," \
              "{data_update_rate_when_ignition_off},{digital_io_status},{analog_io_status}*".format(**kwgs)
        return self.__send_msg(msg)

    def send_loction_alert_information(self, vender_id, firmware_version, packet_type, alert_id,
                                       packet_status, imei, vehicle_reg_no, gps_fix, date, time,
                                       latitude, latitude_dir, longitude, longitude_dir, speed,
                                       heading, no_of_satellites, altitude, pdop, hdop,
                                       operator_name, ignition, main_power_status, main_input_voltage,
                                       internal_battery_voltage, emergency_status, temper_alert,
                                       gsm_strength, mcc, mnc, lac, cell_id, nmr, digital_input_status,
                                       digital_output_status, analog_input_1, analog_input_2, odometer):
        kwgs = {
            "vender_id": vender_id,
            "firmware_version": firmware_version,
            "packet_type": packet_type,
            "alert_id": alert_id,
            "packet_status": packet_status,
            "imei": imei,
            "vehicle_reg_no": vehicle_reg_no,
            "gps_fix": gps_fix,
            "date": date,
            "time": time,
            "latitude": latitude,
            "latitude_dir": latitude_dir,
            "longitude": longitude,
            "longitude_dir": longitude_dir,
            "speed": speed,
            "heading": heading,
            "no_of_satellites": no_of_satellites,
            "altitude": altitude,
            "pdop": pdop,
            "hdop": hdop,
            "operator_name": operator_name,
            "ignition": ignition,
            "main_power_status": main_power_status,
            "main_input_voltage": main_input_voltage,
            "internal_battery_voltage": internal_battery_voltage,
            "emergency_status": emergency_status,
            "temper_alert": temper_alert,
            "gsm_strength": gsm_strength,
            "mcc": mcc,
            "mnc": mnc,
            "lac": lac,
            "cell_id": cell_id,
            "nmr": nmr,
            "digital_input_status": digital_input_status,
            "digital_output_status": digital_output_status,
            "analog_input_1": analog_input_1,
            "analog_input_2": analog_input_2,
            "odometer": odometer,
            "frame_number": self._frame_number()
        }
        msg = "$,NRM,{vender_id},{firmware_version},{packet_type},{alert_id},{packet_status}," \
              "{imei},{vehicle_reg_no},{gps_fix},{date},{time},{latitude},{latitude_dir}," \
              "{longitude},{longitude_dir},{speed},{heading},{no_of_satellites},{altitude}," \
              "{pdop},{hdop},{operator_name},{ignition},{main_power_status},{main_input_voltage}," \
              "{internal_battery_voltage},{emergency_status},{temper_alert},{gsm_strength},{mcc},{mnc}," \
              "{lac},{cell_id},{nmr},{digital_input_status},{digital_output_status},{analog_input_1}," \
              "{analog_input_2},{odometer},{frame_number}".format(**kwgs)
        check_sum = checksum(msg[2:])
        msg += ",%s*" % check_sum
        return self.__send_msg(msg)

    def send_emergency(self, vender_id, packet_type, imei, packet_status, date_time, gps_fix, latitude,
                       latitude_dir, longitude, longitude_dir, altitude, speed, distance, provider,
                       vehicle_reg_no, reply_number):
        kwgs = {
            "vender_id": vender_id,
            "packet_type": packet_type,
            "imei": imei,
            "packet_status": packet_status,
            "date_time": date_time,
            "gps_fix": gps_fix,
            "latitude": latitude,
            "latitude_dir": latitude_dir,
            "longitude": longitude,
            "longitude_dir": longitude_dir,
            "altitude": altitude,
            "speed": speed,
            "distance": distance,
            "provider": provider,
            "vehicle_reg_no": vehicle_reg_no,
            "reply_number": reply_number
        }
        msg = "$,EPB,{vender_id},{packet_type},{imei},{packet_status},{date_time},{gps_fix}," \
              "{latitude},{latitude_dir},{longitude},{longitude_dir},{altitude},{speed}," \
              "{distance},{provider},{vehicle_reg_no},{reply_number}*".format(**kwgs)
        check_sum = crc32_checksum(msg)
        msg += check_sum
        return self.__send_msg(msg)
