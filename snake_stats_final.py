# Quantitative Trading Snake - ASCII Statistics Version

import random
import os
import time
from collections import deque

class TradingSnakeStats:
    def __init__(self):
        self.size = 12
        self.snake = [(6,6), (5,6), (4,6)]
        self.dir = (1,0)
        self.money = 100000
        self.initial_money = 100000
        self.food = []
        
        # Trading statistics
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
        
        self.make_food()
        self.last_update = time.time()
    
    def clear(self):
        os.system('cls')
    
    def draw_barchart(self, data, labels, title, height=8, width=50):
        """Draw ASCII bar chart"""
        if not data:
            return
        
        print(f"\n{title}")
        print("=" * width)
        
        max_val = max(data) if max(data) > 0 else 1
        bar_width = (width - 20) // len(data)
        
        # Draw bars
        for level in range(height, 0, -1):
            threshold = (max_val * level) / height
            line = "  "
            for i, val in enumerate(data):
                if val >= threshold:
                    bar_length = int((val / max_val) * bar_width * 0.8)
                    line += "#" * bar_length + " " * (bar_width - bar_length)
                else:
                    line += " " * bar_width
            print(line)
        
        # Bottom and labels
        line = "  "
        for i in range(len(data)):
            line += "-" * bar_width
        print(line + "|")
        
        # Value labels
        line = "  "
        for i, val in enumerate(data):
            line += f"{val:>{bar_width}}"
        print(line)
        
        # Type labels
        line = "  "
        for i, label in enumerate(labels):
            line += f"{label[:bar_width]:^{bar_width}}"
        print(line)
        print("=" * width)
    
    def draw_linechart(self, data, title, height=6, width=40):
        """Draw ASCII line chart"""
        if len(data) < 2:
            return
        
        print(f"\n{title}")
        print("=" * width)
        
        max_val = max(data)
        min_val = min(data)
        range_val = max_val - min_val if max_val != min_val else 1
        
        # Data points limit
        points = data[-width:] if len(data) > width else data
        
        # Draw chart
        for level in range(height, 0, -1):
            threshold = min_val + (range_val * level / height)
            line = ""
            for i, val in enumerate(points):
                if i == len(points) - 1:  # Last point
                    line += "@" if val >= threshold else " "
                else:
                    next_val = points[i+1] if i+1 < len(points) else val
                    if val >= threshold and next_val >= threshold:
                        line += "-"
                    elif val >= threshold and next_val < threshold:
                        line += "|"
                    elif val < threshold and next_val >= threshold:
                        line += "|"
                    else:
                        line += " "
            print(f"  {line}")
        
        # Bottom
        print("  " + "-" * len(points))
        
        # Show key values
        if len(points) <= 10:
            value_line = "  "
            for i, val in enumerate(points[::2]):  # Every other point
                value_line += f"{val:>6}"
            print(value_line)
        
        print("=" * width)
    
    def draw_main_stats(self):
        """Draw main statistics"""
        print("Trading Snake - Real-time Statistics Dashboard")
        print("=" * 70)
        
        # Basic statistics
        win_rate = (self.win_count / max(1, self.trade_count)) * 100
        current_pnl = self.money - self.initial_money
        pnl_percentage = (current_pnl / self.initial_money) * 100
        game_time = int(time.time() - self.last_update)
        
        # First row
        print(f"Capital: ${self.money:>10,} | P&L: {current_pnl:>+9,} ({pnl_percentage:+5.1f}%) | Time: {game_time:3d}s")
        
        # Second row
        print(f"Trades: {self.trade_count:3d} | Win Rate: {win_rate:5.1f}% | Teleports: {self.teleport_count:2d} | Length: {len(self.snake):2d}")
        
        # Third row
        if self.profit_total > 0:
            avg_profit = self.profit_total / max(1, self.win_count)
            avg_loss = abs(self.loss_total) / max(1, self.loss_count)
            profit_factor = avg_profit / max(0.1, avg_loss)
            print(f"Avg Profit: ${avg_profit:>6.0f} | Avg Loss: ${avg_loss:>6.0f} | Ratio: {profit_factor:>4.2f}")
        
        print("=" * 70)
    
    def draw_game_area(self):
        """Draw game area"""
        print("\nGame Area")
        print("-" * 30)
        
        for y in range(self.size):
            row = ""
            for x in range(self.size):
                if (x,y) == self.snake[0]:
                    row += "S"
                elif (x,y) in self.snake:
                    row += "o"
                elif (x,y) in [f[:2] for f in self.food]:
                    # Find food type
                    food_type = next(f[2] for f in self.food if f[0]==x and f[1]==y)
                    symbols = {"profit": "$", "loss": "L", "breakout": "B", "reversal": "R"}
                    row += symbols.get(food_type, "?")
                else:
                    row += "."
            print(row)
        
        print("-" * 30)
        print("Controls: WASD=Move SPC=Stats C=Charts Q=Quit")
        print("Symbols: $=Profit L=Loss B=Breakout R=Reversal")
    
    def make_food(self):
        """Generate food"""
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
        """Move snake"""
        head = self.snake[0]
        new = (head[0] + self.dir[0], head[1] + self.dir[1])
        
        # Wall collision
        if not (0 <= new[0] < self.size and 0 <= new[1] < self.size):
            self.teleport()
            return
        
        # Self collision
        if new in self.snake[1:]:
            self.teleport()
            return
        
        self.snake.insert(0, new)
        
        # Eat food
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
        """Handle trade"""
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
            print(f"+${pnl:,} {trade_type.upper()}!")
            if len(self.snake) < 8:
                self.snake.append(self.snake[-1])
        else:
            self.loss_count += 1
            self.loss_total += pnl
            print(f"{pnl:,} {trade_type.upper()}!")
    
    def teleport(self):
        """Teleport"""
        while True:
            x, y = random.randint(0,self.size-1), random.randint(0,self.size-1)
            if (x,y) not in self.snake and not any((x,y)==(f[0],f[1]) for f in self.food):
                self.snake[0] = (x,y)
                self.teleport_count += 1
                
                penalty = 2000 + (self.teleport_count - 1) * 500
                self.money = max(10000, self.money - penalty)
                print(f"Teleport #{self.teleport_count} -${penalty:,}")
                
                if len(self.snake) > 2:
                    self.snake = self.snake[:-1]
                break
    
    def show_statistics(self):
        """Show detailed statistics"""
        self.clear()
        print("Detailed Trading Analysis Report")
        print("=" * 80)
        
        # Basic indicators
        win_rate = (self.win_count / max(1, self.trade_count)) * 100
        current_pnl = self.money - self.initial_money
        pnl_percentage = (current_pnl / self.initial_money) * 100
        
        print(f"Capital Analysis:")
        print(f"   Initial Capital: ${self.initial_money:,}")
        print(f"   Current Capital: ${self.money:,}")
        print(f"   Net P&L: ${current_pnl:+,} ({pnl_percentage:+.1f}%)")
        
        print(f"\nTrading Performance:")
        print(f"   Total Trades: {self.trade_count}")
        print(f"   Winning Trades: {self.win_count}")
        print(f"   Losing Trades: {self.loss_count}")
        print(f"   Win Rate: {win_rate:.1f}%")
        
        if self.win_count > 0 and self.loss_count > 0:
            avg_profit = self.profit_total / self.win_count
            avg_loss = abs(self.loss_total) / self.loss_count
            profit_factor = avg_profit / avg_loss
            
            print(f"   Average Profit: ${avg_profit:.0f}")
            print(f"   Average Loss: ${avg_loss:.0f}")
            print(f"   Profit/Loss Ratio: {profit_factor:.2f}")
        
        print(f"\nRisk Control:")
        print(f"   Teleport Count: {self.teleport_count}")
        print(f"   Total Teleport Cost: ${self.teleport_count * 2000 + (self.teleport_count-1)*self.teleport_count//2*500:,}")
        print(f"   Current Snake Length: {len(self.snake)}")
        
        # Trade type charts
        if any(self.trade_types.values()):
            type_data = [self.trade_types[t] for t in ["profit", "loss", "breakout", "reversal"]]
            type_labels = ["Profit", "Loss", "Breakout", "Reversal"]
            self.draw_barchart(type_data, type_labels, "Trade Type Distribution")
        
        # P&L trend chart
        if len(self.money_history) > 1:
            self.draw_linechart(list(self.money_history), "Capital Change Trend")
        
        # Recent trades
        if self.trades:
            print(f"\nRecent 10 Trades:")
            print("-" * 50)
            for i, trade in enumerate(self.trades[-10:], 1):
                status = "WIN" if trade > 0 else "LOSS"
                print(f"   {i:2d}. {status:6} ${trade:+6,}")
        
        print("\n" + "=" * 80)
        print("Press Enter to return to game...")
        input()
    
    def show_charts(self):
        """Show charts"""
        self.clear()
        print("Real-time Chart Analysis")
        print("=" * 70)
        
        # Capital change chart
        if len(self.money_history) > 1:
            self.draw_linechart(list(self.money_history), "Real-time Capital Changes (Last 20)")
        
        # Trade frequency analysis
        if self.trades:
            # Group trades for statistics
            profit_trades = [t for t in self.trades if t > 0]
            loss_trades = [t for t in self.trades if t < 0]
            
            # P&L comparison
            data = []
            labels = []
            
            if profit_trades:
                data.append(sum(profit_trades))
                labels.append("Total Profit")
            if loss_trades:
                data.append(abs(sum(loss_trades)))
                labels.append("Total Loss")
            
            if data:
                self.draw_barchart(data, labels, "Total P&L Comparison")
            
            # Average comparison
            avg_data = []
            avg_labels = []
            
            if profit_trades:
                avg_data.append(sum(profit_trades)/len(profit_trades))
                avg_labels.append("Avg Profit")
            if loss_trades:
                avg_data.append(abs(sum(loss_trades))/len(loss_trades))
                avg_labels.append("Avg Loss")
            
            if avg_data:
                self.draw_barchart(avg_data, avg_labels, "Average per Trade")
        
        print("\n" + "=" * 70)
        print("Press Enter to return to game...")
        input()
    
    def run(self):
        """Main game loop"""
        print("Trading Snake - ASCII Statistics Version")
        print("Controls: WASD=Move, SPC=Detailed Stats, C=Charts, Q=Quit")
        time.sleep(1.5)
        
        import threading
        running = True
        
        def input_thread():
            nonlocal running
            while running:
                try:
                    key = input().lower()
                    if key == 'q':
                        running = False
                    elif key == ' ':
                        self.show_statistics()
                    elif key == 'c':
                        self.show_charts()
                    elif key == 'w' and self.dir != (0,1):
                        self.dir = (0,-1)
                    elif key == 's' and self.dir != (0,-1):
                        self.dir = (0,1)
                    elif key == 'a' and self.dir != (1,0):
                        self.dir = (-1,0)
                    elif key == 'd' and self.dir != (-1,0):
                        self.dir = (1,0)
                except:
                    pass
        
        t = threading.Thread(target=input_thread, daemon=True)
        t.start()
        
        while running:
            self.clear()
            self.draw_main_stats()
            self.draw_game_area()
            
            self.move()
            
            if self.money < 10000:
                print("\nGAME OVER - Capital Depleted!")
                time.sleep(2)
                break
            
            time.sleep(0.25)
        
        # Final report
        self.show_statistics()

if __name__ == "__main__":
    game = TradingSnakeStats()
    game.run()