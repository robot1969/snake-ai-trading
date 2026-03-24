# Quantitative Trading Snake - Text Demo Version

import random
import time
import os

class TextTradingSnake:
    def __init__(self):
        self.grid_size = 12
        self.snake = [(6, 6), (5, 6), (4, 6)]
        self.direction = (1, 0)
        self.capital = 100000
        self.opportunities = []
        self.score = 0
        self.trades = 0
        self.running = True
        
        # Generate initial trading opportunities
        self.spawn_opportunity()
    
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def draw_grid(self):
        self.clear_screen()
        print("=" * 50)
        print("QUANTITATIVE TRADING SNAKE - Text Demo")
        print("=" * 50)
        print(f"Capital: ${self.capital:,} | P&L: ${self.score:,} | Trades: {self.trades}")
        direction_symbols = {(1,0):'→', (-1,0):'←', (0,-1):'↑', (0,1):'↓'}
        direction_symbol = direction_symbols.get(self.direction, '?')
        print(f"Direction: {direction_symbol}")
        print()
        
        # Draw game area
        for y in range(self.grid_size):
            row = ""
            for x in range(self.grid_size):
                if (x, y) in self.snake:
                    if (x, y) == self.snake[0]:
                        row += "S "
                    else:
                        row += "o "
                elif (x, y) in self.opportunities:
                    opp = next(o for o in self.opportunities if o[0] == x and o[1] == y)
                    symbols = {"profit": "+", "loss": "-", "breakout": "!", "reversal": "R"}
                    row += symbols[opp[2]] + " "
                else:
                    row += ". "
            print(row)
        
        print()
        print("Controls:")
        print("w/s/a/d: Up/Down/Left/Right  q: Quit")
        print("Symbols: + Profit  - Loss  ! Breakout  R Reversal")
        print()
    
    def spawn_opportunity(self):
        if len(self.opportunities) < 3:
            while True:
                x, y = random.randint(0, self.grid_size-1), random.randint(0, self.grid_size-1)
                if (x, y) not in self.snake and (x, y) not in [(o[0], o[1]) for o in self.opportunities]:
                    types = ["profit", "loss", "breakout", "reversal"]
                    weights = [0.4, 0.2, 0.2, 0.2]  # More profit opportunities
                    opp_type = random.choices(types, weights)[0]
                    self.opportunities.append((x, y, opp_type))
                    break
    
    def move(self):
        head = self.snake[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        
        # Boundary collision detection
        if new_head[0] < 0 or new_head[0] >= self.grid_size or new_head[1] < 0 or new_head[1] >= self.grid_size:
            print("WALL HIT! Random teleport...")
            self.teleport_random()
            return
        
        # Self collision detection
        if new_head in self.snake:
            print("SELF COLLISION! Random teleport...")
            self.teleport_random()
            return
        
        self.snake.insert(0, new_head)
        
        # Check if snake eats opportunity
        ate = False
        for opp in self.opportunities[:]:
            if new_head[0] == opp[0] and new_head[1] == opp[1]:
                self.take_opportunity(opp[2])
                self.opportunities.remove(opp)
                ate = True
                break
        
        if not ate:
            self.snake.pop()
        
        # Randomly spawn new opportunities
        if random.random() < 0.3:
            self.spawn_opportunity()
    
    def take_opportunity(self, opp_type):
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
    
    def teleport_random(self):
        old_pos = self.snake[0]
        
        # Teleport penalty
        self.capital = max(10000, self.capital - 2000)
        print(f"Teleport penalty: -$2,000, Remaining: ${self.capital:,}")
        
        # Find random empty position
        empty_positions = []
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                if (x, y) not in self.snake and (x, y) not in [(o[0], o[1]) for o in self.opportunities]:
                    empty_positions.append((x, y))
        
        if empty_positions:
            new_pos = random.choice(empty_positions)
            print(f"Teleported from {old_pos} to {new_pos}")
            self.snake[0] = new_pos
            
            # Shorten snake
            if len(self.snake) > 2:
                self.snake = self.snake[:max(2, len(self.snake)-1)]
                print("Snake shortened")
    
    def get_input(self):
        try:
            key = input("Enter direction (w/s/a/d/q): ").lower().strip()
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
        print("Welcome to Quantitative Trading Snake!")
        print("Control the snake to collect trading opportunities")
        time.sleep(2)
        
        while self.running:
            self.draw_grid()
            self.running = self.get_input()
            
            if self.running:
                self.move()
                
                # Check game over conditions
                if self.capital < 10000:
                    print("GAME OVER - Capital depleted!")
                    self.running = False
                elif self.score > 10000:
                    print("CONGRATULATIONS - Huge profit achieved!")
                    self.running = False
        
        print(f"\nFINAL STATISTICS:")
        print(f"Final Capital: ${self.capital:,}")
        print(f"Total P&L: ${self.score:,}")
        print(f"Total Trades: {self.trades}")
        print(f"Final Snake Length: {len(self.snake)}")
        print("\nThanks for playing!")

if __name__ == "__main__":
    game = TextTradingSnake()
    game.run()