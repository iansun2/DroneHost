from pack_type.stream_pack import *
from pack_type.stream_check_pack import *




class Controller():
    def __init__(self) -> None:
        self.boot_ack_pack = "boot,2,0\n"
        self.boot_need_ack = False
        self.boot_ok = False
        self.ping = Ping(0.02)
        self.current_attitude = V4dStream("c_att", [1.0, 0.0, 0.0, 0.0], tx_interval=0.1)
        self.target_attitude = V4dStream("t_att", [0.0, 0.0, 0.0, 0.0], tx_interval=0.1)
        self.pwr_on_cfg = CommonConfig("pwr_on", 0,
                                        tx_drone_interval=1,
                                        check_timeuout=0.5,
                                        tx_app_interval=0.1
                                    )
        self.max_pwr_cfg = CommonConfig("max_pwr", 0,
                                        tx_drone_interval=1,
                                        check_timeuout=0.5,
                                        tx_app_interval=0.1
                                    )
        self.rst_att_cfg = CommonConfig("rst_att", 0,
                                        tx_drone_interval=1,
                                        check_timeuout=0.5,
                                        tx_app_interval=0.1
                                    )
        self.kpid_cfg = V4dConfig("kpid", [5.0, 0.0, 0.0, 0.0],
                                    tx_drone_interval=1,
                                    check_timeuout=0.5,
                                    tx_app_interval=0.1
                                )
        

        self.stream_drone_list = [self.target_attitude,
                                ]
        
        self.stream_app_list = [self.current_attitude,
                            ]

        self.config_list = [self.pwr_on_cfg, 
                            self.max_pwr_cfg, 
                            self.rst_att_cfg, 
                            self.kpid_cfg
                        ]



    # pack: [type, ack, payload]
    def rx_pack_sel(self, pack: list) -> None:
        #print("drone rx pack: ", pack)
        # boot
        if(pack[0] == 'boot'):
            print("rx drone boot pack")
            self.boot_need_ack = True

        # stream
        elif(pack[0] == 'v4d_stream'):
            # drone
            for pack_obj in self.stream_drone_list:
                if(pack[2] == pack_obj.tag):
                    pack_obj.rx_data(pack)
            
            # app
            for pack_obj in self.stream_app_list:
                if(pack[2] == pack_obj.tag):
                    pack_obj.rx_data(pack)
        
        # config
        elif(pack[0] == 'comm_cfg' or pack[0] == 'v4d_cfg'):
            for pack_obj in self.config_list:
                if(pack[2] == pack_obj.tag):
                    pack_obj.rx_data(pack)

        # ping
        elif(pack[0] == 'ping'):
            pass
            
        # unknown
        else:
            print("unknown pack: ", pack)



    def get_drone_tx_pack(self, time: float) -> str:
        tx_buffer = ""

        if(self.boot_need_ack):
            self.boot_ok = True
            self.boot_need_ack = False
            tx_buffer += self.boot_ack_pack
            return tx_buffer
        
        # tx ping
        tx_buffer += self.ping.get_tx_str(time)
        
         # tx stream (drone)
        for pack_obj in self.stream_drone_list:
            tx_buffer += pack_obj.get_tx_str(time)

        # tx config
        for pack_obj in self.config_list:
            tx_buffer += pack_obj.get_tx_drone_str(time)

        return tx_buffer
    


    def get_app_tx_pack(self, time: float) -> str:
        tx_buffer = ""
        
        # tx stream (app)
        for pack_obj in self.stream_app_list:
            tx_buffer += pack_obj.get_tx_str(time)

        # tx config
        for pack_obj in self.config_list:
            tx_buffer += pack_obj.get_tx_app_str(time)

        return tx_buffer
    