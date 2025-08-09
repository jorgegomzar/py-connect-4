import socket

from connect_4.online.utils import HOST, PORT, GameState, recv, send
from connect_4.utils import CELL_DISPLAY_VALUES, CONSOLE, print_board


def main():
    host = input(f"Host (default {HOST}): ").strip() or HOST
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, PORT))

        while True:
            if (game_state := recv(s)) is None:
                break

            if not isinstance(game_state, GameState):
                raise ValueError("data is not a GameState instance")

            print_board(game_state.board, game_state.connect_4_cells)

            if game_state.winner is not None:
                CONSOLE.print(
                    f"Winner is Player {CELL_DISPLAY_VALUES[game_state.winner]}",
                    style="green",
                )
                break

            if not game_state.is_player_turn:
                continue

            col = None
            while col is None:
                try:
                    col = int(
                        input(
                            f"Your turn (Player {CELL_DISPLAY_VALUES[game_state.turn]}). Column: "
                        )
                    )
                except TypeError as e:
                    CONSOLE.print(f"ERROR {e}", style="red")
            send(s, col)


if __name__ == "__main__":
    main()
