import pygame, sys, random, asyncio
from pygame.math import Vector2

pygame.init()

title_font = pygame.font.Font(None, 60)
score_font = pygame.font.Font(None, 40)

SNAKE = (95, 86, 231)
BACKGROUND = (250, 249, 181)
WALLS = (209, 149, 63)
BLACK = (0, 0, 0)
cell_size = 30
number_of_cells = 25

OFFSET = 75

class Food:
	def __init__(self, snake_body):
		self.position = self.generate_random_pos(snake_body)

	def draw(self):
		food_rect = pygame.Rect(OFFSET + self.position.x * cell_size, OFFSET + self.position.y * cell_size, 
			cell_size, cell_size)
		screen.blit(food_surface, food_rect)

	def generate_random_cell(self):
		x = random.randint(0, number_of_cells-1)
		y = random.randint(0, number_of_cells-1)
		return Vector2(x, y)

	def generate_random_pos(self, snake_body):
		position = self.generate_random_cell()
		while position in snake_body:
			position = self.generate_random_cell()
		return position

class Snake:
	def __init__(self):
		self.body = [Vector2(6, 9), Vector2(5,9), Vector2(4,9)]
		self.direction = Vector2(1, 0)
		self.add_segment = False
		# self.eat_sound = pygame.mixer.Sound("Sounds/eat.mp3")
		# self.wall_hit_sound = pygame.mixer.Sound("Sounds/wall.mp3")

	def draw(self):
		for segment in self.body:
			segment_rect = (OFFSET + segment.x * cell_size, OFFSET+ segment.y * cell_size, cell_size, cell_size)
			pygame.draw.rect(screen, SNAKE, segment_rect, 0, 7)

	def update(self):
		self.body.insert(0, self.body[0] + self.direction)
		if self.add_segment == True:
			self.add_segment = False
		else:
			self.body = self.body[:-1]

	def reset(self):
		self.body = [Vector2(6,9), Vector2(5,9), Vector2(4,9)]
		self.direction = Vector2(1, 0)

class Game:
	def __init__(self):
		self.snake = Snake()
		self.food = Food(self.snake.body)
		self.state = "RUNNING"
		self.score = 0
		self.grid = [[0 for _ in range(number_of_cells)] for _ in range(number_of_cells)]
		self.create_walls()

	def draw(self):
		self.food.draw()
		self.snake.draw()

	def update(self):
		if self.state == "RUNNING":
			self.snake.update()
			self.check_collision_with_food()
			self.check_collision_with_edges()
			self.check_collision_with_tail()

	def check_collision_with_food(self):
		if self.snake.body[0] == self.food.position:
			self.food.position = self.food.generate_random_pos(self.snake.body)
			self.snake.add_segment = True
			self.score += 1
			# self.snake.eat_sound.play()

	def check_collision_with_edges(self):
		if self.snake.body[0].x == number_of_cells or self.snake.body[0].x == -1:
			self.game_over()
		if self.snake.body[0].y == number_of_cells or self.snake.body[0].y == -1:
			self.game_over()

	def game_over(self):
		self.snake.reset()
		self.food.position = self.food.generate_random_pos(self.snake.body)
		self.state = "STOPPED"
		self.score = 0
		# self.snake.wall_hit_sound.play()

	def check_collision_with_tail(self):
		headless_body = self.snake.body[1:]
		if self.snake.body[0] in headless_body:
			self.game_over()


	def create_walls(self):
		# Create walls along the edges
		for i in range(number_of_cells):
			num_random_walls = 3  # Number of random walls to add
			for _ in range(num_random_walls):
				x = random.randint(1, number_of_cells - 2)  # Random x position within the border
				y = random.randint(1, number_of_cells - 2)  # Random y position within the border
				self.grid[x][y] = 1  # Set the grid cell to be a wall

	def draw(self):
		self.food.draw()
		self.snake.draw()
	
		# Draw walls
		for x in range(number_of_cells):
			for y in range(number_of_cells):
				if self.grid[x][y] == 1:
					wall_rect = pygame.Rect(OFFSET + x * cell_size, OFFSET + y * cell_size, cell_size, cell_size)
					pygame.draw.rect(screen, WALLS, wall_rect)

	def check_collision_with_edges(self):
		if self.snake.body[0].x == number_of_cells or self.snake.body[0].x == -1 or \
				self.snake.body[0].y == number_of_cells or self.snake.body[0].y == -1 or \
				self.grid[int(self.snake.body[0].x)][int(self.snake.body[0].y)] == 1:
			self.game_over()


screen = pygame.display.set_mode((2*OFFSET + cell_size*number_of_cells, 2*OFFSET + cell_size*number_of_cells))

pygame.display.set_caption("Retro Snake with Walls")

clock = pygame.time.Clock()

game = Game()
food_surface = pygame.image.load("Graphics/food.png")

SNAKE_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SNAKE_UPDATE, 200) 	

async def main():
	while True:
		for event in pygame.event.get():
			if event.type == SNAKE_UPDATE:
				game.update()
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

			if event.type == pygame.KEYDOWN:
				if game.state == "STOPPED":
					game.state = "RUNNING"
				if event.key == pygame.K_UP and game.snake.direction != Vector2(0, 1):
					game.snake.direction = Vector2(0, -1)
				if event.key == pygame.K_DOWN and game.snake.direction != Vector2(0, -1):
					game.snake.direction = Vector2(0, 1)
				if event.key == pygame.K_LEFT and game.snake.direction != Vector2(1, 0):
					game.snake.direction = Vector2(-1, 0)
				if event.key == pygame.K_RIGHT and game.snake.direction != Vector2(-1, 0):
					game.snake.direction = Vector2(1, 0)

		#Drawing
		screen.fill(BACKGROUND)
		pygame.draw.rect(screen, BLACK, 
			(OFFSET-5, OFFSET-5, cell_size*number_of_cells+10, cell_size*number_of_cells+10), 5)
		game.draw()
		title_surface = title_font.render("Retro Snake with Walls", True, BLACK)
		score_surface = score_font.render("Score: " + str(game.score), True, BLACK)
		screen.blit(title_surface, (OFFSET-5, 20))
		screen.blit(score_surface, (OFFSET-5, OFFSET + cell_size*number_of_cells +10))

		pygame.display.update()
		clock.tick(60)
		await asyncio.sleep(0)

asyncio.run(main())