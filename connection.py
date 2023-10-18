import threading
import time
import socket
import controller as ctrl



class DroneConnection():

    def __init__(self, host: str, port: int, controller: ctrl.Controller, thread_pool: list):
        self.host = host
        self.port = port
        self.controller = controller
        self.send_interval = 0.01

        # connection_thread
        thread_pool.append(threading.Thread(target= self.connectionHandler))



    def connectionHandler(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setblocking(False)

        last_tx_time = 0
        last_cnt_print_time = 0
        rx_cnt = 0

        while True:
            tx_time = time.time()
            if(tx_time - last_tx_time > self.send_interval):
                last_tx_time = tx_time
                send_str = self.controller.droneTxPack(tx_time)
                if(send_str == ""):
                    send_str = "ping,0,0\n"
                s.sendto(send_str.encode("ascii"), (self.host,self.port))
                #print("tx!", time.time())

            try:
                rx_data, addr = s.recvfrom(1024)
                rx_data = rx_data.decode("ascii")
                if(rx_data != ""):
                    raw_packs = rx_data.splitlines()
                    for raw_pack in raw_packs:
                        pack = raw_pack.split(',')
                        #print(pack)
                        self.controller.droneRxPack(pack)

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
        thread_pool.append(threading.Thread(target= self.connectionHandler))


    def connectionHandler(self):
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
                    self.controller.appRxPack(pack)

            if(time.time() - last_cnt_print_time > 1):
                last_cnt_print_time = time.time()
                print("app rx cnt 1s", rx_cnt)
                rx_cnt = 0
            else:
                rx_cnt += 1

            tx_data = self.controller.appTxPack(time.time())
            if(tx_data != ""):
                s.sendto(tx_data.encode("ascii"), addr)

            


