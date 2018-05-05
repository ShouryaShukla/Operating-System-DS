import os
import socket
import time
#import PyPDF2

path = 'PDFFolder'
if not os.path.exists(path):
    os.makedirs(path)

def Main():
    #ip = '127.0.1.1'
    host = socket.gethostbyname(socket.gethostname())
    port = 3333

    p = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    p.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    p.bind((host, port))
    p.listen(1)
    d, addr = p.accept()
    print ("Connection from: " + str(addr))

    print("PDF node connected to server " + str(addr[0]) + ":" + str(addr[1]))

    while True:
        size = d.recv(16)
        if not size:
            break
        size = int(size, 2)
        file_name = d.recv(size)

        file_size = d.recv(32)
        file_size = int(file_size, 2)
        block = 4096
        with open(os.path.join(path, file_name), 'wb') as f:
            while file_size > 0:
                if file_size < block:
                    block = file_size
                data = d.recv(block)
                f.write(data)
                file_size -= len(data)
        print("PDF Received " + file_name)

if __name__ == '__main__':
    Main()
