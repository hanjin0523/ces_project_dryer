from dataclasses import dataclass, asdict
import json
import struct

def str_conversion(packet):
    result = ''
    for byte in packet:
        result += str(byte)
    return result

@dataclass
class Base_packet:
    sender: int
    size: int
    p_type: int
    cmd_type: int
    device_id: int
    
    @classmethod
    def base_packet(cls, packet: bytes, str_conversion: callable):
        sender = packet[0]
        size = packet[1]
        p_type = packet[2]
        cmd_type = packet[3]
        device_id = str_conversion(packet[4:10])
        return cls(sender, size, p_type, cmd_type, device_id)
    
    def to_json(self):
        return json.dumps(asdict(self), ensure_ascii=False)

@dataclass
class senser_data(Base_packet):
    max_packet: int
    current_packet: int
    operation: int
    sign: int
    taget_temp: int
    taget_hum: int
    blowing: int
    exhaust: int
    etx: bytes = b'\x0D\x0A'
    
    @classmethod
    def senser_data_response(cls, packet: bytes):
        base_packet = Base_packet.base_packet(packet[0:10], str_conversion)
        max_packet = packet[10]
        current_packet = packet[11]
        operation = packet[12]
        sign = packet[13]
        taget_temp = struct.unpack("H", packet[14:16])
        taget_hum = struct.unpack("H", packet[16:18])
        blowing = packet[18]
        exhaust = packet[19]
        etx	= packet[20:21]
        return cls(base_packet.sender, 
                    base_packet.size,
                    base_packet.p_type,
                    base_packet.cmd_type,
                    base_packet.device_id ,
                    max_packet,
                    current_packet,
                    operation,
                    sign,
                    taget_temp,
                    taget_hum,
                    blowing,
                    exhaust,
                    etx)
    
    def to_json(self):
        data_dict = asdict(self)
        data_dict["etx"] = self.etx.decode()  # Decode the bytes to a string
        return json.dumps(data_dict, ensure_ascii=False)

@dataclass
class dryer_status(Base_packet):

    max_packet: int
    current_packet: int
    op_state: int
    heater: int
    blower: int
    exhaust: int
    hour: int
    minute: int
    second: int
    etx: bytes = b'\x0D\x0A'

    @classmethod
    def dryer_status_response(cls, packet: bytes):
        base_packet = Base_packet.base_packet(packet[0:10], str_conversion)
        max_packet = packet[10]
        current_packet = packet[11]
        op_state = packet[12]
        heater = packet[13]
        blower = packet[14]
        exhaust = packet[15]
        hour = packet[16]
        minute = packet[17]
        second = packet[18]
        etx	= packet[19:20]
        return cls(base_packet.sender, 
                    base_packet.size,
                    base_packet.p_type,
                    base_packet.cmd_type,
                    base_packet.device_id ,
                    max_packet,
                    current_packet,
                    op_state,
                    heater,
                    blower,
                    exhaust,
                    hour,
                    minute,
                    second,
                    etx)
    
    def to_json(self):
        data_dict = asdict(self)
        data_dict["etx"] = self.etx.decode()  # Decode the bytes to a string
        return json.dumps(data_dict, ensure_ascii=False)