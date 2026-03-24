import pygame
import random
import math
import numpy as np
from collections import deque
from enum import Enum
import json
from datetime import datetime, timedelta

pygame.init()

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
GRID_SIZE = 30
CELL_SIZE = 20
BOARD_WIDTH = GRID_SIZE * CELL_SIZE
BOARD_HEIGHT = GRID_SIZE * CELL_SIZE
BOARD_X = 50
BOARD_Y = 100

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
DARK_GREEN = (0, 150, 0)
GOLD = (255, 215, 0)

class MarketCondition(Enum):
    BULL = "bull"
    BEAR = "bear"
    SIDEWAYS = "sideways"
    VOLATILE = "volatile"

class TradingState(Enum):
    MENU = "menu"
    TRADING = "trading"
    PAUSED = "paused"
    GAME_OVER = "game_over"
    ANALYSIS = "analysis"
    SETTINGS = "settings"

class MarketData:
    def __init__(self):
        self.prices = []
        self.volume = []
        self.volatility = 0
        self.trend = 0
        self.condition = MarketCondition.SIDEWAYS
        self.indicators = {}
        self.generate_initial_data()
    
    def generate_initial_data(self):
        base_price = 100
        for i in range(100):
            change = random.gauss(0, 0.02)
            base_price *= (1 + change)
            self.prices.append(base_price)
            self.volume.append(random.randint(1000, 10000))
        
        self.update_indicators()
    
    def update(self):
        if len(self.prices) > 0:
            last_price = self.prices[-1]
            change = random.gauss(self.trend * 0.01, self.volatility * 0.05)
            new_price = last_price * (1 + change)
            
            self.prices.append(new_price)
            self.volume.append(random.randint(1000, 10000))
            
            if len(self.prices) > 200:
                self.prices.pop(0)
                self.volume.pop(0)
            
            self.update_indicators()
            self.update_market_condition()
    
    def update_indicators(self):
        if len(self.prices) < 20:
            return
        
        # Moving averages
        prices_array = np.array(self.prices)
        self.indicators['ma20'] = np.mean(prices_array[-20:])
        self.indicators['ma50'] = np.mean(prices_array[-50:]) if len(prices_array) >= 50 else self.indicators['ma20']
        
        # RSI
        if len(self.prices) >= 14:
            deltas = np.diff(prices_array[-15:])
            gains = np.where(deltas > 0, deltas, 0)
            losses = np.where(deltas < 0, -deltas, 0)
            avg_gain = np.mean(gains)
            avg_loss = np.mean(losses)
            
            if avg_loss > 0:
                rs = avg_gain / avg_loss
                self.indicators['rsi'] = 100 - (100 / (1 + rs))
            else:
                self.indicators['rsi'] = 100
        
        # Volatility
        if len(self.prices) >= 20:
            returns = np.diff(np.log(prices_array[-21:]))
            self.volatility = np.std(returns) * math.sqrt(252)
        
        # Trend
        if len(self.prices) >= 10:
            recent_trend = (prices_array[-1] - prices_array[-10]) / prices_array[-10]
            self.trend = recent_trend
    
    def update_market_condition(self):
        if self.volatility > 0.3:
            self.condition = MarketCondition.VOLATILE
        elif self.trend > 0.02:
            self.condition = MarketCondition.BULL
        elif self.trend < -0.02:
            self.condition = MarketCondition.BEAR
        else:
            self.condition = MarketCondition.SIDEWAYS

