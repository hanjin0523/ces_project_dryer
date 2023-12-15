import socket
import threading
import queue
import struct
import main
import time
import packet.send_packet as send_packet
import packet.recv_packet as recv_packet
import psutil
import json
import logging_file.logging_debug as logging_debug

logger = logging_debug.Logger(__name__).get_logger()
logger.setLevel(logging_debug.logging.DEBUG)

class Socket_test:
    def __init__(self, host:str, port:int):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(10)
        self.accept_thread = threading.Thread(target=self.accept_clients)
        self.accept_thread.start()
        self.my_queues = {}
        self.clients = []
        self.clients_id = []
        self.device_ids = {}
        self.socket_lock = threading.Lock() 
        self.temp_hum_data = []
        self.send_queues = {}

    def accept_clients(self):
        while True:
            try:
                client_socket, client_addr = self.server_socket.accept()
                self.my_queues[client_socket] = queue.Queue(maxsize=4)
                self.send_queues[client_socket] = queue.Queue()
                client_thread = threading.Thread(target=self.client_handler, args=(client_socket,client_addr))
                client_thread.daemon = True
                client_thread.start()
                send_thread = threading.Thread(target=self.send_packets, args=(client_socket,))
                send_thread.daemon = True
                send_thread.start()
                logger.info("connected by : %s", client_addr)
            except KeyboardInterrupt:
                for sock in psutil.net_connections():
                    sock.close()
                break
            except Exception as e:
                logger.error("accept error",e)

    def send_packets(self, client_socket):
        while True:
            packet = self.send_queues[client_socket].get()
            client_socket.send(packet)

    def client_handler(self, client_socket, client_addr):
        client_socket.settimeout(120)  # Set the timeout to 90 seconds
        while True:
            try:
                recv = client_socket.recv(1024)
                # logger.info("recv_message : %s",recv)
                if recv:
                    if len(recv) == 22:
                        self.my_queues[client_socket].put(recv)
                    elif len(recv) == 15:
                        self.received_data_handler(recv, client_socket, client_addr)
                        logger.debug("초기접속&세션Packet : %s",recv)
            except socket.timeout:  # If the socket times out
                self.clients_id.remove(self.device_ids[client_socket])  # Remove the device_id from the clients_id list
                self.clients.remove((client_socket, client_addr))
                del main.dryer_controllers[self.device_ids[client_socket]]
                client_socket.close()  # Close the socket
                logger.info("remove_socket : %s", client_socket)  # Print when the socket is removed
                break  # Exit the loop

    def received_data_handler(self, received_data, client_socket, client_addr):
        device_id = self.id_packet(received_data)
        self.device_ids[client_socket] = device_id
        str_device_id = self.str_conversion(device_id)
        if device_id not in self.clients_id:
            self.clients_id.append(device_id)
            self.clients.append((client_socket,client_addr))
        conversion_length = (received_data[1]*"B")
        unpacked_data = struct.unpack(conversion_length, received_data)
        response_type = unpacked_data[3]
        main.dry_accept.get_dryer_controller(device_id)
        self.handle_response_type(response_type, client_socket, device_id)
        return True

    def handle_response_type(self, response_type, client_socket, device_id):
        if response_type == 5:
            response_packet = send_packet.Id_reponse_packet(0, 13, 1, 1, device_id, 1)
        elif response_type == 2:
            response_packet = send_packet.Default_packet(0, 15, 1, 2, device_id, 1, 1, 0)
        else:
            return
        self.send_queues[client_socket].put(response_packet.create_packet())        

    def create_senser_packet(self, senser_socket):
        return send_packet.Default_packet(0, 15, 2, 0, self.device_ids[senser_socket], 1, 1, 0)

    def get_temp_hum_data(self, senser_socket):
        try:
            temp_hum_data = self.my_queues[senser_socket].get(block=False)
            return temp_hum_data
        except queue.Empty:
            logger.info("No data in queue")
            return None

    def process_temp_hum_data(self, temp_hum_data, select_num):
        # result = self.senser_data_response(temp_hum_data)
        result1 = recv_packet.senser_data.senser_data_response(temp_hum_data)
        result_json = result1.to_json()
        result = json.loads(result_json)
        temp = round((int(result["taget_temp"][0])/100),1)
        hum = round((int(result["taget_hum"][0])/100),1)
        logger.info("%s번 건조기 : %.1f온도, %.1f%%습도", select_num, temp, hum)
        return [temp, hum]

    def clear_queue(self, senser_socket):
        with self.my_queues[senser_socket].mutex:
            self.my_queues[senser_socket].queue.clear()

    def senser(self, select_num: int):
        try:
            senser_socket,_ = self.clients[int(select_num)]
            senser_packet = self.create_senser_packet(senser_socket)
            with self.socket_lock:  # Acquire the lock before accessing the socket
                self.send_queues[senser_socket].put(senser_packet.create_packet())
                temp_hum_data = self.get_temp_hum_data(senser_socket)
                if temp_hum_data is None:
                    return
                temp_hum = self.process_temp_hum_data(temp_hum_data, select_num)
                self.clear_queue(senser_socket)
                return temp_hum
        except Exception as e:
            logger.error("센서에러", str(e))

    def power_on_off(self, select_num:int, operating_conditions):
        with self.socket_lock:
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
                power_packet = send_packet.Drying_stage_packet(0, 28, 0, 3, self.device_ids[power_socket], 0, 14, total_stage, count, hours, minutes, seconds, set_temp, set_hum,1,1)
                self.send_queues[power_socket].put(power_packet.create_packet())

    def send_power_packet(self, select_num:int, packet_code:int):
        with self.socket_lock:
            power_socket,_ = self.clients[int(select_num)]
            power_packet = send_packet.Default_packet(0, 15, 0, packet_code, self.device_ids[power_socket], 1, 1, 0)
            self.send_queues[power_socket].put(power_packet.create_packet())

    def power_pause(self, select_num:int):
        self.send_power_packet(select_num, 7)

    def power_restart(self, select_num:int):
        self.send_power_packet(select_num, 8)

    def power_stop(self, select_num:int):
        self.send_power_packet(select_num, 6)

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
    
    # def senser_data_response(self, packet):
    #     sender = packet[0]  # Sender (1바이트)
    #     size = packet[1]  # Size (1바이트)
    #     p_type = packet[2]  # P Type (1바이트)
    #     cmd_type = packet[3]  # Cmd Type (1바이트)
    #     device_id = self.str_conversion(packet[4:10])  # Device ID (6바이트)
    #     max_packet = packet[10]
    #     current_packet = packet[11]
    #     operation = packet[12]
    #     sign = packet[13]
    #     taget_temp = struct.unpack("H", packet[14:16])
    #     taget_hum = struct.unpack("H", packet[16:18])
    #     blowing = packet[18]
    #     exhaust = packet[19]
    #     etx	= packet[20:21]
        
    #     return {
    #         "sender" : sender,
    #         "size" : size,
    #         "p_type" : p_type,
    #         "cmd_type" : cmd_type,
    #         "device_id" : device_id,
    #         "max_packet" : max_packet,
    #         "current_packet" : current_packet,
    #         "operation" : operation,
    #         "sign" : sign,
    #         "taget_temp" : taget_temp,
    #         "taget_hum" : taget_hum,
    #         "blowing" : blowing,
    #         "exhaust" : exhaust,
    #         "etx" : etx

    #     }