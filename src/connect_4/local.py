from itertools import cycle

import numpy as np

from connect_4.utils import (
    CELL_DISPLAY_VALUES,
    COLS,
    CONSOLE,
    ROWS,
    Connect4Cells,
    find_next_free_row,
    get_connect_4_cells,
    print_board,
)


def main():
    board = np.zeros((ROWS, COLS))
    connect_4_cells: Connect4Cells = []

    players = cycle((1, 2))
    player = next(players)

    while True:
        connect_4_cells = get_connect_4_cells(board)

        try:
            print_board(board, connect_4_cells)

            if connect_4_cells:
                break

            col = int(input(f"Player {CELL_DISPLAY_VALUES[player]}. Col: "))
            if col < 0 or col >= COLS:
                raise ValueError("Invalid col")

            row = find_next_free_row(board[:, col])
        except Exception as e:
            CONSOLE.print(f"ERROR: {e}", style="uu bold blink red")
            continue

        board[row, col] = player
        player = next(players)

    if not connect_4_cells:
        raise RuntimeError("Game cannot finish until we have a winner")

    CONSOLE.print(
        f"WINNER IS PLAYER {CELL_DISPLAY_VALUES[board[connect_4_cells[0]]]}",
        style="green",
    )


if __name__ == "__main__":
    main()
