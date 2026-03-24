# Trading Snake - Final Working Version
# Simplified to work with Python 3.14

import random
import os
import time
import threading
from collections import deque

class FinalTradingSnake:
    def __init__(self):
        self.size = 15
        self.snake = [(7,7), (6,7), (5,7)]
        self.dir = (1,0)
        self.money = 100000
        self.initial_money = 100000
        self.food = []
        self.trades = []
        self.trade_count = 0
        self.win_count = 0
        self.loss_count = 0
        self.teleport_count = 0
        self.trade_types = {"profit": 0, "loss": 0, "breakout": 0, "reversal": 0}
        
        self.game_speed = 0.3
        self.frame_count = 0
        self.make_food()
    
    def clear_screen(self):
        os.system('cls')
    
    def draw_interface(self):
        self.clear_screen()
        
        # Title
        print("=" * 60)
        print("   TRADING SNAKE - FINAL WORKING VERSION")
        print("=" * 60)
        
        # Stats
        win_rate = (self.win_count / max(1, self.trade_count)) * 100
        current_pnl = self.money - self.initial_money
        pnl_symbol = "+" if current_pnl >= 0 else "-"
        
        print(f"Capital: ${self.money:>10,} {pnl_symbol} P&L: {current_pnl:+9,}")
        print(f"Trades: {self.trade_count:3d} Win Rate: {win_rate:5.1f}% Teleports: {self.teleport_count:2d}")
        print("-" * 60)
        
        # Game grid
        print("   " + "".join(f"{i:2d}" for i in range(self.size)))
        print("   " + "-" * (self.size * 3))
        
        for y in range(self.size):
            row = f"{y:2d} "
            for x in range(self.size):
                if (x,y) == self.snake[0]:
                    row += "@"  # Snake head
                elif (x,y) in self.snake:
                    row += "o"  # Snake body
                elif any((x,y)==(f[0],f[1]) for f in self.food):
                    # Find food type
                    for f_item in self.food:
                        if f_item[0]==x and f_item[1]==y:
                            food_type = f_item[2]
                            break
                    symbols = {"profit": "$", "loss": "L", "breakout": "B", "reversal": "R"}
                    row += symbols.get(food_type, "?")
                else:
                    row += "."
            print(row)
        
        print("   " + "-" * (self.size * 3))
        
        # Controls
        dir_symbols = {(1,0):">", (-1,0):"<", (0,-1):"^", (0,1):"v"}
        current_dir = dir_symbols.get(self.dir, "?")
        
        print("Controls: Arrow Keys or WASD | ESC: Quit | SPACE: Stats")
        print(f"Direction: {current_dir} | Frame: {self.frame_count}")
        
        # Recent trades
        if self.trades and self.frame_count % 20 == 0:
            print("Recent: ", end="")
            for trade in self.trades[-3:]:
                symbol = "+" if trade > 0 else "-"
                print(f"{symbol}{trade:+,} ", end="")
            print()
    
    def make_food(self):
        if len(self.food) < 4:
            while True:
                x, y = random.randint(0, self.size-1), random.randint(0, self.size-1)
                if (x,y) not in self.snake and not any((x,y)==(f[0],f[1]) for f in self.food):
                    types = ["profit", "profit", "loss", "breakout", "reversal"]
                    try:
                        weights = [0.4, 0.3, 0.15, 0.1, 0.05]
                        food_type = random.choice(types, weights=weights)
                    except:
                        food_type = random.choice(types)
                    self.food.append((x, y, food_type))
                    break
    
    def move_snake(self):
        head = self.snake[0]
        new = (head[0] + self.dir[0], head[1] + self.dir[1])
        
        # Wall collision
        if not (0 <= new[0] < self.size and 0 <= new[1] < self.size):
            self.teleport_effect()
            return
        
        # Self collision
        if new in self.snake[1:]:
            self.teleport_effect()
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
    
    def take_trade(self, trade_type):
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
            profit_messages = [
                f"EXCELLENT! +${pnl:,}",
                f"GREAT TRADE! +${pnl:,}",
                f"WINNING! +${pnl:,}",
                f"PERFECT! +${pnl:,}"
            ]
            print(f"  {random.choice(profit_messages)}")
            if len(self.snake) < 12:
                self.snake.append(self.snake[-1])
        else:
            self.loss_count += 1
            loss_messages = [
                f"Loss trade: {pnl:,}",
                f"BAD TRADE! {pnl:,}",
                f"MISTAKE! {pnl:,}",
                f"DAMAGE! {pnl:,}"
            ]
            print(f"  {random.choice(loss_messages)}")
    
    def teleport_effect(self):
        old_pos = self.snake[0]
        
        while True:
            x, y = random.randint(0, self.size-1), random.randint(0, self.size-1)
            if (x,y) not in self.snake and not any((x,y)==(f[0],f[1]) for f in self.food):
                self.snake[0] = (x,y)
                self.teleport_count += 1
                
                penalty = 1500 + (self.teleport_count - 1) * 300
                self.money = max(10000, self.money - penalty)
                
                print(f"  TELEPORT! From {old_pos} to ({x},{y})")
                print(f"  Cost: ${penalty:,}")
                
                if len(self.snake) > 2:
                    removed = min(2, len(self.snake) - 1)
                    print(f"  Snake shortened by {removed} segments")
                    for _ in range(removed):
                        if len(self.snake) > 2:
                            self.snake.pop()
                break
    
    def get_keyboard_input(self):
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
        self.clear_screen()
        
        print("=" * 60)
        print("           DETAILED STATISTICS           ")
        print("=" * 60)
        print()
        
        win_rate = (self.win_count / max(1, self.trade_count)) * 100
        current_pnl = self.money - self.initial_money
        
        print("Capital Analysis:")
        print(f"   Initial: ${self.initial_money:,}")
        print(f"   Current: ${self.money:,}")
        print(f"   Net P&L: {current_pnl:+,}")
        print()
        
        print("Performance:")
        print(f"   Total Trades: {self.trade_count}")
        print(f"   Win Rate: {win_rate:.1f}%")
        print(f"   Teleports: {self.teleport_count}")
        print()
        
        if any(self.trade_types.values()):
            print("Trade Types:")
            total = sum(self.trade_types.values())
            for trade_type, count in self.trade_types.items():
                if count > 0:
                    percentage = (count / total) * 100
                    print(f"   {trade_type.capitalize():12}: {count:2d} ({percentage:5.1f}%)")
            print()
        
        print("Press any key to continue...")
        
        try:
            import msvcrt
            msvcrt.getch()
        except:
            input()
    
    def run(self):
        print("Loading Trading Snake - Final Version...")
        time.sleep(2)
        
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
            self.draw_interface()
            
            # Move snake
            current_time = time.time()
            if current_time - last_move_time >= self.game_speed:
                self.move_snake()
                last_move_time = current_time
                self.frame_count += 1
            
            # Check game over
            if self.money < 10000:
                print("\n" + "=" * 60)
                print("              GAME OVER - CAPITAL DEPLETED!              ")
                print("=" * 60)
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
            if self.trade_count >= 30:
                print("\n" + "=" * 60)
                print("                   VICTORY!                   ")
                print(f"            30 Trades Completed!            ")
                print("=" * 60)
                self.show_statistics()
                self.reset_game()
                last_move_time = time.time()
            
            time.sleep(0.05)
        
        print("Thanks for playing!")
    
    def reset_game(self):
        self.snake = [(7,7), (6,7), (5,7)]
        self.dir = (1,0)
        self.money = 100000
        self.food = []
        self.trades = []
        self.trade_count = 0
        self.win_count = 0
        self.loss_count = 0
        self.teleport_count = 0
        self.trade_types = {"profit": 0, "loss": 0, "breakout": 0, "reversal": 0}
        self.frame_count = 0
        self.make_food()

if __name__ == "__main__":
    game = FinalTradingSnake()
    game.run()