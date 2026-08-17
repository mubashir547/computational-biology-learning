import sys
import pandas as pd

def calculate_statistics(data, column):

    values = data[column]

    return {
        "mean": values.mean(),
        "minimum": values.min(),
        "maximum": values.max(),
        "std": values.std()
    }
if len(sys.argv) != 2:
    print("Usage: py md_input_analyzer.py <rmsd.csv>")
    sys.exit(1)


file_path = sys.argv[1]

data = pd.read_csv(file_path)

print("===== MD INPUT ANALYSIS =====")

print("\nDataset:")
print(data)

print("\nDataset information:")
print("Number of frames:", len(data))
print("Columns:", list(data.columns))

print("\nBasic statistics:")
print(data.describe())

print("\n===== QUALITY CONTROL =====")

print("Missing values:")
print(data.isnull().sum())

print("\nDuplicate rows:", data.duplicated().sum())

print("\nData types:")
print(data.dtypes)

numeric_columns = data.select_dtypes(
    include="number"
).columns

for column in numeric_columns:

    if data[column].isnull().any():
        print(
            f"WARNING: Missing values in {column}"
        )
    else:
        print(
            f"{column} missing-value QC: PASS"
        )

    if (data[column] < 0).any():
        print(
            f"WARNING: Negative values in {column}"
        )
    else:
        print(
            f"{column} range QC: PASS"
        )
print("\n===== NUMERIC STATISTICS =====")

numeric_columns = [
    column for column in data.select_dtypes(
        include="number"
    ).columns
    if column != "time_ns"
]
for column in numeric_columns:

    stats = calculate_statistics(
        data,
        column
    )

    print(f"\n{column}:")

    print(f"Mean: {stats['mean']:.3f}")
    print(f"Minimum: {stats['minimum']:.3f}")
    print(f"Maximum: {stats['maximum']:.3f}")
    print(f"Standard deviation: {stats['std']:.3f}")