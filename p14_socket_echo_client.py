import datetime
import os
import socket
import sys

s = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
s = s + "\n" + os.path.basename(__file__)
print(s)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
#server_address = ('localhost', 10000)
#server_address = ('192.168.0.102', 10000)
server_address = ('78.8.146.92', 10020)
#server_address = ('2001:41d0:601:1100:0:0:0:72', 50035, 0, 0)
s = "connecting to: " + str(server_address[0]) + ", port: " + str(server_address[1])
print(s)
#res = socket.getaddrinfo('2001:41d0:601:1100:0:0:0:72', 50035)
#family, socktype, proto, cononname, sockaddr = res[1]
#print(res)
#sys.exit()
sock.connect(server_address)
#sock.connect(('2001:41d0:601:1100:0:0:0:72', 50035, 0, 0))

try:
    message = "qwertyuiop+socket_test"
    s = "sending " + str(message)
    print(s)
    sock.sendall(message.encode())

    amount_received = 0
    amount_expected = len(message)

    while amount_received < amount_expected:
        data = sock.recv(16)
        amount_received = amount_received + len(data)
        s = "received: " + str(data.decode())
        print(s)

finally:
    s = "closing socket"
    print(s)
    sock.close()


