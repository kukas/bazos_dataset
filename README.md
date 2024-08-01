# Bazoš.cz dataset

This dataset comprises two years' worth of postings from Bazoš.cz, the largest marketplace in the Czech Republic for second-hand goods and various short-term advertisements. 

In this repository, I release:
- Python script used for scraping Bazoš.cz
- Script used for post-processing the scraped data
- Dataset description
- Examples of usage
- Links to download the data.

The dataset contains approx. 29 million short advertisements in Czech with title, price, date, permalink and category. 

The main categories are Cars, Children, House and Garden, Electronics, Photography, Music, Books, Mobiles, Motorcycles, Furniture, Clothing, PC, Jobs, Real Estate, Services, Sports, Machinery, Tickets, Animals and Others.

## Český popis

Tento dataset obsahuje dva roky inzercí z největšího českého internetového bazaru Bazoš.cz. 

V tomto repozitáři najdete:
- Skript pro stahování inzerátů z Bazoš.cz
- Skripty pro postprocessing stažených dat
- Popis datasetu
- Příklad použití
- Odkazy ke stažení

Archiv obsahuje téměř 29 milionů inzerátů v češtině. Každý inzerát obsahuje titulek, cenu, datum uveřejnění, odkaz a kategorii. Kategorie jsou uvedeny v tabulce níže.

## Links to download

The dataset is split by category, which can be downloaded individually.

| Category | Number of posts | Link |
| --- | --- | --- |
| Auto | 7032202 | https://jirkabalhar.cz/bazos/section_au.pkl.gz |
| Děti | 3067307 | https://jirkabalhar.cz/bazos/section_de.pkl.gz |
| Ostatní | 2530611 | https://jirkabalhar.cz/bazos/section_os.pkl.gz |
| Dům a zahrada | 2012356 | https://jirkabalhar.cz/bazos/section_du.pkl.gz |
| Oblečení | 2025869 | https://jirkabalhar.cz/bazos/section_ob.pkl.gz |
| Sport | 1667275 | https://jirkabalhar.cz/bazos/section_sp.pkl.gz |
| Elektro | 1426289 | https://jirkabalhar.cz/bazos/section_el.pkl.gz |
| Stroje | 1140778 | https://jirkabalhar.cz/bazos/section_st.pkl.gz |
| PC | 1269895 | https://jirkabalhar.cz/bazos/section_pc.pkl.gz |
| Nábytek | 1316462 | https://jirkabalhar.cz/bazos/section_na.pkl.gz |
| Zvířata | 1084082 | https://jirkabalhar.cz/bazos/section_zv.pkl.gz |
| Motorky | 936476 | https://jirkabalhar.cz/bazos/section_mt.pkl.gz |
| Reality | 719888 | https://jirkabalhar.cz/bazos/section_re.pkl.gz |
| Knihy | 723850 | https://jirkabalhar.cz/bazos/section_kn.pkl.gz |
| Mobily | 666085 | https://jirkabalhar.cz/bazos/section_mo.pkl.gz |
| Hudba | 368105 | https://jirkabalhar.cz/bazos/section_hu.pkl.gz |
| Foto | 243657 | https://jirkabalhar.cz/bazos/section_fo.pkl.gz |
| Vstupenky | 139399 | https://jirkabalhar.cz/bazos/section_vs.pkl.gz |
| Služby | 107204 | https://jirkabalhar.cz/bazos/section_sl.pkl.gz |
| Práce | 102678 | https://jirkabalhar.cz/bazos/section_pr.pkl.gz |

## Notes
- The source of the data is the RSS feed of Bazoš.cz, which does not contain all information from the post.
- I removed the "description" column from the dataset because in some cases it contained contact information or other sensitive information.
- There are two gaps in the data scraped in October 2022 and in the spring of 2024.

## Privacy and legality
As far as I know, this is the only publicly available Czech dataset of this type and I hope it could be useful for research, personal use or other interesting applications. Please contact me if you have any questions or concerns.

According to the Bazoš.cz [terms of service](https://www.bazos.cz/podminky.php), the use of web-scrapers is not prohibited. I made sure that my scraping script was using as little requests as possible to not overload the servers.

The data does not contain any columns with any personal information. I removed the "description" column from the dataset because in some cases it contained contact information or other sensitive information. I also removed emails and phone numbers from the advert titles.
