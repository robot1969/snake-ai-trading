#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
量化交易贪吃蛇游戏 - 稳定版本
Stable Version with Enhanced Messages and Charts
"""

import tkinter as tk
from tkinter import messagebox, font
import random
import time
from collections import deque
from threading import Thread
import json

class TradingSnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🐍 量化交易贪吃蛇 - 增强版")
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
        self.score = 0
        self.capital = 10000
        self.trades = []
        self.teleport_count = 0
        self.food_lifetime = 0
        self.animation_effects = []
        
        # AI和学习参数
        self.ai_mode = True
        self.random_mode = True
        self.auto_rhythm_enabled = True
        self.learning_from_human = True
        self.ai_q_table = {}
        self.ai_learning_rate = 0.1
        self.ai_discount_factor = 0.9
        self.ai_epsilon = 0.1
        self.ai_last_state = None
        self.ai_last_action = None
        self.ai_collision_count = 0
        self.ai_food_collected = 0
        
        # 数据分析参数
        self.performance_history = []
        self.capital_history = []
        self.score_history = []
        self.game_time = 0
        self.message_log = []
        self.max_messages = 50
        
        self.setup_gui()
        self.bind_keys()
        self.center_window()
        self.generate_food()
        self.update_stats()
        
        # 自动启动所有模式
        self.auto_start_all_modes()
        
    def center_window(self):
        self.root.update_idletasks()
        try:
            self.root.geometry("1200x700+50+50")
            self.root.minsize(1100, 650)
            self.root.state('zoomed')
        except:
            pass
            
    def setup_gui(self):
        # 主容器
        main_container = tk.Frame(self.root, bg='#1a1a2e')
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # 左侧游戏区域
        game_frame = tk.Frame(main_container, bg='#1a1a2e')
        game_frame.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
        
        # 游戏画布
        self.canvas = tk.Canvas(
            game_frame, 
            width=self.canvas_width, 
            height=self.canvas_height,
            bg='#0f0f1e',
            highlightthickness=3,
            highlightbackground='#4a4a6e'
        )
        self.canvas.pack()
        
        # 右侧面板容器
        right_container = tk.Frame(main_container, bg='#1a1a2e')
        right_container.grid(row=0, column=1, sticky='nsew', padx=10, pady=10)
        
        # 右侧网格布局
        right_grid = tk.Frame(right_container, bg='#1a1a2e')
        right_grid.pack(fill=tk.BOTH, expand=True)
        
        # 游戏信息面板
        info_panel = tk.Frame(right_grid, bg='#2d2d44', relief=tk.RAISED, bd=2)
        info_panel.grid(row=0, column=0, sticky='ew', pady=(0, 10))
        
        tk.Label(info_panel, text="🎮 游戏状态", font=('Arial', 11, 'bold'), bg='#2d2d44', fg='#ffffff').pack(pady=5)
        
        self.game_info_text = tk.Text(info_panel, height=3, width=50, bg='#1a1a2e', fg='#ffffff', font=('Consolas', 8), relief=tk.FLAT)
        self.game_info_text.pack(padx=10, pady=5)
        
        # 控制按钮
        button_frame = tk.Frame(info_panel, bg='#2d2d44')
        button_frame.pack(pady=5)
        
        self.start_button = tk.Button(button_frame, text="🎮", command=self.start_game, font=('Arial', 12, 'bold'), bg='#4caf50', fg='white', width=3, cursor='hand2')
        self.start_button.pack(side=tk.LEFT, padx=2)
        
        self.pause_button = tk.Button(button_frame, text="⏸️", command=self.toggle_pause, font=('Arial', 12, 'bold'), bg='#ff9800', fg='white', width=3, cursor='hand2', state='disabled')
        self.pause_button.pack(side=tk.LEFT, padx=2)
        
        self.reset_button = tk.Button(button_frame, text="🔄", command=self.reset_game, font=('Arial', 12, 'bold'), bg='#f44336', fg='white', width=3, cursor='hand2')
        self.reset_button.pack(side=tk.LEFT, padx=2)
        
        # 分数和资金
        self.score_label = tk.Label(button_frame, text=f"分数: {self.score}", font=('Arial', 10, 'bold'), bg='#2d2d44', fg='#ffd700')
        self.score_label.pack(side=tk.LEFT, padx=5)
        
        self.capital_label = tk.Label(button_frame, text=f"资金: ${self.capital:,}", font=('Arial', 10, 'bold'), bg='#2d2d44', fg='#4caf50')
        self.capital_label.pack(side=tk.LEFT, padx=5)
        
        # 统计面板
        stats_panel = tk.Frame(right_grid, bg='#3d3d5c', relief=tk.SUNKEN, bd=2)
        stats_panel.grid(row=1, column=0, sticky='ew', pady=(0, 10))
        
        tk.Label(stats_panel, text="📊 交易统计", font=('Arial', 11, 'bold'), bg='#3d3d5c', fg='#ffffff').pack(pady=5)
        
        self.stats_text = tk.Text(stats_panel, height=5, width=25, bg='#2d2d44', fg='#ffffff', font=('Consolas', 8), relief=tk.FLAT)
        self.stats_text.pack(padx=10, pady=5)
        
        # 图表面板
        chart_panel = tk.Frame(right_grid, bg='#3d3d5c', relief=tk.SUNKEN, bd=2)
        chart_panel.grid(row=2, column=0, sticky='ew', pady=(0, 10))
        
        tk.Label(chart_panel, text="📈 详细数据分析图表", font=('Arial', 11, 'bold'), bg='#3d3d5c', fg='#ffffff').pack(pady=5)
        
        # 主图表 - 资金和分数
        self.chart_canvas = tk.Canvas(chart_panel, width=550, height=200, bg='#2d2d44', highlightthickness=1, highlightbackground='#4a4a6e')
        self.chart_canvas.pack(padx=10, pady=5)
        
        # 第二个图表 - AI性能
        self.ai_chart_canvas = tk.Canvas(chart_panel, width=550, height=150, bg='#2d2d44', highlightthickness=1, highlightbackground='#4a4a6e')
        self.ai_chart_canvas.pack(padx=10, pady=5)
        
        # 第三个图表 - 交易分析
        self.trade_chart_canvas = tk.Canvas(chart_panel, width=550, height=150, bg='#2d2d44', highlightthickness=1, highlightbackground='#4a4a6e')
        self.trade_chart_canvas.pack(padx=10, pady=5)
        
        # 消息面板 - 增加高度
        message_panel = tk.Frame(right_grid, bg='#3d3d5c', relief=tk.SUNKEN, bd=2)
        message_panel.grid(row=3, column=0, sticky='ew', pady=(0, 10))
        
        tk.Label(message_panel, text="💬 实时消息 & 数据分析", font=('Arial', 11, 'bold'), bg='#3d3d5c', fg='#ffffff').pack(pady=5)
        
        self.message_text = tk.Text(message_panel, height=8, width=60, bg='#1a1a2e', fg='#00ff00', font=('Consolas', 8), relief=tk.FLAT)
        self.message_text.pack(padx=10, pady=5)
        
        # 消息滚动条
        scrollbar = tk.Scrollbar(self.message_text, command=self.message_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.message_text.config(yscrollcommand=scrollbar.set)
        
        # 配置网格权重 - 给图表更多空间
        main_container.grid_columnconfigure(0, weight=2)
        main_container.grid_columnconfigure(1, weight=3)
        main_container.grid_rowconfigure(0, weight=1)
        right_grid.grid_rowconfigure(0, weight=1)
        right_grid.grid_rowconfigure(1, weight=1)
        right_grid.grid_rowconfigure(2, weight=2)  # 图表面板更高权重
        right_grid.grid_rowconfigure(3, weight=1)
        right_grid.grid_columnconfigure(0, weight=1)
        
    def bind_keys(self):
        self.root.bind('<space>', lambda e: self.toggle_pause())
        self.root.bind('<Escape>', lambda e: self.quit_game())
        
    def create_grid_background(self):
        for i in range(0, self.canvas_width, self.cell_size):
            self.canvas.create_line(i, 0, i, self.canvas_height, fill='#1a1a2e', width=1)
        for i in range(0, self.canvas_height, self.cell_size):
            self.canvas.create_line(0, i, self.canvas_width, i, fill='#1a1a2e', width=1)
            
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
        
        # 绘制蛇
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
                self.canvas.create_rectangle(x1+1, y1+1, x2-1, y2-1, fill=color, outline='#00aa00', width=1)
                
        # 绘制食物
        if self.food:
            x1 = self.food[0] * self.cell_size
            y1 = self.food[1] * self.cell_size
            x2 = x1 + self.cell_size
            y2 = y1 + self.cell_size
            
            colors = ['#4caf50', '#f44336', '#2196f3', '#ff9800']
            food_color = random.choice(colors)
            
            for i in range(3):
                offset = i * 2
                self.canvas.create_oval(x1-offset, y1-offset, x2+offset, y2+offset, fill='', outline=food_color, width=1)
                
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
            self.handle_collision(new_head, "self")
            return
            
        self.snake.append(new_head)
        
        if new_head == self.food:
            self.eat_food()
        else:
            self.snake.popleft()
            
        self.food_lifetime -= 1
        if self.food_lifetime <= 0:
            self.generate_food()
            
    def handle_collision(self, pos, collision_type):
        center_x = pos[0] * self.cell_size + self.cell_size // 2
        center_y = pos[1] * self.cell_size + self.cell_size // 2
        
        for i in range(5):
            radius = (5 - i) * 10
            self.canvas.create_oval(center_x - radius, center_y - radius, center_x + radius, center_y + radius, fill='', outline='#9c27b0', width=2)
            
        new_x = random.randint(2, self.grid_size - 3)
        new_y = random.randint(2, self.grid_size - 3)
        
        self.snake.clear()
        self.snake.append((new_x, new_y))
        
        teleport_penalty = 1500 + (self.teleport_count * 300)
        self.capital -= teleport_penalty
        self.teleport_count += 1
        self.score -= 5
        
        if self.ai_mode:
            self.ai_collision_count += 1
            
        self.add_message(f"传送! 损失 ${teleport_penalty}", '#ff9800')
            
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
            self.add_message(f"盈利交易! +${profit}", '#4caf50')
            if self.ai_mode:
                self.ai_food_collected += 1
        else:
            loss = food_type["loss"]
            self.capital -= loss
            self.score -= 5
            self.trades.append(-loss)
            self.add_message(f"亏损交易! -${loss}", '#f44336')
            
        self.generate_food()
        self.update_stats()
        self.update_display()
        
        if self.capital <= 0:
            self.game_over()
            
    def update_stats(self):
        if hasattr(self, 'stats_text'):
            self.stats_text.delete(1.0, tk.END)
            
            if self.trades:
                total_trades = len(self.trades)
                winning_trades = len([t for t in self.trades if t > 0])
                win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
                total_profit = sum(self.trades)
                
                ai_efficiency = 0
                if self.ai_mode and self.ai_collision_count > 0:
                    ai_efficiency = (self.ai_food_collected / self.ai_collision_count) * 100
                
                stats = f"""交易次数: {total_trades} | 胜率: {win_rate:.1f}%
