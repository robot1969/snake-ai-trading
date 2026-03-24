#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
量化交易贪吃蛇游戏 - 修复版
Fixed Version without Threading Issues
"""

import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
import math
from collections import deque, defaultdict

class TradingSnakeFixed:
    def __init__(self, root):
        self.root = root
        self.root.title("🐍 量化交易贪吃蛇 - 修复版")
        self.root.configure(bg='#0a0a0f')
        self.root.geometry("1200x800")
        
        # 性能优化参数
        self.max_history_points = 100
        self.chart_update_interval = 500
        self.last_chart_update = 0
        
        # 游戏核心参数
        self.canvas_width = 600
        self.canvas_height = 600
        self.grid_size = 20
        self.cell_size = self.canvas_width // self.grid_size
        
        # 游戏状态
        self.snake = deque([(10, 10)], maxlen=400)
        self.direction = (1, 0)
        self.food = None
        self.game_running = False
        self.game_paused = False
        self.game_speed = 150
        self.score = 0
        self.capital = 10000
        self.trades = deque(maxlen=50)
        self.teleport_count = 0
        self.food_lifetime = 0
        self.game_time = 0
        
        # AI优化参数
        self.ai_mode = True
        self.ai_q_table = {}
        self.ai_learning_rate = 0.1
        self.ai_epsilon = 0.1
        self.ai_collision_count = 0
        self.ai_food_collected = 0
        
        # 数据记录（使用deque限制内存）
        self.capital_history = deque(maxlen=self.max_history_points)
        self.score_history = deque(maxlen=self.max_history_points)
        self.message_history = deque(maxlen=50)
        
        # 性能监控（移除多线程）
        self.fps_counter = 0
        self.fps_last_time = time.time()
        self.current_fps = 0
        
        # 创建UI
        self.setup_ui()
        self.bind_keys()
        
    def setup_ui(self):
        main_container = tk.Frame(self.root, bg='#0a0a0f')
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 左侧游戏区域
        game_frame = tk.Frame(main_container, bg='#1a1a2e', relief=tk.RAISED, bd=2)
        game_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)
        
        # 游戏画布
        self.canvas = tk.Canvas(game_frame, width=self.canvas_width, height=self.canvas_height, 
                               bg='#0a0a0f', highlightthickness=2, highlightbackground='#4a4a6e')
        self.canvas.pack(padx=10, pady=10)
        
        # 控制面板
        control_frame = tk.Frame(game_frame, bg='#1a1a2e')
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.start_button = tk.Button(control_frame, text="🎮 开始", command=self.start_game,
                                     bg='#4caf50', fg='white', font=('Arial', 10, 'bold'), width=10)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.pause_button = tk.Button(control_frame, text="⏸️ 暂停", command=self.toggle_pause,
                                     bg='#ff9800', fg='white', font=('Arial', 10, 'bold'), width=10, state='disabled')
        self.pause_button.pack(side=tk.LEFT, padx=5)
        
        self.reset_button = tk.Button(control_frame, text="🔄 重置", command=self.reset_game,
                                     bg='#f44336', fg='white', font=('Arial', 10, 'bold'), width=10)
        self.reset_button.pack(side=tk.LEFT, padx=5)
        
        # 状态显示
        status_frame = tk.Frame(game_frame, bg='#1a1a2e')
        status_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.status_label = tk.Label(status_frame, text="准备就绪", font=('Arial', 10, 'bold'),
                                    bg='#1a1a2e', fg='#00ff00')
        self.status_label.pack()
        
        # 分数和资金显示
        score_frame = tk.Frame(game_frame, bg='#1a1a2e')
        score_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.score_label = tk.Label(score_frame, text=f"分数: {self.score}", 
                                   font=('Arial', 12, 'bold'), bg='#1a1a2e', fg='#ffd700')
        self.score_label.pack(side=tk.LEFT, padx=10)
        
        self.capital_label = tk.Label(score_frame, text=f"资金: ${self.capital:,}", 
                                     font=('Arial', 12, 'bold'), bg='#1a1a2e', fg='#4caf50')
        self.capital_label.pack(side=tk.LEFT, padx=10)
        
        self.fps_label = tk.Label(score_frame, text=f"FPS: {self.current_fps}", 
                                  font=('Arial', 10), bg='#1a1a2e', fg='#00bcd4')
        self.fps_label.pack(side=tk.RIGHT, padx=10)
        
        # 右侧信息区域
        info_frame = tk.Frame(main_container, bg='#1a1a2e', relief=tk.RAISED, bd=2)
        info_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        tk.Label(info_frame, text="📊 实时数据", font=('Arial', 14, 'bold'),
                bg='#1a1a2e', fg='#ffffff').pack(pady=10)
        
        # 实时信息文本
        self.info_text = tk.Text(info_frame, height=20, width=40, bg='#0f0f1e', fg='#00ff00', 
                                font=('Consolas', 9), relief=tk.FLAT)
        self.info_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # 滚动条
        scrollbar = ttk.Scrollbar(self.info_text)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.info_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.info_text.yview)
        
    def bind_keys(self):
        self.root.bind('<space>', lambda e: self.toggle_pause())
        self.root.bind('<Escape>', lambda e: self.quit_game())
        
    def generate_food(self):
        while True:
            x = random.randint(0, self.grid_size - 1)
            y = random.randint(0, self.grid_size - 1)
            if (x, y) not in self.snake:
                self.food = (x, y)
                self.food_lifetime = random.randint(50, 150)
                break
                
    def draw_game(self):
        self.canvas.delete("all")
        
        # 绘制网格
        for i in range(0, self.canvas_width, self.cell_size):
            self.canvas.create_line(i, 0, i, self.canvas_height, fill='#1a1a2e', width=1)
        for i in range(0, self.canvas_height, self.cell_size):
            self.canvas.create_line(0, i, self.canvas_width, i, fill='#1a1a2e', width=1)
            
        # 绘制蛇
        for i, segment in enumerate(self.snake):
            x1 = segment[0] * self.cell_size
            y1 = segment[1] * self.cell_size
            x2 = x1 + self.cell_size
            y2 = y1 + self.cell_size
            
            if i == len(self.snake) - 1:
                self.canvas.create_oval(x1+2, y1+2, x2-2, y2-2, 
                                     fill='#00ff00', outline='#00ff88', width=2)
            else:
                intensity = max(50, int(255 - (i * 255 / len(self.snake))))
                color = f'#{intensity:02x}ff{intensity:02x}'
                self.canvas.create_rectangle(x1+1, y1+1, x2-1, y2-1, 
                                           fill=color, outline='#00aa00')
                
        # 绘制食物
        if self.food:
            x1 = self.food[0] * self.cell_size
            y1 = self.food[1] * self.cell_size
            x2 = x1 + self.cell_size
            y2 = y1 + self.cell_size
            self.canvas.create_oval(x1+3, y1+3, x2-3, y2-3, 
                                  fill='#ffd700', outline='#ffffff', width=2)
                                  
    def ai_decision(self):
        if not self.food or not self.snake:
            return
            
        head = self.snake[-1]
        food_pos = self.food
        
        state = (head[0] - food_pos[0], head[1] - food_pos[1], self.direction)
        
        if random.random() < self.ai_epsilon:
            directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
            valid_directions = []
            
            for direction in directions:
                new_head = (head[0] + direction[0], head[1] + direction[1])
                if 0 <= new_head[0] < self.grid_size and 0 <= new_head[1] < self.grid_size:
                    if new_head not in self.snake:
                        valid_directions.append(direction)
                else:
                    valid_directions.append(direction)
                    
            if valid_directions:
                self.direction = random.choice(valid_directions)
        else:
            if state not in self.ai_q_table:
                self.ai_q_table[state] = [0, 0, 0, 0]
                
            q_values = self.ai_q_table[state]
            best_action = q_values.index(max(q_values))
            
            directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
            chosen_direction = directions[best_action]
            
            new_head = (head[0] + chosen_direction[0], head[1] + chosen_direction[1])
            
            if 0 <= new_head[0] < self.grid_size and 0 <= new_head[1] < self.grid_size:
                if new_head in self.snake:
                    return
                else:
                    self.direction = chosen_direction
            else:
                self.direction = chosen_direction
                
    def update_ai_q_table(self, reward, state, action):
        if state not in self.ai_q_table:
            self.ai_q_table[state] = [0, 0, 0, 0]
            
        old_q = self.ai_q_table[state][action]
        next_max_q = max(self.ai_q_table.get(state, [0, 0, 0, 0]))
        new_q = old_q + self.ai_learning_rate * (reward + 0.9 * next_max_q - old_q)
        
        self.ai_q_table[state][action] = new_q
        
    def move_snake(self):
        if not self.game_running or self.game_paused:
            return
            
        # AI决策
        if self.ai_mode:
            self.ai_decision()
            
        # 计算新位置（使用模运算处理穿墙，和ultimate_stable一样）
        head = self.snake[-1]
        new_head = (
            (head[0] + self.direction[0]) % self.grid_size,
            (head[1] + self.direction[1]) % self.grid_size
        )
        
        if new_head in self.snake:
            self.handle_collision()
            return
            
        self.snake.append(new_head)
        
        # 检查食物
        if new_head == self.food:
            self.handle_food_consumption()
        else:
            self.snake.popleft()
            
        # 更新食物生命周期
        if self.food:
            self.food_lifetime -= 1
            if self.food_lifetime <= 0:
                self.generate_food()
                self.add_message("⏰ 食物超时，重新生成")
                
        # 绘制游戏
        self.draw_game()
        
        # 更新FPS（在主线程中）
        self.fps_counter += 1
        current_time = time.time()
        if current_time - self.fps_last_time >= 1.0:
            self.current_fps = self.fps_counter
            self.fps_counter = 0
            self.fps_last_time = current_time
            self.fps_label.config(text=f"FPS: {self.current_fps}")
        
        # 继续移动
        self.root.after(self.game_speed, self.move_snake)
        

        
    def handle_collision(self):
        # 传送效果（和ultimate_stable一样）
        self.capital -= 1500
        self.teleport_count += 1
        self.score -= 5
        
        if self.ai_mode:
            self.ai_collision_count += 1
            
        # 清空蛇并重新定位
        self.snake.clear()
        self.snake.append((10, 10))
        
        self.add_message(f"传送! 损失 $1500 | 传送次数: {self.teleport_count}")
        
    def handle_food_consumption(self):
        # 和ultimate_stable一样
        food_types = [
            {"name": "盈利交易", "profit": 1500},
            {"name": "亏损交易", "loss": 1200},
            {"name": "突破交易", "profit": 2000},
            {"name": "反转交易", "profit": 1800}
        ]
        
        food_type = random.choice(food_types)
        
        if "profit" in food_type:
            profit = food_type["profit"]
            self.capital += profit
            self.score += 10
            self.add_message(f"💰 {food_type['name']}: +${profit}")
            if self.ai_mode:
                self.ai_food_collected += 1
        else:
            loss = food_type["loss"]
            self.capital -= loss
            self.score -= 5
            self.add_message(f"📉 {food_type['name']}: -${loss}")
            
        self.generate_food()
        
        if self.capital <= 0:
            self.game_over()
        
    def add_message(self, message):
        current_time = time.strftime("%H:%M:%S")
        formatted_message = f"[{current_time}] {message}\n"
        
        self.message_history.append(formatted_message)
        
        self.info_text.config(state=tk.NORMAL)
        self.info_text.insert(tk.END, formatted_message)
        self.info_text.config(state=tk.DISABLED)
        self.info_text.see(tk.END)
        
        if len(self.message_history) > 50:
            self.info_text.config(state=tk.NORMAL)
            self.info_text.delete(1.0, 2.0)
            self.info_text.config(state=tk.DISABLED)
            
    def update_display(self):
        self.score_label.config(text=f"分数: {self.score}")
        self.capital_label.config(text=f"资金: ${self.capital:,}")
        
        if self.game_running:
            self.game_time += 1
            status_text = f"游戏时间: {self.game_time//60:02d}:{self.game_time%60:02d} | "
            status_text += f"蛇身长度: {len(self.snake)} | "
            status_text += f"Q表: {len(self.ai_q_table)}"
            
            self.status_label.config(text=status_text)
            
        self.capital_history.append(self.capital)
        self.score_history.append(self.score)
            
    def start_game(self):
        self.game_running = True
        self.game_paused = False
        self.start_button.config(state='disabled')
        self.pause_button.config(state='normal')
        
        if not self.food:
            self.generate_food()
            
        self.add_message("🎮 游戏开始！")
        self.add_message("🤖 AI模式已启用")
        
        self.move_snake()
        
    def toggle_pause(self):
        self.game_paused = not self.game_paused
        
        if self.game_paused:
            self.pause_button.config(text="▶️ 继续")
            self.add_message("⏸️ 游戏暂停")
        else:
            self.pause_button.config(text="⏸️ 暂停")
            self.add_message("▶️ 游戏继续")
            self.move_snake()
            
    def reset_game(self):
        self.game_running = False
        self.game_paused = False
        
        self.snake.clear()
        self.snake.append((10, 10))
        self.direction = (1, 0)
        self.food = None
        self.score = 0
        self.capital = 10000
        self.teleport_count = 0
        self.game_time = 0
        
        self.ai_collision_count = 0
        self.ai_food_collected = 0
        
        self.trades.clear()
        self.capital_history.clear()
        self.score_history.clear()
        
        self.start_button.config(state='normal')
        self.pause_button.config(state='disabled', text="⏸️ 暂停")
        
        self.canvas.delete("all")
        
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete(1.0, tk.END)
        self.info_text.config(state=tk.DISABLED)
        
        self.draw_game()
        self.update_display()
        
        self.add_message("🔄 游戏已重置")
        
    def game_over(self):
        """游戏结束处理（和ultimate_stable一样）"""
        self.game_running = False
        self.start_button.config(state='normal')
        self.pause_button.config(state='disabled', text="⏸️ 暂停")
        
        messagebox.showinfo("游戏结束", f"💀 资金耗尽！游戏结束\n\n" + 
                          f"🎯 最终分数: {self.score}\n" + 
                          f"💰 最终资金: ${self.capital:,}\n" + 
                          f"🌀 传送次数: {self.teleport_count}")
        
    def quit_game(self):
        if self.game_running:
            if messagebox.askokcancel("退出", "确定要退出游戏吗？"):
                self.root.quit()
        else:
            self.root.quit()
            
def main():
    root = tk.Tk()
    game = TradingSnakeFixed(root)
    root.mainloop()

if __name__ == "__main__":
    main()