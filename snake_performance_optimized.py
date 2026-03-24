#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
量化交易贪吃蛇游戏 - 性能优化版
Performance Optimized Version with Advanced Charting
"""

import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
import math
from collections import deque, defaultdict
import threading

class PerformanceOptimizedTradingSnake:
    def __init__(self, root):
        self.root = root
        self.root.title("🐍 量化交易贪吃蛇 - 性能优化版")
        self.root.configure(bg='#0a0a0f')
        self.root.geometry("1400x900")
        
        # 性能优化参数
        self.max_history_points = 100  # 限制历史数据点
        self.chart_update_interval = 500  # 图表更新间隔(ms)
        self.memory_cleanup_interval = 1000  # 内存清理间隔
        self.last_chart_update = 0
        self.last_memory_cleanup = 0
        
        # 游戏核心参数
        self.canvas_width = 600
        self.canvas_height = 600
        self.grid_size = 20
        self.cell_size = self.canvas_width // self.grid_size
        
        # 游戏状态
        self.snake = deque([(10, 10)], maxlen=400)  # 限制蛇身最大长度
        self.direction = (1, 0)
        self.food = None
        self.game_running = False
        self.game_paused = False
        self.game_speed = 150
        self.base_speed = 150
        self.score = 0
        self.capital = 10000
        self.trades = deque(maxlen=50)  # 限制交易记录
        self.teleport_count = 0
        self.food_lifetime = 0
        self.game_time = 0
        
        # AI优化参数
        self.ai_mode = True
        self.random_mode = True
        self.auto_rhythm_enabled = True
        self.ai_q_table = {}
        self.ai_learning_rate = 0.1
        self.ai_epsilon = 0.1
        self.ai_collision_count = 0
        self.ai_food_collected = 0
        
        # 性能数据记录（使用deque限制内存）
        self.capital_history = deque(maxlen=self.max_history_points)
        self.score_history = deque(maxlen=self.max_history_points)
        self.performance_metrics = deque(maxlen=60)  # 保存60秒的性能数据
        self.message_history = deque(maxlen=100)  # 限制消息历史
        
        # 图表相关
        self.chart_canvases = {}
        self.chart_data_cache = {}
        self.rendering_buffer = {}
        
        # 性能监控
        self.fps_counter = 0
        self.fps_last_time = time.time()
        self.current_fps = 0
        
        # 创建UI
        self.setup_ui()
        self.bind_keys()
        
        # 启动性能监控线程
        self.start_performance_monitoring()
        
    def setup_ui(self):
        main_container = tk.Frame(self.root, bg='#0a0a0f')
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 左侧游戏区域
        game_area = tk.Frame(main_container, bg='#1a1a2e', relief=tk.RAISED, bd=2)
        game_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)
        
        # 游戏画布
        self.canvas = tk.Canvas(game_area, width=self.canvas_width, height=self.canvas_height, 
                               bg='#0a0a0f', highlightthickness=2, highlightbackground='#4a4a6e')
        self.canvas.pack(padx=10, pady=10)
        
        # 控制面板
        control_panel = tk.Frame(game_area, bg='#1a1a2e')
        control_panel.pack(fill=tk.X, padx=10, pady=5)
        
        self.start_button = tk.Button(control_panel, text="🎮 开始", command=self.start_game,
                                     bg='#4caf50', fg='white', font=('Arial', 10, 'bold'), width=10)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.pause_button = tk.Button(control_panel, text="⏸️ 暂停", command=self.toggle_pause,
                                     bg='#ff9800', fg='white', font=('Arial', 10, 'bold'), width=10, state='disabled')
        self.pause_button.pack(side=tk.LEFT, padx=5)
        
        self.reset_button = tk.Button(control_panel, text="🔄 重置", command=self.reset_game,
                                     bg='#f44336', fg='white', font=('Arial', 10, 'bold'), width=10)
        self.reset_button.pack(side=tk.LEFT, padx=5)
        
        # 状态显示
        status_frame = tk.Frame(game_area, bg='#1a1a2e')
        status_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.status_label = tk.Label(status_frame, text="准备就绪", font=('Arial', 10, 'bold'),
                                    bg='#1a1a2e', fg='#00ff00')
        self.status_label.pack()
        
        # 分数和资金显示
        score_frame = tk.Frame(game_area, bg='#1a1a2e')
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
        
        # 右侧数据可视化区域
        viz_area = tk.Frame(main_container, bg='#1a1a2e', relief=tk.RAISED, bd=2)
        viz_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # 标题
        tk.Label(viz_area, text="📊 性能优化数据监控", font=('Arial', 14, 'bold'),
                bg='#1a1a2e', fg='#ffffff').pack(pady=10)
        
        # 创建优化的图表
        self.create_optimized_charts(viz_area)
        
        # 性能指标面板
        self.create_performance_panel(viz_area)
        
        # 消息系统
        self.create_message_system(viz_area)
        
    def create_optimized_charts(self, parent):
        """创建优化的图表系统"""
        chart_container = tk.Frame(parent, bg='#1a1a2e')
        chart_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 资金曲线图
        capital_frame = tk.LabelFrame(chart_container, text="💰 资金曲线", 
                                     bg='#1a1a2e', fg='#ffffff', font=('Arial', 10, 'bold'))
        capital_frame.pack(fill=tk.X, pady=5)
        
        self.chart_canvases['capital'] = tk.Canvas(capital_frame, width=500, height=150, 
                                                   bg='#0a0a0f', highlightthickness=1,
                                                   highlightbackground='#4a4a6e')
        self.chart_canvases['capital'].pack(padx=5, pady=5)
        
        # AI性能图
        ai_frame = tk.LabelFrame(chart_container, text="🤖 AI性能", 
                                bg='#1a1a2e', fg='#ffffff', font=('Arial', 10, 'bold'))
        ai_frame.pack(fill=tk.X, pady=5)
        
        self.chart_canvases['ai_performance'] = tk.Canvas(ai_frame, width=500, height=150, 
                                                         bg='#0a0a0f', highlightthickness=1,
                                                         highlightbackground='#4a4a6e')
        self.chart_canvases['ai_performance'].pack(padx=5, pady=5)
        
        # 交易分析图
        trade_frame = tk.LabelFrame(chart_container, text="📈 交易分析", 
                                   bg='#1a1a2e', fg='#ffffff', font=('Arial', 10, 'bold'))
        trade_frame.pack(fill=tk.X, pady=5)
        
        self.chart_canvases['trade_analysis'] = tk.Canvas(trade_frame, width=500, height=150, 
                                                          bg='#0a0a0f', highlightthickness=1,
                                                          highlightbackground='#4a4a6e')
        self.chart_canvases['trade_analysis'].pack(padx=5, pady=5)
        
    def create_performance_panel(self, parent):
        """创建性能指标面板"""
        perf_frame = tk.LabelFrame(parent, text="⚡ 性能指标", 
                                  bg='#1a1a2e', fg='#ffffff', font=('Arial', 10, 'bold'))
        perf_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.perf_text = tk.Text(perf_frame, height=6, width=60, 
                                bg='#0a0a0f', fg='#00ff00', font=('Consolas', 9),
                                relief=tk.FLAT)
        self.perf_text.pack(padx=5, pady=5)
        
    def create_message_system(self, parent):
        """创建优化的消息系统"""
        msg_frame = tk.LabelFrame(parent, text="📝 实时消息", 
                                 bg='#1a1a2e', fg='#ffffff', font=('Arial', 10, 'bold'))
        msg_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 创建带滚动条的文本框
        text_frame = tk.Frame(msg_frame, bg='#1a1a2e')
        text_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.message_text = tk.Text(text_frame, height=10, width=60, 
                                   bg='#0a0a0f', fg='#00ff00', font=('Consolas', 9),
                                   relief=tk.FLAT, wrap=tk.WORD)
        self.message_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.message_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.message_text.config(yscrollcommand=scrollbar.set)
        
    def bind_keys(self):
        """绑定键盘事件"""
        self.root.bind('<space>', lambda e: self.toggle_pause())
        self.root.bind('<Escape>', lambda e: self.quit_game())
        self.root.bind('<Up>', lambda e: self.change_direction(0, -1))
        self.root.bind('<Down>', lambda e: self.change_direction(0, 1))
        self.root.bind('<Left>', lambda e: self.change_direction(-1, 0))
        self.root.bind('<Right>', lambda e: self.change_direction(1, 0))
        
    def change_direction(self, x, y):
        """手动控制方向（在AI模式下禁用）"""
        if not self.ai_mode:
            new_dir = (x, y)
            if new_dir != (-self.direction[0], -self.direction[1]):  # 防止反向移动
                self.direction = new_dir
                
    def start_performance_monitoring(self):
        """启动性能监控 - 使用主线程更新UI，避免线程安全问题"""
        # 不再使用后台线程，改为在主循环中监控
        self.monitor_performance()
        
    def monitor_performance(self):
        """在主线程中监控性能"""
        current_time = time.time()
        
        # 计算FPS
        self.fps_counter += 1
        if current_time - self.fps_last_time >= 1.0:
            self.current_fps = self.fps_counter
            self.fps_counter = 0
            self.fps_last_time = current_time
            
            # 更新性能指标显示
            if self.root.winfo_exists():
                self.update_performance_metrics()
        
        # 定期清理内存
        if current_time - self.last_memory_cleanup > self.memory_cleanup_interval / 1000:
            self.cleanup_memory()
            self.last_memory_cleanup = current_time
        
    def update_performance_metrics(self):
        """更新性能指标显示 - 在主线程中安全调用"""
        # 更新FPS显示
        self.fps_label.config(text=f"FPS: {self.current_fps}")
        
        # 计算内存使用情况
        q_table_size = len(self.ai_q_table)
        history_size = len(self.capital_history)
        message_size = len(self.message_history)
        
        # 更新性能面板
        perf_info = f"""当前FPS: {self.current_fps}
