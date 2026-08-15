def calculate_gc_content(sequence):
    sequence = sequence.upper()

    if not sequence:
        return None

    valid_bases = "ATGC"

    if not all(base in valid_bases for base in sequence):
        return None

    gc_count = sequence.count("G") + sequence.count("C")
    gc_content = (gc_count / len(sequence)) * 100

    return gc_content


dna_sequences = [
    "ATGCGATCGATCG",
    "ATATATAT",
    "GCGCGCGC"
]

for dna in dna_sequences:
    gc = calculate_gc_content(dna)

    if gc is not None:
        print("DNA:", dna)
        print("GC Content:", round(gc, 2), "%")
        print()
    else:
        print("Invalid DNA sequence:", dna)