import pickle
import socket
from dataclasses import dataclass, field
from typing import Any, Literal

import numpy as np

from connect_4.utils import Connect4Cells

# TODO: these should be asked to the user
HOST = "0.0.0.0"
PORT = 65432


Player = Literal[1, 2]


@dataclass()
class GameState:
    board: np.ndarray
    turn: int = 1
    is_player_turn: bool = False
    winner: Player | None = None
    connect_4_cells: Connect4Cells = field(default_factory=list)


def send(conn: socket.socket, obj: Any) -> None:
    conn.sendall(pickle.dumps(obj))


def recv(conn: socket.socket) -> Any | None:
    data = b""
    while True:
        chunk = conn.recv(4096)
        if not chunk:
            break
        data += chunk
        try:
            return pickle.loads(data)
        except Exception:
            continue
    return None
