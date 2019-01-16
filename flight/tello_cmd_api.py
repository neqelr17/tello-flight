"""Tello Python3 Control Demo.

http://www.ryzerobotics.com/
1/1/2018

Brett R. Ward
Updated PEP8 and minor changes.
"""

import threading
import socket


host = '192.168.10.2'
send_port = 8889
receive_port = 8890
locaddr = (host, receive_port)


# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

tello_address = ('192.168.10.1', 8889)
sock.bind(locaddr)


def recv():
    """Receive Return Messages."""
    while True:
        try:
            data, server = sock.recvfrom(1518)
            print(data.decode(encoding="utf-8"))
        except Exception:
            print('\nExit . . .\n')
            break


if __name__ == "__main__":
    print('Tello: command takeoff land flip forward back left right')
    print('up down cw ccw speed speed?')
    print('end -- quit demo.')

    # recvThread create
    recvThread = threading.Thread(target=recv)
    recvThread.start()

    while True:
        try:
            msg = input("")

            if not msg:
                break

            if 'end' in msg:
                print('...')
                sock.close()
                break

            # Send data
            msg = msg.encode(encoding="utf-8")
            sent = sock.sendto(msg, tello_address)
        except KeyboardInterrupt:
            print('\n . . .\n')
            sock.close()
            break
