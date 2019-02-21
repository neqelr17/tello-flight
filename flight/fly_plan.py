"""Tello Python3 Fly by JSON Flight Plan.

https://github.com/neqelr17/tello-flight
1/11/2019
Brett R. Ward
"""

import json
import socket
from time import sleep


from aircraft import Aircraft


ENCODING = 'utf-8'


class Flight():
    """Main flight plan driver application."""

    def __init__(self):
        """Start up aircraft."""
        self.aircraft = Aircraft()

    def run(self):
        """Start application."""
        print(f'Battery: {self.aircraft.battery}%')
        self.aircraft.take_off()
        self.aircraft.fly('../samples/square.json')
        # self.aircraft.land()
        print(f'Battery: {self.aircraft.battery}%')


if __name__ == "__main__":
    flight = Flight()
    flight.run()
