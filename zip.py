import struct
import os
import sys

def decode_zip_file():
    FILENAME = 'ex.zip'

    # Открываем файл в бинарном режиме
    with open(FILENAME, 'rb') as f:
        # Перемещаем указатель в конец файла
        f.seek(0, 2)
        # Получаем размер файла
        file_size = f.tell()
        # Устанавливаем указатель на 22 байта до конца файла
        f.seek(-22, 2)
        # Считываем EOCD запись
        eocd = f.read()
    
    # Разбираем EOCD запись
    signature, disk_number, disk_start, num_entries_disk, num_entries_total, \
        central_dir_size, central_dir_offset, comment_length = struct.unpack('<4s4H2LH', eocd)

    print(
        'EOCD INFO:',
        '\nSignature:', signature, 
        '\nDisk number:', disk_number,
        '\nDisk start:', disk_start,
        '\nNum entries disk:', num_entries_disk,
        '\nNum entries total:', num_entries_total,
        '\nCentral dir size:', central_dir_size,
        '\nCentral dir offset:', central_dir_offset,
        '\nComment length:', comment_length
        )

    zip_file = open(FILENAME, 'rb')
    
    if(os.stat(FILENAME).st_size < 30):
        print('Wrong size of the ZIP file')
        sys.exit()
        
    dict_zip_file_decode = {
        'Signature' : struct.unpack('I', zip_file.read(4)), 
        'Version' : struct.unpack('H', zip_file.read(2)),
        'Flag' : struct.unpack('H', zip_file.read(2)),
        'Compression method' : struct.unpack('H', zip_file.read(2)),
        'Last time modified' : struct.unpack('H', zip_file.read(2)),
        'Last time changed' : struct.unpack('H', zip_file.read(2)),
        'CRC-32' : struct.unpack('I', zip_file.read(4)),
        'Compressed size' : struct.unpack('I', zip_file.read(4)),
        'Uncompressed size' : struct.unpack('I', zip_file.read(4)),
        'Filename size' : struct.unpack('H', zip_file.read(2)),
        'Additional field size' : struct.unpack('H', zip_file.read(2))
    }

    print('\nFIRST FILE HEADER:')

    print('Signature:', dict_zip_file_decode['Signature'])
    print('Version: %s' % dict_zip_file_decode['Version'])
    print('Flag: %s' % dict_zip_file_decode['Flag'])
    print('Compression method: %s' % dict_zip_file_decode['Compression method'])
    print('Last time modified: %s' % dict_zip_file_decode['Last time modified'])
    print('Last time changed: %s' % dict_zip_file_decode['Last time changed'])
    print('CRC-32: %s' % dict_zip_file_decode['CRC-32'])
    print('Compressed size: %s' % dict_zip_file_decode['Compressed size'])
    print('Uncompressed size: %s' % dict_zip_file_decode['Uncompressed size'])
    filename_size = dict_zip_file_decode['Filename size']
    print('Filename size: %s' % filename_size)
    additional_field_size = dict_zip_file_decode['Additional field size']
    print('Additional field size: %s' % additional_field_size)
    print('Flag: %s' % dict_zip_file_decode['Flag'])
    filename = zip_file.read(filename_size[0]).decode()
    additional_field = zip_file.read(additional_field_size[0]).decode()
    print('Filename: %s' % filename)
    print('Additional field: %s' % additional_field)
    
    zip_file.close()

def main():
    decode_zip_file()

if __name__ == '__main__':
    main()