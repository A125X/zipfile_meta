import struct
import os
import json

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

        current_offset = [0]
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
            zip_file.seek(cd_offset + current_offset[-1])

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
    
            current_offset.append(current_offset[-1]+filename_length[-1]+additional_field_length[-1]+46)

        cd_content = (total_entries, signature_cd, \
            version_made_by, version_to_extract, flag, compression_method, \
                modification_time, modification_date, crc_32, compressed_size, \
                    uncompressed_size, filename_length, additional_field_length, \
                        comment_file_length, disk_cd_number, internal_file_attriburtes, \
                                external_file_attributes, local_file_header_offset, \
                                    filenames_in_archive, additional_fields, comment_files, \
                                        current_offset)

        return eocd_content, cd_content

def show_content(FILENAME):
    eocd_content, cd_content = provide_archive_info(FILENAME)

    print_eocd_structure(eocd_content)
    print_cd_info(cd_content)

    print('\nAll of the filenames:', cd_content[18])

def delete_file_from_archive(FILENAME, file_to_delete, OUT_FILENAME='result.zip'):
    eocd_content, cd_content = provide_archive_info(FILENAME)

    if file_to_delete not in cd_content[18]: 
        raise Exception('Wrong filename')

    number_of_entries = len(cd_content[18])
    if number_of_entries == 1:
        raise Exception('Wrong length')

    file_to_delete_index = 0
    
    for i, val in enumerate(cd_content[18]):
        if val == file_to_delete:
            file_to_delete_index = i
            break
    
    if file_to_delete_index == len(cd_content[18]) - 1:
        file_to_delete_size = eocd_content[6] - cd_content[17][file_to_delete_index]
    else:
        file_to_delete_size = cd_content[17][file_to_delete_index+1]-cd_content[17][file_to_delete_index]
    file_to_delete_offset = cd_content[17][file_to_delete_index]
    cd_new_offset = eocd_content[6] - file_to_delete_size
    file_to_delete_cd_offset = cd_new_offset + cd_content[-1][file_to_delete_index]
    file_to_delete_cd_offset_new = cd_new_offset + cd_content[-1][file_to_delete_index+1]
    
    #changing eocd
    source = bytearray(open(FILENAME, 'rb').read())
    
    source[-14:-12] = struct.pack('H', number_of_entries-1)
    source[-12:-10] = struct.pack('H', number_of_entries-1)
    source[-6:-2] = struct.pack('I', cd_new_offset)
    
    #changing cd file offsets info
    for i in range(file_to_delete_index+1, len(cd_content[18])):
        offset = eocd_content[6] + cd_content[-1][i]
        print('offset %i ==' % i, cd_content[-1][i], cd_content[18][i], cd_content[17][i]-file_to_delete_size)
        source[offset+42:offset+46] = \
            struct.pack('I', cd_content[17][i]-file_to_delete_size)
    
    #deleting file
    source[file_to_delete_offset:] = source[file_to_delete_offset+file_to_delete_size:]
    #deleting cd header
    source[file_to_delete_cd_offset:] = source[file_to_delete_cd_offset_new:]

    #writing info to the file
    with open(OUT_FILENAME, 'wb') as zip_file:
        zip_file.write(source)

def provide_json_archive_info(FILENAME, JSON_NAME='info.json'):
    eocd_content, cd_content = provide_archive_info(FILENAME)

    data = {
    'EOCD signature': str(eocd_content[0]),
    'EOCD disk number': eocd_content[1],
    'Disk with EOCD' : eocd_content[2],
    'Number of entries' : eocd_content[3],
    'Total entries' : eocd_content[4],
    'CD size' : eocd_content[5],
    'CD offset' : eocd_content[6],
    'EOCD comment length' : eocd_content[7]}

    for i in range(cd_content[0]):
        data[f'Central directory file {i+1} signature'] = cd_content[1][i]
        data[f'Central directory file {i+1} version made by'] = cd_content[2][i]
        data[f'Central directory file {i+1} version to extract'] = cd_content[3][i]
        data[f'Central directory file {i+1} flag'] = cd_content[4][i]
        data[f'Central directory file {i+1} compression method'] = cd_content[5][i]
        data[f'Central directory file {i+1} modification time'] = cd_content[6][i]
        data[f'Central directory file {i+1} modification date'] = cd_content[7][i]
        data[f'Central directory file {i+1} CRC-32'] = cd_content[8][i]
        data[f'Central directory file {i+1} compressed size'] = cd_content[9][i]
        data[f'Central directory file {i+1} uncompressed size'] = cd_content[10][i]
        data[f'Central directory file {i+1} filename length'] = cd_content[11][i]
        data[f'Central directory file {i+1} additional field length'] = cd_content[12][i]
        data[f'Central directory file {i+1} comment file length'] = cd_content[13][i]
        data[f'Central directory file {i+1} disc number'] = cd_content[14][i]
        data[f'Central directory file {i+1} internal file attributes'] = cd_content[15][i]
        data[f'Central directory file {i+1} external file attributes'] = cd_content[16][i]
        data[f'Central directory file {i+1} local file header offset'] = cd_content[17][i]
        data[f'Central directory file {i+1} filename'] = cd_content[18][i]
        data[f'Central directory file {i+1} additional field'] = str(cd_content[19][i])
        data[f'Central directory file {i+1} comment file'] = cd_content[20][i]

    with open(JSON_NAME, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def main():
    FILENAME = 'ex.zip'
    #OUT_FILENAME = 'result.zip'
    show_content(FILENAME)
    #file_to_delete = input('\nEnter filename to delete: ')
    #file_to_delete = 'pic1.jpg'
    #delete_file_from_archive(FILENAME, file_to_delete, OUT_FILENAME)
    #show_content(OUT_FILENAME)
    provide_json_archive_info(FILENAME)
    input('\nProgram finished. Press any key to exit...')

if __name__ == '__main__':
    main()