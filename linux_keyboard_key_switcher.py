from flask import Flask
import subprocess
import requests
import atexit

PORT = 18081
PROXY_URL = "http://localhost:18080"

app = Flask(__name__)


def subscribeToKeyboardEvents():
    requests.post(PROXY_URL + "/subscribe?url=http://localhost:%s/osKeymapSwitcher" % PORT)


def unsubscribeToKeyboardEvents():
    requests.post(PROXY_URL + "/unsubscribe?url=http://localhost:%s/osKeymapSwitcher" % PORT)


class KeyboardConf:
    def __init__(self, commands):
        # first command is for clearing other active xkbmap options
        self.commands = ["setxkbmap -option"]
        self.commands.extend(commands)


conf = {
    "3": KeyboardConf(["setxkbmap -option ctrl:swap_lalt_lctl"]),
    "7": KeyboardConf([])
}


@app.route('/osKeymapSwitcher/<deviceId>')
def changeDevice(deviceId):
    if deviceId not in conf.keys():
        return "Configuration for device %(deviceId)s not found" % vars()

    switchKeyboardApplyConf(conf[deviceId])
    return "Swithced to keyboard '%s'" % deviceId


def switchKeyboardApplyConf(conf):
    for cmd in conf.commands:
        subprocess.check_output(cmd, shell=True)


if __name__ == "__main__":
    atexit.register(unsubscribeToKeyboardEvents)

    subscribeToKeyboardEvents()
    app.run(port=PORT)
