import pandas
from glob import glob
import os

category_names = {
    'zv': 'Zvířata',
    'de': 'Děti',
    're': 'Reality',
    'pr': 'Práce',
    'au': 'Auto',
    'mt': 'Motorky',
    'st': 'Stroje',
    'du': 'Dům a zahrada',
    'pc': 'PC',
    'mo': 'Mobily',
    'fo': 'Foto',
    'el': 'Elektro',
    'sp': 'Sport',
    'hu': 'Hudba',
    'vs': 'Vstupenky',
    'kn': 'Knihy',
    'na': 'Nábytek',
    'ob': 'Oblečení',
    'sl': 'Služby',
    'os': 'Ostatní',
}
files = glob("anon_output_merged/*.pkl.gz")
files = sorted(files, key=os.path.getsize, reverse=True)

for file in files:
    section = file.split("section_")[1].split(".pkl.gz")[0]
    df = pandas.read_pickle("anon_output_merged/section_" + section + ".pkl.gz")
    print("|", category_names[section], "|", len(df), "|", f"https://jirkabalhar.cz/bazos/section_{section}.pkl.gz", "|")