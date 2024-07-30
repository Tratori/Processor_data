import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def get_group(model_number):
    simple = ["Platinum", "Gold", "Silver", "Bronze"]
    for group in simple:
        if group in model_number:
            return group
    Es = ["E3", "E5", "E7"]
    for group in Es:
        if group + "-" in model_number:
            return group
    EDW = ["E", "D", "W"]
    for group in EDW:
        if f"Xeon {group}" in model_number:
            return group

    return "Other"


def plot_cores_year():
    df = pd.read_csv("data/polished_XEON_Intel.csv")
    df = df.dropna(subset=["Release date", "Cores"])
    df["Family"] = df["Model number"].apply(get_group)
    df["Release date"] = pd.to_datetime(df["Release date"], errors="raise")

    df.groupby(["Family"])
    # KDE plot for filled areas by family
    # for family in df["Family"].unique():
    #    subset = df[df["Family"] == family]
    #    sns.kdeplot(
    #        data=subset,
    #        x="Release date",
    #        y="Cores",
    #        fill=True,
    #        alpha=0.3,
    #        label=family,
    #    )

    sns.scatterplot(data=df, x="Release date", y="Cores", hue="Family", marker="o")
    plt.show()


if __name__ == "__main__":
    plot_cores_year()
