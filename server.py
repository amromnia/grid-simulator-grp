import datetime
import socket
import threading
import time
import pickle
from typing import Any
from src.core.data_generator import make_instance_generator
from src.core.msg_types import UIUpdate
from src.config import cfg

data_generator = make_instance_generator(cfg.deviation)


def client_connection(conn, addr, results):
    print(f"Connected by {addr}")
    gen, con = data_generator(t)
    conn.sendall(pickle.dumps({"type": "power", "generation": gen, "consumption": con}))
    data = pickle.loads(conn.recv(1024))
    response_type = data["type"]
    match response_type:
        case "power":
            results[addr] = data["response"]["surplus"]
        case "trade":
            return

def moment(t, conns: list[tuple[socket.socket, tuple[str, int]]]):
    """Run a moment of the simulation where meters recieve data and send back a response."""
    print(f"Time: {t}")
    threads: list[threading.Thread] = []
    results: dict[tuple[str, int], float] = {}
    for conn, addr in conns:
        t1 = threading.Thread(target=client_connection, args=(conn, addr, results))
        t1.start()
        threads.append(t1)
    print("Threads started")
    for t1 in threads:
        t1.join()
    print("Threads finished")
    return results


def update_ui(ui_conn: socket.socket, results: dict[tuple[str, int], float]):
    ui_update: UIUpdate = {
        "type": "update",
        "time": t.strftime("%H:%M:%S"),
        "meters": results,
    }
    ui_conn.sendall(pickle.dumps(ui_update))
    print(results)


if __name__ == "__main__":
    ui_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ui_conn.connect(cfg.ui_address)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(cfg.server_address)
        s.listen(cfg.n_meters)
        print("Server started")
        conns: list[tuple[socket.socket, tuple[str, int]]] = []
        print("Waiting to connect to meters...")
        for _ in range(cfg.n_meters):
            conn, addr = s.accept()
            conns.append((conn, addr))
        t = cfg.start_date
        while t < cfg.end_date:
            res = moment(t, conns)
            update_ui(ui_conn, res)
            t += datetime.timedelta(minutes=cfg.increment_mins)
            time.sleep(cfg.refresh_rate)
