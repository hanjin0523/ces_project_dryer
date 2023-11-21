from dataclasses import dataclass

@dataclass
class Base_packet:
    sender: int
    size: int
    p_type: int
    cmd_type: int

    def base_packet(self):
        sender_bytes = bytes([self.sender])
        size_bytes = bytes([self.size])
        p_type_bytes = bytes([self.p_type])
        res_type_bytes = bytes([self.cmd_type])
        packet = sender_bytes + size_bytes + p_type_bytes + res_type_bytes
        return packet

@dataclass
class Id_reponse_packet(Base_packet):
    device_id: int
    result: int
    etx: bytes = b'\x0D\x0A'

    def create_packet(self):
        base_packet = super().base_packet()
        device_id_bytes = self.device_id
        result_bytes = bytes([self.result])
        etx_bytes = self.etx
        packet = base_packet + device_id_bytes + result_bytes + etx_bytes
        print(packet,"id응답패킷생성!!!")
        return packet

@dataclass
class Default_packet(Base_packet):##세션응답, 센서정보요청, 에러체크, 동작정지, 일지정지,

    device_id: int
    max_packet: int
    current_packet: int
    result: int
    etx: bytes = b'\x0D\x0A'

    def create_packet(self):
        base_packet = super().base_packet()
        device_id_bytes = self.device_id
        max_packet_bytes = bytes([self.max_packet])
        current_packet_bytes = bytes([self.current_packet])
        result_bytes = bytes([self.result])
        etx_bytes = bytes(self.etx)
        packet = base_packet + device_id_bytes + max_packet_bytes + current_packet_bytes + result_bytes + etx_bytes
        print(packet,"Default_packet!!!")
        return packet

@dataclass
class Drying_stage_packet(Base_packet):
    device_id: int
    option: int
    crop_type: int
    max_stage: int
    state_cnt: int
    hour: int
    minute: int
    second: int
    taget_temp: int
    taget_hum: int
    blowing: int
    exhaust: int
    etx: bytes = b'\x0D\x0A'

    def create_packet(self):
        base_packet = super().base_packet()
        device_id_bytes = self.device_id
        option_bytes = bytes([self.option])
        crop_type_bytes = bytes([0, self.crop_type])
        max_stage_bytes = bytes([0, self.max_stage])
        state_cnt_bytes = bytes([0, self.state_cnt])
        hour_bytes = bytes([self.hour])
        minute_bytes = bytes([self.minute])
        second_bytes = bytes([self.second])
        taget_temp_bytes = bytes([self.taget_temp, 0])
        taget_hum_bytes = bytes([self.taget_hum, 0])
        blowing_bytes = bytes([self.blowing])
        exhaust_bytes = bytes([self.exhaust])
        etx_bytes = bytes(self.etx)
        packet = base_packet + device_id_bytes + option_bytes + crop_type_bytes + max_stage_bytes + state_cnt_bytes + hour_bytes + minute_bytes + second_bytes + taget_temp_bytes + taget_hum_bytes + blowing_bytes + exhaust_bytes + etx_bytes
        print(packet,"Drying_stage_packet!!!")
        return packet