import pygame
import time
import random
from snake import *

snake_speed = 15
window_x = 720
window_y = 480

black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)


class Game:
	def __init__(self):
		pygame.init()

		self.snake = Snake()

		pygame.display.set_caption('Geeks for Geeks Snakes')
		self.game_window = pygame.display.set_mode((window_x, window_y))

		self.fps = pygame.time.Clock()

		self.fruit_position = Point(random.randrange(1, (window_x // 10)) * 10, random.randrange(1, (window_y // 10)) * 10)
		self.fruit_spawn = True
		self.score = 0

	def show_score(self, choice, color, font, size):
		score_font = pygame.font.SysFont(font, size)

		score_surface = score_font.render('Score : ' + str(self.score), True, color)

		score_rect = score_surface.get_rect()

		self.game_window.blit(score_surface, score_rect)

	def game_over(self):
		my_font = pygame.font.SysFont('times new roman', 50)

		game_over_surface = my_font.render('Your Score is : ' + str(self.score), True, red)

		game_over_rect = game_over_surface.get_rect()
		game_over_rect.midtop = (window_x / 2, window_y / 4)

		self.game_window.blit(game_over_surface, game_over_rect)
		pygame.display.flip()

		time.sleep(2)
		pygame.quit()
		quit()

	def player_move(self):
		new_direction = self.snake.direction
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
		self.snake.move(new_direction)

	def game(self):
		while True:
			self.player_move()

			if self.snake.direction == Direction.Up:
				self.snake.position.y -= 10
			if self.snake.direction == Direction.Down:
				self.snake.position.y += 10
			if self.snake.direction == Direction.Left:
				self.snake.position.x -= 10
			if self.snake.direction == Direction.Right:
				self.snake.position.x += 10

			self.snake.body.insert(0, Point(self.snake.position.x, self.snake.position.y))
			if self.snake.position.x == self.fruit_position.x and self.snake.position.y == self.fruit_position.y:
				self.score += 10
				self.fruit_spawn = False
			else:
				self.snake.body.pop()

			if not self.fruit_spawn:
				self.fruit_position = Point(random.randrange(1, (window_x // 10)) * 10, random.randrange(1, (window_y // 10)) * 10)

			self.fruit_spawn = True
			self.game_window.fill(black)

			for pos in self.snake.body:
				pygame.draw.rect(self.game_window, green, pygame.Rect(pos.x, pos.y, 10, 10))
			pygame.draw.rect(self.game_window, white, pygame.Rect(
				self.fruit_position.x, self.fruit_position.y, 10, 10))

			if self.snake.position.x < 0 or self.snake.position.x > window_x - 10:
				self.game_over()
			if self.snake.position.y < 0 or self.snake.position.y > window_y - 10:
				self.game_over()

			for block in self.snake.body[1:]:
				if self.snake.position.x == block.x and self.snake.position.y == block.y:
					self.game_over()

			self.show_score(1, white, 'times new roman', 20)
			pygame.display.update()
			self.fps.tick(snake_speed)


if __name__ == "__main__":
	game = Game()
	game.game()
