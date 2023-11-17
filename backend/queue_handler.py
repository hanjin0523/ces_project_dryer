
import struct
###test
packet = b'\x00\x0f\x02\x02\x17\n\x17\x00\x00\x01\x01\x01\x00\r\n'

# def id_packet(packet):
#         start_index = packet.find(b'\x17\n')
#         end_index = start_index + 6
#         extracted_packet = packet[start_index:end_index]
#         test_id = struct.unpack('!6B',extracted_packet)
#         result = list(test_id)
#         print(result,"아이디패킷!!!!")
#         return result

# id_packet(packet)