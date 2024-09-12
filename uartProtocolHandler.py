import asyncio
from uartProtocol import UartProtokol, messageTypeData, cmdTypeData
from uartHal import RxTxFonk, sendframe
from uartDataManager import  setdataval

class SetDataValue:
    # Sabit değerler  
    STOP_CHARGE = 2
    START_CHARGE = 1

   
    END_TRANSACTION = 1
    NOT_END_TRANSACTION = 0
    START_BUZZER = 8

class UartHandler:

    def __init__(self, txHAL):
        self.txHAL = txHAL
    
    def sendStartCharging(self):
        sendframe.set_cmd_type(cmdTypeData.SET_DATA)
        sendframe.set_msg_type(messageTypeData.RUN_CTRL)
        sendframe.set_dataL(SetDataValue.START_CHARGE)
        self.txHAL.send_message()
    
    def sendMaxPower(self):
        sendframe.set_cmd_type(cmdTypeData.SET_DATA)
        sendframe.set_msg_type(messageTypeData.MAX_POWER)
        sendframe.set_dataL(setdataval.get_max_charge_val())
        self.txHAL.send_message()

    def sendStopCharging(self):
        sendframe.set_cmd_type(cmdTypeData.SET_DATA)
        sendframe.set_msg_type(messageTypeData.RUN_CTRL)
        sendframe.set_dataL(SetDataValue.STOP_CHARGE)
        self.txHAL.send_message()

    def sendReadEnergyIns(self):
        sendframe.set_cmd_type(cmdTypeData.READ_DATA)
        sendframe.set_msg_type(messageTypeData.ETOTAL)
        self.txHAL.send_message()

    def sendReadDeviceId(self):
        sendframe.set_cmd_type(cmdTypeData.READ_DATA)
        sendframe.set_msg_type(messageTypeData.DEVICE_ID)
        self.txHAL.send_message()

    def sendReadEnergyComplete(self):
        sendframe.set_cmd_type(cmdTypeData.READ_DATA)
        sendframe.set_msg_type(messageTypeData.ETOTAL_CHARGING_COMPLETE)
        self.txHAL.send_message()

    def sendReadChargingTime(self):
        sendframe.set_cmd_type(cmdTypeData.READ_DATA)
        sendframe.set_msg_type(messageTypeData.CHARGING_TIME)
        self.txHAL.send_message()

    def sendReadChargingTimeHour(self):
        sendframe.set_cmd_type(cmdTypeData.READ_DATA)
        sendframe.set_msg_type(messageTypeData.CHARGING_TIME_HOURS)
        self.txHAL.send_message()

    def sendReadPrms(self):
        sendframe.set_cmd_type(cmdTypeData.READ_DATA)
        sendframe.set_msg_type(messageTypeData.PRMS)
        self.txHAL.send_message()

    def sendReadErr(self):
        sendframe.set_cmd_type(cmdTypeData.READ_DATA)
        sendframe.set_msg_type(messageTypeData.ERR_STATUS)
        self.txHAL.send_message()

    def sendReadChargeFinished(self):
        sendframe.set_cmd_type(cmdTypeData.READ_DATA)
        sendframe.set_msg_type(messageTypeData.CHARGE_FINISHED)
        self.txHAL.send_message()

    '''def sendClearChargeSession(self):
        sendframe.set_cmd_type(cmdTypeData.SET_DATA)
        sendframe.set_msg_type(messageTypeData.RUN_CTRL)
        sendframe.set_dataL(SetDataValue.START_BUZZER)
        self.txHAL.send_message()'''

    def sendEndTransaction(self):
        sendframe.set_cmd_type(cmdTypeData.SET_DATA)
        sendframe.set_msg_type(messageTypeData.END_TRANSACTION_SEND)
        sendframe.set_dataL(SetDataValue.END_TRANSACTION)
        self.txHAL.send_message()

    def sendNotEndTransaction(self):
        sendframe.set_cmd_type(cmdTypeData.SET_DATA)
        sendframe.set_msg_type(messageTypeData.END_TRANSACTION_SEND)
        sendframe.set_dataL(SetDataValue.NOT_END_TRANSACTION)
        self.txHAL.send_message()

    def sendReadConnectorStatus(self):
        sendframe.set_cmd_type(cmdTypeData.READ_DATA)
        sendframe.set_msg_type(messageTypeData.CONNECTOR_STATUS)
        self.txHAL.send_message()

    def sendReadChargingStatus(self):
        sendframe.set_cmd_type(cmdTypeData.READ_DATA)    
        sendframe.set_msg_type(messageTypeData.CHARGING_STATUS)   
        self.txHAL.send_message() 
    
    def sendSetBuzzer(self):    
        sendframe.set_cmd_type(cmdTypeData.SET_DATA)    
        sendframe.set_msg_type(messageTypeData.CLEAR_CHARGE)    
        sendframe.set_dataL(setdataval.get_baz_val())    
        self.txHAL.send_message()

    async def handleSET_DATA(self):    
        """"
        self.sendMaxPower()  
        await asyncio.sleep(0.3)
               
        self.sendSetBuzzer()
        await asyncio.sleep(0.3)"""
        
        ''' self.sendClearChargeSession()
        await asyncio.sleep(0.3)'''
         
        if((setdataval.get_start_charge_val()== SetDataValue().START_CHARGE) ):
            
            self.sendStartCharging()    
            await asyncio.sleep(0.3)    
        else:
            self.sendStartCharging()
            #self.sendStopCharging()
            await asyncio.sleep(0.3)
        
        if(setdataval.get_transaction_val() == SetDataValue().END_TRANSACTION):
            self.sendEndTransaction()
            await asyncio.sleep(0.3)
        else:
            self.sendNotEndTransaction()
            await asyncio.sleep(0.3)

    async def handleREAD_DATA(self):
        
        self.sendReadEnergyIns()
        await asyncio.sleep(0.3)
        self.sendReadDeviceId()
        await asyncio.sleep(0.3)
        self.sendReadEnergyComplete()
        await asyncio.sleep(0.3)
        self.sendReadChargingTime()
        await asyncio.sleep(0.3)
        self.sendReadChargingTimeHour()
        await asyncio.sleep(0.3)
        self.sendReadPrms()
        await asyncio.sleep(0.3)
        self.sendReadErr()
        await asyncio.sleep(0.3)
        self.sendReadChargeFinished()
        await asyncio.sleep(0.3)
        self.sendReadConnectorStatus()
        await asyncio.sleep(0.3)
        
        self.sendReadChargingStatus()
        await asyncio.sleep(0.3)

    async def sendHandleUartFrame(self):
        while True:
            await self.handleREAD_DATA()
            await self.handleSET_DATA()



             
async def main():
    rxtx_fonk = RxTxFonk()
    myUart = UartProtokol(rxtx_fonk)
    uart_handler = UartHandler(rxtx_fonk  )
    await asyncio.gather(
        rxtx_fonk.receive_message(),
        myUart.reciveHandleUartFrame(),
        uart_handler.sendHandleUartFrame()
    )

asyncio.run(main())






