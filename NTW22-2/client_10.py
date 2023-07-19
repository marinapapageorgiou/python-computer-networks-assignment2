import socket
from typing import List

from settings import HOST, BUFF_SIZE, ENCODING, get_port_for_challenge


def get_two_bytes(s: socket) -> List[int]:
    data = s.recv(BUFF_SIZE)
    two_bytes = data.decode(ENCODING).strip()
    print(two_bytes)

    bs = []
    # Server will send bytes separated by a space
    for byte in two_bytes.split(" "):
        # As server sends them in binary format, parse them as a base 2 integer
        bs.append(int(byte, 2))
    return bs


def calculate_checksum(bs: List[int]) -> str:
    """
    Given a list of integers, calculate its byte checksum (8 bits).
    :param bs: list of numbers
    :return: checksum as a string of 8 bits
    """
    # Define the byte value
    byte = 2 ** 8

    # Sum all values
    add = sum(bs)
    # Apply module byte, and append the carry-out
    total = (add % byte) + (add // byte)

    # The checksum is the value that, if added to the total, returns 1111 1111
    # So, in this case, substract 1 bit to the byte, to get those 8 one's, and substract the total value
    int_checksum = (byte - 1) - total
    # Generate the bit representation of this value, and fill it with zeroes to the left up to 8 digits
    checksum = "{0:b}".format(int_checksum).zfill(8)
    return checksum


def send_checksum(s: socket, checksum: str):
    s.send(checksum.encode(ENCODING))
    # Send the checksum to the server
    print(checksum)


def get_flag(s: socket) -> None:
    data = s.recv(BUFF_SIZE)
    flag = data.decode(ENCODING).strip()
    print(flag)


def challenge10() -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, get_port_for_challenge(10)))
        # Receive the two bytes from the server
        bs = get_two_bytes(s)
        # Calculate their checksum
        checksum = calculate_checksum(bs)
        # Send the checksum
        send_checksum(s, checksum)
        # Retrive the flag from the server
        get_flag(s)


if __name__ == '__main__':
    challenge10()
