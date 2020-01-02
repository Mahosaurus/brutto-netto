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

def wrapper(request_form, bruttolohn=0):
    if bruttolohn == 0:
        bruttolohn = request.form['f_bruttolohn']
    return request_form.request_website(f_bruttolohn=bruttolohn,
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

if __name__ == '__main__':
    app = Flask(__name__)
    app.debug = True
    app.config['SECRET_KEY'] = ''.join(random.choice(string.ascii_lowercase) for _ in range(10))

    @app.route('/', methods=['GET', 'POST'])
    def provide():
        if request.method == "POST":
            app.logger.info(request.form)
            if request.form['f_how'] == '1': # Single request
                app.logger.info("single_netto")
                respons = wrapper(request_form)
                respons = respons.decode("ISO-8859-1")
                parsed_respons = parse_res.parse_res(respons)

            elif request.form['f_how'] == '2':
                app.logger.info("Marginal Netto")
                range_to_check = re.sub(r'[^a-zA-Z\d\s\,\.]+', '', request.form['f_bruttolohn'])
                range_to_check = range_to_check.split(",")

                results = []
                for i in range(int(range_to_check[0].strip()),
                               int(range_to_check[1].strip()),
                               int(request.form['step'])):

                    app.logger.info("Getting" + str(i))

                    respons = wrapper(request_form, bruttolohn=i)
                    respons = respons.decode("ISO-8859-1")
                    results.append(parse_res.parse_res(respons))

                # Logic
                marg_gain = calculate.marginal_netto(results)

                plotted_marg_gain = plots.plots(marg_gain)
                img1 = io.BytesIO()
                plotted_marg_gain.savefig(img1, format='png')
                img1.seek(0)
                plot_url_marg_gain = base64.b64encode(img1.getvalue()).decode()

                return render_template("main.html",
                                       result={},
                                       img1='data:image/png;base64,{}'.format(plot_url_marg_gain))

            # Range request
            elif request.form['f_how'] == '3':
                app.logger.info("Percentage Netto")
                range_to_check = re.sub(r'[^a-zA-Z\d\s\,\.]+', '', request.form['f_bruttolohn'])
                range_to_check = range_to_check.split(",")

                results = []
                for i in range(int(range_to_check[0].strip()),
                               int(range_to_check[1].strip()),
                               int(request.form['step'])):

                    app.logger.info("Getting" + str(i))

                    respons = wrapper(request_form, bruttolohn=i)
                    respons = respons.decode("ISO-8859-1")
                    results.append(parse_res.parse_res(respons))

                # Logic
                perc_netto = calculate.perc_netto(results)

                plotted_perc_netto = plots.plots(perc_netto)
                img1 = io.BytesIO()
                plotted_perc_netto.savefig(img1, format='png')
                img1.seek(0)
                plot_url_perc_netto = base64.b64encode(img1.getvalue()).decode()

                return render_template("main.html",
                                       result={},
                                       img1='data:image/png;base64,{}'.format(plot_url_perc_netto))
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
