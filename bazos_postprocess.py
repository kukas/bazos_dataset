from glob import glob
import os
import csv
import pandas
from datetime import datetime

def parse_csvs(csv_files):
    all_lines = []
    for csv_file in csv_files:
        with open(csv_file, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if len(row) != 5:
                    print(f"Not enough values in file {csv_file} row {row}")
                    continue
                
                title, description, link, date, category = row
                # extract the price at the end of the title
                # the price separator changed from - to : at some point
                try:
                    title_reversed = title[::-1]
                    dash = title_reversed.find("-")
                    colon = title_reversed.find(":")
                    split_on = "-"
                    if dash != -1 and colon != -1:
                        if dash < colon:
                            split_on = "-"
                        else:
                            split_on = ":"
                    else:
                        if dash != -1:
                            split_on = "-"
                        elif colon != -1:
                            split_on = ":"
                        else:
                            pass
                    title_split = title.rsplit(split_on, 1)
                    title, price = title_split
                except:
                    print(f"Error in file {csv_file} row {row}")
                title = title.strip()
                price = price.strip()
                
                # remove image from the begining of description
                # obr = description.find('/>')
                # if obr:
                #     description = description[obr+2:]

                # parse the price
                price_int = price.replace(" ", "")
                try:
                    price_int = int(price_int)
                except ValueError:
                    price_int = None
                
                # parse the date
                date = datetime.strptime(date, "%a, %d %b %Y %H:%M:%S %z")

                all_lines.append({
                    "title": title,
                    "price": price_int,
                    "price_string": price,
                    # "description": description,
                    "link": link,
                    "datetime": date,
                    # "category": category
                })

    df = pandas.DataFrame(all_lines)
    print(f"Loaded {len(df)} rows")
    return df


sections = [
    "zv",
    "de",
    "re",
    "pr",
    "au",
    "mt",
    "st",
    "du",
    "pc",
    "mo",
    "fo",
    "el",
    "sp",
    "hu",
    "vs",
    "kn",
    "na",
    "ob",
    "sl",
    "os",
]

os.makedirs("output_merged", exist_ok=True)

total = 0
for section in sections:
    print(f"Processing section {section}")
    df = parse_csvs(glob(f"output*/section_{section}*.csv"))
    print(f"Saving section {section}")
    total = total + len(df)
    df.to_pickle(f"output_merged/section_{section}.pkl.gz")

print(f"Exported {total} rows")