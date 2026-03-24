import pygame
import random
import math
import sys
import json
import os
from collections import deque
from enum import Enum

pygame.init()

# Font management function
def get_font(size):
    """Get a font that supports Chinese characters"""
    chinese_fonts = [
        "simhei", "heiti", "microsoftyahei", 
        "sourcehansanscn", "notosanscjksc",
        "arial", "liberation sans", "dejavu sans"
    ]
    
    for font_name in chinese_fonts:
        try:
            return pygame.font.SysFont(font_name, size)
        except:
            continue
    # Fallback to default font
    return pygame.font.Font(None, size)

WINDOW_WIDTH = 900
WINDOW_HEIGHT = 700
GRID_SIZE = 25
CELL_SIZE = min(WINDOW_WIDTH - 200, WINDOW_HEIGHT - 100) // GRID_SIZE
GAME_AREA_WIDTH = GRID_SIZE * CELL_SIZE
GAME_AREA_HEIGHT = GRID_SIZE * CELL_SIZE
GAME_AREA_X = (WINDOW_WIDTH - GAME_AREA_WIDTH) // 2
GAME_AREA_Y = (WINDOW_HEIGHT - GAME_AREA_HEIGHT) // 2 + 20

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_BLACK = (10, 10, 20)
GOLD = (255, 215, 0)
SILVER = (192, 192, 192)
BRONZE = (205, 127, 50)

class GameState(Enum):
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"
    SETTINGS = "settings"
    HIGH_SCORES = "high_scores"

class PowerUpType(Enum):
    SPEED_BOOST = "speed_boost"
    SLOW_MOTION = "slow_motion"
    DOUBLE_POINTS = "double_points"
    INVINCIBLE = "invincible"
    MAGNET = "magnet"
    GHOST = "ghost"

class Particle:
    def __init__(self, x, y, color, particle_type="normal"):
        self.x = x
        self.y = y
        self.vx = random.uniform(-6, 6)
        self.vy = random.uniform(-6, 6)
        self.color = color
        self.life = 255
        self.initial_life = 255
        self.size = random.randint(2, 8)
        self.decay = random.randint(3, 12)
        self.type = particle_type
        self.rotation = random.uniform(0, 360)
        self.rotation_speed = random.uniform(-5, 5)
        
        # Enhanced particle properties
        self.trail = deque(maxlen=10)
        self.pulse_phase = random.uniform(0, 2 * math.pi)
        self.orbit_radius = random.uniform(0, 20)
        self.orbit_speed = random.uniform(0.1, 0.3)
        self.original_x = x
        self.original_y = y
        
        # Set particle-specific properties
        self.set_particle_properties()
    
    def set_particle_properties(self):
        """Set properties based on particle type"""
        if self.type == "normal":
            self.gravity = 0.2
            self.bounce = 0.7
            self.friction = 0.98
        elif self.type == "sparkle":
            self.gravity = 0.05
            self.bounce = 0.9
            self.friction = 0.95
        elif self.type == "star":
            self.gravity = 0.1
            self.bounce = 0.8
            self.friction = 0.97
            self.twinkle_speed = random.uniform(0.1, 0.3)
        elif self.type == "energy":
            self.gravity = 0
            self.bounce = 1.0
            self.friction = 1.0
            self.vx *= 1.5
            self.vy *= 1.5
        elif self.type == "magic":
            self.gravity = -0.1
            self.bounce = 1.2
            self.friction = 0.9
            self.wave_amplitude = random.uniform(5, 15)
            self.wave_frequency = random.uniform(0.1, 0.3)
        elif self.type == "explosion":
            self.gravity = 0.15
            self.bounce = 0.5
            self.friction = 0.85
            self.vx *= 2
            self.vy *= 2
            self.decay = random.randint(5, 15)
        elif self.type == "rainbow":
            self.gravity = 0.1
            self.bounce = 0.8
            self.friction = 0.95
            self.color_shift = random.uniform(0, 360)
            self.color_shift_speed = random.uniform(2, 5)
    
    def update(self):
        # Store previous position for trail
        self.trail.append((self.x, self.y, self.life))
        
        # Update position
        if self.type == "magic":
            # Magic particles move in waves
            wave_offset = math.sin(self.pulse_phase) * self.wave_amplitude
            self.x += self.vx + wave_offset * 0.1
            self.y += self.vy
            self.pulse_phase += self.wave_frequency
        elif self.type == "energy":
            # Energy particles have pulsing motion
            self.x += self.vx * math.cos(self.pulse_phase)
            self.y += self.vy * math.sin(self.pulse_phase)
            self.pulse_phase += 0.2
        elif self.type == "star":
            # Stars orbit their origin
            orbit_angle = self.pulse_phase
            orbit_x = math.cos(orbit_angle) * self.orbit_radius * 0.1
            orbit_y = math.sin(orbit_angle) * self.orbit_radius * 0.1
            self.x += self.vx + orbit_x
            self.y += self.vy + orbit_y
            self.pulse_phase += self.orbit_speed
        else:
            self.x += self.vx
            self.y += self.vy
        
        # Apply physics
        self.vy += self.gravity
        self.vx *= self.friction
        self.vy *= self.friction
        
        # Update life and size
        self.life -= self.decay
        life_ratio = self.life / self.initial_life
        
        # Size pulsing based on type
        if self.type in ["energy", "magic", "rainbow"]:
            pulse_factor = 1 + 0.2 * math.sin(self.pulse_phase)
            self.size = max(1, self.size * (0.5 + 0.5 * life_ratio) * pulse_factor)
        else:
            self.size = max(1, self.size - 0.15)
        
        self.rotation += self.rotation_speed
        
        # Color shifting for rainbow particles
        if self.type == "rainbow":
            self.color_shift += self.color_shift_speed
            if self.color_shift > 360:
                self.color_shift -= 360
        
        return self.life > 0
    
    def draw(self, screen):
        if self.life > 0:
            alpha = max(0, min(255, self.life))
            life_ratio = self.life / self.initial_life
            
            # Get particle color with effects first
            if self.type == "rainbow":
                # Rainbow particles shift colors
                hue = self.color_shift
                r = int(127 * (1 + math.cos(math.radians(hue))))
                g = int(127 * (1 + math.cos(math.radians(hue - 120))))
                b = int(127 * (1 + math.cos(math.radians(hue - 240))))
                color = (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))
            else:
                # Ensure color values are valid (0-255)
                if len(self.color) >= 3:
                    color = tuple(max(0, min(255, c)) for c in self.color[:3])
                else:
                    color = (255, 255, 255)
            
            # Draw trail for enhanced particles
            if self.type in ["energy", "magic", "rainbow"] and len(self.trail) > 1:
                for i in range(len(self.trail) - 1):
                    trail_alpha = int(alpha * (i / len(self.trail)) * 0.3)
                    trail_color = tuple(int(c * trail_alpha / 255) for c in color)
                    trail_size = max(1, int(self.size * (i / len(self.trail))))
                    
                    if i > 0:
                        start_pos = (int(self.trail[i][0]), int(self.trail[i][1]))
                        end_pos = (int(self.trail[i-1][0]), int(self.trail[i-1][1]))
                        pygame.draw.line(screen, trail_color, start_pos, end_pos, trail_size)
            
            pos = (int(self.x), int(self.y))
            
            # Draw different particle types with enhanced effects
            if self.type == "star":
                # Enhanced star with glow
                glow_size = int(self.size * 1.5)
                glow_color = tuple(int(c * 0.3) for c in color)
                pygame.draw.circle(screen, glow_color, pos, glow_size)
                
                points = []
                for i in range(5):
                    angle = self.rotation + i * 72
                    outer_x = pos[0] + self.size * math.cos(math.radians(angle))
                    outer_y = pos[1] + self.size * math.sin(math.radians(angle))
                    points.append((outer_x, outer_y))
                    
                    angle = self.rotation + i * 72 + 36
                    inner_x = pos[0] + (self.size * 0.5) * math.cos(math.radians(angle))
                    inner_y = pos[1] + (self.size * 0.5) * math.sin(math.radians(angle))
                    points.append((inner_x, inner_y))
                
                if len(points) >= 6:
                    pygame.draw.polygon(screen, color, points)
                    
            elif self.type == "sparkle":
                # Enhanced sparkle with multiple rays
                for layer in range(3):
                    layer_size = self.size * (1 - layer * 0.3)
                    layer_alpha = alpha * (1 - layer * 0.3)
                    layer_color = tuple(int(c * layer_alpha / 255) for c in color)
                    
                    pygame.draw.circle(screen, layer_color, pos, int(layer_size * 0.5))
                    
                    for i in range(8):
                        angle = i * 45 + self.rotation
                        ray_length = layer_size * (1.5 if layer == 0 else 1)
                        end_x = pos[0] + ray_length * math.cos(math.radians(angle))
                        end_y = pos[1] + ray_length * math.sin(math.radians(angle))
                        pygame.draw.line(screen, layer_color, pos, (end_x, end_y), 1)
                        
            elif self.type == "energy":
                # Energy particle with pulsing rings
                for i in range(3):
                    ring_size = self.size * (1 + i * 0.5) * (0.8 + 0.2 * math.sin(self.pulse_phase))
                    ring_alpha = int(alpha * (1 - i * 0.3))
                    ring_color = tuple(int(c * ring_alpha / 255) for c in color)
                    pygame.draw.circle(screen, ring_color, pos, int(ring_size), 1)
                    
            elif self.type == "magic":
                # Magic particle with mystical aura
                aura_size = self.size * 2
                for i in range(3):
                    aura_alpha = int(alpha * 0.1 * (3 - i))
                    aura_color = tuple(int(c * aura_alpha / 255) for c in color)
                    pygame.draw.circle(screen, aura_color, pos, int(aura_size - i * 2), 1)
                
                # Central core
                pygame.draw.circle(screen, color, pos, int(self.size))
                
            elif self.type == "explosion":
                # Explosion with expanding shockwave
                shockwave_size = self.size * (2 - life_ratio) * 2
                shockwave_alpha = int(alpha * 0.5 * life_ratio)
                shockwave_color = tuple(int(c * shockwave_alpha / 255) for c in color)
                pygame.draw.circle(screen, shockwave_color, pos, int(shockwave_size), 2)
                
                # Debris
                pygame.draw.circle(screen, color, pos, int(self.size))
                
            else:
                # Enhanced normal particle with glow
                glow_size = int(self.size * 1.2)
                glow_color = tuple(int(c * 0.5) for c in color)
                pygame.draw.circle(screen, glow_color, pos, glow_size)
                pygame.draw.circle(screen, color, pos, int(self.size))

