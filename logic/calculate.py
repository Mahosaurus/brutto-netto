from copy import deepcopy
from collections import OrderedDict

def marginal_netto(results: dict):
    """
    Calculates the net change in income
    results: dict (All information)
    vals: dict (Income: Delta)
    """
    vals = OrderedDict()
    marg_gain = []
    for entry in results:
        if not marg_gain:
            marg_gain.append(entry['Netto_Monat'])
            last = deepcopy(entry['Netto_Monat'])   
        else:
            marg_gain.append(int(entry['Netto_Monat'])-last)
            vals[int(entry['Brutto_Monat'])] = int(entry['Netto_Monat']-last)
            last = deepcopy(entry['Netto_Monat'])
    print(vals)
    return vals


def perc_netto(results: dict):
    """
    Calculates the share of netto to brutto
    results: dict (All information)
    vals: dict (Income: Delta)
    """
    vals = OrderedDict()
    for entry in results:
        vals[int(entry['Brutto_Monat'])] = int(entry['Netto_Monat']) / int(entry['Brutto_Monat']) * 100
    print(vals)
    return vals