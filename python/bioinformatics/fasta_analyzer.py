import sys

def read_fasta(filename):
    sequences = {}
    current_name = None

    with open(filename, "r") as file:
        for line in file:
            line = line.strip()

            if not line:
                continue

            if line.startswith(">"):
                current_name = line[1:]
                sequences[current_name] = ""

            else:
                sequences[current_name] += line.upper()

    return sequences


def validate_sequence(sequence):
    valid_bases = "ATGC"
    return bool(sequence) and all(base in valid_bases for base in sequence)


def gc_content(sequence):
    gc = sequence.count("G") + sequence.count("C")
    return (gc / len(sequence)) * 100


def analyze_sequences(sequences):
    total_bases = 0
    highest_gc = -1
    highest_gc_id = ""

    print("===== FASTA ANALYSIS =====\n")

    for name, sequence in sequences.items():

        if not validate_sequence(sequence):
            print("Warning:", name, "contains an invalid DNA sequence.")
            continue

        length = len(sequence)
        gc = gc_content(sequence)

        total_bases += length

        if gc > highest_gc:
            highest_gc = gc
            highest_gc_id = name

        print("ID:", name)
        print("Sequence:", sequence)
        print("Length:", length)
        print("GC Content:", round(gc, 2), "%")
        print()

    number_of_sequences = len(sequences)

    if number_of_sequences > 0:
        average_length = total_bases / number_of_sequences
    else:
        average_length = 0

    print("===== SUMMARY =====")
    print("Number of sequences:", number_of_sequences)
    print("Total bases:", total_bases)
    print("Average sequence length:", round(average_length, 2))
    print("Highest GC sequence:", highest_gc_id)
    print("Highest GC Content:", round(highest_gc, 2), "%")

if len(sys.argv) != 2:
    print("Usage: py fasta_analyzer.py <fasta_file>")
    sys.exit(1)

filename = sys.argv[1]

sequences = read_fasta(filename)

analyze_sequences(sequences)
