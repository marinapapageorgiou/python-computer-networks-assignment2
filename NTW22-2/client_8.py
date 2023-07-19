import socket
from typing import Tuple

from settings import HOST, BUFF_SIZE, ENCODING, get_port_for_challenge


def get_ip_and_mask(s: socket) -> Tuple[str, int]:
    data = s.recv(BUFF_SIZE)
    ip_mask = data.decode(ENCODING).strip()
    # Server sends the IP address in dotted notation and mask as an integer, with a space in between
    print(ip_mask)
    ip, mask = ip_mask.split(" ")
    mask = int(mask)
    return ip, mask


def calculate_network(ip: str, mask: int) -> str:
    """
    Given an IP address and a mask value, return the network address
    :param ip: IP address in dotted notation
    :param mask: mask as an integer value up to 32
    :return: network address in dotted notation
    """
    # This variable will have the real value of the IP address in base 10
    real_ip = 0
    # Split the dotted notation through dots
    for i, part in enumerate(ip.split(".")):
        # Get the octet value in base 10
        part = int(part)
        # Depending on the byte, the "right part" has to be filled with this number of zero's
        fill_zeros_n = 8 * (3 - i)
        # Shift the octet value to the needed number of zero's, and add it to the real_ip
        real_ip += part << fill_zeros_n

    # For the mask, it will be made up of the specified number of 1's, and filled with 0's up to 32 to
    # the right. So, 2^mask - 1 will return an integer with that binary representation
    mask_ones = (2 ** mask) - 1
    # And then only those number of zeroes are needed
    mask_zeros_n = 32 - mask
    # So shift those positions
    real_mask = mask_ones << mask_zeros_n

    # The integer value of the net is applying the bitwise AND operation with the IP address
    # and the mask integers
    real_net = real_ip & real_mask

    # Create the octets array
    octets = []
    # Helper is just 1111 1111 (one byte with all 1's)
    helper = (2 ** 8) - 1
    # For each octet
    for exp in [3, 2, 1, 0]:
        # Shift the helper (the byte) as many positions as needed to match the respective byte
        byte = helper << (8 * exp)
        # "Remove" all other bytes by applying the bitwise AND operation (this applies for the left part)
        real_byte = real_net & byte
        # And shift the value to the left to get the real octet value (the single byte), and convert it to string
        right_bytes_displacement = 8 * exp
        octets.append(str(real_byte >> right_bytes_displacement))

    # Join all octets with a dot in the middle
    network = ".".join(octets)
    # Return the network address as a string
    return network


def send_network(s: socket, network: str):
    # Send the network address value
    s.send(network.encode(ENCODING))
    print(network)


def get_flag(s: socket) -> None:
    data = s.recv(BUFF_SIZE)
    flag = data.decode(ENCODING).strip()
    print(flag)


def challenge8() -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, get_port_for_challenge(8)))
        # Get IP address and mask values
        ip, mask = get_ip_and_mask(s)
        # Get the network value
        network = calculate_network(ip, mask)
        # Send the network to the challenge server
        send_network(s, network)
        # Retrieve the flag
        get_flag(s)


if __name__ == '__main__':
    challenge8()
