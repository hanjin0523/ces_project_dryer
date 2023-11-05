import socket
import threading
import dataBaseMaria
import struct
import main
import select
import time
import asyncio
import queue

mariadb = dataBaseMaria.DatabaseMaria('211.230.166.113', 3306, 'jang', 'jang','cesdatabase','utf8')

class Socket_test:
    _instance = None  # 클래스 변수로 인스턴스를 저장

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, host: str, port: int):
        if not hasattr(self, 'initialized'):
            self.host = host
            self.port = port
            self.clients = []
            self.clients_id = []
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            self.accept_thread = threading.Thread(target=self.accept_clients)
            self.accept_thread.start()
            self.initialized = True
            self.is_connected = False
            self.device_id = ''
            self.message_queue = queue.Queue()
            self.last_received_data = time.time()
            self.socket_lock = threading.Lock()

    def client_handler(self, client_socket):
        while True:
            try:
                client_socket.settimeout(10)  # Set a timeout for socket operations
                received_data = client_socket.recv(100)
                if not received_data:
                    client_socket.close()  # Close the socket
                    break  # Exit the loop
                self.message_queue.put(received_data)
                result = self.message_queue.get()
                print(result, "---큐에서 가져오는 데이타")
                self.received_data_handler(received_data, client_socket)
            except socket.timeout:
                print("No data received within the timeout")
                client_socket.close()  # Close the socket
                break  # Exit the loop
        
    

    def accept_clients(self):
        while True: 
            try:
                client_socket, client_addr = self.server_socket.accept()
                print(client_addr,"client_addr---접속됨..")
                client_thread = threading.Thread(target=self.client_handler, args=(client_socket,))
                client_thread.daemon = True
                client_thread.start()
            except Exception as e:
                print(str(e))

    
    def senser(self, select_num: int):
        try:##센서데이터 수정해야되!!!
            print(self.clients,"-----clients-----")
            print(self.clients_id,"-----senser-----")
            senser_socket = self.clients[select_num]
            # with self.socket_lock:  # Acquire the lock before sending data
            senser_socket.send(self.에러체크요청())
            # print(re,"11")
            return [11,70]
        except BrokenPipeError as e:
            print(str(e),"error")
            senser_socket = self.clients.pop(select_num)
            del self.clients_id[select_num]
            return False

        
    def power_on_off(self, dryer_set_number:int, operating_conditions):
        print(operating_conditions,"operating_conditions----")
        power_socket,_ = self.clients[dryer_set_number]
        test = self.handler_request("건조레시피명령", power_socket)
        print("건조기동작됨!!", test)

    def received_data_handler(self, received_data, client_socket):
        make_id_packet = self.id_packet(received_data)
        self.device_id = make_id_packet
        str_device_id = self.str_conversion(make_id_packet)
        if str_device_id not in self.clients_id:
            self.clients_id.append(str_device_id)
            self.clients.append((client_socket))
        else:
            pass
        conversion_length = (received_data[1]*"B")
        unpacked_data = struct.unpack(conversion_length, received_data)
        response_type = unpacked_data[3]
        main.dryer_set_device_id = str_device_id
        main.dry_accept.get_dryer_controller(str_device_id)
        if response_type == 2:
            client_socket.send(self.session_response(make_id_packet))
            return True
        elif response_type == 5:
            client_socket.send(self.serial_id_response(make_id_packet, 1))
            return True
        return True
    
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

    def handler_response(self, command):
        try:
            conversion_length = (command[1]*"B")
            unpacked_data = struct.unpack(conversion_length, command)
            packet_size = command[1]
            response_type = command[3]
            if packet_size == 28:
                result = self.건조레시피응답패킷(unpacked_data)
                return result
            elif packet_size == 22:
                result = self.senser_data_response(unpacked_data)
                temp = result["taget_temp"]
                hum = result["taget_hum"]
                temp_hum_data = []
                temp_hum_data.append(temp)
                temp_hum_data.append(hum)
                return temp_hum_data
            elif packet_size == 15:
                if response_type == 1:
                    result = self.dryer_id_response(unpacked_data)
                    return result
                elif response_type == 2:
                    result = self.세션연결정보받음(unpacked_data)
                    return result
                elif response_type == 6:
                    result = self.완전정지응답(unpacked_data)
                    return result
                elif response_type == 7:
                    result = self.일시정지응답(unpacked_data)
                    return result
                elif response_type == 4:
                    result = self.에러요청응답(unpacked_data)
                    return result
                elif response_type == 5:
                    result = self.세션연결확인응답(unpacked_data)
                    # return_msg = self.시리얼ID등록패킷()
                    # print(return_msg)
                    # self.server_socket.send(return_msg)
                    return result
        except Exception as e:
            print("핸들러응답함수예외처리",str(e))

    def handler_request(self, command, client_socket, **kwargs):
        # self.server_socket.connect((self.host, self.port))
        request = {
            "건조레시피명령": self.건조레시피명령,
            "시리얼ID요청": self.dryer_id_request,
            "센서데이터요청": self.senser_data_request,
            # "완전정지요청": SocketHandler.완전정지요청,
            # "일시정지요청": SocketHandler.일시정지요청,
            "에러체크요청": self.에러체크요청,
        }
        client_socket.send(request[command](**kwargs))
        response = client_socket.recv(1024)
        if response:
            result = self.handler_response(response)
        else:
            pass
        return result

    def serial_id_response(self, id_packet, result_num: int):
        packet = b'\x01'  # sender
        packet += b'\x0d'  # size
        packet += b'\x01'  # p type
        packet += b'\x01'  # resp type
        packet += id_packet  # device id (6 bytes)
        packet += b'\x01'  # result
        packet += b'\x0D\x0A'  # etx
        print(packet,"시리얼ID응답리턴패킷...!!!")
        return packet

    def session_response(self,id_packet):
        packet = b'\x01'
        packet += b'\x0F'
        packet += b'\x01'
        packet += b'\x02'
        packet += id_packet
        packet += b'\x01'  # max packet
        packet += b'\x01'  # current packet
        packet += b'\x00'  # result
        packet += b'\x0D\x0A'  # etx
        print(packet,"세션연결확인응답리턴패킷...!!!")
        return packet

    def 세션연결정보받음(self, packet):
        sender = packet[0]
        size = packet[1]
        p_type = packet[2]
        resp_type = packet[3]
        device_id = self.str_conversion(packet[4:10])  # 6바이트 device id
        max_packet = packet[10]
        current_packet = packet[11]
        result = packet[12]
        etx = packet[13:15]  # 2바이트 ETX

        return {
            "sender": sender,
            "size": size,
            "p_type": p_type,
            "resp_type": resp_type,
            "device_id": device_id,
            "max_packet": max_packet,
            "current_packet": current_packet,
            "result": result,
            "etx": etx,
        }

    def 건조레시피명령(self, ):#매개변수(ID,Crop, Max, State, H, M, S, Temp, Hum, Blow, Exhaust)
        # print(device_id,"건조레시피명령1")
        packet = b'\x01'          # Sender (1바이트) 헤더고정
        packet += b'\x1c'         # Size (1바이트) 헤더고정
        packet += b'\x01'       # P Type (1바이트) 헤더고정
        packet += b'\x01'       # Cmd Type (1바이트) 헤더고정
        packet += b'\x01\x01\x01\x01\x01\x01'      # Device ID (6바이트) 가변..
        packet += b'\x01'          # Option (1바이트)
        packet += b'\x00\x0e'        # Crop Type (2바이트) 가변..
        packet += b'\x00\x06'      # Max Stage (2바이트) 가변..
        packet += b'\x00\x06'    # State Count (2바이트) 가변..
        packet += b'\x01'           # H (1바이트) 가변..
        packet += b'\x01'           # M (1바이트) 가변..
        packet += b'\x01'          # S (1바이트) 가변..
        packet += b'\x01\x01'      # Target Temperature (2바이트)가변..
        packet += b'\x01\x01'   # Target Relative Humidity (2바이트)가변..
        packet += b'\x01'          # Blowing (1바이트)
        packet += b'\x01'          # Exhaust (1바이트)
        packet += b'\x0d\x0a'     # ETX (2바이트)
        return packet

    def 건조레시피응답패킷(self,packet):
        sender = packet[0]  # Sender (1바이트)
        size = packet[1]  # Size (1바이트)
        p_type = packet[2]  # P Type (1바이트)
        cmd_type = packet[3]  # Cmd Type (1바이트)
        device_id = self.str_conversion(packet[4:10])  # Device ID (6바이트)
        option = packet[11]  # Option (1바이트)
        crop_type = self.str_conversion(packet[12:13])  # Crop Type (2바이트)
        max_stage = self.str_conversion(packet[14:15]) # Max Stage (2바이트)
        state_cnt = self.str_conversion(packet[16:17])  # State Count (2바이트)
        h = packet[18]  # H (1바이트)
        m = packet[19]  # M (1바이트)
        s = packet[20]  # S (1바이트)
        target_temp = self.str_conversion(packet[21:22])  # Target Temperature (2바이트)
        target_hum = self.str_conversion(packet[23:24])  # Target Relative Humidity (2바이트)
        blowing = packet[25]  # Blowing (1바이트)
        exhaust = packet[26]  # Exhaust (1바이트)
        etx = self.str_conversion(packet[27:28])  # ETX (2바이트)

        return {
            "sender" : sender,
            "size" : size,
            "p_type" : p_type,
            "cmd_type" : cmd_type,
            "device_id" : device_id,
            "option" : option,
            "crop_type" : crop_type,
            "max_stage" : max_stage,
            "state_cnt" : state_cnt,
            "hour" : h,
            "minute" : m,
            "second" : s,
            "target_temp" : target_temp,
            "target_hum" : target_hum,
            "blowing" : blowing,
            "exhaust" : exhaust,
            "etx": etx,
        }

    def dryer_id_response(self, packet):
        sender = packet[0]
        size = packet[1]
        p_type = packet[2]
        resp_type = packet[3]
        device_id = self.str_conversion(packet[4:10]) # 6바이트 device id
        max_packet = packet[10]
        current_packet = packet[11]
        result = packet[12]
        etx = packet[13:15]  # 2바이트 ETX
        ("id응답값..")
        return {
            "sender_data": sender,
            "size": size,
            "p_type": p_type,
            "resp_type": resp_type,
            "device_id": device_id,
            "max_packet": max_packet,
            "current_packet": current_packet,
            "result": result,
            "etx": etx,
        }
    
    def dryer_id_request(self):
        packet = b'\x00'
        packet += b'\x06'
        packet += b'\x02'
        packet += b'\x01'
        packet += b'\x0d\x0a'
        print(packet,"---시리얼아이디요청")
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
        taget_temp = self.str_conversion(packet[14:15])
        taget_hum = self.str_conversion(packet[16:17])
        blowing = packet[18]
        exhaust = packet[19]
        etx	= self.str_conversion(packet[20:21])
        
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
    
    def senser_data_request(self):
        # 패킷 데이터 생성
        packet = b'\x00'  # sender
        packet += b'\x0F'  # size
        packet += b'\x02'  # p type
        packet += b'\x00'  # cmd type
        packet += self.device_id  # device id (6 bytes)
        packet += b'\x01'  # max packet
        packet += b'\x01'  # current packet
        packet += b'\x00'  # result
        packet += b'\x0D\x0A'  # etx
        print(packet,"senser값요청!!!!_--")
        return packet
    
    def 에러체크요청(self):
        packet = b'\x00'
        packet += b'\x0F'
        packet += b'\x02'
        packet += b'\x04'
        packet += b'\x17\x0a\x17\x00\x00\x01'
        packet += b'\x01'
        packet += b'\x01'
        packet += b'\x00'
        packet += b'\x0d\x0a'
        print("에러체크요청")
        return packet

    def 에러요청응답(self, packet):
        sender = packet[0]
        size = packet[1]
        p_type = packet[2]
        resp_type = packet[3]
        device_id = self.str_conversion(packet[4:10])  # 6바이트 device id
        max_packet = packet[10]
        current_packet = packet[11]
        result = packet[12]
        etx = packet[13:15]  # 2바이트 ETX

        return {
            "sender": sender,
            "size": size,
            "p_type": p_type,
            "resp_type": resp_type,
            "device_id": device_id,
            "max_packet": max_packet,
            "current_packet": current_packet,
            "result": result,
            "etx": etx,
        }