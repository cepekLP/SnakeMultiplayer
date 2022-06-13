from snake import *
import struct
from SocketHandler import SocketHandler
import time


class Game:
	def __init__(self):

		self.sh = SocketHandler()
		self.sh.start()
		self.timestamp = 0

		self.player_snake = Snake(
			random.choice(list(Direction)),
			Point(
				random.randrange(5 * BLOCK_SIZE, WINDOW_X - 6 * BLOCK_SIZE, BLOCK_SIZE),
				random.randrange(5 * BLOCK_SIZE, WINDOW_Y - 6 * BLOCK_SIZE, BLOCK_SIZE)),
			SNAKE_COLOR
		)
		self.snakes = [
			Snake(
				random.choice(list(Direction)), Point(
					random.randrange(5 * BLOCK_SIZE, WINDOW_X - 6 * BLOCK_SIZE, BLOCK_SIZE),
					random.randrange(5 * BLOCK_SIZE, WINDOW_Y - 6 * BLOCK_SIZE, BLOCK_SIZE)),
				SNAKES_COLORS[0]),
			Snake(
				random.choice(list(Direction)),
				Point(
					random.randrange(5 * BLOCK_SIZE, WINDOW_X - 6 * BLOCK_SIZE, BLOCK_SIZE),
					random.randrange(5 * BLOCK_SIZE, WINDOW_Y - 6 * BLOCK_SIZE, BLOCK_SIZE)),
				SNAKES_COLORS[1])]

		pygame.display.set_caption("Snake Multiplayer")
		self.game_window = pygame.display.set_mode((WINDOW_X, WINDOW_Y))
		self.fps = pygame.time.Clock()

		self.apple_position = Point(0, 0)
		self.apple_spawned = False
		self.score = 0

	def game_over(self):
		game_over_surface = BIG_FONT.render("Final Score: " + str(self.score), True, WHITE)
		game_over_rect = game_over_surface.get_rect()
		game_over_rect.center = (WINDOW_X / 2, WINDOW_Y / 4)

		self.game_window.blit(game_over_surface, game_over_rect)
		pygame.display.flip()

		pygame.time.wait(500)
		pygame.event.clear()
		while True:
			event = pygame.event.wait()
			if event.type == pygame.QUIT:
				pygame.quit()
				break
			elif event.type == pygame.KEYDOWN:
				break
		pygame.quit()

	def show_score(self):
		score_surface = SMALL_FONT.render("Score: " + str(self.score), True, WHITE)
		score_rect = score_surface.get_rect()
		self.game_window.blit(score_surface, score_rect)

	def draw(self):
		self.game_window.fill(BLACK)

		for snake in self.snakes:
			for block in snake.body:
				pygame.draw.rect(
					self.game_window, snake.color,
					pygame.Rect(block.x, block.y, BLOCK_SIZE, BLOCK_SIZE))
		for block in self.player_snake.body:
			pygame.draw.rect(
				self.game_window, self.player_snake.color,
				pygame.Rect(block.x, block.y, BLOCK_SIZE, BLOCK_SIZE))

		pygame.draw.rect(
			self.game_window, APPLE_COLOR,
			pygame.Rect(self.apple_position.x, self.apple_position.y, APPLE_SIZE, APPLE_SIZE))

		self.show_score()
		pygame.display.update()

	def collisions(self):
		if self.player_snake.apple_collision(self.apple_position):
			self.score += 10
			self.apple_spawned = False
		for snake in self.snakes:
			if snake.apple_collision(self.apple_position):
				self.apple_spawned = False

		if not self.apple_spawned:
			self.apple_position = Point(
				random.randrange(0, WINDOW_X - APPLE_SIZE, BLOCK_SIZE),
				random.randrange(0, WINDOW_Y - APPLE_SIZE, BLOCK_SIZE))
		self.apple_spawned = True

		self.player_snake.snake_collision(self.player_snake)
		self.player_snake.wall_collision()
		for snake in self.snakes:
			self.player_snake.snake_collision(snake)
			snake.snake_collision(self.player_snake)

		for snake in self.snakes:
			for coll_snake in self.snakes:
				snake.snake_collision(coll_snake)
				snake.wall_collision()

		for snake in self.snakes:
			if not snake.alive:
				self.snakes.remove(snake)

	def move(self):
		self.player_snake.player_move()
		for snake in self.snakes:
			snake.random_move()

	def play(self):
		while True:
			self.draw()
			self.move()
			self.fps.tick(FPS)
			self.collisions()

			self.sh.sendCommand('player')
			self.sh.sendStruct(self.pack_snake())
			
			if not self.player_snake.alive:
				break
		self.game_over()
	
	def pack_snake(self):
		packed = PlayerState()
		packed.timestamp = int(round(time.time() * 1000)) % 4000000000
		packed.length = len(self.player_snake.body)
		packed.direction = self.player_snake.direction
		packed.points = self.score
		packed.flags = 0
		#x_list = [block.x for block in self.player_snake.body] + [0] * (MAX_SNAKE_LENGTH - len(self.player_snake.body))
		#y_list = [block.y for block in self.player_snake.body] + [0] * (MAX_SNAKE_LENGTH - len(self.player_snake.body))

		packed.position_x = array('H')
		packed.position_y = array('H')

		# for i in range(0, 50):
		# 	if i < len(self.player_snake.body):
		# 		packed.position_x.append(self.player_snake.body[i].x)
		# 	else:
		# 		packed.position_x.append(0)

		# for i in range(0, 50):
		# 	if i < len(self.player_snake.body):
		# 		packed.position_y.append(self.player_snake.body[i].y)
		# 	else:
		# 		packed.position_y.append(0)

		for i in range(50):
			if i < len(self.player_snake.body):
				packed.position_x.append(self.player_snake.body[i].x)
				packed.position_y.append(self.player_snake.body[i].y)
			else:
				packed.position_x.append(0)
				packed.position_y.append(0)
		
		return packed.pack()


if __name__ == "__main__":
	game = Game()
	game.play()
