sequence = "ATGCGATCGATCGATCGCGCTA"


gc_count = sequence.count("G") + sequence.count("C")
gc_content = (gc_count / len(sequence)) * 100


print("DNA sequence:", sequence)
print("Sequence length:", len(sequence))
print("GC count:", gc_count)
print("GC content:", round(gc_content, 2), "%")
