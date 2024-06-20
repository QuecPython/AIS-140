# AIS-140 API Reference

[中文](../zh/API参考手册.md) | English

This module is based on the TCP/UDP protocol and implements the relevant functions of the AIS-140 protocol client module, including data reporting and instruction reception and analysis functions.

## AIS-140 Client Module Initialization

### `AISClient`

> To initialize the AIS-140 client module, you need to provide the corresponding server IP or domain name, port, connection mode (TCP/UDP), etc.

```python
from usr.ais import AISClient

# Init AIS Client.
ais_client = AISClient(
    ip="xxx.xxx.xxx.xxx",
    port=9000,
    method="TCP",
    timeout=600,
    keep_alive=0
)
```

**Parameter Description:**

|Parameters|Type|Description|
|:---|:---|:---|
|ip|str|Server IPV4/IPV6 address|
|port|int|Server port number|
|domain|str|Server domain name (this parameter and `ip` can be optionally filled in). If both are filled in, the domain name will be used as the connection address.|
|method|str|Protocol type, `TCP` / `UDP`, default: `TCP`|
|timeout|int|Timeout for receiving server messages, unit: seconds, default: 600|
|keep_alive|int|TCP protocol keep-alive time, unit: minutes, default: 0, range: 0 ~ 120, when it is 0, the TCP keep-alive mechanism is not enabled|

**Return Value Description:**

|Type|Description|
|:---|:---|
|obj|AIS-140 client instance object|

## Set server command callback function

### `AISClient.set_callback`

> Used to receive instructions issued by the server to set, query, and clear device configurations.

```python
def server_cmd(cmd, key, val):
    logger.debug("cmd[%s], key[%s], val[%s]" % (cmd, key, val))

res = ais_client.set_callback(server_cmd)
```

**Callback Parameter Description:**

|Parameters|Type|Description|
|:---|:---|:---|
|cmd|str|Instruction operation type:<br>`SET` - Set up<br>`GET` - Query<br>`CLR` - Clear|
|key|str|Command identifier:<br>`PIP` - Primary Server IP (Primary server ip or domain)<br>`PPT` - Primary Server Port<br>`SIP` - Secondary Server IP (Secondary server ip or domain)<br>`SPT` - Secondary Server Port<br>`EO`  - Emergency OFF (Emergency OFF or stop emergency message. Only set is allowed with this key.)<br>`ED`  - Emergency Duration (Emergency timeout duration in minutes.)<br>`APN` - Network APN (Network access point name)<br>`SL`  - Speed Limit (Speed limit in km/h)<br>`VN`  - Vehicle Registration Number<br>`UR`  - Update Rate (Update duration/data rate in seconds when Vehicle in motion.)<br>`URE` - Update Rate Emergency (Update duration or data rate in seconds for emergency packet.)<br>`URH` - Update Rate Health Packet (Update duration or data rate in minutes for health monitoring packet.)<br>`VID` - Vendor ID<br>`ODM` - Odometer (This command can be used to reset odometer or set odometer to a value. The value is in kilometers and can be floating point.)|
|val|str|Command identifier value|

**Return Value Description:**

|Type|Description|
|:---|:---|
|bool|`True` - Success<br>`False` - Fail|

## Connect To Server

### `AISClient.connect`

> Establish a TCP/UDP connection with the server.

```python
# Connect Server
res = ais_client.connect()
```

**Return Value Description:**

|Type|Description|
|:---|:---|
|bool|`True` - Success<br>`False` - Fail|

## Disconnect From Server

### `AISClient.disconnect`

> Disconnect the TCP/UDP connection from the server.

```python
# Disconnect Server
res = ais_client.disconnect()
```

**Return Value Description:**

|Type|Description|
|:---|:---|
|bool|`True` - Success<br>`False` - Fail|

## Send Login Packet

### `AISClient.send_login`

> A login packet is sent to server whenever there is a new TCP connection made by device to server.

```python
# Send Login Packet
login_kwargs = {
    "vender_id": "QUECTEL",
    "vehicle_reg_no": "car123456",
    "imei": "IMEI",
    "firmware_version": "FIRMWARE_VERSION",
    "protocal_version": "AIS140",
    "latitude": "12.896545",
    "latitude_dir": "N",
    "longitude": "76.358759",
    "longtiude_dir": "E"
}
res = ais_client.send_login(**login_kwargs)
```

**Parameter Description:**

|Parameters|Type|Description|
|:---|:---|:---|
|vender_id|str|Manufacturer's Name|
|vehicle_reg_no|str|Vehicle number on which the device is installed|
|imei|str|IMEI|
|firmware_version|str|Version of the firmware used in the hardware|
|protocal_version|str|Version of the frame format protocol.|
|latitude|str|The current setpoint value of the latitude, upto 6 decimal places|
|latitude_dir|str|N (North) / S (South)|
|longitude|str|The current setpoint value longitude, upto 6 decimal places|
|longitude_dir|str|E (East) / W (West)|

