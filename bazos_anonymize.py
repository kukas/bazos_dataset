from glob import glob
import pandas
import os

os.makedirs("anon_output_merged", exist_ok=True)

files = glob("output_merged/*.pkl.gz")
files = sorted(files, key=os.path.getsize)
pandas.options.display.max_colwidth = 200
total = 0
for file in files:
    print(file)
    df = pandas.read_pickle(file)
    print("rows before anonymization: ", len(df))
    df = df[~df.title.str.contains(r"[a-zA-Z]@[a-zA-Z]{2,}\.[a-zA-Z]{2,6}")]
    df = df[~df.title.str.contains(r"(^|^[^0-9]|[^0-9][^0-9])(00)?(420|421)?\s*(\d\s*){9}([^0-9][^0-9]|[^0-9]$|$)")]
    print("rows after anonymization: ", len(df))
    total = total + len(df)
    df.to_pickle("anon_"+file)

print("Total: ", total)