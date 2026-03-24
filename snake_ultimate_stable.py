#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
量化交易贪吃蛇游戏 - 超稳定版本
Ultra Stable Version
"""

import tkinter as tk
from tkinter import messagebox
import random
import time
from collections import deque

class TradingSnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🐍 量化交易贪吃蛇 - 超稳定版")
        self.root.configure(bg='#1a1a2e')
        
        # 游戏参数
        self.canvas_width = 600
        self.canvas_height = 600
        self.grid_size = 20
        self.cell_size = self.canvas_width // self.grid_size
        
        # 游戏状态
        self.snake = deque([(10, 10)])
        self.direction = (1, 0)
        self.food = None
        self.game_running = False
        self.game_paused = False
        self.game_speed = 150
        self.base_speed = 150
        self.score = 0
        self.capital = 10000
        self.trades = []
        self.teleport_count = 0
        self.food_lifetime = 0
        self.game_time = 0
        
        # AI参数
        self.ai_mode = True
        self.random_mode = True
        self.auto_rhythm_enabled = True
        self.ai_food_collected = 0
        self.ai_collision_count = 0
        
        # 数据记录
        self.capital_history = []
        self.score_history = []
        
        # 消息系统
        self.message_log = []
        self.max_messages = 20
        
        self.setup_gui()
        self.bind_keys()
        self.center_window()
        self.generate_food()
        self.auto_start()
        
    def center_window(self):
        try:
            self.root.geometry("1200x700+50+50")
            self.root.minsize(1000, 600)
        except Exception as e:
            print(f"窗口居中错误: {e}")
            
    def setup_gui(self):
        # 主容器
        main_frame = tk.Frame(self.root, bg='#1a1a2e')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 左侧游戏区域
        game_frame = tk.Frame(main_frame, bg='#1a1a2e', relief=tk.RAISED, bd=2)
        game_frame.pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Label(game_frame, text="🎮 游戏区域", font=('Arial', 14, 'bold'), bg='#1a1a2e', fg='#ffffff').pack(pady=10)
        
        # 游戏画布
        self.canvas = tk.Canvas(
            game_frame, 
            width=self.canvas_width, 
            height=self.canvas_height,
            bg='#0f0f1e',
            highlightthickness=2,
            highlightbackground='#4a4a6e'
        )
        self.canvas.pack(padx=10, pady=10)
        
        # 控制按钮
        control_frame = tk.Frame(game_frame, bg='#2d2d44')
        control_frame.pack(fill=tk.X, pady=10)
        
        btn_frame = tk.Frame(control_frame, bg='#2d2d44')
        btn_frame.pack()
        
        self.start_button = tk.Button(btn_frame, text="🎮 开始", command=self.start_game, bg='#4caf50', fg='white', font=('Arial', 10, 'bold'), width=10)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.pause_button = tk.Button(btn_frame, text="⏸️ 暂停", command=self.toggle_pause, bg='#ff9800', fg='white', font=('Arial', 10, 'bold'), width=10, state='disabled')
        self.pause_button.pack(side=tk.LEFT, padx=5)
        
        self.reset_button = tk.Frame(control_frame, bg='#2d2d44')
        
        # 状态显示
        status_frame = tk.Frame(control_frame, bg='#2d2d44')
        status_frame.pack(fill=tk.X, pady=10)
        
        self.status_label = tk.Label(status_frame, text="准备就绪", font=('Arial', 10), bg='#2d2d44', fg='#00ff00')
        self.status_label.pack()
        
        # 分数显示
        score_frame = tk.Frame(game_frame, bg='#2d2d44')
        score_frame.pack(fill=tk.X, pady=5)
        
        self.score_label = tk.Label(score_frame, text=f"分数: {self.score}", font=('Arial', 12, 'bold'), bg='#2d2d44', fg='#ffd700')
        self.score_label.pack(side=tk.LEFT, padx=10)
        
        self.capital_label = tk.Label(score_frame, text=f"资金: ${self.capital:,}", font=('Arial', 12, 'bold'), bg='#2d2d44', fg='#4caf50')
        self.capital_label.pack(side=tk.LEFT, padx=10)
        
        # 右侧信息区域
        info_frame = tk.Frame(main_frame, bg='#1a1a2e', relief=tk.RAISED, bd=2)
        info_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        tk.Label(info_frame, text="📊 实时数据", font=('Arial', 14, 'bold'), bg='#1a1a2e', fg='#ffffff').pack(pady=10)
        
        # 实时信息文本
        self.info_text = tk.Text(info_frame, height=20, width=40, bg='#0f0f1e', fg='#00ff00', font=('Consolas', 9), relief=tk.FLAT)
        self.info_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # 滚动条
        scrollbar = tk.Scrollbar(self.info_text)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.info_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.info_text.yview)
        
    def bind_keys(self):
        self.root.bind('<space>', lambda e: self.toggle_pause())
        self.root.bind('<Escape>', lambda e: self.quit_game())
        self.root.bind('<Up>', lambda e: self.change_direction(0, -1))
        self.root.bind('<Down>', lambda e: self.change_direction(0, 1))
        self.root.bind('<Left>', lambda e: self.change_direction(-1, 0))
        self.root.bind('<Right>', lambda e: self.change_direction(1, 0))
        
    def change_direction(self, x, y):
        # 禁用手动控制，实现完全自动化
        return
        
    def create_grid_background(self):
        self.canvas.delete("grid")
        for i in range(0, self.canvas_width, self.cell_size):
            self.canvas.create_line(i, 0, i, self.canvas_height, fill='#1a1a2e', width=1, tags='grid')
        for i in range(0, self.canvas_height, self.cell_size):
            self.canvas.create_line(0, i, self.canvas_width, i, fill='#1a1a2e', width=1, tags='grid')
            
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
        self.create_grid_background()
        
        # 绘制蛇身
        for i, segment in enumerate(self.snake):
            x1 = segment[0] * self.cell_size
            y1 = segment[1] * self.cell_size
            x2 = x1 + self.cell_size
            y2 = y1 + self.cell_size
            
            if i == len(self.snake) - 1:
                self.canvas.create_oval(x1+2, y1+2, x2-2, y2-2, fill='#00ff00', outline='#00ff88', width=2)
            else:
                intensity = int(255 - (i * 255 / len(self.snake)))
                color = f'#{intensity:02x}ff{intensity:02x}'
                self.canvas.create_rectangle(x1+1, y1+1, x2-1, y2-1, fill=color, outline='#00aa00')
                
        # 绘制食物
        if self.food:
            x1 = self.food[0] * self.cell_size
            y1 = self.food[1] * self.cell_size
            x2 = x1 + self.cell_size
            y2 = y1 + self.cell_size
            
            colors = ['#4caf50', '#f44336', '#2196f3', '#ff9800']
            food_color = random.choice(colors)
            
            self.canvas.create_oval(x1+3, y1+3, x2-3, y2-3, fill=food_color, outline='#ffffff', width=2)
            
    def move_snake(self):
        if not self.game_running or self.game_paused:
            return
            
        head = self.snake[-1]
        new_head = (
            (head[0] + self.direction[0]) % self.grid_size,
            (head[1] + self.direction[1]) % self.grid_size
        )
        
        if new_head in self.snake:
            self.handle_collision()
            return
            
        self.snake.append(new_head)
        
        if new_head == self.food:
            self.eat_food()
        else:
            self.snake.popleft()
            
        self.food_lifetime -= 1
        if self.food_lifetime <= 0:
            self.generate_food()
            
    def handle_collision(self):
        # 传送效果
        self.capital -= 1500
        self.teleport_count += 1
        self.score -= 5
        
        if self.ai_mode:
            self.ai_collision_count += 1
            
        # 清空蛇并重新定位
        self.snake.clear()
        self.snake.append((10, 10))
        
        self.add_message(f"传送! 损失 $1500 | 传送次数: {self.teleport_count}")
        
    def eat_food(self):
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
            self.trades.append(profit)
            self.add_message(f"💰 {food_type['name']}: +${profit}")
            if self.ai_mode:
                self.ai_food_collected += 1
        else:
            loss = food_type["loss"]
            self.capital -= loss
            self.score -= 5
            self.trades.append(-loss)
            self.add_message(f"📉 {food_type['name']}: -${loss}")
            
        self.generate_food()
        
        if self.capital <= 0:
            self.game_over()
            
    def ai_make_move(self):
        # 简化的AI决策
        try:
            if not self.snake or not self.food:
                return
                
            head = self.snake[-1]
            food_dx = self.food[0] - head[0]
            food_dy = self.food[1] - head[1]
            
            possible_moves = [(0, -1), (0, 1), (-1, 0), (1, 0)]
            valid_moves = [m for m in possible_moves if (m[0] * -1, m[1] * -1) != self.direction]
            
            if valid_moves:
                # 简单的朝向食物的AI
                if abs(food_dx) > abs(food_dy):
                    best_move = (1, 0) if food_dx > 0 else (-1, 0)
                else:
                    best_move = (0, 1) if food_dy > 0 else (0, -1)
                    
                if best_move in valid_moves and random.random() < 0.8:  # 80%概率使用AI决策
                    self.direction = best_move
                    
        except Exception as e:
            # 记录错误但不中断游戏
            print(f"AI决策错误: {e}")
            
    def apply_rhythm_mode(self):
        # 节奏模式效果
        if self.game_time % 50 == 0:
            self.game_speed = random.randint(80, 200)
            
    def game_loop(self):
        if not self.game_running or self.game_paused:
            return
            
        self.game_time += 1
            
        # AI决策
        if self.ai_mode:
            self.ai_make_move()
                
        # 随机影响
        if self.random_mode and random.random() < 0.3:
            directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
            valid_directions = [d for d in directions if (d[0] * -1, d[1] * -1) != self.direction]
            if valid_directions:
                self.direction = random.choice(valid_directions)
                
        # 节奏模式
        self.apply_rhythm_mode()
                
        self.move_snake()
        self.draw_game()
        
        # 更新数据显示（降低频率）
        if self.game_time % 20 == 0:
            self.update_display()
            
        # 记录性能数据（降低频率）
        if self.game_time % 50 == 0:
            self.record_performance_data()
            
        # 添加消息（降低频率）
        if self.game_time % 200 == 0:
            self.add_status_message()
            
        # 继续游戏循环
        try:
            self.root.after(self.game_speed, self.game_loop)
        except Exception as e:
            print(f"游戏循环错误: {e}")
            
    def update_display(self):
        # 更新显示
        self.score_label.config(text=f"分数: {self.score}")
        capital_color = '#4caf50' if self.capital > 10000 else '#f44336' if self.capital < 5000 else '#ffd700'
        self.capital_label.config(text=f"资金: ${self.capital:,}", fg=capital_color)
        
        status_text = f"游戏时间: {self.game_time//60:02d}:{self.game_time%60:02d} | 蛇身长度: {len(self.snake)} | Q表: {len(self.capital_history)}"
        self.status_label.config(text=status_text)
        
    def record_performance_data(self):
        # 记录性能数据
        if isinstance(self.capital_history, list):
            self.capital_history.append(self.capital)
            self.score_history.append(self.score)
            
            # 限制历史长度
            if len(self.capital_history) > 50:
                self.capital_history = self.capital_history[-50:]
            if len(self.score_history) > 50:
                self.score_history = self.score_history[-50:]
                
    def add_status_message(self):
        # 添加状态消息
        messages = [
            f"🧠 AI状态: Q表{len(self.capital_history)} | 学习进行中",
            f"🎯 游戏进度: 时间{self.game_time//60:02d}:{self.game_time%60:02d}",
            f"💰 资金状态: ${self.capital:,} | 蛇变率{((self.capital-10000)/10000)*100:+.1f}%",
            f"🤖 性能指标: 食物收集{self.ai_food_collected}/{len(self.trades) if self.trades else 0} | 碰撞率{max(0,100-self.ai_collision_count*2):.0f}%",
            f"📊 模式状态: AI{'✅' if self.ai_mode else '❌'} | 随机{'✅' if self.random_mode else '❌'} | 节奏{'✅' if self.auto_rhythm_enabled else '❌'}"
        ]
        
        message = random.choice(messages)
        self.add_message(message)
        
    def add_message(self, message):
        # 添加消息到日志
        timestamp = time.strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}"
        
        self.message_log.append(formatted_message)
        
        if len(self.message_log) > self.max_messages:
            self.message_log.pop(0)
            
        if hasattr(self, 'info_text'):
            self.info_text.delete(1.0, tk.END)
            for msg in self.message_log:
                self.info_text.insert(tk.END, msg + '\n')
            self.info_text.see(tk.END)
            
    def auto_start(self):
        # 自动启动游戏
        try:
            self.game_running = True
            self.game_paused = False
            self.start_button.config(state='disabled')
            self.pause_button.config(state='normal')
            
            self.add_message("🚀 自动模式启动！AI+随机+节奏+学习 全部运行")
            self.game_loop()
        except:
            self.add_message("❌ 启动失败")
            
    def start_game(self):
        if not self.game_running:
            self.game_running = True
            self.game_paused = False
            self.start_button.config(state='disabled')
            self.pause_button.config(state='normal')
            self.add_message("🎮 游戏开始")
            self.game_loop()
            
    def toggle_pause(self):
        if self.game_running:
            self.game_paused = not self.game_paused
            if self.game_paused:
                self.pause_button.config(text="▶️ 继续")
                self.add_message("⏸️ 游戏暂停")
            else:
                self.pause_button.config(text="⏸️ 暂停")
                self.add_message("▶️ 游戏继续")
                self.game_loop()
                
    def reset_game(self):
        self.game_running = False
        self.game_paused = False
        self.snake = deque([(10, 10)])
        self.direction = (1, 0)
        self.game_speed = self.base_speed
        self.score = 0
        self.capital = 10000
        self.trades = []
        self.teleport_count = 0
        self.game_time = 0
        
        self.ai_mode = True
        self.random_mode = True
        self.auto_rhythm_enabled = True
        self.ai_food_collected = 0
        self.ai_collision_count = 0
        
        self.capital_history = []
        self.score_history = []
        
        self.start_button.config(state='normal')
        self.pause_button.config(state='disabled', text="⏸️ 暂停")
        
        self.generate_food()
        self.draw_game()
        self.update_display()
        
        self.add_message("🔄 游戏重置 - 自动模式启动")
        self.auto_start()
        
    def game_over(self):
        self.game_running = False
        
        if self.trades:
            total_profit = sum(self.trades)
            win_rate = len([t for t in self.trades if t > 0]) / len(self.trades) * 100
            message = f"""
游戏结束！📊

📈 最终统计:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🏆 最终分数: {self.score}
💰 最终资金: ${self.capital:,}
📊 交易统计: 总数{len(self.trades)}笔 | 胜率{win_rate:.1f}%
💹 总盈亏: ${total_profit:+,.0f}
🔄 传送次数: {self.teleport_count}
🤖 AI表现: 收集{self.ai_food_collected} | 碰撞{self.ai_collision_count}

━━━━━━━━━━━━━━━━━━━━━━━━━
3秒后自动重新开始...
"""
        else:
            message = "游戏结束！3秒后自动重新开始..."
            
        self.add_message(message)
        
        # 自动重新开始
        self.root.after(3000, self.reset_game)
        self.root.after(5000, self.start_game)
        
    def quit_game(self):
        if self.game_running:
            result = messagebox.askyesno("退出游戏", "游戏正在进行中，确定要退出吗?")
            if result:
                self.root.quit()
        else:
            self.root.quit()

if __name__ == "__main__":
    try:
        root = tk.Tk()
        game = TradingSnakeGame(root)
        root.mainloop()
    except Exception as e:
        print(f"游戏启动失败: {e}")
        input("按回车键退出...")