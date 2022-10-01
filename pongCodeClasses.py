import pygame, sys, random


class Pong():
    def __init__(self):
        #sets up pygame
        pygame.mixer.pre_init(44100, -16, 2, 256)
        pygame.init()
        self.clock = pygame.time.Clock()

        #Setting up the main window
        self.screen_width = 1200
        self.screen_height = 720
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Pong")

        #Game Rectangles
        #pygame.Rect(xcord, ycord, xsize, ysize)
        self.ball = pygame.Rect(self.screen_width/2 - 15, self.screen_height/2 - 15, 30, 30)
        self.player = pygame.Rect(self.screen_width - 20, self.screen_height/2 - 70, 10, 140)
        self.opponent = pygame.Rect(10, self.screen_height/2 - 70, 10, 140)

        #Colors
        self.dark_green = (61, 107, 69)
        self.light_green = (220, 255, 150)
        self.orange = (255, 218, 150)

        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.gray = (100, 100, 100)

        self.purple = (179, 48, 255)
        self.pink = (254, 179, 255)
        self.turq = (48, 248, 255)

        self.red = (255, 0, 0)
        self.blue = (0, 0, 255)

        self.brown = (56, 40, 24)
        self.yellow = (255, 250, 110)
        self.burnt_orange = (255, 84, 46)

        self.color_max = 255
        self.color_min = 0
        self.r = self.color_max
        self.g = self.color_min
        self.b = self.color_max
        self.r_inc = 5
        self.g_inc = 5
        self.b_inc = 5

        #Physics
        self.ball_speed = 10
        self.ball_speed_x = self.ball_speed * random.choice((1, -1))
        self.ball_speed_y = self.ball_speed * random.choice((1, -1))
        self.player_speed = 0
        self.opponent_speed = 10
        #these two control how fast the players can move
        self.player_movement = 6
        self.opponent_movement = 6

        #Text Variables
        self.player_score = 0
        self.opponent_score = 0
        self.max_score = 11
        self.game_font = pygame.font.Font("freesansbold.ttf", 32)
        self.title_font = pygame.font.Font("freesansbold.ttf", 350)
        self.endgame_font = pygame.font.Font("freesansbold.ttf", 200)

        #Restart Point Variables
        self.restart = True
        self.begin = False

        #Sound
        self.collide_sound = pygame.mixer.Sound("gamefiles/collide.wav")
        self.score_sound = pygame.mixer.Sound("gamefiles/score.wav")

    def rgb_fade(self):
        if self.r == self.color_max and self.g < self.color_max and self.b == self.color_min:
            self.g += self.g_inc
        elif self.r > self.color_min and self.g == self.color_max and self.b == self.color_min:
            self.r -= self.r_inc
        elif self.r == self.color_min and self.g == self.color_max and self.b < self.color_max:
            self.b += self.b_inc
        elif self.r == self.color_min and self.g > self.color_min and self.b == self.color_max:
            self.g -= self.g_inc
        elif self.r < self.color_max and self.g == self.color_min and self.b == self.color_max:
            self.r += self.r_inc
        elif self.r == self.color_max and self.g == self.color_min and self.b > self.color_min:
            self.b -= self.b_inc
     
    def color_scheme(self):
        global color_mode
        if color_mode == 1:
            self.bg_color = self.dark_green
            self.ball_color = self.light_green
            self.accent_color = self.orange
        elif color_mode == 2:
            self.bg_color = self.black
            self.ball_color = self.white
            self.accent_color = self.gray
        elif color_mode == 3:
            self.bg_color = self.purple
            self.ball_color = self.pink
            self.accent_color = self.turq
        elif color_mode == 4:
            self.bg_color = self.white
            self.ball_color = self.red
            self.accent_color = self.blue
        elif color_mode == 5:
            self.bg_color = self.brown
            self.ball_color = self.yellow
            self.accent_color = self.burnt_orange
        elif color_mode == 6: 
            self.rgb_fade()
            self.accent_color = (self.r, self.g, self.b)
            self.bg_color = (self.r/5, self.g/5, self.b/5)
            self.ball_color = (abs(self.r - 255), abs(self.g - 255), abs(self.b - 255))
   

