import threading
import numpy as np


        

class PackProcess:
    def __init__(self):
        self.pack_list = []

    # decode from buffer
    # return pack list
    def getPack(self, rx_buffer: str) ->None :
        pack_list = []
        rx_buffer_len = len(rx_buffer)
        idx = 0
        while(idx < rx_buffer_len):
            pack = {"type":None, "data":None}

            # find pack header
            header_idx = rx_buffer[idx:].find("ph") + idx
            #print("[idx]", idx, "[h_idx]", header_idx)
            
            # if pack header not found or pack too short, break the loop
            if(header_idx < idx or (rx_buffer_len - header_idx) < 7):
                print("buffer end")
                break

            # get pack type and data length
            pack["type"] = rx_buffer[header_idx+2:header_idx+4]
            data_length = int(rx_buffer[header_idx+4:header_idx+7])
            #print("[p_type]", pack["type"], "data_len", data_length)

            # check data integrity
            if(rx_buffer_len < header_idx+7+data_length):
                print("data break")
                break

            # get data
            if(data_length == 0):
                pack["data"] = None
            else:
                pack["data"] = rx_buffer[header_idx+7:header_idx+7+data_length]

            # prepare next loop
            idx = header_idx+7+data_length

            self.pack_list.append(pack)


    def process(self, pack: list) ->None:
        pass



class CurrentAttitude:
    def __init__(self):
        self.frame = 0
        self.last_frame = -1
        self.need_send_event = threading.Event()
        self.attitude = [1.0, 0.0, 0.0, 0.0] # quaternion

    def checkValid(self):
        len = self.attitude[0]**2 + self.attitude[1]**2 + self.attitude[2]**2 + self.attitude[3]**2
        if(abs(len - 1.0) > 0.1):
            self.attitude = [1.0, 0.0, 0.0, 0.0]

    def update(self, data):
        #print("[pack_data]", data)
        self.frame = int(data[0:5])
        #print(frame)

        if(self.last_frame == -1):
            #print("frame new", frame)
            nop = 1
        elif( (self.frame - self.last_frame) != 1 and (self.frame - self.last_frame) != -255 ):
            print("frame skip detect")
        
        self.last_frame = self.frame

        self.attitude[0] = int(data[10:17]) / 1.0e5
        self.attitude[1] = int(data[17:24]) / 1.0e5
        self.attitude[2] = int(data[24:31]) / 1.0e5
        self.attitude[3] = int(data[31:38]) / 1.0e5
        self.checkValid()

        self.need_send_event.set()


    def get(self):
        attitude = np.array([self.attitude[0],
                    self.attitude[1],
                    self.attitude[2],
                    self.attitude[3]
                    ])
        return attitude
    

    def getStr(self):
        attitude = f'{self.attitude[0]:.6f}'[0:8] + \
              f'{self.attitude[1]:.6f}'[0:8] + \
              f'{self.attitude[2]:.6f}'[0:8] + \
              f'{self.attitude[3]:.6f}'[0:8]
        len_str = str(len(attitude)).zfill(3)
        self.need_send_event.clear()
        return len_str + attitude
    

    def isNeedSend(self):
        return self.need_send_event.is_set()






class TargetAttitude:
    def __init__(self):
        self.frame = 0
        self.last_frame = -1
        self.need_send_event = threading.Event()
        self.attitude = [0.0, 0.0, 0.0] # euler


    def update(self, data):
        #print("[pack_data]", data)
        self.attitude[0] = int(data[0:7]) / 1.0e3
        self.attitude[1] = int(data[7:14]) / 1.0e3
        self.attitude[2] = int(data[14:21]) / 1.0e3
        self.need_send_event.set()


    def get(self):
        attitude = np.array([self.attitude[0],
                    self.attitude[1],
                    self.attitude[2],
                    ])
        return attitude
    

    def getStr(self):
        attitude = str(self.attitude[0]).zfill(7) + \
              str(self.attitude[1]).zfill(7) + \
              str(self.attitude[2]).zfill(7)
        len_str = str(len(attitude)).zfill(3)
        self.need_send_event.clear()
        return len_str + attitude
    

    def isNeedSend(self):
        return self.need_send_event.is_set()