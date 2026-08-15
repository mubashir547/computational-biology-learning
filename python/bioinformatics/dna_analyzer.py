sequence = input("Enter a DNA sequence: ")

sequence = sequence.replace(" ", "").replace("\n", "").upper()

valid_bases = "ATGC"

if not sequence:
    print("Error: DNA sequence cannot be empty.")

elif not all(base in valid_bases for base in sequence):
    print("Error: Invalid DNA sequence.")
    print("Only A, T, G, and C are allowed.")

else:
    length = len(sequence)

    a_count = sequence.count("A")
    t_count = sequence.count("T")
    g_count = sequence.count("G")
    c_count = sequence.count("C")

    gc_count = g_count + c_count
    at_count = a_count + t_count

    gc_content = (gc_count / length) * 100
    at_content = (at_count / length) * 100

    complement_table = str.maketrans("ATGC", "TACG")
    complement = sequence.translate(complement_table)
    reverse_complement = complement[::-1]

    print("\n========== DNA ANALYSIS ==========")
    print("DNA Sequence:", sequence)
    print("Sequence Length:", length)

    print("\nNucleotide Counts:")
    print("A:", a_count)
    print("T:", t_count)
    print("G:", g_count)
    print("C:", c_count)

    print("\nComposition:")
    print("GC Content:", round(gc_content, 2), "%")
    print("AT Content:", round(at_content, 2), "%")

    print("\nSequence Information:")
    print("Complement:", complement)
    print("Reverse Complement:", reverse_complement)

    print("\n===================================")