class Menu(Pong):
    def __init__(self):
        Pong.__init__(self)
        self.menu_looping = 1
        self.menu_loop()

    def menu_loop(self):
        current_box = 1
        title_x = self.screen_width/2
        title_y = self.screen_height/2
        title_speed_x = 3
        title_speed_y = 3
        global color_mode

        while self.menu_looping:
            #Handling input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.collide_sound.play()
                        if current_box > 1:
                            current_box -= 1
                        elif current_box == 1:
                            current_box = 4
                    if event.key == pygame.K_RIGHT:
                        self.collide_sound.play()
                        if current_box < 4:
                            current_box += 1
                        elif current_box == 4:
                            current_box = 1
                    
                    if event.key == pygame.K_RETURN:
                        self.score_sound.play()
                        global gamemode
                        if current_box == 1:
                            gamemode = 1
                            self.menu_looping = 0
                        elif current_box == 2:
                            gamemode = 2
                            self.menu_looping = 0
                        elif current_box == 3:
                            gamemode = 3
                            self.menu_looping = 0
                        elif current_box == 4:
                            color_mode += 1
                            if color_mode == 7:
                                color_mode = 1
                        
            self.color_scheme()

            #draw the screen
            self.screen.fill(self.bg_color)

            title_text = self.title_font.render("PONG", False, self.accent_color)
            self.screen.blit(title_text, title_text.get_rect(center = (title_x - 8, title_y - 100)))
            title_text = self.title_font.render("PONG", False, self.ball_color)
            self.screen.blit(title_text, title_text.get_rect(center = (title_x + 8, title_y - 100)))

            if title_x <= 510:
                title_speed_x *= -1
            elif title_x >= self.screen_width - 510:
                title_speed_x *= -1

            if title_y <= 250:
                title_speed_y *= -1
            elif title_y >= self.screen_height - 10:
                title_speed_y *= -1

            title_x += title_speed_x
            title_y += title_speed_y

            box1 = pygame.Rect(80, self.screen_height*8/10, 200, 100)
            pygame.draw.rect(self.screen, self.accent_color, box1)

            box2 = pygame.Rect(80 + 280, self.screen_height*8/10, 200, 100)
            pygame.draw.rect(self.screen, self.accent_color, box2)

            box3 = pygame.Rect(80 + 280*2, self.screen_height*8/10, 200, 100)
            pygame.draw.rect(self.screen, self.accent_color, box3)

            box4 = pygame.Rect(80 + 280*3, self.screen_height*8/10, 200, 100)
            pygame.draw.rect(self.screen, self.accent_color, box4)

            #moving between boxes on the menu
            if current_box == 1:
                box1 = pygame.Rect(80, self.screen_height*8/10, 200, 100)
                pygame.draw.rect(self.screen, self.ball_color, box1)
            elif current_box == 2:
                box2 = pygame.Rect(80 + 280, self.screen_height*8/10, 200, 100)
                pygame.draw.rect(self.screen, self.ball_color, box2)
            elif current_box == 3:
                box3 = pygame.Rect(80 + 280*2, self.screen_height*8/10, 200, 100)
                pygame.draw.rect(self.screen, self.ball_color, box3)
            elif current_box == 4:
                box4 = pygame.Rect(80 + 280*3, self.screen_height*8/10, 200, 100)
                pygame.draw.rect(self.screen, self.ball_color, box4)

            box1_text = self.game_font.render("1-PLAYER", False, self.bg_color)
            self.screen.blit(box1_text, box1_text.get_rect(center = box1.center))

            box2_text = self.game_font.render("2-PLAYER", False, self.bg_color)
            self.screen.blit(box2_text, box2_text.get_rect(center = box2.center))

            box3_text = self.game_font.render("INFINITE", False, self.bg_color)
            self.screen.blit(box3_text, box3_text.get_rect(center = box3.center))

            box4_text = self.game_font.render("COLOR", False, self.bg_color)
            self.screen.blit(box4_text, box4_text.get_rect(center = box4.center))

            #Updating the window
            pygame.display.flip()
            #60 frames per second
            self.clock.tick(60)


