import socket
import threading
import queue
import struct
import main
from dataclasses import dataclass 
import time
import binascii

class Socket_test:

    def __init__(self, host:str, port:int):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.accept_thread = threading.Thread(target=self.accept_clients)
        self.accept_thread.start()
        self.my_queue = queue.Queue()
        self.clients = []
        self.clients_id = []
        self.device_id = ''
        self.socket_lock = threading.Lock() 
        self.temp_hum_data = []

    def accept_clients(self):
        while True:
            client_socket = None
            try:
                client_socket, client_addr = self.server_socket.accept()
                client_thread = threading.Thread(target=self.client_handler, args=(client_socket,client_addr))
                client_thread.setDaemon(True)
                client_thread.start()
                print("connected by", client_addr)
            except KeyboardInterrupt:
                if client_socket:  
                    client_socket.close()
                break
            except Exception as e:
                print("accept error",e)

    def client_handler(self, client_socket, client_addr):
        while True:
            try:
                recv = client_socket.recv(1024)
                if not recv:
                    break
                elif len(recv) == 22:
                    self.temp_hum_data = []
                    self.temp_hum_data.append(recv)
                if recv:
                    self.received_data_handler(recv, client_socket, client_addr)
                    self.my_queue.put(recv)
                else:
                    pass
            except Exception as e:
                print("client handler error", e)
                break

    def received_data_handler(self, received_data, client_socket, client_addr):
        make_id_packet = self.id_packet(received_data)
        self.device_id = make_id_packet
        str_device_id = self.str_conversion(make_id_packet)
        if str_device_id not in self.clients_id:
            self.clients_id.append(str_device_id)
            self.clients.append((client_socket,client_addr))
        else:
            pass
        conversion_length = (received_data[1]*"B")
        unpacked_data = struct.unpack(conversion_length, received_data)
        response_type = unpacked_data[3]
        main.dryer_set_device_id = str_device_id
        main.dry_accept.get_dryer_controller(str_device_id)
        if response_type == 5:
            client_socket.send(self.serial_id_response(make_id_packet, 1))
            return True
        elif response_type == 2:
            client_socket.send(self.session_response(make_id_packet))
            return True
        return True
    
    def senser(self, select_num: int, dryer_set_device_id: str):
        try:##센서데이터 수정해야되!!!
            senser_socket = self.clients[select_num][0]
            # senser_socket.settimeout(15)
            with self.socket_lock:  # Acquire the lock before accessing the socket
                senser_socket.send(self.senser_data_request())
                try:
                    re = self.temp_hum_data[0]
                    result = self.senser_data_response(re)
                    temp = round((int(result["taget_temp"][0])/100),1)
                    hum = round((int(result["taget_hum"][0])/100),1)
                    return [temp,hum]
                except Exception as e:
                    print("온도습도파씽에러", str(e))  
        except TimeoutError as e:
            pass
            # self.clients.pop(select_num)
            # self.clients_id.pop(select_num)

    def power_on_off(self, dryer_set_number:int, operating_conditions):
        with self.socket_lock:
            power_socket,_ = self.clients[dryer_set_number]
            total_stage = sum(stage[2] for stage in operating_conditions)
            def convert_seconds_to_time(seconds):
                hours = seconds // 3600
                minutes = (seconds % 3600) // 60
                seconds = seconds % 60
                return hours, minutes, seconds
            count = -1
            for item in operating_conditions:
                time.sleep(0.1)
                count += item[2]
                hours, minutes, seconds = convert_seconds_to_time(item[3])
                set_temp, set_hum = item[4], item[5]
                power_socket.send(self.건조레시피명령(total_stage, count, hours, minutes, seconds, set_temp, set_hum))

    def id_packet(self, packet):
        start_index = packet.find(b'\x17\n')
        end_index = start_index + 6
        extracted_packet = packet[start_index:end_index]
        return extracted_packet

    def str_conversion(self, packet):
        result = ''
        for byte in packet:
            result += str(byte)
        return result
    
    def int_conversion(self, packet):
        result = 0
        for byte in packet:
            result = result * 256 + byte
        return result

    def serial_id_response(self, id_packet, result_num: int):
        packet = b'\x00'  # sender
        packet += b'\x0d'  # size
        packet += b'\x01'  # p type
        packet += b'\x01'  # resp type
        packet += id_packet  # device id (6 bytes)
        packet += b'\x01'  # result
        packet += b'\x0D\x0A'  # etx
        print(packet,"시리얼ID응답리턴패킷...!!!")
        return packet

    def 건조레시피명령(self, max_stage, state_count, hour, minute, second, temp, hum):#매개변수(ID,Crop, Max, State, H, M, S, Temp, Hum, Blow, Exhaust)
        packet = b'\x00'          # Sender (1바이트) 헤더고정
        packet += b'\x1c'         # Size (1바이트) 헤더고정
        packet += b'\x00'       # P Type (1바이트) 헤더고정
        packet += b'\x03'       # Cmd Type (1바이트) 헤더고정
        packet += b'\x17\x0a\x17\x00\x00\x01'      # Device ID (6바이트) 가변..
        packet += b'\x00'          # Option (1바이트)
        packet += b'\x00\x0e'        # Crop Type (2바이트) 가변..
        packet += bytes([0,max_stage])      # Max Stage (2바이트) 가변..
        packet += bytes([0,state_count]) # State Count (2바이트) 가변..  0///1
        packet += bytes([hour])           # H (1바이트) 가변..
        packet += bytes([minute])          # M (1바이트) 가변..
        packet += bytes([second])          # S (1바이트) 가변..
        packet += bytes([temp,0])      # Target Temperature (2바이트)가변..
        packet += bytes([hum,0])   # Target Relative Humidity (2바이트)가변..
        packet += b'\x01'          # Blowing (1바이트)
        packet += b'\x01'          # Exhaust (1바이트)
        packet += b'\x0d\x0a'     # ETX (2바이트)
        # packet = bytes.fromhex(hex_string)
        print(packet,"건조레시피명령-----")
        return packet

    def session_response(self,id_packet):
        packet = b'\x00'
        packet += b'\x0F'
        packet += b'\x01'
        packet += b'\x02'
        packet += b'\x17\x0a\x17\x00\x00\x01'
        packet += b'\x01'  # max packet
        packet += b'\x01'  # current packet
        packet += b'\x00'  # result
        packet += b'\x0D\x0A'  # etx
        print(packet,"세션연결확인응답리턴패킷...!!!")
        return packet

    def 재시작요청(self,):
        packet = b'\x00'
        packet += b'\x0F'
        packet += b'\x00'
        packet += b'\x08'
        packet += b'\x17\x0a\x17\x00\x00\x01'
        packet += b'\x01'
        packet += b'\x01'
        packet += b'\x00'
        packet += b'\x0D\x0A'
        print(packet,"일시정지패킷날리기!!!")
        return packet
    
    def 일시정지요청(self,):
        packet = b'\x00'
        packet += b'\x0F'
        packet += b'\x00'
        packet += b'\x07'
        packet += b'\x17\x0a\x17\x00\x00\x01'
        packet += b'\x01'
        packet += b'\x01'
        packet += b'\x00'
        packet += b'\x0D\x0A'
        print(packet,"일시정지패킷날리기!!!")
        return packet

    def senser_data_request(self):
        # 패킷 데이터 생성
        packet = b'\x00'  # sender
        packet += b'\x0F'  # size
        packet += b'\x02'  # p type
        packet += b'\x00'  # cmd type
        packet += b'\x17\x0a\x17\x00\x00\x01'  # device id (6 bytes)
        packet += b'\x01'  # max packet
        packet += b'\x01'  # current packet
        packet += b'\x00'  # result
        packet += b'\x0D\x0A'  # etx
        print(packet,"senser값요청!!!!---")
        return packet
    
    def senser_data_response(self, packet):
        sender = packet[0]  # Sender (1바이트)
        size = packet[1]  # Size (1바이트)
        p_type = packet[2]  # P Type (1바이트)
        cmd_type = packet[3]  # Cmd Type (1바이트)
        device_id = self.str_conversion(packet[4:10])  # Device ID (6바이트)
        max_packet = packet[10]
        current_packet = packet[11]
        operation = packet[12]
        sign = packet[13]
        taget_temp = struct.unpack("H", packet[14:16])
        taget_hum = struct.unpack("H", packet[16:18])
        blowing = packet[18]
        exhaust = packet[19]
        etx	= packet[20:21]
        
        return {
            "sender" : sender,
            "size" : size,
            "p_type" : p_type,
            "cmd_type" : cmd_type,
            "device_id" : device_id,
            "max_packet" : max_packet,
            "current_packet" : current_packet,
            "operation" : operation,
            "sign" : sign,
            "taget_temp" : taget_temp,
            "taget_hum" : taget_hum,
            "blowing" : blowing,
            "exhaust" : exhaust,
            "etx" : etx
        }