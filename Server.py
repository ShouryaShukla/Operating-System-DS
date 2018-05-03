import socket
import os
path = 'ServerFolder'
if not os.path.exists(path):
    os.makedirs(path)

def Main():
    host = '0.0.0.0'
    port = 2222


    s = socket.socket()
    s.bind((host,port))

    s.listen(1)
    c, addr = s.accept()
    print ("Connection from: " + str(addr))
    st = 'Please Upload file to be synced.'
    byt = st.encode()
    c.send(byt)

    while True:

        file_name = c.recv(1024)
        file_name = str(file_name.decode())
        print(file_name)
        #print("1")
        file_data=c.recv(1024)
        file_data = str(file_data.decode())
        print(file_data)
        #file_data.decode()
        if not file_name:
            break
        # print "Request received from client: " + str(data)

        # print "Number of results: " + str(len(data))

        File= open(path+"/"+file_name, "a+")
        File.write(file_data)


    c.close()

if __name__ == '__main__':
    Main()