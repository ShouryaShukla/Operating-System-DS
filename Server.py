import socket
import os
newpath = 'C:\Users\shourya\PycharmProjects\OSAssignment3\ServerFolder'
if not os.path.exists(newpath):
    os.makedirs(newpath)

def Main():
    host = '0.0.0.0'
    port = 2345


    s = socket.socket()
    s.bind((host,port))

    s.listen(1)
    c, addr = s.accept()
    print "Connection from: " + str(addr)
    c.send('Please Upload file to be synced.')
    while True:

        file_name = c.recv(1024)
        file_data=c.recv(1024)
        if not file_name:
            break
        # print "Request received from client: " + str(data)

        # print "Number of results: " + str(len(data))

        File= open("C:/Users/shourya/PycharmProjects/OSAssignment3/ServerFolder"+"/"+file_name, "a+")
        File.write(file_data)


    c.close()

if __name__ == '__main__':
    Main()