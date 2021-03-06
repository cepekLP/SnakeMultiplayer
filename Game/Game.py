from math import fabs
from snake import *
import struct
from SocketHandler import SocketHandler
import time


class Game:
	def __init__(self):

		self.sh = SocketHandler()
		#self.sh.game = self
		self.sh.start(self)
		self.timestamp = 0
		self.player_snake_created = False
		

		self.player_snake = Snake(
			random.choice(list(Direction)),
			Point(
				-10000,
				-10000),
			SNAKE_COLOR,
			IS_ALIVE
		)
		self.snakes = []
		for _ in range(MAX_PLAYER_NUMBER):
			self.snakes.append

		pygame.display.set_caption("Snake Multiplayer")
		self.game_window = pygame.display.set_mode((WINDOW_X, WINDOW_Y))
		self.fps = pygame.time.Clock()

		self.apple_position = Point(-500, -500)
		self.apple_spawned = True
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
			if(snake.flags & IS_ALIVE) == IS_ALIVE:
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
			#self.collisions()

			#  !!! temporary!!!

			#  !!! temporary!!!

			self.sh.sendCommand('player')
			self.sh.sendStruct(self.pack_snake())
			
			if not self.player_snake.alive:
				break
			self.fps.tick(FPS)
		self.game_over()
	
	def init_player(self, ps: PlayerState):
		if not self.player_snake_created:
			self.player_snake = Snake(
				ps.direction,
				Point(
					ps.position_x[0],
					ps.position_y[0]),
				SNAKE_COLOR,
				ps.flags
			)
		self.player_snake_created = True

	def pass_snake(self, psArray):
		#print(bin(psArray[0].flags))
		self.score = psArray[0].points
		self.player_snake.flags = psArray[0].flags
		self.player_snake.length = psArray[0].length
		if (psArray[0].flags & IS_ALIVE ) != IS_ALIVE:
			self.player_snake.alive = False
		self.snakes.clear()
		for snake in psArray[1:]:
			print("Snake in game", snake.position_x[0], snake.position_y[0])
			new_snake = Snake(snake.direction, Point(snake.position_x[0], snake.position_y[0]), SNAKES_COLORS[len(self.snakes)], snake.flags)
			new_snake.body = [Point(snake.position_x[i], snake.position_y[i]) for i in range(snake.length)]
			self.snakes.append(new_snake)
	
	def pass_apple(self, apple : Point):
		self.apple_position = apple
		print("Apple:", apple.x, apple.y)

	def pack_snake(self):
		packed = PlayerState()
		packed.timestamp = int(round(time.time() * 1000)) % 4000000000
		packed.length = len(self.player_snake.body)
		packed.direction = self.player_snake.direction
		packed.points = self.score
		packed.flags = self.player_snake.flags
		#x_list = [block.x for block in self.player_snake.body] + [0] * (MAX_SNAKE_LENGTH - len(self.player_snake.body))
		#y_list = [block.y for block in self.player_snake.body] + [0] * (MAX_SNAKE_LENGTH - len(self.player_snake.body))

		packed.position_x = array('h')
		packed.position_y = array('h')

		print(self.player_snake.body[0].y)
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
