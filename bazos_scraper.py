from argparse import ArgumentParser

import feedparser
import logging
import csv
import os
import time
import random


class FeedWatcher:
    def __init__(self, id, url, output_path, category_name):
        self.url = url
        self.output_path = output_path
        self.category_name = category_name
        self.last_timedate = None
        self.fieldnames = ["title", "summary", "link", "published", "category"]
        self.last_update = time.time()
        self.next_update = time.time()
        self.interval = 600
        self.logger = logging.getLogger(name=id)

    def _extract_interesting(self, entry):
        return {key: value for key, value in entry.items() if key in self.fieldnames}

    def parse_new_entries(self):
        self.logger.info(f"parsing {self.url}")
        try:
            d = feedparser.parse(self.url)
        except Exception as e:
            # catch the http.client.RemoteDisconnected error
            self.logger.error(f"Error while parsing {self.url}: {e}")
            # Bazos might be blocking our requests, lets wait
            time.sleep(120)
            return []

        if d["bozo"]:
            self.logger.warning(f"got bozo flag {d}")
            return []

        if d["status"] == 403:
            self.logger.warning(f"got 403 Forbidden response status {d}")

            # Bazos is probably blocking our requests, lets wait
            time.sleep(120)

            return []

        if "entries" not in d:
            self.logger.warning(f"no entries {d}")
            return []

        if not d["entries"]:
            self.logger.warning(f"empty entries {d}")

            # double the interval to next refresh until refreshing once per day
            self.interval = min(self.interval * 2, 24 * 60 * 60)
            self.next_update = time.time() + self.interval

            return []

        entries = d["entries"]
        entries.reverse()

        max_timedate = max([entry["published_parsed"] for entry in entries])
        min_timedate = min([entry["published_parsed"] for entry in entries])
        middle_timedate = entries[int(len(entries) / 2)]["published_parsed"]

        if len(entries) == 1:
            self.logger.info(
                f"Got only one entry in response, computing seconds_between_entries with respect to current time"
            )
            seconds_between_entries = time.time() - time.mktime(min_timedate)
            seconds_between_newest_and_middle = seconds_between_entries / 2
        else:
            seconds_between_entries = time.mktime(max_timedate) - time.mktime(
                min_timedate
            )
            seconds_between_newest_and_middle = time.mktime(max_timedate) - time.mktime(
                middle_timedate
            )

        self.logger.info(
            f"Time between first and last entry is {seconds_between_entries} seconds, half {seconds_between_entries/2}. Time between first and middle entry is {seconds_between_newest_and_middle}"
        )

        seconds_between_15_entries = min(
            seconds_between_newest_and_middle, seconds_between_entries / 2
        )

        if seconds_between_15_entries > self.interval:
            # smoothing when we increase the interval
            interval = self.interval + 0.5 * (
                seconds_between_15_entries - self.interval
            )
        else:
            # no smoothing when we decrease
            interval = seconds_between_15_entries

        interval = int(max(interval, 600))

        # if interval > 24*60*60:
        #     self.logger.info(f"New interval is too long, capping")
        #     a = int(24*60*60)
        #     b = int(min(interval+1, 48*60*60))
        #     interval = random.randint(a, b)

        if interval != self.interval:
            self.logger.info(
                f"Setting update interval to {interval}, was {self.interval}"
            )
            self.interval = interval

        if len(entries) == 30 and time.mktime(min_timedate) > self.last_update:
            self.logger.warning(
                f"We might have skipped some entries!!! Watcher: {self.url}"
            )

        self.last_update = time.time()
        self.next_update = time.time() + self.interval

        if self.last_timedate is not None:
            entries = [
                entry
                for entry in entries
                if entry["published_parsed"] > self.last_timedate
            ]

        entries = [self._extract_interesting(entry) for entry in entries]

        self.last_timedate = max_timedate

        # for entry in entries:
        #     entry["category"] = self.category_name

        return entries

    def append_to_file(self, new_entries):
        if new_entries:
            # Check if output path exists
            # write header if not
            # write_header = not os.path.isfile(self.output_path)

            self.logger.info(
                f"Writing {len(new_entries)} new entries to {self.output_path}"
            )

            with open(self.output_path, "a", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=self.fieldnames)

                # if write_header:
                #     self.logger.info(f"write header to {self.output_path}")
                #     writer.writeheader()

                writer.writerows(new_entries)
        else:
            self.logger.info(f"Skip writing, we have no new entries")

    def run(self):
        current_time = time.time()
        if self.next_update is None or current_time > self.next_update:
            new_entries = self.parse_new_entries()
            self.append_to_file(new_entries)
            return True
        else:
            self.logger.debug(f"This watcher does not need update")
            return False


