import socket

from settings import HOST, BUFF_SIZE, ENCODING, get_port_for_challenge


def get_port(s: socket) -> int:
    data = s.recv(BUFF_SIZE)
    random_port = data.decode(ENCODING).strip()
    # random port will have the format "random port: X"
    print(random_port)
    # Split in the space, and get the last part
    port = random_port.split(" ")[-1]
    # Parse it as an integer
    return int(port)


def get_flag(s: socket) -> None:
    data = s.recv(BUFF_SIZE)
    flag = data.decode(ENCODING).strip()
    print(flag)


def challenge3() -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, get_port_for_challenge(3)))
        # Get the port to receive the flag
        port = get_port(s)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Connect to the specified port
        s.connect((HOST, port))
        # Retrieve the flag
        get_flag(s)


if __name__ == '__main__':
    challenge3()