**Return Value Description:**

|Type|Description|
|:---|:---|
|bool|`True` - Success<br>`False` - Fail|

## Send Health Monitoring Packets

### `AISClient.send_health_monitoring`

> This packet defines status or health of device.

```python
# Send Health Monitoring Packet
hbt_kwargs = {
    "vender_id": "QUECTEL",
    "firmware_version": "FIRMWARE_VERSION",
    "imei": "IMEI",
    "battery_percentage": "60%",
    "Low_battery_threshold_value": "30%",
    "memory_percentage": "30%",
    "data_update_rate_when_ignition_on": 10,
    "data_update_rate_when_ignition_off": 60,
    "digital_io_status": "0001",
    "analog_io_status": 12.6
}
res = ais_client.send_health_monitoring(**hbt_kwargs)
```

**Parameter Description:**

|Parameters|Type|Description|
|:---|:---|:---|
|vender_id|str|Manufacturer's Name|
|firmware_version|str|Version of the firmware used in the hardware|
|imei|str|IMEI|
|battery_percentage|str|Built-in battery percentage|
|Low_battery_threshold_value|str|Low battery alarm threshold percentage|
|memory_percentage|str|Indicates flash memory used in percentage|
|data_update_rate_when_ignition_on|int|ACC ON data upload interval (s)|
|data_update_rate_when_ignition_off|int|ACC OFF data upload interval (s)|
|digital_io_status|str|Digital input status:<br>0001 (DIN1 = 0，DIN2 = 0，DIN3 = 0，DIN4 = 1)|
|analog_io_status|float|Analog input status (in V)|

**Return Value Description:**

|Type|Description|
|:---|:---|
|bool|`True` - Success<br>`False` - Fail|

## Send Positioning or Alarm Data Packets

### `AISClient.send_loction_alert_information`

> This is a periodic location information packet sent by device to server.

```python
# Send Location/Alert Information Packet
lai_kwargs = {
    "vender_id": "QUECTEL",
    "firmware_version": "FIRMWARE_VERSION",
    "packet_type": PacketTypes.NormalReport,
    "alert_id": AlertID.LocationUpdate,
    "packet_status": "L",
    "imei": "IMEI",
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
```

**Parameter Description:**

