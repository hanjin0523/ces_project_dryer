import socket
import threading
import dataBaseMaria
import struct
import main

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
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(1)
            self.accept_thread = threading.Thread(target=self.accept_clients)
            self.accept_thread.start()
            self.initialized = True
            self.is_connected = False

    def accept_clients(self):
        while True:
            try:
                print(self.clients)
                client_socket, client_addr = self.server_socket.accept()
                if client_addr not in self.clients:
                    print(f"{client_addr} 연결됨")
                    self.clients.append((client_socket, client_addr))
                    received_data = client_socket.recv(1024)
                    if received_data:
                        received_data = self.handler_response(received_data)
                    else:
                        pass
                    client_socket.send(self.dryer_id_request())
                    print(received_data,"핸들러응답함수")
                    # mariadb.setting_dryer_num(client_addr[0])
                    main.dryer_set_device_id = received_data["device_id"]
                    dryer_registration_check = main.dry_accept.get_dryer_controller(received_data["device_id"])
                    print(dryer_registration_check,"등록여부..")
            except KeyboardInterrupt:
                self.stop()

    def senser(self, select_num: int):
        client_status = len(self.clients)
        if client_status:
            print(self.clients[0],"!!!")
            try:
                first_client_socket,_ = self.clients[select_num]
                # first_client_socket.settimeout(3)
                first_client_socket.send(self.senser_data_request())
                received_data = first_client_socket.recv(1024)
                if received_data:
                    received_data = self.handler_response(received_data)
                    print(received_data,"received_data11")
                else:
                    print("시불왜안됨")
                print(received_data,"received_data11")
                return 123
            except TimeoutError as e:
                print(str(e), "error")
                del self.clients[select_num]
                return False
            except BrokenPipeError as e:
                print(str(e),"error")
                del self.clients[select_num]
                return False
        else:
            return "No connected clients."

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
                return result
            elif packet_size == 15:
                if response_type == 1:
                    result = self.시리얼ID응답처리(unpacked_data)
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
                    result = self.dryer_id_response(unpacked_data)
                    # return_msg = self.시리얼ID등록패킷()
                    # print(return_msg)
                    # self.server_socket.send(return_msg)
                    return result
        except Exception as e:
            print("핸들러응답함수예외처리",str(e))

    def handler_request(self, command ,**kwargs):
        # self.client_socket.connect((self.server_ip, self.server_port))
        request = {
            # "건조레시피명령": SocketHandler.건조레시피명령,
            # "시리얼ID요청": SocketHandler.시리얼ID요청,
            "센서데이터요청": self.senser_data_request,
            # "완전정지요청": SocketHandler.완전정지요청,
            # "일시정지요청": SocketHandler.일시정지요청,
            # "에러체크요청": SocketHandler.에러체크요청,
        }
        self.client_socket.send(request[command](**kwargs))
        response = self.client_socket.recv(1024)
        if response:
            result = self.handler_response(response)
        else:
            pass
        print(result, f"---{command} result")
        return result

    def dryer_id_response(self, packet):
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
    
    def dryer_id_request(self):
        packet = b'\x00'
        packet += b'\x07'
        packet += b'\x01'
        packet += b'\x01'
        packet += b'\x01'
        packet += b'\x0d\x0a'
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
        packet = b'\x01'  # sender
        packet += b'\x0F'  # size
        packet += b'\x02'  # p type
        packet += b'\x00'  # cmd type
        packet += b'\x17\x0a\x17\x00\x00\x01'  # device id (6 bytes)
        packet += b'\x01'  # max packet
        packet += b'\x01'  # current packet
        packet += b'\x00'  # result
        packet += b'\x0D\x0A'  # etx
        return packet