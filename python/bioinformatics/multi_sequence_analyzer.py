def gc_content(sequence):
    gc = sequence.count("G") + sequence.count("C")
    return (gc / len(sequence)) * 100


sequences = [
    "ATGCGATCG",
    "ATATATAT",
    "GCGCGCGC",
    "ATGCGCGTAA"
]

print("===== MULTI-SEQUENCE DNA ANALYSIS =====\n")

highest_gc = -1
highest_gc_sequence = ""

for sequence in sequences:
    gc = gc_content(sequence)

    print("Sequence:", sequence)
    print("Length:", len(sequence))
    print("GC Content:", round(gc, 2), "%")
    print()

    if gc > highest_gc:
        highest_gc = gc
        highest_gc_sequence = sequence


print("===== SUMMARY =====")
print("Highest GC sequence:", highest_gc_sequence)
print("Highest GC Content:", round(highest_gc, 2), "%")