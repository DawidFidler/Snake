import pygame
import sys
from pygame.math import Vector2
import random
import math

pygame.init()
pygame.display.set_caption("Snake Game")

FPS = 60
CELL_SIZE = 40
CELL_NUMBER = 20

screen = pygame.display.set_mode((CELL_SIZE * CELL_NUMBER, CELL_SIZE * CELL_NUMBER))
clock = pygame.time.Clock()


class Fruit:
    def __init__(self):
        """Creates x and y position, create a vector 2d, draw a square
        """
        self.x = random.randint(0, CELL_NUMBER - 1)
        self.y = random.randint(0, CELL_NUMBER - 1)
        self.pos = Vector2(self.x, self.y)
    
    def draw_fruit(self):
        """Creates a rectangle, draw the rectangle
        """
        fruit_rect = pygame.Rect(int(self.pos.x * CELL_SIZE), int(self.pos.y * CELL_SIZE), CELL_SIZE, CELL_SIZE)
        #pygame.draw.rect(screen, (255, 128, 128), fruit_rect)
        screen.blit(asset_manager.apple, fruit_rect)

    def randomize(self):
        """Makes random fruit position spawn
        """
        self.x = random.randint(0, CELL_NUMBER - 1)
        self.y = random.randint(0, CELL_NUMBER - 1)
        self.pos = Vector2(self.x, self.y)

class Snake:
    def __init__(self):
        self.body = [Vector2(5, 5), Vector2(4, 5), Vector2(3, 5)]
        self.direction = Vector2(1, 0)
        self.new_block = False     

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()
        # for block in self.body:
        #     x_pos = int(block.x * CELL_SIZE)
        #     y_pos = int(block.y * CELL_SIZE)
        #     block_rect = pygame.Rect(x_pos, y_pos, CELL_SIZE, CELL_SIZE)
        #     pygame.draw.rect(screen, (26, 26, 255), block_rect)

        for index, block in enumerate(self.body):
            # 1. I still need a rect for the positioning
            x_pos = int(block.x * CELL_SIZE)
            y_pos = int(block.y * CELL_SIZE)
            block_rect = pygame.Rect(x_pos, y_pos, CELL_SIZE, CELL_SIZE)
            
            # 2. What direction is the face heading
            if index == 0:  # 0 is the first element, so it's always head
                screen.blit(self.head, block_rect)
            elif index == len(self.body) -1:    # Last segment
                screen.blit(self.tail, block_rect)
            else:
                # Indexing from self.body, index is going to be our current element. Adding or subtracting one to get previous or next block. Subtracting the current block to get relation between those two ->
                # Getting the vector pointing the direction
                previous_block = self.body[index + 1] - block   
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(asset_manager.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(asset_manager.body_horizontal, block_rect)
                else:
                    if (previous_block.x == -1 and next_block.y == -1) or (previous_block.y == -1 and next_block.x == -1): 
                        screen.blit(asset_manager.body_tl, block_rect)
                    elif (previous_block.x == -1 and next_block.y == 1) or (previous_block.y == 1 and next_block.x == -1): 
                        screen.blit(asset_manager.body_bl, block_rect)
                    elif (previous_block.x == 1 and next_block.y == -1) or (previous_block.y == -1 and next_block.x == 1): 
                        screen.blit(asset_manager.body_tr, block_rect)
                    elif (previous_block.x == 1 and next_block.y == 1) or (previous_block.y == 1 and next_block.x == 1): 
                        screen.blit(asset_manager.body_br, block_rect)


    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1, 0):
            self.head = asset_manager.head_left
        elif head_relation == Vector2(-1, 0):
            self.head = asset_manager.head_right
        elif head_relation == Vector2(0, 1):
            self.head = asset_manager.head_up
        elif head_relation == Vector2(0, -1):
            self.head = asset_manager.head_down
    

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1, 0):
            self.tail = asset_manager.tail_left
        elif tail_relation == Vector2(-1, 0):
            self.tail = asset_manager.tail_right
        elif tail_relation == Vector2(0, 1):
            self.tail = asset_manager.tail_up
        elif tail_relation == Vector2(0, -1):
            self.tail = asset_manager.tail_down


    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]    # : -> all elements
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]    # : -> all elements


    def add_block(self):
        self.new_block = True
    
    def snake_reset(self):
        """Resets snake position after loose and pressing space again
        """
        self.body = [Vector2(5, 5), Vector2(4, 5), Vector2(3, 5)]
        self.direction = Vector2(1, 0)

