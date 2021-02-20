import pygame, sys, random
from detector import *

def ball_animation():
    '''
    function makes ball move and
    handle its cikkisions with boundaries and player rectangles
    '''
    global ball_speed_x, ball_speed_y, player_score, opponent_score, score_time
    
    # Ball motion
    ball.x += ball_speed_x 
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= screen_height: # if ball touches top or bottom bounds
        ball_speed_y *= -1                            # reverse its direction
        
    
    # if ball out of table (right & left parts)
    # score is counted    
    if ball.left <= 0:
        player_score += 1
        score_time = pygame.time.get_ticks()
        
    if ball.right >= screen_width:
        opponent_score += 1
        score_time = pygame.time.get_ticks()
    
    # if ball touches rectangles (rackets) - it collides and reverses its direction
    if ball.colliderect(player) or ball.colliderect(opponent):
        ball_speed_x *= -1
        
def player_animation():
    '''
    function enables player motion on y axis and
    handles its collisions with top and bottom boundary
    '''
    player.y += player_speed 

    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height
        
def opponent_ai():
    '''
    function enables opponent motion on y axis and
    adds a logic to move on itself
    depending on position of a ball 
    '''
    if opponent.top < ball.y:
        opponent.y += opponent_speed
    if opponent.bottom > ball.y:
        opponent.y -= opponent_speed

    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height

def ball_start():
    '''
    function starts ball motion after 3 seconds the ball was lost
    the direction is random
    '''
    global ball_speed_x, ball_speed_y, score_time

    current_time = pygame.time.get_ticks() # starts timer
    ball.center = (screen_width/2, screen_height/2)
    
    # display counts 3 - 2 - 1 before start of the game
    if current_time - score_time < 700: 
        number_three = game_font.render("3", False, light_grey)
        screen.blit(number_three, (screen_width/2 -10, screen_height/2 + 20))
    
    if 700 < current_time - score_time < 1400:
        number_one = game_font.render("2", False, light_grey)
        screen.blit(number_one, (screen_width/2 -10, screen_height/2 + 20))
    
    if 1400 < current_time - score_time < 2100:
        number_two = game_font.render("1", False, light_grey)
        screen.blit(number_two, (screen_width/2 -10, screen_height/2 + 20))
    
    # start motion after 3 ticks
    if current_time - score_time < 2100:
        ball_speed_x, ball_speed_y = 0, 0
    else:
        ball_speed_y = 13 * random.choice((1,-1))
        ball_speed_x = 13 * random.choice((1,-1))
        score_time = None # remove the True value of score_time

# General setup
pygame.init()
clock = pygame.time.Clock()

# Setting up the main window
screen_width = 640 
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')

# Game Rectangles and their positions
ball = pygame.Rect(screen_width / 2 - 15, screen_height / 2 - 15, 30, 30)
player = pygame.Rect(screen_width - 20, screen_height / 2 - 70, 10, 140)
opponent = pygame.Rect(10, screen_height / 2 - 70, 10,140)

# Colors
light_grey = (230,230,230)
bg_color = pygame.Color(0, 0, 0)

# Game Variables
## speed and random direction of ball
ball_speed_x = 13 * random.choice((1,-1))
ball_speed_y = 13 * random.choice((1,-1))       
player_speed = 0
opponent_speed = 13

# Text Variables
player_score = 0
opponent_score = 0
# Font Settings
game_font = pygame.font.Font("freesansbold.ttf", 24)
pause_text = pygame.font.SysFont('Consolas', 32).render('Hand Not Found', False, (255, 255, 255))

#Score Timer
score_time = True

# get videocapture object, with game window dimensions
cap = init_cap(screen_width, screen_height)

while True:
    # detect hand and get its coordinates (center of y coordinates)
    # draws a rectangle around a palm
    hand_pos = get_pos(cap)

    if hand_pos:

        # if negative returned, close window
        if hand_pos < 0:
            pygame.quit()
            sys.exit()

        # set player position based on hand coordinates
        else:
            player.y = hand_pos - 60

    # if hand is not detected, pause the game 
    else:
        screen.blit(pause_text, (400, 300))
        continue

    #Handling input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Game logic
    ball_animation()
    player_animation()
    opponent_ai()
    
    # Visuals: backgrounfd color, drawing rectangles, and vertical line in the center
    screen.fill(bg_color)
    
    pygame.draw.rect(screen, light_grey, player)
    pygame.draw.rect(screen, light_grey, opponent)
    pygame.draw.ellipse(screen, light_grey, ball)
    pygame.draw.aaline(screen, light_grey, (screen_width / 2, 0),(screen_width / 2, screen_height))
    
    # executes only ones to start a ball in the beginning
    # executes every time ball is out
    if score_time: 
        ball_start()
        
    
    player_text = game_font.render(f"{player_score}", False, light_grey)
    screen.blit(player_text, (350, 10))
    
    opponent_text = game_font.render(f"{opponent_score}", False, light_grey)
    screen.blit(opponent_text, (280, 10))
    
    # Updating the window 
    pygame.display.flip()
    clock.tick(60)

