from collections import OrderedDict
from copy import deepcopy
from pprint import pprint
from request_page import request_form
from parse_res import parse_res

# Config
f_bruttolohn = "3000"
f_abrechnungszeitraum = "monat"
f_geld_werter_vorteil = ""
f_abrechnungsjahr = "2019"
f_steuerfreibetrag = ""
f_steuerklasse = "1"
f_kirche = "nein"
f_bundesland = "baden-wuerttemberg"
f_alter = "10"
f_kinder = "nein"
f_kinderfreibetrag = "0"
f_krankenversicherung = "pflichtversichert"
f_private_kv = ""
f_arbeitgeberzuschuss_pkv = "ja"
f_KVZ = "0.9"
f_rentenversicherung = "pflichtversichert"
f_arbeitslosenversicherung = "pflichtversichert"


# respons = request_form.request_website(f_bruttolohn = 3000,
#                                         f_abrechnungszeitraum = f_abrechnungszeitraum,
#                                         f_geld_werter_vorteil = f_geld_werter_vorteil,
#                                         f_abrechnungsjahr = f_abrechnungsjahr,
#                                         f_steuerfreibetrag = f_steuerfreibetrag,
#                                         f_steuerklasse = f_steuerklasse,
#                                         f_kirche = f_kirche,
#                                         f_bundesland = f_bundesland,
#                                         f_alter = f_alter,
#                                         f_kinder = f_kinder,
#                                         f_kinderfreibetrag = f_kinderfreibetrag,
#                                         f_krankenversicherung = f_krankenversicherung,
#                                         f_private_kv = f_private_kv,
#                                         f_arbeitgeberzuschuss_pkv = f_arbeitgeberzuschuss_pkv,
#                                         f_KVZ = f_KVZ,
#                                         f_rentenversicherung = f_rentenversicherung,
#                                         f_arbeitslosenversicherung = f_arbeitslosenversicherung)
# respons = respons.decode("ISO-8859-1")
# parsed_respons = parse_res.parse_res(respons)
# print(parsed_respons)                                   

vals = OrderedDict()
marg_gain = []
for i in range(3000, 8000, 100):
    respons = request_form.request_website(f_bruttolohn = str(i),
                                           f_abrechnungszeitraum = f_abrechnungszeitraum,
                                           f_geld_werter_vorteil = f_geld_werter_vorteil,
                                           f_abrechnungsjahr = f_abrechnungsjahr,
                                           f_steuerfreibetrag = f_steuerfreibetrag,
                                           f_steuerklasse = f_steuerklasse,
                                           f_kirche = f_kirche,
                                           f_bundesland = f_bundesland,
                                           f_alter = f_alter,
                                           f_kinder = f_kinder,
                                           f_kinderfreibetrag = f_kinderfreibetrag,
                                           f_krankenversicherung = f_krankenversicherung,
                                           f_private_kv = f_private_kv,
                                           f_arbeitgeberzuschuss_pkv = f_arbeitgeberzuschuss_pkv,
                                           f_KVZ = f_KVZ,
                                           f_rentenversicherung = f_rentenversicherung,
                                           f_arbeitslosenversicherung = f_arbeitslosenversicherung)

    respons = respons.decode("ISO-8859-1")
    parsed_respons = parse_res.parse_res(respons)
    netto = parsed_respons['Netto_Monat']
    if not marg_gain:
        marg_gain.append(0)
        last = deepcopy(netto)   
    else:
        marg_gain.append(int(netto-last))
        vals[i] = int(netto-last)
        last = deepcopy(netto)     

pprint(vals)