class Star:
    def __init__(self, layer=0):
        self.layer = layer  # 0=background, 1=middle, 2=foreground
        self.reset()
    
    def reset(self):
        self.x = random.randint(0, WINDOW_WIDTH)
        self.y = random.randint(0, WINDOW_HEIGHT)
        
        # Layer-specific properties
        if self.layer == 0:  # Background stars
            self.brightness = random.randint(20, 100)
            self.twinkle_speed = random.uniform(0.01, 0.03)
            self.size = random.choice([1, 1, 1])
            self.speed = 0.1
            self.color_variation = random.randint(0, 30)
        elif self.layer == 1:  # Middle stars
            self.brightness = random.randint(50, 150)
            self.twinkle_speed = random.uniform(0.02, 0.05)
            self.size = random.choice([1, 1, 2])
            self.speed = 0.3
            self.color_variation = random.randint(0, 40)
        else:  # Foreground stars
            self.brightness = random.randint(100, 255)
            self.twinkle_speed = random.uniform(0.05, 0.08)
            self.size = random.choice([2, 2, 3])
            self.speed = 0.5
            self.color_variation = random.randint(0, 60)
        
        self.twinkle_phase = random.uniform(0, 2 * math.pi)
        self.original_brightness = self.brightness
    
    def update(self):
        self.twinkle_phase += self.twinkle_speed
        self.brightness = self.original_brightness + int(50 * math.sin(self.twinkle_phase))
        
        # Parallax scrolling effect
        self.x += self.speed
        if self.x > WINDOW_WIDTH:
            self.x = 0
        elif self.x < 0:
            self.x = WINDOW_WIDTH
    
    def draw(self, screen):
        # Enhanced color with layer-based tinting
        if self.layer == 0:  # Blue-tinted background stars
            r = max(0, min(255, self.brightness + self.color_variation))
            g = max(0, min(255, self.brightness))
            b = max(0, min(255, min(255, self.brightness + 40)))
        elif self.layer == 1:  # Neutral middle stars
            r = max(0, min(255, self.brightness + self.color_variation))
            g = max(0, min(255, self.brightness))
            b = max(0, min(255, self.brightness + 20))
        else:  # Slightly red-tinted foreground stars
            r = max(0, min(255, self.brightness + self.color_variation + 10))
            g = max(0, min(255, self.brightness))
            b = max(0, min(255, self.brightness + 10))
        
        color = (r, g, b)
        
        # Add glow for larger stars
        if self.size >= 2:
            glow_size = self.size + 1
            glow_color = tuple(c // 3 for c in color)
            pygame.draw.circle(screen, glow_color, (int(self.x), int(self.y)), glow_size)
        
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.size)

