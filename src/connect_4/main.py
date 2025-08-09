import argparse
from enum import Enum
from typing import assert_never

from connect_4 import local


class Modes(str, Enum):
    LOCAL = "local"
    ONLINE = "online"


def main():
    parser = argparse.ArgumentParser("connect-4")

    parser.add_argument("mode", choices=[m.value for m in Modes])

    args = parser.parse_args()

    if args.mode == Modes.LOCAL:
        print("Local mode selected!")
        local.main()
        parser.exit()
    elif args.mode == Modes.ONLINE:
        print("Online mode selected!")
        print("Still not implemented")
        parser.exit()
    else:
        assert_never(args.mode)


if __name__ == "__main__":
    main()
