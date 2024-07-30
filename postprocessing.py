import pandas as pd
import re


df = pd.read_csv("data/XEON_intel.csv")
df = df.drop(columns=df.columns[0])  # drop index
df["Model number"] = (
    df["Model number"].str.encode("ascii", "ignore").str.decode("ascii")
)


def convert_to_ghz(freq_str):
    freq_str = freq_str.replace("\xa0", " ")
    if "GHz" in freq_str:
        return float(freq_str.replace(" GHz", ""))
    elif "MHz" in freq_str:
        return float(freq_str.replace(" MHz", "")) / 1000
    else:
        raise ValueError("Unrecognized frequency unit")


def extract_cores_threads(details):

    if pd.notna(details) and details.strip():
        # Find the substring with cores and threads (e.g., "22 (44)")
        match = re.search(r"(\d+) \((\d+)\)", details)

        if match:
            cores = match.group(1)
            threads = match.group(2)
            return pd.Series([cores, threads], index=["Cores", "Threads"])

    return pd.Series([None, None], index=["Cores", "Threads"])


def fix_dates(date):
    try:
        if "Q" in date:
            quarter, year = date.split()
            year = int(year)

            quarter_to_month = {"Q1": "01", "Q2": "04", "Q3": "07", "Q4": "10"}
            month = quarter_to_month.get(quarter, "01")

            return pd.Timestamp(f"{year}-{month}-01")
        elif date == "February 2004[10]":
            return "February 2004"
        elif date == "March 21, 2001[a]":
            return "March 21, 2001"
        elif date in ["Unreleased"]:
            return ""
        else:
            return date
    except:
        return date


# Apply the extraction function to update only the 'cores' column
extracted = df["Cores (threads)"].apply(extract_cores_threads)
df["Cores"] = extracted["Cores"].combine_first(df["Cores"])
df["Threads"] = extracted["Threads"]
df = df.drop(columns=["Cores (threads)"])

df["Frequency"] = df["Frequency"].apply(convert_to_ghz)

df.loc[df["Cores"].isna() & df["Model number"].str.contains("\."), "Cores"] = 1
dual_cores = [
    "Xeon LV 1.66",
    "Xeon LV 2.0",
    "Xeon LV 2.16",
    "Xeon ULV 1.66",
]
df.loc[df["Model number"].isin(dual_cores), "Cores"] = 2
df.loc[df["sSpec number"] == "SL8MA (A0)", "Cores"] = 2

df["Release date"] = df["Release date"].apply(fix_dates)
df["Release date"] = pd.to_datetime(df["Release date"])

df.to_csv("data/polished_XEON_Intel.csv", index=False)
