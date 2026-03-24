import pygame
import random
import math
from collections import deque
from enum import Enum
import json
from datetime import datetime, timedelta

pygame.init()

# Global font function with better Chinese support
def get_chinese_font(size):
    """Get a font that supports Chinese characters"""
    chinese_fonts = [
        "microsoftyahei",  # Windows Chinese font
        "simhei",          # Simplified Chinese
        "simhei",           # Heiti
        "fangsong",        # Fangsong
        "kaiti",           # Kaiti
        "sourcehansanscn", # Source Han Sans
        "notosanscjksc",   # Noto Sans CJK
        "wqy-zenhei",     # WenQuanYi Zen Hei
        "arial unicode ms", # Arial Unicode
        "code2000",         # Code 2000
        "simsun",          # SimSun
        "arial",
        "liberation sans", 
        "dejavu sans"
    ]
    
    # Try to use Chinese fonts first
    for font_name in chinese_fonts:
        try:
            font = pygame.font.SysFont(font_name, size)
            # Test if the font can render a Chinese character
            test_surface = font.render("中", True, (255, 255, 255))
            if test_surface:
                return font
        except:
            continue
    
    # Fallback to default font
    return pygame.font.Font(None, size)

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
    AUTO_TRADING = "auto_trading"
    PAUSED = "paused"
    GAME_OVER = "game_over"

def calculate_moving_average(prices, period):
    """Calculate moving average without numpy"""
    if len(prices) < period:
        return sum(prices) / len(prices) if prices else 0
    return sum(prices[-period:]) / period