class PowerUp:
    def __init__(self, power_type, position):
        self.type = power_type
        self.position = position
        self.animation_timer = 0
        self.collected = False
        self.spawn_time = pygame.time.get_ticks()
        self.lifespan = 10000  # 10 seconds
        
        self.colors = {
            PowerUpType.SPEED_BOOST: (255, 100, 100),
            PowerUpType.SLOW_MOTION: (100, 100, 255),
            PowerUpType.DOUBLE_POINTS: (255, 215, 0),
            PowerUpType.INVINCIBLE: (255, 255, 100),
            PowerUpType.MAGNET: (255, 100, 255),
            PowerUpType.GHOST: (200, 200, 255)
        }
        
        self.icons = {
            PowerUpType.SPEED_BOOST: "⚡",
            PowerUpType.SLOW_MOTION: "🐌",
            PowerUpType.DOUBLE_POINTS: "💰",
            PowerUpType.INVINCIBLE: "🛡️",
            PowerUpType.MAGNET: "🧲",
            PowerUpType.GHOST: "👻"
        }
    
    def update(self):
        self.animation_timer += 0.1
        return not self.collected and (pygame.time.get_ticks() - self.spawn_time) < self.lifespan
    
    def draw(self, screen):
        if not self.collected:
            x = GAME_AREA_X + self.position[0] * CELL_SIZE + CELL_SIZE // 2
            y = GAME_AREA_Y + self.position[1] * CELL_SIZE + CELL_SIZE // 2
            
            pulse = int(3 * math.sin(self.animation_timer * 2))
            size = CELL_SIZE // 2 + pulse
            
            color = tuple(max(0, min(255, c)) for c in self.colors[self.type])
            
            # Outer glow
            for i in range(3):
                alpha = max(0, 50 - i * 15)
                glow_size = size + i * 5
                glow_color = tuple(max(0, min(255, c - i * 20)) for c in color)
                pygame.draw.circle(screen, glow_color, (int(x), int(y)), glow_size)
            
            # Main circle
            pygame.draw.circle(screen, color, (int(x), int(y)), size)
            pygame.draw.circle(screen, WHITE, (int(x), int(y)), size, 2)
            
            # Inner star
            star_points = []
            for i in range(5):
                angle = self.animation_timer * 50 + i * 72
                outer_x = x + (size * 0.6) * math.cos(math.radians(angle))
                outer_y = y + (size * 0.6) * math.sin(math.radians(angle))
                star_points.append((outer_x, outer_y))
                
                angle = self.animation_timer * 50 + i * 72 + 36
                inner_x = x + (size * 0.3) * math.cos(math.radians(angle))
                inner_y = y + (size * 0.3) * math.sin(math.radians(angle))
                star_points.append((inner_x, inner_y))
            
            if len(star_points) >= 6:
                pygame.draw.polygon(screen, WHITE, star_points)
    
    def create_collection_particles(self):
        x = GAME_AREA_X + self.position[0] * CELL_SIZE + CELL_SIZE // 2
        y = GAME_AREA_Y + self.position[1] * CELL_SIZE + CELL_SIZE // 2
        particles = []
        
        for _ in range(25):
            color = self.colors[self.type]
            particles.append(Particle(x, y, color, "sparkle"))
        
        for _ in range(10):
            particles.append(Particle(x, y, WHITE, "star"))
        
        return particles

