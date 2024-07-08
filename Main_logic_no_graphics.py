import pygame
import sys
from pygame.math import Vector2
import random

FPS = 60
CELL_SIZE = 40
CELL_NUMBER = 20

screen = pygame.display.set_mode((CELL_SIZE * CELL_NUMBER, CELL_SIZE * CELL_NUMBER))
clock = pygame.time.Clock()

class Fruit:
    def __init__(self):
        """Create x and y position, create a vector 2d, draw a quare
        """
        self.x = random.randint(0, CELL_NUMBER - 1)
        self.y = random.randint(0, CELL_NUMBER - 1)
        self.pos = Vector2(self.x, self.y)
    
    def draw_fruit(self):
        """Create a rectangle, draw the rectangle
        """
        fruit_rect = pygame.Rect(int(self.pos.x * CELL_SIZE), int(self.pos.y * CELL_SIZE), CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, (255, 128, 128), fruit_rect)
        
    def randomize(self):
        self.x = random.randint(0, CELL_NUMBER - 1)
        self.y = random.randint(0, CELL_NUMBER - 1)
        self.pos = Vector2(self.x, self.y)

class Snake:
    def __init__(self):
        self.body = [Vector2(5, 5), Vector2(4, 5), Vector2(3, 5)]
        self.direction = Vector2(1, 0)
        self.new_block = False

    def draw_snake(self):
        for block in self.body:
            x_pos = int(block.x * CELL_SIZE)
            y_pos = int(block.y * CELL_SIZE)
            block_rect = pygame.Rect(x_pos, y_pos, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, (26, 26, 255), block_rect)
 
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

class Main:
    """Main class contains the entire game logic as well as snake and fruit object
    """
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()
    
    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.fruit.draw_fruit()
        self.snake.draw_snake()

    def check_collision(self):
        """Checking for colliosn between snake and fruit, reposiiton the fruit, add another block to snake
        """
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
    
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
        pygame.quit()
        sys.exit()


screen_update = pygame.USEREVENT    # castom event - I don;t want to update move_snake every time so I created castom event
pygame.time.set_timer(screen_update, 100)

main_game = Main()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == screen_update:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and main_game.snake.direction.y != 1: #This way cannot reverese amd kill himself
                main_game.snake.direction = Vector2(0, -1) #Chaning vetor -> changing direction
            if event.key == pygame.K_DOWN and main_game.snake.direction.y != -1:
                main_game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_RIGHT and main_game.snake.direction.x != 1:
                main_game.snake.direction = Vector2(1, 0)
            if event.key == pygame.K_LEFT and main_game.snake.direction.x != 1:
                main_game.snake.direction = Vector2(-1, 0)

    screen.fill((150, 219, 159))
    main_game.draw_elements()
    #pygame.draw.rect(screen, (210, 159, 72), test_rect)
    #screen.blit(test_surface, test_rect)   # Surface and coordinates
    
    pygame.display.update()
    clock.tick(FPS)
    
    # 1:02:23