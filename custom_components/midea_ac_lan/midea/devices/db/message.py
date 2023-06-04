from ...core.message import (
    MessageType,
    MessageRequest,
    MessageResponse,
    MessageBody,
)

water_dict = {
    
    0x01: "1",
    0x02: "2",
    0x03: "3",
    0x04: "4",
    0x05: "自动",
}

rinsing_dict = {
    
    0x00: "0",
    0x10: "1",
    0x20: "2",
    0x30: "3",
    0x40: "4",
}

temp_dict = {
    0x01: "冷水",
    0x02: "20", 
    0x03: "30", 
    0x04: "40", 
    0x05: "50", 
    0x06: "60", 
    0x07: "70", 
    0xff: None, 
}

speed_dict = {
    0x00: "None", 
    0x01: "400",
    0x02: "600",
    0x03: "800", 
    0x04: "1000", 
    0x05: "1200", 
}

detergent_dict = {
    0x00: "None", 
    0x01: "1",
    0x02: "2",
    0x03: "3", 
    0x04: "自动", 
    0x05: "4", 
}

softener_dict = {
    0x00: "None", 
    0x01: "自动",
    0x02: "1",
    0x03: "2", 
    0x04: "3", 
    0x05: "4", 
}

#washing_dict = {
#   0x04: "1档", 
#   0x00: "2档", 
#   0x01: "3档",
#   0x02: "4档",
#   0x03: "5档", 
#   
#}
#
#dehydration_dict = {
#   0x03: "1档", 
#   0x04: "2档",
#   0x00: "3档",
#   0x01: "4档", 
#   0x02: "5档", 
#}

mode_dict = {
    0x1f: "标准洗",
    0x17: "30'快洗",
    0x09: "单脱水",
    0x0a: "漂脱",
    0x0b: "大件洗",
    0x64: "桶自洁",
    0x1a: "浸泡洗",
    0x05: "羊毛洗",
    0x63: "除螨洗",
    0x02: "15'快洗",
    0xff: "未知"
}

preset_washing_data = {

   "标准洗": bytearray([
       0xff, 0xff, 0x00, 0x1f, 0x05, 
       0x20, 0x03, 0x03, 0x00, 0x00, 
       0x04, 0x01, 0x00, 0x00, 0x00
   ]),
   "30'快洗": bytearray([
       0xff, 0xff, 0x00, 0x17, 0x01, 
       0x20, 0x03, 0x03, 0x00, 0x00, 
       0x04, 0x01, 0x00, 0x00, 0x00
   ]),
   "单脱水": bytearray([
       0xff, 0xff, 0x00, 0x09, 0x00, 
       0x00, 0xff, 0x03, 0x00, 0x03, 
       0x00, 0x00, 0x00, 0x00, 0x00
   ]),
   "漂脱": bytearray([
       0xff, 0xff, 0x00, 0x0a, 0x01, 
       0x20, 0xff, 0x00, 0x00, 0x00, 
       0x00, 0x01, 0x00, 0x00, 0x00
   ]),
   "大件洗": bytearray([
       0xff, 0xff, 0x00, 0x0b, 0x01, 
       0x20, 0x04, 0x03, 0x00, 0x00, 
       0x04, 0x01, 0x00, 0x00, 0x00
   ]),
   "桶自洁": bytearray([
       0xff, 0xff, 0x00, 0x64, 0x00, 
       0x10, 0x06, 0x00, 0x00, 0x00, 
       0x00, 0x00, 0x00, 0x00, 0x00
   ]),
   "浸泡洗": bytearray([
       0xff, 0xff, 0x00, 0x1a, 0x05, 
       0x20, 0x02, 0x03, 0x00, 0x00, 
       0x04, 0x01, 0x00, 0x00, 0x00
   ])

}

class MessageDBBase(MessageRequest):
    def __init__(self, device_protocol_version, message_type, body_type):
        super().__init__(
            device_protocol_version=device_protocol_version,
            device_type=0xDB,
            message_type=message_type,
            body_type=body_type
        )

    @property
    def _body(self):
        raise NotImplementedError


class MessageQuery(MessageDBBase):
    def __init__(self, device_protocol_version):
        super().__init__(
            device_protocol_version=device_protocol_version,
            message_type=MessageType.query,
            body_type=0x03)

    @property
    def _body(self):
        return bytearray([])


class MessagePower(MessageDBBase):
    def __init__(self, device_protocol_version):
        super().__init__(
            device_protocol_version=device_protocol_version,
            message_type=MessageType.set,
            body_type=0x02)
        self.power = False

    @property
    def _body(self):
        power = 0x01 if self.power else 0x00
        return bytearray([
            power,
            # 0x00, 0x00, 0x17,
            # 0x01, 0x20, 0x01, 0x03,
            # 0x00, 0x00, 0x04, 0x01,
            # 0x00, 0x00, 0x00
            0xff, 0xff, 0xff, 0xff,
            0xff, 0xff, 0xff, 0xff,
            0xff, 0xff, 0xff, 0xff,
            0xff, 0xff, 0xff, 0xff,
            0xff, 0xff, 0xff, 0xff
        ])

