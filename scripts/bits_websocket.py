#!/usr/bin/env python

import websocket
import json
import time
import threading
import argparse
from subprocess import Popen,PIPE

DEFAULT_LOGIN  = "/usr/share/sounds/login.wav"
DEFAULT_LOGOUT = "/usr/share/sounds/logout.wav"

class BitsXP(object):
    def __init__(self, args):
        self.args = args
	self.prev_status = ""

    def on_message(self, ws, message):
        try:
            cur_status = json.loads(message)["status"]["value"]
            if cur_status != self.prev_status:
                self.prev_status = cur_status

                out = devnull if self.args.quiet else PIPE

                if cur_status == "open":
                    print "Now it's opened!"
                    Popen(["mplayer", self.args.login], stdout=out).communicate()
                elif cur_status == "closed":
                    print "Now it's closed!"
                    Popen(["mplayer", self.args.logout], stdout=out).communicate()
                else:
                    print "WTF?" # Se entra qui, non va bene
        except:
            pass

    def on_error(self, ws, error):
        print "Error: " + error.message
        print "Reconnecting..."
        start_websocket()

    def on_close(self, ws):
        print "Connection closed"

    def on_open(self, ws):
        def ping(*args):
            while 1:
                #print "Keep-alive"
                ws.send("Hi")
                time.sleep(15)
        pingthread = threading.Thread(target=ping)
        pingthread.daemon(False)
        pingthread.start()

    def run(self):
        ws = websocket.WebSocketApp(
            "wss://bits.poul.org/ws",
            on_message = self.on_message,
            on_error = self.on_error,
            on_close = self.on_close,
            on_open = self.on_open
        )
        try:
            ws.run_forever()
        except KeyboardInterrupt:
            pass

if __name__== "__main__":
    parser = argparse.ArgumentParser(
	description='Play a sound when BITS changes its status.',
	prog='bitsxp',
	formatter_class = lambda prog: argparse.HelpFormatter(prog,max_help_position=30)
    )
    parser.add_argument('--version', action="version", version='%(prog)s 0.1')
    parser.add_argument('-i', '--login', default=DEFAULT_LOGIN, action='store', help='Specify the login sound.')
    parser.add_argument('-o', '--logout', default=DEFAULT_LOGOUT, action='store', help='Specify the logout sound.')
    parser.add_argument('-q', '--quiet', action='store_true', help='Suppress any output.')
    #daemon = parser.add_mutually_exclusive_group()
    #daemon.add_argument('-d', '--daemon', action='store_true', help='Run the script as a daemon.')
    #daemon.add_argument('-k', '--kill', action='store_true', help='Kill the running daemon.')
    args = parser.parse_args()
    
    BitsXP(args).run()
    