class OnePlayer(Pong):
    def __init__(self):
        Pong.__init__(self)
        self.one_player_looping = 1
        self.one_player_loop()

    #Physics Animations
    def ball_animation(self):
        self.ball.x += self.ball_speed_x
        self.ball.y += self.ball_speed_y

        #make ball stay in the window
        if self.ball.top <= 0 or self.ball.bottom >= self.screen_height:
            self.collide_sound.play()
            self.ball_speed_y *= -1

        #ball goes out left side
        if self.ball.right <= -10:
            self.score_sound.play()
            self.player_score += 1
            self.restart = True

        #ball goes out right side
        if self.ball.left >= self.screen_width + 10:
            self.score_sound.play()
            self.opponent_score += 1
            self.restart = True

        #check for collisions with player
        if self.ball.colliderect(self.player) and self.ball_speed_x > 0:
            #if the ball hits on the left
            self.collide_sound.play()
            if abs(self.ball.right - self.player.left) < self.ball_speed*2:
                self.ball_speed_x *= -1
                #moving down adds curve to the ball
                if self.player_speed > 0:
                    self.ball_speed_y += 5
                #moving up adds curve to the ball
                elif self.player_speed < 0:
                    self.ball_speed_y -= 5

            #if the ball hits on the top
            elif abs(self.ball.bottom - self.player.top) < self.ball_speed*2 and self.ball_speed_y > 0:
                self.ball_speed_y *= -1
            #if the ball hits on the bottom
            elif abs(self.ball.top - self.player.bottom) < self.ball_speed*2 and self.ball_speed_y < 0:
                self.ball_speed_y *= -1

        #check for collisions with opponent
        if self.ball.colliderect(self.opponent) and self.ball_speed_x < 0:
            self.collide_sound.play()
            #if the ball hits on the right
            if abs(self.ball.left - self.opponent.right) < self.ball_speed*2:
                self.ball_speed_x *= -1
                #moving down adds curve to the ball
                if self.opponent_speed > 0:
                    self.ball_speed_y += 2
                #moving up adds curve to the ball
                elif self.opponent_speed < 0:
                    self.ball_speed_y -= 2
            #if the ball hits on the top
            elif abs(self.ball.bottom - self.opponent.top) < self.ball_speed*2 and self.ball_speed_y > 0:
                self.ball_speed_y *= -1
            #if the ball hits on the bottom
            elif abs(self.ball.top - self.opponent.bottom) < self.ball_speed*2 and self.ball_speed_y < 0:
                self.ball_speed_y *= -1

    def ball_restart(self):

        self.ball.right = self.player.left
        self.ball.centery = self.player.centery

        if self.player_score != self.max_score and self.opponent_score != self.max_score:
            self.opponent.centery = self.screen_height/2

        if self.player_score == self.max_score or self.opponent_score == self.max_score:
            space_text = self.game_font.render("Press enter to restart", False, self.ball_color)
            self.screen.blit(space_text, space_text.get_rect(center = (self.screen_width/2, self.screen_height - 30)))
        else:
            space_text = self.game_font.render("Press space to serve", False, self.ball_color)
            self.screen.blit(space_text, space_text.get_rect(center = (self.screen_width/2, self.screen_height - 30)))

        #must click space to start the ball           
        if self.begin:
            self.collide_sound.play()
            self.ball_speed_x = self.ball_speed * -1
            if self.player_speed == 0:
                self.ball_speed_y = self.player_speed
            else:
                self.ball_speed_y = self.player_speed + 1
            self.restart = False
            self.begin = False
        else:
            self.ball_speed_x = 0
            self.ball_speed_y = 0

            
    def player_animation(self):
        self.player.y += self.player_speed
        #keep the player in bounds
        if self.player.top <= 0:
            self.player.top = 0
        if self.player.bottom >= self.screen_height:
            self.player.bottom = self.screen_height

    def opponent_ai(self):
        if self.ball_speed_y == 0:
            self.opponent_speed = 5
        elif abs(self.ball_speed_y) < 10:
            self.opponent_speed = abs(self.ball_speed_y)
        else:
            self.opponent_speed = abs(self.ball_speed_y*4/5)
        #raising the opponent_speed increases the difficulty
        if self.opponent.centery < self.ball.centery:
            self.opponent.centery += self.opponent_speed
        if self.opponent.centery > self.ball.centery:
            self.opponent.centery -= self.opponent_speed
        #keep the opponent in bounds
        if self.opponent.top <= 0:
            self.opponent.top = 0
        if self.opponent.bottom >= self.screen_height:
            self.opponent.bottom = self.screen_height

    def new_game(self):
        self.player_score = 0
        self.opponent_score = 0
        self.player.centery = self.screen_height/2
        self.opponent.centery = self.screen_height/2

    def end_game(self):
        if self.player_score == self.max_score:
            title_text = self.endgame_font.render("YOU WIN", False, self.accent_color)
            self.screen.blit(title_text, title_text.get_rect(center = (self.screen_width/2 - 8, self.screen_height/2)))
            title_text = self.endgame_font.render("YOU WIN", False, self.ball_color)
            self.screen.blit(title_text, title_text.get_rect(center = (self.screen_width/2 + 8, self.screen_height/2)))
        elif self.opponent_score == self.max_score:
            title_text = self.endgame_font.render("YOU LOSE", False, self.accent_color)
            self.screen.blit(title_text, title_text.get_rect(center = (self.screen_width/2 - 8, self.screen_height/2)))
            title_text = self.endgame_font.render("YOU LOSE", False, self.ball_color)
            self.screen.blit(title_text, title_text.get_rect(center = (self.screen_width/2 + 8, self.screen_height/2)))

    def one_player_loop(self):
        while self.one_player_looping:
            #Handling input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.player_speed = self.player_movement
                    if event.key == pygame.K_UP:
                        self.player_speed = -self.player_movement
                    if event.key == pygame.K_SPACE:
                        if self.restart == True:
                            if self.player_score == self.max_score or self.opponent_score == self.max_score:
                                pass
                            else:
                                self.begin = True
                    if event.key == pygame.K_RETURN:
                        if self.restart == True:
                            if self.player_score == self.max_score or self.opponent_score == self.max_score:
                                self.new_game()
                    if event.key == pygame.K_ESCAPE:
                        global gamemode
                        gamemode = 0
                        self.one_player_looping = 0
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN:
                        self.player_speed = 0
                    if event.key == pygame.K_UP:
                        self.player_speed = 0 

            self.color_scheme()

            #Physics Animations
            self.ball_animation()
            self.player_animation()
            self.opponent_ai()
            
            #Visuals
            #background color
            self.screen.fill(self.bg_color)

            #drawing a line: (surface, color, start, end)
            pygame.draw.aaline(self.screen, self.accent_color, (self.screen_width/2, 0), (self.screen_width/2, self.screen_height))
            
            #display the text - f"{variable}" prints the variable as a string
            player_text = self.game_font.render(f"{self.player_score}", False, self.accent_color)
            self.screen.blit(player_text, player_text.get_rect(center = (self.screen_width/2 + 30, 35)))
            opponent_text = self.game_font.render(f"{self.opponent_score}", False, self.accent_color)
            self.screen.blit(opponent_text, opponent_text.get_rect(center = (self.screen_width/2 - 27, 35)))

            #ball and players
            if self.player_score != self.max_score and self.opponent_score != self.max_score:
                pygame.draw.ellipse(self.screen, self.ball_color, self.ball)
            pygame.draw.rect(self.screen, self.accent_color, self.player)
            pygame.draw.rect(self.screen, self.accent_color, self.opponent)

            #if game's over, show who won or lost
            if self.player_score == self.max_score or self.opponent_score == self.max_score:
                self.end_game()

            #if someone scored, reset ball at the middle 
            if self.restart:
                self.ball_restart()
                
            #Updating the window
            pygame.display.flip()
            #60 frames per second
            self.clock.tick(60)


