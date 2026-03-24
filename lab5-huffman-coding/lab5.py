import sys
import os
import pickle
import bitarray
import heapq
import math
from collections import Counter
from typing import Optional

# 37 supported characters: 26 letters + 10 digits + space
CHARACTERS = " abcdefghijklmnopqrstuvwxyz0123456789"

class Node:
    def __init__(self, char: Optional[str], freq: float):
        self.char = char
        self.freq = freq
        self.left: Optional[Node] = None
        self.right: Optional[Node] = None

    def __lt__(self, other):
        return self.freq < other.freq

def read_file(filename: str) -> str:
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read().lower()

def calculate_char_frequency(text: str) -> dict:
    counter = Counter(char for char in text if char in CHARACTERS)
    total_chars = sum(counter.values())
    return {char: count / total_chars for char, count in counter.items()}

def build_huffman_tree(frequencies: dict) -> Optional[Node]:
    """Builds the Huffman tree using a priority queue (heap)."""
    heap = [Node(char, freq) for char, freq in frequencies.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)

    return heap[0] if heap else None

def generate_huffman_codes(node: Optional[Node], current_code: str = "", codes: Optional[dict] = None) -> dict:
    """Recursively traverses the Huffman tree to assign binary codes."""
    if codes is None:
        codes = {}

    if node is not None:
        if node.char is not None:
            codes[node.char] = current_code
        else:
            generate_huffman_codes(node.left, current_code + "0", codes)
            generate_huffman_codes(node.right, current_code + "1", codes)
            
    return codes

def encode(text: str, codes: dict) -> bitarray.bitarray:
    """Encodes text into a bitarray using the provided codes."""
    encoded_bits = bitarray.bitarray()
    encoded_str = "".join(codes[char] for char in text if char in codes)
    encoded_bits.extend(encoded_str)
    return encoded_bits

def decode(encoded_text: bitarray.bitarray, codes: dict) -> str:
    """Decodes a bitarray back into text."""
    reverse_codes = {code: char for char, code in codes.items()}
    decoded_text = []
    current_code = ""
    
    for bit in encoded_text.to01():
        current_code += bit
        if current_code in reverse_codes:
            decoded_text.append(reverse_codes[current_code])
            current_code = ""
            
    return "".join(decoded_text)

def save_data(codes: dict, encoded_text: bitarray.bitarray, filename: str) -> None:
    """Saves the codes, exact bit length, and the bitarray to a file."""
    dir_name = os.path.dirname(filename)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
        
    with open(filename, 'wb') as file:
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

def calculate_entropy(frequencies: dict) -> float:
    """Calculates Shannon entropy."""
    return -sum(prob * math.log2(prob) for prob in frequencies.values() if prob > 0)

def calculate_average_code_length(frequencies: dict, codes: dict) -> float:
    """Calculates the expected length of the code."""
    return sum(frequencies[char] * len(codes[char]) for char in frequencies)

def main(text_sample_path: str):
    print("--- TASK 2: Huffman Coding ---")
    
    text_sample = read_file(text_sample_path)
    
    # 1. Create codes
    frequencies = calculate_char_frequency(text_sample)
    huffman_tree = build_huffman_tree(frequencies)
    huffman_codes = generate_huffman_codes(huffman_tree)
    
    # 2. Encode
    print("Encoding...")
    encoded_text = encode(text_sample, huffman_codes)
    
    # 3. Save
    output_bin_path = "output/encoded_data.bin"
    save_data(huffman_codes, encoded_text, output_bin_path)
    print(f"Data saved to: {output_bin_path}")
    
    # 4. Load & Decode
    print("Loading and decoding...")
    loaded_codes, loaded_encoded_text = load_data(output_bin_path)
    decoded_text = decode(loaded_encoded_text, loaded_codes)
    
    # 5. Save decoded text
    output_decoded_path = "output/decoded_text.txt"
    with open(output_decoded_path, 'w', encoding='utf-8') as file:
        file.write(decoded_text)
    
    # 6. Verify identity
    is_identical = (text_sample == decoded_text)
    print(f"Verification (Original == Decoded): {is_identical}")
    
    # 7. Math & Stats
    entropy = calculate_entropy(frequencies)
    avg_code_length = calculate_average_code_length(frequencies, huffman_codes)
    efficiency = (entropy / avg_code_length) * 100 if avg_code_length > 0 else 0
    
    original_size_bytes = len(text_sample.encode('utf-8'))
    compressed_size_bytes = os.path.getsize(output_bin_path)
    compression_ratio = compressed_size_bytes / original_size_bytes
    
    print("\n--- Statistics ---")
    print(f"Entropy (H):               {entropy:.4f} bits/symbol")
    print(f"Average Code Length (L):   {avg_code_length:.4f} bits/symbol")
    print(f"Coding Efficiency (H/L):   {efficiency:.2f}%")
    print(f"Original file size:        {original_size_bytes / 1024:.2f} KB")
    print(f"Compressed file size:      {compressed_size_bytes / 1024:.2f} KB")
    print(f"Compression ratio:         {compression_ratio:.4f}")

if __name__ == '__main__':
    sample_path = "./data/norm_wiki_sample.txt"
    if len(sys.argv) > 1:
        sample_path = sys.argv[1]
        
    if not os.path.exists(sample_path):
        print(f"Error: File '{sample_path}' not found.")
        sys.exit(1)
        
    main(sample_path)