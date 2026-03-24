# Trading Snake - Guaranteed GUI Version
# 使用最简单的tkinter实现，确保兼容性

try:
    import tkinter as tk
except ImportError:
    print("Error: tkinter not available")
    exit(1)

import random

class GuaranteedGUISnake:
    def __init__(self):
        try:
            self.root = tk.Tk()
            self.root.title("🐍 量化交易贪吃蛇")
            self.root.geometry("700x500")
            self.root.configure(bg='#2c3e50')
            self.root.resizable(False, False)
            
            # Center window
            self.center_window()
            
            # Game settings
            self.cell_size = 20
            self.grid_width = 14
            self.grid_height = 14
            self.canvas_width = self.grid_width * self.cell_size
            self.canvas_height = self.grid_height * self.cell_size
            
            # Game state
            self.snake = [(7, 7), (6, 7), (5, 7)]
            self.direction = (1, 0)
            self.money = 100000
            self.food = []
            self.trade_count = 0
            self.win_count = 0
            self.game_running = False
            self.game_speed = 300
            
            # Colors
            self.bg_color = '#1a1a1a1'
            self.grid_color = '#2a2a2a2'
            self.snake_color = '#4a8a8a8'
            self.food_color = '#4caf50'
            self.text_color = 'white'
            
            self.setup_ui()
            self.make_food()
            self.draw_game()
            self.update_display()
            
        except Exception as e:
            print(f"GUI Error: {e}")
            return
    
    def center_window(self):
        self.root.update_idletasks()
        try:
            self.root.geometry(
                f"{self.canvas_width + 100}x{self.canvas_height + 100}+100+100"
            )
        except:
            pass
    
    def setup_ui(self):
        # Main container
        main_frame = Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Game canvas
        self.canvas = Canvas(
            main_frame,
            width=self.canvas_width,
            height=self.canvas_height,
            bg=self.grid_color
        )
        self.canvas.pack()
        
        # Info panel
        info_frame = Frame(main_frame, bg='#34495e', width=300)
        info_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)
        
        # Title
        Label(info_frame, text="🐍 量化交易贪吃蛇", font=('Arial', 16, 'bold'),
              bg='#34495e', fg='white').pack(pady=10)
        
        # Money
        self.money_label = Label(info_frame, text="💰 资本: $100,000",
                               font=('Arial', 12),
                               bg='#34495e', fg='white').pack(pady=5)
        
        # Stats
        self.stats_label = Label(info_frame, text="交易: 0 | 胜率: 0% | 传送: 0",
                               font=('Arial', 12),
                               bg='#34495e', fg='white').pack(pady=5)
        
        # Controls
        self.controls_label = Label(info_frame, text="控制: 方向键或WASD",
                               font=('Arial', 11),
                               bg='#34495e', fg='white').pack(pady=10)
        
        # Instructions
        Label(info_frame, text="游戏说明:",
                               font=('Arial', 11),
                               bg='#34495e', fg='white').pack(pady=10)
        
        instructions = [
            "• 方向键/WASD 控制移动",
            "• 绿色块 = 盈利 (+$1,500)",
            "• 红色块 = 亏损 (-$1,200)",
            "• 撞墙自动传送",
            "• 传送会损失金钱",
            "• ESC 键退出游戏",
            "• 空格键暂停/继续",
            "🎯 目标: 30笔交易胜利"
        ]
        
        for instruction in instructions:
            Label(info_frame, text=instruction, font=('Arial', 10),
                  bg='#34495e', fg='white').pack(anchor='w', padx=20)
        
        # Separator
        Frame(info_frame, height=2, bg='white').pack(fill=tk.X, pady=10)
        
        # Start button
        self.start_button = tk.Button(info_frame, text="🎮 开始游戏", font=('Arial', 12, 'bold'),
                                     bg='#4caf50', fg='white',
                                     command=self.start_game)
        self.start_button.pack(pady=10)
        
        # Status
        self.status_label = Label(info_frame, text="按'开始游戏",
                               font=('Arial', 11),
                               bg='#34495e', fg='#81c784')
        self.status_label.pack(pady=10)
        
        # Keyboard bindings
        self.root.bind('<Up>', lambda e: self.change_direction(0, -1))
        self.root.bind('<Down>', lambda e: self.change_direction(0, 1))
        self.root.bind('<Left>', lambda e: self.change_direction(-1, 0))
        self.root.bind('<Right>', lambda e: self.change_direction(1, 0))
        self.root.bind('w', lambda e: self.change_direction(0, -1))
        self.root.bind('s', lambda e: self.change_direction(0, 1))
        self.root.bind('a', lambda e: self.change_direction(-1, 0))
        self.root.bind('d', lambda e: self.change_direction(1, 0))
        self.root.bind('<space>', lambda e: self.toggle_pause())
        self.root.bind('<Escape>', lambda e: self.quit_game())
        
        self.root.focus_set()
    
    def change_direction(self, dx, dy):
        if not self.game_running:
            return
        
        # Prevent reverse direction
        current_dx, current_dy = self.direction
        if (dx == -current_dx and dy == 0) or (dx == 0 and dy == -current_dy):
            return
        if dx == current_dx and dy == current_dy:
            return
        
        self.direction = (dx, dy)
    
    def make_food(self):
        """Generate food"""
        if len(self.food) < 3:
            for _ in range(2):
                x = random.randint(0, self.grid_width - 1)
                y = random.randint(0, self.grid_height - 1)
                
                if (x, y) not in self.snake and not any((x, y) == (f[0], f[1]) for f in self.food):
                    food_type = random.choice(['profit', 'profit', 'loss'])
                    self.food.append((x, y, food_type))
                    break
    
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
        eaten = False
        for i, food in enumerate(self.food):
            if (new_x, new_y) == (food[0], food[1]):
                self.eat_food(food[2], i)
                eaten = True
                break
        
        if not eaten:
            self.snake.pop()
        
        self.make_food()
    
    def eat_food(self, food_type, index):
        """Handle eating food"""
        values = {
            'profit': 1500,
            'loss': -1200,
        }
        base_pnl = values.get(food_type, 1000)
        pnl = int(base_pnl * random.uniform(0.8, 1.3))
        
        self.money += pnl
        self.trade_count += 1
        
        if pnl > 0:
            self.win_count += 1
            self.show_message(f"✨ 盈利 +${pnl:,}")
            if len(self.snake) < 12:
                self.snake.append(self.snake[-1])
        else:
            self.show_message(f"💸 亏损 {pnl:,}")
        
        self.food.pop(index)
    
    def teleport_snake(self):
        """Teleport snake randomly"""
        old_pos = self.snake[0]
        
        for _ in range(3):
            x = random.randint(0, self.grid_width - 1)
            y = random.randint(0, self.grid_height - 1)
            
            # Find empty position
            if (x, y) not in self.snake and not any((x, y) == (f[0], f[1]) for f in self.food):
                self.snake[0] = (x, y)
                self.teleport_count += 1
                
                # Teleport penalty
                penalty = 1500 + (self.teleport_count - 1) * 300
                self.money = max(10000, self.money - penalty)
                self.show_message(f"⚡ 传送! 损失${penalty:,}")
                
                # Shorten snake
                if len(self.snake) > 3:
                    for _ in range(min(2, len(self.snake) - 1)):
                        if len(self.snake) > 2:
                            self.snake.pop()
                
                break
    
    def draw_game(self):
        """Draw game state on canvas"""
        self.canvas.delete("all")
        
        # Draw grid
        for i in range(self.grid_width + 1):
            x = i * self.cell_size
            self.canvas.create_line(x, 0, x, self.canvas_height, fill=self.grid_color, width=1)
        for i in range(self.grid_height + 1):
            y = i * self.cell_size
            self.canvas.create_line(0, y, self.canvas_width, y, fill=self.grid_color, width=1)
        
        # Draw food
        for food in self.food:
            x, y = food[0], food[1]
            food_type = food[2]
            
            # Food color
            if food_type == 'profit':
                color = self.food_color_profit
            elif food_type == 'loss':
                color = '#e74c3c'
            else:
                color = self.food_color_profit
            
            # Draw food circle
            self.canvas.create_oval(
                x + 3, y + 3, x + self.cell_size - 3, y + self.cell_size - 3,
                fill=color, outline='white', width=2
            )
            
            # Symbol
            symbols = {'profit': "$", "loss": "L"}
            symbol = symbols.get(food_type, "$")
            self.canvas.create_text(
                x + self.cell_size//2, y + self.cell_size//2,
                symbol, font=('Arial', 10), fill='white'
            )
        
        # Draw snake
        for i, (x, y) in enumerate(self.snake):
            if i == 0:
                # Snake head
                self.canvas.create_rectangle(
                    x + 2, y + 2, x + self.cell_size - 2, y + self.cell_size - 2,
                    fill=self.snake_color, outline='white', width=2
                )
                
                # Simple eyes
                eye_size = max(2, self.cell_size//6)
                self.canvas.create_oval(
                    x + 5 + eye_size, y + 5 + eye_size,
                    x + self.cell_size - 5 - eye_size, y + 5 + eye_size,
                    fill='white'
                )
            else:
                # Snake body
                self.canvas.create_rectangle(
                    x + 2, y + 2, x + self.cell_size - 2, y + self.cell_size - 2,
                    fill=self.snake_color, outline='white', width=1
                )
    
    def update_display(self):
        """Update information display"""
        current_pnl = self.money - 100000
        win_rate = (self.win_count / max(1, self.trade_count)) * 100 if self.trade_count > 0 else 0
        
        self.money_label.config(text=f"💰 资本: ${self.money:,}")
        
        pnl_color = '#4caf50' if current_pnl >= 0 else '#e74c3c'
        self.pnl_label.config(text=f"📈 盈亏: {current_pnl:+,}")
        self.pnl_label.config(fg=pnl_color)
        
        if self.trades:
            recent_trades = self.trades[-5:] if self.trades else []
            recent_text = "最近: " + " ".join([f"{'+{t:,}' if t > 0 else f'{t:,}'}" for t in recent_trades])
            self.status_label.config(text=recent_text, fg='#81c784')
        else:
            self.status_label.config(text="按'开始游戏", fg='#81c784')
    
    def show_message(self, message):
        """Show temporary message"""
        self.status_label.config(text=message)
        self.root.after(2000, lambda: self.status_label.config(text="按'继续游戏", fg='#81c784'))
    
    def start_game(self):
        """Start the game"""
        if not self.game_running:
            self.game_running = True
            self.start_button.config(state='disabled', text="游戏中...")
            self.status_label.config(text="游戏进行中...", fg='#81c784')
            self.game_loop()
    
    def pause_game(self):
        """Toggle pause state"""
        if self.game_running:
            self.game_running = False
            self.pause_button.config(state='normal', text="▶️ 继续")
            self.status_label.config(text="游戏暂停", fg='#ff9800')
        else:
            self.game_running = True
            self.pause_button.config(text='⏸️ 暂停', state='normal')
            self.status_label.config(text="游戏进行中...", fg='#81c784')
            self.game_loop()
    
    def quit_game(self):
        """Quit game"""
        if messagebox.askyesno("退出游戏", "确定要退出游戏吗？"):
            self.root.quit()
    
    def toggle_pause(self):
        """Toggle pause state"""
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
            
            # Check game conditions
            if self.money < 10000:
                self.game_over()
                return
            
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
        self.status_label.config(text="💔 游戏结束！", fg='#e74c3c')
        
        messagebox.showinfo(
            "游戏结束",
            f"资本耗尽！\n\n最终统计:\n"
            f"最终资本: ${self.money:,}\n"
            f"总交易次数: {self.trade_count}\n"
            f"胜率: {(self.win_count/max(1,self.trade_count))*100:.1f}%\n"
            f"传送次数: {self.teleport_count}\n\n"
        )
        
        self.reset_game()
    
    def victory(self):
        """Handle victory"""
        self.game_running = False
        self.start_button.config(state='normal', text="🎉 重新开始")
        self.pause_button.config(state='disabled')
        self.status_label.config(text="🎉 胜利！", fg='#4caf50')
        
        messagebox.showinfo(
            "胜利！",
            f"恭喜完成30笔交易！\n\n最终统计:\n"
            f"最终资本: ${self.money:,}\n"
            f"净盈亏: ${self.money - 100000:+,}\n"
            f"总交易次数: {self.trade_count}\n"
            f"胜率: {(self.win_count/max(1,self.trade_count))*100:.1f}%\n"
            f"传送次数: {self.teleport_count}\n"
            f"你是交易大师！"
        )
        
        self.reset_game()
    
    def reset_game(self):
        """Reset game state"""
        self.snake = [(7,7), (6,7), (5,7)]
        self.direction = (1,0)
        self.money = 100000
        self.food = []
        self.trade_count = 0
        self.win_count = 0
        self.loss_count = 0
        self.teleport_count = 0
        self.draw_game()
        self.update_display()
        self.status_label.config(text="按'开始游戏")
    
    def run(self):
        """Start the GUI application"""
        self.root.mainloop()

if __name__ == "__main__":
    try:
        game = GuaranteedGUISnake()
        game.run()
    except Exception as e:
        print(f"启动失败: {e}")
        input("按回车键退出...")

if __name__ == "__main__":
    game = GuaranteedGUISnake()
    game.run()