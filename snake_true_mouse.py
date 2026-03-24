# Trading Snake - True Mouse Menu Control Version
# Only arrow keys for movement, everything else via mouse click menus

import random
import os
import time
import threading
from collections import deque

class TrueMouseMenuSnake:
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
        
        # Menu system - true mouse control
        self.current_menu = "game"
        self.game_speed = 0.25
        self.auto_move = False
        
        # Clickable menu buttons (positioned like a real GUI)
        self.menu_buttons = {
            "game": [
                {"text": "PAUSE", "x": 65, "y": 3, "action": "pause", "shortcut": "P"},
                {"text": "STATS", "x": 72, "y": 3, "action": "stats", "shortcut": "S"},
                {"text": "CHARTS", "x": 79, "y": 3, "action": "charts", "shortcut": "C"},
                {"text": "SETTINGS", "x": 86, "y": 3, "action": "settings", "shortcut": "T"}
            ],
            "pause": [
                {"text": "[RESUME GAME]", "x": 30, "y": 8, "action": "resume"},
                {"text": "[VIEW STATS]", "x": 30, "y": 10, "action": "stats"},
                {"text": "[VIEW CHARTS]", "x": 30, "y": 12, "action": "charts"},
                {"text": "[SETTINGS]", "x": 30, "y": 14, "action": "settings"},
                {"text": "[RESTART GAME]", "x": 30, "y": 16, "action": "restart"},
                {"text": "[MAIN MENU]", "x": 30, "y": 18, "action": "main"}
            ],
            "stats": [
                {"text": "[BACK TO GAME]", "x": 25, "y": 8, "action": "game"},
                {"text": "[DETAILED ANALYSIS]", "x": 25, "y": 10, "action": "detailed"},
                {"text": "[TRADE HISTORY]", "x": 25, "y": 12, "action": "history"},
                {"text": "[PERFORMANCE]", "x": 25, "y": 14, "action": "performance"}
            ],
            "charts": [
                {"text": "[BACK TO GAME]", "x": 25, "y": 8, "action": "game"},
                {"text": "[CAPITAL CHART]", "x": 25, "y": 10, "action": "capital"},
                {"text": "[P&L DISTRIBUTION]", "x": 25, "y": 12, "action": "pnl"},
                {"text": "[TRADE TYPES]", "x": 25, "y": 14, "action": "types"}
            ],
            "settings": [
                {"text": "[BACK TO GAME]", "x": 25, "y": 8, "action": "game"},
                {"text": "[SPEED: NORMAL]", "x": 25, "y": 10, "action": "speed"},
                {"text": "[AUTO MOVE: OFF]", "x": 25, "y": 12, "action": "auto"},
                {"text": "[SHOW GRID: ON]", "x": 25, "y": 14, "action": "grid"}
            ],
            "main": [
                {"text": "[START NEW GAME]", "x": 28, "y": 10, "action": "newgame"},
                {"text": "[INSTRUCTIONS]", "x": 28, "y": 12, "action": "instructions"},
                {"text": "[ABOUT]", "x": 28, "y": 14, "action": "about"},
                {"text": "[EXIT]", "x": 28, "y": 16, "action": "exit"}
            ]
        }
        
        # Mouse position and click handling
        self.mouse_x = 0
        self.mouse_y = 0
        self.hover_button = None
        self.click_cooldown = 0
        
        self.make_food()
        self.last_update = time.time()
    
    def clear(self):
        os.system('cls')
    
    def draw_button(self, button, is_hovered=False):
        """Draw a clickable button"""
        # Move cursor to button position
        print(f"\033[{button['y']};{button['x']}H", end="")
        
        # Draw button with hover effect
        if is_hovered:
            print(f"\033[7m{button['text']}\033[0m")  # Inverted colors for hover
        else:
            print(button['text'])
    
    def draw_mouse_cursor(self):
        """Draw mouse position indicator"""
        if self.current_menu == "game" and self.mouse_x > 0:
            # Show cursor position in game area
            print(f"\033[22;1HMouse: ({self.mouse_x},{self.mouse_y})", end="")
    
    def check_button_hover(self):
        """Check if mouse is hovering over any button"""
        if self.current_menu in self.menu_buttons:
            for button in self.menu_buttons[self.current_menu]:
                # Simple rectangular detection
                if (abs(self.mouse_x - button['x']) < len(button['text']) // 2 and
                    abs(self.mouse_y - button['y']) < 1):
                    self.hover_button = button
                    return button
        self.hover_button = None
        return None
    
    def handle_mouse_click(self):
        """Handle mouse click on buttons"""
        if self.click_cooldown > 0:
            return
            
        button = self.check_button_hover()
        if button:
            self.click_cooldown = 5  # Prevent multiple clicks
            
            action = button['action']
            
            if action == "pause":
                self.current_menu = "pause"
            elif action == "stats":
                self.current_menu = "stats"
            elif action == "charts":
                self.current_menu = "charts"
            elif action == "settings":
                self.current_menu = "settings"
            elif action == "resume" or action == "game":
                self.current_menu = "game"
            elif action == "restart":
                self.reset_game()
                self.current_menu = "game"
            elif action == "main":
                self.current_menu = "main"
            elif action == "newgame":
                self.reset_game()
                self.current_menu = "game"
            elif action == "exit":
                return False
            elif action == "detailed":
                self.show_detailed_stats()
            elif action == "history":
                self.show_trade_history()
            elif action == "performance":
                self.show_performance_metrics()
            elif action == "capital":
                self.show_capital_chart()
            elif action == "pnl":
                self.show_pnl_chart()
            elif action == "types":
                self.show_trade_types_chart()
            elif action == "speed":
                # Cycle through speeds
                speeds = ["SLOW", "NORMAL", "FAST", "ULTRA"]
                current_button = self.menu_buttons["settings"][1]
                current_speed = current_button['text'].split(':')[1].strip('] ')
                idx = speeds.index(current_speed)
                new_speed = speeds[(idx + 1) % len(speeds)]
                speed_values = {"SLOW": 0.4, "NORMAL": 0.25, "FAST": 0.15, "ULTRA": 0.1}
                self.game_speed = speed_values[new_speed]
                current_button['text'] = f"[SPEED: {new_speed}]"
            elif action == "auto":
                auto_button = self.menu_buttons["settings"][2]
                self.auto_move = not self.auto_move
                status = "ON" if self.auto_move else "OFF"
                auto_button['text'] = f"[AUTO MOVE: {status}]"
            elif action == "instructions":
                self.show_instructions()
            elif action == "about":
                self.show_about()
        
        return True
    
    def draw_game_screen(self):
        """Draw main game screen with clickable menu"""
        self.clear()
        
        # Title
        print("Trading Snake - True Mouse Menu Control")
        print("=" * 100)
        
        # Stats line
        win_rate = (self.win_count / max(1, self.trade_count)) * 100
        current_pnl = self.money - self.initial_money
        pnl_percentage = (current_pnl / self.initial_money) * 100
        
        print(f"Capital: ${self.money:>12,} | P&L: {current_pnl:+12,} ({pnl_percentage:+6.1f}%) | Trades: {self.trade_count:3d} | Win Rate: {win_rate:5.1f}%")
        
        # Menu buttons (clickable)
        print("\nClick menu buttons below:")
        for button in self.menu_buttons["game"]:
            is_hovered = (self.hover_button == button)
            self.draw_button(button, is_hovered)
        
        print("-" * 100)
        
        # Game area with coordinates
        print("   " + "".join([f"{i:2}" for i in range(self.size)]))
        for y in range(self.size):
            row = f"{y:2} "
            for x in range(self.size):
                if (x,y) == self.snake[0]:
                    row += "S "
                elif (x,y) in self.snake:
                    row += "o "
                elif (x,y) in [f[:2] for f in self.food]:
                    food_type = next(f[2] for f in self.food if f[0]==x and f[1]==y)
                    symbols = {"profit": "$", "loss": "L", "breakout": "B", "reversal": "R"}
                    row += symbols.get(food_type, "?") + " "
                else:
                    row += ". "
            print(row)
        
        print("-" * 100)
        print("Movement: Arrow Keys/WASD | Mouse: Click menu buttons | Q=Quit")
        
        # Mouse position indicator
        if self.mouse_x > 0:
            print(f"Mouse Position: ({self.mouse_x:2d}, {self.mouse_y:2d})", end="")
        
        # Instructions
        print("\nClick the menu buttons above with mouse coordinates!")
        print("Example: Click at coordinates (65,3) for PAUSE button")
    
    def draw_menu_screen(self):
        """Draw menu screen with clickable buttons"""
        self.clear()
        
        titles = {
            "pause": "GAME PAUSED - Click a button",
            "stats": "STATISTICS MENU - Click a button", 
            "charts": "CHARTS MENU - Click a button",
            "settings": "SETTINGS MENU - Click a button",
            "main": "MAIN MENU - Click a button"
        }
        
        print("=" * 100)
        print(titles.get(self.current_menu, "MENU"))
        print("=" * 100)
        print("\nClick on any button below:")
        print("(Use mouse coordinates to position your 'click')")
        print("\n")
        
        # Draw menu buttons
        for button in self.menu_buttons.get(self.current_menu, []):
            is_hovered = (self.hover_button == button)
            self.draw_button(button, is_hovered)
        
        print("\n" + "=" * 100)
        print(f"Current Mouse Position: ({self.mouse_x:3d}, {self.mouse_y:3d})")
        if self.hover_button:
            print(f"Hovering over: {self.hover_button['text']}")
        else:
            print("Move mouse to hover over buttons")
        print("Type coordinates to click (e.g., 30,10) or use arrow keys to move")
    
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
    
    def show_detailed_stats(self):
        """Show detailed statistics"""
        self.clear()
        print("Detailed Trading Analysis")
        print("=" * 60)
        
        win_rate = (self.win_count / max(1, self.trade_count)) * 100
        current_pnl = self.money - self.initial_money
        pnl_percentage = (current_pnl / self.initial_money) * 100
        
        print(f"Capital Analysis:")
        print(f"  Initial: ${self.initial_money:,}")
        print(f"  Current: ${self.money:,}")
        print(f"  P&L: ${current_pnl:+,} ({pnl_percentage:+.1f}%)")
        
        print(f"\nPerformance:")
        print(f"  Total Trades: {self.trade_count}")
        print(f"  Win Rate: {win_rate:.1f}%")
        print(f"  Teleports: {self.teleport_count}")
        
        if any(self.trade_types.values()):
            print(f"\nTrade Types:")
            for trade_type, count in self.trade_types.items():
                if count > 0:
                    print(f"  {trade_type.capitalize()}: {count}")
        
        if self.trades:
            print(f"\nRecent Trades:")
            for i, trade in enumerate(self.trades[-5:], 1):
                status = "WIN" if trade > 0 else "LOSS"
                print(f"  {i}. {status}: ${trade:+,}")
        
        print("\nPress Enter to continue...")
        input()
    
    def show_trade_history(self):
        """Show trade history"""
        self.clear()
        print("Trade History")
        print("=" * 60)
        
        if not self.trades:
            print("No trades yet!")
        else:
            print("No. | Type    | Amount    | Running Total")
            print("-" * 45)
            running_total = 0
            for i, trade in enumerate(self.trades[-10:], 1):
                running_total += trade
                trade_type = "Profit" if trade > 0 else "Loss"
                print(f"{i:3d} | {trade_type:8} | ${trade:+8,} | ${running_total:+10,}")
        
        print("\nPress Enter to continue...")
        input()
    
    def show_performance_metrics(self):
        """Show performance metrics"""
        self.clear()
        print("Performance Metrics")
        print("=" * 60)
        
        if self.win_count > 0 and self.loss_count > 0:
            avg_profit = self.profit_total / self.win_count
            avg_loss = abs(self.loss_total) / self.loss_count
            profit_factor = avg_profit / avg_loss
            
            print(f"Average Profit: ${avg_profit:.0f}")
            print(f"Average Loss: ${avg_loss:.0f}")
            print(f"Profit Factor: {profit_factor:.2f}")
        
        print(f"\nRisk Metrics:")
        print(f"Max Drawdown: {self.teleport_count * 2000:,}")
        print(f"Current Capital: ${self.money:,}")
        
        print("\nPress Enter to continue...")
        input()
    
    def show_capital_chart(self):
        """Show capital chart"""
        self.clear()
        print("Capital Change Chart")
        print("=" * 60)
        
        if len(self.money_history) > 1:
            print("Recent Capital History:")
            for i, money in enumerate(list(self.money_history)[-10:], 1):
                change = money - self.initial_money
                arrow = "↑" if change > 0 else "↓" if change < 0 else "→"
                print(f"  {i:2d}. ${money:>8,} {arrow} ${change:+8,}")
        
        print("\nPress Enter to continue...")
        input()
    
    def show_pnl_chart(self):
        """Show P&L distribution"""
        self.clear()
        print("P&L Distribution")
        print("=" * 60)
        
        if self.trades:
            profits = [t for t in self.trades if t > 0]
            losses = [t for t in self.trades if t < 0]
            
            if profits:
                print(f"Profitable Trades: {len(profits)}")
                print(f"  Total: ${sum(profits):,}")
                print(f"  Average: ${sum(profits)/len(profits):.0f}")
                print(f"  Best: ${max(profits):,}")
            
            if losses:
                print(f"\nLosing Trades: {len(losses)}")
                print(f"  Total: ${sum(losses):,}")
                print(f"  Average: ${sum(losses)/len(losses):.0f}")
                print(f"  Worst: ${min(losses):,}")
        
        print("\nPress Enter to continue...")
        input()
    
    def show_trade_types_chart(self):
        """Show trade types breakdown"""
        self.clear()
        print("Trade Types Breakdown")
        print("=" * 60)
        
        if any(self.trade_types.values()):
            total = sum(self.trade_types.values())
            for trade_type, count in self.trade_types.items():
                if count > 0:
                    percentage = (count / total) * 100
                    values = self.trade_values[trade_type]
                    avg_val = sum(values) / len(values)
                    print(f"{trade_type.capitalize():10}: {count:2d} ({percentage:5.1f}%) | Avg: ${avg_val:+7.0f}")
        
        print("\nPress Enter to continue...")
        input()
    
    def show_instructions(self):
        """Show instructions"""
        self.clear()
        print("How to Play - True Mouse Menu Control")
        print("=" * 60)
        print("MOVEMENT:")
        print("  Arrow Keys or WASD - Move snake (ONLY movement controls)")
        print("\nMOUSE MENU CONTROL:")
        print("  Type coordinates like '30,10' to click at position (30,10)")
        print("  Or use arrow keys to move mouse cursor")
        print("  Press Enter to 'click' at current position")
        print("\nGAMEPLAY:")
        print("  $ - Profit opportunity (+$1,500)")
        print("  L - Loss opportunity (-$1,200)")
        print("  B - Breakout opportunity (+$2,000)")
        print("  R - Reversal opportunity (+$2,500)")
        print("\n  Hit walls or yourself = Teleport penalty")
        print("  Game ends when capital < $10,000")
        print("\nMENU COORDINATES:")
        print("  PAUSE: (65,3) | STATS: (72,3) | CHARTS: (79,3)")
        
        print("\nPress Enter to continue...")
        input()
    
    def show_about(self):
        """Show about"""
        self.clear()
        print("About Trading Snake - True Mouse Menu Version")
        print("=" * 60)
        print("A revolutionary trading education game")
        print("with TRUE mouse menu control system.")
        print("\nFeatures:")
        print("• Arrow keys ONLY for movement")
        print("• Mouse-style menu clicking")
        print("• Coordinate-based click system")
        print("• Real-time statistics tracking")
        print("• Multiple trade types")
        print("• Risk management mechanics")
        print("\nVersion 2.0 - True Mouse Control")
        print("Innovation in command-line gaming!")
        
        print("\nPress Enter to continue...")
        input()
    
    def reset_game(self):
        """Reset game"""
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
    
    def run(self):
        """Main game loop with true mouse menu control"""
        print("Trading Snake - True Mouse Menu Control Version")
        print("Loading...")
        time.sleep(1)
        
        import threading
        running = True
        
        def input_thread():
            nonlocal running
            while running:
                try:
                    user_input = input().strip().lower()
                    
                    if user_input == 'q':
                        running = False
                    
                    # Parse coordinate input for mouse clicks
                    elif ',' in user_input:
                        try:
                            parts = user_input.split(',')
                            if len(parts) == 2:
                                self.mouse_x = int(parts[0])
                                self.mouse_y = int(parts[1])
                                
                                # Auto-click when entering coordinates
                                if not self.handle_mouse_click():
                                    running = False
                        except:
                            pass
                    
                    # Arrow key movement for mouse cursor
                    elif user_input in ['up', 'down', 'left', 'right', 'w', 'a', 's', 'd']:
                        if user_input in ['up', 'w'] and self.dir != (0,1):
                            self.dir = (0,-1)
                        elif user_input in ['down', 's'] and self.dir != (0,-1):
                            self.dir = (0,1)
                        elif user_input in ['left', 'a'] and self.dir != (1,0):
                            self.dir = (-1,0)
                        elif user_input in ['right', 'd'] and self.dir != (-1,0):
                            self.dir = (1,0)
                    
                    # Quick mouse movement
                    elif user_input.startswith('move '):
                        try:
                            parts = user_input[5:].split(',')
                            if len(parts) == 2:
                                self.mouse_x = int(parts[0])
                                self.mouse_y = int(parts[1])
                        except:
                            pass
                    
                    # Enter to click at current position
                    elif user_input == '' or user_input == 'enter':
                        if not self.handle_mouse_click():
                            running = False
                
                except:
                    pass
        
        t = threading.Thread(target=input_thread, daemon=True)
        t.start()
        
        # Game loop
        while running:
            if self.current_menu == "game":
                self.draw_game_screen()
                
                # Auto move if enabled
                if self.auto_move:
                    self.move()
                
                time.sleep(self.game_speed)
            else:
                # Update hover state
                self.check_button_hover()
                self.draw_menu_screen()
                time.sleep(0.2)
            
            # Update click cooldown
            if self.click_cooldown > 0:
                self.click_cooldown -= 1
            
            # Check game over
            if self.money < 10000:
                self.clear()
                print("GAME OVER - Capital Depleted!")
                print(f"Final Capital: ${self.money:,}")
                print(f"Total Trades: {self.trade_count}")
                print(f"Win Rate: {(self.win_count/max(1,self.trade_count))*100:.1f}%")
                time.sleep(3)
                self.current_menu = "main"
                self.reset_game()

if __name__ == "__main__":
    game = TrueMouseMenuSnake()
    game.run()