
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


project_dir = Path(
    "python/bioinformatics/md_project"
)


def analyze_file(filepath):

    data = pd.read_csv(filepath)

    numeric_columns = [
        column
        for column in data.select_dtypes(include="number").columns
        if column != "time_ns"
    ]

    results = []

    for column in numeric_columns:

        results.append({
            "parameter": column,
            "frames": len(data),
            "mean": data[column].mean(),
            "minimum": data[column].min(),
            "maximum": data[column].max(),
            "std": data[column].std()
        })

    return results


def create_plot(filepath):

    data = pd.read_csv(filepath)

    numeric_columns = [
        column
        for column in data.select_dtypes(include="number").columns
        if column != "time_ns"
    ]

    for column in numeric_columns:

        plt.figure(figsize=(8, 5))

        plt.plot(
            data["time_ns"],
            data[column],
            marker="o"
        )

        plt.xlabel("Time (ns)")
        plt.ylabel(column)
        plt.title(f"{column} vs Time")

        plt.grid(True)

        output_name = (
            filepath.stem + "_plot.png"
        )

        output_path = (
            project_dir / output_name
        )

        plt.tight_layout()
        plt.savefig(
            output_path,
            dpi=300
        )

        plt.close()

        print(
            f"Plot saved: {output_path}"
        )


csv_files = sorted(
    filepath
    for filepath in project_dir.glob("*.csv")
    if filepath.name != "md_summary.csv"
)


all_results = []


print("===== MULTI-FILE MD ANALYZER =====")
print(f"Files found: {len(csv_files)}")


for filepath in csv_files:

    print(f"\nAnalyzing: {filepath.name}")

    results = analyze_file(filepath)

    all_results.extend(results)

    create_plot(filepath)


summary = pd.DataFrame(all_results)


summary_path = (
    project_dir / "md_summary.csv"
)


summary.to_csv(
    summary_path,
    index=False
)


report_path = (
    project_dir / "md_analysis_report.txt"
)


with open(report_path, "w") as report:

    report.write(
        "===== MD ANALYSIS REPORT =====\n\n"
    )

    report.write(
        f"Parameters analyzed: {len(summary)}\n\n"
    )

    for _, row in summary.iterrows():

        report.write(
            f"{row['parameter']}\n"
        )

        report.write(
            f"Frames: {int(row['frames'])}\n"
        )

        report.write(
            f"Mean: {row['mean']:.3f}\n"
        )

        report.write(
            f"Minimum: {row['minimum']:.3f}\n"
        )

        report.write(
            f"Maximum: {row['maximum']:.3f}\n"
        )

        report.write(
            f"Standard deviation: "
            f"{row['std']:.3f}\n\n"
        )


print("\n===== SUMMARY TABLE =====")
print(summary)

print("\nSummary saved to:")
print(summary_path)

print("\nReport saved to:")
print(report_path)