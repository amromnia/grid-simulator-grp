import socket
from typing import Literal
from src.core.meter import Meter
from src.config import cfg
BUFFER_SIZE = 512


def mksocket() -> socket.socket:
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)


if __name__ == "__main__":
    meters: list[Meter] = [
        Meter(mksocket(), cfg.server_address, BUFFER_SIZE) for _ in range(cfg.n_meters)
    ]
    while True:
        threads = [m.mkthread() for m in meters]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        print("Iteration finished")
