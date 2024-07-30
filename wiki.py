import wikipediaapi
import pandas as pd
import requests

wiki_wiki = wikipediaapi.Wikipedia("CPU_List (Tratori@github.com)", "en")
page = wiki_wiki.page("List_of_Intel_Xeon_processors")


links = page.links
filtered_links = [
    link for link in links if link.startswith("List of Intel Xeon processors ")
]

all_tables = []

for sublink in filtered_links:
    subpage = wiki_wiki.page(sublink)
    if subpage.exists():
        formatted_link = sublink.replace(" ", "_")
        response = requests.get(f"https://en.wikipedia.org/wiki/{formatted_link}")

        if response.status_code == 200:
            tables = pd.read_html(response.text)
            all_tables.extend(tables)
        else:
            print(f"Error fetching {sublink}")

combined_table = pd.concat(all_tables, ignore_index=True)

combined_table.to_csv("data/wikipedia_tables_unfiltered.csv")

filtered_table = combined_table.drop(
    columns=["Unnamed: 14", "Unnamed: 15", "Unnamed: 16", 0, 1]
).dropna(subset=["Model number"])

filtered_table = filtered_table[filtered_table.iloc[:, 0] != filtered_table.iloc[:, 1]]
filtered_table.reset_index(drop=True)
filtered_table.to_csv("data/XEON_intel.csv")
