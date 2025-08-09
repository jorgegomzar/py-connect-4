import socket
from itertools import cycle
from typing import Iterator

import numpy as np
from loguru import logger

from connect_4.online.utils import HOST, PORT, GameState, Player, recv, send
from connect_4.utils import (
    CELL_DISPLAY_VALUES,
    COLS,
    ROWS,
    find_next_free_row,
    get_connect_4_cells,
)


def main():
    board = np.zeros((ROWS, COLS))

    players: dict[Player, socket.socket] = {}

    game_state = GameState(board)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        logger.info("Waiting for 2 players to connect...")

        for player_idx in range(2):
            conn, addr = s.accept()
            logger.info(f"Player {player_idx} connected from {addr}")
            players[player_idx] = conn  # type: ignore

        player_cycle: Iterator[Player] = cycle([1, 2])
        game_state.turn = next(player_cycle)

        while True:
            # Sync game state with all players
            for player, conn in players.items():
                game_state.is_player_turn = player == game_state.turn
                send(conn, game_state)

            if game_state.winner:
                logger.success(f"Winner is {game_state.winner}")
                break

            # Validate player choice
            move = recv(players[game_state.turn])
            if move is None or not str(move).isnumeric() or not (0 <= int(move) < COLS):
                logger.warning(
                    f"Player {CELL_DISPLAY_VALUES[game_state.turn]} provided invalid input"
                )
                continue

            move = int(move)

            try:
                row = find_next_free_row(board[:, move])
            except ValueError:
                logger.warning(
                    f"Player {CELL_DISPLAY_VALUES[game_state.turn]} chose a column that is full"
                )
                continue

            # Valid input
            board[row, move] = game_state.turn

            # We do this to color the winner cells in clients' terminals
            game_state.connect_4_cells = get_connect_4_cells(board)
            if game_state.connect_4_cells:
                game_state.winner = game_state.turn

            game_state.turn = next(player_cycle)

        for current_player_conn in players.values():
            current_player_conn.close()


if __name__ == "__main__":
    main()
