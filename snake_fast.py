# 量化交易贪吃蛇 - 优化版
# Quantitative Trading Snake - Optimized Version

import random
import time
import os
import sys

class OptimizedTradingSnake:
    def __init__(self):
        self.grid_size = 12
        self.snake = [(6, 6), (5, 6), (4, 6)]
        self.direction = (1, 0)
        self.capital = 100000
        self.opportunities = []
        self.score = 0
        self.trades = 0
        self.running = True
        
        # 预计算所有可能位置
        self.all_positions = [(x, y) for x in range(self.grid_size) for y in range(self.grid_size)]
        
        # 生成初始交易机会
        self.spawn_opportunity()
        self.spawn_opportunity()
    
    def clear_screen(self):
        """快速清屏"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def draw_grid_optimized(self):
        """优化的绘制方法"""
        self.clear_screen()
        
        # 构建网格字符串
        grid_lines = []
        
        # 标题
        grid_lines.append("=" * 50)
        grid_lines.append("QUANTITATIVE TRADING SNAKE - Optimized")
        grid_lines.append("=" * 50)
        grid_lines.append(f"Capital: ${self.capital:,} | P&L: ${self.score:,} | Trades: {self.trades}")
        
        direction_symbols = {(1,0):'→', (-1,0):'←', (0,-1):'↑', (0,1):'↓'}
        direction_symbol = direction_symbols.get(self.direction, '?')
        grid_lines.append(f"Direction: {direction_symbol}")
        grid_lines.append("")
        
        # 创建网格映射
        grid_map = {}
        
        # 添加蛇身
        for i, pos in enumerate(self.snake):
            grid_map[pos] = 'S' if i == 0 else 'o'
        
        # 添加交易机会
        symbols = {"profit": "+", "loss": "-", "breakout": "!", "reversal": "R"}
        for opp in self.opportunities:
            grid_map[opp[0:2]] = symbols.get(opp[2], '?')
        
        # 绘制网格
        for y in range(self.grid_size):
            row_chars = []
            for x in range(self.grid_size):
                pos = (x, y)
                row_chars.append(grid_map.get(pos, '.') + ' ')
            grid_lines.append(''.join(row_chars))
        
        # 控制说明
        grid_lines.append("")
        grid_lines.append("Controls: w/s/a/d: Move | q: Quit")
        grid_lines.append("Symbols: +Profit -Loss !Breakout RReversal")
        
        # 一次性输出所有内容
        print('\n'.join(grid_lines))
    
    def spawn_opportunity(self):
        """优化的机会生成"""
        if len(self.opportunities) >= 3:
            return
        
        # 使用预计算的位置列表
        occupied = set(self.snake) | set([opp[0:2] for opp in self.opportunities])
        available = [pos for pos in self.all_positions if pos not in occupied]
        
        if available:
            x, y = random.choice(available)
            types = ["profit", "loss", "breakout", "reversal"]
            weights = [0.4, 0.2, 0.2, 0.2]
            opp_type = random.choices(types, weights)[0]
            self.opportunities.append((x, y, opp_type))
    
    def move(self):
        """优化的移动方法"""
        head = self.snake[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        
        # 边界碰撞检测
        if not (0 <= new_head[0] < self.grid_size and 0 <= new_head[1] < self.grid_size):
            print("WALL HIT! Random teleport...")
            self.teleport_random()
            return
        
        # 自身碰撞检测 - 使用set提高查找速度
        if new_head in set(self.snake[1:]):
            print("SELF COLLISION! Random teleport...")
            self.teleport_random()
            return
        
        # 移动蛇头
        self.snake.insert(0, new_head)
        
        # 检查是否吃到交易机会
        ate = False
        for i, opp in enumerate(self.opportunities):
            if new_head[0] == opp[0] and new_head[1] == opp[1]:
                self.take_opportunity(opp[2])
                self.opportunities.pop(i)
                ate = True
                break
        
        if not ate:
            self.snake.pop()
        
        # 随机生成新机会
        if random.random() < 0.25:  # 降低生成频率
            self.spawn_opportunity()
    
    def take_opportunity(self, opp_type):
        """处理交易机会"""
        values = {"profit": 1000, "loss": -800, "breakout": 1500, "reversal": 2000}
        pnl = values[opp_type]
        
        self.capital += pnl
        self.score += pnl
        self.trades += 1
        
        messages = {
            "profit": "PROFIT TRADE!",
            "loss": "LOSS TRADE...",
            "breakout": "BREAKOUT OPPORTUNITY!", 
            "reversal": "REVERSAL OPPORTUNITY!"
        }
        
        print(f"{messages[opp_type]} P&L: ${pnl:+,}")
        
        if pnl > 0:
            print("Snake grows!")
            # 蛇身增长
            self.snake.append(self.snake[-1])  # 简单增长
    
    def teleport_random(self):
        """优化的随机传送"""
        old_pos = self.snake[0]
        
        # 传送惩罚
        self.capital = max(10000, self.capital - 2000)
        print(f"Teleport penalty: -$2,000, Remaining: ${self.capital:,}")
        
        # 找到随机空位置
        occupied = set(self.snake) | set([opp[0:2] for opp in self.opportunities])
        available = [pos for pos in self.all_positions if pos not in occupied]
        
        if available:
            new_pos = random.choice(available)
            print(f"Teleported from {old_pos} to {new_pos}")
            
            # 传送并缩短蛇身
            self.snake[0] = new_pos
            if len(self.snake) > 2:
                self.snake = self.snake[:max(2, len(self.snake)-1)]
                print("Snake shortened")
    
    def get_input_non_blocking(self):
        """非阻塞输入检测"""
        try:
            # Windows下的快速输入
            import msvcrt
            if msvcrt.kbhit():
                key = msvcrt.getch().decode('utf-8').lower()
                return key
        except:
            # Unix/Linux下的快速输入
            import select
            import tty
            import termios
            
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
                    return sys.stdin.read(1).lower()
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        
        return None
    
    def run(self):
        """优化的主游戏循环"""
        print("Welcome to Quantitative Trading Snake!")
        print("Optimized Version - Faster Performance!")
        time.sleep(1)
        
        game_speed = 0.2  # 移动间隔时间（秒）
        last_move_time = time.time()
        
        while self.running:
            current_time = time.time()
            
            # 快速输入检测
            key = self.get_input_non_blocking()
            if key == 'q':
                self.running = False
                break
            elif key == 'w' and self.direction != (0, 1):
                self.direction = (0, -1)
            elif key == 's' and self.direction != (0, -1):
                self.direction = (0, 1)
            elif key == 'a' and self.direction != (1, 0):
                self.direction = (-1, 0)
            elif key == 'd' and self.direction != (-1, 0):
                self.direction = (1, 0)
            
            # 定时移动
            if current_time - last_move_time >= game_speed:
                self.move()
                self.draw_grid_optimized()
                last_move_time = current_time
                
                # 检查游戏结束条件
                if self.capital < 10000:
                    print("GAME OVER - Capital depleted!")
                    self.running = False
                    break
                elif self.score > 10000:
                    print("CONGRATULATIONS - Huge profit achieved!")
                    self.running = False
                    break
            
            # 短暂休眠，减少CPU占用
            time.sleep(0.05)
        
        print(f"\nFINAL STATISTICS:")
        print(f"Final Capital: ${self.capital:,}")
        print(f"Total P&L: ${self.score:,}")
        print(f"Total Trades: {self.trades}")
        print(f"Final Snake Length: {len(self.snake)}")
        print("\nThanks for playing!")

if __name__ == "__main__":
    game = OptimizedTradingSnake()
    game.run()