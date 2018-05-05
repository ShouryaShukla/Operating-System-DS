import socket
import os
import time
#import PyPDF2

ServerFile = open('Server File.txt', "a+")

def Main():
    host = socket.gethostbyname(socket.gethostname())
    port = 2222
    txtPort= 1112
    pdfPort= 3333
    mp3Port= 4444
    otherPort= 5555

    s = socket.socket()
    s.bind((host, port))

    s.listen(1)
    print("Server is now listening at-"+host)
    c, addr = s.accept()
    print ("Connection from: " + str(addr))


    #t.bind((host, txtPort))
    #t.listen(1)
    #d, addr2 = t.accept()
    #print ("Connection from: " + str(addr2))

    #
    # u=socket.socket()
    # u.bind((host, pdfPort))
    # u.listen(1)
    # e, addr3= t.accept()
    # print ("Connection from: " + str(addr3))
    #
    #
    # v=socket.socket()
    # v.bind((host, mp3Port))
    # v.listen(1)
    # f, addr4= t.accept()
    # print ("Connection from: " + str(addr4))
    #
    #
    #
    # w=socket.socket()
    # w.bind((host, txtPort))
    # w.listen(1)
    # g, addr5= t.accept()
    # print ("Connection from: " + str(addr5))


    # st = 'Please Upload file (with path) to be synced: '
    # byt = st.encode()
    # c.send(byt)
    numFiles = c.recv(3)
    numFiles = str(numFiles.decode())

    t = socket.socket()
    t.connect((host, txtPort))

    print("NumFiles: "+numFiles)
    # print(int(numFiles))
    for i in range(0, int(numFiles)-1):
        # print(int(numFiles[:1]))
        file_name = ''
        file_data = ''
        counter = 1
        SumCurrent = ''
        while True:
            current = c.recv(1)
            current = str(current.decode())
            # print("Current: "+current)
            if current == '#' and counter == 1:
                file_name = SumCurrent
                print("File Name is "+file_name)
                SumCurrent = ''
                counter += 1
            if current == '$' and counter == 2:
                file_data = SumCurrent
                file_data = file_data[1:]
                print("File data is: "+file_data)

                extt = file_name.split('.')
                ext = extt[1]
                print("File Name is " + file_name)
                # print("Data is " + file_data)
                if ext == 'txt':
                    ServerFile.write(file_name + ' ' + 'txtNode ' + str(txtPort) + '\n')


                    SendTxt = file_name + '#' + file_data + '$'
                    print("Sending: " + SendTxt)
                    SendTxt = SendTxt.encode()
                    t.send(SendTxt)
                    time.sleep(5)
                break

            SumCurrent += current
            if not current:
                break

        #file_name = c.recv(1024)
        #file_name = str(file_name.decode())
        #print("Got Name: "+file_name)
        #print(file_name)
        #time.sleep(1)
        #file_data = c.recv(1024)
        #file_data = str(file_data.decode())
        #print("Got Data: "+file_data)
       # print(file_data)
        #file_data.decode()
            # if not file_name:
            #     break
        # print "Request received from client: " + str(data)

        # print "Number of results: " + str(len(data))

        # File= open(path+"/"+file_name, "a+")
        # File.write(file_data)

            # time.sleep(2)
            # d2 = file_data.encode()
            # d.send(d2)

        # Haven't been able to figure this part out
        # elif(ext=='pdf'):
        #     ServerFile.write(file_name + ' ' + 'pdfNode' + str(pdfPort))
        #    send file through pdfPort
        # elif (ext=='mp3'):
        #     ServerFile.write(file_name + ' ' + 'mp3Node' + str(mp3Port))
        #    send file through mp3Port
        # else:
        #     ServerFile.write(file_name + ' ' + 'OoherNode' + str(otherPort))
        #    send file through otherPort

    c.close()
    #d.close()
    # e.close()
    # f.close()
    # g.close()

if __name__ == '__main__':
    Main()
