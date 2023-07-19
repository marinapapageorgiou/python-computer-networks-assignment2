import random
import socket

from settings import HOST, BUFF_SIZE, ENCODING, get_port_for_challenge


def send_fin(s: socket, seq: int, ack: int) -> int:
    syn = "FIN,ACK Seq={} Ack={}".format(seq, ack)
    # Send the FIN and ACK message
    s.send(syn.encode(ENCODING))
    print(syn)
    # Increase client sequence number
    return seq + 1


def recv_ack_fin(s: socket, expected_ack: int, expected_seq: int) -> int:
    data = s.recv(BUFF_SIZE).decode(ENCODING).strip()
    # In this case, both ACK and FIN messages from server are received in the same buffer
    data_ack, data_fin = data.split("\n")
    # Split it, and parse only the ACK here
    data_ack = data_ack.strip()
    print(data_ack)
    msg, raw_seq, raw_ack = data_ack.split(" ")
    # Make sure it is an ACK message
    assert msg == "ACK"

    v_seq, r_seq = raw_seq.split("=")
    seq = int(r_seq)
    # Make sure the sequence number matches the expected one
    assert v_seq == "Seq"
    assert seq == expected_seq

    v_ack, r_ack = raw_ack.split("=")
    ack = int(r_ack)
    # Make sure the server is ACKing the correct sequence number
    assert v_ack == "Ack"
    assert ack == expected_ack

    # Parse the FIN message
    return recv_fin(data_fin, expected_ack, expected_seq)


def recv_fin(data: str, expected_ack: int, expected_seq: int) -> int:
    data = data.strip()
    print(data)
    msg, raw_seq, raw_ack = data.split(" ")
    # Make sure a both FIN and ACK message is received
    assert msg == "FIN,ACK"

    v_seq, r_seq = raw_seq.split("=")
    seq = int(r_seq)
    # Check the sequence number
    assert v_seq == "Seq"
    assert seq == expected_seq

    v_ack, r_ack = raw_ack.split("=")
    ack = int(r_ack)
    # And check the ACK number
    assert v_ack == "Ack"
    assert ack == expected_ack

    # Increase server's sequence number counter
    return seq + 1


def send_ack(s: socket, seq: int, srv_ack: int) -> int:
    ack = "ACK Seq={} Ack={}".format(seq, srv_ack)
    # Send the ACK message
    s.send(ack.encode(ENCODING))
    print(ack)
    # Increase client's sequence number
    return seq + 1


def get_flag(s: socket) -> None:
    data = s.recv(BUFF_SIZE)
    flag = data.decode(ENCODING).strip()
    print(flag)


def challenge6() -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, get_port_for_challenge(7)))
        # Initialize client and server sequence numbers to random values
        seq, srv_seq = int(random.uniform(1, 10)), int(random.uniform(1, 10))
        # Send the close connection request with a FIN message
        seq = send_fin(s, seq, srv_seq)
        # Receive server's ACK, and parse their FIN request
        srv_seq = recv_ack_fin(s, seq, srv_seq)
        # Send the ACK
        send_ack(s, seq, srv_seq)
        # Retrieve the flag
        get_flag(s)


if __name__ == '__main__':
    challenge6()
