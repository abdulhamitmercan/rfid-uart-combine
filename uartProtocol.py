from uartHal import UARTFrame, recieveframe, RxTxFonk
from uartDataManager import setDataResponse,readDataResponse 
import asyncio

# Command and message types

class CmdTypeData:
    SET_DATA = 0
    SET_DATA_RESPONSE = 1
    READ_DATA = 2
    READ_DATA_RESPONSE = 3


class MessageTypeData:
    MODE = 0
    RUN_CTRL = 1
    ETOTAL = 2
    ETOTAL_CHARGING_COMPLETE = 3
    CHARGING_TIME = 4
    PRMS = 5
    ERR_STATUS = 6
    CHARGE_FINISHED = 7
    CLEAR_CHARGE = 8
    END_TRANSACTION_SEND = 9
    CHARGING_STATUS = 10
    CONNECTOR_STATUS = 11
    CHARGING_TIME_HOURS = 12
    DEVICE_ID = 13
    MAX_POWER = 14
    
messageTypeData = MessageTypeData()
cmdTypeData = CmdTypeData()




class UartProtokol:
    def __init__(self, UART_HAL):
        self.recieve_message_err_status = 0
        self.UART_HAL = UART_HAL
        
    def handleSET_DATA_RES(self):
        print("set data response")
        if recieveframe.get_msg_type() == messageTypeData.MODE:
            pass
        elif recieveframe.get_msg_type() == messageTypeData.RUN_CTRL:
            setDataResponse.setRunControl(recieveframe.get_dataL())
            print(f"runcntrl: {recieveframe.get_dataL()}")

            
        elif recieveframe.get_msg_type() == messageTypeData.CLEAR_CHARGE:
            setDataResponse.setClearChargeSession(recieveframe.get_dataL())
            print(f"clear charge:{recieveframe.get_dataL()}")
            
        elif recieveframe.get_msg_type() == messageTypeData.END_TRANSACTION_SEND:
            setDataResponse.setEndTransaction(recieveframe.get_dataL())
            print(f"end transaction send:{recieveframe.get_dataL()}")

    def handleREAD_DATA_RES(self):
        print("read data response")
        if recieveframe.get_msg_type() == messageTypeData.MODE:
            pass
        elif recieveframe.get_msg_type() == messageTypeData.RUN_CTRL:
            readDataResponse.setChargingStartStop(recieveframe.get_dataL())
            print(f"charging start stop:{recieveframe.get_dataL()}")
            
        elif recieveframe.get_msg_type() == messageTypeData.ETOTAL_CHARGING_COMPLETE:
            readDataResponse.setEnergyTotalComplate(recieveframe.get_dataL())
            print(f"read energy:{recieveframe.get_dataL()}") 
            
        elif recieveframe.get_msg_type() == messageTypeData.CHARGING_TIME:
            readDataResponse.setTimeSeconds(recieveframe.get_dataL())
            readDataResponse.setTimeMinutes(recieveframe.get_dataH())
            print(f"read timesaniye{recieveframe.get_dataL()}")
            print(f"read timedakika{recieveframe.get_dataH()}")
        
        elif recieveframe.get_msg_type() == messageTypeData.CHARGING_TIME_HOURS :
            readDataResponse.setTimeHours(recieveframe.get_dataL())
            print("read device time hours ")  
            
        elif recieveframe.get_msg_type() == messageTypeData.PRMS:
            readDataResponse.setRmsPowerValue(recieveframe.get_dataL())
            print(f"read rms value of power:{recieveframe.get_dataL()}")
            
        elif recieveframe.get_msg_type() == messageTypeData.ERR_STATUS:
            readDataResponse.setErrorType(recieveframe.get_dataL())
            print(f"type of error:{recieveframe.get_dataL()}")
            
        elif recieveframe.get_msg_type() == messageTypeData.CHARGE_FINISHED:
            readDataResponse.setChargeFinished(recieveframe.get_dataL())
            print(f"charge finish:{recieveframe.get_dataL()}")
            
        elif recieveframe.get_msg_type() == messageTypeData.CHARGING_STATUS:
            print(f"charge status:{recieveframe.get_dataL()}")
            readDataResponse.setChargingStatus(recieveframe.get_dataL())
            
            
            
        elif recieveframe.get_msg_type() == messageTypeData.CONNECTOR_STATUS:
            readDataResponse.setConnectorStatus(recieveframe.get_dataL())
            print(f"conn status:{recieveframe.get_dataL()}")
            
        elif recieveframe.get_msg_type() == messageTypeData.DEVICE_ID :
            readDataResponse.setDeviceId(recieveframe.get_dataL)
            print("read device id")
 

    async def reciveHandleUartFrame(self):
        while True:
            if(self.UART_HAL.rxSuccess == 1):
                if recieveframe.get_cmd_type() == cmdTypeData.SET_DATA_RESPONSE:
                    self.handleSET_DATA_RES()
                elif recieveframe.get_cmd_type() == cmdTypeData.READ_DATA_RESPONSE:
                    self.handleREAD_DATA_RES()
                    
                self.UART_HAL.rxSuccess = 0
                
                

            await asyncio.sleep(0.1)
