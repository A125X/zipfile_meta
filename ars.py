import struct

# Open the ZIP archive in binary mode
with open('ex.zip', 'rb') as file:
    # Seek to the end of the file and read the EOCD record
    file.seek(-22, 2)
    eocd = file.read(22)

    # Check the EOCD signature
    if eocd[0:4] != b'\x50\x4b\x05\x06':
        raise Exception('Invalid EOCD signature')

    # Get the number of entries in the central directory
    num_entries = struct.unpack('<H', eocd[10:12])[0]

    # Get the location of the start of the central directory
    central_dir_offset = struct.unpack('<I', eocd[16:20])[0]

    # Seek to the start of the central directory and read each central directory header
    file.seek(central_dir_offset, 0)
    for i in range(num_entries):
        central_dir_header = file.read(46)

        # Check the central directory header signature
        if central_dir_header[0:4] != b'\x50\x4b\x01\x02':
            raise Exception('Invalid central directory file header signature')

        # Get the file name and print it
        file_name_length = struct.unpack('<H', central_dir_header[28:30])[0]
        file_name = file.read(file_name_length).decode('utf-8')
        print(file_name)

        # Skip over the variable-length fields that we're not using in this example
        file.seek(12, 1)

        # Get the offset to the start of the file and print it
        relative_offset = struct.unpack('<I', central_dir_header[42:46])[0]
        print(relative_offset)