import socket
import os 
import zlib  

def run_client():
    # Устанавливаем соединение с сервером 
    HOST = 'localhost' 
    PORT = 12345 
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    client_socket.connect((HOST, PORT))  
    # Открываем файл для чтения 
    filename = 'test.txt' 
    with open(filename, 'rb') as f: 
    # Читаем содержимое файла 
        file_content = f.read()  
        # Вычисляем CRC файла 
        crc = zlib.crc32(file_content)  
        # Отправляем файл на сервер 
        client_socket.sendall(file_content)  
        # Получаем CRC файла от сервера 
        data = client_socket.recv(1024) 
        server_crc = int.from_bytes(data, byteorder='big')  
        # Сравниваем CRC на клиенте и сервере 
        if crc == server_crc: 
            print('CRC совпадает') 
        else: 
            print('CRC не совпадает')  
            # Закрываем соединение 
    
    client_socket.close() 

if __name__ == '__main__':
    run_client()