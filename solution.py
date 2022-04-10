from ast import With
from turtle import left
import pygame
pygame.init()


WIDTH, HEIGHT = 700, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_RADIUS = 7
SCORE_FONT = pygame.font.SysFont("comicsans", 20)
WIN_TEXT_FONT = pygame.font.SysFont("comicsan", 75)
WINNING_SCORE = 3 

class Paddle:
    COLOR = WHITE
    VEL = 5
    
    def __init__(self, x, y, width, height):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height
        
    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))
        
    def move(self, up=True):
        if up: 
            self.y -= self.VEL
        else:
            self.y += self.VEL
            
    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        
class Ball:
    MAX_VEL = 6
    COLOR = WHITE
    
    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = self.MAX_VEL 
        self.y_vel = 0
        
    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)
        
    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel
        
    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel *= -1
        
def draw(win, paddLes, ball, left_score, right_score):
    win.fill(BLACK)
    
    left_score_text = SCORE_FONT.render(f"Player One: {left_score}", 1, WHITE)
    right_score_text = SCORE_FONT.render(f"Player Two: {right_score}", 1, WHITE)
    win.blit(left_score_text, (WIDTH//4 - left_score_text.get_width()//2, 20))
    win.blit(right_score_text, (WIDTH*(3/4) - right_score_text.get_width()//2, 20))
    
    for paddle in paddLes:
        paddle.draw(win)
        
    for i in range(10, HEIGHT, HEIGHT//20):
        if i % 2 == 1:
            continue
        pygame.draw.rect(win, WHITE, (WIDTH//2 - 3.5, i, 7, HEIGHT//25)) # Draw the middle white line
    
    ball.draw(win)
    pygame.display.update() # Update the window after drawing

def handle_collision(ball, left_paddle, right_paddle):
    if ball.y + ball.radius >= HEIGHT: # Checking if the ball is hitting the bottom corner
        ball.y_vel *= -1 # Reverse the movement of the ball
    elif ball.y - ball.radius <= 0: # Checking if the ball is hitting the top corner
        ball.y_vel *= -1 
    
    # Checking the collision with the left paddle
    if ball.x_vel < 0: 
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height: 
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width: # Checking the right edge of the paddle, so that we need to add width
                ball.x_vel *= -1
                
                middle_y = left_paddle.y + left_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (left_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel
                
    # Checking the collision with the right paddle
    else: 
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height: 
            if ball.x + ball.radius >= right_paddle.x: # Checking the left edge of the paddle, so that we don't need to add width
                ball.x_vel *= -1 
                
                middle_y = right_paddle.y + right_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (right_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel

def handle_paddle_movement(keys, left_paddle, right_paddle):
    if keys[pygame.K_w] and left_paddle.y - left_paddle.VEL >= 0: 
        left_paddle.move(up=True)
    if keys[pygame.K_s] and left_paddle.y + left_paddle.VEL + left_paddle.height <= HEIGHT:
        left_paddle.move(up=False)
        
    if keys[pygame.K_UP] and right_paddle.y - right_paddle.VEL >= 0:
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.VEL + right_paddle.height <= HEIGHT:
        right_paddle.move(up=False)
        
def main():
    run = True
    clock = pygame.time.Clock()
    left_paddle = Paddle(10, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT) # Draw left paddle 
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT) # Draw right paddle
    ball = Ball(WIDTH//2, HEIGHT//2, BALL_RADIUS)
    right_score = 0
    left_score = 0
    
    while run:
        clock.tick(FPS) # Lock the FPS to 60 frames per second
        draw(WIN, [left_paddle, right_paddle], ball, left_score, right_score)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            
        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, left_paddle, right_paddle)
        ball.move()
        handle_collision(ball, left_paddle, right_paddle)
        
        #Giving the scores if the ball bounces out off the edge and reset the paddles
        if ball.x <0:
            right_score += 1
            ball.reset()
            right_paddle.reset()
        elif ball.x > WIDTH:
            left_score += 1
            ball.reset()
            left_paddle.reset()

        won = False
        if left_score >= WINNING_SCORE:
           won = True
           win_text = "Player One Won!"
        elif right_score >= WINNING_SCORE:
            won = True
            win_text = "Player Two Won!"
            
        if won:
            text = WIN_TEXT_FONT.render(win_text, 1, WHITE)
            WIN.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(3000)
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            left_score = 0 
            right_score = 0
    
    pygame.quit()
    
if __name__ == "__main__":
    main()