import struct
import os
import shutil

def print_eocd_structure(eocd_content):
    print('\nEOCD STRUCTURE')
    print('Signature:', eocd_content[0])
    print('Disk number:', eocd_content[1])
    print('Disk with EOCD:', eocd_content[2])
    print('Number of entries:', eocd_content[3])
    print('Total entries:', eocd_content[4])
    print('CD size:', eocd_content[5])
    print('CD offset:', eocd_content[6])
    print('Comment length:', eocd_content[7])

def print_cd_info(cd_content):
    for i in range(cd_content[0]):
        print('\nCENTRAL DIRECTORY FILE %s HEADER' % (i+1))
    
        print('Signature:', cd_content[1][i])
        print('Version made by:', cd_content[2][i])
        print('Version to extract:', cd_content[3][i])
        print('Flag:', cd_content[4][i])
        print('Compression method:', cd_content[5][i])
        print('Modification time:', cd_content[6][i])
        print('Modification date:', cd_content[7][i])
        print('CRC-32:', cd_content[8][i])
        print('Compressed size:', cd_content[9][i])
        print('Uncompressed size:', cd_content[10][i])
        print('Filename length:', cd_content[11][i])
        print('Additional field length:', cd_content[12][i])
        print('Comment file length:', cd_content[13][i])
        print('Disc number:', cd_content[14][i])
        print('Internal file attributes:', cd_content[15][i])
        print('External file attributes:', cd_content[16][i])
        print('Local file header offset:', cd_content[17][i])
        print('Filename:', cd_content[18][i])
        print('Additional field:', cd_content[19][i])
        print('Comment file:', cd_content[20][i])

def provide_archive_info(FILENAME):
    with open(FILENAME, 'rb') as zip_file:
        zip_file.seek(-22, 2)
        eocd_data = zip_file.read()

        if eocd_data[0:4] != b'\x50\x4b\x05\x06':
            raise Exception('Invalid EOCD signature')
    
        signature, disk_number, disk_with_eocd, num_of_entries, total_entries, \
            cd_size, cd_offset, comment_len = struct.unpack("<4s4H2LH", eocd_data)
        
        eocd_content = (signature, disk_number, disk_with_eocd, num_of_entries, \
            total_entries, cd_size, cd_offset, comment_len)

        current_offset = 0
        signature_cd = []
        version_made_by = []
        version_to_extract = []
        flag = []
        compression_method = []
        modification_time = []
        modification_date = []
        crc_32 = []
        compressed_size = []
        uncompressed_size = []
        filename_length = []
        additional_field_length = []
        comment_file_length = []
        disk_cd_number = []
        internal_file_attriburtes = []
        external_file_attributes = []
        local_file_header_offset = []
        filenames_in_archive = []
        additional_fields = []
        comment_files = []
    
        for i in range(total_entries):
            #possible to made with struct?
            zip_file.seek(cd_offset + current_offset)

            signature_cd.append(struct.unpack('I', zip_file.read(4))[0])
            version_made_by.append(struct.unpack('H', zip_file.read(2))[0])
            version_to_extract.append(struct.unpack('H', zip_file.read(2))[0])
            flag.append(struct.unpack('H', zip_file.read(2))[0])
            compression_method.append(struct.unpack('H', zip_file.read(2))[0])
            modification_time.append(struct.unpack('H', zip_file.read(2))[0])
            modification_date.append(struct.unpack('H', zip_file.read(2))[0])
            crc_32.append(struct.unpack('I', zip_file.read(4))[0])
            compressed_size.append(struct.unpack('I', zip_file.read(4))[0])
            uncompressed_size.append(struct.unpack('I', zip_file.read(4))[0])
            filename_length.append(struct.unpack('H', zip_file.read(2))[0])
            additional_field_length.append(struct.unpack('H', zip_file.read(2))[0])
            comment_file_length.append(struct.unpack('H', zip_file.read(2))[0])
            disk_cd_number.append(struct.unpack('H', zip_file.read(2))[0])
            internal_file_attriburtes.append(struct.unpack('H', zip_file.read(2))[0])
            external_file_attributes.append(struct.unpack('I', zip_file.read(4))[0])
            local_file_header_offset.append(struct.unpack('I', zip_file.read(4))[0])
            filenames_in_archive.append(zip_file.read(filename_length[-1]).decode())
            additional_fields.append(zip_file.read(additional_field_length[-1]))
            comment_files.append(zip_file.read(comment_file_length[-1]).decode())
    
            current_offset += filename_length[-1] + additional_field_length[-1] + 46

        cd_content = (total_entries, signature_cd, \
            version_made_by, version_to_extract, flag, compression_method, \
                modification_time, modification_date, crc_32, compressed_size, \
                    uncompressed_size, filename_length, additional_field_length, \
                        comment_file_length, disk_cd_number, internal_file_attriburtes, \
                                external_file_attributes, local_file_header_offset, \
                                    filenames_in_archive, additional_fields, comment_files)

        return eocd_content, cd_content


def show_content(FILENAME):
    eocd_content, cd_content = provide_archive_info(FILENAME)

    print_eocd_structure(eocd_content)
    print_cd_info(cd_content)

    print('\nAll of the filenames:', cd_content[18])

def delete_file_from_archive(cd_content, file_to_delete, OUT_FILENAME='result'):
    if file_to_delete not in filenames_in_archive: 
        raise Exception('Wrong filename')

    shutil.unpack_archive(FILENAME, 'temp')
    os.remove('temp/%s' % file_to_delete)
    shutil.make_archive(OUT_FILENAME, 'zip', 'temp')
    shutil.rmtree('temp')
    input('\nDeliting completed. Press any key to exit...')

def main():
    FILENAME = 'ex.zip'
    show_content(FILENAME)
    #file_to_delete = input('\nEnter filename to delete: ')
    #delete_file_from_archive(provide_archive_info(FILENAME), file_to_delete, )

if __name__ == '__main__':
    main()