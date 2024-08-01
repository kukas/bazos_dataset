# Bazoš.cz dataset
<p align="middle">
  <img src="/ps4_pro.png" width="450" /> 
</p>

This dataset comprises two years' worth of postings from Bazoš.cz, the largest marketplace in the Czech Republic for second-hand goods and various short-term advertisements. 

In this repository, I release:
- Python script used for scraping Bazoš.cz
- Script used for post-processing the scraped data
- Dataset description
- [Example of usage](bazos_example.ipynb)
- Links to download the data.

The period covered is from 1.5.2022 to 31.7.2024. The dataset contains approx. 29 million short advertisements in Czech with title, price, date, permalink and category. 

The main categories are Cars, Children, House and Garden, Electronics, Photography, Music, Books, Mobiles, Motorcycles, Furniture, Clothing, PC, Jobs, Real Estate, Services, Sports, Machinery, Tickets, Animals and Others.

## Český popis

Tento dataset obsahuje dva roky inzercí z největšího českého internetového bazaru Bazoš.cz. 

V tomto repozitáři najdete:
- Skript pro stahování inzerátů z Bazoš.cz
- Skripty pro postprocessing stažených dat
- Popis datasetu
- [Příklad použití](bazos_example.ipynb)
- Odkazy ke stažení

Archiv pokrývá období od 1.5.2022 do 31.7.2024 a obsahuje téměř 29 milionů inzerátů v češtině. Každý inzerát obsahuje titulek, cenu, datum uveřejnění, odkaz a kategorii. Kategorie jsou uvedeny v tabulce níže.

## Links to download

The dataset is split by category, which can be downloaded individually.

| Category | Number of posts | Link |
| --- | --- | --- |
| Auto | 7032202 | https://jirkabalhar.cz/bazos/section_au.csv.zip |
| Děti | 3067307 | https://jirkabalhar.cz/bazos/section_de.csv.zip |
| Ostatní | 2530611 | https://jirkabalhar.cz/bazos/section_os.csv.zip |
| Dům a zahrada | 2012356 | https://jirkabalhar.cz/bazos/section_du.csv.zip |
| Oblečení | 2025869 | https://jirkabalhar.cz/bazos/section_ob.csv.zip |
| Sport | 1667275 | https://jirkabalhar.cz/bazos/section_sp.csv.zip |
| Elektro | 1426289 | https://jirkabalhar.cz/bazos/section_el.csv.zip |
| Stroje | 1140778 | https://jirkabalhar.cz/bazos/section_st.csv.zip |
| PC | 1269895 | https://jirkabalhar.cz/bazos/section_pc.csv.zip |
| Nábytek | 1316462 | https://jirkabalhar.cz/bazos/section_na.csv.zip |
| Zvířata | 1084082 | https://jirkabalhar.cz/bazos/section_zv.csv.zip |
| Motorky | 936476 | https://jirkabalhar.cz/bazos/section_mt.csv.zip |
| Reality | 719888 | https://jirkabalhar.cz/bazos/section_re.csv.zip |
| Knihy | 723850 | https://jirkabalhar.cz/bazos/section_kn.csv.zip |
| Mobily | 666085 | https://jirkabalhar.cz/bazos/section_mo.csv.zip |
| Hudba | 368105 | https://jirkabalhar.cz/bazos/section_hu.csv.zip |
| Foto | 243657 | https://jirkabalhar.cz/bazos/section_fo.csv.zip |
| Vstupenky | 139399 | https://jirkabalhar.cz/bazos/section_vs.csv.zip |
| Služby | 107204 | https://jirkabalhar.cz/bazos/section_sl.csv.zip |
| Práce | 102678 | https://jirkabalhar.cz/bazos/section_pr.csv.zip |

## Notes
- The source of the data is the RSS feed of Bazoš.cz, which does not contain all information from the post.
- I removed the "description" column from the dataset because in some cases it contained sensitive information.
- There are two gaps in the data scraped in October 2022 and in the spring of 2024.

## Privacy and legality
As far as I know, this is the only publicly available Czech dataset of this type and I hope it could be useful for research, personal use or other interesting applications. Please contact me if you have any questions or concerns.

According to the Bazoš.cz [terms of service](https://www.bazos.cz/podminky.php), the use of web-scrapers is not prohibited. I made sure that my scraping script was using as little requests as possible to not overload the servers.

The data does not contain any columns with any personal information. I removed the "description" column from the dataset because in some cases it contained sensitive information. I also removed posts that contained sensitive information in the title.

## Licence 

The code is released under the GNU General Public License.
