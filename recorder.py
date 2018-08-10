#!/usr/bin/env python3
import time 
import os
from datetime import datetime
import json

import picamera

import lockpid

def get_logger(config):
    import logging
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    handler1 = logging.FileHandler(os.path.join(config["log_dir"], "recorder.log"))
    handler1.setFormatter(logging.Formatter("%(asctime)s %(levelname)8s %(message)s"))
    logger.addHandler(handler1)
    handler2 = logging.StreamHandler()
    handler2.setFormatter(logging.Formatter("%(asctime)s %(levelname)8s %(message)s"))
    logger.addHandler(handler2)
    return logger

def record(camera):
    name = '{base_dir}/{timestamp:%Y-%m-%d/%H-%M-%S}.jpg'.format(
        base_dir=config['base_dir'],
        timestamp=datetime.now())
    parent = os.path.dirname(name)
    if not os.path.exists(parent):
        logger.info('mkdir %s' % parent)
        os.makedirs(parent)
    camera.capture(name, format="jpeg")
    logger.info('Recorded %s' % name)

def capture_update(camera):
    import tempfile
    fh, tname = tempfile.mkstemp(suffix="capture", dir=os.path.dirname(config["capture"]), text=False)
    try:
        camera.annotate_text ='{timestamp:%Y-%m-%d/%H-%M-%S}'.format(
            timestamp=datetime.now())
        camera.annotate_text_size = 30
        camera.capture(tname, format="jpeg")
    finally:
        os.close(fh)
        camera.annotate_text = None
    os.rename(tname, config["capture"])
    logger.info('Captured %s' % config["capture"])

config = json.load(open("config.json"))
logger = get_logger(config)
for pid in lockpid.lock_pid(os.path.join(config["lock_dir"], "recorder.pid")):
    with picamera.PiCamera() as camera:
        logger.info("Start PID=%d" % pid)
        capture_update(camera)
        while True:
            try:
                record(camera)
                lasttime = time.time()
                while lasttime + config["sleep_sec"] > time.time():
                    if os.path.exists(config["need_capture_file"]):
                        if time.time() - os.path.getmtime(config["need_capture_file"]) < 10:
                            capture_update(camera)
                    time.sleep(1)
            except Exception as err:
                logger.exception("exception %s", err)
