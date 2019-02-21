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

        # Other aircraft attributes.
        self.is_airborne = False

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

    def take_off(self):
        """Take off aircraft."""
        if not self.is_airborne:
            self.fly('take_off.json')
            self.fly('flight_test.json')
            self.is_airborne = True

    def land(self):
        """Land aircraft."""
        if self.is_airborne:
            self.fly('flight_test.json')
            self.fly('land.json')
            self.is_airborne = False

    @property
    def battery(self):
        """Get battery percent."""
        sent = self.sock.sendto('battery?'.encode(ENCODING),
                                            self.tello_address)
        data, server = self.sock.recvfrom(self.buffer_size)
        data = data.decode(encoding=ENCODING)
        return data.rstrip()


if __name__ == "__main__":
    aircraft = Aircraft()
    # aircraft.fly('take_off.json')
    # aircraft.fly('../samples/flight_test2.json')
    # aircraft.fly('../samples/flight_test3.json')
    # aircraft.fly('../samples/square2.json')
    # aircraft.fly('../samples/triangle.json')
    aircraft.fly('../samples/flip.json')
    # aircraft.fly('land.json')
    aircraft.sock.close()
