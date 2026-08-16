import pandas as pd


data = pd.read_csv(
    "python/bioinformatics/md_dataset.csv"
)


print("===== MD DATASET =====")
print(data)


print("\n===== DATASET INFORMATION =====")
print("Number of frames:", len(data))
print("Columns:", list(data.columns))


print("\n===== SUMMARY STATISTICS =====")
print(data.describe())
print("\n===== HIGH RMSD FRAMES =====")

high_rmsd = data[data["rmsd_A"] > 2.4]

print(high_rmsd)

print("\nNumber of high RMSD frames:", len(high_rmsd))

print("\n===== HIGH RMSD + HIGH H-BOND FRAMES =====")

stable_interactions = data[
    (data["rmsd_A"] > 2.4) &
    (data["hbonds"] > 480)
]

print(stable_interactions)

print("\nNumber of selected frames:", len(stable_interactions))