import sys
import math
from collections import Counter
from typing import Sequence, List

def read_file(filename: str) -> str:
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read().lower()

def calculate_entropy(tokens: Sequence) -> float:
    # Calculates Shannon entropy for a sequence of tokens (characters or words).
    length = len(tokens)
    if length == 0:
        return 0.0
    
    frequencies = Counter(tokens)
    entropy = 0.0
    for count in frequencies.values():
        probability = count / length
        entropy -= probability * math.log2(probability)
    return entropy

def get_ngrams(tokens: Sequence, n: int) -> List[tuple]:
    # Generates n-grams from a sequence of tokens.
    if n == 1:
        return [(t,) for t in tokens]
    return [tuple(tokens[i:i+n]) for i in range(len(tokens) - n + 1)]

def calculate_conditional_entropy(tokens: Sequence, order: int) -> float:
    """
    Calculates conditional entropy of order N.
    Formula: H(X_n | X_{n-1}, ..., X_1) = H(X_n, ..., X_1) - H(X_{n-1}, ..., X_1)
    """
    if order == 0:
        return calculate_entropy(tokens)
    
    # H(X_n, ..., X_1) is the entropy of (order + 1)-grams
    ngrams_n_plus_1 = get_ngrams(tokens, order + 1)
    joint_entropy = calculate_entropy(ngrams_n_plus_1)
    
    # H(X_{n-1}, ..., X_1) is the entropy of order-grams
    ngrams_n = get_ngrams(tokens, order)
    context_entropy = calculate_entropy(ngrams_n)
    
    return joint_entropy - context_entropy

def analyze_file(filepath: str, max_order: int = 4):
    text = read_file(filepath)
    words = text.split()
    
    print(f"--- Analysis for {filepath} ---")
    
    # Character entropy analysis
    char_entropy = calculate_entropy(text)
    print(f"Character entropy: {char_entropy:.4f}")
    for i in range(1, max_order + 1):
        cond_entropy = calculate_conditional_entropy(text, i)
        print(f"Conditional character entropy (order {i}): {cond_entropy:.4f}")
        
    print()
    
    # Word entropy analysis
    word_entropy = calculate_entropy(words)
    print(f"Word entropy: {word_entropy:.4f}")
    for i in range(1, max_order + 1):
        cond_entropy = calculate_conditional_entropy(words, i)
        print(f"Conditional word entropy (order {i}): {cond_entropy:.4f}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python lab3.py <file1.txt> <file2.txt> ...")
        sys.exit(1)
        
    for filepath in sys.argv[1:]:
        analyze_file(filepath)

if __name__ == '__main__':
    main()

"""
=== Sample Analysis Results ===
* sample0.txt: Not a natural language. Word entropy for order 0 and 1 is identical, whereas it should drop significantly in a natural language.
* sample1.txt: Natural language. Entropy drops consistently according to expectations.
* sample2.txt: Natural language. Entropy drops consistently according to expectations.
* sample3.txt: Natural language. Entropy drops consistently according to expectations.
* sample4.txt: Not a natural language. Character entropy does not drop, lacking the predictability of natural language structures.
* sample5.txt: Not a natural language. Word entropy drops to near zero, which indicates repeating, deterministic patterns rather than natural vocabulary usage.
"""