class TwoPlayer(Pong):
    def __init__(self):
        Pong.__init__(self)
        self.two_player_looping = 1
        self.opponent_speed = 0
        self.previous_point = 1
        self.two_player_loop()

    #Physics Animations
    def ball_animation(self):
        self.ball.x += self.ball_speed_x
        self.ball.y += self.ball_speed_y

        #make ball stay in the window
        if self.ball.top <= 0 or self.ball.bottom >= self.screen_height:
            self.collide_sound.play()
            self.ball_speed_y *= -1

        #ball goes out left side
        if self.ball.right <= -10:
            self.score_sound.play()
            self.player_score += 1
            self.previous_point = 1
            self.restart = True

        #ball goes out right side
        if self.ball.left >= self.screen_width + 10:
            self.score_sound.play()
            self.opponent_score += 1
            self.previous_point = 2
            self.restart = True

        #check for collisions with player
        if self.ball.colliderect(self.player) and self.ball_speed_x > 0:
            #if the ball hits on the left
            self.collide_sound.play()
            if abs(self.ball.right - self.player.left) < self.ball_speed*2:
                self.ball_speed_x *= -1
                #moving down adds curve to the ball
                if self.player_speed > 0:
                    self.ball_speed_y += 3
                #moving up adds curve to the ball
                elif self.player_speed < 0:
                    self.ball_speed_y -= 3

            #if the ball hits on the top
            elif abs(self.ball.bottom - self.player.top) < self.ball_speed*2 and self.ball_speed_y > 0:
                self.ball_speed_y *= -1
            #if the ball hits on the bottom
            elif abs(self.ball.top - self.player.bottom) < self.ball_speed*2 and self.ball_speed_y < 0:
                self.ball_speed_y *= -1

        #check for collisions with opponent
        if self.ball.colliderect(self.opponent) and self.ball_speed_x < 0:
            self.collide_sound.play()
            #if the ball hits on the right
            if abs(self.ball.left - self.opponent.right) < self.ball_speed*2:
                self.ball_speed_x *= -1
                #moving down adds curve to the ball
                if self.opponent_speed > 0:
                    self.ball_speed_y += 3
                #moving up adds curve to the ball
                elif self.opponent_speed < 0:
                    self.ball_speed_y -= 3
            #if the ball hits on the top
            elif abs(self.ball.bottom - self.opponent.top) < self.ball_speed*2 and self.ball_speed_y > 0:
                self.ball_speed_y *= -1
            #if the ball hits on the bottom
            elif abs(self.ball.top - self.opponent.bottom) < self.ball_speed*2 and self.ball_speed_y < 0:
                self.ball_speed_y *= -1

    def ball_restart(self):

        if self.previous_point == 1:
            self.ball.right = self.player.left
            self.ball.centery = self.player.centery
        elif self.previous_point == 2:
            self.ball.left = self.opponent.right
            self.ball.centery = self.opponent.centery

        if self.player_score == self.max_score or self.opponent_score == self.max_score:
            space_text = self.game_font.render("Press enter to restart", False, self.ball_color)
            self.screen.blit(space_text, space_text.get_rect(center = (self.screen_width/2, self.screen_height - 30)))
        else:
            if self.previous_point == 1:
                space_text = self.game_font.render("P1: Press space to serve", False, self.ball_color)
                self.screen.blit(space_text, space_text.get_rect(center = (self.screen_width/2, self.screen_height - 30)))
            elif self.previous_point == 2:
                space_text = self.game_font.render("P2: Press shift to serve", False, self.ball_color)
                self.screen.blit(space_text, space_text.get_rect(center = (self.screen_width/2, self.screen_height - 30)))


        #must click space to start the ball           
        if self.begin:
            self.collide_sound.play()
            #whoever won the previous point serves
            if self.previous_point == 1:
                self.ball_speed_x = self.ball_speed * -1
                if self.player_speed == 0:
                    self.ball_speed_y = self.player_speed
                else:
                    self.ball_speed_y = self.player_speed + 1
            elif self.previous_point == 2:
                self.ball_speed_x = self.ball_speed 
                if self.opponent_speed == 0:
                    self.ball_speed_y = self.opponent_speed
                else:
                    self.ball_speed_y = self.opponent_speed + 1
            self.restart = False
            self.begin = False
        else:
            self.ball_speed_x = 0
            self.ball_speed_y = 0
            
    def player_animation(self):
        self.player.y += self.player_speed
        #keep the player in bounds
        if self.player.top <= 0:
            self.player.top = 0
        if self.player.bottom >= self.screen_height:
            self.player.bottom = self.screen_height

    def opponent_animation(self):
        self.opponent.y += self.opponent_speed
        #keep the opponent in bounds
        if self.opponent.top <= 0:
            self.opponent.top = 0
        if self.opponent.bottom >= self.screen_height:
            self.opponent.bottom = self.screen_height

    def new_game(self):
        self.player_score = 0
        self.opponent_score = 0
        self.opponent.centery = self.screen_height/2
        self.player.centery = self.screen_height/2

    def end_game(self):
        if self.player_score == self.max_score:
            title_text = self.endgame_font.render("P1 WINS", False, self.accent_color)
            self.screen.blit(title_text, title_text.get_rect(center = (self.screen_width/2 - 8, self.screen_height/2)))
            title_text = self.endgame_font.render("P1 WINS", False, self.ball_color)
            self.screen.blit(title_text, title_text.get_rect(center = (self.screen_width/2 + 8, self.screen_height/2)))
        elif self.opponent_score == self.max_score:
            title_text = self.endgame_font.render("P2 WINS", False, self.accent_color)
            self.screen.blit(title_text, title_text.get_rect(center = (self.screen_width/2 - 8, self.screen_height/2)))
            title_text = self.endgame_font.render("P2 WINS", False, self.ball_color)
            self.screen.blit(title_text, title_text.get_rect(center = (self.screen_width/2 + 8, self.screen_height/2)))

    def two_player_loop(self):
        while self.two_player_looping:
            #Handling input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.player_speed = self.player_movement
                    if event.key == pygame.K_UP:
                        self.player_speed = -self.player_movement
                    if event.key == pygame.K_s:
                        self.opponent_speed = self.opponent_movement
                    if event.key == pygame.K_w:
                        self.opponent_speed = -self.opponent_movement
                    if event.key == pygame.K_SPACE:
                        if self.previous_point == 1:
                            if self.restart == True:
                                if self.player_score == self.max_score or self.opponent_score == self.max_score:
                                    pass
                                else:
                                    self.begin = True
                    if event.key == pygame.K_LSHIFT:
                        if self.previous_point == 2:
                            if self.restart == True:
                                if self.player_score == self.max_score or self.opponent_score == self.max_score:
                                    pass
                                else:
                                    self.begin = True
                    if event.key == pygame.K_RETURN:
                        if self.restart == True:
                            if self.player_score == self.max_score or self.opponent_score == self.max_score:
                                self.new_game()
                    if event.key == pygame.K_ESCAPE:
                        global gamemode
                        gamemode = 0
                        self.two_player_looping = 0
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN:
                        self.player_speed = 0
                    if event.key == pygame.K_UP:
                        self.player_speed = 0 
                    if event.key == pygame.K_s:
                        self.opponent_speed = 0
                    if event.key == pygame.K_w:
                        self.opponent_speed = 0

            self.color_scheme()

            #Physics Animations
            self.ball_animation()
            self.player_animation()
            self.opponent_animation()
            
            #Visuals
            #background color
            self.screen.fill(self.bg_color)

            #drawing a line: (surface, color, start, end)
            pygame.draw.aaline(self.screen, self.accent_color, (self.screen_width/2, 0), (self.screen_width/2, self.screen_height))
            
            #display the text - f"{variable}" prints the variable as a string
            player_text = self.game_font.render(f"{self.player_score}", False, self.accent_color)
            self.screen.blit(player_text, player_text.get_rect(center = (self.screen_width/2 + 30, 35)))
            opponent_text = self.game_font.render(f"{self.opponent_score}", False, self.accent_color)
            self.screen.blit(opponent_text, opponent_text.get_rect(center = (self.screen_width/2 - 27, 35)))

            #ball and players
            if self.player_score != self.max_score and self.opponent_score != self.max_score:
                pygame.draw.ellipse(self.screen, self.ball_color, self.ball)
            pygame.draw.rect(self.screen, self.accent_color, self.player)
            pygame.draw.rect(self.screen, self.accent_color, self.opponent)

            #if game's over, show who won or lost
            if self.player_score == self.max_score or self.opponent_score == self.max_score:
                self.end_game()

            #if someone scored, reset ball at the middle 
            if self.restart:
                self.ball_restart()
                
            #Updating the window
            pygame.display.flip()
            #60 frames per second
            self.clock.tick(60)


