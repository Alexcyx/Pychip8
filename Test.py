from Chip8 import Chip8

# Read rom test
r_file = 'c8games/PONG2'
chip = Chip8(r_file)
print str(chip.mem.memory).encode('hex')
while False:
    # inp = input("Next Instruction")
    chip.cpu.emulate_cycle()
    print str(chip.cpu)
    chip.cpu.display_screen()
