import socket

from settings import HOST, BUFF_SIZE, ENCODING, get_port_for_challenge


def get_flag(s: socket) -> None:
    # Receive the buffer data
    data = s.recv(BUFF_SIZE)
    # Decode and remove trailing characters
    flag = data.decode(ENCODING).strip()
    print(flag)


def challenge1() -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Connect to the challenge server
        s.connect((HOST, get_port_for_challenge(1)))
        # Retrieve the flag
        get_flag(s)


if __name__ == '__main__':
    challenge1()
