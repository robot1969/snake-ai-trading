#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
量化交易贪吃蛇游戏 - 图表分析专业版
Chart Analysis Professional Version
"""

import tkinter as tk
from tkinter import messagebox, ttk
import random
import time
from collections import deque
import math

class ChartAnalysisSnake:
    """图表分析版 - 使用tkinter Canvas绘制专业图表"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🐍 量化交易贪吃蛇 - 图表分析专业版")
        self.root.configure(bg='#0a0a0f')
        self.root.geometry("1600x1000")
        
        # 游戏参数
        self.canvas_width = 500
        self.canvas_height = 500
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
        self.initial_capital = 10000
        self.teleport_count = 0
        self.game_time = 0
        
        # AI参数
        self.ai_mode = True
        self.ai_food_collected = 0
        self.ai_collision_count = 0
        
        # 详细数据记录
        self.trade_history = []  # 所有交易记录
        self.capital_history = deque(maxlen=200)  # 资金历史
        self.profit_loss_data = []  # 盈亏数据
        self.ai_decision_history = []  # AI决策历史
        self.speed_history = []  # 速度历史
        
        # 统计分析
        self.total_profit = 0
        self.total_loss = 0
        self.max_capital = 10000
        self.min_capital = 10000
        self.winning_trades = 0
        self.losing_trades = 0
        self.consecutive_wins = 0
        self.consecutive_losses = 0
        self.max_consecutive_wins = 0
        self.max_consecutive_losses = 0
        
        # 消息系统
        self.message_log = []
        self.max_messages = 15
        
        self.setup_gui()
        self.bind_keys()
        self.generate_food()
        
    def setup_gui(self):
        """设置GUI界面"""
        # 主容器
        main_frame = tk.Frame(self.root, bg='#0a0a0f')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 顶部控制栏
        control_frame = tk.Frame(main_frame, bg='#1a1a2e', relief=tk.RAISED, bd=2)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 标题
        tk.Label(control_frame, text="🐍 量化交易贪吃蛇 - 图表分析专业版", 
                font=('Arial', 16, 'bold'), bg='#1a1a2e', fg='#ffd700').pack(side=tk.LEFT, padx=20, pady=10)
        
        # 控制按钮
        btn_frame = tk.Frame(control_frame, bg='#1a1a2e')
        btn_frame.pack(side=tk.RIGHT, padx=20)
        
        self.start_btn = tk.Button(btn_frame, text="▶ 开始", command=self.start_game,
                                  bg='#4caf50', fg='white', font=('Arial', 11, 'bold'), width=10)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.pause_btn = tk.Button(btn_frame, text="⏸ 暂停", command=self.toggle_pause,
                                  bg='#ff9800', fg='white', font=('Arial', 11, 'bold'), width=10, state='disabled')
        self.pause_btn.pack(side=tk.LEFT, padx=5)
        
        self.reset_btn = tk.Button(btn_frame, text="🔄 重置", command=self.reset_game,
                                  bg='#f44336', fg='white', font=('Arial', 11, 'bold'), width=10)
        self.reset_btn.pack(side=tk.LEFT, padx=5)
        
        # 中间内容区（分为左右两部分）
        content_frame = tk.Frame(main_frame, bg='#0a0a0f')
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # 左侧游戏区域
        left_frame = tk.Frame(content_frame, bg='#1a1a2e', relief=tk.RAISED, bd=2)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 10))
        
        # 游戏画布
        self.game_canvas = tk.Canvas(left_frame, width=self.canvas_width, height=self.canvas_height,
                                    bg='#0a0a0f', highlightthickness=2, highlightbackground='#4a4a6e')
        self.game_canvas.pack(padx=15, pady=15)
        
        # 游戏状态信息
        info_frame = tk.Frame(left_frame, bg='#1a1a2e')
        info_frame.pack(fill=tk.X, padx=15, pady=10)
        
        # 分数和资金
        self.score_label = tk.Label(info_frame, text=f"分数: {self.score}",
                                   font=('Arial', 12, 'bold'), bg='#1a1a2e', fg='#ffd700')
        self.score_label.pack(side=tk.LEFT, padx=10)
        
        self.capital_label = tk.Label(info_frame, text=f"资金: ${self.capital:,}",
                                     font=('Arial', 12, 'bold'), bg='#1a1a2e', fg='#4caf50')
        self.capital_label.pack(side=tk.LEFT, padx=10)
        
        # 时间
        self.time_label = tk.Label(info_frame, text=f"时间: 00:00",
                                  font=('Arial', 11), bg='#1a1a2e', fg='#00bcd4')
        self.time_label.pack(side=tk.RIGHT, padx=10)
        
        # 消息日志
        msg_frame = tk.LabelFrame(left_frame, text="📋 实时日志", font=('Arial', 10, 'bold'),
                                 bg='#1a1a2e', fg='#ffffff')
        msg_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        self.msg_text = tk.Text(msg_frame, height=8, bg='#0a0a0f', fg='#00ff00',
                               font=('Consolas', 9), relief=tk.FLAT)
        self.msg_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        scrollbar = tk.Scrollbar(self.msg_text)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.msg_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.msg_text.yview)
        
        # 右侧图表区域
        right_frame = tk.Frame(content_frame, bg='#1a1a2e', relief=tk.RAISED, bd=2)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # 图表区域标题
        tk.Label(right_frame, text="📊 专业图表分析", font=('Arial', 14, 'bold'),
                bg='#1a1a2e', fg='#ffffff').pack(pady=10)
        
        # 创建4个图表
        charts_container = tk.Frame(right_frame, bg='#1a1a2e')
        charts_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 图表1: 资金曲线 (左上)
        self.setup_chart(charts_container, 'capital', "💰 资金曲线", 0, 0)
        
        # 图表2: 盈亏分布 (右上)
        self.setup_chart(charts_container, 'pnl', "📈 盈亏分布", 0, 1)
        
        # 图表3: AI效率 (左下)
        self.setup_chart(charts_container, 'ai', "🤖 AI效率分析", 1, 0)
        
        # 图表4: 交易统计 (右下)
        self.setup_chart(charts_container, 'trade', "🎯 交易统计", 1, 1)
        
        # 底部统计栏
        stats_frame = tk.Frame(main_frame, bg='#1a1a2e', relief=tk.RAISED, bd=2)
        stats_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.stat_labels = {}
        stats = [
            ("总盈亏", lambda: f"${self.total_profit - self.total_loss:+,.0f}"),
            ("盈利率", lambda: f"{((self.capital - self.initial_capital) / self.initial_capital * 100):+.2f}%"),
            ("胜率", lambda: f"{(self.winning_trades / max(1, self.winning_trades + self.losing_trades) * 100):.1f}%"),
            ("最高资金", lambda: f"${self.max_capital:,}"),
            ("最低资金", lambda: f"${self.min_capital:,}"),
            ("连续盈利", lambda: f"{self.consecutive_wins}"),
            ("连续亏损", lambda: f"{self.consecutive_losses}"),
            ("AI成功率", lambda: f"{(self.ai_food_collected / max(1, self.ai_food_collected + self.ai_collision_count) * 100):.1f}%"),
        ]
        
        for i, (name, func) in enumerate(stats):
            frame = tk.Frame(stats_frame, bg='#0f0f1e', relief=tk.RAISED, bd=1)
            frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)
            
            tk.Label(frame, text=name, font=('Arial', 9), bg='#0f0f1e', fg='#888888').pack(pady=2)
            var = tk.StringVar(value="0")
            self.stat_labels[name] = (var, func)
            tk.Label(frame, textvariable=var, font=('Arial', 10, 'bold'), bg='#0f0f1e', fg='#ffd700').pack(pady=2)
            
    def setup_chart(self, parent, chart_type, title, row, col):
        """设置单个图表"""
        frame = tk.LabelFrame(parent, text=title, font=('Arial', 10, 'bold'),
                             bg='#1a1a2e', fg='#ffffff')
        frame.grid(row=row, column=col, padx=5, pady=5, sticky='nsew')
        
        # 设置网格权重
        parent.columnconfigure(0, weight=1)
        parent.columnconfigure(1, weight=1)
        parent.rowconfigure(0, weight=1)
        parent.rowconfigure(1, weight=1)
        
        # 创建画布
        canvas_width = 350
        canvas_height = 200
        canvas = tk.Canvas(frame, width=canvas_width, height=canvas_height,
                          bg='#0a0a0f', highlightthickness=1, highlightbackground='#4a4a6e')
        canvas.pack(padx=5, pady=5)
        
        # 存储图表信息
        setattr(self, f'chart_{chart_type}', {
            'canvas': canvas,
            'width': canvas_width,
            'height': canvas_height,
            'type': chart_type
        })
        
    def bind_keys(self):
        self.root.bind('<space>', lambda e: self.toggle_pause())
        self.root.bind('<Escape>', lambda e: self.quit_game())
        
    def draw_game(self):
        """绘制游戏"""
        self.game_canvas.delete("all")
        
        # 网格
        for i in range(0, self.canvas_width, self.cell_size):
            self.game_canvas.create_line(i, 0, i, self.canvas_height, fill='#1a1a2e', width=1)
        for i in range(0, self.canvas_height, self.cell_size):
            self.game_canvas.create_line(0, i, self.canvas_width, i, fill='#1a1a2e', width=1)
            
        # 蛇
        for i, segment in enumerate(self.snake):
            x1 = segment[0] * self.cell_size
            y1 = segment[1] * self.cell_size
            x2 = x1 + self.cell_size
            y2 = y1 + self.cell_size
            
            if i == len(self.snake) - 1:
                self.game_canvas.create_oval(x1+2, y1+2, x2-2, y2-2,
                                            fill='#00ff00', outline='#00ff88', width=2)
            else:
                intensity = max(50, int(200 - (i * 150 / len(self.snake))))
                color = f'#{intensity:02x}ff{intensity:02x}'
                self.game_canvas.create_rectangle(x1+1, y1+1, x2-1, y2-1,
                                                 fill=color, outline='#00aa00')
                                                 
        # 食物
        if self.food:
            x1 = self.food[0] * self.cell_size
            y1 = self.food[1] * self.cell_size
            x2 = x1 + self.cell_size
            y2 = y1 + self.cell_size
            colors = ['#4caf50', '#f44336', '#2196f3', '#ff9800']
            food_color = random.choice(colors)
            self.game_canvas.create_oval(x1+3, y1+3, x2-3, y2-3,
                                          fill=food_color, outline='#ffffff', width=2)
                                          
    def draw_charts(self):
        """绘制所有图表"""
        self.draw_capital_chart()
        self.draw_pnl_chart()
        self.draw_ai_chart()
        self.draw_trade_chart()
        
    def draw_capital_chart(self):
        """绘制资金曲线图"""
        chart = self.chart_capital
        canvas = chart['canvas']
        width = chart['width']
        height = chart['height']
        
        canvas.delete("all")
        
        if len(self.capital_history) < 2:
            canvas.create_text(width//2, height//2, text="等待数据...",
                             fill='#666666', font=('Arial', 10))
            return
            
        # 边距
        margin = 30
        chart_width = width - 2 * margin
        chart_height = height - 2 * margin
        
        # 计算范围
        data = list(self.capital_history)
        min_val = min(data)
        max_val = max(data)
        val_range = max_val - min_val
        if val_range == 0:
            val_range = 1
            
        # 绘制网格
        for i in range(5):
            y = margin + i * chart_height // 4
            canvas.create_line(margin, y, width - margin, y, fill='#1a1a2e', width=1)
            
        # 绘制数据线
        points = []
        for i, val in enumerate(data):
            x = margin + i * chart_width // (len(data) - 1) if len(data) > 1 else margin
            y = height - margin - (val - min_val) / val_range * chart_height
            points.extend([x, y])
            
        if len(points) >= 4:
            # 渐变色根据盈亏
            color = '#4caf50' if data[-1] >= data[0] else '#f44336'
            canvas.create_line(points, fill=color, width=2, smooth=True)
            
            # 填充区域
            if len(points) >= 4:
                fill_points = points + [points[-2], height - margin, points[0], height - margin]
                canvas.create_polygon(fill_points, fill=color, stipple='gray25', outline='')
                
        # 标签
        canvas.create_text(margin, margin - 10, text=f"${max_val:,.0f}",
                          fill='#4caf50', font=('Arial', 8), anchor='w')
        canvas.create_text(margin, height - margin + 10, text=f"${min_val:,.0f}",
                          fill='#f44336', font=('Arial', 8), anchor='w')
        canvas.create_text(width - margin, margin - 10, text=f"当前: ${data[-1]:,.0f}",
                          fill='#ffd700', font=('Arial', 8, 'bold'), anchor='e')
                          
    def draw_pnl_chart(self):
        """绘制盈亏分布图"""
        chart = self.chart_pnl
        canvas = chart['canvas']
        width = chart['width']
        height = chart['height']
        
        canvas.delete("all")
        
        if not self.trade_history:
            canvas.create_text(width//2, height//2, text="等待交易数据...",
                             fill='#666666', font=('Arial', 10))
            return
            
        margin = 40
        chart_width = width - 2 * margin
        chart_height = height - 2 * margin
        
        # 统计正负交易
        profits = [t['amount'] for t in self.trade_history if t['amount'] > 0]
        losses = [t['amount'] for t in self.trade_history if t['amount'] < 0]
        
        profit_count = len(profits)
        loss_count = len(losses)
        total = profit_count + loss_count
        
        if total == 0:
            return
            
        # 绘制柱状图
        bar_width = 60
        spacing = 80
        
        # 盈利柱
        profit_height = profit_count / total * chart_height
        x1 = margin + 40
        y1 = height - margin - profit_height
        canvas.create_rectangle(x1, y1, x1 + bar_width, height - margin,
                               fill='#4caf50', outline='#2e7d32', width=2)
        canvas.create_text(x1 + bar_width//2, y1 - 10, text=f"盈利\n{profit_count}",
                          fill='#4caf50', font=('Arial', 9, 'bold'))
        
        # 亏损柱
        loss_height = loss_count / total * chart_height
        x2 = x1 + bar_width + spacing
        y2 = height - margin - loss_height
        canvas.create_rectangle(x2, y2, x2 + bar_width, height - margin,
                               fill='#f44336', outline='#c62828', width=2)
        canvas.create_text(x2 + bar_width//2, y2 - 10, text=f"亏损\n{loss_count}",
                          fill='#f44336', font=('Arial', 9, 'bold'))
        
        # 比例线
        win_rate = profit_count / total * 100
        mid_x = (x1 + bar_width + x2) / 2
        canvas.create_line(mid_x, margin, mid_x, height - margin,
                          fill='#ffd700', width=2, dash=(5, 5))
        canvas.create_text(mid_x, margin - 15, text=f"胜率 {win_rate:.1f}%",
                          fill='#ffd700', font=('Arial', 10, 'bold'))
                          
    def draw_ai_chart(self):
        """绘制AI效率图"""
        chart = self.chart_ai
        canvas = chart['canvas']
        width = chart['width']
        height = chart['height']
        
        canvas.delete("all")
        
        margin = 40
        
        total = self.ai_food_collected + self.ai_collision_count
        if total == 0:
            canvas.create_text(width//2, height//2, text="等待AI数据...",
                             fill='#666666', font=('Arial', 10))
            return
            
        success_rate = self.ai_food_collected / total
        
        # 绘制圆形进度条
        center_x = width // 2
        center_y = height // 2
        radius = min(60, min(width, height) // 2 - 20)
        
        # 背景圆
        canvas.create_oval(center_x - radius, center_y - radius,
                          center_x + radius, center_y + radius,
                          outline='#1a1a2e', width=8)
        
        # 进度弧
        extent = success_rate * 360
        color = '#4caf50' if success_rate > 0.6 else '#ff9800' if success_rate > 0.4 else '#f44336'
        
        # 绘制弧形
        canvas.create_arc(center_x - radius, center_y - radius,
                         center_x + radius, center_y + radius,
                         start=90, extent=-extent,
                         outline=color, width=8, style='arc')
        
        # 中心文字
        canvas.create_text(center_x, center_y, text=f"{success_rate*100:.1f}%",
                          fill='#ffffff', font=('Arial', 16, 'bold'))
        canvas.create_text(center_x, center_y + 25, text="成功率",
                          fill='#888888', font=('Arial', 9))
        
        # 统计
        canvas.create_text(margin, height - margin, text=f"成功: {self.ai_food_collected}",
                          fill='#4caf50', font=('Arial', 9), anchor='sw')
        canvas.create_text(width - margin, height - margin, text=f"失败: {self.ai_collision_count}",
                          fill='#f44336', font=('Arial', 9), anchor='se')
                          
    def draw_trade_chart(self):
        """绘制交易统计图"""
        chart = self.chart_trade
        canvas = chart['canvas']
        width = chart['width']
        height = chart['height']
        
        canvas.delete("all")
        
        margin = 30
        
        # 统计数据
        stats = [
            ("总交易", len(self.trade_history)),
            ("总盈利", f"${self.total_profit:,.0f}"),
            ("总亏损", f"${self.total_loss:,.0f}"),
            ("净盈亏", f"${self.total_profit - self.total_loss:+,.0f}"),
            ("最大连续盈", self.max_consecutive_wins),
            ("最大连续亏", self.max_consecutive_losses),
        ]
        
        y_pos = margin
        for name, value in stats:
            canvas.create_text(margin, y_pos, text=name + ":",
                              fill='#888888', font=('Arial', 9), anchor='w')
            
            # 颜色根据数值
            color = '#ffd700'
            if isinstance(value, (int, float)):
                if value > 0:
                    color = '#4caf50'
                elif value < 0:
                    color = '#f44336'
                    
            canvas.create_text(width - margin, y_pos, text=str(value),
                              fill=color, font=('Arial', 10, 'bold'), anchor='e')
            y_pos += 25
            
        # 如果数据足够，绘制趋势线
        if len(self.trade_history) >= 5:
            chart_height = 60
            chart_top = height - margin - chart_height
            chart_width = width - 2 * margin
            
            # 最近的交易盈亏
            recent_trades = self.trade_history[-20:]
            amounts = [t['amount'] for t in recent_trades]
            min_amt = min(amounts)
            max_amt = max(amounts)
            amt_range = max_amt - min_amt if max_amt != min_amt else 1
            
            points = []
            for i, amt in enumerate(amounts):
                x = margin + i * chart_width // (len(amounts) - 1)
                y = chart_top + chart_height - (amt - min_amt) / amt_range * chart_height
                points.extend([x, y])
                
            if len(points) >= 4:
                canvas.create_line(points, fill='#00bcd4', width=2, smooth=True)
                
            canvas.create_text(width//2, chart_top - 10, text="最近交易趋势",
                              fill='#00bcd4', font=('Arial', 9))
                              
    def generate_food(self):
        while True:
            x = random.randint(0, self.grid_size - 1)
            y = random.randint(0, self.grid_size - 1)
            if (x, y) not in self.snake:
                self.food = (x, y)
                break
                
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
                    
        except:
            pass
            
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
            
    def handle_collision(self):
        loss = 1500
        self.capital -= loss
        self.total_loss += loss
        self.teleport_count += 1
        self.score -= 5
        self.losing_trades += 1
        
        # 更新连续记录
        self.consecutive_losses += 1
        self.max_consecutive_losses = max(self.max_consecutive_losses, self.consecutive_losses)
        self.consecutive_wins = 0
        
        if self.ai_mode:
            self.ai_collision_count += 1
            
        self.snake.clear()
        self.snake.append((10, 10))
        
        self.add_message(f"传送! 损失 ${loss:,} | 次数: {self.teleport_count}")
        self.record_trade("传送损失", -loss)
        
        if self.capital <= 0:
            self.game_over()
            
    def eat_food(self):
        food_types = [
            {"name": "盈利交易", "amount": 1500},
            {"name": "亏损交易", "amount": -1200},
            {"name": "突破交易", "amount": 2000},
            {"name": "反转交易", "amount": 1800}
        ]
        
        food = random.choice(food_types)
        amount = food['amount']
        
        self.capital += amount
        self.score += 10 if amount > 0 else -5
        
        if amount > 0:
            self.total_profit += amount
            self.winning_trades += 1
            self.consecutive_wins += 1
            self.max_consecutive_wins = max(self.max_consecutive_wins, self.consecutive_wins)
            self.consecutive_losses = 0
            self.add_message(f"💰 {food['name']}: +${amount:,}")
        else:
            self.total_loss += abs(amount)
            self.losing_trades += 1
            self.consecutive_losses += 1
            self.max_consecutive_losses = max(self.max_consecutive_losses, self.consecutive_losses)
            self.consecutive_wins = 0
            self.add_message(f"📉 {food['name']}: ${amount:,}")
            
        if self.ai_mode and amount > 0:
            self.ai_food_collected += 1
            
        self.record_trade(food['name'], amount)
        self.generate_food()
        
        # 更新极值
        self.max_capital = max(self.max_capital, self.capital)
        self.min_capital = min(self.min_capital, self.capital)
        
        if self.capital <= 0:
            self.game_over()
            
    def record_trade(self, trade_type, amount):
        timestamp = time.strftime("%H:%M:%S")
        self.trade_history.append({
            'time': timestamp,
            'type': trade_type,
            'amount': amount,
            'cumulative': self.capital - self.initial_capital
        })
        
    def add_message(self, message):
        timestamp = time.strftime("%H:%M:%S")
        formatted = f"[{timestamp}] {message}"
        
        self.message_log.append(formatted)
        if len(self.message_log) > self.max_messages:
            self.message_log.pop(0)
            
        self.msg_text.delete(1.0, tk.END)
        for msg in self.message_log:
            self.msg_text.insert(tk.END, msg + '\n')
        self.msg_text.see(tk.END)
        
    def update_stats(self):
        """更新统计显示"""
        for name, (var, func) in self.stat_labels.items():
            try:
                var.set(func())
            except:
                var.set("N/A")
                
        # 记录资金历史
        if self.game_time % 5 == 0:  # 每5帧记录一次
            self.capital_history.append(self.capital)
            
        # 更新时间
        self.time_label.config(text=f"时间: {self.game_time//60:02d}:{self.game_time%60:02d}")
        
    def game_loop(self):
        if not self.game_running or self.game_paused:
            return
            
        self.game_time += 1
        
        if self.ai_mode:
            self.ai_make_move()
            
        if random.random() < 0.3:
            directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
            valid = [d for d in directions if (d[0] * -1, d[1] * -1) != self.direction]
            if valid:
                self.direction = random.choice(valid)
                
        if self.game_time % 50 == 0:
            self.game_speed = random.randint(80, 200)
            
        self.move_snake()
        self.draw_game()
        
        # 更新显示
        self.score_label.config(text=f"分数: {self.score}")
        capital_color = '#4caf50' if self.capital > 10000 else '#f44336' if self.capital < 5000 else '#ffd700'
        self.capital_label.config(text=f"资金: ${self.capital:,}", fg=capital_color)
        
        # 更新统计和图表
        if self.game_time % 10 == 0:
            self.update_stats()
            self.draw_charts()
            
        self.root.after(self.game_speed, self.game_loop)
        
    def start_game(self):
        self.game_running = True
        self.game_paused = False
        self.start_btn.config(state='disabled')
        self.pause_btn.config(state='normal')
        self.add_message("🚀 图表分析版启动！专业数据实时展示")
        self.game_loop()
        
    def toggle_pause(self):
        self.game_paused = not self.game_paused
        if self.game_paused:
            self.pause_btn.config(text="▶ 继续")
            self.add_message("⏸ 游戏暂停")
        else:
            self.pause_btn.config(text="⏸ 暂停")
            self.add_message("▶ 游戏继续")
            self.game_loop()
            
    def reset_game(self):
        self.game_running = False
        self.game_paused = False
        
        # 重置游戏状态
        self.snake.clear()
        self.snake.append((10, 10))
        self.direction = (1, 0)
        self.food = None
        self.score = 0
        self.capital = 10000
        self.teleport_count = 0
        self.game_time = 0
        
        # 重置AI
        self.ai_food_collected = 0
        self.ai_collision_count = 0
        
        # 重置统计
        self.total_profit = 0
        self.total_loss = 0
        self.max_capital = 10000
        self.min_capital = 10000
        self.winning_trades = 0
        self.losing_trades = 0
        self.consecutive_wins = 0
        self.consecutive_losses = 0
        self.max_consecutive_wins = 0
        self.max_consecutive_losses = 0
        
        # 清空历史
        self.trade_history.clear()
        self.capital_history.clear()
        
        # 重置UI
        self.start_btn.config(state='normal')
        self.pause_btn.config(state='disabled', text="⏸ 暂停")
        self.msg_text.delete(1.0, tk.END)
        
        self.draw_game()
        self.draw_charts()
        self.update_stats()
        
        self.add_message("🔄 游戏已重置")
        
    def game_over(self):
        self.game_running = False
        self.start_btn.config(state='normal')
        self.pause_btn.config(state='disabled', text="⏸ 暂停")
        
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
        game = ChartAnalysisSnake(root)
        root.mainloop()
    except Exception as e:
        print(f"游戏启动失败: {e}")
        import traceback
        traceback.print_exc()
        input("按回车键退出...")