def watcher_settings_generator(output_dir, sections, categories):
    for sec in sections:
        if sec in categories:
            for cat, cat_name in categories[sec]:
                id = f"section_{sec}_category_{cat}"
                url = f"https://www.bazos.cz/rss.php?rub={sec}&cat={cat}"
                output_path = os.path.join(output_dir, f"{id}.csv")
                yield id, url, output_path, cat_name
        else:
            id = f"section_{sec}"
            url = f"https://www.bazos.cz/rss.php?rub={sec}"
            output_path = os.path.join(output_dir, f"{id}.csv")
            yield id, url, output_path, None


def main(output_dir):
    logging.getLogger().setLevel(logging.INFO)
    logging.basicConfig(
        format="%(asctime)s.%(msecs)03d %(levelname)s %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

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
    # categories = {}
    categories = {
        #     "zv": [(44, "Akvarijní rybičky"),(45, "Drobní savci"),(47, "Kočky"),(46, "Koně"),(61, "Koně - potřeby"),(48, "Psi"),(49, "Ptactvo"),(50, "Terarijní zvířata"),(51, "Ostatní domácí zvířata"),(53, "Krytí"),(427, "Ztraceni a nalezeni"),(52, "Chovatelské potřeby"),(55, "Drůbež"),(56, "Králíci"),(57, "Ovce a kozy"),(58, "Prasata"),(59, "Skot"),(60, "Ostatní hospodářská zvířata")],
        "de": [
            (117, "Autosedačky"),
            (118, "Baby monitory, chůvičky"),
            (119, "Hračky"),
            (120, "Chodítka a hopsadla"),
            (121, "Kočárky"),
            (122, "Kojenecké potřeby"),
            (456, "Kola"),
            (123, "Nábytek pro děti"),
            (124, "Nosítka"),
            (127, "Odrážedla"),
            (128, "Sedačky na kolo"),
            (129, "Sportovní potřeby"),
            (130, "Školní potřeby"),
            (132, "Ostatní"),
            (133, "Body, dupačky a overaly"),
            (134, "Bundy a kabátky"),
            (135, "Čepice a kloboučky"),
            (136, "Kalhoty, kraťasy a tepláky"),
            (137, "Kombinézy"),
            (442, "Komplety"),
            (138, "Mikiny a svetry"),
            (126, "Obuv"),
            (139, "Plavky"),
            (140, "Ponožky a punčocháče"),
            (141, "Pyžámka a župánky"),
            (142, "Rukavice a šály"),
            (143, "Spodní prádlo"),
            (144, "Sukýnky a šatičky"),
            (145, "Trička a košile"),
            (125, "Ostatní oblečení"),
        ],
        #     "pr": [(277, "Administrativa"),(300, "Brigády"),(278, "Chemie a potravinářství"),(279, "Doprava a logistika"),(280, "Finance a ekonomika"),(281, "IT a telekomunikace"),(283, "Management"),(282, "Marketing a reklama"),(284, "Obchod a prodej"),(285, "Obrana a bezpečnost"),(286, "Pohostinství a ubytování"),(287, "Práce v domácnosti"),(288, "Právo, legislativa"),(289, "Průmysl a výroba"),(290, "Řemeslné práce"),(291, "Servis a služby"),(293, "Stavebnictví"),(294, "Technika a energetika"),(295, "Tisk a polygrafie"),(296, "Výzkum a vývoj"),(297, "Vzdělávání a personalistika"),(298, "Zdravotnictví"),(299, "Zemědělství"),(301, "Ostatní")],
        "au": [
            (443, "Alfa Romeo"),
            (80, "Audi"),
            (81, "BMW"),
            (396, "Chevrolet"),
            (82, "Citroën"),
            (461, "Dacia"),
            (83, "Fiat"),
            (84, "Ford"),
            (395, "Honda"),
            (85, "Hyundai"),
            (397, "Kia"),
            (86, "Mazda"),
            (87, "Mercedes-Benz"),
            (445, "Mitsubishi"),
            (88, "Nissan"),
            (89, "Opel"),
            (90, "Peugeot"),
            (91, "Renault"),
            (92, "Seat"),
            (398, "Suzuki"),
            (93, "Škoda"),
            (94, "Toyota"),
            (95, "Volkswagen"),
            (96, "Volvo"),
            (98, "Havarovaná"),
            (97, "Ostatní značky"),
            (99, "Náhradní díly"),
            (106, "Pneumatiky, kola"),
            (428, "Příslušenství"),
            (107, "Tuning"),
            (108, "Veteráni"),
            (109, "Autobusy"),
            (101, "Dodávky"),
            (110, "Karavany, vozíky"),
            (102, "Mikrobusy"),
            (111, "Nákladní auta"),
            (100, "Pick-up"),
            (103, "Ostatní užitková"),
            (104, "Havarovaná užitková"),
            (105, "Náhradní díly užitková"),
        ],
        # "mt": [(191, "Cestovní motocykly"),(193, "Chopper"),(192, "Čtyřkolky"),(194, "Enduro"),(195, "Minibike"),(196, "Mopedy"),(197, "Silniční motocykly"),(198, "Skútry"),(200, "Skútry sněžné"),(199, "Skútry vodní"),(201, "Tříkolky"),(202, "Veteráni"),(203, "Náhradní díly"),(204, "Oblečení, obuv, helmy"),(205, "Ostatní")],
        # "st": [(174, "Čerpadla"),(175, "Čistící stroje"),(176, "Dřevoobráběcí stroje"),(177, "Generátory"),(178, "Historické stroje"),(179, "Kovoobráběcí stroje"),(180, "Motory"),(181, "Potravinářské stroje"),(182, "Skladová technika"),(183, "Stavební stroje"),(184, "Textilní stroje"),(185, "Tiskařské stroje"),(186, "Vybavení provozoven"),(187, "Výrobní linky"),(188, "Zemědělská technika"),(189, "Náhradní díly"),(190, "Ostatní")],
        "du": [
            (302, "Bazény"),
            (303, "Čerpadla"),
            (451, "Dveře, vrata"),
            (304, "Klimatizace"),
            (305, "Kotle, Kamna, Bojlery"),
            (306, "Malotraktory, Kultivátory"),
            (307, "Míchačky"),
            (308, "Nářadí"),
            (452, "Okna"),
            (453, "Pily"),
            (309, "Radiátory"),
            (310, "Rostliny"),
            (311, "Sekačky"),
            (312, "Sněžná technika"),
            (313, "Stavební materiál"),
            (314, "Vybavení dílen"),
            (315, "Vysavače/Foukače"),
            (316, "Zahradní grily"),
            (318, "Zahradní technika"),
            (319, "Ostatní"),
        ],
        "pc": [
            (27, "Chladiče"),
            (1, "DVD, Blu-ray mechaniky"),
            (32, "GPS navigace"),
            (4, "Grafické karty"),
            (5, "Hard disky, SSD"),
            (25, "Herní konzole"),
            (29, "Herní zařízení"),
            (30, "Hry"),
            (6, "Klávesnice, myši"),
            (7, "Kopírovací stroje"),
            (9, "LCD monitory"),
            (2, "Modemy"),
            (26, "MP3 přehrávače"),
            (10, "Notebooky"),
            (11, "Paměti"),
            (12, "PC, Počítače"),
            (13, "Procesory"),
            (15, "Scanery"),
            (14, "Síťové prvky"),
            (16, "Skříně, zdroje"),
            (17, "Software"),
            (31, "Spotřební materiál"),
            (24, "Tablety, E-čtečky"),
            (18, "Tiskárny"),
            (28, "Wireless, WiFi"),
            (19, "Základní desky"),
            (20, "Záložní zdroje"),
            (21, "Zvukové karty"),
            (22, "Ostatní"),
        ],
        # "mo": [(439, "Apple"),(440, "HTC"),(347, "Huawei, Honor"),(343, "LG"),(344, "Motorola, Lenovo"),(345, "Nokia, Microsoft"),(346, "Samsung"),(348, "Sony"),(455, "Xiaomi"),(349, "Ostatní značky"),(353, "Baterie"),(350, "Bezdrátové telefony"),(354, "Datové kabely"),(351, "Faxy"),(355, "Headsety"),(356, "HF Sady do auta"),(454, "Chytré hodinky"),(444, "Kryty"),(357, "Nabíječky"),(358, "Paměťové karty"),(352, "Stolní telefony"),(360, "Ostatní")],
        #     "fo": [(447, "Analogové fotoaparáty"),(146, "Digitální fotoaparáty"),(460, "Drony"),(148, "Videokamery"),(147, "Zrcadlovky"),(149, "Baterie"),(446, "Blesky a osvětlení"),(150, "Brašny a pouzdra"),(151, "Datové kabely"),(152, "Filtry"),(153, "Nabíječky baterií"),(154, "Objektivy"),(155, "Paměťové karty"),(156, "Stativy"),(157, "Ostatní")],
        "el": [
            (371, "Autorádia"),
            (361, "Digestoře"),
            (373, "Domácí kina"),
            (382, "Epilátory, Depilátory"),
            (383, "Fény, Kulmy"),
            (374, "Hifi systémy, Rádia"),
            (384, "Holící strojky"),
            (385, "Kávovary"),
            (363, "Ledničky"),
            (364, "Mikrovlnné trouby"),
            (365, "Mrazáky"),
            (366, "Myčky"),
            (386, "Nabíječky baterií"),
            (367, "Pračky"),
            (376, "Projektory"),
            (377, "Repro soustavy"),
            (387, "Ruční šlehače, Mixéry"),
            (389, "Šicí stroje"),
            (372, "Sluchátka"),
            (368, "Sporáky"),
            (369, "Sušičky"),
            (388, "Svítidla, Lampy"),
            (378, "Televize"),
            (379, "Video, DVD přehrávače"),
            (390, "Vysavače"),
            (391, "Vysílačky"),
            (380, "Zesilovače"),
            (392, "Zvlhčovače vzduchu"),
            (393, "Žehličky"),
            (370, "Ostatní - bílá"),
            (381, "Ostatní audio video"),
            (394, "Ostatní drobné"),
        ],
        "sp": [
            (243, "Fitness, jogging"),
            (245, "Fotbal"),
            (244, "Golf"),
            (246, "In-line, Skateboarding"),
            (242, "Kempink"),
            (448, "Letectví"),
            (247, "Míčové hry"),
            (248, "Myslivost, lov"),
            (249, "Paintball, airsoft"),
            (250, "Rybaření"),
            (251, "Společenské hry"),
            (252, "Tenis, squash, badminton"),
            (253, "Turistika, horolezectví"),
            (254, "Vodní sporty, potápění"),
            (255, "Vše ostatní"),
            (450, "Koloběžky"),
            (256, "Horská kola"),
            (257, "Silniční kola"),
            (258, "Součástky a díly"),
            (259, "Ostatní cyklistika"),
            (449, "Běžkování"),
            (260, "Lyžování"),
            (463, "Skialpy"),
            (261, "Snowboarding"),
            (262, "Hokej, bruslení"),
            (263, "Ostatní zimní"),
        ],
        #     "hu": [(158,"Bicí nástroje"),(159,"Dechové nástroje"),(160,"Klávesové nástroje"),(161,"Smyčcové nástroje"),(162,"Strunné nástroje"),(163,"Ostatní nástroje"),(164,"DVD, CD, MC, LP"),(165,"Hudebníci a skupiny"),(166,"Koncerty"),(168,"Noty, texty"),(169,"Světelná technika"),(171,"Zkušebny"),(172,"Zvuková technika"),(173,"Ostatní"),],
        #     "vs": [(268,"Dálniční známky"),(269,"Dárkové poukazky"),(276,"Jízdenky"),(264,"Letenky"),(274,"Permanentky"),(265,"Divadlo"),(266,"Festivaly"),(267,"Hudba, Koncerty"),(270,"Pro děti"),(271,"Společenské akce"),(272,"Sport"),(273,"Výstavy"),(275,"Ostatní"),],
        #     "kn": [(320,"Beletrie"),(321,"Časopisy"),(342,"Cizojazyčná literatura"),(322,"Detektivky"),(323,"Dětská literatura"),(324,"Drama"),(325,"Encyklopedie"),(326,"Esoterika"),(327,"Historické romány"),(328,"Hobby, odborné knihy"),(329,"Kuchařky"),(330,"Mapy, cestovní průvodci"),(332,"Počítačová literatura"),(333,"Pro mládež"),(334,"Romány pro ženy"),(335,"Sci-fi, Fantasy"),(341,"Učebnice, skripta - Jazykové"),(337,"Učebnice, skripta - SŠ"),(336,"Učebnice, skripta - VŠ"),(340,"Učebnice, skripta - ZŠ"),(338,"Zábavná"),(339,"Zdravý životní styl"),(331,"Ostatní"),],
        "na": [
            (206, "Jídelní kouty"),
            (207, "Knihovny"),
            (208, "Koberce a podlah. krytina"),
            (209, "Koupelny"),
            (210, "Křesla a gauče"),
            (211, "Kuchyně"),
            (212, "Lampy, osvětlení"),
            (213, "Ložnice"),
            (214, "Matrace"),
            (215, "Obývací stěny"),
            (216, "Postele"),
            (217, "Sedací soupravy"),
            (218, "Skříně"),
            (219, "Stoly"),
            (220, "Zahradní nábytek"),
            (221, "Židle"),
            (429, "Doplňky"),
            (222, "Ostatní nábytek"),
        ],
        "ob": [
            (419, "Batohy, Kufry"),
            (420, "Boty"),
            (426, "Bundy a Kabáty"),
            (399, "Čepice a Šátky"),
            (421, "Doplňky"),
            (400, "Džíny"),
            (401, "Halenky"),
            (422, "Hodinky"),
            (423, "Kabelky"),
            (402, "Kalhoty"),
            (403, "Košile"),
            (404, "Kožené oděvy"),
            (405, "Mikiny"),
            (406, "Obleky a Saka"),
            (407, "Plavky"),
            (462, "Roušky"),
            (408, "Rukavice a Šály"),
            (414, "Šaty, Kostýmky"),
            (415, "Šortky"),
            (424, "Šperky"),
            (409, "Spodní prádlo"),
            (410, "Sportovní oblečení"),
            (411, "Sukně"),
            (412, "Svatební šaty"),
            (416, "Těhotenské oblečení"),
            (413, "Svetry"),
            (417, "Termo prádlo"),
            (418, "Trička, tílka"),
            (425, "Ostatní"),
        ],
        #     "sl": [(430,"Auto Moto"),(223,"Cestování"),(224,"Domácí práce"),(431,"Esoterika"),(227,"Hlídání dětí"),(228,"IT, webdesign"),(441,"Koně - služby"),(229,"Kurzy a školení"),(432,"Opravy, servis"),(433,"Pořádání akcí"),(434,"Právo a bezpečnost"),(230,"Překladatelství"),(231,"Přeprava a Stěhování"),(435,"Půjčovny"),(436,"Realitní služby"),(239,"Reklama na auto"),(240,"Reklamní plochy - ostatní"),(232,"Řemeslné a stavební práce"),(54,"Služby pro zvířata"),(438,"Tvůrčí služby"),(234,"Ubytování"),(226,"Účetnictví, poradenství"),(235,"Úklid"),(437,"Výroba"),(241,"Výuka hudby"),(225,"Výuka, doučování"),(238,"Zdraví a krása"),(236,"Zprostředkovatelské služby"),(237,"Ostatní"),],
        "os": [
            (458, "Mince, bankovky"),
            (457, "Modelářství"),
            (36, "Potraviny"),
            (37, "Sběratelství"),
            (38, "Sklo, keramika"),
            (39, "Starožitnosti"),
            (41, "Umělecké předměty"),
            (42, "Zdraví a krása"),
            (459, "Známky, pohledy"),
            (43, "Ostatní"),
        ],
    }

    # output_dir = "output3"
    os.makedirs(output_dir, exist_ok=True)

    watchers = []
    for id, url, output_path, category_name in watcher_settings_generator(
        output_dir, sections, categories
    ):
        watcher = FeedWatcher(id, url, output_path, category_name)
        watchers.append(watcher)

    rss_refresh_time = 600
    # wait_for = rss_refresh_time / len(watchers)
    wait_for = 12

    logging.info(f"We have {len(watchers)} watchers")
    logging.info(f"Setting the delay between requests to {wait_for:.2f} seconds")

    while True:
        start = time.time()
        for watcher in watchers:
            sent_request = watcher.run()
            if sent_request:
                time.sleep(wait_for)

        end = time.time()
        duration = end - start
        logging.info(f"This scrape loop took {duration:.2f} seconds")

        num_fastest_watchers = sum(
            1 if watcher.interval == 600 else 0 for watcher in watchers
        )
        logging.info(
            f"We have {num_fastest_watchers} watchers refreshing every 600 seconds"
        )

        if duration > rss_refresh_time:
            logging.warning(
                f"This scrape loop took longer than the {rss_refresh_time} second refresh duration"
            )

        # wait for the next watcher event
        earliest_event = min([watcher.next_update for watcher in watchers])
        # logging.info(f"next update is on {earliest_event:.2f}")

        wait_next_refresh = earliest_event - time.time()
        if wait_next_refresh > 0:
            logging.info(f"Wait {wait_next_refresh:.2f} seconds for next event")
            time.sleep(wait_next_refresh)
        else:
            logging.info(f"Start the new scrape loop immediately")


if __name__ == "__main__":
    ap = ArgumentParser(description="Bazos RSS feed scraper")
    ap.add_argument("output_dir", type=str, help="Path to output directory")
    args = ap.parse_args()

    main(args.output_dir)
