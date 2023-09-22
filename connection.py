import threading
import time
import socket
import pack_process as p_proc


class DroneConnection():

    def __init__(self, host, port, data_obj_dict):
        self.host = host
        self.port = port
        self.client = None
        self.data_obj_dict = data_obj_dict

        self.disconnected_event = threading.Event()
        self.disconnected_event.set()

        connection_thread = threading.Thread(target= self.connectionHandler)
        rx_thread = threading.Thread(target= self.rxHandler)
        tx_thread = threading.Thread(target= self.txHandler)
        connection_thread.start()
        rx_thread.start()
        tx_thread.start()



    def rxHandler(self):
        while True:
            try:
                if(self.disconnected_event.is_set()):
                    time.sleep(0.5)
                    continue
                rx_buffer = self.client.recv(5000).decode('utf8')
                #print("[rx length]",drone_rx_buffer_len)
                #print("[Raw]",rx_buffer)
                pack_list = p_proc.getPack(rx_buffer)
                
                for pack in pack_list:

                    #===[data process]===
                    # [current attitude]
                    if(pack["type"] == "ca"):
                        self.data_obj_dict["current_attitude"].update(pack["data"])

            except Exception as error:
                print("drone Rx Except: ", error)
                self.disconnected_event.set()



    def txHandler(self):
        while True:
            try:
                if(self.disconnected_event.is_set()):
                    time.sleep(0.5)
                    continue
                
                #===[send data]===
                # [target attitude]
                if(self.data_obj_dict["target_attitude"].isNeedSend()):
                    outdata = "phta" + self.data_obj_dict["target_attitude"].getStr()
                    self.client.send(outdata.encode())

                time.sleep(0.1)

            except Exception as error:
                print("drone Tx Except: ", error)
                self.disconnected_event.set()



    def connectionHandler(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        s.bind((self.host, self.port))
        #s.setblocking(False)
        s.listen(5)

        while True:
            print("drone server waiting...")
            self.client, addr = s.accept()
            print("new drone client:", self.client)
            self.client.settimeout(5)
            self.disconnected_event.clear()

            self.disconnected_event.wait()
            print("drone timeout:", self.client)
            self.client.close()
            time.sleep(1)








class AppConnection():

    def __init__(self, host, port, data_obj_dict):
        self.host = host
        self.port = port
        self.client = None
        self.data_obj_dict = data_obj_dict

        self.disconnected_event = threading.Event()
        self.disconnected_event.set()

        connection_thread = threading.Thread(target= self.connectionHandler)
        rx_thread = threading.Thread(target= self.rxHandler)
        tx_thread = threading.Thread(target= self.txHandler)
        connection_thread.start()
        rx_thread.start()
        tx_thread.start()

        


    def rxHandler(self):
        while True:
            try:
                if(self.disconnected_event.is_set()):
                    time.sleep(0.5)
                    continue
                rx_buffer = self.client.recv(500).decode('ascii')
                #print("[rx length]",drone_rx_buffer_len)
                #print("[Raw]",rx_buffer)
                pack_list = p_proc.getPack(rx_buffer)
                
                for pack in pack_list:

                    #===[data process]===
                    # [current attitude]
                    if(pack["type"] == "ta"):
                        self.data_obj_dict["target_attitude"].update(pack["data"])

            except Exception as error:
                print("app Rx Except: ", error)
                self.disconnected_event.set()



    def txHandler(self):
        while True:
            try:
                if(self.disconnected_event.is_set()):
                    time.sleep(0.5)
                    continue
                
                #===[send data]===
                # [current attitude]
                if(self.data_obj_dict["current_attitude"].isNeedSend()):
                    outdata = "phca" + self.data_obj_dict["current_attitude"].getStr()
                    self.client.send(outdata.encode('ascii'))
                    #print("app send: ", outdata)

                time.sleep(0.03)

            except Exception as error:
                print("app Tx Except: ", error)
                self.disconnected_event.set()



    def connectionHandler(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        s.bind((self.host, self.port))
        #s.setblocking(False)
        s.listen(5)

        while True:
            print("app server waiting...")
            self.client, addr = s.accept()
            print("new app client:", self.client)
            self.client.settimeout(5)
            self.disconnected_event.clear()

            self.disconnected_event.wait()
            print("app timeout:", self.client)
            self.client.close()
            time.sleep(1)


