#!env python

import os
import subprocess
import time

service_check_interval = 10

def webui_proc():
    global service_check_interval
    while True:
        if os.path.exists("service_url.data"):
            os.remove("service_url.data")
        subp = subprocess.Popen(["./webui.sh --share --api --disable-nan-check"],shell=True,encoding="utf-8")
        while True:
            time.sleep(service_check_interval)
            if os.path.exists("service_url.data"):
                with open("./service_url.data", 'r') as rfile:
                    share_url = rfile.read()
                    print("service check: {}".format(share_url))
                    if not check_live(share_url):
                        subp.kill()
                        break



import requests
from datetime import datetime

def check_live(share_url):
    try:
        pb_arg = datetime.now().timestamp
        response_json = requests.get("{}/sdapi/v1/memory?pb={}".format(share_url, pb_arg)).json()
        print(response_json)
        return True
    except:
        print("link broken")
        return False


import threading

webui_thread = threading.Thread(target=webui_proc)
webui_thread.start()
