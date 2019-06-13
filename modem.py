# An implementation of a 300 Baud Modem

import goertzel
import scipy.io.wavfile as wav
import numpy as np
import sys

if __name__ == "__main__":

    if len(sys.argv) > 1:
        file_name = sys.argv[1]
    else:
        print("No file defined . . . Please supply a file name")
        sys.exit("No file defined")

    block_size = 160
    mark = 2225  # Bit 1
    space = 2025  # Bit 0

    file = wav.read(file_name)
    sample_rate = file[0]
    samples = np.interp(file[1], [0, max(file[1])], [0.0, 1.0])  # Normalize to 0.0-1.0
    blocks = np.array_split(samples, len(samples)/160)  # Split samples into {block_size} blocks

    print(f'File Name: {file_name}\nSample Rate: {sample_rate}\nSamples: {len(samples)}\nBlocks: {len(blocks)}\n')

    # Initialize the 'mark' and 'space' goertzel filters
    goertzel_filter_mark = goertzel.Goertzel(sample_rate, block_size, mark)
    goertzel_filter_space = goertzel.Goertzel(sample_rate, block_size, space)

    # Set up a list to store our filtered assembled bytes
    modem_output = []

    for current_block in range(0, len(blocks), 10):

        filter_output = []

        # filter the {blocks} of samples in groups of 10
        for x in range(0, 10):
            goertzel_filter_mark.filter(blocks[current_block + x])
            goertzel_filter_space.filter(blocks[current_block + x])

            if goertzel_filter_mark > goertzel_filter_space:
                filter_output.append('1')
            else:
                filter_output.append('0')

        filter_output.reverse()  # Reverse the array (convert to 'little' endian)
        filter_output = filter_output[1:-1]  # Chop of the first and last bit
        modem_output.append(chr(int(''.join(filter_output), 2)))  # Byte -> int -> ascii

    print('Modem Output:')
    for ascii_output in modem_output:
        print(ascii_output, end='')
