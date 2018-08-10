#!/usr/bin/env python3

import time
from io import BytesIO
from pathlib import Path
import json
import os
import re

import flask
from flask import Flask, render_template, request, redirect, url_for, send_file, jsonify, send_from_directory
import picamera

app = Flask(__name__)
config = json.load(open("config.json"))

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/list.json')
def list_root():
    return jsonify(os.listdir(path=config["base_dir"]))

@app.route('/list<path>.json')
def list_day(path):
    if not re.match('\d\d\d\d-\d\d-\d\d', path):
        abort(400)
    p = os.path.join(config["base_dir"], path)
    if not os.path.exists(p):
        abort(400)
    return jsonify(os.listdir(path=p))

@app.route('/record/<path:filename>')
def record_image(filename):
    return send_from_directory(config['base_dir'], filename)


@app.route('/now.jpg')
def capture_now():
    app.logger.info("touch %s" % config["need_capture_file"])
    Path(config["need_capture_file"]).touch()
    return send_file(config["capture"], mimetype='image/jpg')

if __name__ == '__main__':
    import lockpid
    import argparse
    import logging
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true', default=False, help='debug')
    args = parser.parse_args()
    for pid in lockpid.lock_pid(os.path.join(config["lock_dir"] ,"server.pid"), lock=not args.debug):
        print("server PID=%d" % pid)
        app.logger.setLevel(logging.INFO)
        handler1 = logging.FileHandler(os.path.join(config["log_dir"], "server.log"))
        handler1.setFormatter(logging.Formatter("%(asctime)s %(levelname)8s %(message)s"))
        app.logger.addHandler(handler1)
        app.run(debug=args.debug, host='::', port=5800) # どこからでもアクセス可能に
        print("ok")
