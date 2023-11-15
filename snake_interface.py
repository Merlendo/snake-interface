# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import random

pygame.init() # Init the pygame engine

# Set the FPS
FPS = 5
CLOCK = pygame.time.Clock()

# Screen information
WIDTH = 500
HEIGHT = 500

# Define color
WHITE = (255, 255, 255)
BLACK = (50, 50, 50)
GREY = (125, 125, 125)
GREEN = (0, 125, 0)
RED = (125, 0, 0)

# Create font
FONT = pygame.font.SysFont('Courier New', int((WIDTH+HEIGHT)//2*0.06), bold=True)

# Display the screen
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("snake")

# Pixel size
PIXEL_SIZE = 20
NB_PIXEL_COL = WIDTH // PIXEL_SIZE # width
NB_PIXEL_ROW = HEIGHT // PIXEL_SIZE # height


def generate_apple(snake):
    """Generate the apple"""
    
    col = random.randint(0, NB_PIXEL_COL - 1)
    row = random.randint(0, NB_PIXEL_ROW - 1)
    
    apple = pygame.Rect(col*PIXEL_SIZE, row*PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE)

    #Ckeck if the apple pos is not in the snake
    while apple.collidelistall(snake):
        col = random.randint(0, NB_PIXEL_COL - 1)
        row = random.randint(0, NB_PIXEL_ROW - 1)
        apple = pygame.Rect(col*PIXEL_SIZE, row*PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE)

    return apple


def move_snake(snake, direction, eating):
    """Move the snake"""
    
    head = snake[0].copy()
    if direction == "up":
        head.y -= PIXEL_SIZE
    if direction == "down":
        head.y += PIXEL_SIZE
    if direction == "left":
        head.x -= PIXEL_SIZE
    if direction == "right":
        head.x += PIXEL_SIZE
    
    snake.insert(0, head)
    
    if not eating:
        snake.pop()
    
    eating = False
        
    return snake, direction, eating
    
    
def check_collision(snake, apple, score, eating, game_active):
    """Manage the collision with the snake"""
    
    # Collision with apple
    if snake[0].colliderect(apple):
        eating = True
        apple = generate_apple(snake)
        score += 1
        
    # Collision with itself
    if snake[0].collidelistall(snake[1:]) and len(snake) > 1:
        game_active = False
        print("collision avec le serpent")
    
    # Collision with the borders
    if snake[0].x < 0 or snake[0].x >= WIDTH or snake[0].y < 0 or snake[0].y >= HEIGHT:
        game_active = False
        print("collision avec le mur")
        
    return snake, apple, score, eating, game_active
    

# Init snake
snake = [pygame.Rect(NB_PIXEL_COL//2*PIXEL_SIZE, (NB_PIXEL_ROW//2-1)*PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE)]
direction = "left"
eating = False

# Init apple
apple = generate_apple(snake)

# Init score
score = 0

# Main game
run = True 
game_active = True
restart = False
while run:
    
    # Display the score
    pygame.display.set_caption(f"snake | score : {score}")
    
    # Exit if the window is closed
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
            
        if game_active: 
            # Change the direction of the snake according to the key pressed
            if event.type == pygame.KEYDOWN:
                if event.key == K_UP and direction != "down":
                    direction = "up"
                if event.key == K_DOWN and direction != "up":
                    direction = "down"
                if event.key == K_LEFT and direction != "right":
                    direction = "left"
                if event.key == K_RIGHT and direction != "left":
                    direction = "right"
        else :
            # Restart the game if the Enter key is pressed
            if event.type == pygame.KEYDOWN:
                if event.key == K_RETURN:
                    restart = True
    
    # When the game is active   
    if game_active: 
         
        # Draw the background
        SCREEN.fill(GREY)
        for col in range(NB_PIXEL_COL):
            for row in range(NB_PIXEL_ROW):
                pygame.draw.rect(SCREEN, BLACK, (col*PIXEL_SIZE, row*PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE), width=1)
          
        # Draw the snake
        for r_snake in snake:
            pygame.draw.rect(SCREEN, GREEN, r_snake)
        
        # Draw the apple
        pygame.draw.rect(SCREEN, RED, apple)
        
        # Move the snake
        snake, direction, eating = move_snake(snake, direction, eating)
        
        # Check collisions
        snake, apple, score, eating, game_active = check_collision(snake, apple, score, eating, game_active)

        pygame.display.update()
    
    # When the game is over  
    else:
        
        # Draw the game over text
        text_end = FONT.render(f"Game Over | score : {score}", True, WHITE, BLACK)
        SCREEN.blit(text_end, (WIDTH//2 - text_end.get_width() // 2, HEIGHT//2 - text_end.get_height()//2))
                    
        pygame.display.update()
        
        # Restart a game if the player press Enter
        if restart:
            # Init snake
            snake = [pygame.Rect(NB_PIXEL_COL//2*PIXEL_SIZE, (NB_PIXEL_ROW//2-1)*PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE)]
            direction = "left"
            eating = False

            # Init apple
            apple = generate_apple(snake)

            # Init score
            score = 0
            
            restart = False
            game_active = True

            
    CLOCK.tick(FPS)

pygame.quit()