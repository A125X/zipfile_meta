import threading
from time import time

def decorator_timer(func):
    def wrapper(*args, **kwargs):
        t1 = time()
        result = func(*args, **kwargs)
        return result, time()-t1

    return wrapper
 
def binary(FILENAME):
    bin_file = bytearray(open(FILENAME, 'rb').read())
    return bin_file

def int_to_bin(n):
    if n>255 or n<0:
        raise Exception('Data is not 8-bit number')
    f = [0]*8
    for i in range(8):
        if n >= (2**(7-i)):
            n = n-2**(7-i)
            f[i] = 1
    return f

def bin_to_int(f):
    n = 0
    for i in range(8):
        if f[i] == 1:
            n = n+2**(7-i)

    return n

def sum(f, g):
    if len(f) != len(g):
        raise Exception('Operation not determined')
    else:
        for i in range(len(f)):
            f[i] = f[i]^g[i]
        return f

def mod(data, poly):
        deg = len(poly)
        div = [None]*(deg-1)
        i = 0
        while(True):
            while (data[i] == 0):
                i = i + 1
                if i == (len(data)):
                    break
    
            if i >= len(data): 
                return [0]*8
    
            if i > len(data)-deg:
                div = data[len(data)-deg+1:]
                return div
            for j in range(deg):
                data[i+j] = data[i+j] ^ poly[j]

def shift(f, n, m):
    h = [0]*m
    for i in range(len(f)):
        h[m-n-1-i] = f[len(f)-1-i]
    return h
 
def polymult(f, g):
    d = len(f) + len(g) - 1
    f = shift(f, 0 ,d)
    h = [0]*d

    for i in range(len(g)):
        if g[len(g)-1-i] == 1:
            h = sum(h, shift(f, i, d))
    return h

def polypow(f, n):
    g = f
    for i in range(1, n):
        f = polymult(f, g)
    return f

def glue(results, lenght, threads_number, poly, remainder):
    for i in range(threads_number):
        results[i] = int_to_bin(results[i])
    f = [0]*(8*remainder+1)
    f[0] = 1
    g = [0]*(8*lenght+1)
    g[0] = 1
    f = mod(f, poly)
    g = mod(g, poly)

    for i in range(2, threads_number):
        results[threads_number-1-i] = mod(polymult(results[threads_number-1-i], polypow(g, i-1)), poly)
    ans = [0]*8
    for i in range(threads_number-1):
        ans = sum(ans, results[i])
    ans = sum(results[threads_number-1], mod(polymult(ans, f), poly))
    return bin_to_int(ans)

def calculate_crc(data, table, crc, results, i):
    for byte in data:
        crc = table[(crc ^ byte) & 0xFF] ^ (crc >> 8)
    results.append((crc, i))
