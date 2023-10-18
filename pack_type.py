import numpy as np
import time
import copy


class BasePack:
    def __init__(self, send_interval: float) -> None:
        self.last_send = 0.0 # seconds
        self.send_interval = send_interval


    def isNeedSend(self, time: float) -> bool:
        return (time - self.last_send > self.send_interval)


    def onSendTxFinish(self, time: float):
        # update last send time
        self.last_send = time

    def onRxFinish(self):
        # mark need send
        self.last_send = 0.0

        



class ConfigPack:
    def __init__(self, send_drone_interval: float, ack_timeout: float, send_app_interval: float) -> None:
        self.waiting_ack = False
        self.last_send_drone = 0.0 # seconds
        self.last_send_app = 0.0 # seconds
        self.send_drone_interval = send_drone_interval
        self.send_app_interval = send_app_interval
        self.ack_timeout = ack_timeout
        

    def onRxAckValid(self):
        # mark not waiting ack
        self.waiting_ack = False


    def onTxDroneFinish(self, time: float):
        # mark need ack
        self.waiting_ack = True
        # update last send time
        self.last_send_drone = time


    def onTxAppFinish(self, time: float):
        # update last send time
        self.last_send_app = time


    def isNeedSendDrone(self, time: float) -> bool:
        if(self.waiting_ack):
            return (time - self.last_send_drone > self.ack_timeout)
        else:
            return (time - self.last_send_drone > self.send_drone_interval)


    def isNeedSendApp(self, time: float) -> bool:
        return (time - self.last_send_app > self.send_app_interval)







class Ping(BasePack):
    def __init__(self, send_interval: float) -> None:
        super().__init__(send_interval)


    def getSendStr(self, time: float) -> str:
        if(self.isNeedSend(time)):
            send_str = "ping,0," + str(time) + "\n"
            self.onSendTxFinish(time)
            return send_str
        else:
            return ""






class CurrentAttitude(BasePack):
    def __init__(self, send_interval: float) -> None:
        super().__init__(send_interval)
        self.attitude = [1.0, 0.0, 0.0, 0.0] # quaternion
        self.dt = 1000


    # make sure attitude is normalized
    def forceNormalized(self):
        len = self.attitude[0]**2 + self.attitude[1]**2 + self.attitude[2]**2 + self.attitude[3]**2
        if(abs(len - 1.0) > 0.1):
            self.attitude = [1.0, 0.0, 0.0, 0.0]


    # pack: [attitude]
    def setData(self, pack: list) -> None:
        #print("c_att recv: ", pack)
        self.dt = int(pack[2])
        self.attitude[0] = float(pack[3])
        self.attitude[1] = float(pack[4])
        self.attitude[2] = float(pack[5])
        self.attitude[3] = float(pack[6])
        self.forceNormalized()
        #print("c_att current: ", self.attitude)
        self.onRxFinish()


    def get(self) -> np.array:
        attitude = np.array([self.attitude[0],
                    self.attitude[1],
                    self.attitude[2],
                    self.attitude[3]
                    ])
        return attitude
    

    def getTxStr(self, time: float) -> str:
        if(self.isNeedSend(time)):
            send_str = "c_att,0," 
            send_str += str(self.dt) + ","
            send_str += str(self.attitude[0]) + ","
            send_str += str(self.attitude[1]) + ","
            send_str += str(self.attitude[2]) + ","
            send_str += str(self.attitude[3]) + "\n"
            self.onSendTxFinish(time)
            return send_str
        else:
            return ""
    





class TargetAttitude(BasePack):
    def __init__(self, send_interval: float) -> None:
        super().__init__(send_interval)
        self.attitude = [0, 0, 0] # euler


    # pack: [attitude]
    def setData(self, pack: list) -> None:
        #print("[pack_data]", data)
        self.attitude[0] = int(pack[0])
        self.attitude[1] = int(pack[1])
        self.attitude[2] = int(pack[2])
        self.onRxFinish()
    

    def getTxStr(self, time: float) -> str:
        if(self.isNeedSend(time)):
            send_str = "t_att,0,"
            send_str += str(self.attitude[0]) + ","
            send_str += str(self.attitude[1]) + ","
            send_str += str(self.attitude[2]) + "\n"
            self.onSendTxFinish(time)
            return send_str
        else:
            return ""





# force need ack respone
class MainCommand(ConfigPack):
    def __init__(self, cmd: str, send_interval: float, ack_timeout: float, send_app_interval: float) -> None:
        self.cmd = cmd
        self.value = 0
        self.current_drone_value = 0
        super().__init__(send_interval, ack_timeout, send_app_interval)
        

    # pack: [type, ack, payload]
    def rxData(self, pack :list) -> None:
        #print("ack data: ", self.ack_data)
        # no ack need (app->host)
        if(pack[1] == "0"):
            self.data[3] = pack[3]
        # ack pack
        elif(pack[1] == "2"):
            self.current_drone_value = int(pack[3])
            if(self.current_drone_value == self.value):
                self.onRxAckValid()
        else:
            print("[mcmd]: rx invalid -> ", pack)


    def getTxDroneStr(self, time: float) -> str:
        if(self.isNeedSendDrone(time)):
            send_str = "cfg_comm,1,"
            send_str += self.cmd + ","
            send_str += str(self.value) + "\n"
            self.onTxDroneFinish(time)
            return send_str
        else:
            return ""


    def getTxAppStr(self, time: float) -> str:
        if(self.isNeedSendApp(time)):
            send_str = "cfg_comm,0,"
            send_str += self.cmd + ","
            send_str += str(self.current_drone_value) + "\n"
            self.onTxAppFinish(time)
            return send_str
        else:
            return ""
