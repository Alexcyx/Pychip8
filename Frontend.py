import pygame
from pygame.locals import * # for event MOUSE variables
import time
import os
import RPi.GPIO as GPIO

#os.putenv('SDL_VIDEODRIVER', 'fbcon') # Display on piTFT
#os.putenv('SDL_FBDEV', '/dev/fb1')
os.putenv('SDL_MOUSEDRV', 'TSLIB') # Track mouse clicks on piTFT
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')

pygame.init()
pygame.mouse.set_visible(False)

WHITE = 255, 255, 255
BLACK = 0,0,0

size = width, height = 320, 240
screen = pygame.display.set_mode(size)
my_font1 = pygame.font.Font(None, 30)
my_font2 = pygame.font.Font(None, 25)
my_font3 = pygame.font.Font(None, 20)

GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

arrow_center = [110, 70]
level = 0

def GPIO22_callback(channel):
    arrow_center[1] = (arrow_center[1] + 30) % 120 + 70 

def GPIO23_callback(channel):
    arrow_center[1] = (arrow_center[1] - 50) % 120 + 70

def GPIO27_callback(channel):
    global level
    level = 1

GPIO.add_event_detect(22, GPIO.FALLING, callback=GPIO22_callback, bouncetime=300)
GPIO.add_event_detect(23, GPIO.FALLING, callback=GPIO23_callback, bouncetime=300)
GPIO.add_event_detect(27, GPIO.FALLING, callback=GPIO27_callback, bouncetime=300)

game_name = ['Game  0','Game  1','Game  2', 'Game  3','Game  4','Game  5']

while True:
    # Erase the Work space
    screen.fill(BLACK) 
    if (not GPIO.input(17)):
        break

    # Welcome screen
    if level == 0:
        text_surface = my_font1.render('Portable Pi Game Console', True, WHITE)
        rect = text_surface.get_rect(center=(160, 80))
        screen.blit(text_surface, rect)
        
        text_surface = my_font2.render('Press A to continue', True, WHITE)
        rect = text_surface.get_rect(center=(160, 160))
        screen.blit(text_surface, rect)
    elif level == 1:
        text_surface = my_font2.render('Please select the game', True, WHITE)
        rect = text_surface.get_rect(center=(160, 30))
        screen.blit(text_surface, rect)
        
        text_surface = my_font3.render(game_name[0], True, WHITE)
        rect = text_surface.get_rect(center=(160, 70))
        screen.blit(text_surface, rect)
        
        text_surface = my_font3.render(game_name[1], True, WHITE)
        rect = text_surface.get_rect(center=(160, 90))
        screen.blit(text_surface, rect)
        
        text_surface = my_font3.render(game_name[2], True, WHITE)
        rect = text_surface.get_rect(center=(160, 110))
        screen.blit(text_surface, rect)
        
        text_surface = my_font3.render(game_name[3], True, WHITE)
        rect = text_surface.get_rect(center=(160, 130))
        screen.blit(text_surface, rect)
        
        text_surface = my_font3.render(game_name[4], True, WHITE)
        rect = text_surface.get_rect(center=(160, 150))
        screen.blit(text_surface, rect)
        
        text_surface = my_font3.render(game_name[5], True, WHITE)
        rect = text_surface.get_rect(center=(160, 170))
        screen.blit(text_surface, rect)
        
        text_surface = my_font3.render('Use arrow key to select. Press A to continue', True, WHITE)
        rect = text_surface.get_rect(center=(160, 210))
        screen.blit(text_surface, rect)
        
        pygame.draw.polygon(screen, WHITE, [[arrow_center[0] - 4, arrow_center[1] - 5], [arrow_center[0] - 4, arrow_center[1] + 5],[arrow_center[0] + 5, arrow_center[1]]], 0)
    # display workspace on screen
    pygame.display.flip() 
    
GPIO.cleanup()