class Infinite(Pong):
    def __init__(self):
        Pong.__init__(self)
        self.infinite_looping = 1
        self.game_over = 0
        self.beating_highscore = 0
        self.increase_speed = 0
        self.infinite_loop()
    
    def ball_animation(self):
        #gets faster every 3 hits
        if self.player_score % 3 == 2:
            self.increase_speed = 1
        if self.player_score != 0 and self.player_score % 3 == 0 and self.increase_speed == 1:
            if self.ball_speed_x > 0:
                self.ball_speed_x += 1
            elif self.ball_speed_x < 0:
                self.ball_speed_x -= 1
            if self.ball_speed_y > 0:
                self.ball_speed_y += 1
            elif self.ball_speed_y < 0:
                self.ball_speed_y -= 1
            self.player_movement += 1
            self.ball_speed += 1
            self.increase_speed = 0
        
        self.ball.x += self.ball_speed_x
        self.ball.y += self.ball_speed_y

        #make ball stay in the window
        if self.ball.top <= 0 or self.ball.bottom >= self.screen_height:
            self.collide_sound.play()
            self.ball_speed_y *= -1

        #ball goes out right side
        if self.ball.left >= self.screen_width + 10:
            self.score_sound.play()
            self.game_over = 1
            self.restart = True

        #check for collisions with player
        if self.ball.colliderect(self.player) and self.ball_speed_x > 0:
            self.collide_sound.play()
            #if the ball hits on the left
            if abs(self.ball.right - self.player.left) < self.ball_speed*5:
                self.player_score += 1
                self.ball_speed_x *= -1
            #if the ball hits on the top
            elif abs(self.ball.bottom - self.player.top) < self.ball_speed*2 and self.ball_speed_y > 0:
                self.ball_speed_y *= -1
            #if the ball hits on the bottom
            elif abs(self.ball.top - self.player.bottom) < self.ball_speed*2 and self.ball_speed_y < 0:
                self.ball_speed_y *= -1

        #check for collisions with opponent
        if self.ball.left <= self.opponent.right and self.ball_speed_x < 0:
            self.collide_sound.play()
            self.ball_speed_x *= -1

    def ball_restart(self):
        self.ball.centerx = self.screen_width/2
        self.ball.centery = self.screen_height/2

        if self.player_score != self.max_score and self.opponent_score != self.max_score:
            self.opponent.centery = self.screen_height/2

        if self.game_over == 1:
            space_text = self.game_font.render("Press enter to restart", False, self.ball_color)
            self.screen.blit(space_text, space_text.get_rect(center = (self.screen_width/2, self.screen_height - 30)))
        else:
            space_text = self.game_font.render("Press space to start", False, self.ball_color)
            self.screen.blit(space_text, space_text.get_rect(center = (self.screen_width/2, self.screen_height - 30)))

        #must click space to start the ball           
        if self.begin:
            self.collide_sound.play()
            self.ball_speed_x = self.ball_speed * -1
            self.ball_speed_y = 3 * random.choice([-1, 1])
            self.restart = False
            self.begin = False
        else:
            self.ball_speed_x = 0
            self.ball_speed_y = 0
           
    def player_animation(self):
        self.player.y += self.player_speed
        #keep the player in bounds
        if self.player.top <= 0:
            self.player.top = 0
        if self.player.bottom >= self.screen_height:
            self.player.bottom = self.screen_height

    def opponent_ai(self):
        self.opponent_speed = abs(self.ball_speed_y)
        #raising the opponent_speed increases the difficulty
        if self.opponent.centery < self.ball.centery:
            self.opponent.centery += self.opponent_speed
        if self.opponent.centery > self.ball.centery:
            self.opponent.centery -= self.opponent_speed
        #keep the opponent in bounds
        if self.opponent.top <= 0:
            self.opponent.top = 0
        if self.opponent.bottom >= self.screen_height:
            self.opponent.bottom = self.screen_height

    def new_game(self):
        global infinite_highscore
        global previous_highscore
        if infinite_highscore > previous_highscore:
            previous_highscore = infinite_highscore
        self.ball_speed = 10
        self.player_movement = 6
        self.beating_highscore = 0
        self.game_over = 0
        self.player_score = 0
        self.player.centery = self.screen_height/2
        self.opponent.centery = self.screen_height/2

    def end_game(self):
        global infinite_highscore
        global previous_highscore
        #display the text
        if infinite_highscore > previous_highscore:
            title_text = self.endgame_font.render("HIGH", False, self.accent_color)
            self.screen.blit(title_text, title_text.get_rect(center = (self.screen_width/2 - 8, self.screen_height/2 - 80)))
            title_text = self.endgame_font.render("HIGH", False, self.ball_color)
            self.screen.blit(title_text, title_text.get_rect(center = (self.screen_width/2 + 8, self.screen_height/2 - 80)))
            title_text = self.endgame_font.render("SCORE", False, self.accent_color)
            self.screen.blit(title_text, title_text.get_rect(center = (self.screen_width/2 - 8, self.screen_height/2 + 80)))
            title_text = self.endgame_font.render("SCORE", False, self.ball_color)
            self.screen.blit(title_text, title_text.get_rect(center = (self.screen_width/2 + 8, self.screen_height/2 + 80)))
        else:
            title_text = self.endgame_font.render("GAME", False, self.accent_color)
            self.screen.blit(title_text, title_text.get_rect(center = (self.screen_width/2 - 8, self.screen_height/2 - 80)))
            title_text = self.endgame_font.render("GAME", False, self.ball_color)
            self.screen.blit(title_text, title_text.get_rect(center = (self.screen_width/2 + 8, self.screen_height/2 - 80)))
            title_text = self.endgame_font.render("OVER", False, self.accent_color)
            self.screen.blit(title_text, title_text.get_rect(center = (self.screen_width/2 - 8, self.screen_height/2 + 80)))
            title_text = self.endgame_font.render("OVER", False, self.ball_color)
            self.screen.blit(title_text, title_text.get_rect(center = (self.screen_width/2 + 8, self.screen_height/2 + 80)))

    def infinite_loop(self):
        global infinite_highscore
        while self.infinite_looping:
            #Handling input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.player_speed = self.player_movement
                    if event.key == pygame.K_UP:
                        self.player_speed = -self.player_movement
                    if event.key == pygame.K_SPACE:
                        if self.restart == True:
                            if self.game_over == 0:
                                self.begin = True
                    if event.key == pygame.K_RETURN:
                        if self.restart == True:
                            if self.game_over == 1:
                                self.new_game()
                    if event.key == pygame.K_ESCAPE:
                        global gamemode
                        gamemode = 0
                        self.infinite_looping = 0
                        self.new_game()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN:
                        self.player_speed = 0
                    if event.key == pygame.K_UP:
                        self.player_speed = 0 

            self.color_scheme()

            #Physics Animations
            self.ball_animation()
            self.player_animation()
            self.opponent_ai()
            
            #Visuals
            #background color
            self.screen.fill(self.bg_color)

            #drawing a line: (surface, color, start, end)
            pygame.draw.aaline(self.screen, self.accent_color, (self.screen_width/2, 0), (self.screen_width/2, self.screen_height))
            
            #display the text - f"{variable}" prints the variable as a string
            if self.player_score > infinite_highscore:
                self.beating_highscore = 1
                infinite_highscore = self.player_score
            if self.beating_highscore:
                player_text = self.game_font.render(f"SCORE: {self.player_score}", False, self.accent_color)
                self.screen.blit(player_text, player_text.get_rect(center = (self.screen_width/4, 35)))
                opponent_text = self.game_font.render(f"HIGH SCORE: {infinite_highscore}", False, self.ball_color)
                self.screen.blit(opponent_text, opponent_text.get_rect(center = (self.screen_width*3/4, 35)))
            else:
                player_text = self.game_font.render(f"SCORE: {self.player_score}", False, self.accent_color)
                self.screen.blit(player_text, player_text.get_rect(center = (self.screen_width/4, 35)))
                opponent_text = self.game_font.render(f"HIGH SCORE: {infinite_highscore}", False, self.accent_color)
                self.screen.blit(opponent_text, opponent_text.get_rect(center = (self.screen_width*3/4, 35)))

            #ball and players
            if self.game_over == 0:
                pygame.draw.ellipse(self.screen, self.ball_color, self.ball)
            pygame.draw.rect(self.screen, self.accent_color, self.player)
            pygame.draw.rect(self.screen, self.accent_color, self.opponent)

            #if game's over, show who won or lost
            if self.game_over:
                self.end_game()

            #if someone scored, reset ball at the middle 
            if self.restart:
                self.ball_restart()
                
            #Updating the window
            pygame.display.flip()
            #60 frames per second
            self.clock.tick(60)


#MAIN LOOP# 
gamemode = 0
color_mode = 1
infinite_highscore = 0
previous_highscore = 0
while True:
    if gamemode == 0:
        menu = Menu()
    elif gamemode == 1:
        one_player = OnePlayer()
    elif gamemode == 2:
        two_player = TwoPlayer()
    elif gamemode == 3:
        infinite = Infinite()