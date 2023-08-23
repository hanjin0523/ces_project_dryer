import socket
import threading
import dataBaseMaria

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
            self.server_socket.listen()
            self.accept_thread = threading.Thread(target=self.accept_clients)
            self.accept_thread.start()
            self.initialized = True

    def accept_clients(self):
        
        while True:
            try:
                client_socket, client_addr = self.server_socket.accept()
                print(f"{client_addr} 연결됨")
                self.clients.append((client_socket, client_addr))
                mariadb.setting_dryer_num(client_addr[0])
            except KeyboardInterrupt:
                self.stop()

    def power_on(self, num, input_text):
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
            
    def power_off(self, num, input_text):
        if len(self.clients) > num:
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

    def senser(self, select_num, dryer_number, input_text):
        client_status = len(self.clients)
        print(dryer_number,"건조기남바변경됨!?!?!?!")
        if client_status:
            for client, idx in self.clients:
                print(idx,"=============")
                first_client_socket = client
                if idx[0] == '192.168.0.23':   
                    print("192.168.0.23","실행")
                    try:
                        first_client_socket.sendall('senser1'.encode())
                        data = first_client_socket.recv(1024)
                        return data
                    except BrokenPipeError:
                        print("Connection with client has been broken.")
                        return 0
                if idx[0] == '192.168.0.24':   
                    try:
                        first_client_socket.sendall('senser1'.encode())
                        data = first_client_socket.recv(1024)
                        print(data,"실행")
                        return data
                    except BrokenPipeError:
                        print("Connection with client has been broken.")
                        return 0
        else:
            return "No connected clients."


    def stop(self):
        print("Stopping server...")
        for client_socket, _ in self.clients:
            client_socket.close()
        self.server_socket.close()
        print("Server stopped.")


    # def power_handler(self, command:list):
    #     for item in command:
    #         self.send_message(item)

    # def senser1(self):
    #     if len(self.clients) > 0: 
    #         client_socket, _ = self.clients[0]
    #         if not client_socket._closed:
    #             client_socket.sendall('senser1'.encode('utf-8'))
    #             data = client_socket.recv(1024)
    #             return data
    #         else:
    #             return b"Client socket closed."
    #     else:
    #         return b"No connected clients."
