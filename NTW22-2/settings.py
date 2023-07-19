# Server for both flag generator and scorebot
HOST = "162.243.73.199"
# Initial port, it will go from 9990 (Challenge 1) to 9999 (Challenge 10)
INITIAL_PORT = 9990
# Port where scorebot is running
SCOREBOT_PORT = 11111

# Buffer size to receive data from the sockets
BUFF_SIZE = 1024
# Encoding to transform bytes to strings, and viceversa
ENCODING = 'utf-8'
# Length of all flags
FLAG_LENGTH = 64

# Default argument to submit all challenges
ARG_ALL_CHALLENGES = 0


def get_port_for_challenge(challenge: int) -> int:
    """
    Given the challenge number, return the port that such CTF is running
    :param challenge: number of the challenge from 1 to 10
    :return: port number
    """
    if challenge < 1 or challenge > 10:
        # Just make sure that port exists
        challenge = 1
    return INITIAL_PORT + (challenge - 1)


def get_client_file(challenge: int) -> str:
    """
    Returns the file that should have the code for that challenge.
    :param challenge: number of the challenge
    :return: string representing the file which contains that code
    """
    return "client_{}.py".format(str(challenge))
