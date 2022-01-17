import pygame, sys, random
from pygame.locals import *

# Handle opponent movement
def ball_animation():
    global ball_speed_x, ball_speed_y, player_score, opponent_score, score_time

    # Move ball according to set ball speed 
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Allow the ball to bounce at the top and bottom of the screen 
    # Increment player or opponent score based on whether the ball leaves screen on the left or right 
    if ball.left <= 0:
        player_score += 1
        score_time = pygame.time.get_ticks()
    elif ball.right >= screen_width:
        opponent_score += 1
        score_time = pygame.time.get_ticks()
    
    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y *= -1

    # Handle the collisions between ball and paddles 
    if ball.colliderect(player) and ball_speed_x > 0:
        if abs(ball.right - player.left) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - player.top) < 10 or abs(ball.top - player.bottom) < 10:
            ball_speed_y *= -1

    if ball.colliderect(opponent) and ball_speed_x < 0:
        if abs(ball.left - opponent.right) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - opponent.top) < 10 or abs(ball.top - opponent.bottom) < 10:
            ball_speed_y *= -1

# Restarts ball at centre if it passes opponent or player. Displays a countdown before the ball is released 
def ball_start():
	global ball_speed_x, ball_speed_y, ball_moving, score_time

    # Reset ball at centre of screen. Get current time 
	ball.center = (screen_width/2, screen_height/2)
	current_time = pygame.time.get_ticks()

    # Display countdown timer
	if current_time - score_time < 700:
		number_three = game_font.render("3", False, obj_colour)
		screen.blit(number_three, (screen_width/2 - 10, screen_height/2 + 20))
	if 700 < current_time - score_time < 1400:
		number_two = game_font.render("2", False, obj_colour)
		screen.blit(number_two,(screen_width/2 - 10, screen_height/2 + 20))
	if 1400 < current_time - score_time < 2100:
		number_one = game_font.render("1", False, obj_colour)
		screen.blit(number_one,(screen_width/2 - 10, screen_height/2 + 20))

    # Ball remains stationary in the centre for 3s
	if current_time - score_time < 2100:
		ball_speed_y, ball_speed_x = 0, 0
	else:
		ball_speed_x = 7 * random.choice((1,-1))
		ball_speed_y = 7 * random.choice((1,-1))
		score_time = None
    
# Handles player movement 
def player_animation():
    player.y += player_speed

    # Restrict player to be within the screen 
    if player.top <= 0:
        player.top = 0 
    if player.bottom >= screen_height: 
        player.bottom = screen_height

# Handles opponent AI 
def opponent_ai(): 
    if opponent.top < ball.y: 
        opponent.top += opponent_speed
    if opponent.bottom > ball.y: 
        opponent.bottom -= opponent_speed 

    # Restrict opponent to be within the screen 
    if opponent.top <= 0:
        opponent.top = 0 
    if opponent.bottom >= screen_height: 
        opponent.bottom = screen_height

# General set up 
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
clock = pygame.time.Clock()

# Setting up the main window 
screen_width = 1280 
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height), RESIZABLE)
pygame.display.set_caption('Pong Pong Pong')

# Define game rectangles. Ball in the middle of the screen, player on the right middle, opponent on the left middle 
ball_radius = 30
ball = pygame.Rect(screen_width / 2 - ball_radius / 2, screen_height / 2 - ball_radius / 2, ball_radius, ball_radius)
player = pygame.Rect(screen_width - 20, screen_height / 2 - 70, 10, 140)
opponent = pygame.Rect(10, screen_height / 2 - 70, 10, 140)

# Set colour variables 
bg_colour = pygame.Color('grey12')
obj_colour = (200, 200, 200)

# Set ball and paddles speed
ball_speed_x = 7 * random.choice((-1, 1))
ball_speed_y = 7 * random.choice((-1, 1))
player_speed = 0
opponent_speed = 7 

# Text variables 
player_score = 0 
opponent_score = 0
game_font = pygame.font.Font("freesansbold.ttf", 32)

# Score Timer (set to True to trigger countdown timer at initialisation)
score_time = True

while True: 
    # Handles inputs 
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            pygame.quit()
            sys.exit()
        # Player can control movement of the board with up/down key
        if event.type == KEYDOWN:
            if event.key == pygame.K_DOWN: 
                player_speed += 7 
            if event.key == pygame.K_UP:
                player_speed -= 7 
        if event.type == KEYUP:
            if event.key == pygame.K_DOWN: 
                player_speed -= 7 
            if event.key == pygame.K_UP:
                player_speed += 7 

    ball_animation()
    player_animation()
    opponent_ai()

    # Visuals (Bottomest layer will be the first object drawn)
    screen.fill(bg_colour)
    pygame.draw.rect(screen, obj_colour, player)
    pygame.draw.rect(screen, obj_colour, opponent)
    pygame.draw.ellipse(screen, obj_colour, ball)
    pygame.draw.aaline(screen, obj_colour, (screen_width / 2, 0), (screen_width / 2, screen_height))

    # At the start of each round, trigger countdown timer
    if score_time:
        ball_start()

    # Attach player's score and opponent score to display surface 
    player_text = game_font.render(f'{player_score}', False, obj_colour)
    screen.blit(player_text, (660, 350))
    opponent_text = game_font.render(f'{opponent_score}', False, obj_colour)
    screen.blit(opponent_text, (600, 350))

    # Updating the window 
    pygame.display.flip()
    clock.tick(60)