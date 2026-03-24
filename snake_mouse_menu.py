# Trading Snake - Mouse Menu Control Version
# Only arrow keys for movement, everything else via mouse menus

import random
import os
import time
import threading
from collections import deque

class MouseMenuSnake:
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
        
        # Menu system
        self.current_menu = "game"  # game, stats, charts, settings, pause
        self.menu_cursor = 0
        self.game_speed = 0.25
        self.auto_move = False
        self.show_help = False
        
        self.make_food()
        self.last_update = time.time()
        
        # Menu items for each menu
        self.menus = {
            "pause": [
                "Resume Game",
                "View Statistics", 
                "View Charts",
                "Settings",
                "Restart Game",
                "Main Menu"
            ],
            "stats": [
                "Back to Game",
                "Detailed Analysis",
                "Trade History",
                "Performance Metrics"
            ],
            "charts": [
                "Back to Game", 
                "Capital Chart",
                "P&L Distribution",
                "Trade Types"
            ],
            "settings": [
                "Back to Game",
                "Game Speed: Normal",
                "Auto Move: OFF",
                "Show Grid: ON",
                "Sound Effects: OFF"
            ],
            "main": [
                "Start New Game",
                "Instructions",
                "About",
                "Exit"
            ]
        }
    
    def clear(self):
        os.system('cls')
    
    def draw_menu_header(self, title):
        """Draw menu header"""
        print("=" * 60)
        print(f"  {title}")
        print("=" * 60)
    
    def draw_menu_item(self, item, index, cursor_pos):
        """Draw single menu item"""
        if index == cursor_pos:
            print(f"> {item} <")
        else:
            print(f"  {item}")
    
    def draw_menu(self, menu_type):
        """Draw menu with cursor"""
        self.clear()
        
        titles = {
            "pause": "GAME PAUSED",
            "stats": "STATISTICS MENU",
            "charts": "CHARTS MENU", 
            "settings": "SETTINGS MENU",
            "main": "MAIN MENU"
        }
        
        self.draw_menu_header(titles.get(menu_type, "MENU"))
        
        menu_items = self.menus.get(menu_type, [])
        for i, item in enumerate(menu_items):
            self.draw_menu_item(item, i, self.menu_cursor)
        
        print("\n" + "=" * 60)
        print("Controls: Arrow Keys= Navigate | Enter= Select | ESC= Back")
        print("Movement Keys: WASD (only during gameplay)")
    
    def update_menu_item(self, menu_type, index, new_text):
        """Update specific menu item text"""
        if menu_type in self.menus and index < len(self.menus[menu_type]):
            self.menus[menu_type][index] = new_text
    
    def handle_menu_selection(self, menu_type):
        """Handle menu item selection"""
        items = self.menus.get(menu_type, [])
        if not items or self.menu_cursor >= len(items):
            return "game"
        
        selected = items[self.menu_cursor]
        
        if menu_type == "pause":
            if selected == "Resume Game":
                return "game"
            elif selected == "View Statistics":
                return "stats"
            elif selected == "View Charts":
                return "charts"
            elif selected == "Settings":
                return "settings"
            elif selected == "Restart Game":
                self.reset_game()
                return "game"
            elif selected == "Main Menu":
                return "main"
        
        elif menu_type == "stats":
            if selected == "Back to Game":
                return "game"
            elif selected == "Detailed Analysis":
                self.show_detailed_stats()
                return "stats"
            elif selected == "Trade History":
                self.show_trade_history()
                return "stats"
            elif selected == "Performance Metrics":
                self.show_performance_metrics()
                return "stats"
        
        elif menu_type == "charts":
            if selected == "Back to Game":
                return "game"
            elif selected == "Capital Chart":
                self.show_capital_chart()
                return "charts"
            elif selected == "P&L Distribution":
                self.show_pnl_chart()
                return "charts"
            elif selected == "Trade Types":
                self.show_trade_types_chart()
                return "charts"
        
        elif menu_type == "settings":
            if selected == "Back to Game":
                return "game"
            elif selected.startswith("Game Speed"):
                # Cycle through speeds
                speeds = ["Slow", "Normal", "Fast", "Ultra"]
                current = selected.split(":")[1].strip()
                idx = speeds.index(current)
                new_speed = speeds[(idx + 1) % len(speeds)]
                speed_values = {"Slow": 0.4, "Normal": 0.25, "Fast": 0.15, "Ultra": 0.1}
                self.game_speed = speed_values[new_speed]
                self.update_menu_item("settings", 1, f"Game Speed: {new_speed}")
                return "settings"
            elif selected.startswith("Auto Move"):
                self.auto_move = not self.auto_move
                status = "ON" if self.auto_move else "OFF"
                self.update_menu_item("settings", 2, f"Auto Move: {status}")
                return "settings"
        
        elif menu_type == "main":
            if selected == "Start New Game":
                self.reset_game()
                return "game"
            elif selected == "Instructions":
                self.show_instructions()
                return "main"
            elif selected == "About":
                self.show_about()
                return "main"
            elif selected == "Exit":
                return "exit"
        
        return "game"
    
    def draw_game_screen(self):
        """Draw main game screen"""
        self.clear()
        print("Trading Snake - Mouse Menu Control")
        print("=" * 60)
        
        # Game stats row
        win_rate = (self.win_count / max(1, self.trade_count)) * 100
        current_pnl = self.money - self.initial_money
        pnl_percentage = (current_pnl / self.initial_money) * 100
        
        print(f"Capital: ${self.money:>10,} | P&L: {current_pnl:>+9,} ({pnl_percentage:+5.1f}%)")
        print(f"Trades: {self.trade_count:3d} | Win Rate: {win_rate:5.1f}% | Teleports: {self.teleport_count:2d}")
        
        # Menu hint
        print(f"\nMenu Options: [P]ause [S]tatistics [C]harts [T]oggle Settings")
        print("-" * 60)
        
        # Game area
        for y in range(self.size):
            row = ""
            for x in range(self.size):
                if (x,y) == self.snake[0]:
                    row += "S"
                elif (x,y) in self.snake:
                    row += "o"
                elif (x,y) in [f[:2] for f in self.food]:
                    food_type = next(f[2] for f in self.food if f[0]==x and f[1]==y)
                    symbols = {"profit": "$", "loss": "L", "breakout": "B", "reversal": "R"}
                    row += symbols.get(food_type, "?")
                else:
                    row += "."
            print(row)
        
        print("-" * 60)
        print("Movement: WASD | Menu: P/S/C/T | Q=Quit")
    
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
            
            if len(self.money_history) > 1:
                volatility = (max(self.money_history) - min(self.money_history)) / self.initial_money * 100
                print(f"Volatility: {volatility:.1f}%")
        
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
        print("How to Play")
        print("=" * 60)
        print("MOVEMENT:")
        print("  W/A/S/D - Move snake (arrow keys also work)")
        print("\nMENU CONTROLS:")
        print("  P - Pause/Resume Menu")
        print("  S - Statistics Menu") 
        print("  C - Charts Menu")
        print("  T - Settings Menu")
        print("\nMENU NAVIGATION:")
        print("  Arrow Keys - Navigate menu")
        print("  Enter - Select menu item")
        print("  ESC - Go back")
        print("\nGAMEPLAY:")
        print("  $ - Profit opportunity (+$1,500)")
        print("  L - Loss opportunity (-$1,200)")
        print("  B - Breakout opportunity (+$2,000)")
        print("  R - Reversal opportunity (+$2,500)")
        print("\n  Hit walls or yourself = Teleport penalty")
        print("  Game ends when capital < $10,000")
        
        print("\nPress Enter to continue...")
        input()
    
    def show_about(self):
        """Show about"""
        self.clear()
        print("About Trading Snake")
        print("=" * 60)
        print("A quantitative trading education game")
        print("that combines classic snake gameplay")
        print("with real trading concepts.")
        print("\nFeatures:")
        print("• Mouse menu control system")
        print("• Real-time statistics tracking")
        print("• Multiple trade types")
        print("• Risk management mechanics")
        print("• Performance analysis tools")
        print("\nVersion 1.0")
        print("Created for educational purposes")
        
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
        """Main game loop"""
        print("Trading Snake - Mouse Menu Control Version")
        print("Loading...")
        time.sleep(1)
        
        import threading
        running = True
        
        def input_thread():
            nonlocal running
            while running:
                try:
                    key = input().lower()
                    
                    if self.current_menu == "game":
                        # Game controls
                        if key == 'q':
                            running = False
                        elif key == 'p':
                            self.current_menu = "pause"
                            self.menu_cursor = 0
                        elif key == 's':
                            self.current_menu = "stats"
                            self.menu_cursor = 0
                        elif key == 'c':
                            self.current_menu = "charts"
                            self.menu_cursor = 0
                        elif key == 't':
                            self.current_menu = "settings"
                            self.menu_cursor = 0
                        elif key == 'w' and self.dir != (0,1):
                            self.dir = (0,-1)
                        elif key == 's' and self.dir != (0,-1):
                            self.dir = (0,1)
                        elif key == 'a' and self.dir != (1,0):
                            self.dir = (-1,0)
                        elif key == 'd' and self.dir != (-1,0):
                            self.dir = (1,0)
                    
                    elif self.current_menu in self.menus:
                        # Menu navigation
                        if key == 'esc':
                            if self.current_menu in ["stats", "charts", "settings"]:
                                self.current_menu = "game"
                            elif self.current_menu == "pause":
                                self.current_menu = "game"
                            elif self.current_menu == "main":
                                self.current_menu = "game"
                        elif key == 'enter':
                            new_menu = self.handle_menu_selection(self.current_menu)
                            if new_menu == "exit":
                                running = False
                            elif new_menu != self.current_menu:
                                self.current_menu = new_menu
                                self.menu_cursor = 0
                        elif key == 'up':
                            self.menu_cursor = (self.menu_cursor - 1) % len(self.menus[self.current_menu])
                        elif key == 'down':
                            self.menu_cursor = (self.menu_cursor + 1) % len(self.menus[self.current_menu])
                
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
                self.draw_menu(self.current_menu)
                time.sleep(0.1)
            
            # Check game over
            if self.money < 10000:
                self.clear()
                print("GAME OVER - Capital Depleted!")
                print(f"Final Capital: ${self.money:,}")
                print(f"Total Trades: {self.trade_count}")
                print(f"Win Rate: {(self.win_count/max(1,self.trade_count))*100:.1f}%")
                time.sleep(3)
                self.current_menu = "main"
                self.menu_cursor = 0
                self.reset_game()

if __name__ == "__main__":
    game = MouseMenuSnake()
    game.run()