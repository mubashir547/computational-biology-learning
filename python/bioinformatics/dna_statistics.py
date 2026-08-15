def analyze_dna(sequence):
    sequence = sequence.replace(" ", "").upper()

    valid_bases = "ATGC"

    if not sequence:
        return None

    if not all(base in valid_bases for base in sequence):
        return None

    counts = {
        "A": sequence.count("A"),
        "T": sequence.count("T"),
        "G": sequence.count("G"),
        "C": sequence.count("C")
    }

    gc = counts["G"] + counts["C"]
    gc_percent = (gc / len(sequence)) * 100

    return counts, gc_percent


dna = input("Enter DNA sequence: ")

result = analyze_dna(dna)

if result is None:
    print("Error: Invalid DNA sequence.")
    print("Only A, T, G, and C are allowed.")
else:
    counts, gc_percent = result

    print("\nDNA:", dna.upper())
    print("Length:", len(dna.replace(" ", "")))
    print("Counts:", counts)
    print("GC Content:", round(gc_percent, 2), "%")