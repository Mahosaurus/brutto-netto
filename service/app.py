import logging
import re
import sys
import io
import base64

import random
import string
import subprocess

from flask import Flask, render_template, request

from gevent.pywsgi import WSGIServer

sys.path.append("../")
from parse_res import parse_res
from request_page import request_form
from logic import calculate
from plots import plots

PORT = 80

# Detect OS
try:
    subprocess.run("ipconfig")
    print("PORT: ", PORT)
    windows = True
    linux = False
    print("Windows")
except Exception as exc:
    cmd = "ip a | grep 'inet 192'"
    ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = ps.communicate()[0]
    print(output)
    print("PORT: ", PORT)
    linux = True
    windows = False
    print("Linux")


if __name__ == '__main__':
    app = Flask(__name__)
    app.debug = True
    app.config['SECRET_KEY'] = ''.join(random.choice(string.ascii_lowercase) for _ in range(10))

    @app.route('/', methods=['GET', 'POST'])
    def provide():
        if request.method == "POST":
            # Single request
            if "[" not in request.form['f_bruttolohn']:
                respons = request_form.request_website(f_bruttolohn=request.form['f_bruttolohn'],
                                                       f_abrechnungszeitraum=request.form['f_abrechnungszeitraum'],
                                                       f_geld_werter_vorteil=request.form['f_geld_werter_vorteil'],
                                                       f_abrechnungsjahr=request.form['f_abrechnungsjahr'],
                                                       f_steuerfreibetrag=request.form['f_steuerfreibetrag'],
                                                       f_steuerklasse=request.form['f_steuerklasse'],
                                                       f_kirche=request.form['f_kirche'],
                                                       f_bundesland=request.form['f_bundesland'],
                                                       f_alter=request.form['f_alter'],
                                                       f_kinder=request.form['f_kinder'],
                                                       f_kinderfreibetrag=request.form['f_kinderfreibetrag'],
                                                       f_krankenversicherung=request.form['f_krankenversicherung'],
                                                       f_private_kv=request.form['f_private_kv'],
                                                       f_arbeitgeberzuschuss_pkv=request.form['f_arbeitgeberzuschuss_pkv'],
                                                       f_KVZ=request.form['f_KVZ'],
                                                       f_rentenversicherung=request.form['f_rentenversicherung'],
                                                       f_arbeitslosenversicherung=request.form['f_arbeitslosenversicherung'])
                respons = respons.decode("ISO-8859-1")
                parsed_respons = parse_res.parse_res(respons)
            # Range request
            else:
                range_to_check = re.sub(r'[^a-zA-Z\d\s\,\.]+', '', request.form['f_bruttolohn'])
                range_to_check = range_to_check.split(",")

                results = []
                for i in range(int(range_to_check[0].strip()),
                               int(range_to_check[1].strip()),
                               int(request.form['step'])):
                    app.logger.info("Getting" + str(i))
                    respons = request_form.request_website(f_bruttolohn=i,
                                                           f_abrechnungszeitraum=request.form['f_abrechnungszeitraum'],
                                                           f_geld_werter_vorteil=request.form['f_geld_werter_vorteil'],
                                                           f_abrechnungsjahr=request.form['f_abrechnungsjahr'],
                                                           f_steuerfreibetrag=request.form['f_steuerfreibetrag'],
                                                           f_steuerklasse=request.form['f_steuerklasse'],
                                                           f_kirche=request.form['f_kirche'],
                                                           f_bundesland=request.form['f_bundesland'],
                                                           f_alter=request.form['f_alter'],
                                                           f_kinder=request.form['f_kinder'],
                                                           f_kinderfreibetrag=request.form['f_kinderfreibetrag'],
                                                           f_krankenversicherung=request.form['f_krankenversicherung'],
                                                           f_private_kv=request.form['f_private_kv'],
                                                           f_arbeitgeberzuschuss_pkv=request.form['f_arbeitgeberzuschuss_pkv'],
                                                           f_KVZ=request.form['f_KVZ'],
                                                           f_rentenversicherung=request.form['f_rentenversicherung'],
                                                           f_arbeitslosenversicherung=request.form['f_arbeitslosenversicherung'])
                    respons = respons.decode("ISO-8859-1")
                    results.append(parse_res.parse_res(respons))

                # Logic
                marg_gain = calculate.marginal_netto(results)
                plotted = plots.plots(marg_gain)

                img = io.BytesIO()
                plotted.savefig(img, format='png')

                img.seek(0)
                plot_url = base64.b64encode(img.getvalue()).decode()

                return render_template("main.html", result={}, img='data:image/png;base64,{}'.format(plot_url))

        else:
            # Get Request
            parsed_respons = {}
        return render_template("main.html", result=parsed_respons)

    app.logger.info("Starting app...")
    # DEBUG
    if linux:
        app.run()
    # PRD
    if windows:
        HTTP_SERVER = WSGIServer(('0.0.0.0', int(PORT)), app)
        HTTP_SERVER.serve_forever()
