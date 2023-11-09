import threading
import time
import socket
import controller as ctrl



class DroneConnection():

    def __init__(self, host: str, port: int, controller: ctrl.Controller, thread_pool: list):
        self.host = host
        self.port = port
        self.controller = controller

        # connection_thread
        thread_pool.append(threading.Thread(target= self.connection_handler))



    def connection_handler(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setblocking(False)

        last_cnt_print_time = 0
        rx_cnt = 0

        while True:
            tx_time = time.time()

            tx_str = self.controller.get_drone_tx_pack(tx_time)
            if(tx_str != ""):
                self.controller.ping.set_last_tx_timer(tx_time)
                s.sendto(tx_str.encode("ascii"), (self.host,self.port))
                #if(tx_str.find("rst_att") != -1):
                #    print(tx_str)

            try:
                rx_data, addr = s.recvfrom(1024)
                rx_data = rx_data.decode("ascii")
                if(rx_data != ""):
                    raw_packs = rx_data.splitlines()
                    for raw_pack in raw_packs:
                        pack = raw_pack.split(',')
                        #print(pack)
                        self.controller.rx_pack_sel(pack)

                    if(time.time() - last_cnt_print_time > 1):
                        last_cnt_print_time = time.time()
                        print("drone rx cnt 1s", rx_cnt)
                        rx_cnt = 0
                    else:
                        rx_cnt += 1
            except:
                pass





class AppConnection():

    def __init__(self, host: str, port: int, controller: ctrl.Controller, thread_pool: list):
        self.host = host
        self.port = port
        self.controller = controller

        # connection_thread
        thread_pool.append(threading.Thread(target= self.connection_handler))


    def connection_handler(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind((self.host, self.port))

        last_cnt_print_time = 0
        rx_cnt = 0

        while True:
            rx_data, addr = s.recvfrom(1024)
            rx_data = rx_data.decode("ascii")
            if(rx_data != ""):
                raw_packs = rx_data.splitlines()
                for raw_pack in raw_packs:
                    pack = raw_pack.split(',')
                    self.controller.rx_pack_sel(pack)

            if(time.time() - last_cnt_print_time > 1):
                last_cnt_print_time = time.time()
                print("app rx cnt 1s", rx_cnt)
                rx_cnt = 0
            else:
                rx_cnt += 1

            tx_str = self.controller.get_app_tx_pack(time.time())
            if(tx_str != ""):
                s.sendto(tx_str.encode("ascii"), addr)
                #if(tx_str.find("c_att") != -1):
                #    print(tx_str)

            


