# Trading Snake - GUI Graphics Version
# Using tkinter for true graphical interface

import tkinter as tk
from tkinter import Canvas, Label, Frame, messagebox
import random
import time
from collections import deque

class GUITradingSnake:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("量化交易贪吃蛇 - 图形版")
        self.root.configure(bg='#1a1a1a')
        self.root.resizable(False, False)
        
        # Game settings
        self.cell_size = 20
        self.grid_width = 20
        self.grid_height = 20
        self.canvas_width = self.grid_width * self.cell_size
        self.canvas_height = self.grid_height * self.cell_size
        
        # Center window on screen
        self.center_window()
        
        # Game state
        self.snake = [(10, 10), (9, 10), (8, 10)]
        self.direction = (1, 0)
        self.money = 100000
        self.initial_money = 100000
        self.food = []
        self.trade_count = 0
        self.win_count = 0
        self.loss_count = 0
        self.teleport_count = 0
        self.trade_types = {"profit": 0, "loss": 0, "breakout": 0, "reversal": 0}
        self.trades = []
        self.game_running = False
        self.game_speed = 150  # milliseconds
        self.food_eaten = False
        
        # Colors
        self.colors = {
            'bg': '#1a1a1a',
            'grid': '#2c3e50',
            'snake': '#4caf50',
            'snake_head': '#8bc34a',
            'food_profit': '#4caf50',
            'food_loss': '#f44336',
            'food_breakout': '#ff9800',
            'food_reversal': '#9c27b0',
            'text': 'white',
            'panel': '#0d47a1'
        }
        
        self.setup_ui()
        self.make_food()
        self.update_display()
    
    def center_window(self):
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (self.canvas_width // 2)
        y = (self.root.winfo_screenheight() // 2) - (self.canvas_height // 2)
        self.root.geometry(f'{self.canvas_width + 400}x{self.canvas_height + 100}+{x}+{y}')
    
    def setup_ui(self):
        # Main frame
        main_frame = Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - Game canvas
        game_frame = Frame(main_frame, bg=self.colors['bg'])
        game_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Canvas for game
        self.canvas = Canvas(
            game_frame,
            width=self.canvas_width,
            height=self.canvas_height,
            bg=self.colors['grid'],
            highlightthickness=0
        )
        self.canvas.pack()
        
        # Right panel - Stats and controls
        info_frame = Frame(main_frame, bg=self.colors['panel'], width=300)
        info_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=10, pady=10)
        info_frame.pack_propagate(False)
        
        # Title in info panel
        title_label = Label(
            info_frame,
            text="🐍 量化交易贪吃蛇",
            font=('Arial', 18, 'bold'),
            bg=self.colors['panel'],
            fg=self.colors['text']
        )
        title_label.pack(pady=10)
        
        # Money display
        self.money_label = Label(
            info_frame,
            text="💰 资本: $100,000",
            font=('Arial', 14, 'bold'),
            bg=self.colors['panel'],
            fg=self.colors['text']
        )
        self.money_label.pack(pady=5)
        
        # P&L display
        self.pnl_label = Label(
            info_frame,
            text="📈 盈亏: +$0",
            font=('Arial', 12),
            bg=self.colors['panel'],
            fg=self.colors['text']
        )
        self.pnl_label.pack(pady=5)
        
        # Trade stats
        self.trades_label = Label(
            info_frame,
            text="🤝 交易次数: 0",
            font=('Arial', 12),
            bg=self.colors['panel'],
            fg=self.colors['text']
        )
        self.trades_label.pack(pady=5)
        
        self.winrate_label = Label(
            info_frame,
            text="🎯 胜率: 0.0%",
            font=('Arial', 12),
            bg=self.colors['panel'],
            fg=self.colors['text']
        )
        self.winrate_label.pack(pady=5)
        
        # Teleport counter
        self.teleport_label = Label(
            info_frame,
            text="⚡ 传送次数: 0",
            font=('Arial', 12),
            bg=self.colors['panel'],
            fg=self.colors['text']
        )
        self.teleport_label.pack(pady=5)
        
        # Separator
        separator = Frame(info_frame, height=2, bg='white')
        separator.pack(fill=tk.X, pady=10)
        
        # Control buttons
        self.start_button = tk.Button(
            info_frame,
            text="🎮 开始游戏",
            font=('Arial', 12, 'bold'),
            bg='#4caf50',
            fg='white',
            command=self.start_game,
            width=15,
            height=2
        )
        self.start_button.pack(pady=5)
        
        self.pause_button = tk.Button(
            info_frame,
            text="⏸️ 暂停",
            font=('Arial', 12),
            bg='#ff9800',
            fg='white',
            command=self.pause_game,
            width=15,
            state='disabled'
        )
        self.pause_button.pack(pady=5)
        
        # Instructions
        instructions_frame = Frame(info_frame, bg=self.colors['panel'])
        instructions_frame.pack(pady=10)
        
        instructions = [
            "📖 操作说明:",
            "方向键: ↑↓←→",
            "或 W/A/S/D 控制",
            "",
            "💰 绿色: 盈利机会",
            "🔴 红色: 亏损机会",
            "🟠 橙色: 突破机会", 
            "🟣 紫色: 反转机会",
            "",
            "⚡ 撞墙自动传送",
            "传送会损失金钱",
            "",
            "ESC 退出游戏"
        ]
        
        for instruction in instructions:
            label = Label(
                instructions_frame,
                text=instruction,
                font=('Arial', 10),
                bg=self.colors['panel'],
                fg=self.colors['text']
            )
            label.pack(anchor='w', pady=2)
        
        # Trade type legend
        legend_frame = Frame(info_frame, bg=self.colors['panel'])
        legend_frame.pack(pady=10)
        
        legend_title = Label(
            legend_frame,
            text="📊 交易类型:",
            font=('Arial', 12, 'bold'),
            bg=self.colors['panel'],
            fg=self.colors['text']
        )
        legend_title.pack(anchor='w', pady=5)
        
        # Draw legend items with colors
        legend_items = [
            ("💰", "盈利交易 +$1,500"),
            ("🔴", "亏损交易 -$1,200"),
            ("🟠", "突破 +$2,000"),
            ("🟣", "反转 +$2,500")
        ]
        
        for symbol, description in legend_items:
            item_frame = Frame(legend_frame, bg=self.colors['panel'])
            item_frame.pack(anchor='w', pady=2)
            
            # Color indicator
            color_label = Label(
                item_frame,
                text="  " + symbol,
                font=('Arial', 12),
                bg=self.colors['panel'],
                fg=self.colors['text']
            )
            color_label.pack(side='left')
            
            # Description
            desc_label = Label(
                item_frame,
                text=description,
                font=('Arial', 10),
                bg=self.colors['panel'],
                fg=self.colors['text']
            )
            desc_label.pack(side='left', padx=10)
        
        # Status message
        self.status_label = Label(
            info_frame,
            text="按 '开始游戏' 开始",
            font=('Arial', 11, 'italic'),
            bg=self.colors['panel'],
            fg='#81c784'
        )
        self.status_label.pack(pady=10)
        
        # Recent trades
        self.recent_trades_label = Label(
            info_frame,
            text="最近交易: -",
            font=('Arial', 10),
            bg=self.colors['panel'],
            fg=self.colors['text']
        )
        self.recent_trades_label.pack(anchor='w', pady=5)
        
        # Bind keyboard events
        self.root.bind('<Up>', lambda e: self.change_direction(0, -1))
        self.root.bind('<Down>', lambda e: self.change_direction(0, 1))
        self.root.bind('<Left>', lambda e: self.change_direction(-1, 0))
        self.root.bind('<Right>', lambda e: self.change_direction(1, 0))
        
        # WASD keys
        self.root.bind('w', lambda e: self.change_direction(0, -1))
        self.root.bind('s', lambda e: self.change_direction(0, 1))
        self.root.bind('a', lambda e: self.change_direction(-1, 0))
        self.root.bind('d', lambda e: self.change_direction(1, 0))
        self.root.bind('W', lambda e: self.change_direction(0, -1))
        self.root.bind('S', lambda e: self.change_direction(0, 1))
        self.root.bind('A', lambda e: self.change_direction(-1, 0))
        self.root.bind('D', lambda e: self.change_direction(1, 0))
        
        self.root.bind('<space>', lambda e: self.toggle_pause())
        self.root.bind('<Escape>', lambda e: self.quit_game())
        
        # Focus on window
        self.root.focus_set()
    
    def change_direction(self, dx, dy):
        """Change snake direction"""
        if not self.game_running:
            return
        
        # Prevent reverse direction
        current_dx, current_dy = self.direction
        
        # Check if new direction is opposite to current
        if (dx == -current_dx and dy == 0) or (dx == 0 and dy == -current_dy):
            return
            
        # Check if new direction is same as current (prevent redundant calls)
        if dx == current_dx and dy == current_dy:
            return
            
        self.direction = (dx, dy)
    
    def make_food(self):
        """Generate food items"""
        while len(self.food) < 4:
            x = random.randint(0, self.grid_width - 1)
            y = random.randint(0, self.grid_height - 1)
            
            # Check if position is not occupied
            if (x, y) not in self.snake and not any((x, y) == (f[0], f[1]) for f in self.food):
                # Random food type with weights
                types = ["profit", "profit", "loss", "breakout", "reversal"]
                weights = [0.4, 0.3, 0.15, 0.1, 0.05]
                try:
                    food_type = random.choice(types, weights=weights)
                except:
                    food_type = random.choice(types)
                self.food.append((x, y, food_type))
    
    def move_snake(self):
        """Move the snake"""
        if not self.game_running:
            return
            
        head_x, head_y = self.snake[0]
        new_x = head_x + self.direction[0]
        new_y = head_y + self.direction[1]
        
        # Check wall collision
        if new_x < 0 or new_x >= self.grid_width or new_y < 0 or new_y >= self.grid_height:
            self.teleport_snake()
            return
        
        # Check self collision
        if (new_x, new_y) in self.snake[1:]:
            self.teleport_snake()
            return
        
        # Move snake
        self.snake.insert(0, (new_x, new_y))
        
        # Check food collision
        for i, food in enumerate(self.food):
            if (new_x, new_y) == (food[0], food[1]):
                self.eat_food(food[2], i)
                break
        
        if not self.food_eaten:
            self.snake.pop()
        
        self.food_eaten = False
        self.make_food()
    
    def eat_food(self, food_type, index):
        """Handle eating food"""
        values = {
            "profit": 1500,
            "loss": -1200,
            "breakout": 2000,
            "reversal": 2500
        }
        base_pnl = values[food_type]
        pnl = int(base_pnl * random.uniform(0.8, 1.3))
        
        self.money += pnl
        self.trade_count += 1
        self.trades.append(pnl)
        
        # Update statistics
        self.trade_types[food_type] += 1
        if pnl > 0:
            self.win_count += 1
            self.show_message(f"🎉 盈利! +${pnl:,}", '#4caf50')
            if len(self.snake) < 15:
                self.snake.append(self.snake[-1])
        else:
            self.loss_count += 1
            self.show_message(f"💸 亏损! {pnl:,}", '#f44336')
        
        # Remove eaten food
        self.food.pop(index)
        self.food_eaten = True
    
    def teleport_snake(self):
        """Teleport snake to random position"""
        old_pos = self.snake[0]
        
        while True:
            x = random.randint(0, self.grid_width - 1)
            y = random.randint(0, self.grid_height - 1)
            
            # Find empty position
            if (x, y) not in self.snake and not any((x, y) == (f[0], f[1]) for f in self.food):
                self.snake[0] = (x, y)
                self.teleport_count += 1
                
                # Teleport penalty
                penalty = 1500 + (self.teleport_count - 1) * 300
                self.money = max(10000, self.money - penalty)
                
                self.show_message(f"⚡ 传送! 费用 ${penalty:,}", '#ff9800')
                
                # Shorten snake
                if len(self.snake) > 3:
                    removed = min(2, len(self.snake) - 1)
                    for _ in range(removed):
                        if len(self.snake) > 2:
                            self.snake.pop()
                
                break
    
    def draw_game(self):
        """Draw the game on canvas"""
        self.canvas.delete("all")
        
        # Draw grid
        for i in range(self.grid_width + 1):
            x = i * self.cell_size
            self.canvas.create_line(x, 0, x, self.canvas_height, fill=self.colors['grid'], width=1)
        
        for i in range(self.grid_height + 1):
            y = i * self.cell_size
            self.canvas.create_line(0, y, self.canvas_width, y, fill=self.colors['grid'], width=1)
        
        # Draw food
        for food in self.food:
            x, y = food[0], food[1]
            food_type = food[2]
            
            # Food color based on type
            if food_type == "profit":
                color = self.colors['food_profit']
            elif food_type == "loss":
                color = self.colors['food_loss']
            elif food_type == "breakout":
                color = self.colors['food_breakout']
            elif food_type == "reversal":
                color = self.colors['food_reversal']
            else:
                color = self.colors['food_profit']
            
            # Draw food circle
            self.canvas.create_oval(
                x + 2, y + 2, x + self.cell_size - 2, y + self.cell_size - 2,
                fill=color,
                outline='white',
                width=2
            )
            
            # Add symbol
            symbols = {"profit": "$", "loss": "L", "breakout": "B", "reversal": "R"}
            symbol = symbols.get(food_type, "$")
            self.canvas.create_text(
                x + self.cell_size//2, y + self.cell_size//2,
                symbol,
                font=('Arial', 12, 'bold'),
                fill='white'
            )
        
        # Draw snake
        for i, segment in enumerate(self.snake):
            x, y = segment
            
            if i == 0:
                # Snake head
                self.canvas.create_rectangle(
                    x + 1, y + 1, x + self.cell_size - 1, y + self.cell_size - 1,
                    fill=self.colors['snake_head'],
                    outline='white',
                    width=2
                )
                
                # Eyes
                eye_size = 3
                self.canvas.create_oval(
                    x + 4, y + 5, x + 4 + eye_size, y + 5 + eye_size,
                    fill='white'
                )
                self.canvas.create_oval(
                    x + self.cell_size - 7, y + 5, x + self.cell_size - 7 + eye_size, y + 5 + eye_size,
                    fill='white'
                )
            else:
                # Snake body
                self.canvas.create_rectangle(
                    x + 2, y + 2, x + self.cell_size - 2, y + self.cell_size - 2,
                    fill=self.colors['snake'],
                    outline='white',
                    width=1
                )
    
    def update_display(self):
        """Update information display"""
        current_pnl = self.money - self.initial_money
        win_rate = (self.win_count / max(1, self.trade_count)) * 100
        
        # Update labels
        self.money_label.config(text=f"💰 资本: ${self.money:,}")
        
        pnl_color = '#4caf50' if current_pnl >= 0 else '#f44336'
        self.pnl_label.config(text=f"📈 盈亏: {current_pnl:+,}")
        self.pnl_label.config(fg=pnl_color)
        
        self.trades_label.config(text=f"🤝 交易次数: {self.trade_count}")
        self.winrate_label.config(text=f"🎯 胜率: {win_rate:.1f}%")
        self.teleport_label.config(text=f"⚡ 传送次数: {self.teleport_count}")
        
        # Update recent trades
        if self.trades:
            recent_trades = self.trades[-3:]  # Last 3 trades
            recent_text = "最近: " + " ".join([f"{'+' if t > 0 else ''}${t:,}" for t in recent_trades])
            self.recent_trades_label.config(text=recent_text)
    
    def show_message(self, message, color='#4caf50'):
        """Show temporary message"""
        self.status_label.config(text=message, fg=color)
        self.root.after(2000, lambda: self.status_label.config(text="游戏进行中...", fg='#81c784'))
    
    def start_game(self):
        """Start the game"""
        if not self.game_running:
            self.game_running = True
            self.start_button.config(state='disabled', text="游戏中...")
            self.pause_button.config(state='normal')
            self.status_label.config(text="游戏进行中...", fg='#81c784')
            self.game_loop()
    
    def pause_game(self):
        """Pause/unpause the game"""
        if self.game_running:
            self.game_running = False
            self.pause_button.config(text="▶️ 继续")
            self.status_label.config(text="游戏暂停", fg='#ff9800')
        else:
            self.game_running = True
            self.pause_button.config(text="⏸️ 暂停")
            self.status_label.config(text="游戏进行中...", fg='#81c784')
            self.game_loop()
    
    def quit_game(self):
        """Quit game"""
        if messagebox.askyesno("退出游戏", "确定要退出游戏吗？"):
            self.root.quit()
    
    def toggle_pause(self):
        """Toggle pause with spacebar"""
        if self.game_running:
            self.pause_game()
        else:
            self.start_game()
    
    def game_loop(self):
        """Main game loop"""
        if self.game_running:
            self.move_snake()
            self.draw_game()
            self.update_display()
            
            # Check game over
            if self.money < 10000:
                self.game_over()
                return
            
            # Check victory condition
            if self.trade_count >= 30:
                self.victory()
                return
            
            # Schedule next frame
            self.root.after(self.game_speed, self.game_loop)
    
    def game_over(self):
        """Handle game over"""
        self.game_running = False
        self.start_button.config(state='normal', text="🎮 重新开始")
        self.pause_button.config(state='disabled')
        self.status_label.config(text="💔 游戏结束！", fg='#f44336')
        
        # Show game over message
        messagebox.showinfo(
            "游戏结束",
            f"资本耗尽！\n\n最终统计:\n"
            f"最终资本: ${self.money:,}\n"
            f"总交易次数: {self.trade_count}\n"
            f"胜率: {(self.win_count/max(1,self.trade_count))*100:.1f}%\n"
            f"传送次数: {self.teleport_count}\n\n"
            f"点击'重新开始'再玩一次！"
        )
        
        # Reset game
        self.reset_game()
    
    def victory(self):
        """Handle victory"""
        self.game_running = False
        self.start_button.config(state='normal', text="🎮 重新开始")
        self.pause_button.config(state='disabled')
        self.status_label.config(text="🎉 胜利！", fg='#4caf50')
        
        # Show victory message
        messagebox.showinfo(
            "胜利！",
            f"恭喜完成30笔交易！\n\n最终统计:\n"
            f"最终资本: ${self.money:,}\n"
            f"净盈亏: ${self.money - self.initial_money:+,}\n"
            f"总交易次数: {self.trade_count}\n"
            f"胜率: {(self.win_count/max(1,self.trade_count))*100:.1f}%\n"
            f"传送次数: {self.teleport_count}\n\n"
            f"你是交易大师！"
        )
        
        # Reset game
        self.reset_game()
    
    def reset_game(self):
        """Reset game state"""
        self.snake = [(10, 10), (9, 10), (8, 10)]
        self.direction = (1, 0)
        self.money = 100000
        self.food = []
        self.trade_count = 0
        self.win_count = 0
        self.loss_count = 0
        self.teleport_count = 0
        self.trade_types = {"profit": 0, "loss": 0, "breakout": 0, "reversal": 0}
        self.trades = []
        self.make_food()
        self.draw_game()
        self.update_display()
    
    def run(self):
        """Start the GUI application"""
        self.root.mainloop()

if __name__ == "__main__":
    game = GUITradingSnake()
    game.run()