# Trading Snake - Enhanced Console (English)
# No pygame required - Windows console enhanced version

import random
import os
import time
import sys
import threading
from collections import deque

class EnhancedConsoleSnake:
    def __init__(self):
        self.size = 15
        self.snake = [(7,7), (6,7), (5,7)]
        self.dir = (1,0)
        self.money = 100000
        self.initial_money = 100000
        self.food = []
        
        # Statistics
        self.trades = []
        self.money_history = deque([100000], maxlen=25)
        self.trade_count = 0
        self.win_count = 0
        self.loss_count = 0
        self.profit_total = 0
        self.loss_total = 0
        self.teleport_count = 0
        
        # Trade types
        self.trade_types = {"profit": 0, "loss": 0, "breakout": 0, "reversal": 0}
        
        # Game settings
        self.game_speed = 0.25
        self.frame_count = 0
        self.animation_frame = 0
        
        self.make_food()
    
    def clear_screen(self):
        """Clear screen"""
        os.system('cls')
    
    def draw_enhanced_interface(self):
        """Draw enhanced console interface"""
        self.clear_screen()
        
        # Title with border
        border = "+" + "-" * 58 + "+"
        print(border)
        print("|         TRADING SNAKE - ENHANCED CONSOLE         |")
        print(border)
        
        # Stats bar
        win_rate = (self.win_count / max(1, self.trade_count)) * 100
        current_pnl = self.money - self.initial_money
        pnl_symbol = "+" if current_pnl >= 0 else "-"
        
        stats1 = f"Capital: ${self.money:>10,} {pnl_symbol} P&L: {current_pnl:+9,}"
        stats2 = f"Trades: {self.trade_count:3d} Win Rate: {win_rate:5.1f}% Teleports: {self.teleport_count:2d}"
        
        print(f"| {stats1:<58} |")
        print(f"| {stats2:<58} |")
        
        # Mini chart
        if len(self.money_history) > 1:
            chart_line = "Capital: "
            recent = list(self.money_history)[-10:]
            for money in recent:
                change = money - self.initial_money
                if change >= 0:
                    chart_line += "^"
                else:
                    chart_line += "v"
            print(f"| {chart_line:<58} |")
        
        print("+" + "-" * 58 + "+")
        
        # Game grid with coordinates
        print("|    0 1 2 3 4 5 6 7 8 9 0 1 2 3 4")
        print("|   " + "-" * (self.size * 2))
        
        for y in range(self.size):
            # Grid row
            row = f"| {y:2d} "
            for x in range(self.size):
                if (x,y) == self.snake[0]:
                    # Animated snake head
                    if self.animation_frame % 2 == 0:
                        row += "@"
                    else:
                        row += "#"
                elif (x,y) in self.snake:
                    row += "o"
                elif (x,y) in [f[:2] for f in self.food]:
                    food_type = next(f[2] for f in self.food if f[0]==x and f[1]==y)
                    food_symbols = {
                        "profit": "$", "loss": "L", 
                        "breakout": "B", "reversal": "R"
                    }
                    row += food_symbols.get(food_type, "?")
                else:
                    row += "."
            print(row)
        
        print("|   " + "-" * (self.size * 2))
        print("+" + "-" * 58 + "+")
        
        # Controls
        controls = "CONTROLS: Arrow Keys or WASD to move | ESC to quit | SPACE for stats"
        print(f"  {controls}")
        
        # Direction indicator
        dir_display = {(1,0):">", (-1,0):"<", (0,-1):"^", (0,1):"v"}
        current_dir = dir_display.get(self.dir, "?")
        print(f"  Direction: {current_dir} | Frame: {self.frame_count}")
        
        # Recent trades
        if self.trades and self.frame_count % 20 == 0:
            recent_trades = "Recent: "
            for trade in self.trades[-3:]:
                symbol = "+" if trade > 0 else "-"
                recent_trades += f"{symbol}{trade:+,} "
            print(f"  {recent_trades}")
        
        self.animation_frame += 1
    
    def make_food(self):
        """Generate food"""
        if len(self.food) < 4:
            while True:
                x, y = random.randint(0,self.size-1), random.randint(0,self.size-1)
                if (x,y) not in self.snake and not any((x,y)==(f[0],f[1]) for f in self.food):
                    types = ["profit", "profit", "loss", "breakout", "reversal"]
                    weights = [0.35, 0.35, 0.15, 0.1, 0.05]
                    food_type = random.choices(types, weights)[0]
                    self.food.append((x, y, food_type))
                    break
    
    def move_snake(self):
        """Move snake"""
        head = self.snake[0]
        new = (head[0] + self.dir[0], head[1] + self.dir[1])
        
        # Wall collision - teleport
        if not (0 <= new[0] < self.size and 0 <= new[1] < self.size):
            self.teleport_effect()
            return
        
        # Self collision - teleport
        if new in self.snake[1:]:
            self.teleport_effect()
            return
        
        self.snake.insert(0, new)
        
        # Eat food
        ate = False
        for i, food in enumerate(self.food):
            if new[0] == food[0] and new[1] == food[1]:
                self.take_trade_enhanced(food[2])
                self.food.pop(i)
                ate = True
                break
        
        if not ate:
            self.snake.pop()
        
        self.make_food()
        self.money_history.append(self.money)
    
    def take_trade_enhanced(self, trade_type):
        """Enhanced trade handling"""
        values = {
            "profit": 1200, 
            "loss": -900, 
            "breakout": 1800, 
            "reversal": 2200
        }
        base_pnl = values[trade_type]
        pnl = int(base_pnl * random.uniform(0.8, 1.3))
        
        self.money += pnl
        self.trade_count += 1
        self.trades.append(pnl)
        
        self.trade_types[trade_type] += 1
        
        if pnl > 0:
            self.win_count += 1
            self.profit_total += pnl
            
            profit_messages = [
                f"EXCELLENT! +${pnl:,} profit!",
                f"GREAT TRADE! +${pnl:,}",
                f"WINNING! +${pnl:,}",
                f"PERFECT! +${pnl:,}"
            ]
            print(f"  {random.choice(profit_messages)}")
            
            if len(self.snake) < 10:
                self.snake.append(self.snake[-1])
                print(f"  Snake length: {len(self.snake)}")
        else:
            self.loss_count += 1
            self.loss_total += pnl
            print(f"  Loss trade: {pnl:,}")
    
    def teleport_effect(self):
        """Teleport with feedback"""
        old_pos = self.snake[0]
        
        while True:
            x, y = random.randint(0,self.size-1), random.randint(0,self.size-1)
            if (x,y) not in self.snake and not any((x,y)==(f[0],f[1]) for f in self.food):
                self.snake[0] = (x,y)
                self.teleport_count += 1
                
                penalty = 1500 + (self.teleport_count - 1) * 300
                self.money = max(10000, self.money - penalty)
                
                teleport_messages = [
                    f"TELEPORT! From {old_pos} to ({x},{y})",
                    f"SPACE-WARP! Cost: ${penalty:,}",
                    f"QUANTUM JUMP! -${penalty:,}"
                ]
                print(f"  {random.choice(teleport_messages)}")
                
                if len(self.snake) > 2:
                    removed = min(2, len(self.snake) - 1)
                    for _ in range(removed):
                        if len(self.snake) > 2:
                            self.snake.pop()
                    print(f"  Snake shortened by {removed} segments")
                break
    
    def get_keyboard_input(self):
        """Get keyboard input"""
        try:
            import msvcrt
            
            if msvcrt.kbhit():
                key = msvcrt.getch()
                
                # Arrow keys
                if key == b'\xe0':
                    key = msvcrt.getch()
                    if key == b'H':  # Up
                        if self.dir != (0, 1):
                            self.dir = (0, -1)
                    elif key == b'P':  # Down
                        if self.dir != (0, -1):
                            self.dir = (0, 1)
                    elif key == b'K':  # Left
                        if self.dir != (1, 0):
                            self.dir = (-1, 0)
                    elif key == b'M':  # Right
                        if self.dir != (-1, 0):
                            self.dir = (1, 0)
                
                # WASD and other keys
                elif key in [b'w', b'W']:  # W up
                    if self.dir != (0, 1):
                        self.dir = (0, -1)
                elif key in [b's', b'S']:  # S down
                    if self.dir != (0, -1):
                        self.dir = (0, 1)
                elif key in [b'a', b'A']:  # A left
                    if self.dir != (1, 0):
                        self.dir = (-1, 0)
                elif key in [b'd', b'D']:  # D right
                    if self.dir != (-1, 0):
                        self.dir = (1, 0)
                elif key == b'\x1b':  # ESC
                    return False
                elif key == b' ':  # Space
                    self.show_statistics()
                
        except ImportError:
            pass
        except:
            pass
        
        return True
    
    def show_statistics(self):
        """Show statistics"""
        self.clear_screen()
        
        print("+" + "-" * 58 + "+")
        print("|              TRADING STATISTICS              |")
        print("+" + "-" * 58 + "+")
        print()
        
        win_rate = (self.win_count / max(1, self.trade_count)) * 100
        current_pnl = self.money - self.initial_money
        
        print(f"Capital Analysis:")
        print(f"   Initial: ${self.initial_money:,}")
        print(f"   Current: ${self.money:,}")
        print(f"   Net P&L: {current_pnl:+,}")
        print()
        
        print(f"Performance:")
        print(f"   Total Trades: {self.trade_count}")
        print(f"   Win Rate: {win_rate:.1f}%")
        print(f"   Teleports: {self.teleport_count}")
        print()
        
        if any(self.trade_types.values()):
            print(f"Trade Types:")
            total = sum(self.trade_types.values())
            for trade_type, count in self.trade_types.items():
                if count > 0:
                    percentage = (count / total) * 100
                    print(f"   {trade_type.capitalize():10}: {count:2d} ({percentage:5.1f}%)")
            print()
        
        print("Press any key to continue...")
        
        try:
            import msvcrt
            msvcrt.getch()
        except:
            input()
    
    def run(self):
        """Main game loop"""
        print("Loading Trading Snake - Enhanced Console Version...")
        time.sleep(1)
        
        running = True
        last_move_time = time.time()
        
        def input_thread():
            nonlocal running
            while running:
                try:
                    running = self.get_keyboard_input()
                except:
                    pass
                time.sleep(0.01)
        
        input_thread_obj = threading.Thread(target=input_thread, daemon=True)
        input_thread_obj.start()
        
        while running:
            self.draw_enhanced_interface()
            
            # Move snake
            current_time = time.time()
            if current_time - last_move_time >= self.game_speed:
                self.move_snake()
                last_move_time = current_time
                self.frame_count += 1
            
            # Check game over
            if self.money < 10000:
                self.clear_screen()
                print("+" + "-" * 58 + "+")
                print("|                GAME OVER - CAPITAL DEPLETED!               |")
                print("+" + "-" * 58 + "+")
                print()
                print(f"Final Capital: ${self.money:,}")
                print(f"Total Trades: {self.trade_count}")
                print(f"Win Rate: {(self.win_count/max(1,self.trade_count))*100:.1f}%")
                print()
                print("Press any key to restart...")
                
                try:
                    import msvcrt
                    msvcrt.getch()
                except:
                    input()
                
                self.reset_game()
                last_move_time = time.time()
            
            # Victory
            if self.trade_count >= 25:
                self.clear_screen()
                print("+" + "-" * 58 + "+")
                print("|                   VICTORY!                   |")
                print("|            25 Trades Completed!            |")
                print("+" + "-" * 58 + "+")
                print()
                self.show_statistics()
                self.reset_game()
                last_move_time = time.time()
            
            time.sleep(0.05)
        
        print("Thanks for playing!")
    
    def reset_game(self):
        """Reset game"""
        self.snake = [(7,7), (6,7), (5,7)]
        self.dir = (1,0)
        self.money = 100000
        self.food = []
        self.trades = []
        self.money_history = deque([100000], maxlen=25)
        self.trade_count = 0
        self.win_count = 0
        self.loss_count = 0
        self.profit_total = 0
        self.loss_total = 0
        self.teleport_count = 0
        self.trade_types = {"profit": 0, "loss": 0, "breakout": 0, "reversal": 0}
        self.frame_count = 0
        self.animation_frame = 0
        self.make_food()

if __name__ == "__main__":
    game = EnhancedConsoleSnake()
    game.run()