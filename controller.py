import pack_type as pt



class Controller():
    def __init__(self) -> None:
        self.current_attitude = pt.CurrentAttitude(0.1)
        self.target_attitude = pt.TargetAttitude(0.1)
        self.main_cmd_pwr_on = pt.MainCommand("pwr_on", 1, 0.5, 0.1)
        self.main_cmd_max_pwr = pt.MainCommand("max_pwr", 1, 0.5, 0.1)

        self.boot_ack_pack = "boot,2,0\n"
        self.boot_need_ack = False
        self.boot_ok = False
        

    # pack: [type, ack, payload]
    def configCommonSel(self, pack: list) -> None:
        if(pack[2] == 'pwr_on'):
            #print("m_cmd pwr_on rx")
            self.main_cmd_pwr_on.rxData(pack)
        elif(pack[2] == 'max_pwr'):
            #print("m_cmd max_pwr rx")
            self.main_cmd_max_pwr.rxData(pack)
            




    # pack: [type, ack, payload]
    def droneRxPack(self, pack: list) -> None:
        #print("drone rx pack: ", pack)
        if(pack[0] == 'boot'):
            self.boot_need_ack = True
        elif(pack[0] == 'c_att'):
            self.current_attitude.setData(pack)
        elif(pack[0] == 'cfg_comm'):
            self.configCommonSel(pack)
        elif(pack[0] == 'cfg_pid'):
            pass



    def droneTxPack(self, time: float) -> str:
        send_buffer = ""

        if(self.boot_need_ack):
            self.boot_ok = True
            self.boot_need_ack = False
            send_buffer += self.boot_ack_pack
            return send_buffer
        
        send_buffer += self.target_attitude.getTxStr(time)

        send_buffer += self.main_cmd_pwr_on.getTxDroneStr(time)
        send_buffer += self.main_cmd_max_pwr.getTxDroneStr(time)

        return send_buffer






    def appRxPack(self, pack: list) -> None:
        if(pack[0] == 't_att'):
            pass
        elif(pack[0] == 'cfg_comm'):
            pass
        elif(pack[0] == 'cfg_pid'):
            pass

        

    def appTxPack(self, time: float) -> str:
        send_buffer = ""
        
        send_buffer += self.current_attitude.getTxStr(time)

        #send_buffer += self.main_cmd_pwr_on.getTxAppStr(time)
        #send_buffer += self.main_cmd_max_pwr.getTxAppStr(time)

        return send_buffer
    