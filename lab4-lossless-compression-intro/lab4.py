import sys
import os
import pickle
import bitarray
from collections import Counter

# 37 supported characters: 26 letters + 10 digits + space
CHARACTERS = " abcdefghijklmnopqrstuvwxyz0123456789"

def read_file(filename: str) -> str:
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read().lower()

def calculate_char_frequency(text: str) -> dict:
    counter = Counter(char for char in text if char in CHARACTERS)
    total_chars = sum(counter.values())
    return {char: count / total_chars for char, count in counter.items()}

def create_codes(characters_freq: dict) -> dict:
    """Creates a fixed-length (6-bit) code for each character."""
    codes = {}
    code_value = 0
    # Sort by frequency descending
    sorted_chars = sorted(characters_freq.items(), key=lambda x: x[1], reverse=True)
    
    for char, _ in sorted_chars:
        # 2^6 = 64, which is enough to store 37 characters
        codes[char] = bin(code_value)[2:].zfill(6)
        code_value += 1
        
    return codes

def encode(text: str, codes: dict) -> bitarray.bitarray:
    """Encodes text into a bitarray using the provided codes."""
    encoded_bits = bitarray.bitarray()
    # Using string concatenation/join is faster before converting to bitarray
    encoded_str = "".join(codes[char] for char in text if char in codes)
    encoded_bits.extend(encoded_str)
    return encoded_bits

def decode(encoded_text: bitarray.bitarray, codes: dict) -> str:
    """Decodes a bitarray back into text."""
    reverse_codes = {code: char for char, code in codes.items()}
    decoded_text = []
    current_code = ""
    
    # Iterate over the binary string representation
    for bit in encoded_text.to01():
        current_code += bit
        if current_code in reverse_codes:
            decoded_text.append(reverse_codes[current_code])
            current_code = ""
            
    return "".join(decoded_text)

def save_data(codes: dict, encoded_text: bitarray.bitarray, filename: str) -> None:
    """Saves the codes, original bit length, and the bitarray to a file."""
    dir_name = os.path.dirname(filename)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
        
    with open(filename, 'wb') as file:
        # Save metadata (codes and exact bit length to avoid padding issues)
        metadata = {
            "codes": codes,
            "bit_length": len(encoded_text)
        }
        pickle.dump(metadata, file)
        encoded_text.tofile(file)

def load_data(filename: str) -> tuple:
    """Loads the codes and the unpadded bitarray from a file."""
    with open(filename, 'rb') as file:
        metadata = pickle.load(file)
        encoded_text = bitarray.bitarray()
        encoded_text.fromfile(file)
        
        # Trim the bitarray to its original length (remove byte padding)
        encoded_text = encoded_text[:metadata["bit_length"]]
        
    return metadata["codes"], encoded_text

def main(text_sample_path: str):
    print(f"--- TASK 1: Fixed-length coding (Symbol-by-symbol) ---")
    
    text_sample = read_file(text_sample_path)
    
    # 1. Create codes
    frequencies = calculate_char_frequency(text_sample)
    codes = create_codes(frequencies)
    
    # 2. Encode
    print("Encoding...")
    encoded_text = encode(text_sample, codes)
    
    # 3. Save
    output_bin_path = "output/encoded_data.bin"
    save_data(codes, encoded_text, output_bin_path)
    print(f"Data saved to: {output_bin_path}")
    
    # 4. Load & Decode
    print("Loading and decoding...")
    loaded_codes, loaded_encoded_text = load_data(output_bin_path)
    decoded_text = decode(loaded_encoded_text, loaded_codes)
    
    # 5. Verify
    is_identical = (text_sample == decoded_text)
    print(f"Verification (Original == Decoded): {is_identical}")
    
    # 6. Save decoded text
    output_decoded_path = "output/decoded_text.txt"
    with open(output_decoded_path, 'w', encoding='utf-8') as file:
        file.write(decoded_text)
    print(f"Decoded text saved to: {output_decoded_path}")
        
    # 7. Print stats
    original_size_bytes = len(text_sample.encode('utf-8'))
    compressed_size_bytes = os.path.getsize(output_bin_path)
    compression_ratio = compressed_size_bytes / original_size_bytes
    
    print("\n--- Statistics ---")
    print(f"Original file size:   {original_size_bytes / 1024:.2f} KB")
    print(f"Compressed file size: {compressed_size_bytes / 1024:.2f} KB")
    print(f"Compression ratio:    {compression_ratio:.4f}")

if __name__ == '__main__':
    # Default file path if not provided
    sample_path = "./data/norm_wiki_sample.txt"
    if len(sys.argv) > 1:
        sample_path = sys.argv[1]
        
    if not os.path.exists(sample_path):
        print(f"Error: File '{sample_path}' not found.")
        sys.exit(1)
        
    main(sample_path)

"""
=== Analysis Answers ===
- Najkrótsza możliwa długość kodu: 6 bitów (2^6 = 64, co wystarcza do zakodowania 37 znaków).
- Co zrobić, by bardziej skompresować tekst?: Przypisać krótsze kody do częściej występujących znaków (kodowanie zmiennodługościowe, np. Huffmana).
- Co z nieużytymi kodami?: Pozostają niewykorzystane i marnują przestrzeń w kodowaniu stałodługościowym.
- Jak odkodowywać kody o zmiennej długości?: Należy zbudować kody bezprzedrostkowe (prefix-free), np. za pomocą drzewa binarnego, by unikać dwuznaczności podczas czytania bit po bicie.
"""