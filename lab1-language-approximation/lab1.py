import sys
import random
import os
from collections import Counter

def read_file(filename: str) -> str:
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read().lower()

def save_text_to_file(text: str, filename: str) -> None:
    dir_name = os.path.dirname(filename)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(text)

def avg_word_length(text: str) -> float:
    words = text.split()
    if not words:
        return 0.0
    return sum(len(word) for word in words) / len(words)

def calculate_char_frequency(text: str) -> dict:
    counter = Counter(text)
    total_chars = sum(counter.values())
    return {char: count / total_chars for char, count in counter.items()}

def generate_text(chars_frequencies: dict, length: int) -> str:
    chars = list(chars_frequencies.keys())
    probabilities = list(chars_frequencies.values())
    
    generated_chars = random.choices(chars, weights=probabilities, k=length)
    return "".join(generated_chars)

def generate_markov_chain(text: str, order: int) -> dict:
    chain = {}
    for i in range(len(text) - order):
        fragment = text[i:i+order]
        next_letter = text[i+order]
        if fragment not in chain:
            chain[fragment] = Counter()
        chain[fragment][next_letter] += 1
    return chain

def generate_markov_text(chain: dict, order: int, length: int, start_sequence: str = "") -> str:
    if start_sequence and len(start_sequence) >= order and start_sequence[-order:] in chain:
        generated_text = start_sequence
        current_fragment = start_sequence[-order:]
    else:
        current_fragment = random.choice(list(chain.keys()))
        generated_text = current_fragment

    for _ in range(length - len(generated_text)):
        if current_fragment not in chain:
            break
        
        possible_next = chain[current_fragment]
        next_letter = random.choices(list(possible_next.keys()), weights=list(possible_next.values()))[0]
        
        generated_text += next_letter
        current_fragment = generated_text[-order:]
        
    return generated_text

def main(text_sample_path: str, length: int):
    text_sample = read_file(text_sample_path)
    print(f'Avg word length in text sample: {avg_word_length(text_sample):.4f}')
    
    # ZAD1: Przybliżenie zerowego rzędu
    characters = " abcdefghijklmnopqrstuvwxyz"
    const_frequencies = {char: 1/27 for char in characters}
    const_chars_freq_text = generate_text(const_frequencies, length)
    print(f'\nAvg word length (zero-order approx): {avg_word_length(const_chars_freq_text):.4f}')
    
    # ZAD2: Częstość liter w korpusie
    frequencies = calculate_char_frequency(text_sample)
    print("\nTop 5 frequent characters:")
    sorted_frequencies = sorted(frequencies.items(), key=lambda x: x[1], reverse=True)
    for char, freq in sorted_frequencies[:5]:
        print(f"\t'{char}': {freq:.4f}")  
        
    # ZAD3: Przybliżenie pierwszego rzędu
    wiki_chars_freq_text = generate_text(frequencies, length)
    print(f'\nAvg word length (first-order approx): {avg_word_length(wiki_chars_freq_text):.4f}') 
    
    # ZAD4: Prawdopodobieństwo warunkowe dla 2 najczęstszych znaków
    print("\nConditional probabilities for top 2 characters:")
    top_2_chars = [char for char, freq in sorted_frequencies[:2]]
    chain_order_1 = generate_markov_chain(text_sample, 1)
    
    for char in top_2_chars:
        following_chars = chain_order_1.get(char, Counter())
        total_following = sum(following_chars.values())
        
        print(f"Probabilities after '{char}':")
        for next_char, count in following_chars.most_common(5):
            print(f"\t'{next_char}': {count / total_following:.4f}")

    # ZAD5: Łańcuchy Markowa (rzędy 1, 3 i 5)
    print("\nGenerating Markov chains...")
    for order in [1, 3, 5]:
        chain = generate_markov_chain(text_sample, order)
        start_seq = "probability" if order == 5 else ""
        
        markov_text = generate_markov_text(chain, order, length, start_sequence=start_seq)
        print(f'Avg word length (Markov order {order}): {avg_word_length(markov_text):.4f}')
        
        generated_text_path = f"output/markov_{order}.txt"
        save_text_to_file(markov_text, generated_text_path)
        print(f'\tSaved to: {generated_text_path}')


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python lab1.py <text_sample_path> <generated_text_length>")
        sys.exit(1)
        
    main(sys.argv[1], int(sys.argv[2]))