class Score:
    def __init__(self, snake):
        self.snake = snake

    def draw_actual_score(self):
        """Draws actual score in current gameplay
        """
        self.score = str(len(self.snake.body) - 3)
        self.score_text = asset_manager.actual_score_font.render(f"score: {self.score}", 1, (255, 255, 255))
        #This way text is set perfectly in the center on X axis
        self.text_width = self.score_text.get_width()
        screen.blit(self.score_text, ((CELL_NUMBER * CELL_SIZE) / 2 - (self.text_width / 2), 20))
        #print(self.score)
        

    def draw_game_over(self):
        """Draws text after loosing
        """     
        self.game_over_text = asset_manager.game_over_font.render("GAME OVER", 1, (255, 255, 255))
        #This way text is set perfectly in the center on X and Y axis
        self.text_width = self.game_over_text.get_width()
        self.text_height = self.game_over_text.get_height()
        screen.blit(self.game_over_text, ((CELL_NUMBER * CELL_SIZE / 2) - self.text_width/2, 
                                          (CELL_NUMBER * CELL_SIZE / 2) - self.text_height/2))
        pygame.display.update()


    def draw_best_score(self):
        """Draws best score based on number read from text file
        """
        with open("best_score.txt", "r") as file:
            self.data = file.read()
        
        self.best_score_text = asset_manager.actual_score_font.render(f"best: {self.data}", 1, (255, 255, 255))
        screen.blit(self.best_score_text, (640, 750))
        

    def update_best_score(self):
        """Reads txt file with best score. When actual score is greater, the one in file is updated
        """
        self.score = len(self.snake.body) - 3
        with open("best_score.txt", "r") as file:
            self.old_best = file.read()
            self.old_best_int = int(self.old_best)
        
        if self.score > self.old_best_int:
            self.new_best = str(self.score)
            with open("best_score.txt", "w") as file:
                file.write(self.new_best)
        
class SoundManager:
    """Contains and manages all sound and music used in game
    """
    def __init__(self):
        pygame.mixer.init()
        self.background_music = "Sound/music_background.mp3"
        self.crunch = pygame.mixer.Sound("Sound/crunch.wav")
        self.game_over = pygame.mixer.Sound("Sound\lose_trumpet.mp3")
        
        self.crunch.set_volume(0.1)
        pygame.mixer.music.load(self.background_music)
        pygame.mixer.music.set_volume(0.1)


    def play_background_music(self):
        pygame.mixer.music.play(-1)

    def stop_background_music(self):
        pygame.mixer.music.stop()

    def play_crunch(self):
        self.crunch.play()
    
    def play_game_over(self):
        self.game_over.play()

