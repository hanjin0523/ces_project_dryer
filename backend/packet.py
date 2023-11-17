from dataclasses import dataclass

@dataclass
class Base_packet:
    sender: int
    size: int
    p_type: int
    cmd_type: int

    # def base_packet(self):
        
    #     packet = sender_bytes + size_bytes + p_type_bytes + res_type_bytes
    #     return packet

@dataclass
class Id_reponse_packet(Base_packet):
    device_id: int
    result: int
    etx: bytes = b'\x0D\x0A'

    def create_packet(self):
        sender_bytes = bytes([self.sender])
        size_bytes = bytes([self.size])
        p_type_bytes = bytes([self.p_type])
        res_type_bytes = bytes([self.cmd_type])
        device_id_bytes = self.device_id
        result_bytes = bytes([self.result])
        etx_bytes = self.etx
        packet = sender_bytes + size_bytes + p_type_bytes + res_type_bytes + device_id_bytes + result_bytes + etx_bytes
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
        sender_bytes = bytes([self.sender])
        size_bytes = bytes([self.size])
        p_type_bytes = bytes([self.p_type])
        res_type_bytes = bytes([self.cmd_type])
        device_id_bytes = self.device_id
        max_packet_bytes = bytes([self.max_packet])
        current_packet_bytes = bytes([self.current_packet])
        result_bytes = bytes([self.result])
        etx_bytes = bytes(self.etx)
        packet = sender_bytes + size_bytes + p_type_bytes + res_type_bytes + device_id_bytes + max_packet_bytes + current_packet_bytes + result_bytes + etx_bytes
        print(packet,"Default_packet!!!")
        return packet

@dataclass
class Default_packet1(Base_packet):##세션응답, 센서정보요청, 에러체크, 동작정지, 일지정지,

    device_id: int
    max_packet: int
    current_packet: int
    result: int
    etx: bytes = b'\x0D\x0A'

    def create_packet(self):
        sender_bytes = bytes([self.sender])
        size_bytes = bytes([self.size])
        p_type_bytes = bytes([self.p_type])
        res_type_bytes = bytes([self.cmd_type])
        device_id_bytes = self.device_id
        max_packet_bytes = bytes([self.max_packet])
        current_packet_bytes = bytes([self.current_packet])
        result_bytes = bytes([self.result])
        etx_bytes = bytes(self.etx)
        packet = sender_bytes + size_bytes + p_type_bytes + res_type_bytes + device_id_bytes + max_packet_bytes + current_packet_bytes + result_bytes + etx_bytes
        print(packet,"session_response패킷생성!!!")
        return packet


