import numpy as np
from rich.align import Align
from rich.console import Console
from rich.table import Table

# TODO: could ask the user for these values
ROWS = 6
COLS = 7

Connect4Cells = list[tuple[int, int]]

CELL_DISPLAY_VALUES = {
    0: " ",
    1: "🟠",
    2: "🔵",
}

CONSOLE = Console()


def find_next_free_row(column: np.ndarray) -> int:
    if not column.any():
        # column is full of zeros
        return ROWS - 1

    for row, cell in enumerate(column):
        if cell != 0:
            if row == 0:
                raise ValueError("No free row on this column")
            return row - 1

    raise RuntimeError("Should not be possible")


def get_connect_4_cells(board: np.ndarray) -> Connect4Cells:
    rows, cols = board.shape

    # HORIZONTAL
    for r in range(rows):
        for c in range(cols - 3):
            val = board[r, c]
            if val != 0 and (board[r, c : c + 4] == val).all():
                return [(r, c + i) for i in range(4)]

    # VERTICAL
    for r in range(rows - 3):
        for c in range(cols):
            val = board[r, c]
            if val != 0 and (board[r : r + 4, c] == val).all():
                return [(r + i, c) for i in range(4)]

    # DIAGONAL DOWN-RIGHT
    for r in range(rows - 3):
        for c in range(cols - 3):
            val = board[r, c]
            if val != 0 and all(board[r + i, c + i] == val for i in range(4)):
                return [(r + i, c + i) for i in range(4)]

    # DIAGONAL UP-RIGHT
    for r in range(3, rows):
        for c in range(cols - 3):
            val = board[r, c]
            if val != 0 and all(board[r - i, c + i] == val for i in range(4)):
                return [(r - i, c + i) for i in range(4)]

    return []


def print_board(
    board: np.ndarray,
    connect_4_cells: Connect4Cells | None = None,
) -> None:
    _, cols = board.shape
    if connect_4_cells is None:
        connect_4_cells = []

    table = Table(
        show_header=True,
        show_lines=True,
        header_style="bold magenta",
    )

    # Add columns for the board (7 columns for standard Connect 4)
    for col in range(cols):
        table.add_column(str(col), justify="center")

    # Add rows to the table, reversing the order to match the standard Connect 4 display
    for row_idx, row in enumerate(board):
        table.add_row(
            *[
                Align(
                    CELL_DISPLAY_VALUES[cell],
                    style="on green" if (row_idx, col_idx) in connect_4_cells else "",
                )
                for col_idx, cell in enumerate(row)
            ]
        )

    CONSOLE.print(table)
