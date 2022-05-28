from enum import Enum


class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y


class Direction(Enum):
	Up = 0
	Left = 1
	Down = 2
	Right = 3


class Snake:
	def __init__(self):
		self.position = Point(100, 50)
		self.body = [Point(100, 50), Point(90, 50), Point(80, 50), Point(70, 50)]
		self.direction = Direction.Right

	def move(self, new_direction):
		if new_direction == Direction.Up and self.direction != Direction.Down:
			self.direction = Direction.Up
		if new_direction == Direction.Down and self.direction != Direction.Up:
			self.direction = Direction.Down
		if new_direction == Direction.Left and self.direction != Direction.Right:
			self.direction = Direction.Left
		if new_direction == Direction.Right and self.direction != Direction.Left:
			self.direction = Direction.Right
