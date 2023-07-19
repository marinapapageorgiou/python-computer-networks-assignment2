import socket
from typing import Tuple, List, Optional

from settings import HOST, BUFF_SIZE, ENCODING, get_port_for_challenge


def get_interfaces_and_destination(s: socket) -> Tuple[List[Tuple[str, int, str]], str, str]:
    data = s.recv(BUFF_SIZE)
    ifaces_dest = data.decode(ENCODING).strip()
    # ifaces_dest will have a format like "IP/MASK I,IP/MASK I,...,otherwise I,DESTINATION"
    print(ifaces_dest)
    # Split the data through the commas
    entries = ifaces_dest.split(",")

    ifaces = []
    # Interfaces are all of them except the last two elements in the response (default and destination)
    for entry in entries[:-2]:
        # Split the entry through the space, to get the network and the mask
        net, iface = entry.split(" ")
        # Split the IP and the mask
        ip, mask = net.split("/")
        mask = int(mask)
        # Add the tuple to the interfaces array
        ifaces.append((ip, mask, iface))

    # The default interface is the previous last element, splitted by space and the last element in the list
    default = entries[-2].split(" ")[-1]
    # The destination address is the very last element in the entries
    destination = entries[-1]

    # Return the list of tuples with the interfaces, the default one and the destination address
    return ifaces, default, destination


def dotted_to_int(addr: str) -> int:
    """
    Given an IP address as a string, return its integer value.
    :param addr: IP address in dotted notation
    :return: IP address in integer (base 1o) value
    """
    ip = 0
    for i, part in enumerate(addr.split(".")):
        # For each byte, shift its value the needed amount of zeroes
        ip += int(part) << (8 * (3 - i))
    return ip


def get_out_iface(ifaces: List[Tuple[str, int, str]], destination: str) -> Optional[str]:
    """
    Given a list of interfaces and an IP address, return the out interface if any matches.
    :param ifaces: list of tuples containing the network, mask and out interface for each interface
    :param destination: destination IP address in dotted notation
    :return: out interface, if any network matches
    """
    # Convert the IP to integer
    ip = dotted_to_int(destination)
    iface_out, max_mask = None, None

    # For each interface,
    for addr, mask, iface in ifaces:
        # Convert the network to its integer value
        network = dotted_to_int(addr)
        # matches = ((network >> antimask) ^ (ip >> antimask)) == 0
        # Convert the mask to its integer value
        bitmask = ((2 ** mask) - 1) << (32 - mask)
        # If the destination IP address shall go through that interface, it is because applying
        # the bitwise AND operation between this address and the mask returns the network it is
        # linked to
        matches = (ip & bitmask) == network
        if matches:
            # Only use this interface if none was found previously, or if the mask is bigger
            # (the longest matching prefix)
            if max_mask is None or mask > max_mask:
                iface_out = iface
                max_mask = mask

    # Return the out interface
    return iface_out


def send_interface(s: socket, iface: str) -> None:
    s.send(iface.encode(ENCODING))
    # Send the interface
    print(iface)


def get_flag(s: socket) -> None:
    data = s.recv(BUFF_SIZE)
    flag = data.decode(ENCODING).strip()
    print(flag)


def challenge9() -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, get_port_for_challenge(9)))
        # Get the interfaces, default interface and destination address
        ifaces, default, destination = get_interfaces_and_destination(s)
        # Get the out interface
        iface = get_out_iface(ifaces, destination)
        # If the interface is null, then use the default one
        if iface is None:
            iface = default
        # Send the interface to the challenge server
        send_interface(s, iface)
        # Retrieve the flag
        get_flag(s)


if __name__ == '__main__':
    challenge9()
