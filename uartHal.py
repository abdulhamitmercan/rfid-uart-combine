import serial
import asyncio
from dataclasses import dataclass

@dataclass
class UARTFrame:
    header: int = 0x62  # Sabit değer
    cmd_type: int = 0x00
    msg_type: int = 0x00
    dataH: int = 0x00
    dataL: int = 0x00
    eof: int = 0x6B  # Sabit değer

    def __post_init__(self):
        # Her değeri 1 byte (0xFF)
        self.cmd_type &= 0xFF
        self.msg_type &= 0xFF
        self.dataH &= 0xFF
        self.dataL &= 0xFF

    @property
    def rsv1(self):
        return 0x00  # Sabit değer

    @property
    def rsv0(self):
        return 0x00  # Sabit değer

    def get_cmd_type(self):
        return self.cmd_type

    def get_msg_type(self):
        return self.msg_type

    def get_dataH(self):
        return self.dataH

    def get_dataL(self):
        return self.dataL

    def set_cmd_type(self, value):
        self.cmd_type = value & 0xFF

    def set_msg_type(self, value):
        self.msg_type = value & 0xFF

    def set_dataH(self, value):
        self.dataH = value & 0xFF

    def set_dataL(self, value):
        self.dataL = value & 0xFF

sendframe = UARTFrame()
recieveframe = UARTFrame()

ser = serial.Serial("/dev/ttyS0", 9600)

import asyncio

class RxTxFonk:
    def __init__(self):
        self.recieve_message_err_status = None
        self.rxSuccess = 0

    def uartformat_to_rawdata_send_message(self): 
        byte_list = [
            sendframe.header,
            sendframe.get_cmd_type(),
            sendframe.get_msg_type(),
            sendframe.rsv1,
            sendframe.rsv0,
            sendframe.get_dataH(),
            sendframe.get_dataL(),
            sendframe.eof,
        ]
        return bytearray(byte_list)

    def rawdata_to_uartformat_recieve_message(self, received_message):
        if len(received_message) != 8:
            print("Geçersiz mesaj uzunluğu:", len(received_message))
            return None
        else:
            byte_list = [0] * 8
            for index, byte in enumerate(received_message):
                byte_list[index] = byte

            if byte_list[0] == 0x62 and byte_list[3] == 0x00 and byte_list[4] == 0x00 and byte_list[7] == 0x6B:
                recieveframe.set_cmd_type(byte_list[1])
                recieveframe.set_msg_type(byte_list[2])
                recieveframe.set_dataH(byte_list[5])
                recieveframe.set_dataL(byte_list[6])
                self.recieve_message_err_status = 0
                
                self.rxSuccess = 1
                
                return self.recieve_message_err_status
            else:
                print("Hatalı mesaj alındı")
                self.recieve_message_err_status = 1
                return self.recieve_message_err_status

    def send_message(self):
        #while True:
        formatted_message = self.uartformat_to_rawdata_send_message()
            #await asyncio.sleep(2)
        ser.write(formatted_message)
            #await asyncio.sleep(0.01)

    async def receive_message(self):
        while True:
            if ser.in_waiting >= 8:
                received_data = ser.read()
                await asyncio.sleep(0.03)
                data_left = ser.in_waiting
                received_data += ser.read(data_left)
                recieve_message_err_status = self.rawdata_to_uartformat_recieve_message(received_data)
                """  
                if recieve_message_err_status == 1:
                    print("Alınan veri:")
                    for index, byte in enumerate(received_data):
                        print(f"Bayt {index}: {byte:02X}")"""
                
            await asyncio.sleep(0.1)
        

            

