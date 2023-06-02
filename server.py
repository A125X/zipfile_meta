import socket
import sys
import crc
import threading

def recvall(sock):
    BUFF_SIZE = 4096 # 4 KiB
    data = b''
    while True:
        part = sock.recv(BUFF_SIZE)
        data += part
        if len(part) < BUFF_SIZE:
            # either 0 or end of data
            break
    return data

def do(sock):
    print('Connect')
    file_content = recvall(sock)
    print('File received')

    poly = [1, 0, 0, 0, 0, 0, 1, 1, 1]
    n = 6
    file_crc , time = crc.calculate_crc8(file_content, n, poly)
    sock.sendall(file_crc.to_bytes(4, byteorder=sys.byteorder))
    sock.close() 
    
def run_server():
    HOST = 'localhost'
    PORT = 12345
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(10)
    print('Working...')
    while True:
        client_socket, addr = server_socket.accept()
        thread = threading.Thread(target=do, args=(client_socket,), daemon=True)
        thread.start()


def main():
    text='hello world'.encode('utf-8')
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('127.0.0.1', 8080)
    server.bind(server_address)
    server.listen(10)
    
    client_socket, adress = server.accept()
    data = client_socket.recv(1024).decode('utf-8')
    #print(type(data))

    HDRS = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'
    content = 'done'.encode('utf-8')    
    client_socket.send(HDRS.encode('utf-8') + content)
    print('shut down')

if __name__ == '__main__':
    run_server()