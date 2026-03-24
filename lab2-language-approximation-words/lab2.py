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

def calculate_word_frequencies(words: list) -> dict:
    counter = Counter(words)
    total_words = sum(counter.values())
    return {word: count / total_words for word, count in counter.items()}

def generate_text_first_order(words_frequencies: dict, length: int) -> str:
    words = list(words_frequencies.keys())
    probabilities = list(words_frequencies.values())
    
    generated_words = random.choices(words, weights=probabilities, k=length)
    return " ".join(generated_words)

def generate_markov_chain(words: list, order: int) -> dict:
    chain = {}
    for i in range(len(words) - order):
        ngram = tuple(words[i:i+order])
        next_word = words[i+order]
        if ngram not in chain:
            chain[ngram] = Counter()
        chain[ngram][next_word] += 1
    return chain

def generate_markov_text(chain: dict, order: int, length: int, start_word: str = "") -> str:
    if start_word:
        possible_seeds = [key for key in chain.keys() if key[0] == start_word]
        if not possible_seeds:
            print(f"Warning: No n-grams starting with '{start_word}'.")
            return ""
        current_ngram = random.choice(possible_seeds)
    else:
        current_ngram = random.choice(list(chain.keys()))
        
    generated_words = list(current_ngram)
    
    for _ in range(length - len(generated_words)):
        if current_ngram not in chain:
            break
            
        possible_next = chain[current_ngram]
        next_word = random.choices(list(possible_next.keys()), weights=list(possible_next.values()))[0]
        
        generated_words.append(next_word)
        current_ngram = tuple(generated_words[-order:])
        
    return " ".join(generated_words)

def main(text_sample_path: str, length: int):
    text_sample = read_file(text_sample_path)
    words = text_sample.split()
    
    print(f"Total words in sample: {len(words)}")
    
    # TASK 1: Word frequencies and Pareto principle
    print("--- TASK 1: Word frequencies ---")
    words_count = Counter(words)
    total_words = sum(words_count.values())
    
    top_10 = words_count.most_common(10)
    print("Top 10 words:")
    for word, count in top_10:
        print(f"  '{word}': {count} ({(count/total_words)*100:.2f}%)")
        
    top_6k_count = sum(count for word, count in words_count.most_common(6000))
    top_30k_count = sum(count for word, count in words_count.most_common(30000))
    
    print(f"\nText coverage by top 6k words: {(top_6k_count/total_words)*100:.2f}%")
    print(f"Text coverage by top 30k words: {(top_30k_count/total_words)*100:.2f}%")
    
    # TASK 2: First-order approximation (independent words)
    print("\n--- TASK 2: First-order approximation ---")
    words_freq = calculate_word_frequencies(words)
    first_order_text = generate_text_first_order(words_freq, length)
    save_text_to_file(first_order_text, "output/lab2_first_order.txt")
    print("Saved to: output/lab2_first_order.txt")
    
    # TASK 3: Markov chain approximations
    print("\n--- TASK 3: Markov Chains ---")
    
    # 1st order
    chain_1 = generate_markov_chain(words, 1)
    text_markov_1 = generate_markov_text(chain_1, 1, length)
    save_text_to_file(text_markov_1, "output/lab2_markov_1.txt")
    print("Saved 1st order Markov text to: output/lab2_markov_1.txt")

    # 2nd order
    chain_2 = generate_markov_chain(words, 2)
    text_markov_2 = generate_markov_text(chain_2, 2, length)
    save_text_to_file(text_markov_2, "output/lab2_markov_2.txt")
    print("Saved 2nd order Markov text to: output/lab2_markov_2.txt")

    # 2nd order starting with "probability"
    text_markov_2_seed = generate_markov_text(chain_2, 2, length, start_word="probability")
    save_text_to_file(text_markov_2_seed, "output/lab2_markov_2_seed.txt")
    print("Saved 2nd order Markov text (seed: 'probability') to: output/lab2_markov_2_seed.txt")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python lab2.py <text_sample_path> <length_of_text_to_generate>")
        sys.exit(1)
        
    main(sys.argv[1], int(sys.argv[2]))