# pn532_reader.py

import asyncio
import board
import busio
from digitalio import DigitalInOut
from adafruit_pn532.i2c import PN532_I2C
from debug_logger import DebugLogger
from uartDataManager import setdataval
class IdTag:
    def __init__(self):
        self._idTag = None
        self.a = None
    def setIdTag(self, idTag):
        self._idTag = idTag
        print(f"New RFID tag set: {self._idTag}")

    def getIdTag(self):
        return self._idTag
    
    def update_a(self):
        if self._idTag == "03193E95":
            setdataval.set_start_charge_val(0)
        else:
            setdataval.set_start_charge_val(1)
            
idtagus = IdTag()


class PN532Reader:
    def __init__(self, logger=None):
        self.logger = logger
        self.idTag = bytearray(b'')
        try:
            self.pn532 = self.initialize_pn532()
        except ValueError as e:
            self.logger.error(f"Initialization Error: {e}", filename="pn532_reader.py", category="PN532Reader", status="ERROR")
            raise

    def initialize_pn532(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        self.irq_pin = DigitalInOut(board.D4)
        return PN532_I2C(i2c, debug=False, irq=self.irq_pin)

    def setup(self):
        try:
            ic, ver, rev, support = self.pn532.firmware_version
            self.logger.info(f"Found PN532 with firmware version: {ver}.{rev}", filename="pn532_reader.py", category="PN532Reader", status="INFO")
            self.pn532.SAM_configuration()
            self.logger.info("PN532 configured to communicate with MiFare cards.", filename="pn532_reader.py", category="PN532Reader", status="INFO")
        except Exception as e:
            self.logger.error(f"Setup Error: {e}", filename="pn532_reader.py", category="PN532Reader", status="ERROR")

    async def listen_for_cards(self):
        try:
            self.pn532.listen_for_passive_target()
            self.logger.info("Waiting for RFID/NFC card...", filename="pn532_reader.py", category="PN532Reader", status="WAITING")
            while True:
                if self.irq_pin.value == 0:
                    uid = self.pn532.get_passive_target()
                    if uid is not None:
                        self.idTag = uid
                        idtagus.setIdTag(uid)
                        idtagus.update_a()
                        self.logger.info(f"Found card with UID: {uid}", filename="pn532_reader.py", category="PN532Reader", status="CARD_FOUND")
                        self.pn532.listen_for_passive_target()
                        
                await asyncio.sleep(0.1)
        except Exception as e:
            self.logger.error(f"Listening Error: {e}", filename="pn532_reader.py", category="PN532Reader", status="ERROR")
            self.idTag = ""

    async def restart(self):
        """PN532'yi sıfırlayıp, tekrar başlatır ve RFID okumasını yeniden başlatır."""
        self.logger.info("Restarting PN532...", filename="pn532_reader.py", category="PN532Reader", status="RESTARTING")
        self.pn532 = self.initialize_pn532()
        self.setup()
        self.pn532.listen_for_passive_target()
        self.idTag = ""
        self.logger.info("PN532 restarted and RFID reading re-enabled.", filename="pn532_reader.py", category="PN532Reader", status="RESTARTED")



