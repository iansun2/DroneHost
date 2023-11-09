class StreamPack:
    def __init__(self, tx_interval: float) -> None:
        self.last_tx_time = 0.0 # seconds
        self.tx_interval = tx_interval


    def is_need_tx(self, time: float) -> bool:
        return (time - self.last_tx_time > self.tx_interval)


    def on_tx_finish(self, time: float):
        # update last tx time
        self.last_tx_time = time

    def on_rx_finish(self):
        # mark tx immediately
        self.last_tx_time = 0.0

        



class StreamCheckPack:
    def __init__(self, tx_drone_interval: float, check_timeout: float, tx_app_interval: float) -> None:
        self.last_tx_drone_time = 0.0 # seconds
        self.last_tx_app_time = 0.0 # seconds
        self.tx_drone_interval = tx_drone_interval
        self.tx_app_interval = tx_app_interval
        self.check_timeout = check_timeout
        self.response_match = False


    def on_rx_app_finish(self):
        # mark tx immediately
        self.last_tx_drone_time = 0


    def on_rx_drone_finish(self, response_match: bool):
        # tx current drone state to app immediately
        self.last_tx_app_time = 0
        # mark response match
        self.response_match = response_match


    def on_tx_drone_finish(self, time: float):
        # mark response not match
        self.response_match = False
        # update last tx time
        self.last_tx_drone_time = time


    def on_tx_app_finish(self, time: float):
        # update last tx time
        self.last_tx_app_time = time


    def is_need_tx_drone(self, time: float) -> bool:
        if(not self.response_match):
            return (time - self.last_tx_drone_time > self.check_timeout)
        else:
            return (time - self.last_tx_drone_time > self.tx_drone_interval)


    def is_need_tx_app(self, time: float) -> bool:
        return (time - self.last_tx_app_time > self.tx_app_interval)

