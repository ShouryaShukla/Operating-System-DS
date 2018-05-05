import socket
import time


class Server():
    def __init__(self, storage_IP):
        self.Server_IP = socket.gethostbyname(socket.gethostname())
        self.Server_PORT = 2222
        print("Server IP: " + self.Server_IP)
        print("Server port: " + str(self.Server_PORT))
        self.index = {}
        self.connect(storage_IP)

    def connect(self, storage_IP):
        self.client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.client_sock.bind((self.Server_IP, self.Server_PORT))

        self.txt_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.txt_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.txt_sock.connect((storage_IP, 1234))
        self.pdf_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.pdf_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.pdf_sock.connect((storage_IP, 2345))
        self.mp3_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.mp3_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.mp3_sock.connect((storage_IP, 3456))
        self.other_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.other_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.other_sock.connect((storage_IP, 4567))
        print("Connected to storage nodes.")
        self.storage = {"txt": self.txt_sock, "pdf": self.pdf_sock, "mp3": self.mp3_sock, "other": self.other_sock}

        print("Server is listening...")
        # connect to client
        self.client_sock.listen(1)
        (self.conn, add) = self.client_sock.accept()
        print("Connection established with client at " + str(add[0]) + ":" + str(add[1]) + "\n")

        self.getData()

    def getData(self):
        while True:
            size = self.conn.recv(16)
            if not size:
                break
            int_size = int(size, 2)
            file_name = self.conn.recv(int_size).decode()
            print(file_name)

            file_type = file_name[file_name.index('.') + 1:]
            if file_type != "txt" and file_type != "pdf" and file_type != "mp3":
                file_type = "other"

            self.storage[file_type].send(size)
            self.storage[file_type].send(file_name.encode())

            self.index[file_name] = self.storage[file_type]

            file_size = self.conn.recv(32)
            self.storage[file_type].send(file_size)
            file_size = int(file_size, 2)
            block = 4096
            while file_size > 0:
                if file_size < block:
                    block = file_size
                data = self.conn.recv(block)
                self.storage[file_type].send(data)
                file_size -= len(data)


server_node = Server("127.0.1.1")
