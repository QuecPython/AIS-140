# AIS-140 API 参考手册

中文 | [English](../en/API_Reference.md)

本模块基于 TCP/UDP 协议，实现了 AIS-140 协议客户端模块的相关功能，包含数据上报和指令接收解析功能。

## AIS-140 客户端模块初始化

### `AISClient`

> 初始化 AIS-140 客户端模块，需要提供对应服务器IP或域名，端口，连接模式（TCP/UDP）等。

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

**参数说明：**

|参数|类型|说明|
|:---|:---|:---|
|ip|str|对应服务器 IPV4/IPV6 地址|
|port|int|对应服务器端口号|
|domain|str|对应服务器域名（该参数与 `ip` 选填其实中一个即可），如果都填写，则以域名为连接地址|
|method|str|协议类型，`TCP` / `UDP`，默认：`TCP`|
|timeout|int|接收服务器消息超时时间，单位：秒，默认：600|
|keep_alive|int|TCP 协议保活时间，单位：分钟，默认：0，范围：0 ~ 120，当为 0 时，则不开启 TCP 保活机制|

**返回值说明：**

|类型|说明|
|:---|:---|
|obj|AIS-140 客户端实例对象|

## 设置服务器指令回调函数

### `AISClient.set_callback`

> 用于接收服务器下发的指令，设置、查询、清除设备配置。

```python
def server_cmd(cmd, key, val):
    logger.debug("cmd[%s], key[%s], val[%s]" % (cmd, key, val))

res = ais_client.set_callback(server_cmd)
```

**回调函数参数说明：**

|参数|类型|说明|
|:---|:---|:---|
|cmd|str|指令操作类型：<br>`SET` - 设置<br>`GET` - 查询<br>`CLR` - 清除|
|key|str|指令标识：<br>`PIP` - 主服务器 IP（主服务器IP或域名）<br>`PPT` - 主服务器端口<br>`SIP` - 辅助服务器 IP（辅助服务器IP或域名）<br>`SPT` - 辅助服务器端口<br>`EO`  - 紧急关闭（紧急关闭或停止紧急消息。仅允许使用此键进行设置。）<br>`ED`  - 紧急情况持续时间（紧急超时持续时间以分钟为单位。）<br>`APN` - 网络 APN（网络接入点名称）<br>`SL`  - 速度限制（速度限制以公里/小时为单位）<br>`VN`  - 车辆登记号码<br>`UR`  - 更新频率（车辆行驶时更新持续时间/数据速率（以秒为单位）。）<br>`URE` - 报警更新频率（更新紧急数据包的持续时间或数据速率（以秒为单位）。）<br>`URH` - 健康监控数据包更新频率（健康监控数据包的更新持续时间或数据速率（以分钟为单位）。）<br>`VID` - 供应商 ID<br>`ODM` - 设置里程表（该命令可用于重置里程表或将里程表设置为一个值。该值以公里为单位，可以是浮点数。）|
|val|str|指令标识值|

**返回值说明：**

|类型|说明|
|:---|:---|
|bool|`True` - 成功<br>`False` - 失败|

## 连接服务器

### `AISClient.connect`

> 与服务器建立 TCP/UDP 连接。

```python
# Connect Server
res = ais_client.connect()
```

**返回值说明：**

|类型|说明|
|:---|:---|
|bool|`True` - 成功<br>`False` - 失败|

## 断开服务器连接

### `AISClient.disconnect`

> 与服务器断开 TCP/UDP 连接。

```python
# Disconnect Server
res = ais_client.disconnect()
```

**返回值说明：**

|类型|说明|
|:---|:---|
|bool|`True` - 成功<br>`False` - 失败|

## 发送登录数据包

### `AISClient.send_login`

> 每当设备与服务器建立新的 TCP 连接时，就会向服务器发送登录数据包。

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

**参数说明：**

|参数|类型|说明|
|:---|:---|:---|
|vender_id|str|供应商 ID|
|vehicle_reg_no|str|车辆登记号|
|imei|str|IMEI号|
|firmware_version|str|固件版本|
|protocal_version|str|协议版本|
|latitude|str|纬度，精确到小数点后 6 位|
|latitude_dir|str|纬度方向，N（北）/ S（南）|
|longitude|str|经度，精确到小数点后 6 位|
|longitude_dir|str|经度方向，E（东）/ W（西）|

