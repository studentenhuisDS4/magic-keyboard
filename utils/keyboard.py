import evdev
from pprint import pprint


def print_devices():
    devices = get_devices()
    for device in devices:
        print(device.name)


def find_keyboard(filter=['AT Translated Set 2 keyboard']):
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    for device in devices:
        if device.name in filter:
            return device
    return None


def get_devices():
    return [evdev.InputDevice(path) for path in evdev.list_devices()]