总盈亏: ${total_profit:+,.0f}
传送次数: {self.teleport_count}
AI效率: {ai_efficiency:.1f}% | Q表: {len(self.ai_q_table)}"""
            else:
                stats = "暂无交易数据"
                
            self.stats_text.insert(tk.END, stats)
            
    def update_display(self):
        if hasattr(self, 'score_label'):
            self.score_label.config(text=f"分数: {self.score}")
        
        if hasattr(self, 'capital_label'):
            capital_color = '#4caf50' if self.capital > 10000 else '#f44336' if self.capital < 5000 else '#ffd700'
            self.capital_label.config(text=f"资金: ${self.capital:,}", fg=capital_color)
            
    def update_charts(self):
        if not hasattr(self, 'chart_canvas'):
            return
            
        self.chart_canvas.delete("all")
        
        if not self.capital_history:
            self.chart_canvas.create_text(275, 75, text="暂无数据\n开始游戏后将显示图表", font=('Arial', 12), fill='#81c784')
            return
            
        data_points = min(50, len(self.capital_history))
        capital_data = self.capital_history[-data_points:]
        
        if hasattr(self, 'score_history') and isinstance(self.score_history, list) and len(self.score_history) > 0:
            score_data = self.score_history[-data_points:]
        else:
            score_data = []
        
        if len(capital_data) < 2:
            return
            
        width = 550
        height = 150
        margin = 20
        chart_width = width - 2 * margin
        chart_height = height - 2 * margin
        
        min_capital = min(capital_data)
        max_capital = max(capital_data)
        capital_range = max_capital - min_capital if max_capital != min_capital else 1
        
        # 绘制坐标轴
        self.chart_canvas.create_line(margin, height - margin, width - margin, height - margin, fill='#666666', width=1)
        self.chart_canvas.create_line(margin, margin, margin, height - margin, fill='#666666', width=1)
        
        # 资金曲线
        capital_points = []
        for i, value in enumerate(capital_data):
            x = margin + (i * chart_width / (len(capital_data) - 1))
            y = height - margin - ((value - min_capital) / capital_range) * chart_height
            capital_points.extend([x, y])
            
        if len(capital_points) >= 4:
            self.chart_canvas.create_line(capital_points, fill='#4caf50', width=2, smooth=True)
            
        # 显示当前值
        self.chart_canvas.create_text(10, 10, text=f"当前: ${self.capital:,} | 分数: {self.score}", font=('Arial', 10), fill='#ffffff', anchor='w')
        
    def add_message(self, message, color='#00ff00'):
        timestamp = time.strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}"
        
        self.message_log.append({
            'text': formatted_message,
            'color': color,
            'time': time.time()
        })
        
        if len(self.message_log) > self.max_messages:
            self.message_log.pop(0)
        
        if hasattr(self, 'message_text'):
            self.message_text.delete(1.0, tk.END)
            for msg in self.message_log[-20:]:
                self.message_text.insert(tk.END, msg['text'] + '\n')
            
            self.message_text.see(tk.END)
            
    def auto_start_all_modes(self):
        try:
            self.game_running = True
            self.game_paused = False
            
            if hasattr(self, 'start_button'):
                self.start_button.config(state='disabled')
            if hasattr(self, 'pause_button'):
                self.pause_button.config(state='normal')
            
            self.add_message("🚀 全自动模式启动！AI+随机+节奏+学习 全部运行", '#00ff00')
            self.game_loop()
            
        except Exception as e:
            print(f"自动启动错误: {e}")
            self.add_message(f"启动失败: {e}", '#ff0000')
            
    def game_loop(self):
        if self.game_running and not self.game_paused:
            self.game_time += 1
            
            # AI决策
            if self.ai_mode:
                try:
                    self.ai_make_move()
                except Exception as e:
                    print(f"AI决策错误: {e}")
                    
            # 随机影响
            if self.random_mode and random.random() < 0.3:
                try:
                    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
                    valid_directions = [d for d in directions if (d[0] * -1, d[1] * -1) != self.direction]
                    if valid_directions:
                        self.direction = random.choice(valid_directions)
                except Exception as e:
                    print(f"随机方向错误: {e}")
                    
            # 节奏模式
            if self.auto_rhythm_enabled:
                try:
                    if self.game_time % 50 == 0:
                        self.game_speed = random.randint(80, 200)
                except Exception as e:
                    print(f"节奏变化错误: {e}")
                    
            self.move_snake()
            self.draw_game()
            
            # 更新图表（降低频率）
            if self.game_time % 20 == 0:
                try:
                    self.update_advanced_panels()
                except Exception as e:
                    print(f"图表更新错误: {e}")
                    
            # 记录性能数据（降低频率）
            if self.game_time % 10 == 0:
                try:
                    self.record_performance_data()
                except Exception as e:
                    print(f"数据记录错误: {e}")
                    
            # 添加消息（降低频率）
            if self.game_time % 100 == 0:
                try:
                    self.add_periodic_message()
                except Exception as e:
                    print(f"消息添加错误: {e}")
                
        if self.game_running:
            try:
                self.root.after(self.game_speed, self.game_loop)
            except Exception as e:
                print(f"游戏循环错误: {e}")
            
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
            print(f"AI决策错误: {e}")
                
    def update_advanced_panels(self):
        # 更新游戏信息面板
        if hasattr(self, 'game_info_text'):
            self.game_info_text.delete(1.0, tk.END)
            
            # 详细的游戏信息
            distance_to_food = abs(self.snake[-1][0] - self.food[0]) + abs(self.snake[-1][1] - self.food[1]) if self.snake and self.food else 0
            direction_names = {(0, -1): "北", (0, 1): "南", (-1, 0): "西", (1, 0): "东"}
            current_direction = direction_names.get(self.direction, "未知")
            
            # 计算资金趋势
            if len(self.capital_history) >= 2:
                capital_trend = "↗" if self.capital_history[-1] > self.capital_history[-2] else "↘" if self.capital_history[-1] < self.capital_history[-2] else "→"
            else:
                capital_trend = "→"
                
            game_info = f"""🎮 当前状态 | 时间: {self.game_time//60:02d}:{self.game_time%60:02d} | 模式: 全自动
🐍 蛇身信息 | 长度: {len(self.snake)} | 位置: ({self.snake[-1][0]},{self.snake[-1][1]}) | 方向: {current_direction}
🎯 目标信息 | 食物: ({self.food[0]},{self.food[1]}) | 距离: {distance_to_food} | 趋势: {capital_trend}
🧠 AI状态 | Q表: {len(self.ai_q_table)} | 学习率: {self.ai_learning_rate:.3f} | 探索率: {self.ai_epsilon:.3f}
💰 资金状态 | 当前: ${self.capital:,} | 变化: {self.capital-10000:+,} | 传送次数: {self.teleport_count}
📊 效率统计 | 食物收集: {self.ai_food_collected} | 碰撞避免: {max(0,100-self.ai_collision_count*5):.1f}% | FPS: {1000//max(self.game_speed,50)}"""
            self.game_info_text.insert(tk.END, game_info)
            
        # 更新详细统计
        if hasattr(self, 'stats_text'):
            self.stats_text.delete(1.0, tk.END)
            
            if hasattr(self, 'trades') and len(self.trades) > 0:
                winning_trades = len([t for t in self.trades if t > 0])
                win_rate = (winning_trades / len(self.trades)) * 100
                total_profit = sum(self.trades)
                avg_profit = total_profit / len(self.trades)
                max_profit = max(self.trades)
                min_loss = min(self.trades)
                
                # 计算最近表现
                recent_10 = self.trades[-10:] if len(self.trades) >= 10 else self.trades
                recent_profit = sum(recent_10)
                recent_win_rate = (len([t for t in recent_10 if t > 0]) / len(recent_10)) * 100
                
                stats = f"""📊 交易统计概览
────────────────────────
📈 总体表现: 交易{len(self.trades)}笔 | 胜率{win_rate:.1f}% | 盈亏${total_profit:+,.0f}
💰 平均表现: 每笔${avg_profit:+,.0f} | 最大${max_profit:+,} | 最小${min_loss:+,}
🎯 最近10笔: {len(recent_10)}笔 | 盈亏${recent_profit:+,} | 胜率{recent_win_rate:.1f}%
🧠 AI学习: Q表{len(self.ai_q_table)}项 | 收集{self.ai_food_collected} | 碰撞{self.ai_collision_count}
🎵 模式状态: AI{'✅' if self.ai_mode else '❌'} | 随机{'✅' if self.random_mode else '❌'} | 节奏{'✅' if self.auto_rhythm_enabled else '❌'}
────────────────────────"""
            else:
                stats = f"""📊 暂无交易数据
────────────────────────
🎮 游戏进行中... | 等待第一次交易
🧠 AI准备就绪 | Q表大小: {len(self.ai_q_table)}
🎵 模式运行中 | AI+随机+节奏+学习
────────────────────────"""
                
            self.stats_text.insert(tk.END, stats)
            
        # 更新所有图表 - 添加错误处理
        try:
            self.update_main_chart()
            self.update_ai_chart()
            self.update_trade_chart()
        except Exception as e:
            print(f"图表更新错误: {e}")
            self.add_message(f"图表错误: {e}", '#ff0000')
        
    def update_main_chart(self):
        """更新主图表 - 资金和分数曲线"""
        if not hasattr(self, 'chart_canvas'):
            return
            
        self.chart_canvas.delete("all")
        
        width = 550
        height = 200
        margin = 20
        chart_width = width - 2 * margin
        chart_height = height - 2 * margin
        
        if not self.capital_history:
            self.chart_canvas.create_text(width//2, height//2, text="暂无数据\n开始游戏后将显示图表", font=('Arial', 12), fill='#81c784')
            return
            
        data_points = min(100, len(self.capital_history))
        capital_data = self.capital_history[-data_points:]
        
        if len(capital_data) < 2:
            return
            
        min_capital = min(capital_data)
        max_capital = max(capital_data)
        capital_range = max_capital - min_capital if max_capital != min_capital else 1
        
        # 绘制资金曲线
        capital_points = []
        for i, value in enumerate(capital_data):
            x = margin + (i * chart_width / (len(capital_data) - 1))
            y = height - margin - ((value - min_capital) / capital_range) * chart_height
            capital_points.extend([x, y])
            
        if len(capital_points) >= 4:
            self.chart_canvas.create_line(capital_points, fill='#4caf50', width=3, smooth=True)
            
        # 绘制零线
        if min_capital <= 10000 <= max_capital:
            zero_y = height - margin - ((10000 - min_capital) / capital_range) * chart_height
            self.chart_canvas.create_line(margin, zero_y, width - margin, zero_y, fill='#ff5722', width=2, dash=(5, 5))
        
        # 标题和图例
        self.chart_canvas.create_text(width//2, 10, text="💰 资金变化曲线", font=('Arial', 12, 'bold'), fill='#ffffff')
        self.chart_canvas.create_text(width - 80, 20, text=f"当前: ${self.capital:,}", font=('Arial', 10, 'bold'), fill='#4caf50')
        self.chart_canvas.create_text(width - 80, height - 20, text=f"分数: {self.score}", font=('Arial', 10, 'bold'), fill='#ffd700')
        
        # 绘制数据点
        for i in range(0, len(capital_data), max(1, len(capital_data)//20)):
            x = margin + (i * chart_width / (len(capital_data) - 1))
            y = height - margin - ((capital_data[i] - min_capital) / capital_range) * chart_height
            self.chart_canvas.create_oval(x-3, y-3, x+3, y+3, fill='#4caf50', outline='#ffffff', width=1)
            
    def update_ai_chart(self):
        """更新AI性能图表"""
        if not hasattr(self, 'ai_chart_canvas'):
            return
            
        self.ai_chart_canvas.delete("all")
        
        width = 550
        height = 150
        margin = 20
        chart_width = width - 2 * margin
        chart_height = height - 2 * margin
        
        # AI性能数据
        q_size = len(self.ai_q_table)
        learning_rate = self.ai_learning_rate * 100
        efficiency = (self.ai_food_collected / max(1, self.ai_collision_count)) * 100 if self.ai_collision_count > 0 else 100
        
        # 绘制柱状图
        metrics = [
            ('Q表', q_size, 1000, '#4caf50'),
            ('学习率', learning_rate, 100, '#2196f3'),
            ('效率', efficiency, 100, '#ff9800')
        ]
        
        bar_width = chart_width // (len(metrics) * 2)
        
        for i, (name, value, max_val, color) in enumerate(metrics):
            x = margin + i * 2 * bar_width + bar_width // 2
            bar_height = int((value / max_val) * (chart_height - 40))
            y = height - margin - 20 - bar_height
            
            # 绘制柱子
            self.ai_chart_canvas.create_rectangle(x, y, x + bar_width, height - margin - 20, fill=color, outline='#ffffff', width=2)
            
            # 绘制数值
            text_value = f"{value:.0f}" if name != '学习率' else f"{value:.1f}%"
            self.ai_chart_canvas.create_text(x + bar_width//2, y - 5, text=text_value, font=('Arial', 9, 'bold'), fill='#ffffff')
            self.ai_chart_canvas.create_text(x + bar_width//2, height - margin - 5, text=name, font=('Arial', 8), fill='#ffffff')
            
        # 标题
        self.ai_chart_canvas.create_text(width//2, 10, text="🧠 AI性能分析", font=('Arial', 12, 'bold'), fill='#ffffff')
        
    def update_trade_chart(self):
        """更新交易分析图表"""
        if not hasattr(self, 'trade_chart_canvas'):
            return
            
        self.trade_chart_canvas.delete("all")
        
        width = 550
        height = 150
        margin = 20
        chart_width = width - 2 * margin
        chart_height = height - 2 * margin
        
        if not hasattr(self, 'trades') or len(self.trades) == 0:
            self.trade_chart_canvas.create_text(width//2, height//2, text="暂无交易数据", font=('Arial', 12), fill='#81c784')
            return
            
        # 交易分布统计
        positive_trades = [t for t in self.trades if t > 0]
        negative_trades = [t for t in self.trades if t < 0]
        win_rate = len(positive_trades) / len(self.trades) * 100
        total_profit = sum(self.trades)
        
        # 绘制简化的交易分析图
        bar_width = 40
        max_bar_height = chart_height - 40
        
        # 绘制柱状图
        positive_height = int((len(positive_trades) / max(1, len(self.trades))) * max_bar_height)
        negative_height = int((len(negative_trades) / max(1, len(self.trades))) * max_bar_height)
        
        # 盈利柱
        pos_x = margin + chart_width // 4 - bar_width
        pos_y = height - margin - 20 - positive_height
        self.trade_chart_canvas.create_rectangle(pos_x, pos_y, pos_x + bar_width, height - margin - 20, fill='#4caf50', outline='#ffffff', width=2)
        
        # 亏损柱
        neg_x = margin + 3 * chart_width // 4 - bar_width
        neg_y = height - margin - 20 - negative_height
        self.trade_chart_canvas.create_rectangle(neg_x, neg_y, neg_x + bar_width, height - margin - 20, fill='#f44336', outline='#ffffff', width=2)
        
        # 数值标签
        self.trade_chart_canvas.create_text(pos_x + bar_width//2, pos_y - 5, text=str(len(positive_trades)), font=('Arial', 10, 'bold'), fill='#ffffff')
        self.trade_chart_canvas.create_text(neg_x + bar_width//2, neg_y - 5, text=str(len(negative_trades)), font=('Arial', 10, 'bold'), fill='#ffffff')
        
        # 统计信息
        info_x = margin + chart_width // 2
        info_y = height - margin - 5
        info_text = f"胜率: {win_rate:.1f}% | 平均: {total_profit/len(self.trades):+.0f}"
        self.trade_chart_canvas.create_text(info_x, info_y, text=info_text, font=('Arial', 12, 'bold'), fill='#ffffff')
        self.trade_chart_canvas.create_text(info_x, info_y + 15, text=f"总盈亏: ${total_profit:+,}", font=('Arial', 10, 'bold'), fill='#4caf50' if total_profit > 0 else '#f44336')
        
        # 标题
        self.trade_chart_canvas.create_text(width//2, 10, text="📊 交易统计分析", font=('Arial', 12, 'bold'), fill='#ffffff')
        self.update_main_chart()
        self.update_ai_chart()
        self.update_trade_chart()
        
    def record_performance_data(self):
        # 确保是列表
        if not hasattr(self, 'capital_history') or not isinstance(self.capital_history, list):
            self.capital_history = []
        if not hasattr(self, 'score_history') or not isinstance(self.score_history, list):
            self.score_history = []
            
        self.capital_history.append(self.capital)
        self.score_history.append(self.score)
        
        max_history = 100
        if len(self.capital_history) > max_history:
            self.capital_history = self.capital_history[-max_history:]
        if len(self.score_history) > max_history:
            self.score_history = self.score_history[-max_history]
            
    def add_periodic_message(self):
        # 计算更详细的统计信息
        if hasattr(self, 'trades') and len(self.trades) > 0:
            win_rate = len([t for t in self.trades if t > 0]) / len(self.trades) * 100
            total_profit = sum(self.trades)
            max_trade = max(self.trades)
            min_trade = min(self.trades)
            avg_trade = total_profit / len(self.trades)
        else:
            win_rate = 0
            total_profit = 0
            max_trade = 0
            min_trade = 0
            avg_trade = 0
            
        # 计算性能指标
        fps = 1000 // max(self.game_speed, 50)
        efficiency = len(self.snake) / max(1, self.game_time // 100)
        food_rate = (self.ai_food_collected / max(1, len(self.trades))) * 100 if len(self.trades) > 0 else 0
        collision_rate = (self.ai_collision_count / max(1, self.game_time // 50)) * 100
        
        messages = [
            f"🧠 AI学习状态 | Q表大小: {len(self.ai_q_table)} | 学习率: {self.ai_learning_rate:.3f}",
            f"📊 交易统计 | 总数: {len(self.trades)} | 胜率: {win_rate:.1f}% | 总盈亏: ${total_profit:+,}",
            f"💰 资金分析 | 当前: ${self.capital:,} | 变化率: {((self.capital-10000)/10000)*100:+.1f}% | 最大: ${max_trade:+,} | 最小: ${min_trade:+,}",
            f"🎯 效率指标 | 食物率: {food_rate:.1f}% | 碰撞率: {collision_rate:.1f}% | 移动效率: {efficiency:.2f}",
            f"⚡ 性能数据 | FPS: {fps} | 速度: {self.game_speed}ms | 游戏时间: {self.game_time//60:02d}:{self.game_time%60:02d}",
            f"🐍 游戏状态 | 蛇长: {len(self.snake)} | 位置: ({self.snake[-1][0]},{self.snake[-1][1]}) | 食物: ({self.food[0]},{self.food[1]})",
            f"🎵 模式状态 | AI: {'✅' if self.ai_mode else '❌'} | 随机: {'✅' if self.random_mode else '❌'} | 节奏: {'✅' if self.auto_rhythm_enabled else '❌'} | 学习: {'✅' if self.learning_from_human else '❌'}",
            f"🔄 事件统计 | 传送: {self.teleport_count} | AI碰撞: {self.ai_collision_count} | 食物收集: {self.ai_food_collected}",
            f"📈 资金历史 | 最近10笔: {self.trades[-10:] if len(self.trades) >= 10 else self.trades}",
            f"🎯 路径分析 | 距离食物: {abs(self.snake[-1][0]-self.food[0]) + abs(self.snake[-1][1]-self.food[1])} | 方向向量: ({self.direction[0]},{self.direction[1]})"
        ]
        
        # 轮换显示不同类型的消息
        if not hasattr(self, 'last_message_type'):
            self.last_message_type = 0
            
        message = messages[self.last_message_type]
        
        # 根据消息内容智能选择颜色
        if 'AI学习' in message or '收集' in message:
            color = '#00ff00'
        elif '交易统计' in message or '资金' in message:
            color = '#4caf50'
        elif '效率' in message:
            color = '#ff9800'
        elif '性能数据' in message:
            color = '#2196f3'
        elif '游戏状态' in message or '模式状态' in message:
            color = '#9c27b0'
        elif '事件统计' in message:
            color = '#673ab7'
        else:
            color = '#00bcd4'
            
        self.last_message_type = (self.last_message_type + 1) % len(messages)
        self.add_message(message, color)
            
    def start_game(self):
        if not self.game_running:
            self.game_running = True
            self.game_paused = False
            self.start_button.config(state='disabled')
            self.pause_button.config(state='normal')
            self.add_message("游戏开始！", '#4caf50')
            self.game_loop()
            
    def toggle_pause(self):
        if self.game_running:
            self.game_paused = not self.game_paused
            if self.game_paused:
                self.pause_button.config(text="▶️")
                self.add_message("游戏暂停", '#ff9800')
            else:
                self.pause_button.config(text="⏸️")
                self.add_message("游戏继续", '#4caf50')
                self.game_loop()
                
    def reset_game(self):
        self.game_running = False
        self.game_paused = False
        self.snake = deque([(10, 10)])
        self.direction = (1, 0)
        self.score = 0
        self.capital = 10000
        self.trades = []
        self.teleport_count = 0
        self.animation_effects = []
        self.game_time = 0
        
        self.ai_mode = True
        self.random_mode = True
        self.auto_rhythm_enabled = True
        self.learning_from_human = True
        
        self.ai_collision_count = 0
        self.ai_food_collected = 0
        
        self.start_button.config(state='normal')
        self.pause_button.config(state='disabled', text="⏸️")
        
        self.generate_food()
        self.draw_game()
        self.update_stats()
        self.update_display()
        
        self.add_message("游戏已重置 - 全自动模式", '#2196f3')
        
    def game_over(self):
        self.game_running = False
        
        if self.trades:
            total_profit = sum(self.trades)
            win_rate = len([t for t in self.trades if t > 0]) / len(self.trades) * 100
            
            message = f"""
游戏结束!

📊 最终统计:
- 最终分数: {self.score}
- 最终资金: ${self.capital:,}
- 总盈亏: ${total_profit:+,.0f}
- 胜率: {win_rate:.1f}%
- 交易次数: {len(self.trades)}
- 传送次数: {self.teleport_count}

游戏将自动重新开始...
"""
        else:
            message = "游戏结束! 自动重新开始..."
            
        self.add_message(message, '#ff0000')
        
        # 自动重新开始
        self.root.after(3000, self.reset_game)
        self.root.after(3500, self.start_game)
        
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