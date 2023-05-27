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

#Такую форму используем в calculate_crc32. 
def binary(FILENAME):
    bin_file = bytearray(open(FILENAME, 'rb').read())
    return bin_file

#Образцовая функция. Надо бы переделать под CRC8
#Но в целом, можно забить на это. Хотя надо бы сделать.
@decorator_timer
def answer(bin_file):
    sum = zlib.crc32(bin_file)
    return sum

def calculate_crc(data, table, crc, results):
    for byte in data:
        crc = table[(crc ^ byte) & 0xFF] ^ (crc >> 8)
    results.append(crc^ 0xFFFFFFFF)

#Пока что это функция возвращает только 0. Но главное не это
#Главное, что эта функция записывает в results CRC частей
@decorator_timer
def calculate_crc32(data, threads_number):
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
        if i == threads_number-1:
            chunk_start = i * chunk_size
            chunk_data = data[chunk_start:]
        else:
            chunk_start = i * chunk_size
            chunk_end = (i + 1) * chunk_size
            chunk_data = data[chunk_start:chunk_end]
        thread = threading.Thread(target=calculate_crc, args=(chunk_data, table, crc, results))
        thread.start()
        threads.append(thread)
        for thread in threads:
            thread.join()
        return crc^0xFFFFFFFF

#Эта функция суммирует многочлены одной длины.
def sum(f,g):
    if len(f) != len(g):
        print('Wrong data')
        return -1
    else:
        for i in range(len(f)):
            f[i] = f[i]^g[i]
        return f

#Деление с остатком data на poly.
def mod(data, poly):
        deg = len(poly)
        div = [None]*(deg-1)
        i = 0
        while(True):
            while data[i] == 0:
                i = i + 1
    
            if i >= len(data):
                return 0
    
            if i > len(data)-deg:
                div = data[len(data)-deg+1:]
                return div
            for j in range(deg):
                data[i+j] = data[i+j] ^ poly[j]

#Функция умножает многочлен f на x^n и делает его запись длины m.
#По сути мы просто сдвигаем на n символов влево.
def shift(f, n, m):
    h = [0]*m
    for i in range(len(f)):
        h[m-n-1-i] = f[len(f)-1-i]
    return h

#Произведение многочленов. Алгоритм основан на том, что это просто билинейная формаю 
def polymult(f, g):
    d = len(f)+len(g)-1
    f = shift(f, 0 ,d)
    h = [0]*d

    for i in range(len(g)):
        if g[len(g)-1-i] == 1:
            h = sum(h, shift(f, i, d))
    return h

#Наконец, если умеем умножать, то легко возведем в степень
def polypow(f, n):
    g = f
    for i in range(1, n):
        f = polymult(f, g)
    return f

#ВСЕ! Написаны все функции, которые мне нужны, чтобы собрать crc из кусочков. 
#Вроде я проверил, они правильно работают
def main():
    FILENAME = 'help.txt'
    BIN_FILE = binary(FILENAME)
    data =[0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
    poly = [1, 0, 0, 0, 0, 0, 1, 1, 1]
    #result, time = calculate_crc32(BIN_FILE, int(input('Enter number of threads: ')))
    result = mod(data, poly)
    f = [1, 0, 0, 1, 1]
    print(f)
    g = [1, 1, 0, 1, 1, 0, 1, 0]
    print(g)
    h = polypow(f, 2)
    print(h)
    input('\nProgram finished. Press any key to exit...')

if __name__ == '__main__':
    main()