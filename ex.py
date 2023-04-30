import struct
import os
import shutil

def print_eocd_structure(signature, disk_number, disk_with_eocd, num_of_entries, total_entries, \
            cd_size, cd_offset, comment_len):
    print('EOCD STRUCTURE')
    print('Signature:', signature)
    print('Disk number:', disk_number)
    print('Disk with EOCD:', disk_with_eocd)
    print('Number of entries:', num_of_entries)
    print('Total entries:', total_entries)
    print('CD size:', cd_size)
    print('CD offset:', cd_offset)
    print('Comment length:', comment_len)

def show_content(FILENAME):
    filenames_in_archive = []

    with open(FILENAME, 'rb') as zip_file:
        # Считываем структуру EOCD
        zip_file.seek(-22, 2)
        eocd_data = zip_file.read()
        # Check the EOCD signature
        if eocd_data[0:4] != b'\x50\x4b\x05\x06':
            raise Exception('Invalid EOCD signature')
    
        signature, disk_number, disk_with_eocd, num_of_entries, total_entries, \
            cd_size, cd_offset, comment_len = struct.unpack("<4s4H2LH", eocd_data)

        print_eocd_structure(signature, disk_number, disk_with_eocd, \
            num_of_entries, total_entries, cd_size, cd_offset, comment_len)
        
        current_offset = 0
    
        # Читаем локальные заголовочные файлы
        for i in range(total_entries):
            # Считываем данные из центрального каталога (CD)
            zip_file.seek(cd_offset + current_offset)
        
            print('\nCENTRAL DIRECTORY FILE %s HEADER' % (i+1))

            print('Signature:', struct.unpack('I', zip_file.read(4))[0])
            print('Version made by:', struct.unpack('H', zip_file.read(2))[0])
            print('Version to extract:', struct.unpack('H', zip_file.read(2))[0])
            print('Flag:', struct.unpack('H', zip_file.read(2))[0])
            print('Compression method:', struct.unpack('H', zip_file.read(2))[0])
            print('Modification time:', struct.unpack('H', zip_file.read(2))[0])
            print('Modification date:', struct.unpack('H', zip_file.read(2))[0])
            print('CRC-32:', struct.unpack('I', zip_file.read(4))[0])
            print('Compressed size:', struct.unpack('I', zip_file.read(4))[0])
            print('Uncompressed size:', struct.unpack('I', zip_file.read(4))[0])
            filename_length = struct.unpack('H', zip_file.read(2))[0]
            print('Filename length:', filename_length)
            additional_field_length = struct.unpack('H', zip_file.read(2))[0]
            print('Additional field length:', additional_field_length)
            comment_file_length = struct.unpack('H', zip_file.read(2))[0]
            print('Comment file length:', comment_file_length)
            print('Disc number:', struct.unpack('H', zip_file.read(2))[0])
            print('Internal file attributes:', struct.unpack('H', zip_file.read(2))[0])
            print('External file attributes:', struct.unpack('I', zip_file.read(4))[0])
            print('Local file header offset:', struct.unpack('I', zip_file.read(4))[0])

            filename = zip_file.read(filename_length).decode()
            print('Filename:', filename)
            additional_field = zip_file.read(filename_length)
            print('Additional field:', additional_field)
            comment_file = zip_file.read(comment_file_length).decode()
            print('Comment file:', comment_file)
    
            current_offset += filename_length + additional_field_length + 46
            filenames_in_archive.append(filename)

        return filenames_in_archive

def delete_file_from_archive(FILENAME, file_to_delete, filenames_in_archive, OUT_FILENAME='deleted.zip'):    
    if file_to_delete not in filenames_in_archive: 
        raise Exception('Wrong filename')

    shutil.copy2(FILENAME, OUT_FILENAME)

    with open(OUT_FILENAME, 'rb') as zip_file:
        # Считываем структуру EOCD
        zip_file.seek(-22, 2)
        eocd_data = zip_file.read()
        # Check the EOCD signature
        if eocd_data[0:4] != b'\x50\x4b\x05\x06':
            raise Exception('Invalid EOCD signature')
    
        signature, disk_number, disk_with_eocd, num_of_entries, total_entries, \
            cd_size, cd_offset, comment_len = struct.unpack("<4s4H2LH", eocd_data)

        print_eocd_structure(signature, disk_number, disk_with_eocd, \
            num_of_entries, total_entries, cd_size, cd_offset, comment_len)
        
        current_offset = 0
    
        # Читаем локальные заголовочные файлы
        for i in range(total_entries):
            # Считываем данные из центрального каталога (CD)
            zip_file.seek(cd_offset + current_offset)

def main():
    FILENAME = 'ex.zip'
    filenames_in_archive = show_content(FILENAME)
    print('\nAll of the filenames:', filenames_in_archive)
    file_to_delete = 'pic1.jpg'
    #file_to_delete = input('\nEnter filename to delete: ')
    delete_file_from_archive(FILENAME, file_to_delete, filenames_in_archive)
    input()

if __name__ == '__main__':
    main()