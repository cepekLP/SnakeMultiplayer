from enum import IntEnum
import pygame
import random
import numpy as np
import struct
from array import array
import sys

FPS = 30
WINDOW_X = 800
WINDOW_Y = 600

BLOCK_SIZE = 5
APPLE_SIZE = 15
START_SNAKE_BLOCKS_NR = 20
MAX_SNAKE_LENGTH = 50
MAX_PLAYER_NUMBER = 6


class Point:
	def __init__(self, x, y):
		self.x: np.uint16 = x
		self.y: np.uint16 = y


class Direction(IntEnum):
	Up = 0
	Left = 1
	Down = 2
	Right = 3


class PlayerState:
	timestamp: int
	length: int
	direction: int
	points: int
	flags: int
	position_x: array('h')
	position_y: array('h')

	def pack(self):
		return struct.pack(self.getPackType(), self.timestamp, self.length, self.direction, self.points, self.flags, *self.position_x, *self.position_y)

	@staticmethod
	def unpack(package):
		gamedata = struct.unpack(PlayerState.getPackType(), package)
		timestamp = gamedata[0]
		length = gamedata[1]
		direction = gamedata[2]
		points = gamedata[3]
		flags = gamedata[4]

		posX = gamedata[5:55]
		posY = gamedata[55:105]
		
		result = PlayerState()
		result.timestamp = timestamp
		result.length = length
		result.direction = direction
		result.points = points
		result.flags = flags
		result.position_x = posX
		result.position_y = posY

		return result


	@staticmethod
	def getSize():
		return 212

	@staticmethod
	def getPackType():
		return 'IHHHH50h50h'

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



ACCELERATION      = 0x0001
IS_ALIVE          = 0x0002
IS_FINISHED       = 0x0004
IS_STARTED        = 0x0008
IS_GOING_TO_START = 0x000C
IS_ENDED          = 0x0010