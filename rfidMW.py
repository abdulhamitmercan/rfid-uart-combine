# main.py

import asyncio
from rfidDriver import PN532Reader
from i2c_device_checker import I2CDeviceChecker
from debug_logger import DebugLogger
from uartProtocol import UartProtokol
from uartHal import RxTxFonk
from uartDataManager import setdataval
from uartProtocolHandler import UartHandler  # Assumed you moved UartHandler to uartHandler.py

async def main():
    try:
        # Logger configuration
        logger = DebugLogger(level=DebugLogger.LEVEL_INFO, format_type=DebugLogger.FORMAT_FILE_LINE, log_file_path='app.log')

        # Initialize components
        pn532_reader = PN532Reader(logger=logger)
        pn532_reader.setup()
        
        # idtagus = IdTag()
        i2c_address = 0x24
        i2c_checker = I2CDeviceChecker(i2c_address, ping_interval=5, error_timeout=15, logger=logger)

        rxtx_fonk = RxTxFonk()
        myUart = UartProtokol(rxtx_fonk)
        uart_handler = UartHandler(rxtx_fonk)

        # Start asynchronous tasks
        await asyncio.gather(
            rxtx_fonk.receive_message(),
            myUart.reciveHandleUartFrame(),
            uart_handler.sendHandleUartFrame(),
            pn532_reader.listen_for_cards(),
            i2c_checker.ping_pong_test(pn532_reader)
        )
    except Exception as e:
        logger.error(f"Main Error: {e}", filename="main_tasks.py", category="MAIN", status="ERROR")

if __name__ == "__main__":
    asyncio.run(main()) 