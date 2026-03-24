# Trading Snake - Fixed Arrow Keys Version
# ONLY arrow keys to move snake, FIXED input handling

import random
import os
import time
import threading
from collections import deque

class FixedArrowKeysSnake:
    def __init__(self):
        self.size = 12
        self.snake = [(6,6), (5,6), (4,6)]
        self.dir = (1,0)  # Start moving right
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
        
        # Game settings
        self.game_speed = 0.3
        self.frame_count = 0
        
        self.make_food()
    
    def clear(self):
        os.system('cls')
    
    def draw_interface(self):
        """Draw game interface"""
        self.clear()
        
        # Title and controls
        print("Trading Snake - Arrow Keys Only (FIXED)")
        print("=" * 50)
        print("Arrow Keys: UP/DOWN/LEFT/RIGHT | ESC: Exit")
        print("=" * 50)
        
        # Auto stats
        win_rate = (self.win_count / max(1, self.trade_count)) * 100
        current_pnl = self.money - self.initial_money
        pnl_percentage = (current_pnl / self.initial_money) * 100
        
        print(f"Capital: ${self.money:>10,} | P&L: {current_pnl:+9,} ({pnl_percentage:+5.1f}%)")
        print(f"Trades: {self.trade_count:3d} | Win Rate: {win_rate:5.1f}% | Teleports: {self.teleport_count:2d}")
        
        # Current direction indicator
        dir_symbols = {(1,0):"→", (-1,0):"←", (0,-1):"↑", (0,1):"↓"}
        current_dir = dir_symbols.get(self.dir, "?")
        print(f"Current Direction: {current_dir}")
        
        print("-" * 50)
        
        # Game area
        for y in range(self.size):
            row = ""
            for x in range(self.size):
                if (x,y) == self.snake[0]:
                    row += "@"  # Snake head
                elif (x,y) in self.snake:
                    row += "o"  # Snake body
                elif (x,y) in [f[:2] for f in self.food]:
                    food_type = next(f[2] for f in self.food if f[0]==x and f[1]==y)
                    symbols = {"profit": "$", "loss": "L", "breakout": "B", "reversal": "R"}
                    row += symbols.get(food_type, "?")
                else:
                    row += "."
            print(row)
        
        print("-" * 50)
        print(f"Frame: {self.frame_count} | Press arrow keys to move!")
    
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
    
    def move_snake(self):
        """Move snake in current direction"""
        head = self.snake[0]
        new = (head[0] + self.dir[0], head[1] + self.dir[1])
        
        # Wall collision - teleport
        if not (0 <= new[0] < self.size and 0 <= new[1] < self.size):
            self.teleport()
            return
        
        # Self collision - teleport
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
        
        self.trade_types[trade_type] += 1
        self.trade_values[trade_type].append(pnl)
        
        if pnl > 0:
            self.win_count += 1
            self.profit_total += pnl
            print(f"PROFIT! +${pnl:,}")
            if len(self.snake) < 8:
                self.snake.append(self.snake[-1])
        else:
            self.loss_count += 1
            self.loss_total += pnl
            print(f"LOSS! {pnl:,}")
    
    def teleport(self):
        """Teleport with penalty"""
        while True:
            x, y = random.randint(0,self.size-1), random.randint(0,self.size-1)
            if (x,y) not in self.snake and not any((x,y)==(f[0],f[1]) for f in self.food):
                self.snake[0] = (x,y)
                self.teleport_count += 1
                
                penalty = 2000 + (self.teleport_count - 1) * 500
                self.money = max(10000, self.money - penalty)
                print(f"TELEPORT! -${penalty:,}")
                
                if len(self.snake) > 2:
                    self.snake = self.snake[:-1]
                break
    
    def run(self):
        """Main game loop with FIXED input handling"""
        print("Trading Snake - Arrow Keys Only (FIXED VERSION)")
        print("Loading...")
        time.sleep(2)
        
        running = True
        move_pending = False
        
        def input_thread():
            nonlocal running, move_pending
            while running:
                try:
                    # Use getch-style input for immediate key detection
                    import msvcrt
                    
                    if msvcrt.kbhit():  # Check if key was pressed
                        key = msvcrt.getch()
                        
                        # Handle arrow keys (Windows)
                        if key == b'\xe0':  # Arrow key prefix
                            key = msvcrt.getch()
                            if key == b'H':  # Up arrow
                                if self.dir != (0, 1):
                                    self.dir = (0, -1)
                                    move_pending = True
                            elif key == b'P':  # Down arrow
                                if self.dir != (0, -1):
                                    self.dir = (0, 1)
                                    move_pending = True
                            elif key == b'K':  # Left arrow
                                if self.dir != (1, 0):
                                    self.dir = (-1, 0)
                                    move_pending = True
                            elif key == b'M':  # Right arrow
                                if self.dir != (-1, 0):
                                    self.dir = (1, 0)
                                    move_pending = True
                        
                        # Handle WASD and ESC
                        elif key == b'w' or key == b'W':  # W up
                            if self.dir != (0, 1):
                                self.dir = (0, -1)
                                move_pending = True
                        elif key == b's' or key == b'S':  # S down
                            if self.dir != (0, -1):
                                self.dir = (0, 1)
                                move_pending = True
                        elif key == b'a' or key == b'A':  # A left
                            if self.dir != (1, 0):
                                self.dir = (-1, 0)
                                move_pending = True
                        elif key == b'd' or key == b'D':  # D right
                            if self.dir != (-1, 0):
                                self.dir = (1, 0)
                                move_pending = True
                        elif key == b'\x1b':  # ESC
                            running = False
                
                except ImportError:
                    # Fallback for non-Windows systems
                    import select
                    import sys
                    import tty
                    import termios
                    
                    fd = sys.stdin.fileno()
                    old_settings = termios.tcgetattr(fd)
                    
                    try:
                        tty.setraw(sys.stdin.fileno())
                        if select.select([sys.stdin], [], [], 0.1) == ([sys.stdin], [], []):
                            key = sys.stdin.read(1)
                            
                            if key == '\x1b':  # ESC
                                running = False
                            elif key in ['w', 'W', 'a', 'A', 's', 'S', 'd', 'D']:
                                if key in ['w', 'W'] and self.dir != (0, 1):
                                    self.dir = (0, -1)
                                    move_pending = True
                                elif key in ['s', 'S'] and self.dir != (0, -1):
                                    self.dir = (0, 1)
                                    move_pending = True
                                elif key in ['a', 'A'] and self.dir != (1, 0):
                                    self.dir = (-1, 0)
                                    move_pending = True
                                elif key in ['d', 'D'] and self.dir != (-1, 0):
                                    self.dir = (1, 0)
                                    move_pending = True
                    
                    finally:
                        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                
                except:
                    pass
                
                time.sleep(0.01)  # Small delay to prevent CPU hogging
        
        # Start input thread
        input_thread_obj = threading.Thread(target=input_thread, daemon=True)
        input_thread_obj.start()
        
        # Main game loop
        last_move_time = time.time()
        
        while running:
            self.draw_interface()
            
            # Move snake at fixed intervals
            current_time = time.time()
            if current_time - last_move_time >= self.game_speed:
                self.move_snake()
                last_move_time = current_time
                move_pending = False
                self.frame_count += 1
            
            # Check game over
            if self.money < 10000:
                print("\nGAME OVER - Capital Depleted!")
                print("Press ESC to exit...")
                time.sleep(3)
                # Reset game
                self.reset_game()
                last_move_time = time.time()
            
            time.sleep(0.05)
        
        print("\nThanks for playing!")
        print(f"Final Score: ${self.money:,}")
        print(f"Total Trades: {self.trade_count}")
        print(f"Win Rate: {(self.win_count/max(1,self.trade_count))*100:.1f}%")
    
    def reset_game(self):
        """Reset game for continuous play"""
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

if __name__ == "__main__":
    game = FixedArrowKeysSnake()
    game.run()