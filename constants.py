from enum import IntEnum
import pygame
import random

FPS = 30
WINDOW_X = 800
WINDOW_Y = 600

BLOCK_SIZE = 5
APPLE_SIZE = 15
START_SNAKE_BLOCKS_NR = 20


class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y


class Direction(IntEnum):
	Up = 0
	Left = 1
	Down = 2
	Right = 3


pygame.init()
random.seed()

SMALL_FONT = pygame.font.SysFont("times new roman", 20)
BIG_FONT = pygame.font.SysFont("times new roman", 50, bold=True)

BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)

RED = pygame.Color(255, 0, 0)
GREEN = pygame.Color(0, 255, 0)
BLUE = pygame.Color(0, 0, 255)

YELLOW = pygame.Color(255, 255, 0)
MAGENTA = pygame.Color(255, 0, 255)
CYAN = pygame.Color(0, 255, 255)

APPLE_COLOR = RED
SNAKE_COLOR = GREEN
SNAKES_COLORS = [BLUE, YELLOW, MAGENTA, CYAN]
