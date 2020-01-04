from collections import OrderedDict
from logic.calculate import marginal_netto, perc_netto, adapter

def test_marginal_netto():
    sample = [OrderedDict([('Brutto_Monat', 4000), ('Netto_Monat', 2000)]),
              OrderedDict([('Brutto_Monat', 4100), ('Netto_Monat', 2050)]),
              OrderedDict([('Brutto_Monat', 4200), ('Netto_Monat', 2100)]),
              OrderedDict([('Brutto_Monat', 4300), ('Netto_Monat', 2140)]),
              OrderedDict([('Brutto_Monat', 4400), ('Netto_Monat', 2170)]),
              OrderedDict([('Brutto_Monat', 4500), ('Netto_Monat', 2190)]),]
    res = marginal_netto(sample)
    assert res == OrderedDict([(4100, 50), (4200, 50), (4300, 40), (4400, 30), (4500, 20)])


def test_perc_netto():
    sample = [OrderedDict([('Brutto_Monat', 4000), ('Netto_Monat', 2000)]),
              OrderedDict([('Brutto_Monat', 4100), ('Netto_Monat', 2050)]),
              OrderedDict([('Brutto_Monat', 4200), ('Netto_Monat', 2100)]),
              OrderedDict([('Brutto_Monat', 4300), ('Netto_Monat', 2140)]),
              OrderedDict([('Brutto_Monat', 4400), ('Netto_Monat', 2170)]),
              OrderedDict([('Brutto_Monat', 4500), ('Netto_Monat', 450)]),]
    res = perc_netto(sample)
    assert res == OrderedDict([(4000, 50), (4100, 50), (4200, 50), (4300, 49), (4400, 49), (4500, 10)])

def test_adapter():
    sample = [OrderedDict([('Brutto_Monat', 4000), ('Netto_Monat', 1500), ('Rentenversicherung_Monat', 500)]),
              OrderedDict([('Brutto_Monat', 4100), ('Netto_Monat', 1550), ('Rentenversicherung_Monat', 500)]),
              OrderedDict([('Brutto_Monat', 4200), ('Netto_Monat', 1600), ('Rentenversicherung_Monat', 500)]),
              OrderedDict([('Brutto_Monat', 4300), ('Netto_Monat', 1640), ('Rentenversicherung_Monat', 500)]),
              OrderedDict([('Brutto_Monat', 4400), ('Netto_Monat', 1670), ('Rentenversicherung_Monat', 500)]),
              OrderedDict([('Brutto_Monat', 4500), ('Netto_Monat', 1690), ('Rentenversicherung_Monat', 500)]),]
    res = adapter("marg_netto_wo_pension", sample)
    assert res == OrderedDict([(4100, 50), (4200, 50), (4300, 40), (4400, 30), (4500, 20)])

    sample = [OrderedDict([('Brutto_Monat', 4000), ('Netto_Monat', 1500), ('Rentenversicherung_Monat', 500)]),
                OrderedDict([('Brutto_Monat', 4100), ('Netto_Monat', 1550), ('Rentenversicherung_Monat', 500)]),
                OrderedDict([('Brutto_Monat', 4200), ('Netto_Monat', 1600), ('Rentenversicherung_Monat', 500)]),
                OrderedDict([('Brutto_Monat', 4300), ('Netto_Monat', 1640), ('Rentenversicherung_Monat', 500)]),
                OrderedDict([('Brutto_Monat', 4400), ('Netto_Monat', 1670), ('Rentenversicherung_Monat', 500)]),
                OrderedDict([('Brutto_Monat', 4500), ('Netto_Monat',  -50), ('Rentenversicherung_Monat', 500)]),]
    res = adapter("perc_netto_wo_pension", sample)
    assert res == OrderedDict([(4000, 50), (4100, 50), (4200, 50), (4300, 49), (4400, 49), (4500, 10)])

