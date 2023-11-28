import socket
import threading
import queue
import struct
import main
import time
import packet
import psutil

class Socket_test:

    def __init__(self, host:str, port:int):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(10)
        self.accept_thread = threading.Thread(target=self.accept_clients)
        self.accept_thread.start()
        self.my_queue = queue.Queue(maxsize=4)
        self.clients = []
        self.clients_id = []
        self.device_id = ''
        self.socket_lock = threading.Lock() 
        self.temp_hum_data = []

    def accept_clients(self):
        while True:
            try:
                client_socket, client_addr = self.server_socket.accept()
                client_thread = threading.Thread(target=self.client_handler, args=(client_socket,client_addr))
                client_thread.daemon = True
                client_thread.start()
                print("connected by", client_addr)
            except KeyboardInterrupt:
                for sock in psutil.net_connections():
                    sock.close()
                break
            except Exception as e:
                print("accept error",e)

    def client_handler(self, client_socket, client_addr):
        while True:
            try:
                recv = client_socket.recv(100)
            except ConnectionResetError as e:
                print("파씽실패!!")
                continue
            # if not recv:
            #     continue
            if len(recv) == 22:
                # self.temp_hum_data = []
                # self.temp_hum_data.append(recv)
                self.my_queue.put(recv)
            if len(recv) == 15:
                self.received_data_handler(recv, client_socket, client_addr)
                print(recv,"초기접속, 세션임")
            else:
                pass

    def received_data_handler(self, received_data, client_socket, client_addr):
        make_id_packet = self.id_packet(received_data)
        self.device_id = make_id_packet
        str_device_id = self.str_conversion(make_id_packet)
        if self.device_id not in self.clients_id:
            self.clients_id.append(self.device_id)
            self.clients.append((client_socket,client_addr))
        else:
            pass
        conversion_length = (received_data[1]*"B")
        unpacked_data = struct.unpack(conversion_length, received_data)
        response_type = unpacked_data[3]
        main.dryer_set_device_id = str_device_id
        main.dry_accept.get_dryer_controller(str_device_id)
        if response_type == 5:
            id_reponse_packet = packet.Id_reponse_packet(0, 13, 1, 1, make_id_packet, 1)
            client_socket.send(id_reponse_packet.create_packet())
            return True
        elif response_type == 2:
            serial_id_response = packet.Default_packet(0, 15, 1, 2, make_id_packet, 1, 1, 0)
            client_socket.send(serial_id_response.create_packet())
            return True
        return True           
    
    def senser(self, select_num: int, dryer_set_device_id: str):
        try:##센서데이터 수정해야되!!!
            senser_socket,_ = self.clients[int(select_num)]
            senser_packet = packet.Default_packet(0, 15, 2, 0, self.clients_id[int(select_num)], 1, 1, 0)
            with self.socket_lock:  # Acquire the lock before accessing the socket
                senser_socket.send(senser_packet.create_packet())
                temp_hum_data1 = self.my_queue.get()
                temp_hum_data = self.my_queue.get()
                # temp_hum_data = self.temp_hum_data[0]
                result = self.senser_data_response(temp_hum_data)
                temp = round((int(result["taget_temp"][0])/100),1)
                hum = round((int(result["taget_hum"][0])/100),1)
                print(f"{select_num}번 건조기 :{temp}온도, {hum}%습도")
                with self.my_queue.mutex:
                    self.my_queue.queue.clear()
                return [temp,hum]
        except Exception as e:
            print("센서에러", str(e))
            # senser_socket.close()
            # self.clients.pop(select_num)
            # self.clients_id.pop(select_num)

    def power_on_off(self, select_num:int, operating_conditions):
        with self.socket_lock:
            print(select_num)
            power_socket,_ = self.clients[int(select_num)]
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
                power_packet = packet.Drying_stage_packet(0, 28, 0, 3, self.clients_id[int(select_num)], 0, 14, total_stage, count, hours, minutes, seconds, set_temp, set_hum,1,1)
                power_socket.send(power_packet.create_packet())

    def power_pause(self, select_num:int):
        with self.socket_lock:
            power_socket,_ = self.clients[int(select_num)]
            power_packet = packet.Default_packet(0, 15, 0, 7, self.clients_id[int(select_num)], 1, 1, 0)
            power_socket.send(power_packet.create_packet())

    def power_restart(self, select_num:int):
        with self.socket_lock:
            power_socket,_ = self.clients[int(select_num)]
            power_packet = packet.Default_packet(0, 15, 0, 8, self.clients_id[int(select_num)], 1, 1, 0)
            power_socket.send(power_packet.create_packet())

    def power_stop(self, select_num:int):
        with self.socket_lock:
            power_socket,_ = self.clients[int(select_num)]
            power_packet = packet.Default_packet(0, 15, 0, 6, self.clients_id[int(select_num)], 1, 1, 0)
            power_socket.send(power_packet.create_packet())

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