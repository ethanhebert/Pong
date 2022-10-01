import pygame, sys, random

#Physics Animations
def ball_animation():
    global ball_speed_x, ball_speed_y, player_score, opponent_score, restart
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    #make ball stay in the window
    if ball.top <= 0 or ball.bottom >= screen_height:
        collide_sound.play()
        ball_speed_y *= -1

    #ball goes out left side
    if ball.right <= -10:
        score_sound.play()
        player_score += 1
        restart = True

    #ball goes out right side
    if ball.left >= screen_width + 10:
        score_sound.play()
        opponent_score += 1
        restart = True

    #check for collisions with player
    if ball.colliderect(player) and ball_speed_x > 0:
        #if the ball hits on the left
        collide_sound.play()
        if abs(ball.right - player.left) < ball_speed*2:
            ball_speed_x *= -1
        #if the ball hits on the top
        elif abs(ball.bottom - player.top) < ball_speed*2 and ball_speed_y > 0:
            ball_speed_y *= -1
        #if the ball hits on the bottom
        elif abs(ball.top - player.bottom) < ball_speed*2 and ball_speed_y < 0:
            ball_speed_y *= -1

    #check for collisions with opponent
    if ball.colliderect(opponent) and ball_speed_x < 0:
        collide_sound.play()
        #if the ball hits on the right
        if abs(ball.left - opponent.right) < ball_speed*2:
            ball_speed_x *= -1
        #if the ball hits on the top
        elif abs(ball.bottom - opponent.top) < ball_speed*2 and ball_speed_y > 0:
            ball_speed_y *= -1
        #if the ball hits on the bottom
        elif abs(ball.top - opponent.bottom) < ball_speed*2 and ball_speed_y < 0:
            ball_speed_y *= -1

def ball_restart():
    global ball_speed_x, ball_speed_y, ball_speed, restart, begin

    ball.center = (screen_width/2, screen_height/2)
    space_text = game_font.render("Press space to begin", False, LIGHT_GREEN)
    screen.blit(space_text, (screen_width/2 - 160, screen_height - 40))

    #must click space to start the ball           
    if begin:
        ball_speed_x = ball_speed * random.choice((1, -1))
        ball_speed_y = ball_speed * random.choice((1, -1))
        restart = False
        begin = False
    else:
        ball_speed_x = 0
        ball_speed_y = 0
        
def player_animation():
    player.y += player_speed
    #keep the player in bounds
    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height

def opponent_ai():
    #raising the opponent_speed increases the difficulty
    if opponent.centery < ball.centery:
        opponent.centery += opponent_speed
    if opponent.centery > ball.centery:
        opponent.centery -= opponent_speed
    #keep the opponent in bounds
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height



#General setup
pygame.mixer.pre_init(44100, -16, 2, 256)
pygame.init()
clock = pygame.time.Clock()

#Setting up the main window
screen_width = 1200 #960
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pong")

#Game Rectangles
#pygame.Rect(xcord, ycord, xsize, ysize)
ball = pygame.Rect(screen_width/2 - 15, screen_height/2 - 15, 30, 30)
player = pygame.Rect(screen_width - 20, screen_height/2 - 70, 10, 140)
opponent = pygame.Rect(10, screen_height/2 - 70, 10, 140)

#Colors
DARK_GREEN = (61, 107, 69)
LIGHT_GREEN = (220, 255, 150)
ORANGE = (255, 218, 150)

#Physics
ball_speed = 10
ball_speed_x = ball_speed * random.choice((1, -1))
ball_speed_y = ball_speed * random.choice((1, -1))
player_speed = 0
opponent_speed = 7

#Text Variables
player_score = 0
opponent_score = 0
game_font = pygame.font.Font("freesansbold.ttf", 32)

#Restart Point Variables
restart = True
begin = False

#Sound
collide_sound = pygame.mixer.Sound("gamefiles/collide.wav")
score_sound = pygame.mixer.Sound("gamefiles/score.wav")

while True:
    #Handling input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player_speed = 7
            if event.key == pygame.K_UP:
                player_speed = -7
            if event.key == pygame.K_SPACE:
                if restart == True:
                    begin = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player_speed = 0
            if event.key == pygame.K_UP:
                player_speed = 0 


    #Physics Animations
    ball_animation()
    player_animation()
    opponent_ai()
    
    #Visuals
    #background color
    screen.fill(DARK_GREEN)

    #drawing a line: (surface, color, start, end)
    pygame.draw.aaline(screen, ORANGE, (screen_width/2, 0), (screen_width/2, screen_height))
    
    #display the text - f"{variable}" prints the variable as a string
    player_text = game_font.render(f"{player_score}", False, ORANGE)
    screen.blit(player_text, (screen_width/2 + 20, 20))
    opponent_text = game_font.render(f"{opponent_score}", False, ORANGE)
    screen.blit(opponent_text, (screen_width/2 - 35, 20))

    #ball and players
    pygame.draw.ellipse(screen, LIGHT_GREEN, ball)
    pygame.draw.rect(screen, ORANGE, player)
    pygame.draw.rect(screen, ORANGE, opponent)
    

    #if someone scored, reset ball at the middle 
    if restart:
        ball_restart()
        
    #Updating the window
    pygame.display.flip()
    #60 frames per second
    clock.tick(60)
