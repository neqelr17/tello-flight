"""Tello Python3 Fly by JSON Flight Plan.

https://github.com/neqelr17/tello-flight
1/11/2019
Brett R. Ward
"""

import json
import socket
from time import sleep


ENCODING = 'utf-8'


class Aircraft():
    """Tello aircraft."""

    def __init__(self):
        """Init Tello."""
        self.buffer_size = 1518
        self.host = '192.168.10.2'
        self.send_port = 8889
        self.receive_port = 8890
        self.localaddr = (self.host, self.receive_port)
        self.tello_address = ('192.168.10.1', 8889)

        # Create a UDP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(self.localaddr)
        self.plan = []

    def import_flight_plan(self, plan):
        """Import JSON flight plan."""
        try:
            fh_plan = open(plan, 'r', encoding=ENCODING)
            self.plan = json.load(fh_plan)
            fh_plan.close()
        except Exception:
            print('ERROR: Could not load flight plan.')

    def fly(self, plan):
        """Fly aircraft based on flight plan."""
        self.import_flight_plan(plan)
        # print(self.plan)

        try:
            for cmd in self.plan:
                print(f"cmd: {cmd['command']}")
                if cmd['command'] == 'wait':
                    sleep(cmd['seconds'])
                    print(f"result: {cmd['seconds']}")
                else:
                    sent = self.sock.sendto(cmd['command'].encode(ENCODING),
                                            self.tello_address)

                    data, server = self.sock.recvfrom(self.buffer_size)
                    data = data.decode(encoding=ENCODING)
                    print(f"result: {data}")
                    if data != cmd['result']:
                        break

        except Exception:
            self.sock.close()


if __name__ == "__main__":
    aircraft = Aircraft()
    aircraft.fly('take_off.json')
    aircraft.fly('flight_test2.json')
    aircraft.fly('flight_test3.json')
    # aircraft.fly('square2.json')
    # aircraft.fly('triangle.json')
    aircraft.fly('land.json')
    aircraft.sock.close()
