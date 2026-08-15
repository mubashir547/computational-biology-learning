sequence = "ATGCGATCGATCGATCGCGCTA"

print("DNA Sequence:", sequence)
print("Sequence Length:", len(sequence))

print("A:", sequence.count("A"))
print("T:", sequence.count("T"))
print("G:", sequence.count("G"))
print("C:", sequence.count("C"))

gc_count = sequence.count("G") + sequence.count("C")
gc_content = (gc_count / len(sequence)) * 100

print("GC Content:", round(gc_content, 2), "%")