import socket

from settings import HOST, ENCODING, BUFF_SIZE, get_port_for_challenge


def send_helo(s: socket) -> None:
    helo = 'helo'
    # Encode the helo string, and send it specifying the destination
    s.sendto(helo.encode(ENCODING), (HOST, get_port_for_challenge(2)))
    print(helo)


def get_flag(s: socket) -> None:
    data, server = s.recvfrom(BUFF_SIZE)
    flag = data.decode(ENCODING).strip()
    print(flag)


def challenge2() -> None:
    # Use UDP in this case
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        # Send a helo message
        send_helo(s)
        # Retrieve the flag
        get_flag(s)


if __name__ == '__main__':
    challenge2()