class Food:
    def __init__(self):
        self.position = self.generate_position()
        self.animation_timer = 0
        self.glow_timer = 0
        self.food_type = random.choice(["normal", "bonus", "super"])
        
        self.colors = {
            "normal": (255, 100, 100),
            "bonus": (255, 215, 0),
            "super": (255, 100, 255)
        }
        
        self.values = {
            "normal": 10,
            "bonus": 25,
            "super": 50
        }
    
    def generate_position(self):
        while True:
            x = random.randint(0, GRID_SIZE - 1)
            y = random.randint(0, GRID_SIZE - 1)
            return (x, y)
    
    def respawn(self, snake_body, power_up_positions):
        while True:
            x = random.randint(0, GRID_SIZE - 1)
            y = random.randint(0, GRID_SIZE - 1)
            position = (x, y)
            
            if position not in snake_body and position not in power_up_positions:
                self.position = position
                self.food_type = random.choices(
                    ["normal", "bonus", "super"], 
                    weights=[70, 25, 5]
                )[0]
                break
    
    def update(self):
        self.animation_timer += 0.15
        self.glow_timer += 0.08
    
    def get_color(self):
        pulse = int(128 + 127 * math.sin(self.glow_timer))
        base_color = self.colors[self.food_type]
        return tuple(min(255, c + pulse // 2) for c in base_color)
    
    def get_value(self):
        return self.values[self.food_type]

class Snake:
    def __init__(self):
        self.body = deque([(GRID_SIZE // 2, GRID_SIZE // 2)])
        self.direction = (1, 0)
        self.grow = 0
        self.color_timer = 0
        self.trail = deque(maxlen=15)
        
        # Power-up effects
        self.speed_boost = 0
        self.invincible = 0
        self.ghost = 0
        self.magnet = False
        self.double_points = False
        
        self.move_cooldown = 0
    
    def move(self):
        if self.move_cooldown > 0:
            self.move_cooldown -= 1
            return True
        
        head = self.body[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        
        if self.check_collision(new_head) and not self.invincible:
            return False
        
        self.trail.append(head)
        self.body.appendleft(new_head)
        
        if self.grow > 0:
            self.grow -= 1
        else:
            self.body.pop()
        
        # Update power-up durations
        if self.speed_boost > 0:
            self.speed_boost -= 1
            self.move_cooldown = 0 if self.speed_boost % 2 == 0 else 1
        
        if self.invincible > 0:
            self.invincible -= 1
        
        if self.ghost > 0:
            self.ghost -= 1
        
        self.color_timer += 2
        return True
    
    def check_collision(self, position):
        x, y = position
        if x < 0 or x >= GRID_SIZE or y < 0 or y >= GRID_SIZE:
            return True
        
        if self.ghost == 0 and position in self.body:
            return True
        
        return False
    
    def change_direction(self, new_direction):
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.direction = new_direction
    
    def eat_food(self, value):
        if self.double_points:
            value *= 2
        self.grow += value // 10 + 1
    
    def get_segment_color(self, index):
        if self.invincible > 0:
            hue = (self.color_timer * 3 + index * 20) % 360
            return self.hsv_to_rgb(hue, 1.0, 1.0)
        elif self.ghost > 0:
            # For ghost mode, return RGB without alpha, alpha will be handled in drawing
            base_brightness = 100 + int(155 * abs(math.sin(self.color_timer * 0.1 + index * 0.5)))
            brightness = max(0, min(255, base_brightness))
            return (brightness // 2, brightness // 2, brightness)
        else:
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
        
        colors = [
            (v, t, p), (q, v, p), (p, v, t),
            (p, q, v), (t, p, v), (v, p, q)
        ]
        
        r, g, b = colors[i]
        return (max(0, min(255, int(r * 255))), 
                max(0, min(255, int(g * 255))), 
                max(0, min(255, int(b * 255))))
    
    def apply_power_up(self, power_type):
        if power_type == PowerUpType.SPEED_BOOST:
            self.speed_boost = 100
        elif power_type == PowerUpType.SLOW_MOTION:
            self.move_cooldown = 50
        elif power_type == PowerUpType.DOUBLE_POINTS:
            self.double_points = True
        elif power_type == PowerUpType.INVINCIBLE:
            self.invincible = 100
        elif power_type == PowerUpType.MAGNET:
            self.magnet = True
        elif power_type == PowerUpType.GHOST:
            self.ghost = 50

class Button:
    def __init__(self, x, y, width, height, text, font_size=36):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = get_font(font_size)
        self.hovered = False
        self.animation_offset = 0
        self.pulse_timer = 0
    
    def update(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)
        self.pulse_timer += 0.1
    
    def draw(self, screen):
        self.animation_offset = math.sin(self.pulse_timer) * 2 if self.hovered else 0
        
        y_offset = self.rect.y + self.animation_offset
        
        if self.hovered:
            pygame.draw.rect(screen, (100, 100, 150), 
                           (self.rect.x - 2, y_offset - 2, 
                            self.rect.width + 4, self.rect.height + 4), 
                           border_radius=12)
        
        gradient_color = (80 + int(20 * math.sin(self.pulse_timer)), 
                         80 + int(20 * math.sin(self.pulse_timer + 1)), 
                         120 + int(20 * math.sin(self.pulse_timer + 2)))
        
        pygame.draw.rect(screen, gradient_color, 
                        (self.rect.x, y_offset, self.rect.width, self.rect.height), 
                        border_radius=10)
        
        pygame.draw.rect(screen, WHITE, 
                        (self.rect.x, y_offset, self.rect.width, self.rect.height), 
                        2, border_radius=10)
        
        text_color = GOLD if self.hovered else WHITE
        text_surface = self.font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect(center=(self.rect.centerx, y_offset + self.rect.height // 2))
        screen.blit(text_surface, text_rect)
    
    def is_clicked(self, mouse_pos, mouse_click):
        return self.rect.collidepoint(mouse_pos) and mouse_click

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("🌟 极致华丽贪吃蛇 🌟")
        self.clock = pygame.time.Clock()
        
        # Fonts - use Chinese font support
        self.title_font = get_font(72)
        self.large_font = get_font(48)
        self.font = get_font(36)
        self.small_font = get_font(28)
        self.tiny_font = get_font(20)
        
        # Game objects
        self.snake = None
        self.food = None
        self.power_ups = []
        self.particles = []
        self.stars = []
        # Create multi-layer starfield
        for layer in range(3):
            layer_stars = 50 if layer == 0 else 40 if layer == 1 else 30
            self.stars.extend([Star(layer) for _ in range(layer_stars)])
        
        # Game state
        self.state = GameState.MENU
        self.score = 0
        self.high_score = 0
        self.combo = 0
        self.last_food_time = 0
        self.game_timer = 0
        self.shake_amount = 0
        self.difficulty_level = 1
        self.foods_eaten = 0
        
        # Power-up spawn timer
        self.power_up_spawn_timer = 0
        
        # Menu buttons
        self.menu_buttons = [
            Button(WINDOW_WIDTH // 2 - 150, 250, 300, 60, "开始游戏"),
            Button(WINDOW_WIDTH // 2 - 150, 330, 300, 60, "最高分"),
            Button(WINDOW_WIDTH // 2 - 150, 410, 300, 60, "设置"),
            Button(WINDOW_WIDTH // 2 - 150, 490, 300, 60, "退出游戏")
        ]
        
        # Game over buttons
        self.game_over_buttons = [
            Button(WINDOW_WIDTH // 2 - 150, 400, 300, 60, "重新开始"),
            Button(WINDOW_WIDTH // 2 - 150, 480, 300, 60, "返回菜单")
        ]
        
        # Settings buttons
        self.settings_buttons = [
            Button(WINDOW_WIDTH // 2 - 150, 250, 300, 60, "音效: 开启"),
            Button(WINDOW_WIDTH // 2 - 150, 330, 300, 60, "粒子质量: 高"),
            Button(WINDOW_WIDTH // 2 - 150, 410, 300, 60, "游戏速度: 正常"),
            Button(WINDOW_WIDTH // 2 - 150, 490, 300, 60, "返回主菜单")
        ]
        
        # High scores
        self.high_scores = self.load_high_scores()
        
        # Settings
        self.sound_enabled = True
        self.particle_quality = "high"
        self.game_speed_setting = 1  # 0=slow, 1=normal, 2=fast
        
        self.reset_game()
    
    def load_high_scores(self):
        try:
            if os.path.exists("snake_high_scores.json"):
                with open("snake_high_scores.json", "r") as f:
                    return json.load(f)
        except:
            pass
        return [0, 0, 0, 0, 0]
    
    def save_high_scores(self):
        try:
            with open("snake_high_scores.json", "w") as f:
                json.dump(self.high_scores, f)
        except:
            pass
    
    def update_high_scores(self, score):
        self.high_scores.append(score)
        self.high_scores.sort(reverse=True)
        self.high_scores = self.high_scores[:5]
        self.save_high_scores()
    
    def reset_game(self):
        self.snake = Snake()
        self.food = Food()
        self.power_ups.clear()
        self.particles.clear()
        self.score = 0
        self.combo = 0
        self.last_food_time = 0
        self.game_timer = 0
        self.shake_amount = 0
        self.foods_eaten = 0
        self.power_up_spawn_timer = 0
    
    def handle_events(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if self.state == GameState.PLAYING:
                    if event.key == pygame.K_UP:
                        self.snake.change_direction((0, -1))
                    elif event.key == pygame.K_DOWN:
                        self.snake.change_direction((0, 1))
                    elif event.key == pygame.K_LEFT:
                        self.snake.change_direction((-1, 0))
                    elif event.key == pygame.K_RIGHT:
                        self.snake.change_direction((1, 0))
                    elif event.key == pygame.K_p:
                        self.state = GameState.PAUSED
                    elif event.key == pygame.K_ESCAPE:
                        self.state = GameState.MENU
                
                elif self.state == GameState.PAUSED:
                    if event.key == pygame.K_p:
                        self.state = GameState.PLAYING
                    elif event.key == pygame.K_ESCAPE:
                        self.state = GameState.MENU
                
                elif self.state == GameState.MENU:
                    if event.key == pygame.K_ESCAPE:
                        return False
                
                elif self.state in [GameState.GAME_OVER, GameState.HIGH_SCORES]:
                    if event.key == pygame.K_ESCAPE:
                        self.state = GameState.MENU
                
                elif self.state == GameState.SETTINGS:
                    if event.key == pygame.K_ESCAPE:
                        self.state = GameState.MENU
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_click = True
        
        if self.state == GameState.MENU:
            if self.menu_buttons[0].is_clicked(mouse_pos, mouse_click):
                self.reset_game()
                self.state = GameState.PLAYING
            elif self.menu_buttons[1].is_clicked(mouse_pos, mouse_click):
                self.state = GameState.HIGH_SCORES
            elif self.menu_buttons[2].is_clicked(mouse_pos, mouse_click):
                self.state = GameState.SETTINGS
            elif self.menu_buttons[3].is_clicked(mouse_pos, mouse_click):
                return False
        
        elif self.state == GameState.GAME_OVER:
            if self.game_over_buttons[0].is_clicked(mouse_pos, mouse_click):
                self.reset_game()
                self.state = GameState.PLAYING
            elif self.game_over_buttons[1].is_clicked(mouse_pos, mouse_click):
                self.state = GameState.MENU
        

            
            # Handle settings button clicks
            if self.settings_buttons[0].is_clicked(mouse_pos, mouse_click):
                self.sound_enabled = not self.sound_enabled
                sound_text = "音效: 开启" if self.sound_enabled else "音效: 关闭"
                self.settings_buttons[0] = Button(WINDOW_WIDTH // 2 - 150, 250, 300, 60, sound_text)
            
            elif self.settings_buttons[1].is_clicked(mouse_pos, mouse_click):
                qualities = ["高", "中", "低"]
                current_idx = qualities.index(self.particle_quality)
                next_idx = (current_idx + 1) % len(qualities)
                self.particle_quality = qualities[next_idx]
                self.settings_buttons[1] = Button(WINDOW_WIDTH // 2 - 150, 330, 300, 60, f"粒子质量: {self.particle_quality}")
            
            elif self.settings_buttons[2].is_clicked(mouse_pos, mouse_click):
                speeds = ["慢", "正常", "快"]
                # Find current speed based on a base_speed setting
                base_speed = getattr(self, 'game_speed_setting', 1)  # 0=slow, 1=normal, 2=fast
                next_speed = (base_speed + 1) % len(speeds)
                self.game_speed_setting = next_speed
                self.settings_buttons[2] = Button(WINDOW_WIDTH // 2 - 150, 410, 300, 60, f"游戏速度: {speeds[next_speed]}")
            
            elif self.settings_buttons[3].is_clicked(mouse_pos, mouse_click):
                self.state = GameState.MENU
        
        for button in self.menu_buttons + self.game_over_buttons + self.settings_buttons:
            button.update(mouse_pos)
        
        return True
    
    def create_food_particles(self, x, y, food_type):
        colors = {
            "normal": [(255, 100, 100), (255, 150, 150), (255, 200, 100)],
            "bonus": [(255, 215, 0), (255, 255, 100), (255, 200, 50)],
            "super": [(255, 100, 255), (255, 200, 255), (200, 100, 255)]
        }
        
        food_colors = colors.get(food_type, colors["normal"])
        particle_count = {"normal": 30, "bonus": 45, "super": 60}[food_type]
        
        # Create enhanced particle effects based on food type
        for _ in range(particle_count):
            color = random.choice(food_colors)
            
            # Different particle types for different foods
            if food_type == "normal":
                particle_types = ["normal", "sparkle", "star", "energy"]
                weights = [0.4, 0.3, 0.2, 0.1]
            elif food_type == "bonus":
                particle_types = ["sparkle", "star", "energy", "magic"]
                weights = [0.3, 0.3, 0.2, 0.2]
            else:  # super
                particle_types = ["star", "energy", "magic", "rainbow", "explosion"]
                weights = [0.2, 0.2, 0.2, 0.2, 0.2]
            
            particle_type = random.choices(particle_types, weights=weights)[0]
            
            self.particles.append(Particle(
                GAME_AREA_X + x * CELL_SIZE + CELL_SIZE // 2,
                GAME_AREA_Y + y * CELL_SIZE + CELL_SIZE // 2,
                color, particle_type
            ))
        
        # Add special explosion effect for super food
        if food_type == "super":
            for _ in range(20):
                explosion_color = random.choice([(255, 255, 255), (255, 200, 0), (255, 100, 100)])
                self.particles.append(Particle(
                    GAME_AREA_X + x * CELL_SIZE + CELL_SIZE // 2,
                    GAME_AREA_Y + y * CELL_SIZE + CELL_SIZE // 2,
                    explosion_color, "explosion"
                ))
    
    def spawn_power_up(self):
        if len(self.power_ups) < 3 and random.random() < 0.3:
            power_type = random.choice(list(PowerUpType))
            position = self.food.generate_position()
            
            occupied = [self.food.position] + [p.position for p in self.power_ups]
            occupied += list(self.snake.body)
            
            if position not in occupied:
                self.power_ups.append(PowerUp(power_type, position))
    
    def update(self):
        if self.state == GameState.PLAYING:
            self.game_timer += 1
            
            # Update difficulty
            self.difficulty_level = 1 + (self.score // 200)
            
            # Spawn power-ups
            self.power_up_spawn_timer += 1
            if self.power_up_spawn_timer > 300 - (self.difficulty_level * 20):
                self.spawn_power_up()
                self.power_up_spawn_timer = 0
            
            # Update game objects
            self.food.update()
            
            for power_up in self.power_ups[:]:
                if not power_up.update():
                    self.power_ups.remove(power_up)
            
            # Magnet effect
            if self.snake.magnet:
                head = self.snake.body[0]
                for power_up in self.power_ups:
                    dist = abs(power_up.position[0] - head[0]) + abs(power_up.position[1] - head[1])
                    if dist < 5:
                        dx = 1 if head[0] > power_up.position[0] else -1 if head[0] < power_up.position[0] else 0
                        dy = 1 if head[1] > power_up.position[1] else -1 if head[1] < power_up.position[1] else 0
                        new_pos = (power_up.position[0] + dx, power_up.position[1] + dy)
                        
                        if new_pos not in self.snake.body and new_pos != self.food.position:
                            power_up.position = new_pos
            
            # Move snake
            game_speed = 12 + (self.difficulty_level * 2)
            if self.game_timer % max(1, game_speed - (self.snake.speed_boost // 10)) == 0:
                if not self.snake.move():
                    self.state = GameState.GAME_OVER
                    self.create_explosion()
                    self.shake_amount = 25
                    self.update_high_scores(self.score)
                    if self.score > self.high_score:
                        self.high_score = self.score
            
            # Check food collision
            if self.snake.body[0] == self.food.position:
                food_value = self.food.get_value()
                self.snake.eat_food(food_value)
                
                current_time = pygame.time.get_ticks()
                if current_time - self.last_food_time < 2000:
                    self.combo += 1
                else:
                    self.combo = 1
                
                self.last_food_time = current_time
                bonus_score = food_value * self.combo
                self.score += bonus_score
                
                food_x, food_y = self.food.position
                self.create_food_particles(food_x, food_y, self.food.food_type)
                self.shake_amount = min(8, 2 + self.combo)
                
                power_up_positions = [p.position for p in self.power_ups]
                self.food.respawn(self.snake.body, power_up_positions)
                self.foods_eaten += 1
            
            # Check power-up collision
            for power_up in self.power_ups[:]:
                if self.snake.body[0] == power_up.position:
                    self.snake.apply_power_up(power_up.type)
                    self.particles.extend(power_up.create_collection_particles())
                    self.power_ups.remove(power_up)
                    self.score += 50
                    self.shake_amount = 5
        
        # Update visual effects
        for star in self.stars:
            star.update()
        
        if self.shake_amount > 0:
            self.shake_amount -= 1
        
        self.particles = [p for p in self.particles if p.update()]
    
    def create_explosion(self):
        head = self.snake.body[0]
        x = GAME_AREA_X + head[0] * CELL_SIZE + CELL_SIZE // 2
        y = GAME_AREA_Y + head[1] * CELL_SIZE + CELL_SIZE // 2
        
        for _ in range(80):
            color = random.choice([(255, 100, 100), (255, 200, 100), (255, 255, 100)])
            particle_type = random.choice(["normal", "sparkle", "star"])
            self.particles.append(Particle(x, y, color, particle_type))
    
    def draw_gradient_background(self):
        # Enhanced animated gradient background
        time_offset = self.game_timer * 0.001
        
        for y in range(0, WINDOW_HEIGHT, 2):  # Draw every 2 lines for performance
            progress = y / WINDOW_HEIGHT
            
            # Animated gradient colors
            r = int(10 + 25 * progress + 5 * math.sin(time_offset + progress * 3))
            g = int(0 + 10 * progress + 3 * math.sin(time_offset * 1.5 + progress * 2))
            b = int(30 + 40 * progress + 7 * math.sin(time_offset * 2 + progress * 4))
            
            # Clamp values
            r = max(0, min(255, r))
            g = max(0, min(255, g))
            b = max(0, min(255, b))
            
            color = (r, g, b)
            pygame.draw.line(self.screen, color, (0, y), (WINDOW_WIDTH, y))
    
    def draw_starfield(self):
        for star in self.stars:
            star.draw(self.screen)
    
    def draw_game_area(self):
        shake_x = random.randint(-self.shake_amount, self.shake_amount) if self.shake_amount > 0 else 0
        shake_y = random.randint(-self.shake_amount, self.shake_amount) if self.shake_amount > 0 else 0
        
        game_surface = pygame.Surface((GAME_AREA_WIDTH, GAME_AREA_HEIGHT))
        game_surface.fill(DARK_BLACK)
        
        # Draw grid
        for i in range(GRID_SIZE + 1):
            color = (30, 30, 40) if i % 5 == 0 else (20, 20, 30)
            pygame.draw.line(game_surface, color, 
                           (i * CELL_SIZE, 0), 
                           (i * CELL_SIZE, GAME_AREA_HEIGHT), 1)
            pygame.draw.line(game_surface, color, 
                           (0, i * CELL_SIZE), 
                           (GAME_AREA_WIDTH, i * CELL_SIZE), 1)
        
        # Draw snake
        for i, segment in enumerate(self.snake.body):
            x = segment[0] * CELL_SIZE
            y = segment[1] * CELL_SIZE
            
            color = self.snake.get_segment_color(i)
            
            if i == 0:
                # Head with special effects
                if self.snake.invincible > 0:
                    glow_size = CELL_SIZE + int(8 * math.sin(self.game_timer * 0.2))
                    glow_color = (*color, 100)
                    pygame.draw.rect(game_surface, glow_color, 
                                   (x - (glow_size - CELL_SIZE) // 2, 
                                    y - (glow_size - CELL_SIZE) // 2, 
                                    glow_size, glow_size), border_radius=15)
                
                pygame.draw.rect(game_surface, color, 
                               (x + 2, y + 2, CELL_SIZE - 4, CELL_SIZE - 4), 
                               border_radius=12)
                
                # Eyes
                eye_size = 4
                eye_offset = 6
                if self.snake.direction == (1, 0):  # Right
                    pygame.draw.circle(game_surface, WHITE, (x + CELL_SIZE - eye_offset, y + eye_offset), eye_size)
                    pygame.draw.circle(game_surface, WHITE, (x + CELL_SIZE - eye_offset, y + CELL_SIZE - eye_offset), eye_size)
                elif self.snake.direction == (-1, 0):  # Left
                    pygame.draw.circle(game_surface, WHITE, (x + eye_offset, y + eye_offset), eye_size)
                    pygame.draw.circle(game_surface, WHITE, (x + eye_offset, y + CELL_SIZE - eye_offset), eye_size)
                elif self.snake.direction == (0, -1):  # Up
                    pygame.draw.circle(game_surface, WHITE, (x + eye_offset, y + eye_offset), eye_size)
                    pygame.draw.circle(game_surface, WHITE, (x + CELL_SIZE - eye_offset, y + eye_offset), eye_size)
                else:  # Down
                    pygame.draw.circle(game_surface, WHITE, (x + eye_offset, y + CELL_SIZE - eye_offset), eye_size)
                    pygame.draw.circle(game_surface, WHITE, (x + CELL_SIZE - eye_offset, y + CELL_SIZE - eye_offset), eye_size)
            else:
                # Body segments
                size = CELL_SIZE - 4 - (i * 0.2)
                if self.snake.ghost > 0:
                    size = int(size * 0.7)
                
                pygame.draw.rect(game_surface, color, 
                               (x + (CELL_SIZE - size) // 2, 
                                y + (CELL_SIZE - size) // 2, 
                                size, size), border_radius=6)
        
        # Draw power-ups
        for power_up in self.power_ups:
            power_up.draw(game_surface)
        
        # Draw food
        food_x, food_y = self.food.position
        food_color = self.food.get_color()
        
        pulse = int(4 * math.sin(self.food.animation_timer))
        food_size = CELL_SIZE - 6 + pulse
        
        # Food glow
        if self.food.food_type == "super":
            for i in range(3):
                glow_size = food_size + i * 8
                glow_alpha = 60 - i * 20
                glow_color = (*food_color, glow_alpha)
                pygame.draw.circle(game_surface, glow_color[:3],
                                 (food_x * CELL_SIZE + CELL_SIZE // 2,
                                  food_y * CELL_SIZE + CELL_SIZE // 2),
                                 glow_size)
        
        pygame.draw.circle(game_surface, food_color, 
                         (food_x * CELL_SIZE + CELL_SIZE // 2,
                          food_y * CELL_SIZE + CELL_SIZE // 2),
                         food_size)
        
        # Food shine
        shine_offset = food_size // 3
        pygame.draw.circle(game_surface, WHITE,
                         (food_x * CELL_SIZE + CELL_SIZE // 2 - shine_offset,
                          food_y * CELL_SIZE + CELL_SIZE // 2 - shine_offset),
                         food_size // 4)
        
        self.screen.blit(game_surface, (GAME_AREA_X + shake_x, GAME_AREA_Y + shake_y))
        
        # Draw border
        border_color = (100, 100, 150) if self.snake.invincible > 0 else (80, 80, 120)
        pygame.draw.rect(self.screen, border_color, 
                        (GAME_AREA_X + shake_x, GAME_AREA_Y + shake_y, 
                         GAME_AREA_WIDTH, GAME_AREA_HEIGHT), 3)
    
    def draw_ui(self):
        # Score panel
        panel_surface = pygame.Surface((200, 150))
        panel_surface.set_alpha(200)
        panel_surface.fill((20, 20, 40))
        self.screen.blit(panel_surface, (10, 10))
        
        score_text = self.font.render(f"得分: {self.score}", True, WHITE)
        self.screen.blit(score_text, (20, 20))
        
        high_score_text = self.small_font.render(f"最高: {self.high_score}", True, GOLD)
        self.screen.blit(high_score_text, (20, 60))
        
        level_text = self.small_font.render(f"等级: {self.difficulty_level}", True, (200, 200, 255))
        self.screen.blit(level_text, (20, 90))
        
        foods_text = self.small_font.render(f"食物: {self.foods_eaten}", True, (150, 255, 150))
        self.screen.blit(foods_text, (20, 120))
        
        # Combo indicator
        if self.combo > 1:
            combo_size = 36 + self.combo * 2
            combo_font = get_font(combo_size)
            combo_text = combo_font.render(f"连击 x{self.combo}!", True, (255, 200, 0))
            combo_rect = combo_text.get_rect(center=(WINDOW_WIDTH // 2, 100))
            self.screen.blit(combo_text, combo_rect)
        
        # Power-ups status panel
        if any([self.snake.speed_boost, self.snake.invincible, self.snake.ghost, 
                self.snake.magnet, self.snake.double_points]):
            power_panel = pygame.Surface((200, 120))
            power_panel.set_alpha(200)
            power_panel.fill((30, 20, 40))
            self.screen.blit(power_panel, (WINDOW_WIDTH - 210, 10))
            
            y_offset = 20
            if self.snake.speed_boost > 0:
                text = self.tiny_font.render(f"⚡ 加速: {self.snake.speed_boost // 10}s", True, (255, 100, 100))
                self.screen.blit(text, (WINDOW_WIDTH - 200, y_offset))
                y_offset += 20
            
            if self.snake.invincible > 0:
                text = self.tiny_font.render(f"🛡️ 无敌: {self.snake.invincible // 10}s", True, (255, 255, 100))
                self.screen.blit(text, (WINDOW_WIDTH - 200, y_offset))
                y_offset += 20
            
            if self.snake.ghost > 0:
                text = self.tiny_font.render(f"👻 幽灵: {self.snake.ghost // 10}s", True, (200, 200, 255))
                self.screen.blit(text, (WINDOW_WIDTH - 200, y_offset))
                y_offset += 20
            
            if self.snake.magnet:
                text = self.tiny_font.render(f"🧲 磁铁: 激活", True, (255, 100, 255))
                self.screen.blit(text, (WINDOW_WIDTH - 200, y_offset))
                y_offset += 20
            
            if self.snake.double_points:
                text = self.tiny_font.render(f"💰 双倍: 激活", True, (255, 215, 0))
                self.screen.blit(text, (WINDOW_WIDTH - 200, y_offset))
        
        # Controls help
        controls = [
            "方向键: 移动",
            "P: 暂停",
            "ESC: 菜单"
        ]
        
        for i, control in enumerate(controls):
            text = self.tiny_font.render(control, True, (120, 120, 140))
            self.screen.blit(text, (WINDOW_WIDTH - 120, WINDOW_HEIGHT - 80 + i * 25))
    
    def draw_menu(self):
        title_text = self.title_font.render("🌟 极致贪吃蛇 🌟", True, GOLD)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 120))
        
        # Add glow effect to title
        for i in range(3):
            glow_surface = pygame.Surface((title_rect.width + i * 10, title_rect.height + i * 10))
            glow_surface.set_alpha(50 - i * 15)
            glow_surface.fill((255, 215, 0))
            self.screen.blit(glow_surface, 
                           (title_rect.x - i * 5, title_rect.y - i * 5))
        
        self.screen.blit(title_text, title_rect)
        
        subtitle_text = self.small_font.render("按空格键快速开始", True, (200, 200, 200))
        subtitle_rect = subtitle_text.get_rect(center=(WINDOW_WIDTH // 2, 180))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        for button in self.menu_buttons:
            button.draw(self.screen)
    
    def draw_high_scores(self):
        title_text = self.large_font.render("🏆 最高分 🏆", True, GOLD)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 100))
        self.screen.blit(title_text, title_rect)
        
        medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"]
        
        for i, score in enumerate(self.high_scores):
            y_pos = 200 + i * 60
            color = [GOLD, SILVER, BRONZE, WHITE, WHITE][i]
            
            medal_text = self.font.render(f"{medals[i]}", True, color)
            self.screen.blit(medal_text, (WINDOW_WIDTH // 2 - 150, y_pos))
            
            score_text = self.font.render(f"{score:,} 分", True, WHITE)
            score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2 + 50, y_pos + 15))
            self.screen.blit(score_text, score_rect)
        
        back_text = self.small_font.render("按 ESC 返回菜单", True, (200, 200, 200))
        back_rect = back_text.get_rect(center=(WINDOW_WIDTH // 2, 550))
        self.screen.blit(back_text, back_rect)
    
    def draw_game_over(self):
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        if self.score == self.high_score and self.score > 0:
            title_text = self.title_font.render("🎉 新纪录! 🎉", True, GOLD)
        else:
            title_text = self.title_font.render("游戏结束", True, (255, 100, 100))
        
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 150))
        self.screen.blit(title_text, title_rect)
        
        score_text = self.large_font.render(f"最终得分: {self.score:,}", True, WHITE)
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 80))
        self.screen.blit(score_text, score_rect)
        
        stats = [
            f"达到等级: {self.difficulty_level}",
            f"吃掉食物: {self.foods_eaten}",
            f"最高分: {self.high_score:,}"
        ]
        
        for i, stat in enumerate(stats):
            stat_text = self.small_font.render(stat, True, (200, 200, 200))
            stat_rect = stat_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 20 + i * 30))
            self.screen.blit(stat_text, stat_rect)
        
        for button in self.game_over_buttons:
            button.draw(self.screen)
    
    def draw_pause(self):
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(150)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        pause_text = self.title_font.render("暂停", True, WHITE)
        pause_rect = pause_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
        self.screen.blit(pause_text, pause_rect)
        
        continue_text = self.font.render("按 P 继续游戏", True, WHITE)
        continue_rect = continue_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20))
        self.screen.blit(continue_text, continue_rect)
        
        menu_text = self.small_font.render("按 ESC 返回菜单", True, (200, 200, 200))
        menu_rect = menu_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 60))
        self.screen.blit(menu_text, menu_rect)
    
    def draw_settings(self):
        title_text = self.large_font.render("游戏设置", True, WHITE)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 150))
        self.screen.blit(title_text, title_rect)
        
        # Draw settings buttons
        for button in self.settings_buttons:
            button.draw(self.screen)
        
        # Settings description
        descriptions = [
            "开启/关闭游戏音效",
            "调整粒子效果质量",
            "设置游戏基础速度",
            "返回主菜单"
        ]
        
        for i, desc in enumerate(descriptions):
            desc_text = self.small_font.render(desc, True, (150, 150, 150))
            desc_rect = desc_text.get_rect(center=(WINDOW_WIDTH // 2, 290 + i * 80))
            self.screen.blit(desc_text, desc_rect)
        
        back_text = self.small_font.render("按 ESC 返回主菜单", True, (200, 200, 200))
        back_rect = back_text.get_rect(center=(WINDOW_WIDTH // 2, 580))
        self.screen.blit(back_text, back_rect)
    
    def draw(self):
        self.draw_gradient_background()
        self.draw_starfield()
        
        if self.state == GameState.MENU:
            self.draw_menu()
        elif self.state in [GameState.PLAYING, GameState.PAUSED]:
            self.draw_game_area()
            self.draw_particles()
            self.draw_ui()
            
            if self.state == GameState.PAUSED:
                self.draw_pause()
        
        elif self.state == GameState.GAME_OVER:
            self.draw_game_area()
            self.draw_particles()
            self.draw_game_over()
        
        elif self.state == GameState.HIGH_SCORES:
            self.draw_high_scores()
        
        elif self.state == GameState.SETTINGS:
            self.draw_settings()
        
        pygame.display.flip()
    
    def draw_particles(self):
        for particle in self.particles:
            particle.draw(self.screen)
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()