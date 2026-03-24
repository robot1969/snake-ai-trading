# Trading Snake - Arrow Keys Movement Only
# ONLY arrow keys to move snake, everything else automatic

import random
import os
import time
from collections import deque

class ArrowKeysOnlySnake:
    def __init__(self):
        self.size = 12
        self.snake = [(6,6), (5,6), (4,6)]
        self.dir = (1,0)
        self.money = 100000
        self.initial_money = 100000
        self.food = []
        
        # Trading statistics (automatic)
        self.trades = []
        self.money_history = deque([100000], maxlen=20)
        self.trade_count = 0
        self.win_count = 0
        self.loss_count = 0
        self.profit_total = 0
        self.loss_total = 0
        self.teleport_count = 0
        
        # Trade type statistics
        self.trade_types = {"profit": 0, "loss": 0, "breakout": 0, "reversal": 0}
        self.trade_values = {"profit": [], "loss": [], "breakout": [], "reversal": []}
        
        # Game settings (fixed)
        self.game_speed = 0.3
        self.show_stats = True
        self.show_chart = True
        self.auto_pause = False
        
        self.make_food()
        self.last_update = time.time()
        self.frame_count = 0
    
    def clear(self):
        os.system('cls')
    
    def draw_simple_interface(self):
        """Draw simple interface - no menus, just game and auto stats"""
        self.clear()
        
        # Title
        print("🐍 Trading Snake - Arrow Keys Only")
        print("=" * 50)
        
        # Auto stats display
        if self.show_stats:
            win_rate = (self.win_count / max(1, self.trade_count)) * 100
            current_pnl = self.money - self.initial_money
            pnl_percentage = (current_pnl / self.initial_money) * 100
            
            print(f"💰 Capital: ${self.money:>10,} | 📈 P&L: {current_pnl:+9,} ({pnl_percentage:+5.1f}%)")
            print(f"🤝 Trades: {self.trade_count:3d} | 🎯 Win Rate: {win_rate:5.1f}% | ⚡ Teleports: {self.teleport_count:2d}")
        
        # Auto mini chart
        if self.show_chart and len(self.money_history) > 1:
            print("📊 Recent Capital: ", end="")
            recent = list(self.money_history)[-10:]
            for money in recent[-5:]:  # Show last 5
                if money >= self.initial_money:
                    print("▲", end=" ")
                else:
                    print("▼", end=" ")
            print()
        
        print("-" * 50)
        
        # Game area with coordinates
        print("   " + "".join([f"{i:2}" for i in range(self.size)]))
        for y in range(self.size):
            row = f"{y:2} "
            for x in range(self.size):
                if (x,y) == self.snake[0]:
                    row += "🐍" if self.frame_count % 2 == 0 else "S "
                elif (x,y) in self.snake:
                    row += "◻ "
                elif (x,y) in [f[:2] for f in self.food]:
                    food_type = next(f[2] for f in self.food if f[0]==x and f[1]==y)
                    symbols = {"profit": "💰", "loss": "💸", "breakout": "🚀", "reversal": "🔄"}
                    row += symbols.get(food_type, "?") + " "
                else:
                    row += ". "
            print(row)
        
        print("-" * 50)
        print("🎮 CONTROLS: Arrow Keys Only | ESC = Exit")
        print("📍 TIP: Use UP/DOWN/LEFT/RIGHT to move the snake")
        print("⚡ Auto-stats and auto-charts always on")
        
        # Auto trade history (last 3)
        if self.trades and self.frame_count % 30 == 0:  # Show every 30 frames
            print("📜 Recent Trades: ", end="")
            for trade in self.trades[-3:]:
                status = "+" if trade > 0 else ""
                print(f"${trade:+,} ", end="")
            print()
    
    def make_food(self):
        """Generate food automatically"""
        if len(self.food) < 3:
            while True:
                x, y = random.randint(0,self.size-1), random.randint(0,self.size-1)
                if (x,y) not in self.snake and not any((x,y)==(f[0],f[1]) for f in self.food):
                    types = ["profit", "loss", "breakout", "reversal"]
                    weights = [0.4, 0.25, 0.2, 0.15]
                    food_type = random.choices(types, weights)[0]
                    self.food.append((x, y, food_type))
                    break
    
    def move(self):
        """Move snake based on current direction"""
        head = self.snake[0]
        new = (head[0] + self.dir[0], head[1] + self.dir[1])
        
        # Wall collision - auto teleport
        if not (0 <= new[0] < self.size and 0 <= new[1] < self.size):
            self.teleport()
            return
        
        # Self collision - auto teleport
        if new in self.snake[1:]:
            self.teleport()
            return
        
        self.snake.insert(0, new)
        
        # Auto eat food
        ate = False
        for i, food in enumerate(self.food):
            if new[0] == food[0] and new[1] == food[1]:
                self.take_trade(food[2])
                self.food.pop(i)
                ate = True
                break
        
        if not ate:
            self.snake.pop()
        
        self.make_food()
        self.money_history.append(self.money)
    
    def take_trade(self, trade_type):
        """Auto handle trade with visual feedback"""
        values = {"profit": 1500, "loss": -1200, "breakout": 2000, "reversal": 2500}
        pnl = int(values[trade_type] * random.uniform(0.8, 1.2))
        
        self.money += pnl
        self.trade_count += 1
        self.trades.append(pnl)
        
        # Update statistics
        self.trade_types[trade_type] += 1
        self.trade_values[trade_type].append(pnl)
        
        if pnl > 0:
            self.win_count += 1
            self.profit_total += pnl
            print(f"✨ PROFIT! +${pnl:,}")
            if len(self.snake) < 8:
                self.snake.append(self.snake[-1])
        else:
            self.loss_count += 1
            self.loss_total += pnl
            print(f"💸 LOSS! {pnl:,}")
    
    def teleport(self):
        """Auto teleport with penalty"""
        while True:
            x, y = random.randint(0,self.size-1), random.randint(0,self.size-1)
            if (x,y) not in self.snake and not any((x,y)==(f[0],f[1]) for f in self.food):
                old_pos = self.snake[0]
                self.snake[0] = (x,y)
                self.teleport_count += 1
                
                penalty = 2000 + (self.teleport_count - 1) * 500
                self.money = max(10000, self.money - penalty)
                print(f"⚡ TELEPORT! From {old_pos} to ({x},{y}) -${penalty:,}")
                
                if len(self.snake) > 2:
                    self.snake = self.snake[:-1]
                break
    
    def show_auto_summary(self):
        """Show automatic game summary"""
        self.clear()
        print("🎮 GAME SUMMARY")
        print("=" * 50)
        
        win_rate = (self.win_count / max(1, self.trade_count)) * 100
        current_pnl = self.money - self.initial_money
        pnl_percentage = (current_pnl / self.initial_money) * 100
        
        print(f"💰 Final Capital: ${self.money:,}")
        print(f"📈 Net P&L: {current_pnl:+,} ({pnl_percentage:+.1f}%)")
        print(f"🤝 Total Trades: {self.trade_count}")
        print(f"🎯 Win Rate: {win_rate:.1f}%")
        print(f"⚡ Teleports: {self.teleport_count}")
        
        if self.win_count > 0:
            avg_profit = self.profit_total / self.win_count
            avg_loss = abs(self.loss_total) / max(1, self.loss_count)
            print(f"💎 Avg Profit: ${avg_profit:.0f}")
            print(f"📉 Avg Loss: ${avg_loss:.0f}")
            if avg_loss > 0:
                print(f"📊 Profit Factor: {avg_profit/avg_loss:.2f}")
        
        if any(self.trade_types.values()):
            print(f"\n📋 Trade Types:")
            for trade_type, count in self.trade_types.items():
                if count > 0:
                    print(f"   {trade_type.capitalize()}: {count}")
        
        print("\n" + "=" * 50)
        print("🎮 Thanks for playing!")
        print("💡 Tip: Arrow keys are all you need!")
        time.sleep(3)
    
    def run(self):
        """Main game loop - arrow keys only"""
        print("🐍 Trading Snake - Arrow Keys Only Version")
        print("Loading... Get ready to use only arrow keys!")
        time.sleep(2)
        
        import threading
        running = True
        
        def input_thread():
            nonlocal running
            while running:
                try:
                    key = input().lower().strip()
                    
                    # ONLY arrow key controls
                    if key in ['up', 'w']:
                        if self.dir != (0, 1):  # Can't go down if going up
                            self.dir = (0, -1)
                    elif key in ['down', 's']:
                        if self.dir != (0, -1):  # Can't go up if going down
                            self.dir = (0, 1)
                    elif key in ['left', 'a']:
                        if self.dir != (1, 0):  # Can't go right if going left
                            self.dir = (-1, 0)
                    elif key in ['right', 'd']:
                        if self.dir != (-1, 0):  # Can't go left if going right
                            self.dir = (1, 0)
                    elif key in ['esc', 'q', 'quit', 'exit']:
                        running = False
                    # All other inputs are ignored!
                
                except:
                    pass
        
        t = threading.Thread(target=input_thread, daemon=True)
        t.start()
        
        # Simple game loop
        while running:
            self.draw_simple_interface()
            self.move()
            self.frame_count += 1
            
            # Auto game over check
            if self.money < 10000:
                print("\n💔 GAME OVER - Capital Depleted!")
                time.sleep(2)
                self.show_auto_summary()
                self.reset_game()
            
            # Auto victory check
            if self.trade_count >= 50:
                print("\n🎉 VICTORY! 50 trades completed!")
                time.sleep(2)
                self.show_auto_summary()
                self.reset_game()
            
            time.sleep(self.game_speed)
        
        # Final summary
        self.show_auto_summary()
    
    def reset_game(self):
        """Auto reset for continuous play"""
        self.snake = [(6,6), (5,6), (4,6)]
        self.dir = (1,0)
        self.money = 100000
        self.food = []
        self.trades = []
        self.money_history = deque([100000], maxlen=20)
        self.trade_count = 0
        self.win_count = 0
        self.loss_count = 0
        self.profit_total = 0
        self.loss_total = 0
        self.teleport_count = 0
        self.trade_types = {"profit": 0, "loss": 0, "breakout": 0, "reversal": 0}
        self.trade_values = {"profit": [], "loss": [], "breakout": [], "reversal": []}
        self.make_food()
        self.frame_count = 0
        
        print("\n🔄 Auto-resetting... New game starting!")
        time.sleep(1)

if __name__ == "__main__":
    game = ArrowKeysOnlySnake()
    game.run()