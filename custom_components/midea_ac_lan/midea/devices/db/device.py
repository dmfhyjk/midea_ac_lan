import logging
from .message import (
    MessageQuery,
    MessagePower,
    MessageStart,
    MessageSet,
    MessageDBResponse,
    water_dict,
    rinsing_dict,
    temp_dict,
    speed_dict,
    detergent_dict,
    softener_dict,
    mode_dict
)
from ...core.device import MiedaDevice
from ...backports.enum import StrEnum

_LOGGER = logging.getLogger(__name__)

class DeviceAttributes(StrEnum):
    power = "power"
    start = "start"
    time_remaining = "time_remaining"
    mode = "mode"
    preset_mode = "preset_mode"
    progress = "progress"
    washing_data = "washing_data"
    water_level = "water_level"
#    washing_level = "washing_level"
#    dehydration_level = "dehydration_level"
    temperature = "temperature"
    washing_time = "washing_time"
    rinsing = "rinsing"
    speed = "speed"
    dehydration_time = "dehydration_time"
    detergent = "detergent"
    softener = "softener"
    nanobubbles = "nanobubbles"
    uv = "uv"
    
class MideaDBDevice(MiedaDevice):

    _water_dict = water_dict
    
    _rinsing_dict = rinsing_dict
    
    _temp_dict = temp_dict
    
    _speed_dict = speed_dict
    
    _detergent_dict = detergent_dict
    
    _softener_dict = softener_dict

    _mode_dict = mode_dict

    _preset_mode_dict = {
	    0x1f: "标准洗",
	    0x17: "30'快洗",
	    0x09: "单脱水",
	    0x0a: "漂脱",
	    0x0b: "大件洗",
	    0x64: "桶自洁",
	    0x1a: "浸泡洗",
}

#    preset_washing_data = {
#
#        "标准洗": bytearray([
#            0xff, 0xff, 0x00, 0x1f, 0x05, 
#            0x20, 0x03, 0x03, 0x00, 0x00, 
#            0x04, 0x01, 0x00, 0x00, 0x00
#        ]),
#        "30'快洗": bytearray([
#            0xff, 0xff, 0x00, 0x17, 0x01, 
#            0x20, 0x03, 0x03, 0x00, 0x00, 
#            0x04, 0x01, 0x00, 0x00, 0x00
#        ]),
#        "单脱水": bytearray([
#            0xff, 0xff, 0x00, 0x09, 0x00, 
#            0x00, 0xff, 0x03, 0x00, 0x03, 
#            0x00, 0x00, 0x00, 0x00, 0x00
#        ]),
#        "漂脱": bytearray([
#            0xff, 0xff, 0x00, 0x0a, 0x01, 
#            0x20, 0xff, 0x00, 0x00, 0x00, 
#            0x00, 0x01, 0x00, 0x00, 0x00
#        ]),
#        "大件洗": bytearray([
#            0xff, 0xff, 0x00, 0x0b, 0x01, 
#            0x20, 0x04, 0x03, 0x00, 0x00, 
#            0x04, 0x01, 0x00, 0x00, 0x00
#        ]),
#        "桶自洁": bytearray([
#            0xff, 0xff, 0x00, 0x64, 0x00, 
#            0x10, 0x06, 0x00, 0x00, 0x00, 
#            0x00, 0x00, 0x00, 0x00, 0x00
#        ]),
#        "浸泡洗": bytearray([
#            0xff, 0xff, 0x00, 0x1a, 0x05, 
#            0x20, 0x02, 0x03, 0x00, 0x00, 
#            0x04, 0x01, 0x00, 0x00, 0x00
#        ])
#
#    }

#    _washing_dict = {
#        0x04: "1档", 
#        0x00: "2档", 
#        0x01: "3档",
#        0x02: "4档",
#        0x03: "5档", 
#        
#    }
#
#    _dehydration_dict = {
#        0x03: "1档", 
#        0x04: "2档",
#        0x00: "3档",
#        0x01: "4档", 
#        0x02: "5档", 
#    }
    
    def __init__(
            self,
            name: str,
            device_id: int,
            ip_address: str,
            port: int,
            token: str,
            key: str,
            protocol: int,
            model: str,
            customize: str
    ):
        super().__init__(
            name=name,
            device_id=device_id,
            device_type=0xDB,
            ip_address=ip_address,
            port=port,
            token=token,
            key=key,
            protocol=protocol,
            model=model
        )
        self._attributes = {
            DeviceAttributes.power: False,
            DeviceAttributes.start: False,
            DeviceAttributes.washing_data: bytearray([]),
            DeviceAttributes.mode: 0x1f,
            DeviceAttributes.progress: "Unknown",
            DeviceAttributes.time_remaining: None,
            DeviceAttributes.water_level: "自动",
            DeviceAttributes.preset_mode: "30'快洗",
#            DeviceAttributes.washing_level: "2档",
#            DeviceAttributes.dehydration_level: "3档",
            DeviceAttributes.temperature: "None",
            DeviceAttributes.washing_time: "None",
            DeviceAttributes.dehydration_time: "None",
            DeviceAttributes.rinsing: "None",
            DeviceAttributes.speed: "800",
            DeviceAttributes.dehydration_time: "None",
            DeviceAttributes.detergent: "自动",
            DeviceAttributes.softener: "自动",
            DeviceAttributes.nanobubbles: True,
            DeviceAttributes.uv: True,
        }
        