def calculate_rsi(prices, period=14):
    """Calculate RSI without numpy"""
    if len(prices) < period + 1:
        return 50
    
    gains = []
    losses = []
    
    for i in range(1, len(prices)):
        change = prices[i] - prices[i-1]
        if change > 0:
            gains.append(change)
            losses.append(0)
        else:
            gains.append(0)
            losses.append(-change)
    
    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period
    
    if avg_loss == 0:
        return 100
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_volatility(prices):
    """Calculate volatility without numpy"""
    if len(prices) < 2:
        return 0
    
    returns = []
    for i in range(1, len(prices)):
        ret = (prices[i] - prices[i-1]) / prices[i-1]
        returns.append(ret)
    
    if not returns:
        return 0
    
    mean_return = sum(returns) / len(returns)
    variance = sum((r - mean_return) ** 2 for r in returns) / len(returns)
    volatility = math.sqrt(variance) * math.sqrt(252)
    
    return volatility

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
        self.indicators['ma20'] = calculate_moving_average(self.prices, 20)
        self.indicators['ma50'] = calculate_moving_average(self.prices, 50) if len(self.prices) >= 50 else self.indicators['ma20']
        
        # RSI
        if len(self.prices) >= 14:
            self.indicators['rsi'] = calculate_rsi(self.prices, 14)
        
        # Volatility
        if len(self.prices) >= 20:
            self.volatility = calculate_volatility(self.prices[-21:])
        
        # Trend
        if len(self.prices) >= 10:
            recent_trend = (self.prices[-1] - self.prices[-10]) / self.prices[-10]
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
        
        # Check boundaries
        if (new_head[0] < 0 or new_head[0] >= GRID_SIZE or 
            new_head[1] < 0 or new_head[1] >= GRID_SIZE):
            return False
        
        # Check self collision
        if new_head in list(self.body)[:-1]:
            return False
        
        self.body.appendleft(new_head)
        
        if self.grow_count > 0:
            self.grow_count -= 1
        else:
            self.body.pop()
        
        return True
    
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
        
        # Fonts - use Chinese font support
        self.font_large = get_chinese_font(36)
        self.font_medium = get_chinese_font(24)
        self.font_small = get_chinese_font(18)

        
        # Game objects
        self.snake = TradingSnake()
        self.market = MarketData()
        self.opportunities = []
        self.state = TradingState.MENU
        
        # Game settings
        self.game_speed = 10
        self.opportunity_spawn_rate = 0.15
        self.difficulty_multiplier = 1.0
        
        # Auto trading settings
        self.auto_mode = False
        self.auto_direction_change_timer = 0
        self.auto_direction_change_interval = 20  # Change direction every 20 frames
        self.auto_target_opportunity = None
        self.auto_path = []
        
        # Performance tracking
        self.session_start_time = datetime.now()
        self.high_score = 0
        
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
    
    def auto_move_snake(self):
        """Automatically move the snake towards trading opportunities"""
        head = self.snake.body[0]
        
        # Find nearest opportunity
        if self.opportunities:
            nearest_opportunity = None
            min_distance = float('inf')
            
            for opportunity in self.opportunities:
                distance = abs(opportunity.x - head[0]) + abs(opportunity.y - head[1])
                if distance < min_distance:
                    min_distance = distance
                    nearest_opportunity = opportunity
            
            if nearest_opportunity:
                self.auto_target_opportunity = nearest_opportunity
        else:
            # No opportunities, move randomly
            self.auto_target_opportunity = None
        
        # Determine best direction
        if self.auto_target_opportunity:
            target = self.auto_target_opportunity
            target_x, target_y = target.x, target.y
            
            # Calculate direction to target
            dx = target_x - head[0]
            dy = target_y - head[1]
            
            # Determine preferred direction
            if abs(dx) > abs(dy):
                # Horizontal movement is more important
                if dx > 0 and self.snake.direction != (-1, 0):
                    new_direction = (1, 0)
                elif dx < 0 and self.snake.direction != (1, 0):
                    new_direction = (-1, 0)
                else:
                    new_direction = self.snake.direction
            else:
                # Vertical movement is more important
                if dy > 0 and self.snake.direction != (0, -1):
                    new_direction = (0, 1)
                elif dy < 0 and self.snake.direction != (0, 1):
                    new_direction = (0, -1)
                else:
                    new_direction = self.snake.direction
        else:
            # No target, move randomly but avoid walls
            possible_directions = []
            current_dir = self.snake.direction
            
            # Check all four directions
            directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
            opposite_directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            
            for i, direction in enumerate(directions):
                # Can't go backwards
                if direction == opposite_directions[directions.index(current_dir)]:
                    continue
                
                # Check if direction is safe (not hitting wall immediately)
                new_head = (head[0] + direction[0], head[1] + direction[1])
                if (0 <= new_head[0] < GRID_SIZE and 0 <= new_head[1] < GRID_SIZE):
                    if new_head not in list(self.snake.body)[:-1]:
                        possible_directions.append(direction)
            
            if possible_directions:
                # Prefer continuation, then random
                if current_dir in possible_directions:
                    new_direction = current_dir
                else:
                    new_direction = random.choice(possible_directions)
            else:
                new_direction = self.snake.direction  # No safe move
        
        # Apply direction change periodically
        self.auto_direction_change_timer += 1
        if self.auto_direction_change_timer >= self.auto_direction_change_interval:
            self.snake.change_direction(new_direction)
            self.auto_direction_change_timer = 0
        
        # Actually move the snake
        return self.snake.move()
    
    def update(self):
        if self.state in [TradingState.TRADING, TradingState.AUTO_TRADING]:
            # Update market
            self.market.update()
            
            # Update snake movement timing
            current_time = pygame.time.get_ticks()
            should_move = current_time % (1000 // self.game_speed) == 0
            
            if should_move:
                if self.state == TradingState.AUTO_TRADING:
                    # Auto trading mode
                    if not self.auto_move_snake():
                        self.state = TradingState.GAME_OVER
                        if self.snake.total_pnl > self.high_score:
                            self.high_score = self.snake.total_pnl
                else:
                    # Manual trading mode
                    if not self.snake.move():
                        self.state = TradingState.GAME_OVER
                        if self.snake.total_pnl > self.high_score:
                            self.high_score = self.snake.total_pnl
            
            # Spawn opportunities
            self.spawn_opportunity()
            
            # Update opportunities
            self.opportunities = [opp for opp in self.opportunities if opp.update()]
            
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
        
        # Mode display
        mode_text = f"模式: {'自动' if self.auto_mode else '手动'}"
        mode_color = (255, 100, 100) if self.auto_mode else (100, 255, 100)
        
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
            f"难度系数: {self.difficulty_multiplier:.2f}",
            mode_text
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
        subtitle_text = self.font_medium.render("Quantitative Trading System", True, WHITE)
        subtitle_rect = subtitle_text.get_rect(center=(WINDOW_WIDTH // 2, 150))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # Instructions
        instructions = [
            "方向键: 移动交易蛇",
            "绿色: 盈利机会 (+$)",
            "红色: 亏损机会 (-$)",
            "橙色: 突破机会",
            "紫色: 反转机会", 
            "青色: 剥头皮机会",
            "深紫: 摆动交易机会",
            "",
            "按空格键开始交易",
            "按A键启动自动模式",
            "按ESC键退出系统"
        ]
        
        y_offset = 250
        for instruction in instructions:
            if instruction:
                inst_surface = self.font_medium.render(instruction, True, WHITE)
                inst_rect = inst_surface.get_rect(center=(WINDOW_WIDTH // 2, y_offset))
                self.screen.blit(inst_surface, inst_rect)
            y_offset += 35
        
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
    
    def draw(self):
        self.screen.fill(BLACK)
        
        if self.state == TradingState.MENU:
            self.draw_menu()
        else:
            # Draw game elements
            self.draw_board()
            self.draw_market_info()
            
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
                pause_text = self.font_large.render("游戏暂停", True, WHITE)
                pause_rect = pause_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
                self.screen.blit(pause_text, pause_rect)
        
        pygame.display.flip()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if self.state == TradingState.MENU:
                    if event.key == pygame.K_SPACE:
                        self.reset_game()
                        self.state = TradingState.TRADING
                    elif event.key == pygame.K_a:  # Start in auto mode
                        self.reset_game()
                        self.state = TradingState.AUTO_TRADING
                        self.auto_mode = True
                        print("自动模式已开启！")
                    elif event.key == pygame.K_ESCAPE:
                        return False
                
                elif self.state == TradingState.TRADING:
                    if event.key == pygame.K_UP:
                        self.snake.change_direction((0, -1))
                    elif event.key == pygame.K_DOWN:
                        self.snake.change_direction((0, 1))
                    elif event.key == pygame.K_LEFT:
                        self.snake.change_direction((-1, 0))
                    elif event.key == pygame.K_RIGHT:
                        self.snake.change_direction((1, 0))
                    elif event.key == pygame.K_p:
                        self.state = TradingState.PAUSED
                    elif event.key == pygame.K_a:  # Toggle auto mode
                        self.reset_game()
                        self.state = TradingState.AUTO_TRADING
                        self.auto_mode = True
                        print("自动模式已开启！")
                    elif event.key == pygame.K_ESCAPE:
                        self.state = TradingState.MENU
                
            elif self.state == TradingState.PAUSED:
                if event.key == pygame.K_p:
                    self.state = TradingState.TRADING
                elif event.key == pygame.K_a:  # Toggle auto mode
                    self.state = TradingState.AUTO_TRADING
                    self.auto_mode = True
                    print("自动模式已开启！")
                elif event.key == pygame.K_ESCAPE:
                    self.state = TradingState.MENU
                
                elif self.state == TradingState.AUTO_TRADING:
                    # In auto mode, allow manual direction override
                    if event.key == pygame.K_UP:
                        self.snake.change_direction((0, -1))
                    elif event.key == pygame.K_DOWN:
                        self.snake.change_direction((0, 1))
                    elif event.key == pygame.K_LEFT:
                        self.snake.change_direction((-1, 0))
                    elif event.key == pygame.K_RIGHT:
                        self.snake.change_direction((1, 0))
                    elif event.key == pygame.K_p:
                        self.state = TradingState.PAUSED
                    elif event.key == pygame.K_m:  # Toggle back to manual
                        self.state = TradingState.TRADING
                        self.auto_mode = False
                        print("手动模式已开启！")
                    elif event.key == pygame.K_ESCAPE:
                        self.state = TradingState.MENU
                
                elif self.state == TradingState.GAME_OVER:
                    if event.key == pygame.K_SPACE:
                        self.reset_game()
                        self.state = TradingState.TRADING
                    elif event.key == pygame.K_ESCAPE:
                        self.state = TradingState.MENU
        
        return True
    
    def reset_game(self):
        self.snake = TradingSnake()
        self.market = MarketData()
        self.opportunities = []
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
    print("方向键: 移动  |  A键: 自动模式  |  P键: 暂停  |  ESC: 退出")
    print("Controls: Arrow Keys to move, SPACE to start, P to pause, ESC to exit")
    
    game = QuantTradingGame()
    game.run()