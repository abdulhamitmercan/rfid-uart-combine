# main.py

import asyncio
from rfidDriver import PN532Reader
from i2c_device_checker import I2CDeviceChecker
from debug_logger import DebugLogger

async def main():
    try:
        # Logger configuration
        logger = DebugLogger(level=DebugLogger.LEVEL_INFO, format_type=DebugLogger.FORMAT_FILE_LINE, log_file_path='app.log')

        pn532_reader = PN532Reader(logger=logger)
        pn532_reader.setup()
        # I2C adresi genellikle 0x24'tür; bunu cihazınıza uygun olanla değiştirin
        i2c_address = 0x24
        i2c_checker = I2CDeviceChecker(i2c_address, ping_interval=5, error_timeout=15, logger=logger)

        # Asenkron görevler olarak dinleme ve ping-pong testini başlatın
        await asyncio.gather(
            pn532_reader.listen_for_cards(),
            i2c_checker.ping_pong_test(pn532_reader)
        )
    except Exception as e:
        logger.error(f"Main Error: {e}", filename="main.py", category="MAIN", status="ERROR")

if __name__ == "__main__":
    asyncio.run(main())
  