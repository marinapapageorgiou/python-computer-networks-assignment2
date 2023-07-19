import socket
from typing import Tuple

from settings import HOST, BUFF_SIZE, ENCODING, get_port_for_challenge


def get_data(s: socket) -> Tuple[int, float, int]:
    data = s.recv(BUFF_SIZE)
    raw_data = data.decode(ENCODING).strip()
    # raw_data will have a format like "Xms X Xms"
    print(raw_data)
    # Remove the ms string, and split by spaces
    rtt, alpha, lrtt = raw_data.replace("ms", "").split(" ")
    # Convert the values to the respective types
    rtt = int(rtt)
    alpha = float(alpha)
    lrtt = int(lrtt)
    return rtt, alpha, lrtt


def calculate_ertt(rtt: int, alpha: float, lrtt: int) -> int:
    """
    Given the current rtt, an alpha value and a last rtt, return the new estimated rtt
    :param rtt: integer for the current ertt
    :param alpha: float alpha value
    :param lrtt: integer with the last rtt value
    :return: new estimated rtt
    """
    # "Old" weighted rtt
    old_rtt = rtt * (1 - alpha)
    # New weighted rtt
    new_rtt = lrtt * alpha
    # Round to the nearest integer
    return round(old_rtt + new_rtt)


def send_ertt(s: socket, ertt: int) -> None:
    ertt = str(ertt)
    s.send(ertt.encode(ENCODING))
    print(ertt)


def get_flag(s: socket) -> None:
    data = s.recv(BUFF_SIZE)
    flag = data.decode(ENCODING).strip()
    print(flag)


def challenge4() -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, get_port_for_challenge(4)))
        # Get the parameters to calculate the estimated rtt
        rtt, alpha, lrtt = get_data(s)
        # Calculate the estimated rtt
        ertt = calculate_ertt(rtt, alpha, lrtt)
        # Send the rtt to the challenge server
        send_ertt(s, ertt)
        # Retrieve the flag
        get_flag(s)


if __name__ == '__main__':
    challenge4()
