import os
import math
import sys

def load_file(file_path: str) -> bytes:
    with open(file_path, 'rb') as file:
        return file.read()

def save_file(file_path: str, data: bytes) -> None:
    dir_name = os.path.dirname(file_path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    with open(file_path, 'wb') as file:
        file.write(data)

def create_initial_dict() -> tuple:
    """Creates the initial 256-byte dictionary."""
    base_dic = {bytes([i]): i for i in range(256)}
    inverse_dic = {i: bytes([i]) for i in range(256)}
    return base_dic, inverse_dic, 256

def lzw_compress(data: bytes, max_dic_size: float) -> tuple:
    dic, _, next_code = create_initial_dict()
    
    if not data:
        return b"", 0, 0
        
    sequence = bytes([data[0]])
    compressed_data = []

    for byte in data[1:]:
        extended_sequence = sequence + bytes([byte])
        if extended_sequence in dic:
            sequence = extended_sequence
        else:
            compressed_data.append(dic[sequence])
            if len(dic) < max_dic_size:
                dic[extended_sequence] = next_code
                next_code += 1
            sequence = bytes([byte])
    
    compressed_data.append(dic[sequence])
    
    # Calculate bits needed to represent the largest code
    bits_per_code = math.ceil(math.log2(next_code))
    
    # Convert codes to a single bitstring
    bitstring = ''.join(format(code, f'0{bits_per_code}b') for code in compressed_data)
    padding_length = (8 - len(bitstring) % 8) % 8
    bitstring += '0' * padding_length

    # Convert bitstring to bytearray
    byte_array = bytearray(int(bitstring[i:i + 8], 2) for i in range(0, len(bitstring), 8))
    
    return bytes(byte_array), bits_per_code, padding_length

def lzw_decompress(compressed_bytes: bytes, bits_per_code: int, max_dic_size: float, padding_length: int) -> bytes:
    _, reverse_dic, next_code = create_initial_dict()
    
    if not compressed_bytes:
        return b""
        
    bitstring = ''.join(format(byte, '08b') for byte in compressed_bytes)
    
    if padding_length > 0:
        bitstring = bitstring[:-padding_length]

    if len(bitstring) == 0:
        print("Warning: Bitstring length is zero after removing padding.")
        return b""

    codes = [int(bitstring[i:i + bits_per_code], 2) for i in range(0, len(bitstring), bits_per_code)]

    if len(codes) == 0:
        print("Warning: No codes found in the bitstring.")
        return b""

    previous_code = codes[0]
    decompressed_data = bytearray(reverse_dic[previous_code])
    sequence = reverse_dic[previous_code]

    for code in codes[1:]:
        if code in reverse_dic:
            current_sequence = reverse_dic[code]
        else:
            current_sequence = sequence + bytes([sequence[0]])
        
        decompressed_data.extend(current_sequence)
        
        if len(reverse_dic) < max_dic_size:
            new_sequence = sequence + bytes([current_sequence[0]])
            reverse_dic[next_code] = new_sequence
            next_code += 1
        
        sequence = current_sequence

    return bytes(decompressed_data)

def process_file(filepath: str, dic_limits: dict) -> dict:
    size_results = {}
    data = load_file(filepath)
    filename = os.path.basename(filepath)
    name, extension = os.path.splitext(filename)

    print(f"\n--- Processing: {filename} ---")
    original_size = len(data)
    print(f"Original size: {original_size} bytes")

    for key, limit in dic_limits.items():
        print(f"  Compressing with dict limit: 2^{key} ...")
        
        # Compress
        compressed_data, bit_length, padding_length = lzw_compress(data, limit)
        encoded_path = f'output/encoded/{name}_{key}.bin'
        save_file(encoded_path, compressed_data)

        # Decompress
        decompressed_data = lzw_decompress(compressed_data, bit_length, limit, padding_length)
        decoded_path = f'output/decoded/{name}_{key}{extension}'
        save_file(decoded_path, decompressed_data)

        # Verification
        is_identical = (data == decompressed_data)
        
        # Stats
        compressed_size = os.path.getsize(encoded_path)
        size_results[key] = compressed_size
        compression_ratio = compressed_size / original_size if original_size > 0 else 0
        
        print(f"    Verification (Orig == Decoded): {is_identical}")
        print(f"    Compressed size: {compressed_size} bytes (Ratio: {compression_ratio:.4f})")
    
    return size_results

def print_statistics(statistics: dict) -> None:
    print("\n=== Final Size Statistics ===")
    for file, sizes in statistics.items():
        print(f"File: {file}")
        for key, size in sizes.items():
            print(f"  Dict limit 2^{key}: {size} bytes")

def main():
    files_to_process = [
        'data/norm_wiki_sample.txt', 
        'data/cat.png'
    ]
    
    limits = {
        '12': 2 ** 12, 
        '18': 2 ** 18, 
        'max': float('inf') 
    }

    compression_results = {}
    
    for filepath in files_to_process:
        if os.path.exists(filepath):
            compression_results[os.path.basename(filepath)] = process_file(filepath, limits)
        else:
            print(f"\nError: File '{filepath}' not found. Skipping.")

    print_statistics(compression_results)

if __name__ == '__main__':
    main()