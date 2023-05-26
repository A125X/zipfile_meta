import zlib
import threading
from time import time
import sys

def decorator_timer(func):
    def wrapper(*args, **kwargs):
        t1 = time()
        result = func(*args, **kwargs)
        return result, time()-t1

    return wrapper

def binary(FILENAME):
    bin_file = bytearray(open(FILENAME, 'rb').read())
    return bin_file

@decorator_timer
def answer(bin_file):
    sum = zlib.crc32(bin_file)
    return sum

def calculate_crc(data, table, crc, results):
    for byte in data:
        crc = table[(crc ^ byte) & 0xFF] ^ (crc >> 8)
    results.append(crc)

def access_bit(data, num):
    base = int(num // 8)
    shift = int(num % 8)
    return (data[base] >> shift) & 0x1

@decorator_timer
def calculate_crc32(data, threads_number):
    '''
    # Pre-compute the table of CRC32 remainders using the polynomial 0xEDB88320
    table = [0] * 256
    for i in range(256):
        crc = i
        for j in range(8):
            if crc & 1:
                crc = 0xEDB88320 ^ (crc >> 1)
            else:
                crc = crc >> 1
        table[i] = crc
    
    crc = 0xFFFFFFFF
    chunk_size = len(data) // threads_number
    threads = []
    results = []
    for i in range(threads_number):
        chunk_start = i * chunk_size
        chunk_end = (i + 1) * chunk_size
        chunk_data = data[chunk_start:chunk_end]
        thread = threading.Thread(target=calculate_crc, args=(chunk_data, table, crc, results))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    for n in results:
        print(n ^ 0xFFFFFFFF)

    return crc ^ 0xFFFFFFFF
    '''
    data = [access_bit(data,i) for i in range(len(data)*8)]
    
    poly = [1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, \
        0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1]

    div = []
    i = 0
    while(True):
        while data[i] == 0:
            i = i + 1
    
            if i >= len(data):
                return 0
    
            if i >= len(data)-33:
                div = data[len(data)-33:]
                return div
    
        for j in range(33):
            data[i+j] = data[i+j] ^ poly[j]
            div[j] = data[i+j]

    return div

def main():
    FILENAME = 'help.txt'
    BIN_FILE=binary(FILENAME)
    
    result, time = answer(BIN_FILE)
    print('Control sum is:', result)
    print('Control time:', time)
    
    #result, time = calculate_crc32(BIN_FILE, int(input('Enter number of threads: ')))
    result, time = calculate_crc32(BIN_FILE, 2)
    print('\nOur answer is: ', result)
    print('Answer time:', time)

    input('\nProgram finished. Press any key to exit...')

if __name__ == '__main__':
    main()
