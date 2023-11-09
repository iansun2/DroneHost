from pack_type.core_pack import *
import numpy as np
import copy
import time


class Ping(StreamPack):
    def __init__(self, tx_interval: float) -> None:
        super().__init__(tx_interval)


    def get_tx_str(self, time: float) -> str:
        if(self.is_need_tx(time)):
            tx_str = "ping,0," + str(time) + "\n"
            self.on_tx_finish(time)
            return tx_str
        else:
            return ""
        

    def set_last_tx_timer(self, time: float) -> None:
        self.last_tx_time = time

        



class V4dStream(StreamPack):
    def __init__(self, tag: str, init_value: list, tx_interval: float) -> None:
        super().__init__(tx_interval)
        self.tag = tag
        self.value = copy.deepcopy(init_value)
        self.tx_interval = tx_interval


    def set_data(self, value: list) -> None:
        self.value = copy.deepcopy(value)


    def rx_data(self, pack: list) -> None:
        if(len(pack) < 6):
            return
        self.value[0] = float(pack[3])
        self.value[1] = float(pack[4])
        self.value[2] = float(pack[5])
        self.value[3] = float(pack[6])
        self.on_rx_finish()


    def get_data(self) -> list:
        return copy.deepcopy(self.value)
    

    def get_tx_str(self, time: float) -> str:
        if(self.is_need_tx(time)):
            tx_str = "v4d_stream,0," 
            tx_str += self.tag + ","
            tx_str += str(self.value[0]) + ","
            tx_str += str(self.value[1]) + ","
            tx_str += str(self.value[2]) + ","
            tx_str += str(self.value[3]) + "\n"
            self.on_tx_finish(time)
            return tx_str
        else:
            return ""





    # filt unnormalize vector4
    def filt_unnormalized(vector4: list) -> list:
        len = vector4[0]**2 + vector4[1]**2 + vector4[2]**2 + vector4[3]**2
        if(abs(len - 1.0) > 0.01):
            return [1.0, 0.0, 0.0, 0.0]
        else:
            return vector4