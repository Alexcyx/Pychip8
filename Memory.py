from Config import (
    MAX_MEMORY
)


class Mem:
    def __init__(self):
        self.memory = bytearray(MAX_MEMORY)

    def load_rom(self, rom_file):
        with open(rom_file, 'rb') as f:
            byte = f.read(1)
            addr = 0x200
            while byte != "":
                self.memory[addr] = byte
                addr += 1
                byte = f.read(1)
        f.close()

    def fetch_opcode(self, addr):
        return self.memory[addr] << 8 | self.memory[addr + 1]

    def store_byte(self, byte, addr):
        self.memory[addr] = byte

    def load_byte(self, addr):
        return self.memory[addr]
