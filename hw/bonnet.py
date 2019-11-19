import logging

import pwnagotchi.ui.fonts as fonts
from pwnagotchi.ui.hw.base import DisplayImpl



class Bonnet(DisplayImpl):
    def __init__(self, config):
        super(Bonnet, self).__init__(config, 'bonnet')
        self._display = None

    def layout(self):
        fonts.setup(8, 8, 8, 8)
        self._layout['width'] = 128
        self._layout['height'] = 64
        self._layout['face'] = (0, 32)
        self._layout['name'] = (0, 10)
        self._layout['channel'] = (0, 0)
        self._layout['aps'] = (25, 0)
        self._layout['uptime'] = (65, 0)
        self._layout['line1'] = [0, 9, 128, 9]
        self._layout['line2'] = [0, 53, 128, 53]
        self._layout['friend_face'] = (0, 41)
        self._layout['friend_name'] = (40, 43)
        self._layout['shakes'] = (0, 53)
        self._layout['mode'] = (103, 10)
        self._layout['status'] = {
            'pos': (30, 18),
            'font': fonts.Small,
            'max': 18
        }
        return self._layout

    def initialize(self):
        logging.info("initializing bonnet display")
        from pwnagotchi.ui.hw.libs.adafruit.bonnet.oled import Display
        self._display = Display()
       
        self._display.init()

    def render(self, canvas):
        self._display.display(canvas)

    def clear(self):
        self._display.clear()