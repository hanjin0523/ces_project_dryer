import socket

class Socket_test:
    def __init__(self, HOST, PORT):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((HOST, PORT))
        self.s.listen()
        self.conn, self.addr = self.s.accept()
        print(self.addr)

    def send_message(self, message):
        self.conn.sendall(message.encode('utf-8'))
        print('Connected by', self.addr)

    def power_handler(self, command:list):
        for item in command:
            self.send_message(item)

    def senser1(self,):
        self.send_message('senser1')
        data = self.conn.recv(1024)
        return data
