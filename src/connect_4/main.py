import argparse
from enum import Enum

from connect_4 import local, online


class Networking(str, Enum):
    LOCAL = "local"
    ONLINE = "online"


class OnlineModes(str, Enum):
    HOST = "host"
    JOIN = "join"


def main():
    parser = argparse.ArgumentParser("connect-4")

    subparsers = parser.add_subparsers(help="Networking", dest="networking")
    subparsers.add_parser(Networking.LOCAL.value)
    online_parser = subparsers.add_parser(Networking.ONLINE.value)

    online_parser.add_argument("online_mode", choices=[m.value for m in OnlineModes])

    args = parser.parse_args()

    if args.networking == Networking.LOCAL:
        print("Local mode selected!")
        local.main()
        parser.exit()

    if args.networking == Networking.ONLINE:
        print("Online mode selected!")
        if args.online_mode == OnlineModes.HOST:
            online.server.main()
        elif args.online_mode == OnlineModes.JOIN:
            online.client.main()
        parser.exit()

    parser.print_help()
    parser.exit(-1)


if __name__ == "__main__":
    main()
