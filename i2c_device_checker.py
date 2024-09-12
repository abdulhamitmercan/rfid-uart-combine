# i2c_device_checker.py

import asyncio
import busio
import board
from debug_logger import DebugLogger

class I2CDeviceChecker:
    def __init__(self, i2c_address, ping_interval=5, error_timeout=15, logger=None):
        self.i2c_address = i2c_address
        self.ping_interval = ping_interval
        self.error_timeout = error_timeout
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.timeoutFlg = 0
        self.logger = logger

    async def ping_pong_test(self, pn532_reader):
        """I2C cihazının aktif olup olmadığını kontrol etmek için ping-pong testi."""
        self.logger.info(f"Starting Ping-Pong test on I2C address 0x{self.i2c_address:02X}...", filename="i2c_device_checker.py", category="I2CDeviceChecker", status="STARTING")
        last_ping_time = asyncio.get_event_loop().time()
        error_start_time = None
        
        while True:
            try:
                devices = self.i2c.scan()  # Tarama yaparak bağlı cihazları bulur
                current_time = asyncio.get_event_loop().time()
                
                if self.i2c_address in devices:
                    if self.timeoutFlg != 1:
                        self.logger.info(f"I2C device found at address 0x{self.i2c_address:02X}.", filename="i2c_device_checker.py", category="I2CDeviceChecker", status="DEVICE_FOUND")
                        if error_start_time is not None:
                            self.logger.info(f"Device reconnected at address 0x{self.i2c_address:02X}. Restarting PN532...", filename="i2c_device_checker.py", category="I2CDeviceChecker", status="RECONNECTING")
                            await pn532_reader.restart()  # Restart PN532 using method from PN532Reader
                            error_start_time = None
                else:
                    if error_start_time is None:
                        error_start_time = current_time
                        self.logger.warn(f"No I2C device found at address 0x{self.i2c_address:02X}. Starting error timer.", filename="i2c_device_checker.py", category="I2CDeviceChecker", status="NO_DEVICE")
                    elif current_time - error_start_time >= self.error_timeout:
                        self.logger.error(f"Error: No I2C device found at address 0x{self.i2c_address:02X} for {self.error_timeout} seconds.", filename="i2c_device_checker.py", category="I2CDeviceChecker", status="ERROR")
                        self.logger.error("++++++++++++++++++++++++RFID YOK+++++++++++++++++++++++", filename="i2c_device_checker.py", category="I2CDeviceChecker", status="NO_RFID")
                        self.timeoutFlg = 1
                
                await asyncio.sleep(self.ping_interval)
            except Exception as e:
                self.logger.error(f"Ping-Pong Error: {e}", filename="i2c_device_checker.py", category="I2CDeviceChecker", status="ERROR")
                await asyncio.sleep(self.ping_interval)