|Parameters|Type|Description|
|:---|:---|:---|
|vender_id|str|Manufacturer's Name|
|firmware_version|str|Version of the firmware used in the hardware|
|packet_type|str|See [`PacketTypes`](#packettypes) enumeration type|
|alert_id|str|See [`AlertID`](#alertid) enumeration type|
|packet_status|str|Status of packet<br>`L` - Live Packet<br>`H` - History Packet|
|imei|str|IMEI|
|vehicle_reg_no|str|Mapped Vehicle Registration Number|
|gps_fix|int|GPS Fix information<br>0 - GPS Invalid<br>1 - GPS Fix|
|date|str|Date value as per GPS in DDMMYYYY format|
|time|str|Time value as per GPS in HHMMSS format|
|latitude|str|Latitude value upto 6 decimal places|
|latitude_dir|str|N (North) / S (South)|
|longitude|str|Longitude value upto 6 decimal places|
|longitude_dir|str|E (East) / W (West)|
|speed|float|Speed of vehicle upto 1 decimal place in km/h|
|heading|float|Course over ground in degrees|
|no_of_satellites|int|No. of satellite in view for location fix|
|altitude|int|Altitude of device in meters|
|pdop|foat|Positional dilution of precision|
|hdop|float|Horizontal dilution of precision|
|operator_name|str|Name of network operator|
|ignition|int|Status of Ignition<br>0 - Ignition Off<br>1 - Ignition On|
|main_power_status|int|Main power status<br>0 - Vehicle Battery Disconnected<br>1 - Vehicle Battery Connected|
|main_input_voltage|float|Indicator showing source voltage in Volts (Upto 1 decimal place)|
|internal_battery_voltage|float|Indicator of battery charge in volts (upto 1 decimal place)|
|emergency_status|int|Emergency status<br>0 - Emergency Off<br>1 - Emergency On|
|temper_alert|str|Temper alert<br>`O` - Box open<br>`C` - Box Closed|
|gsm_strength|int|Value range from 0 – 31|
|mcc|int|Mobile Country Code|
|mnc|int|Mobile Network Code|
|lac|int|Location Area Code|
|cell_id|int|GSM Cell ID|
|nmr|str|NMR (Network Measurement Report)<br>Cell ID, LAC and Signal Strength of 4 Neighboring cells<br>Such as: `(CELL ID,LAC,GSM STRENGTH)` * 4|
|digital_input_status|str|Status of 4 Digital Inputs in order:<br>[DIN3, DIN2, DIN1, DIN0]<br>0 - Off, 1 - On<br>Such as: `0001`|
|digital_output_status|str|Status of 2 Digital Outputs in order:<br>[DOUT1, DOUT0]<br>0 - Off, 1 - On<br>Such as: `01`|
|analog_input_1|float|Analog Input 1 voltage in V|
|analog_input_2|float|Analog Input 2 voltage in V|
|odometer|int|Odometer value in m|

**Return Value Description:**

|Type|Description|
|:---|:---|
|bool|`True` - Success<br>`False` - Fail|

## Send Emergency Alert Packet

### `AISClient.send_emergency`

> When SOS button is pressed, device send following emergency packet to server.

```python
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
```

**Parameter Description:**

|Parameters|Type|Description|
|:---|:---|:---|
|vender_id|str|Manufacturer's Name|
|packet_type|str|Emergency Packet type<br>`EMR` - Emergency Message<br>`SEM` - Stop Message|
|imei|str|IMEI|
|packet_status|str|Status of packet<br>`NM` - Normal Packet<br>`SP` - Stored Packet|
|date_time|str|Date value as per GPS date time per GPS time (DDMMYYYYHHmmss)|
|gps_fix|str|GPS Fix information<br>`V` - GPS Invalid<br>`A` - GPS fix|
|latitude|str|Latitude value upto 6 decimal places|
|latitude_dir|str|N (North) / S (South)|
|longitude|str|Longitude value upto 6 decimal places|
|longitude_dir|str|E (East) / W (West)|
|altitude|int|Altitude of device in meters|
|speed|float|Speed of vehicle upto 1 decimal place in km/h|
|distance|int|Distance calculated from previous GPS data|
|provider|str|`G` - Fine GPS<br>`N` - Coarse GPS or data from Netwrok|
|vehicle_reg_no|str|Vehicle Registration Number|
|reply_number|str|The mobile number to which Test response needs to be sent. If not, fill in `NA`.|

**Return Value Description:**

|Type|Description|
|:---|:---|
|bool|`True` - Success<br>`False` - Fail|

## <span id="packettypes">Packet Type Enumeration Value</span>

### PacketTypes

> Packet type enumeration value, used to send positioning or alarm data packets `send_loction_alert_information` interface `packet_type` parameter.

```python
from usr.ais import PacketTypes

PacketTypes.NormalReport
PacketTypes.EmergencyAlert
...
```

**Enumeration Value Description:**

|Enumeration value|Corresponding value|Description|
|:---|:---|:---|
|NormalReport|`NR`|Normal Report|
|EmergencyAlert|`EA`|Emergency Alert|
|TemperAlert|`TA`|Temper Alert|
|HealthPacket|`HP`|Health Packet|
|IgnitionOn|`IN`|Ignition On|
|IgnitionOff|`IF`|Ignition Off|
|VehicleBatteryDisconnected|`BD`|Vehicle Battery Disconnected|
|VehicleBatteryReconnected|`BR`|Vehicle Battery Reconnected|
|InternalBatteryLow|`BL`|Internal Battery Low|
|HarshBreaking|`HB`|Harsh Breaking|
|HarshAcceleration|`HA`|Harsh Acceleration|
|RashTurning|`RT`|Rash Turning|
|SOSEmergencyButtonWireDisconnect|`WD`|SOS Emergency Button Wire Disconnect|
|OverspeedAlert|`OS`|Overspeed Alert|

## <span id="alertid">Alarm Identification Enumeration Value</span>

### AlertID

> Alarm ID enumeration value, used to send positioning or alarm data packets `send_loction_alert_information` interface `alert_id` parameter.

```python
from usr.ais import AlertID

AlertID.LocationUpdate
AlertID.LocationUpdateHistory
...
```

**Enumeration Value Description:**

|Enumeration value|Corresponding value|Description|
|:---|:---|:---|
|LocationUpdate|`01`|Default Message from device|
|LocationUpdateHistory|`02`|If GPRS is not available at time of sending message|
|Mainsoff|`03`|When device is disconnected from vehicle battery|
|LowBattery|`04`|Device internal battery low alert|
|LowBatteryremoved|`05`|Device internal battery ok|
|MainsOn|`06`|Device is reconnected to vehicle battery|
|IgnitionOn|`07`|Vehicle ignition on alert|
|IgnitionOff|`08`|Vehicle Ignition off alert|
|TemperAlert|`09`|Device box open|
|EmergencyOn|`10`|Emergency on alert|
|EmergencyOff|`11`|Emergency off alert|
|OTAAlert|`12`|Parameter change/query alert packet|
|HarshBreaking|`13`|Alert indication a hash break|
|HarshAcceleration|`14`|Alert indicating harsh acceleration|
|RashTurning|`15`|Alert indicating rash turn|
|WireDisconnect|`16`|SOS/Emergency button wire disconnect alert|
|Overspeed|`17`|Alert indicating overspeed|
