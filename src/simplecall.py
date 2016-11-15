#!/usr/bin/env python
# -*- coding: utf-8 -*-

### POUZITI:      python simplecall.py sip:00420xxxxxxxxx@odorik.cz


import sys
import pjsua as pj
import threading
import wave
from time import sleep

# https://trac.pjsip.org/repos/wiki/Python_SIP/Hello_World

hangup = False
dtmf_number = -1
call_total_time = -1
call_connected_time = -1

# Logging callback
def log_cb(level, str, len):
    print str,


class MyAccountCallback(pj.AccountCallback):
    sem = None

    def __init__(self, account):
        pj.AccountCallback.__init__(self, account)

    def wait(self):
        self.sem = threading.Semaphore(0)
        self.sem.acquire()


    def on_reg_state(self):
        if self.sem:
            self.sem.release()

    # Notification on incoming call
    def on_incoming_call(self, call):
        call.answer(486, "Busy")
        return

# Callback to receive events from Call
class MyCallCallback(pj.CallCallback):
    def __init__(self, call=None):
        pj.CallCallback.__init__(self, call)

    def play_wav_file(self, file_name):
        wfile = wave.open(file_name)
        time = (1.0 * wfile.getnframes()) / wfile.getframerate()
        print str(time) + "ms"
        wfile.close()
        call_slot = call.info().conf_slot
        wav_player_id = pj.Lib.instance().create_player(file_name, loop=False)
        wav_slot = pj.Lib.instance().player_get_slot(wav_player_id)
        pj.Lib.instance().conf_connect(wav_slot, call_slot)
        sleep(time)
        pj.Lib.instance().player_destroy(wav_player_id)

    # ZBYTECNE, MOZNO SMAZAT:
    # Notification when call's media state has changed.
    def on_media_state(self):
        global lib
        if self.call.info().media_state == pj.MediaState.ACTIVE:
            print "Hello world, I can talk!"

    # Notification when call state has changed
    def on_state(self):
        print "Call is ", self.call.info().state_text,
        print "last code =", self.call.info().last_code,
        print "(" + self.call.info().last_reason + ")"

        if self.call.info().state == pj.CallState.CONFIRMED:
            # Call is Answred

            print "Call Answered"
            call_slot = self.call.info().conf_slot

            sleep(3)
            self.play_wav_file("upozorneni-zprava.wav") # zprava

            sleep(2)
            self.play_wav_file("navigace.wav")

        elif self.call.info().state == pj.CallState.DISCONNECTED:
            global hangup
            hangup = True

    # Notification on incoming DTMF digits. http://www.pjsip.org/python/pjsua.htm
    def on_dtmf_digit(self, digits):
        global dtmf_number
        dtmf_number = digits
        print "_______________DTMF_DIGITS_ " + str(digits)

        call_slot = self.call.info().conf_slot

        if dtmf_number == "1":
            self.call.hangup()
        elif dtmf_number == "2":
            self.play_wav_file("navigace.wav")
        else:
            print "TIME=", self.call.info().total_time
            self.play_wav_file("neznama_volba.wav")

        dtmf_number = None

# Check command line argument
if len(sys.argv) != 2:
    print "Usage: simplecall.py <dst-URI>"
    sys.exit(1)

try:
    # Create library instance
    lib = pj.Lib()

    # Init library with default config
    lib.init(log_cfg=pj.LogConfig(level=3, callback=log_cb))

    # Create UDP transport which listens to any available port
    transport = lib.create_transport(pj.TransportType.UDP)

    # Start the library
    lib.start(with_thread=True)

    # Create local/user-less account
    acc = lib.create_account(pj.AccountConfig(username='USER', password='PASS', domain='sip.odorik.cz'))

    acc_cb = MyAccountCallback(acc)
    acc.set_callback(acc_cb)
    acc_cb.wait()

    print "\n"
    print "Registration complete, status=", acc.info().reg_status, \
        "(" + acc.info().reg_reason + ")"

    # Make call
    call = acc.make_call(sys.argv[1], MyCallCallback())

    while True:
        sleep(0.5)
        call_total_time = call.info().total_time
        call_connected_time = call.info().call_time
        print "Call total time ", call_total_time
        print "Call connected time ", call_connected_time
        if call_total_time > 180 or call_connected_time > 30:
            print "___________DLOUHY HOVOR - ZAVESUJI____________"
            call.hangup()
            hangup = True
            sleep(1)
        if hangup:
            print "____________________HANGUP____________________"
            # We're done, shutdown the library
            acc.delete()
            acc = None
            lib.destroy()
            lib = None
            sys.exit(0)

except pj.Error, e:
    print "Exception: " + str(e)
    if acc is not None:
        acc.delete()
        acc = None
    if lib is not None:
        lib.destroy()
        lib = None
    sys.exit(1)

