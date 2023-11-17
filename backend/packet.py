from dataclasses import dataclass

@dataclass
class default_packet:
    sender: int
    size: int
    p_type: int
    cmd_type: int
    device_id: int
    max_packet: int
    current_packet: int
    result: int
    etx: bytes = b'\x0D\x0A'

    def create_packet(self):
        self.sender = bytes([self.sender])
        self.size = bytes([self.size])
        self.p_type = bytes([self.p_type])
        self.cmd_type = bytes([self.cmd_type])
        self.device_id = bytes(self.device_id)
        self.max_packet = bytes([self.max_packet])
        self.current_packet = bytes([self.current_packet])
        self.result = bytes([self.result])
        self.etx = bytes(self.etx)
        packet = self.sender + self.size + self.p_type + self.cmd_type + self.device_id + self.max_packet + self.current_packet + self.result + self.etx
        return packet

data = default_packet(0, 15, 2, 2, [23,10,23,0,0,1], 1, 1, 0)
print(data.create_packet())