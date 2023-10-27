import socket
import threading
import dataBaseMaria
import time
import main

mariadb = dataBaseMaria.DatabaseMaria('211.230.166.113', 3306, 'jang', 'jang','cesdatabase','utf8')

class Socket_test:
    _instance = None  # 클래스 변수로 인스턴스를 저장

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, host, port, max_connections):
        if not hasattr(self, 'initialized'):
            self.host = host
            self.port = port
            self.max_connections = max_connections
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
                client_socket, client_addr = self.server_socket.accept()
                print(f"{client_addr} 연결됨")
                self.clients.append((client_socket, client_addr))
                mariadb.setting_dryer_num(client_addr[0])
                main.dryer_set_device_id = client_addr[0]
                main.dry_accept.get_dryer_controller(client_addr[0])
                print(self.clients,"모든접촉한클라")
            except KeyboardInterrupt:
                self.stop()

    def power_on_off(self, num, input_text):
        if len(self.clients) > num:
                first_client_socket, _ = self.clients[num]
                try:
                    for text in input_text:
                        first_client_socket.sendall(text.encode())
                    return True
                except BrokenPipeError:
                    print("Connection with client has been broken.")
                    return False
        else:
            print("No connected clients.")      
            
    def blower_on_off(self, num, input_text):
        time.sleep(0.1)##반복문 도는 타이밍때문에 sleep줌
        if len(self.clients) >= num:
                first_client_socket, _ = self.clients[num]  
                try:
                    for text in input_text:
                        first_client_socket.sendall(text.encode())
                    return False
                except BrokenPipeError:
                    print("Connection with client has been broken.")
                    return False
        else:
            print("No connected clients.")          

    def senser(self, dryer_number: int):
        client_status = len(self.clients)
        if client_status:
            try:
                first_client_socket,_ = self.clients[dryer_number]
                first_client_socket.settimeout(3)
                first_client_socket.sendall('senser1'.encode())
                data = first_client_socket.recv(1024)
                return data
            except TimeoutError as e:
                print(str(e), "error")
                del self.clients[dryer_number]
                return False
            except BrokenPipeError as e:
                print(str(e),"error")
                del self.clients[dryer_number]
                return False
        else:
            return "No connected clients."