class MessageSet(MessageDBBase):
    def __init__(self, device_protocol_version, preset_mode="30'快洗"):
        super().__init__(
            device_protocol_version=device_protocol_version,
            message_type=MessageType.set,
            body_type=0x02)

#        self.mode = 0x17
#        self.water_level = 0x40            # 水量
#        self.temperature = 0x01              # 温度
#        self.rinsing = 0x20                # 漂洗次数
#        self.speed = 0x03                    # 脱水转速挡位
#        self.detergent = 0x04             # 洗涤剂
#        self.softener = 0x01                # 柔顺剂
#        self.water_level = 0x05            # 水量挡位
#        self.washing_level = 0x00            # 洗涤挡位
#        self.dehydration_level = 0x00        # 脱水挡位
        self.preset_mode = preset_mode        # 脱水挡位

    @property
    def _body(self):
        # byte2 mode
#        mode = self.mode if self.mode else 0x17
#
#        water_level = self.water_level if self.water_level else 0x40
#        washing_level = self.washing_level if self.washing_level else 0x00
#        dehydration_level = self.dehydration_level if self.dehydration_level else 0x00
#        temperature = self.temperature if self.temperature else 0x01
#        rinsing = self.rinsing if self.rinsing else 0x02
#        speed = self.speed if self.speed else 0x03
#        detergent = self.detergent if self.detergent else 0x04
#        softener = self.softener if self.softener else 0x01
#        return bytearray([
#            0xff,            # 电源
#            0xff,            # 运行状态
#            0x00,            # 空
#            mode,             # 洗涤模式
#            water_level,     # 水量
#            rinsing,         # 漂洗次数
#            temperature,     # 洗涤温度
#            speed,             # 脱水转速
#            washing_level,         # 洗涤等级
#            dehydration_level,     # 脱水等级
#            detergent,             # 洗涤剂
#            softener,            # 柔顺剂
#            0x00, 0x00, 0x00
#        ])
        return preset_washing_data[self.preset_mode]

class MessageStart(MessageDBBase):
    def __init__(self, device_protocol_version):
        super().__init__(
            device_protocol_version=device_protocol_version,
            message_type=MessageType.set,
            body_type=0x02)
        self.start = False
        self.washing_data = bytearray([])

    @property
    def _body(self):
        if self.start: # Pause
            return bytearray([
                0xFF, 0x01,
            # ]) + self.washing_data

                0x00, 0x17, 0x01, 0x20, 
                0x03, 0x03, 0x00, 0x00, 
                0x04, 0x01, 0x00, 0x00, 
                0x00
            ])
        else:
            # Pause
            return bytearray([
                0xFF, 0x00
            ])


class DBGeneralMessageBody(MessageBody):
    def __init__(self, body):
        super().__init__(body)
        self.power = body[1] > 0                                                                   # 电源
        self.start = True if body[2] in [2, 6] else False                                          # 运行状态
        self.washing_data = body[3:16]
              
        self.mode = mode_dict[body[4]] if body[4] in mode_dict.keys() else None                     # 洗涤模式
        self.preset_mode = mode_dict[body[4]] if body[4] in mode_dict.keys() else None
        self.water_level = water_dict[body[5]] if body[5] in water_dict.keys() else None            # 水量
        self.temperature = temp_dict[body[7]] if body[7] in temp_dict.keys() else None              # 温度
        self.washing_time = body[27] if self.power else None                                        # 洗涤时间
        self.rinsing = rinsing_dict[body[6]] if body[6] in rinsing_dict.keys() else None            # 漂洗次数
        self.speed = speed_dict[body[8]] if body[8] in speed_dict.keys() else None                    # 脱水转速挡位
#        self.washing_level = washing_dict[body[9]] if body[9] in washing_dict.keys() else None                # 洗涤时长等级
#        self.dehydration_level = dehydration_dict[body[10]] if body[10] in dehydration_dict.keys() else None                # 脱水时长等级
        self.washing_level = body[9]                # 洗涤时长等级
        self.dehydration_level = body[10]                # 脱水时长等级
        self.dehydration_time = body[28] if self.power else None                                   # 脱水时间
        self.detergent = detergent_dict[body[11]] if body[11] in detergent_dict.keys() else None     # 洗涤剂
        self.softener = softener_dict[body[12]] if body[12] in softener_dict.keys() else None        # 柔顺剂
        self.nanobubbles = True if (body[29] & 0x20) else False                      # 超微净泡
        self.uv = True if (body[29] & 0x08) else False                             # uv除菌
        self.time_remaining = (body[17] + (body[18] << 8)) if self.power else None     # 剩余时间

        self.progress = 0
        for i in range(0, 7):            # 当前步骤
            if (body[16] & (1 << i)) > 0:
                self.progress = i + 1
                break
        # if self.power:
        #     self.time_remaining = body[17] + (body[18] << 8)    # 剩余时间
        # else:
        #     self.time_remaining = None


class MessageDBResponse(MessageResponse):
    def __init__(self, message):
        super().__init__(message)
        body = message[self.HEADER_LENGTH: -1]
        if self._message_type in [MessageType.query, MessageType.set] or \
                (self._message_type == MessageType.notify1 and self._body_type == 0x04):
            self._body = DBGeneralMessageBody(body)
        self.set_attr()
