import re

from collections import OrderedDict
import numpy as np
from bs4 import BeautifulSoup

def sort_dict(diction):
    """ Sorts the dict alphabetically """
    out = OrderedDict()
    for key in sorted(diction.keys()):
        out[key] = diction[key]
    return out

def parse_res(respons):
    """ Parses response from website """
    parsed_html = BeautifulSoup(respons, features="html.parser")
    text = parsed_html.body.find('div', attrs={'class':'calculator_area'}).text
    text = re.sub(r'[\s]+', ' ', text)
    text = re.sub(r'[^a-zA-Z\d\s\,\.]+', '', text)
    text = text.replace("Renten versicherung", "Rentenversicherung")
    text = text.replace("Kranken versicherung", "Krankennversicherung")
    text = text.replace("Pflege versicherung", "Pflegeversicherung")
    text = text.replace("Arbeitslosen versicherung", "Arbeitslosenversicherung")
    text = text.replace("Solidaritts zuschlag", "Solidaritätszuschlag")

    values = {}
    cur_entity = ""
    list_of_entities = ["Brutto", "Vorteil", "Solidaritätszuschlag", "Kirchensteuer",
                        "Lohnsteuer", "Steuern", "Sozialabgaben",
                        "Rentenversicherung", "Krankennversicherung",
                        "Pflegeversicherung", "Arbeitslosenversicherung", "Netto"]
    for word in text.split():
        if word in list_of_entities:
            cur_entity = word
            continue
        if cur_entity in list_of_entities:
            if cur_entity + "_Monat" not in values:
                values[cur_entity + '_Monat'] = np.float(word.replace(".", "").replace(",", "."))
            elif cur_entity + "_Jahr" not in values:
                values[cur_entity + '_Jahr'] = np.float(word.replace(".", "").replace(",", "."))
            else:
                continue
    values = sort_dict(values)
    return values

if __name__ == "__main__":
    print(parse_res("abc"))
