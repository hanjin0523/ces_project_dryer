import socket
import threading
import dataBaseMaria
import time
import atexit

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

    def stop(self):
    # 프로그램을 종료할 때 호출되는 메서드
        print("서버를 종료합니다.")
        for client_socket, _ in self.clients:
            client_socket.close()  # 모든 클라이언트 소켓을 닫음
        self.server_socket.close()  # 서버 소켓을 닫음
    # 기타 정리 작업 추가

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
            
    def power_off(self, num, input_text):
        if len(self.clients) >= num:
                first_client_socket = self.clients[num]  
                try:
                    for text in input_text:
                        first_client_socket[0].sendall(text.encode())
                    return False
                except BrokenPipeError:
                    print("Connection with client has been broken.")
                    return False
        else:
            print("No connected clients.")      

    def senser(self, select_num, dryer_number, input_text):
        client_status = len(self.clients)
        if client_status:
            try:
                first_client_socket,_ = self.clients[dryer_number]
                first_client_socket.sendall('senser1'.encode())
                data = first_client_socket.recv(1024)
                return data
            except BrokenPipeError as e:
                print(str(e),"error")
                del self.clients[dryer_number]
                return False
        else:
            return "No connected clients."
