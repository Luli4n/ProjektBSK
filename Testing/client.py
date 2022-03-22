import sys
import socket
import threading

def connect(s):
    while True:
        r_msg = s.recv(1024)
        if not r_msg:
            break
        if r_msg == '':
            pass
        else:
            print(r_msg.decode())

def receive(s):
    while True:
        s_msg = input().replace('b', '').encode('utf-8')
        if s_msg == '':
            pass
        if s_msg.decode() == 'exit':
            print("wan exit")
            break
        else:
            s.sendall(s_msg)

if __name__ == '__main__':

    connected = False
    while not connected:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(('',11111))
            connected = True
        except Exception as e:
            print(e)
            s.close()
            pass #Do nothing, just try again
    
    print('dupa')
    thread1 = threading.Thread(target = connect, args = ([s]))
    thread2 = threading.Thread(target = receive, args = ([s]))
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()