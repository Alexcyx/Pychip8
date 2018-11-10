from CPU import CPU
from Memory import Mem


class Chip8:
    def __init__(self, rom_file):
        self.mem = Mem()
        self.mem.load_rom(rom_file)
        self.cpu = CPU(0x200, self.mem)
