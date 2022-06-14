from constants import *
import math


class Snake:
	def __init__(self, direction, position, color, flags):
		self.color = color
		self.alive = True
		self.direction = direction
		self.position = position
		self.flags = flags
		self.body = []
		for i in range(START_SNAKE_BLOCKS_NR):
			self.body.append(Point(
				self.position.x + i * BLOCK_SIZE * round(math.sin(self.direction * math.pi / 2)),
				self.position.y + i * BLOCK_SIZE * round(math.cos(self.direction * math.pi / 2))))

	def direction_check(self, new_direction):
		if new_direction == Direction.Up and self.direction != Direction.Down:
			self.direction = Direction.Up
		if new_direction == Direction.Down and self.direction != Direction.Up:
			self.direction = Direction.Down
		if new_direction == Direction.Left and self.direction != Direction.Right:
			self.direction = Direction.Left
		if new_direction == Direction.Right and self.direction != Direction.Left:
			self.direction = Direction.Right

	def move(self):
		if self.direction == Direction.Up:
			self.position.y -= BLOCK_SIZE
		if self.direction == Direction.Down:
			self.position.y += BLOCK_SIZE
		if self.direction == Direction.Left:
			self.position.x -= BLOCK_SIZE
		if self.direction == Direction.Right:
			self.position.x += BLOCK_SIZE
		self.body.insert(0, Point(self.position.x, self.position.y))
		self.body.pop()


	def player_move(self):
		new_direction = self.direction
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP:
					new_direction = Direction.Up
				if event.key == pygame.K_DOWN:
					new_direction = Direction.Down
				if event.key == pygame.K_LEFT:
					new_direction = Direction.Left
				if event.key == pygame.K_RIGHT:
					new_direction = Direction.Right
		self.direction_check(new_direction)
		self.move()

	def random_move(self):
		if random.randrange(0, 10) == 0:
			new_direction = random.choice(list(Direction))
			self.direction_check(new_direction)
		self.move()

	def self_collision(self):
		for block in self.body[1:]:
			if self.position.x == block.x and self.position.y == block.y:
				return True
		return False

	def snake_collision(self, snake):
		if snake == self:
			if snake.self_collision():
				self.alive = False
		else:
			for block in snake.body:
				if self.position.x == block.x and self.position.y == block.y:
					self.alive = False

	def wall_collision(self):
		if self.position.x < 0 or self.position.x > WINDOW_X - BLOCK_SIZE:
			self.alive = False
		if self.position.y < 0 or self.position.y > WINDOW_Y - BLOCK_SIZE:
			self.alive = False

	def apple_collision(self, apple_position):
		self.body.insert(0, Point(self.position.x, self.position.y))
		if (apple_position.x <= self.position.x < apple_position.x + APPLE_SIZE) and\
			(apple_position.y <= self.position.y < apple_position.y + APPLE_SIZE):
			return True
		else:
			self.body.pop()
		return False
