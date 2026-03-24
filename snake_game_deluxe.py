import pygame
import random
import math
import sys
from collections import deque

pygame.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
CELL_SIZE = min(WINDOW_WIDTH, WINDOW_HEIGHT) // GRID_SIZE
GAME_AREA_WIDTH = GRID_SIZE * CELL_SIZE
GAME_AREA_HEIGHT = GRID_SIZE * CELL_SIZE
GAME_AREA_X = (WINDOW_WIDTH - GAME_AREA_WIDTH) // 2
GAME_AREA_Y = (WINDOW_HEIGHT - GAME_AREA_HEIGHT) // 2

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_BLACK = (10, 10, 20)

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.vx = random.uniform(-5, 5)
        self.vy = random.uniform(-5, 5)
        self.color = color
        self.life = 255
        self.size = random.randint(2, 6)
        self.decay = random.randint(5, 15)
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.2
        self.life -= self.decay
        self.size = max(1, self.size - 0.1)
        return self.life > 0
    
    def draw(self, screen):
        if self.life > 0:
            alpha = min(255, self.life)
            color = (*self.color, alpha) if len(self.color) == 3 else self.color
            pos = (int(self.x), int(self.y))
            pygame.draw.circle(screen, color[:3], pos, int(self.size))

class Star:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.x = random.randint(0, WINDOW_WIDTH)
        self.y = random.randint(0, WINDOW_HEIGHT)
        self.brightness = random.randint(50, 255)
        self.twinkle_speed = random.uniform(0.01, 0.05)
        self.twinkle_phase = random.uniform(0, 2 * math.pi)
    
    def update(self):
        self.twinkle_phase += self.twinkle_speed
        self.brightness = int(128 + 127 * math.sin(self.twinkle_phase))
    
    def draw(self, screen):
        color = (self.brightness, self.brightness, self.brightness)
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), 1)

