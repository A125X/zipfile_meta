import socket
import sys
import zlib
import crc

def run_client():
    HOST = 'localhost' 
    PORT = 12345 
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    client_socket.connect((HOST, PORT))  
    filename = 'test.txt' 

    with open(filename, 'rb') as f: 
        file_content = f.read()
        poly = [1, 0, 0, 0, 0, 0, 1, 1, 1]
        n = 6
        file_crc , time = crc.calculate_crc8(file_content, n, poly)
        print('CRC8 = ', file_crc, 'Time = ', time)

        client_socket.sendall(file_content)
        data = client_socket.recv(1024)
        server_crc = int.from_bytes(data, byteorder=sys.byteorder)  
        if file_crc == server_crc: 
            print('CRC совпадает') 
            print(file_crc)
        else: 
            print('CRC не совпадает')  
            print(file_crc, server_crc)
    
    client_socket.close() 

if __name__ == '__main__':
    run_client()