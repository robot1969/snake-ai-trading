import pygame
import random
import sys

pygame.init()

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
GRID_SIZE = 20
CELL_SIZE = WINDOW_WIDTH // GRID_SIZE

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
DARK_GREEN = (0, 150, 0)

class Snake:
    def __init__(self):
        self.body = [(GRID_SIZE // 2, GRID_SIZE // 2)]
        self.direction = (1, 0)
        self.grow = False
    
    def move(self):
        head = self.body[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        
        if self.check_collision(new_head):
            return False
        
        self.body.insert(0, new_head)
        
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False
        
        return True
    
    def check_collision(self, position):
        x, y = position
        if x < 0 or x >= GRID_SIZE or y < 0 or y >= GRID_SIZE:
            return True
        if position in self.body:
            return True
        return False
    
    def change_direction(self, new_direction):
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.direction = new_direction
    
    def eat_food(self):
        self.grow = True

class Food:
    def __init__(self):
        self.position = self.generate_position()
    
    def generate_position(self):
        while True:
            x = random.randint(0, GRID_SIZE - 1)
            y = random.randint(0, GRID_SIZE - 1)
            return (x, y)
    
    def respawn(self, snake_body):
        while True:
            x = random.randint(0, GRID_SIZE - 1)
            y = random.randint(0, GRID_SIZE - 1)
            if (x, y) not in snake_body:
                self.position = (x, y)
                break

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("贪吃蛇游戏")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.game_over = False
        self.paused = False
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.snake.change_direction((0, -1))
                elif event.key == pygame.K_DOWN:
                    self.snake.change_direction((0, 1))
                elif event.key == pygame.K_LEFT:
                    self.snake.change_direction((-1, 0))
                elif event.key == pygame.K_RIGHT:
                    self.snake.change_direction((1, 0))
                elif event.key == pygame.K_SPACE and self.game_over:
                    self.restart_game()
                elif event.key == pygame.K_p and not self.game_over:
                    self.paused = not self.paused
        
        return True
    
    def update(self):
        if not self.game_over and not self.paused:
            if not self.snake.move():
                self.game_over = True
            
            if self.snake.body[0] == self.food.position:
                self.snake.eat_food()
                self.score += 10
                self.food.respawn(self.snake.body)
    
    def draw(self):
        self.screen.fill(BLACK)
        
        for i, segment in enumerate(self.snake.body):
            x = segment[0] * CELL_SIZE
            y = segment[1] * CELL_SIZE
            if i == 0:
                pygame.draw.rect(self.screen, DARK_GREEN, (x, y, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(self.screen, GREEN, (x + 2, y + 2, CELL_SIZE - 4, CELL_SIZE - 4))
            else:
                pygame.draw.rect(self.screen, GREEN, (x, y, CELL_SIZE, CELL_SIZE))
        
        food_x = self.food.position[0] * CELL_SIZE
        food_y = self.food.position[1] * CELL_SIZE
        pygame.draw.rect(self.screen, RED, (food_x, food_y, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(self.screen, WHITE, (food_x + 2, food_y + 2, CELL_SIZE - 4, CELL_SIZE - 4))
        
        score_text = self.font.render(f"得分: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        if self.paused:
            pause_text = self.font.render("暂停", True, WHITE)
            text_rect = pause_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            self.screen.blit(pause_text, text_rect)
            
            continue_text = self.small_font.render("按 P 继续", True, WHITE)
            continue_rect = continue_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 40))
            self.screen.blit(continue_text, continue_rect)
        
        if self.game_over:
            game_over_text = self.font.render("游戏结束!", True, RED)
            text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 40))
            self.screen.blit(game_over_text, text_rect)
            
            final_score_text = self.font.render(f"最终得分: {self.score}", True, WHITE)
            score_rect = final_score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            self.screen.blit(final_score_text, score_rect)
            
            restart_text = self.small_font.render("按空格键重新开始", True, WHITE)
            restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 40))
            self.screen.blit(restart_text, restart_rect)
        
        pygame.display.flip()
    
    def restart_game(self):
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.game_over = False
        self.paused = False
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(10)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()