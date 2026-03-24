#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
量化交易贪吃蛇游戏 - 超稳定版本增强版
Ultra Stable Version Enhanced with More Analytics
"""

import tkinter as tk
from tkinter import messagebox, ttk
import random
import time
from collections import deque

class TradingSnakeGameEnhanced:
    def __init__(self, root):
        self.root = root
        self.root.title("🐍 量化交易贪吃蛇 - 增强分析版")
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
        self.initial_capital = 10000
        self.trades = []
        self.trade_history = deque(maxlen=100)  # 交易历史
        self.teleport_count = 0
        self.food_lifetime = 0
        self.game_time = 0
        self.start_time = None  # 游戏开始时间
        
        # AI参数
        self.ai_mode = True
        self.random_mode = True
        self.auto_rhythm_enabled = True
        self.ai_food_collected = 0
        self.ai_collision_count = 0
        
        # 数据分析
        self.capital_history = []
        self.score_history = []
        self.profit_loss_history = deque(maxlen=50)  # 盈亏历史
        self.speed_history = deque(maxlen=30)  # 速度历史
        self.food_efficiency = []  # 食物获取效率
        self.total_moves = 0  # 总移动次数
        self.successful_moves = 0  # 成功移动次数
        
        # 统计数据
        self.total_profit = 0
        self.total_loss = 0
        self.max_capital = 10000
        self.min_capital = 10000
        self.best_trade = 0
        self.worst_trade = 0
        self.winning_trades = 0
        self.losing_trades = 0
        
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
            self.root.geometry("1400x800+50+50")
            self.root.minsize(1200, 700)
        except:
            pass
            
    def setup_gui(self):
        # 主容器
        main_frame = tk.Frame(self.root, bg='#1a1a2e')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 左侧游戏区域
        left_frame = tk.Frame(main_frame, bg='#1a1a2e')
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 10))
        
        # 游戏区域
        game_frame = tk.Frame(left_frame, bg='#1a1a2e', relief=tk.RAISED, bd=2)
        game_frame.pack(fill=tk.BOTH, expand=True)
        
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
        
        self.reset_button = tk.Button(btn_frame, text="🔄 重置", command=self.reset_game, bg='#f44336', fg='white', font=('Arial', 10, 'bold'), width=10)
        self.reset_button.pack(side=tk.LEFT, padx=5)
        
        # 状态显示
        status_frame = tk.Frame(control_frame, bg='#2d2d44')
        status_frame.pack(fill=tk.X, pady=10)
        
        self.status_label = tk.Label(status_frame, text="准备就绪", font=('Arial', 10), bg='#2d2d44', fg='#00ff00')
        self.status_label.pack()
        
        # 分数和资金显示
        score_frame = tk.Frame(game_frame, bg='#2d2d44')
        score_frame.pack(fill=tk.X, pady=5)
        
        self.score_label = tk.Label(score_frame, text=f"分数: {self.score}", font=('Arial', 12, 'bold'), bg='#2d2d44', fg='#ffd700')
        self.score_label.pack(side=tk.LEFT, padx=10)
        
        self.capital_label = tk.Label(score_frame, text=f"资金: ${self.capital:,}", font=('Arial', 12, 'bold'), bg='#2d2d44', fg='#4caf50')
        self.capital_label.pack(side=tk.LEFT, padx=10)
        
        # 右侧信息区域（分为上下两部分）
        right_frame = tk.Frame(main_frame, bg='#1a1a2e')
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # 上半部分：实时消息
        msg_frame = tk.LabelFrame(right_frame, text="📊 实时数据", font=('Arial', 12, 'bold'), bg='#1a1a2e', fg='#ffffff')
        msg_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
        
        self.info_text = tk.Text(msg_frame, height=12, bg='#0f0f1e', fg='#00ff00', font=('Consolas', 9), relief=tk.FLAT)
        self.info_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(self.info_text)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.info_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.info_text.yview)
        
        # 下半部分：详细分析数据（选项卡）
        tabs_frame = tk.Frame(right_frame, bg='#1a1a2e')
        tabs_frame.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        
        # 创建选项卡控件
        self.notebook = ttk.Notebook(tabs_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # 统计摘要选项卡
        self.stats_frame = tk.Frame(self.notebook, bg='#0f0f1e')
        self.notebook.add(self.stats_frame, text="📈 统计摘要")
        self.setup_stats_tab()
        
        # 历史记录选项卡
        self.history_frame = tk.Frame(self.notebook, bg='#0f0f1e')
        self.notebook.add(self.history_frame, text="📜 历史记录")
        self.setup_history_tab()
        
        # 性能分析选项卡
        self.performance_frame = tk.Frame(self.notebook, bg='#0f0f1e')
        self.notebook.add(self.performance_frame, text="⚡ 性能分析")
        self.setup_performance_tab()
        
        # AI分析选项卡
        self.ai_frame = tk.Frame(self.notebook, bg='#0f0f1e')
        self.notebook.add(self.ai_frame, text="🤖 AI分析")
        self.setup_ai_tab()
        
    def setup_stats_tab(self):
        """设置统计摘要选项卡"""
        # 创建网格布局
        stats_labels = [
            ("💰 总盈亏", lambda: f"${self.total_profit - self.total_loss:+,.0f}"),
            ("📈 盈利率", lambda: f"{((self.capital - self.initial_capital) / self.initial_capital * 100):+.2f}%"),
            ("🏆 最高资金", lambda: f"${self.max_capital:,}"),
            ("📉 最低资金", lambda: f"${self.min_capital:,}"),
            ("🎯 胜率", lambda: f"{(self.winning_trades / max(1, self.winning_trades + self.losing_trades) * 100):.1f}%"),
            ("📊 交易次数", lambda: f"{len(self.trades)}"),
            ("🏅 最佳交易", lambda: f"+${self.best_trade:,}"),
            ("🚫 最差交易", lambda: f"${self.worst_trade:,}"),
            ("⏱️ 游戏时间", lambda: f"{self.game_time // 60:02d}:{self.game_time % 60:02d}"),
            ("🐍 蛇身长度", lambda: f"{len(self.snake)}"),
            ("🌀 传送次数", lambda: f"{self.teleport_count}"),
            ("🎮 移动效率", lambda: f"{(self.successful_moves / max(1, self.total_moves) * 100):.1f}%"),
        ]
        
        self.stats_vars = []
        for i, (label_text, value_func) in enumerate(stats_labels):
            row = i // 2
            col = i % 2
            
            frame = tk.Frame(self.stats_frame, bg='#1a1a2e', relief=tk.RAISED, bd=1)
            frame.grid(row=row, column=col, padx=5, pady=5, sticky='nsew')
            
            tk.Label(frame, text=label_text, font=('Arial', 10, 'bold'), 
                    bg='#1a1a2e', fg='#4caf50').pack(pady=5)
            
            var = tk.StringVar(value="0")
            self.stats_vars.append((var, value_func))
            tk.Label(frame, textvariable=var, font=('Arial', 12, 'bold'), 
                    bg='#0f0f1e', fg='#ffd700').pack(pady=5)
        
        # 设置列权重
        self.stats_frame.columnconfigure(0, weight=1)
        self.stats_frame.columnconfigure(1, weight=1)
        
    def setup_history_tab(self):
        """设置历史记录选项卡"""
        # 交易历史列表
        columns = ('时间', '类型', '金额', '累计盈亏')
        self.history_tree = ttk.Treeview(self.history_frame, columns=columns, show='headings', height=10)
        
        for col in columns:
            self.history_tree.heading(col, text=col)
            self.history_tree.column(col, width=120, anchor='center')
        
        self.history_tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # 滚动条
        scrollbar = ttk.Scrollbar(self.history_tree, orient=tk.VERTICAL, command=self.history_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.history_tree.config(yscrollcommand=scrollbar.set)
        
    def setup_performance_tab(self):
        """设置性能分析选项卡"""
        # 速度历史
        tk.Label(self.performance_frame, text="⏱️ 游戏速度历史", font=('Arial', 11, 'bold'), 
                bg='#0f0f1e', fg='#00ff00').pack(pady=5)
        
        self.speed_text = tk.Text(self.performance_frame, height=6, bg='#0f0f1e', fg='#00ff00', font=('Consolas', 9))
        self.speed_text.pack(padx=10, pady=5, fill=tk.X)
        
        # 资本曲线文本展示
        tk.Label(self.performance_frame, text="💰 资金曲线 (最近20个点)", font=('Arial', 11, 'bold'), 
                bg='#0f0f1e', fg='#00ff00').pack(pady=5)
        
        self.capital_curve_text = tk.Text(self.performance_frame, height=8, bg='#0f0f1e', fg='#00ff00', font=('Consolas', 9))
        self.capital_curve_text.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        
    def setup_ai_tab(self):
        """设置AI分析选项卡"""
        # AI决策统计
        ai_stats = [
            ("🧠 AI食物收集", lambda: f"{self.ai_food_collected}"),
            ("💥 AI碰撞次数", lambda: f"{self.ai_collision_count}"),
            ("🎯 AI成功率", lambda: f"{(self.ai_food_collected / max(1, self.ai_food_collected + self.ai_collision_count) * 100):.1f}%"),
            ("🔄 当前速度", lambda: f"{self.game_speed}ms"),
            ("📊 当前模式", lambda: f"AI:{self.ai_mode} 随机:{self.random_mode} 节奏:{self.auto_rhythm_enabled}"),
        ]
        
        for i, (label_text, value_func) in enumerate(ai_stats):
            frame = tk.Frame(self.ai_frame, bg='#1a1a2e')
            frame.pack(fill=tk.X, padx=10, pady=5)
            
            tk.Label(frame, text=label_text, font=('Arial', 10), 
                    bg='#1a1a2e', fg='#4caf50').pack(side=tk.LEFT)
            
            var = tk.StringVar(value="0")
            tk.Label(frame, textvariable=var, font=('Arial', 10, 'bold'), 
                    bg='#0f0f1e', fg='#ffd700').pack(side=tk.RIGHT)
        
        # AI效率图表（文本形式）
        tk.Label(self.ai_frame, text="📈 AI效率趋势", font=('Arial', 11, 'bold'), 
                bg='#0f0f1e', fg='#00ff00').pack(pady=10)
        
        self.ai_efficiency_text = tk.Text(self.ai_frame, height=10, bg='#0f0f1e', fg='#00ff00', font=('Consolas', 9))
        self.ai_efficiency_text.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        
    def bind_keys(self):
        self.root.bind('<space>', lambda e: self.toggle_pause())
        self.root.bind('<Escape>', lambda e: self.quit_game())
        self.root.bind('<Up>', lambda e: self.change_direction(0, -1))
        self.root.bind('<Down>', lambda e: self.change_direction(0, 1))
        self.root.bind('<Left>', lambda e: self.change_direction(-1, 0))
        self.root.bind('<Right>', lambda e: self.change_direction(1, 0))
        
    def change_direction(self, x, y):
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
            
        self.total_moves += 1
        head = self.snake[-1]
        new_head = (
            (head[0] + self.direction[0]) % self.grid_size,
            (head[1] + self.direction[1]) % self.grid_size
        )
        
        if new_head in self.snake:
            self.handle_collision()
            return
            
        self.snake.append(new_head)
        self.successful_moves += 1
        
        if new_head == self.food:
            self.eat_food()
        else:
            self.snake.popleft()
            
        self.food_lifetime -= 1
        if self.food_lifetime <= 0:
            self.generate_food()
            
    def handle_collision(self):
        self.capital -= 1500
        self.total_loss += 1500
        self.teleport_count += 1
        self.score -= 5
        
        if self.ai_mode:
            self.ai_collision_count += 1
            
        self.snake.clear()
        self.snake.append((10, 10))
        
        self.add_message(f"传送! 损失 $1500 | 传送次数: {self.teleport_count}")
        self.record_trade("传送损失", -1500)
        
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
            self.total_profit += profit
            self.score += 10
            self.trades.append(profit)
            self.winning_trades += 1
            self.best_trade = max(self.best_trade, profit)
            self.add_message(f"💰 {food_type['name']}: +${profit}")
            self.record_trade(food_type['name'], profit)
            if self.ai_mode:
                self.ai_food_collected += 1
        else:
            loss = food_type["loss"]
            self.capital -= loss
            self.total_loss += loss
            self.score -= 5
            self.trades.append(-loss)
            self.losing_trades += 1
            self.worst_trade = min(self.worst_trade, -loss)
            self.add_message(f"📉 {food_type['name']}: -${loss}")
            self.record_trade(food_type['name'], -loss)
            
        self.generate_food()
        
        if self.capital <= 0:
            self.game_over()
            
    def record_trade(self, trade_type, amount):
        """记录交易到历史"""
        timestamp = time.strftime("%H:%M:%S")
        self.trade_history.append({
            'time': timestamp,
            'type': trade_type,
            'amount': amount,
            'cumulative': self.capital - self.initial_capital
        })
        
        # 更新历史表格
        cumulative = self.capital - self.initial_capital
        self.history_tree.insert('', 0, values=(timestamp, trade_type, f"${amount:+,}", f"${cumulative:+,}"))
        
        # 限制历史表格行数
        if len(self.history_tree.get_children()) > 20:
            self.history_tree.delete(self.history_tree.get_children()[-1])
            
    def ai_make_move(self):
        try:
            if not self.snake or not self.food:
                return
                
            head = self.snake[-1]
            food_dx = self.food[0] - head[0]
            food_dy = self.food[1] - head[1]
            
            possible_moves = [(0, -1), (0, 1), (-1, 0), (1, 0)]
            valid_moves = [m for m in possible_moves if (m[0] * -1, m[1] * -1) != self.direction]
            
            if valid_moves:
                if abs(food_dx) > abs(food_dy):
                    best_move = (1, 0) if food_dx > 0 else (-1, 0)
                else:
                    best_move = (0, 1) if food_dy > 0 else (0, -1)
                    
                if best_move in valid_moves and random.random() < 0.8:
                    self.direction = best_move
                    
        except Exception as e:
            pass
            
    def apply_rhythm_mode(self):
        if self.game_time % 50 == 0:
            old_speed = self.game_speed
            self.game_speed = random.randint(80, 200)
            if self.game_time % 100 == 0:
                self.speed_history.append(f"T{self.game_time}: {old_speed}→{self.game_speed}ms")
            
    def game_loop(self):
        if not self.game_running or self.game_paused:
            return
            
        self.game_time += 1
            
        if self.ai_mode:
            self.ai_make_move()
                
        if self.random_mode and random.random() < 0.3:
            directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
            valid_directions = [d for d in directions if (d[0] * -1, d[1] * -1) != self.direction]
            if valid_directions:
                self.direction = random.choice(valid_directions)
                
        self.apply_rhythm_mode()
                
        self.move_snake()
        self.draw_game()
        
        # 更新统计
        if self.game_time % 10 == 0:
            self.update_stats()
            self.update_performance_data()
            self.update_ai_data()
            
        if self.game_time % 20 == 0:
            self.update_display()
            
        if self.game_time % 50 == 0:
            self.record_performance_data()
            
        if self.game_time % 200 == 0:
            self.add_status_message()
            
        try:
            self.root.after(self.game_speed, self.game_loop)
        except:
            pass
            
    def update_stats(self):
        """更新统计数据"""
        # 更新资金极值
        self.max_capital = max(self.max_capital, self.capital)
        self.min_capital = min(self.min_capital, self.capital)
        
        # 更新统计标签
        for var, func in self.stats_vars:
            try:
                var.set(func())
            except:
                var.set("N/A")
                
    def update_performance_data(self):
        """更新性能数据"""
        # 更新速度历史
        if self.speed_history:
            self.speed_text.delete(1.0, tk.END)
            for speed_record in list(self.speed_history)[-10:]:
                self.speed_text.insert(tk.END, speed_record + '\n')
                
        # 更新资金曲线
        if self.capital_history:
            self.capital_curve_text.delete(1.0, tk.END)
            recent_capital = self.capital_history[-20:]
            chart_height = 10
            if len(recent_capital) > 1:
                min_val = min(recent_capital)
                max_val = max(recent_capital)
                range_val = max_val - min_val if max_val != min_val else 1
                
                for i, val in enumerate(recent_capital):
                    normalized = int((val - min_val) / range_val * chart_height)
                    bar = '█' * normalized + '░' * (chart_height - normalized)
                    change = ""
                    if i > 0:
                        diff = val - recent_capital[i-1]
                        change = f" ({diff:+.0f})"
                    self.capital_curve_text.insert(tk.END, f"{bar} ${val:,}{change}\n")
                    
    def update_ai_data(self):
        """更新AI数据"""
        if self.ai_food_collected > 0 or self.ai_collision_count > 0:
            efficiency = self.ai_food_collected / (self.ai_food_collected + self.ai_collision_count) * 100
            self.ai_efficiency_text.delete(1.0, tk.END)
            self.ai_efficiency_text.insert(tk.END, f"AI效率: {efficiency:.1f}%\n")
            self.ai_efficiency_text.insert(tk.END, f"成功/失败: {self.ai_food_collected}/{self.ai_collision_count}\n")
            
            # 简单的效率条
            bar_length = 20
            filled = int(efficiency / 100 * bar_length)
            bar = '█' * filled + '░' * (bar_length - filled)
            self.ai_efficiency_text.insert(tk.END, f"[{bar}]\n")
            
    def update_display(self):
        self.score_label.config(text=f"分数: {self.score}")
        capital_color = '#4caf50' if self.capital > 10000 else '#f44336' if self.capital < 5000 else '#ffd700'
        self.capital_label.config(text=f"资金: ${self.capital:,}", fg=capital_color)
        
        status_text = f"游戏时间: {self.game_time//60:02d}:{self.game_time%60:02d} | 蛇身长度: {len(self.snake)} | 交易次数: {len(self.trades)}"
        self.status_label.config(text=status_text)
        
    def record_performance_data(self):
        if isinstance(self.capital_history, list):
            self.capital_history.append(self.capital)
            self.score_history.append(self.score)
            
            if len(self.capital_history) > 50:
                self.capital_history = self.capital_history[-50:]
            if len(self.score_history) > 50:
                self.score_history = self.score_history[-50:]
                
    def add_status_message(self):
        messages = [
            f"🧠 AI状态: 效率{(self.ai_food_collected / max(1, self.ai_food_collected + self.ai_collision_count) * 100):.0f}% | 运行中",
            f"🎯 游戏进度: 时间{self.game_time//60:02d}:{self.game_time%60:02d} | 移动{self.total_moves}",
            f"💰 资金状态: ${self.capital:,} | 收益率{((self.capital-10000)/10000)*100:+.1f}%",
            f"🤖 性能指标: 胜率{(self.winning_trades / max(1, self.winning_trades + self.losing_trades) * 100):.0f}% | 传送{self.teleport_count}",
            f"📊 模式状态: AI{'✅' if self.ai_mode else '❌'} | 随机{'✅' if self.random_mode else '❌'} | 节奏{'✅' if self.auto_rhythm_enabled else '❌'}"
        ]
        
        message = random.choice(messages)
        self.add_message(message)
        
    def add_message(self, message):
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
        try:
            self.game_running = True
            self.game_paused = False
            self.start_button.config(state='disabled')
            self.pause_button.config(state='normal')
            self.start_time = time.time()
            
            self.add_message("🚀 增强分析版启动！更多数据实时展示")
            self.game_loop()
        except:
            self.add_message("❌ 启动失败")
            
    def start_game(self):
        self.game_running = True
        self.game_paused = False
        self.start_button.config(state='disabled')
        self.pause_button.config(state='normal')
        self.start_time = time.time()
        
        self.add_message("🎮 游戏开始！")
        self.game_loop()
        
    def toggle_pause(self):
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
        
        self.snake.clear()
        self.snake.append((10, 10))
        self.direction = (1, 0)
        self.food = None
        self.score = 0
        self.capital = 10000
        self.teleport_count = 0
        self.game_time = 0
        self.total_moves = 0
        self.successful_moves = 0
        
        self.ai_collision_count = 0
        self.ai_food_collected = 0
        
        # 重置统计数据
        self.total_profit = 0
        self.total_loss = 0
        self.max_capital = 10000
        self.min_capital = 10000
        self.best_trade = 0
        self.worst_trade = 0
        self.winning_trades = 0
        self.losing_trades = 0
        
        self.trades.clear()
        self.trade_history.clear()
        self.speed_history.clear()
        
        self.capital_history.clear()
        self.score_history.clear()
        
        self.start_button.config(state='normal')
        self.pause_button.config(state='disabled', text="⏸️ 暂停")
        
        self.canvas.delete("all")
        self.info_text.delete(1.0, tk.END)
        self.history_tree.delete(*self.history_tree.get_children())
        self.speed_text.delete(1.0, tk.END)
        self.capital_curve_text.delete(1.0, tk.END)
        self.ai_efficiency_text.delete(1.0, tk.END)
        
        self.draw_game()
        self.update_display()
        
        self.add_message("🔄 游戏已重置")
        
    def game_over(self):
        self.game_running = False
        self.start_button.config(state='normal')
        self.pause_button.config(state='disabled', text="⏸️ 暂停")
        
        # 计算统计
        total_trades = self.winning_trades + self.losing_trades
        win_rate = (self.winning_trades / total_trades * 100) if total_trades > 0 else 0
        final_profit = self.capital - self.initial_capital
        
        messagebox.showinfo("游戏结束", 
            f"💀 资金耗尽！游戏结束\n\n" +
            f"🎯 最终分数: {self.score}\n" +
            f"💰 最终资金: ${self.capital:,}\n" +
            f"📊 总盈亏: ${final_profit:+,.0f}\n" +
            f"🏆 最高资金: ${self.max_capital:,}\n" +
            f"📉 最低资金: ${self.min_capital:,}\n" +
            f"🎯 胜率: {win_rate:.1f}%\n" +
            f"🌀 传送次数: {self.teleport_count}\n" +
            f"⏱️ 游戏时长: {self.game_time//60:02d}:{self.game_time%60:02d}")
        
    def quit_game(self):
        if self.game_running:
            if messagebox.askokcancel("退出", "确定要退出游戏吗？"):
                self.root.quit()
        else:
            self.root.quit()
            
if __name__ == "__main__":
    try:
        root = tk.Tk()
        game = TradingSnakeGameEnhanced(root)
        root.mainloop()
    except Exception as e:
        print(f"游戏启动失败: {e}")
        input("按回车键退出...")