**返回值说明：**

|类型|说明|
|:---|:---|
|bool|`True` - 成功<br>`False` - 失败|

## 发送健康监控数据包

### `AISClient.send_health_monitoring`

> 该数据包定义设备的状态或健康状况。

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

**参数说明：**

|参数|类型|说明|
|:---|:---|:---|
|vender_id|str|供应商 ID|
|firmware_version|str|固件版本|
|imei|str|IMEI号|
|battery_percentage|str|电池电量百分比|
|Low_battery_threshold_value|str|低电报警阈值|
|memory_percentage|str|内存使用百分比|
|data_update_rate_when_ignition_on|int|设备点火时数据上报周期，单位：秒|
|data_update_rate_when_ignition_off|int|设备熄火时数据上报周期，单位：秒|
|digital_io_status|str|数字输入状态：<br>0001 (DIN1 = 0，DIN2 = 0，DIN3 = 0，DIN4 = 1)|
|analog_io_status|float|输入电压值，单位：伏（V）|

**返回值说明：**

|类型|说明|
|:---|:---|
|bool|`True` - 成功<br>`False` - 失败|

## 发送定位或报警数据包

### `AISClient.send_loction_alert_information`

> 这是设备向服务器周期性发送的位置信息包。

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

**参数说明：**

|参数|类型|说明|
|:---|:---|:---|
|vender_id|str|供应商 ID|
|firmware_version|str|固件版本|
|packet_type|str|详见 [`PacketTypes`](#packettypes) 枚举类型|
|alert_id|str|详见 [`AlertID`](#alertid) 枚举类型|
|packet_status|str|包状态<br>`L` - 实时数据包<br>`H` - 历史数据包|
|imei|str|IMEI号|
|vehicle_reg_no|str|车辆登记号|
|gps_fix|int|GPS 数据是否有效<br>0 - 无效<br>1 - 有效|
|date|str|GPS 日期数据，数据格式：DDMMYYYY（日月年）|
|time|str|GPS 时间数据，数据格式：HHmmss（时分秒）|
|latitude|str|纬度，精确到小数点后 6 位|
|latitude_dir|str|纬度方向，N（北）/ S（南）|
|longitude|str|经度，精确到小数点后 6 位|
|longitude_dir|str|经度方向，E（东）/ W（西）|
|speed|float|车辆速度，精确至小数点后 1 位（公里/小时）|
|heading|float|地面航向（以度为单位）|
|no_of_satellites|int|用于定位的可见卫星数量|
|altitude|int|设备的海拔高度（以米为单位）|
|pdop|foat|位置精度稀释|
|hdop|float|水平精度衰减|
|operator_name|str|网络运营商名称|
|ignition|int|点火状态<br>0 - 熄火<br>1 - 点火|
|main_power_status|int|主电源状态<br>0 - 车辆电池断开<br>1 - 车辆电池连接|
|main_input_voltage|float|显示源电压的指示器，单位为伏特（最多 1 位小数）|
|internal_battery_voltage|float|电池电量指示器（以伏特为单位）（精确到小数点后 1 位）|
|emergency_status|int|报警状态<br>0 - 报警关<br>1 - 报警开|
|temper_alert|str|防拆报警<br>`O` - 盒子打开<br>`C` - 盒子关闭|
|gsm_strength|int|GSM信号强度，范围 0 ~ 31|
|mcc|int|移动国家代码|
|mnc|int|移动网络代码|
|lac|int|位置区域码|
|cell_id|int|GSM 小区 ID|
|nmr|str|NMR（Network Measurement Report）（网络测量报告）<br>4 个相邻小区的小区 ID、LAC 和信号强度<br>如：`(CELL ID,LAC,GSM STRENGTH)` * 4|
|digital_input_status|str|4 个数字输入的状态（按顺序）：<br>[DIN3，DIN2，DIN1，DIN0]<br>0 - 关闭，1 - 开启<br>如：`0001`|
|digital_output_status|str|2 个数字输入的状态（按顺序）：<br>[DOUT1，DOUT0]<br>0 - 关闭，1 - 开启<br>如：`01`|
|analog_input_1|float|模拟输入 1 电压（V）|
|analog_input_2|float|模拟输入 2 电压（V）|
|odometer|int|里程表值（米）|

**返回值说明：**

|类型|说明|
|:---|:---|
|bool|`True` - 成功<br>`False` - 失败|

## 发送紧急报警数据包

### `AISClient.send_emergency`

> 当设备紧急按键被触发时，则开始上报该紧急报警数据包

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

**参数说明：**

|参数|类型|说明|
|:---|:---|:---|
|vender_id|str|供应商 ID|
|packet_type|str|紧急数据包类型<br>`EMR` - 紧急呼救信号<br>`SEM` - 停止讯息|
|imei|str|IMEI号|
|packet_status|str|数据包状态<br>`NM` - 普通数据包<br>`SP` - 存储数据包|
|date_time|str|GPS 日期时间值，数据格式：DDMMYYYYHHmmss（日月年时分秒）|
|gps_fix|str|GPS 数据是否有效<br>`V` - 无效<br>`A` - 有效|
|latitude|str|纬度，精确到小数点后 6 位|
|latitude_dir|str|纬度方向，N（北）/ S（南）|
|longitude|str|经度，精确到小数点后 6 位|
|longitude_dir|str|经度方向，E（东）/ W（西）|
|altitude|int|设备的海拔高度（以米为单位）|
|speed|float|车辆速度，精确至小数点后 1 位（公里/小时）|
|distance|int|根据之前的 GPS 数据计算出的距离|
|provider|str|`G` - 来自 GPS 精确定位<br>`N` - 粗略 GPS 或 基站定位数据|
|vehicle_reg_no|str|车辆登记号|
|reply_number|str|需要发送测试响应的手机号码，无则填写 `NA`|

**返回值说明：**

|类型|说明|
|:---|:---|
|bool|`True` - 成功<br>`False` - 失败|

## <span id="packettypes">数据包类型枚举值</span>

### PacketTypes

> 数据包类型枚举值，用于发送定位或报警数据包 `send_loction_alert_information` 接口 `packet_type` 参数。

```python
from usr.ais import PacketTypes

PacketTypes.NormalReport
PacketTypes.EmergencyAlert
...
```

**枚举值说明:**

|枚举值|对应值|说明|
|:---|:---|:---|
|NormalReport|`NR`|正常数据包|
|EmergencyAlert|`EA`|紧急报警包|
|TemperAlert|`TA`|拆卸报警包|
|HealthPacket|`HP`|心跳数据包|
|IgnitionOn|`IN`|点火数据包|
|IgnitionOff|`IF`|熄火数据包|
|VehicleBatteryDisconnected|`BD`|车辆电池断开数据包|
|VehicleBatteryReconnected|`BR`|车辆电池连接数据包|
|InternalBatteryLow|`BL`|内置电池低电报警包|
|HarshBreaking|`HB`|撞击报警包|
|HarshAcceleration|`HA`|急加速报警包|
|RashTurning|`RT`|急转弯报警包|
|SOSEmergencyButtonWireDisconnect|`WD`|SOS 紧急按钮断线报警包|
|OverspeedAlert|`OS`|超速报警包|

## <span id="alertid">报警标识枚举值</span>

### AlertID

> 报警ID枚举值，用于发送定位或报警数据包 `send_loction_alert_information` 接口 `alert_id` 参数。

```python
from usr.ais import AlertID

AlertID.LocationUpdate
AlertID.LocationUpdateHistory
...
```

**枚举值说明:**

|枚举值|对应值|说明|
|:---|:---|:---|
|LocationUpdate|`01`|来自设备的默认消息|
|LocationUpdateHistory|`02`|如果发送消息时 GPRS 不可用|
|Mainsoff|`03`|当设备与车辆电池断开连接时|
|LowBattery|`04`|设备内部电池电量低警报|
|LowBatteryremoved|`05`|设备内部电池正常|
|MainsOn|`06`|设备重新连接至车辆电池|
|IgnitionOn|`07`|车辆点火开|
|IgnitionOff|`08`|车辆点火关|
|TemperAlert|`09`|设备盒打开|
|EmergencyOn|`10`|紧急报警开|
|EmergencyOff|`11`|紧急报警关|
|OTAAlert|`12`|参数变更/查询警报|
|HarshBreaking|`13`|撞击报警|
|HarshAcceleration|`14`|急加速报警|
|RashTurning|`15`|急转弯报警|
|WireDisconnect|`16`|SOS 紧急按钮断线报警|
|Overspeed|`17`|超速报警|
