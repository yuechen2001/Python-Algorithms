import pygame, sys, random

class Block(pygame.sprite.Sprite):
	def __init__(self, path, x_pos, y_pos):
		super().__init__()

		# Loads image from memory and draws a rectangle around the image 
		self.image = pygame.image.load(path)
		self.rect = self.image.get_rect(center = (x_pos, y_pos))

class Player(Block):
	def __init__(self, path, x_pos, y_pos, speed):
		super().__init__(path, x_pos, y_pos)
		self.speed = speed 
		self.movement = 0

	# Stops player from leaving the screen 
	def screen_constrain(self):
		if self.rect.top <= 0:
			self.rect.top = 0
		if self.rect.bottom >= screen_height:
			self.rect.bottom = screen_height

	# Updates player movement
	def update(self, ball_group): 
		self.rect.y += self.movement 
		self.screen_constrain()

class Ball(Block):
	def __init__(self, path, x_pos, y_pos, speed_x, speed_y, paddles):
		super().__init__(path, x_pos, y_pos)
		self.speed_x = speed_x * random.choice((-1, 1))
		self.speed_y = speed_y * random.choice((-1, 1))
		self.paddles = paddles 
		self.active = False
		# Records the time when someone scores a point. Used for resetting ball 
		self.score_time = 0 

	def update(self):
		if self.active:
			self.rect.x += self.speed_x
			self.rect.y += self.speed_y
			self.collision_detection()
		else: 
			self.restart_counter()

	# Detects the collisions between ball and paddle. Determine whether to reverse velocity of ball
	def collision_detection(self):

		# Ball bounces off the ceiling and floor of the game 
		if self.rect.top <= 0 or self.rect.bottom >= screen_height:
				self.speed_y *= -1

		# Checks collisions between ball and paddle 
		# By returning a list of objects that collided with the ball (if any)
		if pygame.sprite.spritecollide(self, self.paddles, False):

				# Returns the rectangle of first object of the list 
				collision_paddle = pygame.sprite.spritecollide(self, self.paddles, False)[0].rect
				
				# Check direction of travel of ball and which side of the object did the collision occur
				if abs(self.rect.right - collision_paddle.left) < 10 and self.speed_x > 0:
					self.speed_x *= -1
				if abs(self.rect.left - collision_paddle.right) < 10 and self.speed_x < 0:
					self.speed_x *= -1
				if abs(self.rect.top - collision_paddle.bottom) < 10 and self.speed_y < 0:
					self.speed_y *= -1
				if abs(self.rect.bottom - collision_paddle.top) < 10 and self.speed_y > 0:
					self.speed_y *= -1

	# Reset ball to centre and start new round 
	def reset_ball(self):
		self.active = False 
		self.speed_x *= random.choice((-1,1))
		self.speed_y *= random.choice((-1,1))

		# Get current time 
		self.score_time = pygame.time.get_ticks()
		self.rect.center = (screen_width / 2, screen_height / 2)

	# Draw timer onto the screen, and restart timer every new round 
	def restart_counter(self): 
		current_time = pygame.time.get_ticks()
		countdown_number = 3

		# Decrease countdown_number by 1 each passing second, and set ball to active once counter reaches 0
		if current_time - self.score_time <= 700:
			countdown_number = 3
		if 700 < current_time - self.score_time <= 1400:
			countdown_number = 2
		if 1400 < current_time - self.score_time <= 2100:
			countdown_number = 1
		if current_time - self.score_time >= 2100:
			self.active = True

		# Draw and blit timer onto screen
		time_counter = basic_font.render(str(countdown_number), True, accent_colour)
		time_counter_rect = time_counter.get_rect(center = (screen_width / 2, screen_height / 2 + 50))
		pygame.draw.rect(screen, bg_colour, time_counter_rect)
		screen.blit(time_counter, time_counter_rect)

class Opponent(Block):
	def __init__(self,path,x_pos,y_pos,speed):
		super().__init__(path,x_pos,y_pos)
		self.speed = speed

	# Opponent paddle follows ball up and down 
	def update(self,ball_group):
		if self.rect.top < ball_group.sprite.rect.y:
			self.rect.y += self.speed
		if self.rect.bottom > ball_group.sprite.rect.y:
			self.rect.y -= self.speed
		self.constrain()

	def constrain(self):
		if self.rect.top <= 0: self.rect.top = 0
		if self.rect.bottom >= screen_height: self.rect.bottom = screen_height

class GameManager:
	def __init__(self, ball_group, paddle_group):
		self.player_score = 0 
		self.opponent_score = 0 
		self.ball_group = ball_group
		self.paddle_group = paddle_group

	def run_game(self):
		# Draw game objects onto the screen 
		self.paddle_group.draw(screen)
		self.ball_group.draw(screen)

		# Update game objects 
		self.paddle_group.update(self.ball_group)
		self.ball_group.update()
		self.reset_ball()
		self.draw_score()

	# Using Ball's function, reset ball to centre and start timer 
	def reset_ball(self): 
		# Check if ball passes left or right side of the screen
		if self.ball_group.sprite.rect.right >= screen_width:
			self.opponent_score += 1
			self.ball_group.sprite.reset_ball()
		if self.ball_group.sprite.rect.left <= 0:
			self.player_score += 1
			self.ball_group.sprite.reset_ball()

	# Draws the score of player and opponent onto the screen 
	def draw_score(self): 
		player_score = basic_font.render(str(self.player_score), True, accent_colour)
		opponent_score = basic_font.render(str(self.opponent_score), True, accent_colour)

		player_score_rect = player_score.get_rect(midleft = (screen_width / 2 + 40, screen_height / 2))
		opponent_score_rect = opponent_score.get_rect(midright = (screen_width / 2 - 40, screen_height / 2))

		screen.blit(player_score, player_score_rect)
		screen.blit(opponent_score, opponent_score_rect)

# General set up 
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
clock = pygame.time.Clock()

# Setting up the main window 
screen_width = 1280 
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong Pong Pong')

# Global variables 
bg_colour = pygame.Color('#2F373F')
accent_colour = (27, 35, 42)
basic_font = pygame.font.Font('freesansbold.ttf', 32)
middle_strip = pygame.Rect(screen_width / 2 - 2, 0, 4, screen_height)

# Initialise Game objects 
player = Player('D:\Python\Pygame\pong\paddle.png', screen_width - 20, screen_height / 2, 5)
opponent = Opponent('D:\Python\Pygame\pong\paddle.png', 20, screen_width / 2, 5)
paddle_group = pygame.sprite.Group()
paddle_group.add(player)
paddle_group.add(opponent)

ball = Ball('D:\Python\Pygame\pong\Ball.png', screen_width / 2, screen_height / 2, 4, 4, paddle_group)
ball_group = pygame.sprite.GroupSingle()
ball_group.add(ball)

game_manager = GameManager(ball_group, paddle_group)

while True: 
	# Handles inputs 
	for event in pygame.event.get():
		if event.type == pygame.QUIT: 
			pygame.quit()
			sys.exit()
		# Player can control movement of the board with up/down key
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_DOWN: 
				player.movement += player.speed
			if event.key == pygame.K_UP:
				player.movement -= player.speed
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_DOWN: 
				player.movement -= player.speed
			if event.key == pygame.K_UP:
				player.movement += player.speed

	# Visuals (Bottomest layer will be the first object drawn)
	screen.fill(bg_colour)
	pygame.draw.rect(screen, accent_colour, middle_strip)

	# Run the game 
	game_manager.run_game()

	# Updating the window 
	pygame.display.flip()
	clock.tick(120)