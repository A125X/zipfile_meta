import zlib
import struct

def binary(FILENAME):
    bin_file = bytearray(open(FILENAME, 'rb').read())
    print(bin_file)
    return bin_file
def answer(bin_file):
    sum = zlib.crc32(bin_file)
    return sum
def crc(bin_file):
    polynom=100000100110000010001110110110111
    return

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
    print('Control sim is equal to ')
    print(answer(BIN_FILE))
    print('\nOur answer is ')
    print(calculate_crc32(BIN_FILE))
    input('\nProgram finished. Press any key to exit...')

if __name__ == '__main__':
    main()