#Надо на всякий случай отсортировать список
@decorator_timer
def calculate_crc8(data, threads_number, poly):
    table = [0x00, 0x07, 0x0e, 0x09, 0x1c, 0x1b, 0x12, 0x15, 
             0x38, 0x3f, 0x36, 0x31, 0x24, 0x23, 0x2a, 0x2d, 
             0x70, 0x77, 0x7e, 0x79, 0x6c, 0x6b, 0x62, 0x65, 
             0x48, 0x4f, 0x46, 0x41, 0x54, 0x53, 0x5a, 0x5d, 
             0xe0, 0xe7, 0xee, 0xe9, 0xfc, 0xfb, 0xf2, 0xf5, 
             0xd8, 0xdf, 0xd6, 0xd1, 0xc4, 0xc3, 0xca, 0xcd, 
             0x90, 0x97, 0x9e, 0x99, 0x8c, 0x8b, 0x82, 0x85, 
             0xa8, 0xaf, 0xa6, 0xa1, 0xb4, 0xb3, 0xba, 0xbd, 
             0xc7, 0xc0, 0xc9, 0xce, 0xdb, 0xdc, 0xd5, 0xd2, 
             0xff, 0xf8, 0xf1, 0xf6, 0xe3, 0xe4, 0xed, 0xea, 
             0xb7, 0xb0, 0xb9, 0xbe, 0xab, 0xac, 0xa5, 0xa2, 
             0x8f, 0x88, 0x81, 0x86, 0x93, 0x94, 0x9d, 0x9a, 
             0x27, 0x20, 0x29, 0x2e, 0x3b, 0x3c, 0x35, 0x32, 
             0x1f, 0x18, 0x11, 0x16, 0x03, 0x04, 0x0d, 0x0a, 
             0x57, 0x50, 0x59, 0x5e, 0x4b, 0x4c, 0x45, 0x42, 
             0x6f, 0x68, 0x61, 0x66, 0x73, 0x74, 0x7d, 0x7a, 
             0x89, 0x8e, 0x87, 0x80, 0x95, 0x92, 0x9b, 0x9c, 
             0xb1, 0xb6, 0xbf, 0xb8, 0xad, 0xaa, 0xa3, 0xa4, 
             0xf9, 0xfe, 0xf7, 0xf0, 0xe5, 0xe2, 0xeb, 0xec, 
             0xc1, 0xc6, 0xcf, 0xc8, 0xdd, 0xda, 0xd3, 0xd4, 
             0x69, 0x6e, 0x67, 0x60, 0x75, 0x72, 0x7b, 0x7c, 
             0x51, 0x56, 0x5f, 0x58, 0x4d, 0x4a, 0x43, 0x44, 
             0x19, 0x1e, 0x17, 0x10, 0x05, 0x02, 0x0b, 0x0c, 
             0x21, 0x26, 0x2f, 0x28, 0x3d, 0x3a, 0x33, 0x34, 
             0x4e, 0x49, 0x40, 0x47, 0x52, 0x55, 0x5c, 0x5b, 
             0x76, 0x71, 0x78, 0x7f, 0x6a, 0x6d, 0x64, 0x63, 
             0x3e, 0x39, 0x30, 0x37, 0x22, 0x25, 0x2c, 0x2b, 
             0x06, 0x01, 0x08, 0x0f, 0x1a, 0x1d, 0x14, 0x13, 
             0xae, 0xa9, 0xa0, 0xa7, 0xb2, 0xb5, 0xbc, 0xbb, 
             0x96, 0x91, 0x98, 0x9f, 0x8a, 0x8d, 0x84, 0x83, 
             0xde, 0xd9, 0xd0, 0xd7, 0xc2, 0xc5, 0xcc, 0xcb, 
             0xe6, 0xe1, 0xe8, 0xef, 0xfa, 0xfd, 0xf4, 0xf3]
    
    crc = 0
    chunk_size = len(data) // threads_number
    remainder = len(data) - chunk_size*(threads_number-1)
    threads = []
    results = []
    for i in range(threads_number):
        if i == threads_number-1:
            chunk_start = i * chunk_size
            chunk_data = data[chunk_start:]
        else:
            chunk_start = i * chunk_size
            chunk_end = (i + 1) * chunk_size
            chunk_data = data[chunk_start:chunk_end]
        thread = threading.Thread(
            target=calculate_crc, 
            args=(chunk_data, table, crc, results, i))
        thread.start()
        threads.append(thread)
        for thread in threads:
            thread.join()

    #print(results)
    results.sort(key=lambda x: x[1])
    results = [n[0] for n in results]
    #print(results)

    crc = glue(results, chunk_size, threads_number, poly, remainder)
    return crc

def main():
    FILENAME = 'test.txt'
    BIN_FILE = binary(FILENAME)
    poly = [1, 0, 0, 0, 0, 0, 1, 1, 1]
    n = int(input('Enter number of threads '))
    result , time = calculate_crc8(BIN_FILE, n, poly)
    print('CRC8 = ', result, 'Time = ', time)
    input('\nProgram finished. Press any key to exit...')
if __name__ == '__main__':
    main()