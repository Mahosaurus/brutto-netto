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

    return vals