#    @property
#    def water_level_sets(self):
#        return list(MideaDBDevice._water_dict.values())
#
#    @property
#    def washing_level_sets(self):
#        return list(MideaDBDevice._washing_dict.values())
#
#    @property
#    def dehydration_level_sets(self):
#        return list(MideaDBDevice._dehydration_dict.values())

    @property
    def preset_mode_sets(self):
        return list(MideaDBDevice._preset_mode_dict.values())

    def build_query(self):
        return [MessageQuery(self._device_protocol_version)]

    def process_message(self, msg):
        message = MessageDBResponse(msg)
        _LOGGER.debug(f"[{self.device_id}] Received: {message}")
        new_status = {}
        progress = ["待机", "脱水", "漂洗", "洗涤", "预洗",
                    "干燥", "称重", "高速脱水", "未知"]
        for status in self._attributes.keys():
            if hasattr(message, status.value):
                if status == DeviceAttributes.progress:
                    self._attributes[status] = progress[getattr(message, status.value)]
                else:
                    self._attributes[status] = getattr(message, status.value)
                new_status[status.value] = self._attributes[status]
        
        return new_status

    def make_message_set(self):
        message = MessageSet(self._device_protocol_version)

#        message.mode = 0x17 if self._attributes[DeviceAttributes.mode] is None else \
#            list(MideaDBDevice._mode_dict.keys())[list(MideaDBDevice._mode_dict.values()).index(
#                self._attributes[DeviceAttributes.mode]
#            )]
        # message.mode = 0x02

        # message.temperature = self._attributes[DeviceAttributes.temperature]
              # 温度
        # message.rinsing = self._attributes[DeviceAttributes.rinsing]
                # 漂洗次数
        # message.speed = self._attributes[DeviceAttributes.speed]
                    # 脱水转速挡位
        # message.detergent = self._attributes[DeviceAttributes.detergent]
             # 洗涤剂
        # message.softener = self._attributes[DeviceAttributes.softener]
                # 柔顺剂
#        message.water_level = 0x05 if self._attributes[DeviceAttributes.water_level] is None else \
#            list(MideaDBDevice._water_dict.keys())[list(MideaDBDevice._water_dict.values()).index(
#                self._attributes[DeviceAttributes.water_level]
#            )]
    
        # message.washing_level = self._attributes[DeviceAttributes.washing_level]
            # 洗涤挡位
        # message.dehydration_level = self._attributes[DeviceAttributes.dehydration_level]
        # 脱水挡位

#        _LOGGER.debug(f"[{self.device_id}] build message: {message}")

        return message

    def set_attribute(self, attr, value):
        if attr == DeviceAttributes.power:
            message = MessagePower(self._device_protocol_version)
            message.power = value
            self.build_send(message)
        elif attr == DeviceAttributes.start:
            message = MessageStart(self._device_protocol_version)
            message.start = value
            message.washing_data = self._attributes[DeviceAttributes.washing_data]
            self.build_send(message)

        elif attr == DeviceAttributes.preset_mode:
            message = MessageSet(self._device_protocol_version, preset_mode=value)
#            message = self.make_message_set()
#            message.washing_data = self.preset_washing_data[value]
            _LOGGER.debug(f"[{self.device_id}] value: {value} build message: {message}")

#            if attr == DeviceAttributes.preset_mode:
#                pass
#                if value in MideaDBDevice._water_dict.values():
#                    message.water_level = list(MideaDBDevice._water_dict.keys())[
#                        list(MideaDBDevice._water_dict.values()).index(value)
#                    ]
#            if attr == DeviceAttributes.washing_level:
#                if value in MideaDBDevice._washing_dict.values():
#                    message.washing_level = list(MideaDBDevice._washing_dict.keys())[
#                        list(MideaDBDevice._washing_dict.values()).index(value)
#                    ]
#            if attr == DeviceAttributes.dehydration_level:
#                if value in MideaDBDevice._dehydration_dict.values():
#                    message.dehydration_level = list(MideaDBDevice._dehydration_dict.keys())[
#                        list(MideaDBDevice._dehydration_dict.values()).index(value)
#                    ]
            self.build_send(message)

class MideaAppliance(MideaDBDevice):
    pass
