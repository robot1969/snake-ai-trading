# Trading Snake - Simple Arrow Keys Only
# ONLY arrow keys, simple input handling

import random
import os
import time
from collections import deque

class SimpleArrowSnake:
    def __init__(self):
        self.size = 10
        self.snake = [(5,5), (4,5), (3,5)]
        self.dir = (1,0)
        self.money = 100000
        self.initial_money = 100000
        self.food = []
        
        # Statistics
        self.trades = []
        self.trade_count = 0
        self.win_count = 0
        self.loss_count = 0
        self.teleport_count = 0
        
        self.make_food()
        self.frame_count = 0
    
    def clear(self):
        os.system('cls')
    
    def draw_game(self):
        """Draw game"""
        self.clear()
        
        print("=" * 40)
        print("TRADING SNAKE - ARROW KEYS ONLY")
        print("=" * 40)
        print(f"Money: ${self.money:,} | Trades: {self.trade_count}")
        print(f"Direction: {['→','←','↑','↓'][[(1,0),(-1,0),(0,-1),(0,1)].index(self.dir)] if self.dir in [(1,0),(-1,0),(0,-1),(0,1)] else '?'}")
        print("=" * 40)
        
        # Draw grid
        for y in range(self.size):
            for x in range(self.size):
                if (x,y) == self.snake[0]:
                    print("S", end="")
                elif (x,y) in self.snake:
                    print("o", end="")
                elif (x,y) in [f[:2] for f in self.food]:
                    food_type = next(f[2] for f in self.food if f[0]==x and f[1]==y)
                    symbols = {"profit": "$", "loss": "L", "breakout": "B", "reversal": "R"}
                    print(symbols.get(food_type, "?"), end="")
                else:
                    print(".", end="")
            print()
        
        print("=" * 40)
        print("Controls: Arrow Keys | Enter to quit")
        print("Type: up/down/left/right or WASD")
        print(f"Frame: {self.frame_count}")
    
    def make_food(self):
        """Generate food"""
        if len(self.food) < 2:
            while True:
                x, y = random.randint(0,self.size-1), random.randint(0,self.size-1)
                if (x,y) not in self.snake:
                    types = ["profit", "loss"]
                    food_type = random.choice(types)
                    self.food.append((x, y, food_type))
                    break
    
    def move_snake(self):
        """Move snake"""
        head = self.snake[0]
        new = (head[0] + self.dir[0], head[1] + self.dir[1])
        
        # Wall - teleport
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
    
    def take_trade(self, trade_type):
        """Handle trade"""
        if trade_type == "profit":
            pnl = 1000
            self.win_count += 1
            print(f"PROFIT +${pnl}!")
            self.snake.append(self.snake[-1])
        else:
            pnl = -800
            self.loss_count += 1
            print(f"LOSS {pnl}!")
        
        self.money += pnl
        self.trade_count += 1
        self.trades.append(pnl)
    
    def teleport(self):
        """Teleport"""
        while True:
            x, y = random.randint(0,self.size-1), random.randint(0,self.size-1)
            if (x,y) not in self.snake and not any((x,y)==(f[0],f[1]) for f in self.food):
                self.snake[0] = (x,y)
                self.teleport_count += 1
                self.money = max(10000, self.money - 1000)
                print(f"TELEPORT! -1000")
                if len(self.snake) > 2:
                    self.snake.pop()
                break
    
    def get_direction_input(self):
        """Get direction input"""
        print("Enter direction (up/down/left/right/w/a/s/d): ", end="", flush=True)
        
        try:
            import sys
            import select
            
            # Non-blocking input for 0.5 seconds
            if select.select([sys.stdin], [], [], 0.5)[0]:
                key = sys.stdin.readline().strip().lower()
                
                if key in ['up', 'w']:
                    if self.dir != (0, 1):
                        self.dir = (0, -1)
                elif key in ['down', 's']:
                    if self.dir != (0, -1):
                        self.dir = (0, 1)
                elif key in ['left', 'a']:
                    if self.dir != (1, 0):
                        self.dir = (-1, 0)
                elif key in ['right', 'd']:
                    if self.dir != (-1, 0):
                        self.dir = (1, 0)
                elif key in ['quit', 'exit', 'q', 'esc']:
                    return False
        except:
            pass
        
        return True
    
    def run(self):
        """Main game loop"""
        print("TRADING SNAKE - SIMPLE ARROW KEYS VERSION")
        print("Loading...")
        time.sleep(2)
        
        running = True
        
        while running:
            self.draw_game()
            
            # Get input
            running = self.get_direction_input()
            
            if not running:
                break
            
            # Move snake
            self.move_snake()
            self.frame_count += 1
            
            # Check game over
            if self.money < 10000:
                print("\nGAME OVER!")
                print(f"Final Money: ${self.money:,}")
                print(f"Total Trades: {self.trade_count}")
                print("Starting new game...")
                time.sleep(2)
                self.reset_game()
            
            time.sleep(0.1)
        
        print("Thanks for playing!")
    
    def reset_game(self):
        """Reset game"""
        self.snake = [(5,5), (4,5), (3,5)]
        self.dir = (1,0)
        self.money = 100000
        self.food = []
        self.trades = []
        self.trade_count = 0
        self.win_count = 0
        self.loss_count = 0
        self.teleport_count = 0
        self.frame_count = 0
        self.make_food()

if __name__ == "__main__":
    game = SimpleArrowSnake()
    game.run()