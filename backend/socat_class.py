import socket
import threading

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
            client_socket, client_addr = self.server_socket.accept()
            print(f"{client_addr} 연결됨")
            self.clients.append((client_socket, client_addr))
            # 연결된 클라이언트를 처리하는 쓰레드 시작
            # for client in self.clients:
            #     client_thread = threading.Thread(target=self.handle_client, args=(client[0], client[1]))
            #     client_thread.start()

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

    def senser(self, num, input_text):
        if len(self.clients) > num:
                first_client_socket, _ = self.clients[num]  
                try:
                    for text in input_text:
                        first_client_socket.sendall(text.encode())
                        data = first_client_socket.recv(1024)
                    return data
                except BrokenPipeError:
                    print("Connection with client has been broken.")
                    return 0
        else:
            print("No connected clients.")  

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
