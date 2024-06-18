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
@file      : ais_client_demo.py
@author    : Jack Sun (jack.sun@quectel.com)
@brief     : <Description>
@version   : v1.0.0
@date      : 2024-04-29 14:41:17
@copyright : Copyright (c) 2024
"""
import modem
import utime as time
from usr.ais import AISClient, PacketTypes, AlertID
from usr import logging

logger = logging.getLogger(__name__)


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
    logger.debug("cmd[%s], key[%s], val[%s]" % (cmd, key, val))


if __name__ == "__main__":
    # Init AIS Client.
    cfg = {
        "ip": "XXX.XXX.XXX.XXX",
        "port": 31500,
    }
    ais_client = AISClient(**cfg)
    ais_client.set_callback(server_cmd)

    # Connect Server
    res = ais_client.connect()
    logger.debug("ais_client.connect() %s" % res)
    time.sleep(1)

    # Send Login Packet
    login_kwargs = {
        "vender_id": "QUECTEL",
        "vehicle_reg_no": "car123456",
        "imei": modem.getDevImei(),
        "firmware_version": modem.getDevFwVersion(),
        "protocal_version": "AIS140",
        "latitude": "12.896545",
        "latitude_dir": "N",
        "longitude": "76.358759",
        "longtiude_dir": "E"
    }
    res = ais_client.send_login(**login_kwargs)
    logger.debug("ais_client.send_login() %s" % res)
    time.sleep(1)

    # Send Health Monitoring Packet
    hbt_kwargs = {
        "vender_id": "QUECTEL",
        "firmware_version": modem.getDevFwVersion(),
        "imei": modem.getDevImei(),
        "battery_percentage": "60%",
        "Low_battery_threshold_value": "30%",
        "memory_percentage": "30%",
        "data_update_rate_when_ignition_on": 10,
        "data_update_rate_when_ignition_off": 60,
        "digital_io_status": "0001",
        "analog_io_status": 12.6
    }
    res = ais_client.send_health_monitoring(**hbt_kwargs)
    logger.debug("ais_client.send_health_monitoring() %s" % res)
    time.sleep(1)

    # Send Location/Alert Information Packet
    lai_kwargs = {
        "vender_id": "QUECTEL",
        "firmware_version": modem.getDevFwVersion(),
        "packet_type": PacketTypes.NormalReport,
        "alert_id": AlertID.LocationUpdate,
        "packet_status": "L",
        "imei": modem.getDevImei(),
        "vehicle_reg_no": "car123456",
        "gps_fix": 1,
        "date": "29042024",
        "time": "152000",
        "latitude": "12.896545",
        "latitude_dir": "N",
        "longitude": "76.358759",
        "longitude_dir": "E",
        "speed": 25,
        "heading": 135,
        "no_of_satellites": 10,
        "altitude": 76,
        "pdop": 2.5,
        "hdop": 1.9,
        "operator_name": "QUECTEL",
        "ignition": 1,
        "main_power_status": 1,
        "main_input_voltage": 12.4,
        "internal_battery_voltage": 4.2,
        "emergency_status": 0,
        "temper_alert": "C",
        "gsm_strength": 31,
        "mcc": 404,
        "mnc": 98,
        "lac": 123,
        "cell_id": 456,
        "nmr": "1,2,3,1,2,3,1,2,3,1,2,3",
        "digital_input_status": "0000",
        "digital_output_status": "00",
        "analog_input_1": 6.7,
        "analog_input_2": 2.5,
        "odometer": 123456,
    }
    res = ais_client.send_loction_alert_information(**lai_kwargs)
    logger.debug("ais_client.send_loction_alert_information() %s" % res)
    time.sleep(1)

    # Send Emergency Packet
    meg_kwargs = {
        "vender_id": "QUECTEL",
        "packet_type": "EMR",
        "imei": modem.getDevImei(),
        "packet_status": "NM",
        "date_time": "18122017124850",
        "gps_fix": "A",
        "latitude": 12.896545,
        "latitude_dir": "N",
        "longitude": 76.358759,
        "longitude_dir": "E",
        "altitude": 123,
        "speed": 25,
        "distance": 12345,
        "provider": "G",
        "vehicle_reg_no": "CAR12345",
        "reply_number": "NA"
    }
    res = ais_client.send_emergency(**meg_kwargs)
    logger.debug("ais_client.send_emergency() %s" % res)

    # Wait receive server messages.
    time.sleep(20)

    # Disconnect Server
    res = ais_client.disconnect()
    logger.debug("ais_client.disconnect() %s" % res)
