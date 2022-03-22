import sys
import socket
import threading

#TODO: exit program when client ends the connection
def connect(conn):
    while True:
        received = conn.recv(1024)
        if received ==' ':
            pass
        else:
            print(received.decode())

def sendMsg(conn):
    while True:
        send_msg = input().replace('b', '').encode()
        if send_msg == ' ':
            pass
        else:
            conn.sendall(send_msg)

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 11111))
    s.listen()
    (conn, addr) = s.accept() 
    thread1 = threading.Thread(target = connect, args = ([conn]))
    thread2 = threading.Thread(target = sendMsg, args = ([conn]))
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()