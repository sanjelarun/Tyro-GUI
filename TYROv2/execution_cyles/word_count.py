str = "The quick brown fox jumps over the lazy dog"
counts = dict()
words = str.split()

for word in words:
    if word in counts:
        counts[word] += 1
    else:
        counts[word] = 1

print(counts)
