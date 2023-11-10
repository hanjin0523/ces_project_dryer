import socket
import threading
import dataBaseMaria
import struct
import main
import select
import time
import asyncio
import queue
import select

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

    def client_handler(self, client_socket,client_addr):
        # threading.Thread.setDaemon(self, True)
        while client_socket:
            try:
                print("돈다 돌아~")
                client_socket.settimeout(300)  # Set a timeout for socket operations
                self.clients.append((client_socket,client_addr))
                received_data = client_socket.recv(1024)
                if received_data:
                    self.received_data_handler(received_data, client_socket, client_addr)
            except socket.timeout:
                print("No data received within the timeout")
                client_socket.close()  # Close the socket
                break  # Exit the loop

    def accept_clients(self):
        while True: 
            try:
                client_socket, client_addr = self.server_socket.accept()
                print(client_addr,"client_addr---접속됨..")
                client_thread = threading.Thread(target=self.client_handler, args=(client_socket,client_addr))
                client_thread.setDaemon(True)
                client_thread.start()
            except KeyboardInterrupt :
                break
            
    def senser(self, select_num: int, dryer_set_device_id: str):
        try:##센서데이터 수정해야되!!!
            with self.socket_lock:
                print(self.clients[select_num][0],"-----clients-----")
                print(self.clients_id,"-----senser-----")
                senser_socket = self.clients[select_num][0]
                print(time.time(),"start----")
                senser_socket.send(self.senser_data_request())
                # re = self.handler_request("센서데이터요청",senser_socket)
                re = senser_socket.recv(1024)
                result = self.senser_data_response(re)
                print(time.time(),"-----reuslt")
                print(result,"-----senser----")
                return re
        finally:
            pass
            # except BrokenPipeError as e:
            #     print(str(e),"error")
            #     senser_socket = self.clients.pop(select_num)
            #     del self.clients_id[dryer_set_device_id]
            #     return False
        
    def power_on_off(self, dryer_set_number:int, operating_conditions):
        with self.socket_lock:
            power_socket,_ = self.clients[dryer_set_number]
            # command = ["001c0003170a1700000100000b000300000100003c00000001010d0a",
            #             "001c0003170a1700000100000b000300010300004100000001010d0a",
            #             "001c0003170a1700000100000b000300020100004600000001010d0a"]
            # for item in command:
            #     # gg = hex(command)
            #     power_socket.send(bytes.fromhex(item))
            print(operating_conditions,"operating_conditions----")
            total_stage = 0
            for sum_stage in operating_conditions:  
                total_stage += sum_stage[2]
            print(total_stage)
            def convert_seconds_to_time(seconds):
                hours = seconds // 3600
                minutes = (seconds % 3600) // 60
                seconds = seconds % 60
                return hours, minutes, seconds
            count = -1
            for item in operating_conditions:
                count += item[2]
                hours, minutes, seconds = convert_seconds_to_time(item[3])
                hour = hours
                minute = minutes
                second = seconds
                set_temp = item[4]
                set_hum = item[5]
                power_socket.send(self.건조레시피명령(total_stage, count, hour, minute, second, set_temp, set_hum))
                print(hour,"시간",minute,"분",second,"초")
    def power_pause(self, dryer_set_number:int):
        with self.socket_lock:
            pause_socket, _ = self.clients[dryer_set_number]
            pause_socket.send(self.일시정지요청())
            re = pause_socket.recv(1024)
            print(re,"일시정지패킷응답...")

    def stop_and_go(self, dryer_set_number:int):
        with self.socket_lock:
            stop_and_go_packet, _ = self.clients[dryer_set_number]
            stop_and_go_packet.send(self.재시작요청())
            re = stop_and_go_packet.recv(1024)
            print(re,"재시작패킷응답...")

    def stop_dryer(self, dryer_set_number:int):
        with self.socket_lock:
            stop_dryer_packet, _ = self.clients[dryer_set_number]
            stop_dryer_packet.send(self.완전정지요청())
            re = stop_dryer_packet.recv(1024)
            print(re,"완전정지요청패킷응답...")

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
                    result = self.session_request(unpacked_data)
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

    # def 동작정지명령App():
    #     pac

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
        packet += b'\x17\x0a\x17\x00\x00\x01'
        packet += b'\x01'  # max packet
        packet += b'\x01'  # current packet
        packet += b'\x00'  # result
        packet += b'\x0D\x0A'  # etx
        print(packet,"세션연결확인응답리턴패킷...!!!")
        return packet

    def session_request(self, packet):
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
        packet += b'\x17\x0a\x17\x00\x00\x01'  # device id (6 bytes)
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

    def 재시작응답(self,packet):
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
    
    def 일시정지응답(self,packet):
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

    def 완전정지요청(self,):
        packet = b'\x00'
        packet += b'\x0F'
        packet += b'\x00'
        packet += b'\x06'
        packet += b'\x17\x0a\x17\x00\x00\x01'
        packet += b'\x01'
        packet += b'\x01'
        packet += b'\x00'
        packet += b'\x0D\x0A'
        print(packet,"완전정지요청패킷날리기!!!")
        return packet

    def 완전정지응답(self,packet):
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

    # def 건조레시피명령(self, hex_string: int):#매개변수(ID,Crop, Max, State, H, M, S, Temp, Hum, Blow, Exhaust)
    #     packet = b'\x00'          # Sender (1바이트) 헤더고정
    #     packet += b'\x1c'         # Size (1바이트) 헤더고정
    #     packet += b'\x00'       # P Type (1바이트) 헤더고정
    #     packet += b'\x03'       # Cmd Type (1바이트) 헤더고정
    #     packet += b'\x17\x0a\x17\x00\x00\x01'      # Device ID (6바이트) 가변..
    #     packet += b'\x00'          # Option (1바이트)
    #     packet += b'\x00\x0e'        # Crop Type (2바이트) 가변..
    #     packet += b'\x00\x02'      # Max Stage (2바이트) 가변..
    #     packet += b'\x00\x00'
    #     packet += b'\x00' # State Count (2바이트) 가변..  0///1
    #     packet += b'\0x02'           # H (1바이트) 가변..
    #     packet += b'\0x02'           # M (1바이트) 가변..
    #     packet += b'\x00'          # S (1바이트) 가변..
    #     packet += b'\0x3C\x02'      # Target Temperature (2바이트)가변..
    #     packet += b'\0x14\x00'   # Target Relative Humidity (2바이트)가변..
    #     packet += b'\x01'          # Blowing (1바이트)
    #     packet += b'\x01'          # Exhaust (1바이트)
    #     packet += b'\x0d\x0a'     # ETX (2바이트)
    #     packet = bytes.fromhex(hex_string)
    #     print(packet,"건조레시피명령-----")
    #     return packet
    
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

    def test_packet(self,command: str):
        with self.socket_lock:
            test_socket = self.clients[0][0]
            if command == "session":
                print(command,"----commnad_name")
                test_socket.send(self.session_response(self.device_id))
                msg = test_socket.recv(1024)
                print(msg,"-----session-----")
            elif command == "sensertest":
                print(command,"----commnad_name")
                test_socket.send(self.senser_data_request())
                msg = test_socket.recv(1024)
                self.message_queue.put(msg)
                print(self.senser_data_response(msg),"-----sensertest-----")
            elif command == "pause":
                print(command,"----commnad_name")
                test_socket.send(self.일시정지요청())
                msg = test_socket.recv(1024)
                print(self.일시정지응답(msg),"-----일시정지응답-----")
            elif command == "completelystop":
                print(command,"----commnad_name")
                test_socket.send(self.완전정지요청())
                msg = test_socket.recv(1024)
                print(self.완전정지응답(msg),"-----완전정지응답-----")
            elif command == "action":
                print(command,"----commnad_name")
                test_socket.send(self.건조레시피명령())
                # msg = test_socket.recv(1024)
                # print(self.건조레시피응답패킷(msg),"-----건조레시피응답패킷-----")
            # except Exception as e:
            #     print(str(e))