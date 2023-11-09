from pack_type.core_pack import *
import copy


# force need ack respone
class CommonConfig(StreamCheckPack):
    def __init__(self, tag: str, init_value: int, tx_drone_interval: float, check_timeuout: float, tx_app_interval: float) -> None:
        self.tag = tag
        self.target_value = init_value
        self.current_drone_value = init_value
        super().__init__(tx_drone_interval, check_timeuout, tx_app_interval)


    def rx_data(self, pack: list) -> None:
        # pack len check
        if(len(pack) < 4):
            return
        
        # set target (rx pack from app)
        if(pack[1] == "0"):
            self.target_value = int(pack[3])
            self.on_rx_app_finish()
        # rx response (rx pack from drone)
        elif(pack[1] == "2"):
            self.current_drone_value = int(pack[3])
            self.on_rx_drone_finish(self.current_drone_value == self.target_value)
        else:
            print("[comm cfg]: rx invalid -> ", pack)


    def get_tx_drone_str(self, time: float) -> str:
        if(self.is_need_tx_drone(time)):
            tx_str = "comm_cfg,1,"
            tx_str += self.tag + ","
            tx_str += str(self.target_value) + "\n"
            self.on_tx_drone_finish(time)
            return tx_str
        else:
            return ""


    def get_tx_app_str(self, time: float) -> str:
        if(self.is_need_tx_app(time)):
            tx_str = "comm_cfg,0,"
            tx_str += self.tag + ","
            tx_str += str(self.current_drone_value) + "\n"
            self.on_tx_app_finish(time)
            return tx_str
        else:
            return ""




class V4dConfig(StreamCheckPack):
    def __init__(self, tag: str, init_value: list, tx_drone_interval: float, check_timeuout: float, tx_app_interval: float) -> None:
        self.tag = tag
        self.target_value = copy.deepcopy(init_value)
        self.current_drone_value = copy.deepcopy(init_value)
        super().__init__(tx_drone_interval, check_timeuout, tx_app_interval)


    def rx_data(self, pack :list) -> None:
        # pack len check
        if(len(pack) < 7):
            return
        
        # set target (rx pack from app)
        if(pack[1] == "0"):
            self.target_value[0] = float(pack[3])
            self.target_value[1] = float(pack[4])
            self.target_value[2] = float(pack[5])
            self.target_value[3] = float(pack[6])
            self.on_rx_app_finish()
        # rx response (rx pack from drone)
        elif(pack[1] == "2"):
            self.current_drone_value[0] = float(pack[3])
            self.current_drone_value[1] = float(pack[4])
            self.current_drone_value[2] = float(pack[5])
            self.current_drone_value[3] = float(pack[6])
            self.on_rx_drone_finish(self.current_drone_value == self.target_value)
        else:
            print("[v4d cfg]: rx invalid -> ", pack)


    def get_tx_drone_str(self, time: float) -> str:
        if(self.is_need_tx_drone(time)):
            tx_str = "v4d_cfg,1,"
            tx_str += self.tag + ","
            tx_str += str(self.target_value[0]) + ","
            tx_str += str(self.target_value[1]) + ","
            tx_str += str(self.target_value[2]) + ","
            tx_str += str(self.target_value[3]) + "\n"
            self.on_tx_drone_finish(time)
            return tx_str
        else:
            return ""


    def get_tx_app_str(self, time: float) -> str:
        if(self.is_need_tx_app(time)):
            tx_str = "v4d_cfg,0,"
            tx_str += self.tag + ","
            tx_str += str(self.current_drone_value[0]) + ","
            tx_str += str(self.current_drone_value[1]) + ","
            tx_str += str(self.current_drone_value[2]) + ","
            tx_str += str(self.current_drone_value[3]) + "\n"
            self.on_tx_app_finish(time)
            return tx_str
        else:
            return ""