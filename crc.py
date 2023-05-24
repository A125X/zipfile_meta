import zlib
import struct
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

@decorator_timer
def answer(bin_file):
    sum = zlib.crc32(bin_file)
    return sum

@decorator_timer
def calculate_crc32(data):
    # Pre-compute the table of CRC32 remainders using the polynomial 0xEDB88320
    crc_table = [0] * 256
    for i in range(256):
        crc = i
        for j in range(8):
            if crc & 1:
                crc = 0xEDB88320 ^ (crc >> 1)
            else:
                crc = crc >> 1
        crc_table[i] = crc

    # Calculate the CRC32 value of the provided data
    crc = 0xFFFFFFFF
    for byte in data:
        crc = crc_table[(crc ^ byte) & 0xFF] ^ (crc >> 8)
    return crc ^ 0xFFFFFFFF

def main():
    FILENAME = 'test.txt'
    BIN_FILE=binary(FILENAME)
    
    result, time = answer(BIN_FILE)
    print('Control sum is:', result)
    print('Control time:', time)
    
    result, time = calculate_crc32(BIN_FILE)
    print('\nOur answer is: ', result)
    print('Answer time:', time)

    input('\nProgram finished. Press any key to exit...')

if __name__ == '__main__':
    main()
