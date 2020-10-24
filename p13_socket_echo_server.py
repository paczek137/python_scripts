import datetime
import os
import socket

s = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
s = s + "\n" + os.path.basename(__file__)
print(s)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#server_address = ('localhost', 10000)
server_address = ('192.168.0.102', 10000)
s = "starting up on: " + str(server_address[0]) + ", port: " + str(server_address[1])
print(s)

sock.bind(server_address)
sock.listen(1)

while True:
        s = "waiting for connection...\n"
        print(s)
        connection, client_address = sock.accept()

        try:
            s = "connection from " + str(client_address)
            print(s)
            while True:
                data = connection.recv(16)
                s = "received " + str(data.decode())
                print(s)
                if data:
                    s = "sending data back to the client"
                    print(s)
                    connection.sendall(data)
                else:
                    s = "no more data from " + str(client_address)
                    print(s)
                    break

        finally:
            connection.close()
