from Chip8 import Chip8

# Read rom test
r_file = 'c8games/TETRIS'
chip = Chip8(r_file)
# print str(chip.mem.memory).encode('hex')
chip.cpu.emulate_cycle()

print str(chip.cpu.op_code)
