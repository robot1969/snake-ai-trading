# 量化交易贪吃蛇 - 文字演示版
# Quantitative Trading Snake - Text Demo

import random
import time
import os

class TextTradingSnake:
    def __init__(self):
        self.grid_size = 15
        self.snake = [(7, 7), (6, 7), (5, 7)]
        self.direction = (1, 0)
        self.capital = 100000
        self.opportunities = []
        self.score = 0
        self.trades = 0
        self.running = True
        
        # 生成初始交易机会
        self.spawn_opportunity()
    
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def draw_grid(self):
        self.clear_screen()
        print("=" * 60)
        print("🐍 量化交易贪吃蛇 - 文字演示版")
        print("=" * 60)
        print(f"💰 资本: ${self.capital:,} | 📈 盈亏: ${self.score:,} | 🤝 交易次数: {self.trades}")
        print(f"🎯 方向: {['→', '←', '↑', '↓'][[(1,0),(-1,0),(0,-1),(0,1)].index(self.direction)] if self.direction in [(1,0),(-1,0),(0,-1),(0,1)] else '→'}")
        print()
        
        # 绘制游戏区域
        for y in range(self.grid_size):
            row = ""
            for x in range(self.grid_size):
                if (x, y) in self.snake:
                    if (x, y) == self.snake[0]:
                        row += "🐍 "
                    else:
                        row += "◻ "
                elif (x, y) in self.opportunities:
                    opp = next(o for o in self.opportunities if o[0] == x and o[1] == y)
                    row += {"profit": "💚", "loss": "❤️", "breakout": "🧡", "reversal": "💜"}[opp[2]] + " "
                else:
                    row += "⬛ "
            print(row)
        
        print()
        print("控制说明:")
        print("w/s/a/d: 上/下/左/右  q: 退出")
        print("💚盈利 ❤️亏损 🧡突破 💜反转")
        print()
    
    def spawn_opportunity(self):
        if len(self.opportunities) < 3:
            while True:
                x, y = random.randint(0, self.grid_size-1), random.randint(0, self.grid_size-1)
                if (x, y) not in self.snake and (x, y) not in [(o[0], o[1]) for o in self.opportunities]:
                    types = ["profit", "loss", "breakout", "reversal"]
                    weights = [0.4, 0.2, 0.2, 0.2]  # 盈利机会更多
                    opp_type = random.choices(types, weights)[0]
                    self.opportunities.append((x, y, opp_type))
                    break
    
    def move(self):
        head = self.snake[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        
        # 边界碰撞检测
        if new_head[0] < 0 or new_head[0] >= self.grid_size or new_head[1] < 0 or new_head[1] >= self.grid_size:
            print("💥 撞墙！随机传送...")
            self.teleport_random()
            return
        
        # 自身碰撞检测
        if new_head in self.snake:
            print("💥 撞到自己！随机传送...")
            self.teleport_random()
            return
        
        self.snake.insert(0, new_head)
        
        # 检查是否吃到交易机会
        ate = False
        for opp in self.opportunities[:]:
            if new_head[0] == opp[0] and new_head[1] == opp[1]:
                self.take_opportunity(opp[2])
                self.opportunities.remove(opp)
                ate = True
                break
        
        if not ate:
            self.snake.pop()
        
        # 随机生成新的交易机会
        if random.random() < 0.3:
            self.spawn_opportunity()
    
    def take_opportunity(self, opp_type):
        values = {"profit": 1000, "loss": -800, "breakout": 1500, "reversal": 2000}
        pnl = values[opp_type]
        
        self.capital += pnl
        self.score += pnl
        self.trades += 1
        
        effects = {
            "profit": "✨ 盈利交易！",
            "loss": "💸 亏损交易...",
            "breakout": "🚀 突破机会！", 
            "reversal": "🔄 反转机会！"
        }
        
        print(f"{effects[opp_type]} P&L: ${pnl:+,}")
        
        if pnl > 0:
            print("🐍 蛇身增长了！")
    
    def teleport_random(self):
        old_pos = self.snake[0]
        
        # 传送惩罚
        self.capital = max(10000, self.capital - 2000)
        print(f"传送惩罚: -$2,000, 剩余: ${self.capital:,}")
        
        # 找到随机空位置
        empty_positions = []
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                if (x, y) not in self.snake and (x, y) not in [(o[0], o[1]) for o in self.opportunities]:
                    empty_positions.append((x, y))
        
        if empty_positions:
            new_pos = random.choice(empty_positions)
            print(f"✨ 从 {old_pos} 传送到 {new_pos}")
            self.snake[0] = new_pos
            
            # 缩短蛇身
            if len(self.snake) > 2:
                self.snake = self.snake[:max(2, len(self.snake)-1)]
                print(f"🐍 蛇身缩短了")
    
    def get_input(self):
        try:
            key = input("输入方向 (w/s/a/d/q): ").lower().strip()
            if key == 'q':
                return False
            elif key == 'w' and self.direction != (0, 1):
                self.direction = (0, -1)
            elif key == 's' and self.direction != (0, -1):
                self.direction = (0, 1)
            elif key == 'a' and self.direction != (1, 0):
                self.direction = (-1, 0)
            elif key == 'd' and self.direction != (-1, 0):
                self.direction = (1, 0)
        except:
            pass
        return True
    
    def run(self):
        print("欢迎来到量化交易贪吃蛇！")
        print("控制交易蛇收集不同的交易机会")
        time.sleep(2)
        
        while self.running:
            self.draw_grid()
            self.running = self.get_input()
            
            if self.running:
                self.move()
                
                # 检查游戏结束条件
                if self.capital < 10000:
                    print("💔 资本耗尽！游戏结束！")
                    self.running = False
                elif self.score > 10000:
                    print("🎉 恭喜！你获得了巨额利润！")
                    self.running = False
        
        print(f"\n📊 最终统计:")
        print(f"💰 最终资本: ${self.capital:,}")
        print(f"📈 总盈亏: ${self.score:,}")
        print(f"🤝 总交易次数: {self.trades}")
        print(f"🐍 最终蛇身长度: {len(self.snake)}")
        print("\n感谢游玩！")

if __name__ == "__main__":
    game = TextTradingSnake()
    game.run()