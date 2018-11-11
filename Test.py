from Chip8 import Chip8

# Read rom test
r_file = 'c8games/TETRIS'
chip = Chip8(r_file)
# print str(hex(chip.mem.memory[0x03E7]))
while True:
    # inp = input("Next Instruction")
    chip.cpu.emulate_cycle()
    print str(chip.cpu)
