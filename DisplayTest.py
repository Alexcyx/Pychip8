import pygame
from pygame.locals import * # for event MOUSE variables
from Chip8 import Chip8
import time

pygame.init()
pygame.mouse.set_visible(False)

WHITE = 255, 255, 255
BLACK = 0,0,0

size = width, height = 320, 240
screen = pygame.display.set_mode(size)

r_file = 'c8games/PUZZLE'
chip = Chip8(r_file)
while True:
    # Erase the Work space
    screen.fill(BLACK) 
    # inp = input("Next Instruction")
    chip.cpu.emulate_cycle()
    for i in range(0, 2048):
        x = (i % 64) * 5
        y = (i / 64) * 5 + 40
        if chip.cpu.gfx[i] == 1:
            pygame.draw.rect(screen, WHITE, [x, y, 5, 5], 0)
    # display workspace on screen
    pygame.display.flip() 