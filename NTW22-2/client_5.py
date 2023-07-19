import socket
from typing import Tuple

from settings import HOST, BUFF_SIZE, ENCODING, get_port_for_challenge


def get_data(s: socket) -> Tuple[float, float, float]:
    data = s.recv(BUFF_SIZE)
    raw_data = data.decode(ENCODING).strip()
    # raw_data will have a format like "L=X Gb R1=X Gbps R2=X Gbps" with different units
    print(raw_data)

    # Split all the values
    l_v, l_u, r1_v, r1_u, r2_v, r2_u = raw_data.split(" ")
    l_v = float(l_v.replace("L=", ""))
    r1_v, r2_v = float(r1_v.replace("R1=", "")), float(r2_v.replace("R2=", ""))

    # Convert all units to bits
    expos = {'K': 10 ** 3, 'M': 10 ** 6, 'G': 10 ** 9}
    for key, value in expos.items():
        if l_u.startswith(key):
            l_v *= value
        if r1_u.startswith(key):
            r1_v *= value
        if r2_u.startswith(key):
            r2_v *= value

    # Return L, R1 and R2
    return l_v, r1_v, r2_v


def calculate_delay(l, r1, r2) -> float:
    """
    Given a packet size and two node links bandwidth, return the transmission delay.
    :param l: packet size in bits
    :param r1: first link bandwidth in bits per second
    :param r2: second link bandwidth in bits per second
    :return: transmission delay in seconds
    """
    n1 = l / r1
    n2 = l / r2
    return n1 + n2


def send_delay(s: socket, delay: float) -> None:
    delay = str(delay)
    s.send(delay.encode(ENCODING))
    print(delay)


def get_flag(s: socket) -> None:
    data = s.recv(BUFF_SIZE)
    flag = data.decode(ENCODING).strip()
    print(flag)


def challenge5() -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, get_port_for_challenge(5)))
        # Get L, R1 and R2
        l, r1, r2 = get_data(s)
        # Get the transmission delay
        delay = calculate_delay(l, r1, r2)
        # Send the transmission delay to the challenge server
        send_delay(s, delay)
        # Retrieve the flag
        get_flag(s)


if __name__ == '__main__':
    challenge5()
