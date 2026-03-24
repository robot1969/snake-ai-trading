# Trading Snake - Simple GUI Version
# Simplified tkinter version for better compatibility

import tkinter as tk
from tkinter import Canvas, Label, Frame, messagebox
import random
import time
from collections import deque

class SimpleGUISnake:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🐍 量化交易贪吃蛇")
        self.root.configure(bg='#2c3e50')
        
        # Game settings
        self.cell_size = 25
        self.grid_width = 16
        self.grid_height = 16
        self.canvas_width = self.grid_width * self.cell_size
        self.canvas_height = self.grid_height * self.cell_size
        
        # Game state
        self.snake = [(8, 8), (7, 8), (6, 8)]
        self.direction = (1, 0)
        self.money = 100000
        self.food = []
        self.trade_count = 0
        self.win_count = 0
        self.game_running = False
        self.game_speed = 200
        
        # Create UI
        self.setup_ui()
        self.make_food()
        self.draw_game()
        self.update_stats()
    
    def setup_ui(self):
        # Main container
        main_container = Frame(self.root, bg='#2c3e50')
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = Label(
            main_container,
            text="🐍 量化交易贪吃蛇 - 图形版",
            font=('Arial', 16, 'bold'),
            bg='#2c3e50',
            fg='white'
        )
        title_label.pack(pady=(0, 10))
        
        # Game area
        game_frame = Frame(main_container, bg='#1b5e20')
        game_frame.pack(fill=tk.BOTH, expand=True)
        
        # Canvas
        self.canvas = Canvas(
            game_frame,
            width=self.canvas_width,
            height=self.canvas_height,
            bg='#0f3460'
        )
        self.canvas.pack()
        
        # Stats frame
        stats_frame = Frame(main_container, bg='#2c3e50')
        stats_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Money
        self.money_label = Label(
            stats_frame,
            text="💰 资本: $100,000",
            font=('Arial', 14, 'bold'),
            bg='#2c3e50',
            fg='white'
        )
        self.money_label.pack(pady=5)
        
        # P&L
        self.pnl_label = Label(
            stats_frame,
            text="📈 盈亏: +$0",
            font=('Arial', 12),
            bg='#2c3e50',
            fg='white'
        )
        self.pnl_label.pack(pady=5)
        
        # Trades
        self.trades_label = Label(
            stats_frame,
            text="🤝 交易: 0",
            font=('Arial', 12),
            bg='#2c3e50',
            fg='white'
        )
        self.trades_label.pack(pady=5)
        
        # Win rate
        self.winrate_label = Label(
            stats_frame,
            text="🎯 胜率: 0%",
            font=('Arial', 12),
            bg='#2c3e50',
            fg='white'
        )
        self.winrate_label.pack(pady=5)
        
        # Buttons
        button_frame = Frame(stats_frame, bg='#2c3e50')
        button_frame.pack(pady=10)
        
        self.start_button = tk.Button(
            button_frame,
            text="🎮 开始",
            font=('Arial', 12, 'bold'),
            bg='#4caf50',
            fg='white',
            command=self.start_game
        )
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.pause_button = tk.Button(
            button_frame,
            text="⏸️ 暂停",
            font=('Arial', 12),
            bg='#ff9800',
            fg='white',
            command=self.pause_game,
            state='disabled'
        )
        self.pause_button.pack(side=tk.LEFT, padx=5)
        
        # Status
        self.status_label = Label(
            main_container,
            text="按 '开始游戏' 开始",
            font=('Arial', 11),
            bg='#2c3e50',
            fg='#ffeb3b'
        )
        self.status_label.pack(pady=(10, 0))
        
        # Instructions
        instructions = [
            "🎮 控制: 方向键 或 WASD",
            "💰 绿色: 盈利 +$1,500",
            "🔴 红色: 亏损 -$1,200", 
            "📊 撞墙自动传送"
            "⚡ 传送费用: $1,500+",
            "🎯 目标: 30笔交易胜利"
        ]
        
        for instruction in instructions:
            label = Label(
                main_container,
                text=instruction,
                font=('Arial', 10),
                bg='#2c3e50',
                fg='white'
            )
            label.pack(anchor='w', padx=(20, 0))
        
        # Bind keys
        self.root.bind('<Key>', self.on_key_press)
        
        # Focus
        self.root.focus_set()
    
    def on_key_press(self, event):
        """Handle keyboard input"""
        key = event.keysym.lower()
        
        if not self.game_running:
            if key == 'space':
                self.start_game()
            elif key == 'escape':
                self.quit_game()
            return
        
        # Movement keys
        if key in ('up', 'w'):
            if self.direction != (0, 1):
                self.direction = (0, -1)
        elif key in ('down', 's'):
            if self.direction != (0, -1):
                self.direction = (0, 1)
        elif key in ('left', 'a'):
            if self.direction != (1, 0):
                self.direction = (-1, 0)
        elif key in ('right', 'd'):
            if self.direction != (-1, 0):
                self.direction = (1, 0)
        elif key == 'space':
            self.pause_game()
        elif key == 'escape':
            self.game_running = False
            self.status_label.config(text="游戏暂停")
    
    def make_food(self):
        """Generate food"""
        while len(self.food) < 3:
            x = random.randint(0, self.grid_width - 1)
            y = random.randint(0, self.grid_height - 1)
            
            # Check empty position
            if (x, y) not in self.snake and not any((x, y) == (f[0], f[1]) for f in self.food):
                # Food type with simple random
                food_type = random.choice(['profit', 'profit', 'loss', 'breakout', 'reversal'])
                self.food.append((x, y, food_type))
    
    def move_snake(self):
        """Move snake"""
        if not self.game_running:
            return
        
        head_x, head_y = self.snake[0]
        new_x = head_x + self.direction[0]
        new_y = head_y + self.direction[1]
        
        # Wall collision - teleport
        if new_x < 0 or new_x >= self.grid_width or new_y < 0 or new_y >= self.grid_height:
            self.teleport_snake()
            return
        
        # Self collision - teleport
        if (new_x, new_y) in self.snake[1:]:
            self.teleport_snake()
            return
        
        self.snake.insert(0, (new_x, new_y))
        
        # Food collision
        for i, food in enumerate(self.food):
            if (new_x, new_y) == (food[0], food[1]):
                self.eat_food(food[2], i)
                break
        
        # Remove tail if no food eaten
        if len(self.snake) > 3 and not hasattr(self, 'food_eaten'):
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
        base_pnl = values.get(food_type, 1000)
        pnl = int(base_pnl * random.uniform(0.8, 1.3))
        
        self.money += pnl
        self.trade_count += 1
        
        # Update statistics
        if pnl > 0:
            self.win_count += 1
            self.status_label.config(text=f"🎉 盈利 +${pnl:,}!", fg='#4caf50')
            if len(self.snake) < 12:
                self.snake.append(self.snake[-1])
        else:
            self.status_label.config(text=f"💸 亏损 {pnl:,}", fg='#f44336')
        
        # Remove eaten food
        self.food.pop(index)
        self.food_eaten = True
        
        # Update display
        self.draw_game()
        self.update_stats()
    
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
                penalty = 1500 + (self.teleport_count - 1) * 500
                self.money = max(10000, self.money - penalty)
                
                self.status_label.config(text=f"⚡ 传送! 费用 ${penalty:,}", fg='#ff9800')
                
                # Shorten snake
                if len(self.snake) > 3:
                    for _ in range(min(2, len(self.snake) - 1)):
                        if len(self.snake) > 2:
                            self.snake.pop()
                
                break
    
    def draw_game(self):
        """Draw game on canvas"""
        self.canvas.delete("all")
        
        # Draw grid
        for i in range(self.grid_width + 1):
            x = i * self.cell_size
            self.canvas.create_line(x, 0, x, self.canvas_height, fill='#34495e', width=1)
        for i in range(self.grid_height + 1):
            y = i * self.cell_size
            self.canvas.create_line(0, y, self.canvas_width, y, fill='#34495e', width=1)
        
        # Draw food
        for food in self.food:
            x, y = food[0], food[1]
            food_type = food[2]
            
            # Food colors
            if food_type == "profit":
                color = '#4caf50'
            elif food_type == "loss":
                color = '#f44336'
            elif food_type == "breakout":
                color = '#ff9800'
            elif food_type == "reversal":
                color = '#9c27b0'
            else:
                color = '#4caf50'
            
            # Draw food circle
            self.canvas.create_oval(
                x + 3, y + 3, x + self.cell_size - 3, y + self.cell_size - 3,
                fill=color, outline='white', width=2
            )
            
            # Add symbol
            symbols = {"profit": "$", "loss": "L", "breakout": "B", "reversal": "R"}
            symbol = symbols.get(food_type, "$")
            self.canvas.create_text(
                x + self.cell_size//2, y + self.cell_size//2,
                symbol,
                font=('Arial', 12, 'bold'), fill='white'
            )
        
        # Draw snake
        for i, (x, y) in enumerate(self.snake):
            if i == 0:
                # Snake head
                self.canvas.create_rectangle(
                    x + 2, y + 2, x + self.cell_size - 2, y + self.cell_size - 2,
                    fill='#8bc34a', outline='white', width=2
                )
                # Eyes
                eye_size = 4
                self.canvas.create_oval(
                    x + 5, y + 6, x + 5 + eye_size, y + 6 + eye_size,
                    fill='white'
                )
                self.canvas.create_oval(
                    x + self.cell_size - 9, y + 6, x + self.cell_size - 9 + eye_size, y + 6 + eye_size,
                    fill='white'
                )
            else:
                # Snake body
                self.canvas.create_rectangle(
                    x + 3, y + 3, x + self.cell_size - 3, y + self.cell_size - 3,
                    fill='#4caf50', outline='white', width=1
                )
    
    def update_stats(self):
        """Update statistics display"""
        current_pnl = self.money - 100000
        win_rate = (self.win_count / max(1, self.trade_count)) * 100
        
        pnl_color = '#4caf50' if current_pnl >= 0 else '#f44336'
        
        self.money_label.config(text=f"💰 资本: ${self.money:,}")
        self.pnl_label.config(text=f"📈 盈亏: {current_pnl:+,}")
        self.pnl_label.config(fg=pnl_color)
        self.trades_label.config(text=f"🤝 交易: {self.trade_count}")
        self.winrate_label.config(text=f"🎯 胜率: {win_rate:.1f}%")
    
    def game_loop(self):
        """Main game loop"""
        if self.game_running:
            self.move_snake()
            self.draw_game()
            self.update_stats()
            
            # Check game over
            if self.money < 10000:
                self.game_over()
                return
            
            # Check victory
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
        self.status_label.config(text="💔 游戏结束!", fg='#f44336')
        
        messagebox.showinfo(
            "游戏结束",
            f"资本耗尽！\n\n最终统计:\n"
            f"最终资本: ${self.money:,}\n"
            f"总交易次数: {self.trade_count}\n"
            f"胜率: {(self.win_count/max(1,self.trade_count))*100:.1f}%\n"
            f"传送次数: {self.teleport_count}\n\n"
            f"点击'重新开始'再玩一次！"
        )
        
        self.reset_game()
    
    def victory(self):
        """Handle victory"""
        self.game_running = False
        self.start_button.config(state='normal', text="🎮 重新开始")
        self.pause_button.config(state='disabled')
        self.status_label.config(text="🎉 胜利！", fg='#4caf50')
        
        messagebox.showinfo(
            "胜利！",
            f"恭喜完成30笔交易！\n\n最终统计:\n"
            f"最终资本: ${self.money:,}\n"
            f"净盈亏: ${self.money - 100000:+,}\n"
            f"总交易次数: {self.trade_count}\n"
            f"胜率: {(self.win_count/max(1,self.trade_count))*100:.1f}%\n\n"
            f"你是交易大师！"
        )
        
        self.reset_game()
    
    def reset_game(self):
        """Reset game"""
        self.snake = [(8, 8), (7, 8), (6, 8)]
        self.direction = (1, 0)
        self.money = 100000
        self.food = []
        self.trade_count = 0
        self.win_count = 0
        self.loss_count = 0
        self.teleport_count = 0
        self.draw_game()
        self.update_stats()
    
    def start_game(self):
        """Start the game"""
        if not self.game_running:
            self.game_running = True
            self.start_button.config(state='disabled', text="游戏中...")
            self.pause_button.config(state='normal')
            self.status_label.config(text="游戏进行中...", fg='#ffeb3b')
            self.game_loop()
    
    def pause_game(self):
        """Pause/unpause"""
        if self.game_running:
            self.game_running = False
            self.pause_button.config(text="▶️ 继续")
            self.status_label.config(text="游戏暂停", fg='#ff9800')
        else:
            self.game_running = True
            self.pause_button.config(text="⏸️ 暂停")
            self.status_label.config(text="游戏进行中...", fg='#ffeb3b')
            self.game_loop()
    
    def quit_game(self):
        """Quit game"""
        if messagebox.askyesno("退出游戏", "确定要退出游戏吗？"):
            self.root.destroy()
    
    def run(self):
        """Start the GUI application"""
        self.root.mainloop()

if __name__ "__main__":
    game = SimpleGUISnake()
    game.run()