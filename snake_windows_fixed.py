# Trading Snake - Windows Native Graphics Version (Fixed for Python 3.14)
# Uses Windows console API for better performance - NO pygame needed!

import random
import os
import time
import sys
import threading
import ctypes
from collections import deque

class WindowsNativeSnake:
    def __init__(self):
        self.size = 20
        self.snake = [(10,10), (9,10), (8,10)]
        self.dir = (1, 0)
        self.money = 100000
        self.initial_money = 100000
        self.food = []
        
        # Statistics
        self.trades = []
        self.money_history = deque([100000], maxlen=30)
        self.trade_count = 0
        self.win_count = 0
        self.loss_count = 0
        self.profit_total = 0
        self.loss_total = 0
        self.teleport_count = 0
        self.trade_types = {"profit": 0, "loss": 0, "breakout": 0, "reversal": 0}
        
        # Game settings
        self.game_speed = 0.2
        self.frame_count = 0
        self.animation_frame = 0
        self.colors = {
            'BLACK': 0,
            'WHITE': 15,
            'RED': 12,
            'GREEN': 10,
            'BLUE': 9,
            'YELLOW': 14,
            'CYAN': 11,
            'MAGENTA': 13,
            'LIGHT_GRAY': 7,
            'DARK_GRAY': 8
        }
        
        # Setup console
        if os.name == 'nt':
            self.setup_console()
        
        self.make_food()
        self.last_input_time = time.time()
    
    def setup_console(self):
        """Setup Windows console for better performance"""
        try:
            kernel32 = ctypes.windll.kernel32
            
            # Enable virtual terminal processing
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 1)
            
            # Set console title
            kernel32.SetConsoleTitleW("Trading Snake - Windows Native Version")
            
            # Hide cursor
            CONSOLE_CURSOR_INFO = ctypes.c_ulong * 2
            kernel32.GetConsoleCursorInfo(kernel32.GetStdHandle(-11), ctypes.byref(CONSOLE_CURSOR_INFO()))
            kernel32.SetConsoleCursorInfo(kernel32.GetStdHandle(-11), ctypes.byref(CONSOLE_CURSOR_INFO(1, CONSOLE_INFO().bVisible)))
        except:
            pass
    
    def set_color(self, color):
        """Set console text color"""
        if os.name == 'nt':
            try:
                import msvcrt
                kernel32 = ctypes.windll.kernel32
                kernel32.SetConsoleTextAttribute(kernel32.GetStdHandle(-11), color)
            except:
                pass
    
    def clear_screen(self):
        """Clear screen efficiently"""
        if os.name == 'nt':
            try:
                kernel32 = ctypes.windll.kernel32
                csbi = (ctypes.c_char * 100)()
                kernel32.GetConsoleScreenBufferInfo(kernel32.GetStdHandle(-11), csbi)
                coord = csbi.dwCursorPosition
                cells = csbi.dwSize.X * csbi.dwSize.Y
                kernel32.FillConsoleOutputCharacter(
                    kernel32.GetStdHandle(-11), ' ', cells,
                    coord, ctypes.byref(ctypes.c_ulong()))
            except:
                pass
        else:
            os.system('clear')
    
    def draw_border(self, text, color=None):
        """Draw text with border"""
        if color is not None and os.name == 'nt':
            self.set_color(color)
        
        border = "+" + "-" * (len(text) + 2) + "+"
        content = "| " + text + " |"
        bottom = "+" + "-" * (len(text) + 2) + "+"
        
        print(border)
        print(content)
        print(bottom)
        
        # Reset color
        if color is not None and os.name == 'nt':
            self.set_color(self.colors['WHITE'])
    
    def draw_enhanced_interface(self):
        """Draw enhanced Windows console interface"""
        self.clear_screen()
        
        # Title
        self.set_color(self.colors['YELLOW'])
        self.draw_border("   TRADING SNAKE - WINDOWS NATIVE VERSION   ", self.colors['YELLOW'])
        
        # Stats
        self.set_color(self.colors['WHITE'])
        win_rate = (self.win_count / max(1, self.trade_count)) * 100
        current_pnl = self.money - self.initial_money
        
        print(f" Capital: ${self.money:>10,}", end="")
        
        if current_pnl > 0:
            self.set_color(self.colors['GREEN'])
            print(f" P&L: {current_pnl:+9,} ↑")
        elif current_pnl < -5000:
            self.set_color(self.colors['RED'])
            print(f" P&L: {current_pnl:+9,} ↓")
        else:
            self.set_color(self.colors['YELLOW'])
            print(f" P&L: {current_pnl:+9,} →")
        
        self.set_color(self.colors['WHITE'])
        print(f" | Trades: {self.trade_count:3d} | Win Rate: {win_rate:5.1f}% | Teleports: {self.teleport_count:2d}")
        
        # Mini chart
        if len(self.money_history) > 1:
            chart_line = " Chart: "
            recent = list(self.money_history)[-10:]
            for money in recent:
                change = money - self.initial_money
                if change >= 0:
                    self.set_color(self.colors['GREEN'])
                    chart_line += "↑"
                else:
                    self.set_color(self.colors['RED'])
                    chart_line += "↓"
            print(f" {chart_line}")
            self.set_color(self.colors['WHITE'])
        
        print("-" * 70)
        
        # Direction
        dir_symbols = {(1,0):">", (-1,0):"<", (0,-1):"^", (0,1):"v"}
        current_dir = dir_symbols.get(self.dir, "?")
        
        self.set_color(self.colors['MAGENTA'])
        print(f" Direction: {current_dir} | Frame: {self.frame_count:4d}")
        self.set_color(self.colors['WHITE'])
        print(" Controls: Arrow Keys or WASD | ESC: Quit | SPACE: Stats")
        
        # Game grid
        print("    " + "".join(f"{x:2d}" for x in range(self.size)))
        
        for y in range(self.size):
            print(f"   {y:2d}", end="")
            
            for x in range(self.size):
                if (x,y) == self.snake[0]:
                    if self.animation_frame % 3 == 0:
                        self.set_color(self.colors['GREEN'])
                        print("@", end="")
                    elif self.animation_frame % 3 == 1:
                        self.set_color(self.colors['YELLOW'])
                        print("@", end="")
                    else:
                        self.set_color(self.colors['CYAN'])
                        print("@", end="")
                elif (x,y) in self.snake:
                    self.set_color(self.colors['BLUE'])
                    print("o", end="")
                elif (x,y) in [f[0:2] for f in self.food]:
                    food_type = food[2]
                    food_colors = {
                        "profit": (self.colors['GREEN'], "$"),
                        "loss": (self.colors['RED'], "L"),
                        "breakout": (self.colors['YELLOW'], "B"),
                        "reversal": (self.colors['MAGENTA'], "R")
                    }
                    color, symbol = food_colors.get(food_type, (self.colors['WHITE'], "?"))
                    self.set_color(color)
                    print(symbol, end="")
                    self.set_color(self.colors['WHITE'])
                else:
                    print(".", end="")
            print()
        
        self.set_color(self.colors['WHITE'])
        print("    " + "-" * (self.size * 3))
        
        # Recent trades
        if self.trades and self.frame_count % 15 == 0:
            print(" Recent: ", end="")
            for trade in self.trades[-5:]:
                if trade > 0:
                    self.set_color(self.colors['GREEN'])
                    print(f"+${trade:,} ", end="")
                else:
                    self.set_color(self.colors['RED'])
                    print(f"{trade:,} ", end="")
                self.set_color(self.colors['WHITE'])
            print()
        
        self.animation_frame += 1
    
    def make_food(self):
        """Generate food"""
        if len(self.food) < 5:
            while True:
                x, y = random.randint(0, self.size-1), random.randint(0, self.size-1)
                if (x,y) not in self.snake and not any((x,y)==(f[0],f[1]) for f in self.food):
                    types = ["profit", "profit", "profit", "loss", "breakout", "reversal"]
                    weights = [0.4, 0.3, 0.1, 0.1, 0.05]
                    try:
                        food_type = random.choice(types, weights=weights)
                    except:
                        # Fallback for Python 3.14 compatibility
                        food_type = random.choice(types)
                    self.food.append((x, y, food_type))
                    break
    
    def move_snake(self):
        """Move snake"""
        head = self.snake[0]
        new = (head[0] + self.dir[0], head[1] + self.dir[1])
        
        # Wall collision
        if not (0 <= new[0] < self.size and 0 <= new[1] < self.size):
            self.teleport_enhanced()
            return
        
        # Self collision
        if new in self.snake[1:]:
            self.teleport_enhanced()
            return
        
        self.snake.insert(0, new)
        
        # Food eating
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
            "profit": 1500, 
            "loss": -1200, 
            "breakout": 2000, 
            "reversal": 2500
        }
        base_pnl = values[trade_type]
        pnl = int(base_pnl * random.uniform(0.7, 1.4))
        
        self.money += pnl
        self.trade_count += 1
        self.trades.append(pnl)
        
        self.trade_types[trade_type] += 1
        
        if pnl > 0:
            self.win_count += 1
            self.profit_total += pnl
            
            profit_messages = [
                f"EXCELLENT! +${pnl:,}",
                f"PERFECT DEAL! +${pnl:,}",
                f"WINNING STREAK! +${pnl:,}"
                f"AMAZING PROFIT! +${pnl:,}"
            ]
            
            self.set_color(self.colors['GREEN'])
            print(f"  {random.choice(profit_messages)}")
            
            if len(self.snake) < 15:
                self.snake.append(self.snake[-1])
                self.set_color(self.colors['WHITE'])
                print(f" Snake length: {len(self.snake)}")
        else:
            self.loss_count += 1
            self.loss_total += pnl
            
            loss_messages = [
                f"Loss trade: {pnl:,}",
                f"BAD TRADE! {pnl:,}",
                f"MISTAKE! {pnl:,}",
                f"DAMAGE! {pnl:,}"
            ]
            
            self.set_color(self.colors['RED'])
            print(f"  {random.choice(loss_messages)}")
        
        self.set_color(self.colors['WHITE'])
    
    def teleport_enhanced(self):
        """Enhanced teleport with visual effects"""
        old_pos = self.snake[0]
        
        while True:
            x, y = random.randint(0, self.size-1), random.randint(0, self.size-1)
            if (x,y) not in self.snake and not any((x,y)==(f[0],f[1]) for f in self.food):
                self.snake[0] = (x,y)
                self.teleport_count += 1
                
                penalty = 1500 + (self.teleport_count - 1) * 250
                self.money = max(10000, self.money - penalty)
                
                # Visual effects
                self.set_color(self.colors['CYAN'])
                print(f"  SPACE-WARP ACTIVATED!")
                self.set_color(self.colors['YELLOW'])
                print(f"  From: {old_pos} → To: ({x},{y})")
                self.set_color(self.colors['RED'])
                print(f"  Cost: ${penalty:,}")
                
                for _ in range(2):
                    self.set_color(self.colors['MAGENTA'])
                    print(f"  ✨✨ TELEPORTING!")
                    time.sleep(0.05)
                    time.sleep(0.05)
                
                if len(self.snake) > 2:
                    self.set_color(self.colors['RED'])
                    print(f"  Snake shortened by 2 segments")
                    for _ in range(2):
                        if len(self.snake) > 2:
                            self.snake.pop()
                    print(f"  Mass reduced!")
                    time.sleep(0.1)
                break
        
        self.set_color(self.colors['WHITE'])
    
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
                
                # WASD keys
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
                    self.show_detailed_statistics()
                
        except ImportError:
            pass
        except:
            pass
        
        return True
    
    def show_detailed_statistics(self):
        """Show detailed statistics"""
        self.clear_screen()
        
        self.set_color(self.colors['YELLOW'])
        self.draw_border("         DETAILED STATISTICS         ", self.colors['YELLOW'])
        
        self.set_color(self.colors['WHITE'])
        print()
        print("💰 Capital Analysis:")
        print(f"   Initial Capital: ${self.initial_money:,}")
        
        win_rate = (self.win_count / max(1, self.trade_count)) * 100
        current_pnl = self.money - self.initial_money
        
        if current_pnl >= 0:
            self.set_color(self.colors['GREEN'])
        else:
            self.set_color(self.colors['RED'])
        print(f"   Current Capital: ${self.money:,}")
        print(f"   Net P&L: {current_pnl:+,}")
        print(f"   Performance: {win_rate:.1f}%")
        print()
        
        if any(self.trade_types.values()):
            self.set_color(self.colors['CYAN'])
            print("📈 Trading Analysis:")
            total = sum(self.trade_types.values())
            for trade_type, count in self.trade_types.items():
                if count > 0:
                    percentage = (count / total) * 100
                    print(f"   {trade_type.capitalize():12}: {count:2d} ({percentage:5.1f}%)")
            print()
        
        self.set_color(self.colors['WHITE'])
        print("Press any key to continue...")
        
        try:
            import msvcrt
            msvcrt.getch()
        except:
            input()
        
        self.set_color(self.colors['WHITE'])
    
    def run(self):
        """Main game loop"""
        self.set_color(self.colors['YELLOW'])
        self.draw_border(" LOADING WINDOWS NATIVE TRADING SNAKE... ", self.colors['YELLOW'])
        self.set_color(self.colors['WHITE'])
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
            self.draw_enhanced_interface()
            
            current_time = time.time()
            if current_time - last_move_time >= self.game_speed:
                self.move_snake()
                last_move_time = current_time
                self.frame_count += 1
            
            if self.money < 10000:
                self.set_color(self.colors['RED'])
                self.draw_border("           GAME OVER - CAPITAL DEPLETED!           ", self.colors['RED'])
                self.set_color(self.colors['WHITE'])
                print()
                print(f"Final Statistics:")
                print(f"   Final Capital: ${self.money:,}")
                print(f"   Total Trades: {self.trade_count}")
                print(f"   Win Rate: {(self.win_count/max(1,self.trade_count))*100:.1f}%")
                print()
                print("Press any key to restart...")
                
                try:
                    import msvcrt
                    msvcrt.getch()
                except:
                    input()
                
                self.reset_game()
                last_move_time = time.time()
            
            if self.trade_count >= 50:
                self.set_color(self.colors['GREEN'])
                self.draw_border("                VICTORY ACHIEVED! 🎉                ", self.colors['GREEN'])
                self.set_color(self.colors['YELLOW'])
                print()
                print(f"OUTSTANDING PERFORMANCE!")
                print(f"   {self.trade_count} Trades Completed!")
                print(f"   Win Rate: {(self.win_count/max(1,self.trade_count))*100:.1f}%")
                print()
                self.show_detailed_statistics()
                self.reset_game()
                last_move_time = time.time()
            
            time.sleep(0.03)
        
        self.set_color(self.colors['WHITE'])
        print("Thanks for playing Trading Snake! 🐍")
    
    def reset_game(self):
        """Reset game"""
        self.snake = [(10,10), (9,10), (8,10)]
        self.dir = (1,0)
        self.money = 100000
        self.food = []
        self.trades = []
        self.money_history = deque([100000], maxlen=30)
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
    game = WindowsNativeSnake()
    game.run()