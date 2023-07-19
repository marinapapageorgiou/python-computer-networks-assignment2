import argparse
import logging
import socket
import subprocess
from typing import Optional

from settings import ARG_ALL_CHALLENGES, FLAG_LENGTH, HOST, SCOREBOT_PORT, BUFF_SIZE, ENCODING, get_client_file


def submit(username: str, challenge: int, flag: str):
    """
    Submits the specified flag for the specified user and challenge.
    :param username: user to which the flag will be registered
    :param challenge: challenge that originated the flag
    :param flag: 64-long character flag
    """
    # Open scorebot socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, SCOREBOT_PORT))
        # Send the username, challenge and flag
        s.send("{} {} {}".format(username, str(challenge), flag).encode(ENCODING))
        # Get the response message
        data = s.recv(BUFF_SIZE).decode(ENCODING)

    # Parse the response message
    message = data.strip()
    # If is not correct, print an error
    if message != "flag saved. Well done!":
        logging.error("Flag for Challenge {} is not correct".format(str(challenge)))
    else:
        # If fine, log an info file
        logging.error("Flag for Challenge {} submitted!".format(str(challenge)))


def get_flag(challenge: int) -> Optional[str]:
    """
    Given the challenge, run and get the flag for the respective challenge.
    :param challenge: number of the challenge to run
    :return: flag if no errors happened
    """
    try:
        # Try to run python3 (as some computers have python as Python2 and python3 as Python3)
        result = subprocess.run(["python3", get_client_file(challenge)], capture_output=True, text=True)
        # If it executes but the response code is not 0 (like in Windows because of Windows Store), then
        # try normal python
        if result.returncode != 0:
            raise Exception()
    except Exception:
        # We can assume that either python3 or python will be installed, as this script has been executed from
        # a python callable command, so no errors at this point shall occur
        result = subprocess.run(["python", get_client_file(challenge)], capture_output=True, text=True)

    if result.returncode != 0:
        # If the return code is not 0, then something bad happened in that challenge and flag could not be obtained
        logging.error("Could not get flag for Challenge {}".format(str(challenge)))
        return

    # Parse the output data
    data = result.stdout.strip()
    out_lines = data.split("\n")
    # Flag will be the last line
    flag = out_lines[-1]
    if len(flag) != FLAG_LENGTH:
        # If the flag does not have the required length, then something bad happened
        logging.error("Flag for Challenge {} does not match the required length".format(str(challenge)))
        return

    # Return the flag
    return flag


if __name__ == '__main__':
    # Define logging format
    logging.basicConfig(format='%(asctime)s | %(message)s')
    # And output all logging messages
    logging.getLogger().setLevel(logging.DEBUG)
    # Initialize the argument parser
    parser = argparse.ArgumentParser(description="Scorebot Submitter")
    # Specifying the username is mandatory
    parser.add_argument("-u", "-U", "--username",
                        help="username of the user to which the flag(s) will be registered",
                        type=str,
                        required=True)
    # Optionally allow specifying a single challenge
    total_challenges = range(1, 10 + 1)
    parser.add_argument("-c", "--challenge",
                        help="challenge of which the flag will be submitted (if none, it will submit all of them)",
                        choices=total_challenges, metavar="1-10",
                        type=int,
                        nargs='?',
                        const=ARG_ALL_CHALLENGES, default=ARG_ALL_CHALLENGES)
    # Parse the arguments
    args = parser.parse_args()

    challenges = []
    # If challenge argument is 0 (default), it will run all challenges
    if args.challenge == ARG_ALL_CHALLENGES:
        challenges = list(total_challenges)
    else:
        # If not, only that specific challenge
        challenges = [args.challenge]

    # For each challenge to be run
    for challenge in challenges:
        # Get its flag
        flag = get_flag(challenge)
        if flag is not None:
            # And if flag is present, submit it
            submit(args.username, challenge, flag)
