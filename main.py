import requests
from evdev import *
from utils.server import *
from utils import keyboard, server
from utils.state import S
import pyttsx3

engine = pyttsx3.init()

# Own state machine
CODE_STATE = S.IDLE
VM_KEYBOARD = ['AT Translated Set 2 keyboard']
LAST_ACCEPTED_VAL = None
BINDINGS = {
    ecodes.KEY_A: 11,
    ecodes.KEY_S: 12,
    ecodes.KEY_D: 14,
    ecodes.KEY_F: 16,
    ecodes.KEY_G: 28,
    ecodes.KEY_H: 19,
    ecodes.KEY_J: 20,
    ecodes.KEY_K: 21,
    ecodes.KEY_L: 21,
}

server = Server()
code = server.login()
if code == 200:
    print("Login success:", code)
else:
    exit("couldnt login. Quitting")
engine.say(f"Login success")
engine.runAndWait()

engine.say(f'Awaiting...')
engine.runAndWait()
kb = keyboard.find_keyboard(filter=VM_KEYBOARD)
for event in kb.read_loop():
    if event.type == ecodes.EV_KEY and event.value == 0:
        if not CODE_STATE == S.BUSY and not CODE_STATE == S.BUSY_USER:
            if event.code in BINDINGS.keys():
                LAST_ACCEPTED_VAL = BINDINGS[event.code]
                print('Getting user')
                json = server.user(user_id=LAST_ACCEPTED_VAL)
                if json is None:
                    print('Received failure, cancelling turf.')
                    LAST_ACCEPTED_KEY = None
                    CODE_STATE = S.IDLE
                    continue
                else:
                    CODE_STATE = S.BUSY_USER
                    engine.say(f"User {json['first_name']} {json['last_name']}. Confirm.")
                    engine.runAndWait()
                CODE_STATE = S.IDLE_CONFIRM
            elif event.code == ecodes.KEY_ENTER:
                CODE_STATE = S.BUSY
                if LAST_ACCEPTED_VAL:
                    # success = server.turf(user_id=LAST_ACCEPTED_VAL)
                    success = True
                    if success:
                        print("successfully turfed on {}")
                        engine.say(f"Plus one confirmed")
                        engine.runAndWait()
                    else:
                        print("failed to turf on {}")
                    print('Awaiting user keybinding...')
                    LAST_ACCEPTED_KEY = None
                    CODE_STATE = S.IDLE
                else:
                    CODE_STATE = S.IDLE
            else:
                LAST_ACCEPTED_KEY = None
                CODE_STATE = S.IDLE
        else:
            print('Sorry, busy turfing something else. Timeout in ... sec')
