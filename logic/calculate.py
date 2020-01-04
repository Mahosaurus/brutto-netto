from copy import deepcopy
from collections import OrderedDict

def adapter(request, results):
    if request == "marg_netto":
        return marginal_netto(results)
    if request == "perc_netto":
        return perc_netto(results)
    if request == "marg_netto_wo_pension":
        for entry in results:
            entry['Netto_Monat'] = entry['Netto_Monat'] + entry['Rentenversicherung_Monat']
        return marginal_netto(results)
    if request == "perc_netto_wo_pension":
        for entry in results:
            entry['Netto_Monat'] = entry['Netto_Monat'] + entry['Rentenversicherung_Monat']
        return perc_netto(results)

def marginal_netto(results: list):
    """
    Calculates the net out of an increase in income in %
    x = (Netto(t+1)-Netto(t))/(Brutto(t+1)-Brutto(t)) * 100
    results: dict (All information)
    vals: dict (Income: Delta)
    """
    vals = OrderedDict()
    netto = []
    brutto = []

    for entry in results:
        if not netto:
            netto.append(entry['Netto_Monat'])
            brutto.append(entry['Brutto_Monat'])
            last_netto = deepcopy(entry['Netto_Monat'])
            last_brutto = deepcopy(entry['Brutto_Monat'])
        else:
            netto.append(int(entry['Netto_Monat'])-last_netto)
            brutto.append(int(entry['Brutto_Monat'])-last_brutto)
            vals[int(entry['Brutto_Monat'])] = int((entry['Netto_Monat']-last_netto)/(entry['Brutto_Monat']-last_brutto) * 100)
            last_netto = deepcopy(entry['Netto_Monat'])
            last_brutto = deepcopy(entry['Brutto_Monat'])
    print(vals)
    return vals


def perc_netto(results: list):
    """
    Calculates the share of netto to brutto in %
    x = Netto/Brutto * 100
    results: dict (All information)
    vals: dict (Income: Average percentage)
    """
    vals = OrderedDict()
    for entry in results:
        vals[int(entry['Brutto_Monat'])] = int(entry['Netto_Monat'] / entry['Brutto_Monat'] * 100)
    print(vals)
    return vals