class AssetManager:
    """Contains and manages graphics and fonts used in game
    """
    def __init__(self):
        self.apple = pygame.transform.scale(pygame.image.load("Graphics/apple_2.png"), (CELL_SIZE, CELL_SIZE))
        self.head_up = pygame.image.load('Graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('Graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('Graphics/head_left.png').convert_alpha()
        self.tail_up = pygame.image.load('Graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Graphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('Graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('Graphics/tail_left.png').convert_alpha()
        self.body_vertical = pygame.image.load('Graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Graphics/body_horizontal.png').convert_alpha()
        self.body_tr = pygame.image.load('Graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('Graphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('Graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('Graphics/body_bl.png').convert_alpha()
        self.grass = pygame.transform.scale(pygame.image.load("Graphics/grass_template2.jpg"), (CELL_SIZE * CELL_NUMBER, CELL_SIZE * CELL_NUMBER))
        self.menu_background = pygame.transform.scale(pygame.image.load("Graphics/menu_background.jpg"), (CELL_SIZE * CELL_NUMBER, CELL_SIZE * CELL_NUMBER))

        self.actual_score_font = pygame.font.Font("Font/score.ttf", 30)
        self.game_over_font = pygame.font.Font("Font/game_over.ttf", 120)
        self.menu_font = pygame.font.Font(None, 64)

class MainGame:
    """Contains the entire game logic as well as snake and fruit object
    """
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()
        self.score = Score(self.snake)  #passing existing snake object in order to have correct snake length

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.score.draw_actual_score()
        self.score.draw_best_score()
        
    def check_collision(self):
        """Checking for collision between snake and fruit, reposition the fruit, add another block to snake
        """
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            sound_manager.play_crunch()
        
        for block in self.snake.body[1:]:   # Fruit won't spawn in snake
            if block == self.fruit.pos:
                self.fruit.randomize()

    def check_fail(self):
        """Check if snake id outside the screen, check if snake hit himself
        """
        if self.snake.body[0].x < 0 or self.snake.body[0].x > CELL_NUMBER - 1:
            self.game_over()
        if self.snake.body[0].y < 0 or self.snake.body[0].y > CELL_NUMBER - 1:
            self.game_over()

        for block in self.snake.body[1:]:    # Taking elements that come after the head
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        self.score.draw_game_over()
        self.score.update_best_score()
        sound_manager.play_game_over()
        sound_manager.stop_background_music()
        pygame.time.delay(2000)
        main_menu.display_menu()

    def draw_grass(self):
        screen.blit(asset_manager.grass, (0, 0))
    
class MainMenu:
    """Displays main menu after run script, allows to start main game or stop executing code"""
    def __init__(self):
        self.menu_title_text = asset_manager.menu_font.render("Welcome to Snake Game", True, (255, 255, 255))

    def display_menu(self):
        """Creates loop with main menu"""
        sound_manager.play_background_music()

        run = True
        while run:
            screen.blit(asset_manager.menu_background, (0, 0))
            screen.blit(self.menu_title_text, (135, 150))
            self.display_pulsing_text(35, "Press SPACE to Play", (255, 255, 255), (400, 650))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        main_game.snake.snake_reset()
                        run = False
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
    
    def display_pulsing_text(self, base_size, text, color, position):
        '''As time progresses, this function causes the font size to increase and decrease,
        making the text pulsing/breathing'''
        self.base_size = base_size
        self.text = text
        self.color = color
        self.position = position
        self.time = pygame.time.get_ticks() / 1000 # returns the time(in seconds) since the start of the game
        self.base_size = 35
        self.time = pygame.time.get_ticks() / 1000 # returns the time(in seconds) since the start of the game

        self.size_offset = int(base_size + 10 * math.sin(self.time * 4)) # This line calculates how much the font size should pulsate ath the current time
            # math.sin(self.time * 4)creates a sinusoidal wave that oscillates between -1 and 1. Multiplication by 4 makes the oscillation faster
        self.size_offset = int(self.base_size + 10 * math.sin(self.time * 4)) # This line calculates how much the font size should pulsate ath the current time
            # math.sin(self.time)creates a sinusoidal wave that oscillates between -1 and 1. Multiplication by 4 makes the oscillation faster
            # Multiplication this by 10 scales the oscillation to a range of -10 to 10
            # Adding base size (35) result in the final font size, which oscillates between 25 and 45
        
        self.animated_font = pygame.font.Font(None, base_size + self.size_offset) # Creating new font with fluctuating size based on previous line
        self.play_text = self.animated_font.render(text, True, color)
        self.center = self.play_text.get_rect(center=position) # Creating a rectangle which is centered at the given coordinates
        screen.blit(self.play_text, self.center)
        

screen_update = pygame.USEREVENT    # custom event - I don;t want to update move_snake every time so I created custom event
pygame.time.set_timer(screen_update, 100)

main_game = MainGame()
sound_manager = SoundManager()
asset_manager = AssetManager()
main_menu = MainMenu()

main_menu.display_menu()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == screen_update:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and main_game.snake.direction.y != 1: #This way cannot reverse amd kill himself
                main_game.snake.direction = Vector2(0, -1) #Changing vector -> changing direction
            if event.key == pygame.K_DOWN and main_game.snake.direction.y != -1:
                main_game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_RIGHT and main_game.snake.direction.x != -1:
                main_game.snake.direction = Vector2(1, 0)
            if event.key == pygame.K_LEFT and main_game.snake.direction.x != 1:
                main_game.snake.direction = Vector2(-1, 0)

    
    main_game.draw_elements()   
    pygame.display.update()
    clock.tick(FPS)
    