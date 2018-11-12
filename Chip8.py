from CPU import CPU
from Memory import Mem
from Config import START_ADDRESS


class Chip8:
    def __init__(self, rom_file):
        self.mem = Mem()
        self.mem.load_rom(rom_file)
        self.cpu = CPU(START_ADDRESS, self.mem)

    def run(self):
        while True:
            self.cpu.emulate_cycle()

