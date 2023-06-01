import socket
import os 
import zlib  

def run_server():
    # Создаем сокет и начинаем слушать порт 
    HOST = '' 
    PORT = 12345 
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    server_socket.bind((HOST, PORT)) 
    server_socket.listen(1)  
    # Принимаем соединение от клиента 
    client_socket, addr = server_socket.accept()  
    # Получаем файл от клиента 
    data = client_socket.recv(1024) 
    file_content = data 
    while data: 
        data = client_socket.recv(1024) 
        file_content += data  
        # Вычисляем CRC файла 
        crc = zlib.crc32(file_content)  
        # Отправляем CRC клиенту 
        client_socket.sendall(crc.to_bytes(4, byteorder='big'))  

    # Закрываем соединение 
    client_socket.close() 
    server_socket.close()

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