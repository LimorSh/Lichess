# third-party libraries
import argparse
import os
import sys

# inner classes
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from services.Lichess import Lichess    # noqa


def run_program(param1=None, param2=None):
    obj = Lichess(param1, param2)
    obj.run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--username", help="your Lichess username", required=True)
    parser.add_argument("-p", "--password", help="your Lichess password", required=True)
    args = parser.parse_args()

    username = args.username
    password = args.password

    run_program(username, password)

