import tiktoken
enc = tiktoken.get_encoding("cl100k_base")
"""
text = enc.decode([1, 2, 3, 4, 5])  # Example token IDs to decode
tokens = enc.encode(text)

print("Original text:", text)
print("Original token IDs:", tokens)
print("Decoded tokens:", [enc.decode([t]) for t in tokens])
print("Decoded text:", enc.decode(tokens))
"""

samples = [
    "Hello, world!",
    "The quick brown fox jumps over the lazy dog.",
    "Supercalifragilisticexpialidocious",
    "This is a longer paragraph designed to test how tokenization works across multiple sentences."
]

for s in samples:
    tokens = enc.encode(s)
    print(f"Text: {s}")
    print(f"Word count: {len(s.split())}, Token count: {len(tokens)}")
    print([enc.decode([tokens]) for tokens in tokens], "\n")
    