import socket

from settings import HOST, BUFF_SIZE, ENCODING, get_port_for_challenge


def send_syn(s: socket, seq: int) -> int:
    syn = "SYN Seq={}".format(seq)
    # Send the SYN string
    s.send(syn.encode(ENCODING))
    print(syn)
    # Increase the sequence number
    return seq + 1


def recv_ack(s: socket, expected_ack: int, expected_seq) -> int:
    data = s.recv(BUFF_SIZE).decode(ENCODING).strip()
    print(data)
    msg, raw_seq, raw_ack = data.split(" ")
    # Confirm that both SYN and ACK is present
    assert msg == "SYN,ACK"

    v_seq, r_seq = raw_seq.split("=")
    seq = int(r_seq)
    # Make sure the expected sequence number matches
    assert v_seq == "Seq"
    assert seq == expected_seq

    v_ack, r_ack = raw_ack.split("=")
    ack = int(r_ack)
    # Make sure the expected ACK matches
    assert v_ack == "Ack"
    assert ack == expected_ack

    # Increase the server sequence number
    return seq + 1


def send_ack(s: socket, seq: int, srv_ack: int) -> int:
    ack = "ACK Seq={} Ack={}".format(seq, srv_ack)
    # Send the ACK with the sequence number
    s.send(ack.encode(ENCODING))
    print(ack)
    # Increase client sequence number
    return seq + 1


def get_flag(s: socket) -> None:
    data = s.recv(BUFF_SIZE)
    flag = data.decode(ENCODING).strip()
    print(flag)


def challenge6() -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, get_port_for_challenge(6)))
        # Init both sequence and server sequence numbers to 0
        seq, srv_seq = 0, 0
        # Request opening a connection with SYN
        seq = send_syn(s, seq)
        # Receive server's ACK and SYN
        srv_seq = recv_ack(s, seq, srv_seq)
        # Send the ACK back
        send_ack(s, seq, srv_seq)
        # Retrieve the flag
        get_flag(s)


if __name__ == '__main__':
    challenge6()
