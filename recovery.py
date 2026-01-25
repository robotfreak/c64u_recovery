
from jtag_xilinx import JtagClientException, JtagClient
import time
import struct
import logging
import sys

class TestFail(Exception):
    pass

class TestFailCritical(TestFail):
    pass

# create logger
logger = logging.getLogger('Tests')
logger.setLevel(logging.INFO)

dut_fpga  = 'binaries/u64_mk2_artix.bit'
dut_appl  = 'binaries/ultimate.app'

class Ultimate64II:
    def __init__(self):
        pass

    def startup(self):
        self.dut = JtagClient()    
        self.reset_variables()

    def reset_variables(self):
        self.proto = False
        self.flashid = 0
        self.unique = 0
        self.revision = 0
        self.off = False
    
    def unique_id(self):
        """Unique ID"""
        if self.dut.xilinx_read_id() != 0x0362C093:
            print(self.dut.xilinx_read_id())
            raise TestFailCritical("FPGA on DUT not recognized")
        self.unique = self.dut.xilinx_read_dna()

    def board_revision(self):
        """Board Revision"""
        self.revision = int(self.dut.user_read_io(0x10000c, 1)[0]) >> 3
        self.dut.user_write_io(0x60208, b'\x03')
        self.dut.user_write_io(0x60200, b'\xFF')
        self.dut.user_write_io(0x60208, b'\x01')
        self.dut.user_write_io(0x60200, b'\x4B')
        self.dut.user_write_io(0x60200, b'\x00\x00\x00\x00')
        idbytes = self.dut.user_read_io(0x60200, 4)
        idbytes += self.dut.user_read_io(0x60200, 4)
        self.dut.user_write_io(0x60208, b'\x03')
        logger.info(f"FlashID = {idbytes.hex()}")
        self.flashid = struct.unpack(">Q", idbytes)[0]
        #print(self.flashid)

    def load_fpga(self):
        """FPGA Detection & Load"""
        id = self.dut.xilinx_read_id()
        if id != 0x0362C093:
            logger.error(f"IDCODE does not match: {id:08x}")
            raise TestFailCritical("FPGA on DUT not recognized")
        
        self.dut.xilinx_load_fpga(dut_fpga)

        self.dut.user_set_outputs(0x80) # Unreset

    def load_app(self):
        """Run Application on DUT"""
        self.dut.user_upload(dut_appl, 0x30000)
        self.dut.user_run_app(0x30000)
        time.sleep(0.5)
        text = self.dut.user_read_console(True)
        logger.info(f"Console Output:\n{text}")

    @staticmethod
    def add_log_handler(ch):
        global logger
        logger.addHandler(ch)

if __name__ == '__main__':
    u64ii = Ultimate64II()
    u64ii.startup()
    u64ii.unique_id()
    u64ii.board_revision()
    u64ii.load_fpga()
    u64ii.start_app()