Q表大小: {q_table_size:,} 条目
历史数据: {history_size}/{self.max_history_points}
消息缓存: {message_size}/100
游戏时长: {self.game_time//60:02d}:{self.game_time%60:02d}
内存清理: {'OK' if time.time() - self.last_memory_cleanup < 2 else '-'}"""
        
        self.perf_text.delete(1.0, tk.END)
        self.perf_text.insert(1.0, perf_info)
            
    def cleanup_memory(self):
        """定期清理内存"""
        # 清理过期的Q表条目（保持最近使用的）
        if len(self.ai_q_table) > 10000:
            # 简单的清理策略：保留一半条目
            keys_to_keep = list(self.ai_q_table.keys())[-5000:]
            new_q_table = {}
            for key in keys_to_keep:
                new_q_table[key] = self.ai_q_table[key]
            self.ai_q_table = new_q_table
            
        # 清理图表缓存
        self.chart_data_cache.clear()
        
        self.add_message("🧹 执行内存清理", "system")
        
    def add_message(self, message, msg_type="info"):
        """添加消息到消息系统"""
        current_time = time.strftime("%H:%M:%S")
        
        # 根据消息类型设置颜色
        colors = {
            "info": "#00ff00",
            "trade": "#ffd700",
            "ai": "#00bcd4",
            "system": "#ff9800",
            "error": "#f44336"
        }
        
        color = colors.get(msg_type, "#00ff00")
        formatted_message = f"[{current_time}] {message}\n"
        
        self.message_history.append((formatted_message, color))
        
        # 更新显示
        self.message_text.config(state=tk.NORMAL)
        self.message_text.insert(tk.END, formatted_message)
        self.message_text.tag_add("last_line", "end-2l", "end-1l")
        self.message_text.tag_config("last_line", foreground=color)
        self.message_text.config(state=tk.DISABLED)
        
        # 自动滚动到底部
        self.message_text.see(tk.END)
        
        # 限制消息历史长度
        if len(self.message_history) > 100:
            self.message_text.config(state=tk.NORMAL)
            self.message_text.delete(1.0, 2.0)
            self.message_text.config(state=tk.DISABLED)
            
    def generate_food(self):
        """生成食物"""
        while True:
            x = random.randint(0, self.grid_size - 1)
            y = random.randint(0, self.grid_size - 1)
            if (x, y) not in self.snake:
                self.food = (x, y)
                self.food_lifetime = random.randint(50, 150)
                break
                
    def draw_game(self):
        """绘制游戏画面（优化版）"""
        self.canvas.delete("all")
        
        # 绘制网格背景
        for i in range(0, self.canvas_width, self.cell_size):
            self.canvas.create_line(i, 0, i, self.canvas_height, fill='#1a1a2e', width=1)
        for i in range(0, self.canvas_height, self.cell_size):
            self.canvas.create_line(0, i, self.canvas_width, i, fill='#1a1a2e', width=1)
            
        # 绘制蛇身（优化渲染）
        for i, segment in enumerate(self.snake):
            x1 = segment[0] * self.cell_size
            y1 = segment[1] * self.cell_size
            x2 = x1 + self.cell_size
            y2 = y1 + self.cell_size
            
            if i == len(self.snake) - 1:  # 蛇头
                self.canvas.create_oval(x1+2, y1+2, x2-2, y2-2, 
                                     fill='#00ff00', outline='#00ff88', width=2)
            else:  # 蛇身
                intensity = max(50, int(255 - (i * 200 / len(self.snake))))
                color = f'#{intensity:02x}ff{intensity:02x}'
                self.canvas.create_rectangle(x1+1, y1+1, x2-1, y2-1, 
                                           fill=color, outline='#00aa00')
                
        # 绘制食物
        if self.food:
            x1 = self.food[0] * self.cell_size
            y1 = self.food[1] * self.cell_size
            x2 = x1 + self.cell_size
            y2 = y1 + self.cell_size
            
            # 根据食物类型选择颜色
            colors = ['#4caf50', '#f44336', '#2196f3', '#ff9800']
            food_color = random.choice(colors)
            
            self.canvas.create_oval(x1+3, y1+3, x2-3, y2-3, 
                                  fill=food_color, outline='#ffffff', width=2)
                                  
    def update_charts_optimized(self):
        """优化版图表更新"""
        current_time = time.time() * 1000  # 转换为毫秒
        
        # 限制更新频率
        if current_time - self.last_chart_update < self.chart_update_interval:
            return
            
        self.last_chart_update = current_time
        
        # 更新资金曲线图
        self.draw_capital_chart_optimized()
        
        # 更新AI性能图
        self.draw_ai_performance_chart()
        
        # 更新交易分析图
        self.draw_trade_analysis_chart()
        
    def draw_capital_chart_optimized(self):
        """优化版资金曲线图"""
        canvas = self.chart_canvases['capital']
        canvas.delete("all")
        
        if len(self.capital_history) < 2:
            canvas.create_text(250, 75, text="等待数据...", fill='#666666', font=('Arial', 10))
            return
            
        # 计算缩放比例
        min_capital = min(self.capital_history)
        max_capital = max(self.capital_history)
        range_capital = max_capital - min_capital
        if range_capital == 0:
            range_capital = 1
            
        width = 500
        height = 150
        padding = 10
        
        # 绘制背景网格
        for i in range(5):
            y = padding + i * (height - 2*padding) // 4
            canvas.create_line(padding, y, width-padding, y, fill='#1a1a2e', width=1)
            
        # 绘制曲线
        points = []
        for i, capital in enumerate(self.capital_history):
            x = padding + i * (width - 2*padding) // (len(self.capital_history) - 1)
            y = height - padding - int((capital - min_capital) / range_capital * (height - 2*padding))
            points.extend([x, y])
            
        if len(points) >= 4:
            canvas.create_line(points, fill='#4caf50', width=2, smooth=True)
            
        # 绘制当前值
        current_value = self.capital_history[-1]
        canvas.create_text(width-5, padding, text=f"${current_value:.0f}", 
                          anchor='ne', fill='#4caf50', font=('Arial', 9, 'bold'))
                          
    def draw_ai_performance_chart(self):
        """绘制AI性能图"""
        canvas = self.chart_canvases['ai_performance']
        canvas.delete("all")
        
        width = 500
        height = 150
        padding = 10
        
        # 计算指标
        total_actions = self.ai_food_collected + self.ai_collision_count
        success_rate = (self.ai_food_collected / max(1, total_actions)) * 100
        q_table_size = len(self.ai_q_table)
        
        # 绘制柱状图
        bar_width = 80
        bar_spacing = 120
        start_x = padding + 50
        
        # 成功率柱
        success_height = int(success_rate / 100 * (height - 2*padding))
        canvas.create_rectangle(start_x, height-padding-success_height, 
                               start_x+bar_width, height-padding,
                               fill='#4caf50', outline='#2e7d32')
        canvas.create_text(start_x+bar_width//2, height-padding+5, 
                          text=f"成功率\n{success_rate:.1f}%", 
                          fill='#ffffff', font=('Arial', 8))
        
        # Q表大小柱
        max_q_size = 1000
        q_height = min(int(q_table_size / max_q_size * (height - 2*padding)), height - 2*padding)
        canvas.create_rectangle(start_x+bar_spacing, height-padding-q_height,
                               start_x+bar_spacing+bar_width, height-padding,
                               fill='#2196f3', outline='#1565c0')
        canvas.create_text(start_x+bar_spacing+bar_width//2, height-padding+5,
                          text=f"Q表\n{q_table_size}", 
                          fill='#ffffff', font=('Arial', 8))
        
        # 学习率柱
        learning_rate = self.ai_epsilon * 100
        lr_height = int(learning_rate / 100 * (height - 2*padding))
        canvas.create_rectangle(start_x+bar_spacing*2, height-padding-lr_height,
                               start_x+bar_spacing*2+bar_width, height-padding,
                               fill='#ff9800', outline='#f57c00')
        canvas.create_text(start_x+bar_spacing*2+bar_width//2, height-padding+5,
                          text=f"探索率\n{learning_rate:.0f}%", 
                          fill='#ffffff', font=('Arial', 8))
                          
    def draw_trade_analysis_chart(self):
        """绘制交易分析图"""
        canvas = self.chart_canvases['trade_analysis']
        canvas.delete("all")
        
        width = 500
        height = 150
        padding = 10
        
        if not self.trades:
            canvas.create_text(250, 75, text="暂无交易数据", fill='#666666', font=('Arial', 10))
            return
            
        # 统计交易类型
        trade_types = defaultdict(int)
        for trade in self.trades:
            trade_types[trade['type']] += 1
            
        if not trade_types:
            canvas.create_text(250, 75, text="暂无交易数据", fill='#666666', font=('Arial', 10))
            return
            
        # 绘制饼图
        colors = {
            'profit': '#4caf50',
            'loss': '#f44336',
            'breakout': '#2196f3',
            'reversal': '#ff9800'
        }
        
        total_trades = sum(trade_types.values())
        current_angle = 0
        
        center_x = width // 2
        center_y = height // 2
        radius = min(60, min(width, height) // 2 - 20)
        
        for trade_type, count in trade_types.items():
            percentage = count / total_trades
            angle = percentage * 360
            
            # 绘制扇形
            color = colors.get(trade_type, '#666666')
            canvas.create_arc(center_x - radius, center_y - radius,
                            center_x + radius, center_y + radius,
                            start=current_angle, extent=angle,
                            fill=color, outline='#ffffff', width=1)
            
            # 绘制标签
            label_angle = current_angle + angle / 2
            label_x = center_x + radius * 0.7 * math.cos(math.radians(label_angle))
            label_y = center_y - radius * 0.7 * math.sin(math.radians(label_angle))
            
            canvas.create_text(label_x, label_y, 
                              text=f"{trade_type}\n{percentage*100:.0f}%",
                              fill='#ffffff', font=('Arial', 8))
            
            current_angle += angle
            
    def ai_decision(self):
        """AI决策系统"""
        if not self.food or not self.snake:
            return
            
        # 获取当前状态
        head = self.snake[-1]
        food_pos = self.food
        
        # 简化的状态表示
        state = (head[0] - food_pos[0], head[1] - food_pos[1], self.direction)
        
        # 探索或利用
        if random.random() < self.ai_epsilon:
            # 探索：随机选择
            directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
            valid_directions = []
            
            for direction in directions:
                new_head = (head[0] + direction[0], head[1] + direction[1])
                
                # 检查边界穿越
                if 0 <= new_head[0] < self.grid_size and 0 <= new_head[1] < self.grid_size:
                    if new_head not in self.snake:
                        valid_directions.append(direction)
                else:
                    # 允许穿越边界
                    valid_directions.append(direction)
                    
            if valid_directions:
                self.direction = random.choice(valid_directions)
        else:
            # 利用：基于Q表选择
            if state not in self.ai_q_table:
                self.ai_q_table[state] = [0, 0, 0, 0]  # 上下左右的Q值
                
            # 选择最优动作
            q_values = self.ai_q_table[state]
            best_action = q_values.index(max(q_values))
            
            directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
            chosen_direction = directions[best_action]
            
            # 检查是否安全
            new_head = (head[0] + chosen_direction[0], head[1] + chosen_direction[1])
            
            if 0 <= new_head[0] < self.grid_size and 0 <= new_head[1] < self.grid_size:
                if new_head in self.snake:
                    # 选择随机方向避免碰撞
                    random.choice([(0, -1), (0, 1), (-1, 0), (1, 0)])
                else:
                    self.direction = chosen_direction
            else:
                # 允许穿越边界
                self.direction = chosen_direction
                
    def update_ai_q_table(self, reward, state, action):
        """更新Q表"""
        if state not in self.ai_q_table:
            self.ai_q_table[state] = [0, 0, 0, 0]
            
        # Q学习更新公式
        old_q = self.ai_q_table[state][action]
        next_max_q = max(self.ai_q_table.get(state, [0, 0, 0, 0]))
        new_q = old_q + self.ai_learning_rate * (reward + 0.9 * next_max_q - old_q)
        
        self.ai_q_table[state][action] = new_q
        
    def move_snake(self):
        """移动蛇"""
        if not self.game_running or self.game_paused:
            return
            
        # AI决策
        if self.ai_mode:
            self.ai_decision()
            
        # 计算新位置
        head = self.snake[-1]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        
        # 边界穿越逻辑
        if 0 <= new_head[0] < self.grid_size and 0 <= new_head[1] < self.grid_size:
            if new_head in self.snake:
                self.handle_collision()
                return
        else:
            # 穿墙处理
            self.handle_teleport(new_head)
            
        self.snake.append(new_head)
        
        # 检查是否吃到食物
        if new_head == self.food:
            self.handle_food_consumption()
        else:
            self.snake.popleft()
            
        # 更新食物生命周期
        if self.food:
            self.food_lifetime -= 1
            if self.food_lifetime <= 0:
                self.generate_food()
                self.add_message("⏰ 食物超时，重新生成", "info")
                
        # 绘制游戏
        self.draw_game()
        
        # 更新图表（优化频率）
        self.update_charts_optimized()
        
        # 性能监控（在主线程中安全调用）
        self.monitor_performance()
        
        # 继续移动
        self.root.after(self.game_speed, self.move_snake)
        
    def handle_teleport(self, new_head):
        """处理穿越逻辑"""
        self.teleport_count += 1
        
        # 计算穿越位置
        if new_head[0] < 0:
            new_head = (self.grid_size - 1, new_head[1])
        elif new_head[0] >= self.grid_size:
            new_head = (0, new_head[1])
        elif new_head[1] < 0:
            new_head = (new_head[0], self.grid_size - 1)
        elif new_head[1] >= self.grid_size:
            new_head = (new_head[0], 0)
            
        # 穿越惩罚
        self.capital -= 50
        self.add_message(f"🌀 穿墙 #{self.teleport_count}，资金 -${50}", "trade")
        
        # 调整速度
        if self.teleport_count % 3 == 0:
            self.game_speed = min(250, self.game_speed + 10)
            self.add_message(f"⚡ 速度调整至 {250-self.game_speed+10}ms", "system")
            
    def handle_collision(self):
        """处理碰撞"""
        self.ai_collision_count += 1
        
        # 碰撞惩罚
        self.capital -= 200
        
        # 记录交易
        trade = {
            'type': 'loss',
            'amount': -200,
            'timestamp': time.time()
        }
        self.trades.append(trade)
        
        self.add_message(f"💥 碰撞！资金 -${200}", "error")
        
        # 更新Q表
        head = self.snake[-1]
        state = (head[0] - self.food[0] if self.food else 0, 
                head[1] - self.food[1] if self.food else 0, 
                self.direction)
        
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        action = directions.index(self.direction) if self.direction in directions else 0
        
        self.update_ai_q_table(-10, state, action)
        
    def handle_food_consumption(self):
        """处理食物消费"""
        self.ai_food_collected += 1
        self.score += 1
        
        # 随机奖励
        rewards = [100, 150, 200, 250, 300]
        reward = random.choice(rewards)
        self.capital += reward
        
        # 记录交易
        trade_type = random.choice(['profit', 'breakout', 'reversal'])
        trade = {
            'type': trade_type,
            'amount': reward,
            'timestamp': time.time()
        }
        self.trades.append(trade)
        
        self.add_message(f"🎯 {trade_type.upper()} +${reward}", "trade")
        
        # 更新Q表
        head = self.snake[-1]
        state = (head[0] - self.food[0], head[1] - self.food[1], self.direction)
        
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        action = directions.index(self.direction) if self.direction in directions else 0
        
        self.update_ai_q_table(10, state, action)
        
        # 生成新食物
        self.generate_food()
        
        # 更新显示
        self.update_display()
        
    def update_display(self):
        """更新显示"""
        self.score_label.config(text=f"分数: {self.score}")
        self.capital_label.config(text=f"资金: ${self.capital:,}")
        
        # 更新状态
        if self.game_running:
            self.game_time += 1
            status_text = f"游戏时间: {self.game_time//60:02d}:{self.game_time%60:02d} | "
            status_text += f"蛇身长度: {len(self.snake)} | "
            status_text += f"Q表: {len(self.ai_q_table)} | "
            status_text += f"AI学习进行中"
            
            self.status_label.config(text=status_text)
            
        # 记录历史数据
        self.capital_history.append(self.capital)
        self.score_history.append(self.score)
        
        # 定期保存性能指标
        if self.game_time % 10 == 0:
            self.performance_metrics.append({
                'time': self.game_time,
                'fps': self.current_fps,
                'memory': len(self.ai_q_table)
            })
            
    def start_game(self):
        """开始游戏"""
        self.game_running = True
        self.game_paused = False
        self.start_button.config(state='disabled')
        self.pause_button.config(state='normal')
        
        if not self.food:
            self.generate_food()
            
        self.add_message("🎮 游戏开始！", "info")
        self.add_message("🤖 AI模式已启用", "ai")
        
        self.move_snake()
        
    def toggle_pause(self):
        """切换暂停状态"""
        self.game_paused = not self.game_paused
        
        if self.game_paused:
            self.pause_button.config(text="▶️ 继续")
            self.add_message("⏸️ 游戏暂停", "system")
        else:
            self.pause_button.config(text="⏸️ 暂停")
            self.add_message("▶️ 游戏继续", "system")
            self.move_snake()
            
    def reset_game(self):
        """重置游戏"""
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
        
        # 重置AI状态
        self.ai_collision_count = 0
        self.ai_food_collected = 0
        
        # 清空数据
        self.trades.clear()
        self.capital_history.clear()
        self.score_history.clear()
        self.performance_metrics.clear()
        
        # 重置按钮状态
        self.start_button.config(state='normal')
        self.pause_button.config(state='disabled', text="⏸️ 暂停")
        
        # 清空图表
        for canvas in self.chart_canvases.values():
            canvas.delete("all")
            
        # 清空消息
        self.message_text.config(state=tk.NORMAL)
        self.message_text.delete(1.0, tk.END)
        self.message_text.config(state=tk.DISABLED)
        
        # 重绘游戏
        self.draw_game()
        self.update_display()
        
        self.add_message("🔄 游戏已重置", "system")
        
    def quit_game(self):
        """退出游戏"""
        if self.game_running:
            if messagebox.askokcancel("退出", "确定要退出游戏吗？"):
                self.root.quit()
        else:
            self.root.quit()
            
def main():
    root = tk.Tk()
    game = PerformanceOptimizedTradingSnake(root)
    root.mainloop()

if __name__ == "__main__":
    main()