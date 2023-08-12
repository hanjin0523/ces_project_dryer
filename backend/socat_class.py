import socket
import threading

class Socket_test:
    def __init__(self, HOST, PORT, max_connections):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.max_connections = max_connections
        self.server_socket.bind((HOST,PORT))
        self.server_socket.listen()
        self.accept_thread = threading.Thread(target=self.accept_clients, daemon=True)
        self.accept_thread.start()
        self.clients = []

    def accept_clients(self):
        while True:
            client_socket, client_addr = self.server_socket.accept()
            print(f"{client_addr} 연결됨")
            self.clients.append((client_socket, client_addr))
            # 연결된 클라이언트를 처리하는 쓰레드 시작
            # for client in self.clients:
            #     client_thread = threading.Thread(target=self.handle_client, args=(client[0], client[1]))
            #     client_thread.start()

    def handle_client(self, client_socket, client_addr):
        while True:
            data = client_socket.recv(1024).decode()
            if data == "h1_on":
                print(f"{client_addr}: h1_on 수신, 응답: 가동")
                client_socket.sendall("가동".encode())

    def send_message(self, message):
        if len(self.clients) > 0:
            client_socket, _ = self.clients[0]
            client_socket.sendall(message.encode('utf-8'))
        else:
            print("No connected clients.")

    def power_handler(self, command:list):
        for item in command:
            self.send_message(item)

    def senser1(self):
        if len(self.clients) > 0: 
            client_socket, _ = self.clients[0]
            if not client_socket._closed:
                client_socket.sendall('senser1'.encode('utf-8'))
                data = client_socket.recv(1024)
                return data
            else:
                return b"Client socket closed."
        else:
            return b"No connected clients."
