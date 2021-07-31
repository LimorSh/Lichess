# third-party libraries
import argparse
import sys

# inner classes
import consts
sys.path.append(consts.PROJECT_DIR_PATH)
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

