import datetime


class SimConfig:
    n_meters: int
    refresh_rate: float
    increment_mins: int
    server_address: tuple[str, int]
    ui_address: tuple[str, int]
    start_date: datetime.datetime
    end_date: datetime.datetime
    deviation: float

    def __init__(
        self,
        n_meters: int,
        refresh_rate: float,
        increment_mins: int,
        server_address: tuple[str, int],
        ui_address: tuple[str, int],
        start_date: datetime.datetime,
        end_date: datetime.datetime,
        deviation: float,
    ) -> None:
        self.n_meters = n_meters
        self.refresh_rate = refresh_rate
        self.increment_mins = increment_mins
        self.server_address = server_address
        self.ui_address = ui_address
        self.start_date = start_date
        self.end_date = end_date
        self.deviation = deviation


cfg = SimConfig(
    n_meters=12,
    refresh_rate=1,
    increment_mins=1,
    server_address=("localhost", 1234),
    ui_address=("localhost", 1235),
    start_date=datetime.datetime(2010, 1, 1, 10, 0, 0),
    end_date=datetime.datetime(2010, 1, 1, 19, 0, 0),
    deviation=0.1,
)
