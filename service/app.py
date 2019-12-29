import logging
import os

from pathlib import Path
from collections import defaultdict

import random
import string
import subprocess

from flask import Flask, render_template, request, redirect, flash
from flask_table.html import element
from flask import send_file
from flask_table import Col, Table, LinkCol

from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

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
    ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
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
        return render_template("main.html", result=request.data)

    app.logger.info("Starting app...")
    # DEBUG
    if linux:
        app.run()
    # PRD
    if windows:
        HTTP_SERVER = WSGIServer(('0.0.0.0', int(PORT)), app)
        HTTP_SERVER.serve_forever()    