class TradingOpportunity:
    def __init__(self, x, y, opportunity_type):
        self.x = x
        self.y = y
        self.type = opportunity_type
        self.value = self.calculate_value()
        self.risk = self.calculate_risk()
        self.lifetime = random.randint(100, 300)
        self.age = 0
        
        self.colors = {
            'profit': (0, 255, 0),
            'loss': (255, 0, 0),
            'breakout': (255, 165, 0),
            'reversal': (255, 0, 255),
            'scalp': (0, 255, 255),
            'swing': (128, 0, 128)
        }
    
    def calculate_value(self):
        values = {
            'profit': random.randint(10, 50),
            'loss': random.randint(-30, -10),
            'breakout': random.randint(20, 80),
            'reversal': random.randint(30, 100),
            'scalp': random.randint(5, 25),
            'swing': random.randint(40, 120)
        }
        return values.get(self.type, 10)
    
    def calculate_risk(self):
        risks = {
            'profit': 0.3,
            'loss': 0.8,
            'breakout': 0.6,
            'reversal': 0.7,
            'scalp': 0.2,
            'swing': 0.5
        }
        return risks.get(self.type, 0.5)
    
    def update(self):
        self.age += 1
        return self.age < self.lifetime
    
    def draw(self, screen, font):
        color = self.colors[self.type]
        
        # Pulsing effect based on age
        pulse = 1 + 0.3 * math.sin(self.age * 0.1)
        size = int(CELL_SIZE // 2 * pulse)
        
        # Draw opportunity
        pos_x = BOARD_X + self.x * CELL_SIZE + CELL_SIZE // 2
        pos_y = BOARD_Y + self.y * CELL_SIZE + CELL_SIZE // 2
        
        # Glow effect
        for i in range(3):
            glow_size = size + i * 3
            glow_alpha = 100 - i * 30
            glow_color = (*color, glow_alpha) if len(color) == 3 else color
            pygame.draw.circle(screen, glow_color[:3], (pos_x, pos_y), glow_size)
        
        # Main circle
        pygame.draw.circle(screen, color, (pos_x, pos_y), size)
        
        # Icon
        icons = {
            'profit': '$',
            'loss': 'L',
            'breakout': 'B',
            'reversal': 'R',
            'scalp': 'S',
            'swing': 'W'
        }
        
        icon_text = font.render(icons[self.type], True, WHITE)
        icon_rect = icon_text.get_rect(center=(pos_x, pos_y))
        screen.blit(icon_text, icon_rect)

class TeleportEffect:
    """传送特效类"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.particles = []
        self.lifetime = 30
        self.age = 0
        
        # 创建粒子效果
        for _ in range(20):
            self.particles.append({
                'x': x * CELL_SIZE + CELL_SIZE // 2,
                'y': y * CELL_SIZE + CELL_SIZE // 2,
                'vx': random.uniform(-5, 5),
                'vy': random.uniform(-5, 5),
                'life': random.randint(15, 30),
                'color': random.choice([PURPLE, BLUE, WHITE])
            })
    
    def update(self):
        self.age += 1
        for particle in self.particles:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['life'] -= 1
            particle['vx'] *= 0.9
            particle['vy'] *= 0.9
        
        self.particles = [p for p in self.particles if p['life'] > 0]
        return self.age < self.lifetime
    
    def draw(self, screen):
        # 在屏幕上绘制粒子
        for particle in self.particles:
            alpha = particle['life'] / 30.0
            size = int(3 * alpha)
            if size > 0:
                pos_x = BOARD_X + particle['x']
                pos_y = BOARD_Y + particle['y']
                pygame.draw.circle(screen, particle['color'], 
                                 (int(pos_x), int(pos_y)), size)

class TradingSnake:
    def __init__(self):
        self.body = deque([(GRID_SIZE // 2, GRID_SIZE // 2)])
        self.direction = (1, 0)
        self.grow_count = 0
        self.capital = 100000  # $100,000 starting capital
        self.position_size = 1000  # $1,000 per position
        self.total_pnl = 0
        self.win_rate = 0
        self.trades_taken = 0
        self.winning_trades = 0
        self.max_drawdown = 0
        self.peak_capital = self.capital
        self.risk_score = 0
        self.strategy = "momentum"
        
    def move(self):
        head = self.body[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        
        # Check boundaries - teleport to random position
        if (new_head[0] < 0 or new_head[0] >= GRID_SIZE or 
            new_head[1] < 0 or new_head[1] >= GRID_SIZE):
            return self.teleport_to_random_position()  # Will be updated in game class
        
        # Check self collision - teleport to random position
        if new_head in list(self.body)[:-1]:
            return self.teleport_to_random_position()  # Will be updated in game class
        
        self.body.appendleft(new_head)
        
        if self.grow_count > 0:
            self.grow_count -= 1
        else:
            self.body.pop()
        
        return True
    
    def teleport_to_random_position(self, game_instance=None):
        """随机传送到游戏场地中的任意位置"""
        # 记录旧位置用于创建特效
        old_pos = self.body[0]
        
        # 获取所有可能的空位置
        empty_positions = []
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                if (x, y) not in self.body:
                    empty_positions.append((x, y))
        
        # 如果有空位置，随机选择一个
        if empty_positions:
            random_pos = random.choice(empty_positions)
            
            # 在旧位置创建传送特效
            if game_instance:
                game_instance.teleport_effects.append(
                    TeleportEffect(old_pos[0], old_pos[1])
                )
                # 在新位置也创建特效
                game_instance.teleport_effects.append(
                    TeleportEffect(random_pos[0], random_pos[1])
                )
            
            # 将蛇头传送到新位置，保持蛇身长度不变
            self.body = deque([random_pos] + list(self.body)[:min(len(self.body)-1, 5)])
            
            # 碰墙惩罚：减少一些长度和资本
            self.capital = max(10000, self.capital - 1000)  # 最少保留$10,000
            if len(self.body) > 3:
                # 移除尾部几段作为惩罚
                for _ in range(min(3, len(self.body) - 2)):
                    if len(self.body) > 2:
                        self.body.pop()
            
            return True
        else:
            return False
    
    def change_direction(self, new_direction):
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.direction = new_direction
    
    def take_opportunity(self, opportunity):
        # Calculate P&L based on opportunity value and risk
        pnl = opportunity.value * self.position_size / 1000
        
        # Apply risk management
        if opportunity.risk > 0.5:
            # Reduce position size for high-risk trades
            pnl *= 0.7
        elif opportunity.risk < 0.3:
            # Increase position size for low-risk trades
            pnl *= 1.2
        
        self.capital += pnl
        self.total_pnl += pnl
        self.trades_taken += 1
        
        if pnl > 0:
            self.winning_trades += 1
            self.grow_count = 3  # Grow snake for winning trades
        else:
            self.grow_count = max(0, self.grow_count - 1)  # Shrink for losing trades
        
        # Update statistics
        self.win_rate = self.winning_trades / self.trades_taken if self.trades_taken > 0 else 0
        
        # Update drawdown
        if self.capital > self.peak_capital:
            self.peak_capital = self.capital
        
        current_drawdown = (self.peak_capital - self.capital) / self.peak_capital
        self.max_drawdown = max(self.max_drawdown, current_drawdown)
        
        # Update risk score
        self.update_risk_score()
    
    def update_risk_score(self):
        # Risk score based on multiple factors
        size_risk = min(1.0, self.position_size / (self.capital * 0.1))
        drawdown_risk = min(1.0, self.max_drawdown * 2)
        concentration_risk = min(1.0, len(self.body) / GRID_SIZE)
        
        self.risk_score = (size_risk + drawdown_risk + concentration_risk) / 3
    
    def draw(self, screen, font):
        # Draw snake with gradient based on performance
        for i, segment in enumerate(self.body):
            x = BOARD_X + segment[0] * CELL_SIZE
            y = BOARD_Y + segment[1] * CELL_SIZE
            
            # Color based on P&L performance
            if self.total_pnl > 0:
                color_intensity = min(255, 100 + int(155 * (self.total_pnl / 10000)))
                color = (0, color_intensity, 0)
            else:
                color_intensity = min(255, 100 + int(155 * (-self.total_pnl / 10000)))
                color = (color_intensity, 0, 0)
            
            # Head is special
            if i == 0:
                pygame.draw.rect(screen, color, (x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2))
                
                # Draw eyes
                eye_size = 3
                if self.direction == (1, 0):  # Right
                    pygame.draw.circle(screen, WHITE, (x + CELL_SIZE - 5, y + 5), eye_size)
                    pygame.draw.circle(screen, WHITE, (x + CELL_SIZE - 5, y + CELL_SIZE - 5), eye_size)
                elif self.direction == (-1, 0):  # Left
                    pygame.draw.circle(screen, WHITE, (x + 5, y + 5), eye_size)
                    pygame.draw.circle(screen, WHITE, (x + 5, y + CELL_SIZE - 5), eye_size)
                elif self.direction == (0, -1):  # Up
                    pygame.draw.circle(screen, WHITE, (x + 5, y + 5), eye_size)
                    pygame.draw.circle(screen, WHITE, (x + CELL_SIZE - 5, y + 5), eye_size)
                else:  # Down
                    pygame.draw.circle(screen, WHITE, (x + 5, y + CELL_SIZE - 5), eye_size)
                    pygame.draw.circle(screen, WHITE, (x + CELL_SIZE - 5, y + CELL_SIZE - 5), eye_size)
            else:
                size = CELL_SIZE - 4 - (i * 0.1)
                offset = (CELL_SIZE - size) // 2
                pygame.draw.rect(screen, color, (x + offset, y + offset, size, size))

class QuantTradingGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("量化交易贪吃蛇系统 - Quant Trading Snake")
        self.clock = pygame.time.Clock()
        
        # Fonts - 加载中文字体
        try:
            self.font_large = pygame.font.Font("C:/Windows/Fonts/simhei.ttf", 36)
            self.font_medium = pygame.font.Font("C:/Windows/Fonts/simhei.ttf", 24)
            self.font_small = pygame.font.Font("C:/Windows/Fonts/simhei.ttf", 18)
            self.menu_font = pygame.font.Font("C:/Windows/Fonts/simhei.ttf", 28)
        except:
            self.font_large = pygame.font.Font(None, 36)
            self.font_medium = pygame.font.Font(None, 24)
            self.font_small = pygame.font.Font(None, 18)
            self.menu_font = pygame.font.Font(None, 28)
        
        # Menu buttons
        self.menu_buttons = []
        self.selected_button = 0
        
        # Initialize menu buttons
        self.create_menu_buttons()
        
        # Game objects
        self.snake = TradingSnake()
        self.market = MarketData()
        self.opportunities = []
        self.teleport_effects = []
        self.state = TradingState.MENU
        
        # Game settings
        self.game_speed = 10
        self.opportunity_spawn_rate = 0.15
        self.difficulty_multiplier = 1.0
        
        # In-game menu buttons (for pause menu)
        self.pause_buttons = []
        self.selected_pause_button = 0
        
        # Performance tracking
        self.session_start_time = datetime.now()
        self.high_score = 0
        
    def create_menu_buttons(self):
        """创建主菜单按钮"""
        self.menu_buttons = [
            {"text": "开始交易", "action": "start", "rect": pygame.Rect(WINDOW_WIDTH//2 - 100, 300, 200, 50)},
            {"text": "游戏设置", "action": "settings", "rect": pygame.Rect(WINDOW_WIDTH//2 - 100, 370, 200, 50)},
            {"text": "查看说明", "action": "instructions", "rect": pygame.Rect(WINDOW_WIDTH//2 - 100, 440, 200, 50)},
            {"text": "退出系统", "action": "exit", "rect": pygame.Rect(WINDOW_WIDTH//2 - 100, 510, 200, 50)}
        ]
    
    def create_pause_buttons(self):
        """创建暂停菜单按钮"""
        self.pause_buttons = [
            {"text": "继续游戏", "action": "resume", "rect": pygame.Rect(WINDOW_WIDTH//2 - 100, 300, 200, 50)},
            {"text": "重新开始", "action": "restart", "rect": pygame.Rect(WINDOW_WIDTH//2 - 100, 370, 200, 50)},
            {"text": "返回主菜单", "action": "menu", "rect": pygame.Rect(WINDOW_WIDTH//2 - 100, 440, 200, 50)}
        ]
    
    def draw_button(self, button, selected=False):
        """绘制按钮"""
        color = GOLD if selected else BLUE
        text_color = BLACK if selected else WHITE
        
        # Button background
        pygame.draw.rect(self.screen, color, button["rect"])
        pygame.draw.rect(self.screen, WHITE, button["rect"], 2)
        
        # Button text
        text_surface = self.menu_font.render(button["text"], True, text_color)
        text_rect = text_surface.get_rect(center=button["rect"].center)
        self.screen.blit(text_surface, text_rect)
    
    def handle_menu_click(self, pos):
        """处理菜单点击"""
        for button in self.menu_buttons:
            if button["rect"].collidepoint(pos):
                if button["action"] == "start":
                    self.reset_game()
                    self.state = TradingState.TRADING
                elif button["action"] == "settings":
                    self.state = TradingState.SETTINGS
                elif button["action"] == "instructions":
                    self.state = TradingState.ANALYSIS
                elif button["action"] == "exit":
                    return False
        return True
    
    def handle_pause_click(self, pos):
        """处理暂停菜单点击"""
        for button in self.pause_buttons:
            if button["rect"].collidepoint(pos):
                if button["action"] == "resume":
                    self.state = TradingState.TRADING
                elif button["action"] == "restart":
                    self.reset_game()
                    self.state = TradingState.TRADING
                elif button["action"] == "menu":
                    self.state = TradingState.MENU
        return True
    
    def spawn_opportunity(self):
        if random.random() < self.opportunity_spawn_rate * self.difficulty_multiplier:
            x = random.randint(0, GRID_SIZE - 1)
            y = random.randint(0, GRID_SIZE - 1)
            
            # Don't spawn on snake
            if (x, y) not in self.snake.body:
                # Weighted opportunity types based on market condition
                types = self.get_weighted_opportunity_types()
                opportunity_type = random.choices(types['types'], weights=types['weights'])[0]
                
                self.opportunities.append(TradingOpportunity(x, y, opportunity_type))
    
    def get_weighted_opportunity_types(self):
        base_types = ['profit', 'profit', 'loss', 'breakout', 'reversal', 'scalp', 'swing']
        base_weights = [0.25, 0.25, 0.15, 0.15, 0.10, 0.05, 0.05]
        
        # Adjust based on market condition
        if self.market.condition == MarketCondition.BULL:
            base_weights[0] += 0.1  # More profit opportunities
            base_weights[1] += 0.1
            base_weights[2] -= 0.05  # Fewer losses
        elif self.market.condition == MarketCondition.BEAR:
            base_weights[2] += 0.15  # More losses
            base_weights[4] += 0.1  # More reversals
            base_weights[0] -= 0.1
        elif self.market.condition == MarketCondition.VOLATILE:
            base_weights[3] += 0.2  # More breakouts
            base_weights[5] += 0.1  # More scalping
        
        return {'types': base_types, 'weights': base_weights}
    
    def update(self):
        if self.state == TradingState.TRADING:
            # Update market
            self.market.update()
            
            # Update snake
            if pygame.time.get_ticks() % (1000 // self.game_speed) == 0:
                # 检查是否需要传送
                head = self.snake.body[0]
                new_head = (head[0] + self.snake.direction[0], head[1] + self.snake.direction[1])
                
                # 预先检查碰撞
                will_teleport = False
                if (new_head[0] < 0 or new_head[0] >= GRID_SIZE or 
                    new_head[1] < 0 or new_head[1] >= GRID_SIZE):
                    will_teleport = True
                elif new_head in list(self.snake.body)[:-1]:
                    will_teleport = True
                
                if will_teleport:
                    # 更新蛇的传送方法，传递self实例
                    self.snake.teleport_to_random_position(self)
                else:
                    # 正常移动
                    if not self.snake.move():
                        self.state = TradingState.GAME_OVER
                        if self.snake.total_pnl > self.high_score:
                            self.high_score = self.snake.total_pnl
            
            # Spawn opportunities
            self.spawn_opportunity()
            
            # Update opportunities
            self.opportunities = [opp for opp in self.opportunities if opp.update()]
            
            # Update teleport effects
            self.teleport_effects = [effect for effect in self.teleport_effects if effect.update()]
            
            # Check for collisions
            head = self.snake.body[0]
            for opportunity in self.opportunities[:]:
                if (head[0], head[1]) == (opportunity.x, opportunity.y):
                    self.snake.take_opportunity(opportunity)
                    self.opportunities.remove(opportunity)
            
            # Update difficulty based on performance
            if self.snake.total_pnl > 0:
                self.difficulty_multiplier = min(2.0, 1.0 + self.snake.total_pnl / 50000)
            else:
                self.difficulty_multiplier = max(0.5, 1.0 + self.snake.total_pnl / 50000)
    
    def draw_board(self):
        # Draw grid
        for x in range(GRID_SIZE + 1):
            pygame.draw.line(self.screen, (40, 40, 40), 
                           (BOARD_X + x * CELL_SIZE, BOARD_Y), 
                           (BOARD_X + x * CELL_SIZE, BOARD_Y + BOARD_HEIGHT))
        
        for y in range(GRID_SIZE + 1):
            pygame.draw.line(self.screen, (40, 40, 40), 
                           (BOARD_X, BOARD_Y + y * CELL_SIZE), 
                           (BOARD_X + BOARD_WIDTH, BOARD_Y + y * CELL_SIZE))
    
    def draw_market_info(self):
        # Market condition indicator
        condition_colors = {
            MarketCondition.BULL: GREEN,
            MarketCondition.BEAR: RED,
            MarketCondition.SIDEWAYS: YELLOW,
            MarketCondition.VOLATILE: PURPLE
        }
        
        condition_color = condition_colors[self.market.condition]
        condition_text = f"Market: {self.market.condition.value.upper()}"
        text_surface = self.font_medium.render(condition_text, True, condition_color)
        self.screen.blit(text_surface, (BOARD_X, 20))
        
        # Price and volatility
        if len(self.market.prices) > 0:
            current_price = self.market.prices[-1]
            price_text = f"Price: ${current_price:.2f}"
            price_surface = self.font_medium.render(price_text, True, WHITE)
            self.screen.blit(price_surface, (BOARD_X + 200, 20))
            
            vol_text = f"Vol: {self.market.volatility:.3f}"
            vol_surface = self.font_medium.render(vol_text, True, WHITE)
            self.screen.blit(vol_surface, (BOARD_X + 400, 20))
        
        # RSI
        if 'rsi' in self.market.indicators:
            rsi = self.market.indicators['rsi']
            rsi_color = GREEN if 30 < rsi < 70 else RED
            rsi_text = f"RSI: {rsi:.1f}"
            rsi_surface = self.font_medium.render(rsi_text, True, rsi_color)
            self.screen.blit(rsi_surface, (BOARD_X + 600, 20))
    
    def draw_trader_info(self):
        # Trader statistics panel
        panel_x = BOARD_X + BOARD_WIDTH + 50
        panel_y = BOARD_Y
        panel_width = 300
        panel_height = 400
        
        # Panel background
        panel_surface = pygame.Surface((panel_width, panel_height))
        panel_surface.set_alpha(200)
        panel_surface.fill((20, 20, 40))
        self.screen.blit(panel_surface, (panel_x, panel_y))
        
        # Panel border
        pygame.draw.rect(self.screen, BLUE, (panel_x, panel_y, panel_width, panel_height), 2)
        
        # Title
        title_text = self.font_large.render("交易统计", True, WHITE)
        self.screen.blit(title_text, (panel_x + 10, panel_y + 10))
        
        # Statistics
        stats = [
            f"资本: ${self.snake.capital:,.2f}",
            f"总盈亏: ${self.snake.total_pnl:,.2f}",
            f"胜率: {self.snake.win_rate:.1%}",
            f"交易次数: {self.snake.trades_taken}",
            f"盈利交易: {self.snake.winning_trades}",
            f"最大回撤: {self.snake.max_drawdown:.1%}",
            f"风险评分: {self.snake.risk_score:.2f}",
            f"持仓大小: ${self.snake.position_size:,}",
            f"蛇身长度: {len(self.snake.body)}",
            f"难度系数: {self.difficulty_multiplier:.2f}"
        ]
        
        y_offset = panel_y + 60
        for stat in stats:
            stat_surface = self.font_small.render(stat, True, WHITE)
            self.screen.blit(stat_surface, (panel_x + 20, y_offset))
            y_offset += 30
    
    def draw_menu(self):
        # Title
        title_text = self.font_large.render("量化交易贪吃蛇系统", True, GOLD)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 100))
        self.screen.blit(title_text, title_rect)
        
        # Subtitle
        subtitle_text = self.font_medium.render("Quantitative Trading Snake System", True, WHITE)
        subtitle_rect = subtitle_text.get_rect(center=(WINDOW_WIDTH // 2, 150))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # Game controls info
        control_info = "使用方向键控制交易蛇移动 | 鼠标点击菜单选项"
        info_surface = self.font_small.render(control_info, True, WHITE)
        info_rect = info_surface.get_rect(center=(WINDOW_WIDTH // 2, 200))
        self.screen.blit(info_surface, info_rect)
        
        # Draw menu buttons
        if not self.menu_buttons:
            self.create_menu_buttons()
        
        for i, button in enumerate(self.menu_buttons):
            self.draw_button(button, selected=(i == self.selected_button))
        
        # Trading opportunities legend
        legend_y = 580
        legend_items = [
            ("盈利机会", GREEN),
            ("亏损机会", RED),
            ("突破机会", ORANGE),
            ("反转机会", PURPLE),
            ("剥头皮机会", (0, 255, 255)),
            ("摆动交易", (128, 0, 128))
        ]
        
        legend_text = "交易机会类型: "
        legend_surface = self.font_small.render(legend_text, True, WHITE)
        self.screen.blit(legend_surface, (50, legend_y))
        
        x_offset = 150
        for text, color in legend_items:
            pygame.draw.circle(self.screen, color, (x_offset, legend_y + 8), 6)
            text_surface = self.font_small.render(text, True, WHITE)
            self.screen.blit(text_surface, (x_offset + 12, legend_y))
            x_offset += 120
        
        # High score
        if self.high_score > 0:
            high_score_text = self.font_large.render(f"最高盈亏: ${self.high_score:,.2f}", True, GOLD)
            high_score_rect = high_score_text.get_rect(center=(WINDOW_WIDTH // 2, 650))
            self.screen.blit(high_score_text, high_score_rect)
    
    def draw_game_over(self):
        # Overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Game over text
        game_over_text = self.font_large.render("交易结束!", True, RED)
        game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, 250))
        self.screen.blit(game_over_text, game_over_rect)
        
        # Final statistics
        final_stats = [
            f"最终资本: ${self.snake.capital:,.2f}",
            f"总盈亏: ${self.snake.total_pnl:,.2f}",
            f"胜率: {self.snake.win_rate:.1%}",
            f"总交易次数: {self.snake.trades_taken}",
            f"最大回撤: {self.snake.max_drawdown:.1%}"
        ]
        
        y_offset = 320
        for stat in final_stats:
            stat_surface = self.font_medium.render(stat, True, WHITE)
            stat_rect = stat_surface.get_rect(center=(WINDOW_WIDTH // 2, y_offset))
            self.screen.blit(stat_surface, stat_rect)
            y_offset += 40
        
        # New record?
        if self.snake.total_pnl > self.high_score:
            record_text = self.font_large.render("新纪录!", True, GOLD)
            record_rect = record_text.get_rect(center=(WINDOW_WIDTH // 2, y_offset + 30))
            self.screen.blit(record_text, record_rect)
        
        # Restart instruction
        restart_text = self.font_medium.render("按空格键重新开始 | 按ESC返回主菜单", True, WHITE)
        restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, 600))
        self.screen.blit(restart_text, restart_rect)
    
    def draw_pause_menu(self):
        """绘制暂停菜单"""
        # Overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Title
        pause_text = self.font_large.render("游戏暂停", True, WHITE)
        pause_rect = pause_text.get_rect(center=(WINDOW_WIDTH // 2, 200))
        self.screen.blit(pause_text, pause_rect)
        
        # Draw pause buttons
        if not self.pause_buttons:
            self.create_pause_buttons()
        
        for i, button in enumerate(self.pause_buttons):
            self.draw_button(button, selected=(i == self.selected_pause_button))
        
        # Control hint
        hint_text = self.font_small.render("点击按钮选择 | ESC返回主菜单", True, WHITE)
        hint_rect = hint_text.get_rect(center=(WINDOW_WIDTH // 2, 550))
        self.screen.blit(hint_text, hint_rect)
    
    def draw_settings(self):
        """绘制设置界面"""
        self.screen.fill(BLACK)
        
        # Title
        title_text = self.font_large.render("游戏设置", True, GOLD)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 80))
        self.screen.blit(title_text, title_rect)
        
        # Settings panels
        settings_info = [
            "游戏控制:",
            "  • 方向键: 控制蛇的移动方向",
            "  • 鼠标点击: 选择菜单选项",
            "  • ESC键: 返回上一级菜单",
            "",
            "游戏规则:",
            "  • 控制交易蛇收集不同的交易机会",
            "  • 绿色机会带来盈利，红色带来亏损",
            "  • 每次交易都会影响你的资本和蛇的长度",
            "  • 避免撞墙或撞到自己",
            "",
            "市场指标:",
            "  • RSI: 相对强弱指数 (30-70为正常)",
            "  • Vol: 波动率 (市场波动程度)",
            "  • Market: 市场状态 (牛市/熊市/横盘/震荡)",
            "",
            "点击任意位置返回主菜单"
        ]
        
        y_offset = 150
        for info in settings_info:
            if info.startswith("  "):
                info_surface = self.font_small.render(info, True, WHITE)
                self.screen.blit(info_surface, (WINDOW_WIDTH // 2 - 200, y_offset))
            else:
                info_surface = self.font_medium.render(info, True, GOLD if info.endswith(":") else WHITE)
                info_rect = info_surface.get_rect(center=(WINDOW_WIDTH // 2 if not info.startswith("  ") else None, y_offset))
                if info.endswith(":"):
                    info_rect.x = WINDOW_WIDTH // 2 - 100
                self.screen.blit(info_surface, info_rect)
            y_offset += 30
    
    def draw_instructions(self):
        """绘制游戏说明界面"""
        self.screen.fill(BLACK)
        
        # Title
        title_text = self.font_large.render("游戏说明", True, GOLD)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 60))
        self.screen.blit(title_text, title_rect)
        
        # Instructions content
        instructions = [
            "🎮 游戏概述:",
            "   量化交易贪吃蛇是一款创新的金融教育游戏",
            "   将经典贪吃蛇玩法与量化交易概念相结合",
            "",
            "📈 交易机会类型:",
            "   • 绿色($): 盈利机会 - 稳定收益",
            "   • 红色(L): 亏损风险 - 需要避免",
            "   • 橙色(B): 突破机会 - 高风险高收益",
            "   • 紫色(R): 反转机会 - 市场转折点",
            "   • 青色(S): 剥头皮 - 快速小额交易",
            "   • 深紫(W): 摆动交易 - 中期持仓",
            "",
            "💼 交易策略:",
            "   • 根据市场条件调整交易频率",
            "   • 在牛市中积极寻找盈利机会",
            "   • 在熊市中谨慎选择反转机会",
            "   • 管理风险，控制最大回撤",
            "",
            "📊 性能指标:",
            "   • 胜率: 盈利交易占总交易的比例",
            "   • 最大回撤: 从最高点到最低点的损失",
            "   • 风险评分: 综合风险控制指标",
            "",
            "🎯 游戏目标:",
            "   • 最大化交易收益",
            "   • 保持合理的风险水平", 
            "   • 创造新的盈亏记录",
            "",
            "⚡ 特殊机制:",
            "   • 碰墙传送: 撞墙或撞到自己会随机传送",
            "   • 传送惩罚: 损失$1,000资本和部分蛇身长度",
            "   • 视觉特效: 传送时显示紫色粒子效果",
            "   • 策略调整: 谨慎移动，避免频繁传送损失",
            "",
            "点击任意位置返回主菜单"
        ]
        
        y_offset = 120
        for instruction in instructions:
            if instruction.startswith("   "):
                text_surface = self.font_small.render(instruction, True, WHITE)
                self.screen.blit(text_surface, (WINDOW_WIDTH // 2 - 250, y_offset))
            elif instruction.startswith("📈") or instruction.startswith("💼") or instruction.startswith("📊") or instruction.startswith("🎯") or instruction.startswith("🎮"):
                text_surface = self.font_medium.render(instruction, True, GOLD)
                self.screen.blit(text_surface, (WINDOW_WIDTH // 2 - 200, y_offset))
            else:
                text_surface = self.font_medium.render(instruction, True, WHITE)
                self.screen.blit(text_surface, (WINDOW_WIDTH // 2 - 100, y_offset))
            y_offset += 25
    
    def draw(self):
        self.screen.fill(BLACK)
        
        if self.state == TradingState.MENU:
            self.draw_menu()
        else:
            # Draw game elements
            self.draw_board()
            self.draw_market_info()
            
            # Draw teleport effects (underneath other elements)
            for effect in self.teleport_effects:
                effect.draw(self.screen)
            
            # Draw opportunities
            for opportunity in self.opportunities:
                opportunity.draw(self.screen, self.font_small)
            
            # Draw snake
            self.snake.draw(self.screen, self.font_small)
            
            # Draw trader info
            self.draw_trader_info()
            
            if self.state == TradingState.GAME_OVER:
                self.draw_game_over()
            elif self.state == TradingState.PAUSED:
                self.draw_pause_menu()
            elif self.state == TradingState.SETTINGS:
                self.draw_settings()
            elif self.state == TradingState.ANALYSIS:
                self.draw_instructions()
        
        pygame.display.flip()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            # Handle mouse clicks for menus
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    pos = pygame.mouse.get_pos()
                    
                    if self.state == TradingState.MENU:
                        if not self.handle_menu_click(pos):
                            return False
                    elif self.state == TradingState.PAUSED:
                        self.handle_pause_click(pos)
                    elif self.state == TradingState.SETTINGS or self.state == TradingState.ANALYSIS:
                        self.state = TradingState.MENU
                    elif self.state == TradingState.TRADING:
                        # In trading mode, clicking shows pause menu
                        self.state = TradingState.PAUSED
            
            # Handle keyboard input (only arrow keys for movement and ESC for menu)
            if event.type == pygame.KEYDOWN:
                if self.state == TradingState.TRADING:
                    if event.key == pygame.K_UP:
                        self.snake.change_direction((0, -1))
                    elif event.key == pygame.K_DOWN:
                        self.snake.change_direction((0, 1))
                    elif event.key == pygame.K_LEFT:
                        self.snake.change_direction((-1, 0))
                    elif event.key == pygame.K_RIGHT:
                        self.snake.change_direction((1, 0))
                    elif event.key == pygame.K_ESCAPE:
                        self.state = TradingState.PAUSED
                
                elif self.state == TradingState.PAUSED:
                    if event.key == pygame.K_ESCAPE:
                        self.state = TradingState.MENU
                
                elif self.state == TradingState.GAME_OVER:
                    if event.key == pygame.K_SPACE:
                        self.reset_game()
                        self.state = TradingState.TRADING
                    elif event.key == pygame.K_ESCAPE:
                        self.state = TradingState.MENU
                
                elif self.state in [TradingState.SETTINGS, TradingState.ANALYSIS]:
                    if event.key == pygame.K_ESCAPE:
                        self.state = TradingState.MENU
                
                elif self.state == TradingState.MENU:
                    if event.key == pygame.K_ESCAPE:
                        return False
                    elif event.key == pygame.K_UP:
                        self.selected_button = (self.selected_button - 1) % len(self.menu_buttons)
                    elif event.key == pygame.K_DOWN:
                        self.selected_button = (self.selected_button + 1) % len(self.menu_buttons)
                    elif event.key == pygame.K_RETURN:
                        if self.menu_buttons:
                            button = self.menu_buttons[self.selected_button]
                            if button["action"] == "start":
                                self.reset_game()
                                self.state = TradingState.TRADING
                            elif button["action"] == "settings":
                                self.state = TradingState.SETTINGS
                            elif button["action"] == "instructions":
                                self.state = TradingState.ANALYSIS
                            elif button["action"] == "exit":
                                return False
        
        return True
    
    def reset_game(self):
        self.snake = TradingSnake()
        self.market = MarketData()
        self.opportunities = []
        self.teleport_effects = []
        self.session_start_time = datetime.now()
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        
        pygame.quit()

if __name__ == "__main__":
    print("正在启动量化交易贪吃蛇系统...")
    print("Quantitative Trading Snake System Starting...")
    
    game = QuantTradingGame()
    game.run()