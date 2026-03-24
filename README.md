# Information Theory and Data Compression
The `information-theory-and-data-compression` repository contains a collection of projects completed during the TIMKOD course at Poznan University of Technology. The goal of these projects was to explore natural language approximation and implement lossless data compression algorithms.

## 🛠️ Technologies & Concepts Used
* **Python** (Vanilla Python, `collections`, `math`, `heapq`, `pickle`)
* **External Libraries** (`bitarray` for bit-level manipulation)
* **Information Theory** (Shannon entropy, Conditional entropy)
* **Algorithms** (Markov Chains, Huffman Coding, LZW Compression)

## 📂 Project descriptions

### [lab1-language-approximation](./lab1-language-approximation)
Introduction to natural language approximation at the character level.
* Generating zero-order and first-order approximations based on character frequencies.
* Implementing Markov chains (first, third, and fifth order) to predict succeeding characters.

### [lab2-language-approximation-words](./lab2-language-approximation-words)
Advanced language approximation using whole words.
* Analyzing word frequencies to demonstrate Zipf's law and the Pareto principle.
* Generating text using first-order approximation and word-level Markov chains.

### [lab3-conditional-entropy](./lab3-conditional-entropy)
Analyzing languages using information theory concepts.
* Calculating Shannon entropy and conditional entropy of consecutive orders for characters and words.
* Recognizing whether a given text sample is a natural language based on conditional entropy drops.

### [lab4-fixed-length-coding](./lab4-fixed-length-coding)
Introduction to lossless data compression.
* Creating a generic framework for symbol-by-symbol text compression and decompression.
* Implementing fixed-length binary coding and measuring compression levels.

### [lab5-huffman-coding](./lab5-huffman-coding)
Lossless compression using Huffman coding.
* Building a Huffman tree based on character frequencies to generate prefix-free codes.
* Calculating average code length and overall coding efficiency.

### [lab6-lzw-compression](./lab6-lzw-compression)
Dictionary-based lossless data compression.
* Implementing the Lempel-Ziv-Welch (LZW) algorithm for text and binary file compression.
* Testing compression performance on various files with different dictionary size limits.

## 🔍 Interesting Findings

### Lab 3: Natural Language vs. Random Data Analysis
By calculating the conditional entropy of characters and words across different samples, we can mathematically determine if a given dataset represents a natural language:

* **[sample0.txt](./lab3-conditional-entropy/samples/sample0.txt)**: Not a natural language. Word entropy for order 0 and 1 is identical, whereas it should drop significantly in a natural language.
* **[sample1.txt](./lab3-conditional-entropy/samples/sample1.txt)**: Natural language. Entropy drops consistently according to expectations.
* **[sample2.txt](./lab3-conditional-entropy/samples/sample2.txt)**: Natural language. Entropy drops consistently according to expectations.
* **[sample3.txt](./lab3-conditional-entropy/samples/sample3.txt)**: Natural language. Entropy drops consistently according to expectations.
* **[sample4.txt](./lab3-conditional-entropy/samples/sample4.txt)**: Not a natural language. Character entropy does not drop, lacking the predictability of natural language structures.
* **[sample5.txt](./lab3-conditional-entropy/samples/sample5.txt)**: Not a natural language. Word entropy drops to near zero, which indicates repeating, deterministic patterns rather than natural vocabulary usage.