class Snake:
    def __init__(self):
        self.body = deque([(GRID_SIZE // 2, GRID_SIZE // 2)])
        self.direction = (1, 0)
        self.grow = False
        self.color_timer = 0
        self.trail = deque(maxlen=10)
    
    def move(self):
        head = self.body[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        
        if self.check_collision(new_head):
            return False
        
        self.trail.append(head)
        self.body.appendleft(new_head)
        
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False
        
        self.color_timer += 1
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
    
    def get_segment_color(self, index):
        hue = (self.color_timer * 2 + index * 15) % 360
        return self.hsv_to_rgb(hue, 1.0, 1.0)
    
    def hsv_to_rgb(self, h, s, v):
        h = h / 360
        i = int(h * 6)
        f = h * 6 - i
        p = v * (1 - s)
        q = v * (1 - f * s)
        t = v * (1 - (1 - f) * s)
        i = i % 6
        
        if i == 0:
            r, g, b = v, t, p
        elif i == 1:
            r, g, b = q, v, p
        elif i == 2:
            r, g, b = p, v, t
        elif i == 3:
            r, g, b = p, q, v
        elif i == 4:
            r, g, b = t, p, v
        else:
            r, g, b = v, p, q
        
        return (int(r * 255), int(g * 255), int(b * 255))

class Food:
    def __init__(self):
        self.position = self.generate_position()
        self.animation_timer = 0
        self.glow_timer = 0
    
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
    
    def update(self):
        self.animation_timer += 0.1
        self.glow_timer += 0.05
    
    def get_color(self):
        pulse = int(128 + 127 * math.sin(self.glow_timer))
        return (255, pulse, pulse)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("华丽贪吃蛇 ✨")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 32)
        self.tiny_font = pygame.font.Font(None, 24)
        
        self.snake = Snake()
        self.food = Food()
        self.particles = []
        self.stars = [Star() for _ in range(100)]
        
        self.score = 0
        self.game_over = False
        self.paused = False
        self.game_timer = 0
        self.shake_amount = 0
        
        self.high_score = 0
        self.combo = 0
        self.last_food_time = 0
    
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
                elif event.key == pygame.K_ESCAPE:
                    return False
        
        return True
    
    def create_food_particles(self, x, y):
        for _ in range(20):
            self.particles.append(Particle(
                GAME_AREA_X + x * CELL_SIZE + CELL_SIZE // 2,
                GAME_AREA_Y + y * CELL_SIZE + CELL_SIZE // 2,
                (255, random.randint(100, 255), random.randint(0, 100))
            ))
    
    def update(self):
        if not self.game_over and not self.paused:
            self.game_timer += 1
            self.food.update()
            
            for star in self.stars:
                star.update()
            
            if not self.snake.move():
                self.game_over = True
                self.create_explosion()
                self.shake_amount = 20
                if self.score > self.high_score:
                    self.high_score = self.score
            
            if self.snake.body[0] == self.food.position:
                self.snake.eat_food()
                
                current_time = pygame.time.get_ticks()
                if current_time - self.last_food_time < 2000:
                    self.combo += 1
                else:
                    self.combo = 1
                
                self.last_food_time = current_time
                bonus_score = 10 * self.combo
                self.score += bonus_score
                
                food_x, food_y = self.food.position
                self.create_food_particles(food_x, food_y)
                self.shake_amount = 5
                
                self.food.respawn(self.snake.body)
        
        if self.shake_amount > 0:
            self.shake_amount -= 1
        
        self.particles = [p for p in self.particles if p.update()]
    
    def create_explosion(self):
        head = self.snake.body[0]
        x = GAME_AREA_X + head[0] * CELL_SIZE + CELL_SIZE // 2
        y = GAME_AREA_Y + head[1] * CELL_SIZE + CELL_SIZE // 2
        for _ in range(50):
            self.particles.append(Particle(x, y, (255, random.randint(0, 100), 0)))
    
    def draw_gradient_background(self):
        for y in range(WINDOW_HEIGHT):
            color_value = int(20 + 15 * (y / WINDOW_HEIGHT))
            color = (color_value // 3, 0, color_value)
            pygame.draw.line(self.screen, color, (0, y), (WINDOW_WIDTH, y))
    
    def draw_starfield(self):
        for star in self.stars:
            star.draw(self.screen)
    
    def draw_game_area(self):
        shake_x = random.randint(-self.shake_amount, self.shake_amount) if self.shake_amount > 0 else 0
        shake_y = random.randint(-self.shake_amount, self.shake_amount) if self.shake_amount > 0 else 0
        
        game_surface = pygame.Surface((GAME_AREA_WIDTH, GAME_AREA_HEIGHT))
        game_surface.fill(DARK_BLACK)
        
        for i, segment in enumerate(self.snake.body):
            x = segment[0] * CELL_SIZE
            y = segment[1] * CELL_SIZE
            
            color = self.snake.get_segment_color(i)
            
            if i == 0:
                pygame.draw.rect(game_surface, color, (x + 2, y + 2, CELL_SIZE - 4, CELL_SIZE - 4), border_radius=8)
                glow_size = CELL_SIZE + int(5 * math.sin(self.game_timer * 0.1))
                glow_color = (*color, 50)
                pygame.draw.rect(game_surface, glow_color, 
                               (x - (glow_size - CELL_SIZE) // 2, 
                                y - (glow_size - CELL_SIZE) // 2, 
                                glow_size, glow_size), border_radius=10)
            else:
                size = CELL_SIZE - 4 - (i * 0.1)
                pygame.draw.rect(game_surface, color, 
                               (x + (CELL_SIZE - size) // 2, 
                                y + (CELL_SIZE - size) // 2, 
                                size, size), border_radius=4)
        
        food_x, food_y = self.food.position
        food_color = self.food.get_color()
        
        pulse = int(3 * math.sin(self.food.animation_timer))
        food_size = CELL_SIZE - 6 + pulse
        
        pygame.draw.rect(game_surface, food_color, 
                        (food_x * CELL_SIZE + (CELL_SIZE - food_size) // 2,
                         food_y * CELL_SIZE + (CELL_SIZE - food_size) // 2,
                         food_size, food_size), border_radius=food_size // 2)
        
        glow_size = food_size + 10
        glow_color = (*food_color, 30)
        pygame.draw.rect(game_surface, glow_color,
                        (food_x * CELL_SIZE + (CELL_SIZE - glow_size) // 2,
                         food_y * CELL_SIZE + (CELL_SIZE - glow_size) // 2,
                         glow_size, glow_size), border_radius=glow_size // 2)
        
        self.screen.blit(game_surface, (GAME_AREA_X + shake_x, GAME_AREA_Y + shake_y))
    
    def draw_ui(self):
        score_text = self.font.render(f"得分: {self.score}", True, WHITE)
        self.screen.blit(score_text, (20, 20))
        
        if self.combo > 1:
            combo_text = self.small_font.render(f"连击 x{self.combo}!", True, (255, 255, 0))
            self.screen.blit(combo_text, (20, 70))
        
        high_score_text = self.small_font.render(f"最高分: {self.high_score}", True, (200, 200, 200))
        self.screen.blit(high_score_text, (WINDOW_WIDTH - 200, 20))
        
        controls = [
            "方向键: 移动",
            "P: 暂停",
            "ESC: 退出"
        ]
        
        for i, control in enumerate(controls):
            text = self.tiny_font.render(control, True, (150, 150, 150))
            self.screen.blit(text, (WINDOW_WIDTH - 120, WINDOW_HEIGHT - 80 + i * 25))
    
    def draw_particles(self):
        for particle in self.particles:
            particle.draw(self.screen)
    
    def draw_game_over(self):
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        game_over_text = self.font.render("游戏结束!", True, (255, 100, 100))
        text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 100))
        self.screen.blit(game_over_text, text_rect)
        
        final_score_text = self.font.render(f"最终得分: {self.score}", True, WHITE)
        score_rect = final_score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 40))
        self.screen.blit(final_score_text, score_rect)
        
        if self.score == self.high_score and self.score > 0:
            new_record_text = self.small_font.render("🏆 新纪录! 🏆", True, (255, 215, 0))
            record_rect = new_record_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            self.screen.blit(new_record_text, record_rect)
        
        restart_text = self.small_font.render("按空格键重新开始", True, WHITE)
        restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
        self.screen.blit(restart_text, restart_rect)
    
    def draw_pause(self):
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(100)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        pause_text = self.font.render("暂停", True, WHITE)
        text_rect = pause_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        self.screen.blit(pause_text, text_rect)
        
        continue_text = self.small_font.render("按 P 继续", True, WHITE)
        continue_rect = continue_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
        self.screen.blit(continue_text, continue_rect)
    
    def restart_game(self):
        self.snake = Snake()
        self.food = Food()
        self.particles.clear()
        self.score = 0
        self.game_over = False
        self.paused = False
        self.game_timer = 0
        self.shake_amount = 0
        self.combo = 0
        self.last_food_time = 0
    
    def draw(self):
        self.draw_gradient_background()
        self.draw_starfield()
        self.draw_game_area()
        self.draw_particles()
        self.draw_ui()
        
        if self.paused:
            self.draw_pause()
        
        if self.game_over:
            self.draw_game_over()
        
        pygame.display.flip()
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(12)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()