import pygame
import sys
from pygame.math import Vector2
import random

pygame.init()

pygame.display.set_caption("Snake Game")

FPS = 60
CELL_SIZE = 40
CELL_NUMBER = 20

screen = pygame.display.set_mode((CELL_SIZE * CELL_NUMBER, CELL_SIZE * CELL_NUMBER))
clock = pygame.time.Clock()


class Fruit:
    def __init__(self):
        """Create x and y position, create a vector 2d, draw a square
        """
        self.apple = pygame.transform.scale(pygame.image.load("Graphics/apple_2.png"), (CELL_SIZE, CELL_SIZE))
        self.x = random.randint(0, CELL_NUMBER - 1)
        self.y = random.randint(0, CELL_NUMBER - 1)
        self.pos = Vector2(self.x, self.y)
    
    def draw_fruit(self):
        """Create a rectangle, draw the rectangle
        """
        fruit_rect = pygame.Rect(int(self.pos.x * CELL_SIZE), int(self.pos.y * CELL_SIZE), CELL_SIZE, CELL_SIZE)
        #pygame.draw.rect(screen, (255, 128, 128), fruit_rect)
        screen.blit(self.apple, fruit_rect)

    def randomize(self):
        self.x = random.randint(0, CELL_NUMBER - 1)
        self.y = random.randint(0, CELL_NUMBER - 1)
        self.pos = Vector2(self.x, self.y)

class Snake:
    def __init__(self):
        self.body = [Vector2(5, 5), Vector2(4, 5), Vector2(3, 5)]
        self.direction = Vector2(1, 0)
        self.new_block = False

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


    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()
        # for block in self.body:
        #     x_pos = int(block.x * CELL_SIZE)
        #     y_pos = int(block.y * CELL_SIZE)
        #     block_rect = pygame.Rect(x_pos, y_pos, CELL_SIZE, CELL_SIZE)
        #     pygame.draw.rect(screen, (26, 26, 255), block_rect)

        for index, block in enumerate(self.body):
            # 1. We still need a rect for the positioning
            x_pos = int(block.x * CELL_SIZE)
            y_pos = int(block.y * CELL_SIZE)
            block_rect = pygame.Rect(x_pos, y_pos, CELL_SIZE, CELL_SIZE)
            
            # 2. What direction is the face heading
            if index == 0:  # 0 is the first element, so it's always head
                screen.blit(self.head, block_rect)
            elif index == len(self.body) -1:    #Last segment
                screen.blit(self.tail, block_rect)
            else:
                # Indexing from self.body, index is going to be our current element. Adding or subtracting one to get previous or next block. Subtracting the current block to get relation between those two ->
                # Getting the vector pointing the direction
                previous_block = self.body[index + 1] - block   
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    if (previous_block.x == -1 and next_block.y == -1) or (previous_block.y == -1 and next_block.x == -1): 
                        screen.blit(self.body_tl, block_rect)
                    elif (previous_block.x == -1 and next_block.y == 1) or (previous_block.y == 1 and next_block.x == -1): 
                        screen.blit(self.body_bl, block_rect)
                    elif (previous_block.x == 1 and next_block.y == -1) or (previous_block.y == -1 and next_block.x == 1): 
                        screen.blit(self.body_tr, block_rect)
                    elif (previous_block.x == 1 and next_block.y == 1) or (previous_block.y == 1 and next_block.x == 1): 
                        screen.blit(self.body_br, block_rect)


    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1, 0):
            self.head = self.head_left
        elif head_relation == Vector2(-1, 0):
            self.head = self.head_right
        elif head_relation == Vector2(0, 1):
            self.head = self.head_up
        elif head_relation == Vector2(0, -1):
            self.head = self.head_down
    

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1, 0):
            self.tail = self.tail_left
        elif tail_relation == Vector2(-1, 0):
            self.tail = self.tail_right
        elif tail_relation == Vector2(0, 1):
            self.tail = self.tail_up
        elif tail_relation == Vector2(0, -1):
            self.tail = self.tail_down


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

class Score:
    def __init__(self, snake):
        self.score_font = pygame.font.Font("Font/score.ttf", 30)
        self.game_over_font = pygame.font.Font("Font/game_over.ttf", 120)
        self.snake = snake

    def draw_score(self):
        self.score = str(len(self.snake.body) - 3)
        self.score_text = self.score_font.render(f"Score: {self.score}", 1, (255, 255, 255))
        #This way text is set perfectly in the center on X axis
        self.text_width = self.score_text.get_width()
        screen.blit(self.score_text, ((CELL_NUMBER * CELL_SIZE) / 2 - (self.text_width / 2), 20))
        #print(self.score)
        

    def draw_game_over(self):
        self.game_over_text = self.game_over_font.render("GAME OVER", 1, (255, 255, 255))
        #This way text is set perfectly in the center on X and Y axis
        self.text_width = self.game_over_text.get_width()
        self.text_height = self.game_over_text.get_height()
        screen.blit(self.game_over_text, ((CELL_NUMBER * CELL_SIZE / 2) - self.text_width/2, (CELL_NUMBER * CELL_SIZE / 2) - self.text_height/2))
        pygame.display.update()


class SoundManager:
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

class Main:
    """Main class contains the entire game logic as well as snake and fruit object
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
        self.score.draw_score()
        
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
        sound_manager.play_game_over()
        sound_manager.stop_background_music()
        pygame.time.delay(3000)
        pygame.quit()
        sys.exit()



    def draw_grass(self):
        self.grass = pygame.transform.scale(pygame.image.load("Graphics/grass_template2.jpg"), (CELL_SIZE * CELL_NUMBER, CELL_SIZE * CELL_NUMBER))
        screen.blit(self.grass, (0, 0))


    

screen_update = pygame.USEREVENT    # custom event - I don;t want to update move_snake every time so I created custom event
pygame.time.set_timer(screen_update, 100)

main_game = Main()
# pygame.mixer.music.play(-1)
sound_manager = SoundManager()
sound_manager.play_background_music()

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

    screen.fill((150, 219, 159))
    main_game.draw_elements()
    #pygame.draw.rect(screen, (210, 159, 72), test_rect)
    #screen.blit(test_surface, test_rect)   # Surface and coordinates
    
    pygame.display.update()
    clock.tick(FPS)
    