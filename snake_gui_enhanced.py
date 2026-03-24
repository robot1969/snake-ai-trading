#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
量化交易贪吃蛇游戏 - 增强视觉效果版本
Enhanced Visual Effects GUI Version
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
        self.base_speed = 150
        self.score = 0
        self.capital = 10000
        self.trades = []
        self.teleport_count = 0
        self.food_lifetime = 0
        self.animation_effects = []
        
        # 随机运动参数
        self.random_mode = False
        self.speed_change_timer = 0
        self.direction_change_timer = 0
        self.min_speed = 30
        self.max_speed = 500
        self.speed_change_interval = 100  # 每100帧可能改变速度
        self.direction_change_interval = 50  # 每50帧可能改变方向
        
        # 穿墙增强参数
        self.teleport_effect_duration = 0
        self.teleport_speed_boost = 1.5
        self.teleport_direction_change = True
        self.rhythm_pattern = []
        self.rhythm_index = 0
        self.auto_rhythm_enabled = False
        
        # 手动控制和学习参数
        self.manual_actions = []  # 记录手动操作
        self.human_q_table = {}  # 人类专家Q表
        self.learning_from_human = False
        self.manual_session_count = 0
        self.manual_food_collected = 0
        self.manual_collisions = 0
        self.expert_demo_mode = False
        self.manual_override = False  # 手动干预标志
        self.override_duration = 0  # 干预持续时间
        self.auto_mode_original = None  # 原始自动模式
        self.manual_override_count = 0  # 干预次数统计
        
        # AI学习参数
        # 初始化时激活所有模式
        self.ai_mode = True
        self.random_mode = True
        self.auto_rhythm_enabled = True
        self.learning_from_human = True
        
        self.ai_q_table = {}  # Q-learning table
        self.ai_learning_rate = 0.1
        self.ai_discount_factor = 0.9
        self.ai_epsilon = 0.1  # 探索率
        self.ai_last_state = None
        self.ai_last_action = None
        self.ai_food_history = []  # 食物位置历史
        self.ai_collision_count = 0
        self.ai_food_collected = 0
        
        # 数据分析参数
        self.performance_history = []  # 性能历史记录
        self.capital_history = []  # 资金历史
        self.score_history = []  # 分数历史
        self.game_time = 0  # 游戏时间
        self.chart_update_interval = 10  # 图表更新间隔
        
        # 交易类型
        self.trade_types = [
            {"name": "盈利交易", "color": "#4caf50", "profit": 1500, "symbol": "🟢"},
            {"name": "亏损交易", "color": "#f44336", "loss": 1200, "symbol": "🔴"},
            {"name": "突破交易", "color": "#2196f3", "profit": 2000, "symbol": "🔵"},
            {"name": "反转交易", "color": "#ff9800", "profit": 1800, "symbol": "🟠"}
        ]
        
        self.setup_gui()
        self.bind_keys()
        self.center_window()
        self.generate_food()
        self.update_stats()
        
        # 运行即启动所有自动模式
        self.auto_start_all_modes()
        
    def center_window(self):
        self.root.update_idletasks()
        try:
            # 最大化窗口显示更多功能
            self.root.geometry("1200x700+50+50")
            # 设置最小窗口大小
            self.root.minsize(1100, 650)
            # 最大化窗口
            self.root.state('zoomed')  # Windows最大化
        except:
            pass
        
    def setup_gui(self):
        # 主框架
        main_frame = tk.Frame(self.root, bg='#1a1a2e')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 主容器 - 使用网格布局
        main_container = tk.Frame(main_frame, bg='#1a1a2e')
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # 左侧游戏区域
        game_frame = tk.Frame(main_container, bg='#1a1a2e')
        game_frame.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
        
        # 游戏画布 - 增大尺寸
        canvas_size = 550
        self.canvas = tk.Canvas(
            game_frame, 
            width=canvas_size, 
            height=canvas_size,
            bg='#0f0f1e',
            highlightthickness=3,
            highlightbackground='#4a4a6e'
        )
        self.canvas.pack()
        
        # 调整网格大小
        self.cell_size = canvas_size // self.grid_size
        
        # 创建网格背景
        self.create_grid_background()
        
        # 右侧面板容器
        right_container = tk.Frame(main_container, bg='#1a1a2e')
        right_container.grid(row=0, column=1, sticky='nsew', padx=10, pady=10)
        
        # 配置网格权重
        main_container.grid_columnconfigure(0, weight=2)
        main_container.grid_columnconfigure(1, weight=3)
        main_container.grid_rowconfigure(0, weight=1)
        

        
        # 右侧面板 - 使用网格布局
        right_grid = tk.Frame(right_container, bg='#1a1a2e')
        right_grid.pack(fill=tk.BOTH, expand=True)
        
        # 顶部行 - 控制和信息
        top_row = tk.Frame(right_grid, bg='#1a1a2e')
        top_row.grid(row=0, column=0, sticky='ew', pady=(0, 10))
        
        # 游戏信息面板
        info_panel = tk.Frame(top_row, bg='#2d2d44', relief=tk.RAISED, bd=2)
        info_panel.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        tk.Label(
            info_panel,
            text="🎮 游戏状态",
            font=('Arial', 11, 'bold'),
            bg='#2d2d44',
            fg='#ffffff'
        ).pack(pady=5)
        
        self.game_info_text = tk.Text(
            info_panel,
            height=3,
            width=40,
            bg='#1a1a2e',
            fg='#ffffff',
            font=('Consolas', 8),
            relief=tk.FLAT
        )
        self.game_info_text.pack(padx=5, pady=5)
        
        # 控制面板
        control_panel = tk.Frame(top_row, bg='#2d2d44', relief=tk.RAISED, bd=2)
        control_panel.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        
        tk.Label(
            control_panel,
            text="🎮 基础控制",
            font=('Arial', 11, 'bold'),
            bg='#2d2d44',
            fg='#ffffff'
        ).pack(pady=5)
        
        self.create_control_buttons(control_panel)
        
        # 中间行 - 统计和图表
        middle_row = tk.Frame(right_grid, bg='#1a1a2e')
        middle_row.grid(row=1, column=0, sticky='ew', pady=(0, 10))
        
        # 统计面板
        self.create_stats_panel(middle_row, 'left')
        
        # 图表面板
        self.create_chart_panel(middle_row, 'right')
        
        # 底部行 - 设置和智能模式
        bottom_row = tk.Frame(right_grid, bg='#1a1a2e')
        bottom_row.grid(row=2, column=0, sticky='ew')
        
        # 设置面板
        # self.create_settings_panel(bottom_row, 'left')  # 暂时注释掉
        
        # 智能模式面板
        self.create_learning_panel(bottom_row, 'right')
        
        # 配置网格权重
        right_grid.grid_rowconfigure(0, weight=1)
        right_grid.grid_rowconfigure(1, weight=2)
        right_grid.grid_rowconfigure(2, weight=2)
        right_grid.grid_rowconfigure(3, weight=1)
        right_grid.grid_columnconfigure(0, weight=1)
        
        # 数据分析面板
        analysis_frame = tk.Frame(right_grid, bg='#3d3d5c', relief=tk.SUNKEN, bd=2)
        analysis_frame.grid(row=3, column=0, sticky='ew', pady=(10, 0))
        
        tk.Label(
            analysis_frame,
            text="📊 实时数据分析",
            font=('Arial', 11, 'bold'),
            bg='#3d3d5c',
            fg='#ffffff'
        ).pack(pady=5)
        
        # 创建分析图表
        self.analysis_canvas = tk.Canvas(
            analysis_frame,
            width=550,
            height=100,
            bg='#2d2d44',
            highlightthickness=1,
            highlightbackground='#4a4a6e'
        )
        self.analysis_canvas.pack(padx=10, pady=5)
        
        # 消息记录
        self.message_log = []
        self.max_messages = 50
        
    def add_message(self, message, color='#00ff00'):
        """添加消息到日志"""
        timestamp = time.strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}"
        
        self.message_log.append({
            'text': formatted_message,
            'color': color,
            'time': time.time()
        })
        
        # 限制消息数量
        if len(self.message_log) > self.max_messages:
            self.message_log.pop(0)
        
        # 更新显示
        if hasattr(self, 'message_text'):
            self.message_text.delete(1.0, tk.END)
            for msg in self.message_log[-20:]:  # 显示最近20条
                self.message_text.insert(tk.END, msg['text'] + '\n')
            
            # 滚动到底部
            self.message_text.see(tk.END)
            
    def update_secondary_chart(self):
        """更新辅助图表 - 模式活跃度"""
        if not hasattr(self, 'secondary_chart_canvas'):
            return
            
        self.secondary_chart_canvas.delete("all")
        
        width = 280
        height = 100
        margin = 10
        
        # 绘制标题
        self.secondary_chart_canvas.create_text(
            width//2, 10,
            text="模式活跃度分析",
            font=('Arial', 9, 'bold'),
            fill='#ffffff'
        )
        
        # 绘制柱状图
        modes = [
            ('AI', self.ai_mode, '#00bcd4'),
            ('随机', self.random_mode, '#9c27b0'),
            ('节奏', self.auto_rhythm_enabled, '#e91e63'),
            ('学习', self.learning_from_human, '#673ab7')
        ]
        
        bar_width = (width - 2*margin) // len(modes) - 10
        bar_height = height - 40
        
        for i, (name, active, color) in enumerate(modes):
            x = margin + i * (bar_width + 10) + 5
            y = height - 20
            
            # 柱子高度
            h = bar_height if active else bar_height * 0.3
            
            # 绘制柱子
            self.secondary_chart_canvas.create_rectangle(
                x, y - h, x + bar_width, y,
                fill=color if active else '#666666',
                outline='#ffffff'
            )
            
            # 绘制标签
            self.secondary_chart_canvas.create_text(
                x + bar_width//2, y + 5,
                text=name,
                font=('Arial', 7),
                fill='#ffffff'
            )
            
    def update_analysis_chart(self):
        """更新数据分析图表"""
        if not hasattr(self, 'analysis_canvas'):
            return
            
        self.analysis_canvas.delete("all")
        
        width = 550
        height = 100
        margin = 15
        
        # 绘制标题
        self.analysis_canvas.create_text(
            width//2, 10,
            text="实时性能分析 - Q表大小 | 学习效率 | 决策准确率",
            font=('Arial', 9, 'bold'),
            fill='#ffffff'
        )
        
        # 计算数据
        q_table_size = len(self.ai_q_table) + len(self.human_q_table)
        learning_efficiency = 0
        if self.ai_collision_count > 0:
            learning_efficiency = (self.ai_food_collected / max(1, self.ai_collision_count)) * 100
        decision_accuracy = min(100, (self.game_time / max(1, len(self.trades))) * 10)
        
        # 绘制进度条
        metrics = [
            ('Q表', q_table_size, 1000, '#4caf50'),
            ('学习率', learning_efficiency, 100, '#ff9800'),
            ('准确率', decision_accuracy, 100, '#2196f3')
        ]
        
        bar_width = (width - 2*margin) // len(metrics) - 15
        bar_height = height - 35
        
        for i, (name, value, max_val, color) in enumerate(metrics):
            x = margin + i * (bar_width + 15)
            y = height - 20
            
            # 计算百分比
            percentage = min(100, (value / max_val) * 100)
            bar_actual_height = int(bar_height * percentage / 100)
            
            # 绘制背景
            self.analysis_canvas.create_rectangle(
                x, y - bar_height, x + bar_width, y,
                fill='#333333',
                outline='#666666'
            )
            
            # 绘制进度
            self.analysis_canvas.create_rectangle(
                x, y - bar_actual_height, x + bar_width, y,
                fill=color,
                outline='#ffffff'
            )
            
            # 绘制数值
            self.analysis_canvas.create_text(
                x + bar_width//2, y + 5,
                text=f"{value:.0f}",
                font=('Arial', 8, 'bold'),
                fill='#ffffff'
            )
            
    def add_periodic_message(self):
        """添加定期消息"""
        messages = [
            f"🧠 Q表持续学习中... 当前大小: {len(self.ai_q_table)}",
            f"📊 游戏时间: {self.game_time//60}分{self.game_time%60}秒",
            f"🎯 食物收集进度: {self.ai_food_collected}/{len(self.trades)}",
            f"⚡ 当前速度: {self.game_speed}ms | FPS: {1000//max(self.game_speed,1)}",
            f"🎵 节奏模式活跃度: {'高' if self.auto_rhythm_enabled else '低'}",
            f"🎲 随机影响因子: {'活跃' if self.random_mode else '休眠'}",
            f"💰 资金状态: {self.capital:,} | 资金变化: {'+' if self.capital > 10000 else '-'}",
            f"🐍 蛇身长度: {len(self.snake)} | 移动效率: {self.game_time//max(1,len(self.trades))}",
            f"🔄 传送次数: {self.teleport_count} | 碰撞避免率: {max(0,100-self.ai_collision_count*5):.0f}%"
        ]
        
        # 随机选择一条消息
        message = random.choice(messages)
        color = '#00ff00' if '📊' in message or '🎯' in message else '#ffff00' if '⚡' in message else '#00ffff'
        
        self.add_message(message, color)
        
    def create_control_buttons(self, parent):
        """创建控制按钮"""
        # 分数和资本显示
        score_frame = tk.Frame(parent, bg='#2d2d44')
        score_frame.pack(pady=5)
        
        self.score_label = tk.Label(
            score_frame, 
            text=f"分数: {self.score}", 
            font=('Arial', 10, 'bold'),
            bg='#2d2d44', 
            fg='#ffd700'
        )
        self.score_label.pack(side=tk.LEFT, padx=5)
        
        self.capital_label = tk.Label(
            score_frame, 
            text=f"资金: ${self.capital:,}", 
            font=('Arial', 10, 'bold'),
            bg='#2d2d44', 
            fg='#4caf50'
        )
        self.capital_label.pack(side=tk.LEFT, padx=5)
        
        # 控制按钮
        button_frame = tk.Frame(parent, bg='#2d2d44')
        button_frame.pack(pady=5)
        
        self.start_button = tk.Button(
            button_frame,
            text="🎮",
            command=self.start_game,
            font=('Arial', 12, 'bold'),
            bg='#4caf50',
            fg='white',
            width=3,
            height=1,
            relief=tk.RAISED,
            bd=2,
            cursor='hand2'
        )
        self.start_button.pack(side=tk.LEFT, padx=2)
        
        self.pause_button = tk.Button(
            button_frame,
            text="⏸️",
            command=self.toggle_pause,
            font=('Arial', 12, 'bold'),
            bg='#ff9800',
            fg='white',
            width=3,
            height=1,
            relief=tk.RAISED,
            bd=2,
            cursor='hand2',
            state='disabled'
        )
        self.pause_button.pack(side=tk.LEFT, padx=2)
        
        self.reset_button = tk.Button(
            button_frame,
            text="🔄",
            command=self.reset_game,
            font=('Arial', 12, 'bold'),
            bg='#f44336',
            fg='white',
            width=3,
            height=1,
            relief=tk.RAISED,
            bd=2,
            cursor='hand2'
        )
        self.reset_button.pack(side=tk.LEFT, padx=2)
        
        options_button = tk.Button(
            button_frame,
            text="⚙️",
            command=self.show_options_menu,
            font=('Arial', 12, 'bold'),
            bg='#607d8b',
            fg='white',
            width=3,
            height=1,
            relief=tk.RAISED,
            bd=2,
            cursor='hand2'
        )
        options_button.pack(side=tk.LEFT, padx=2)
        
    def create_stats_panel(self, parent, position='left'):
        """创建统计信息面板"""
        stats_frame = tk.Frame(parent, bg='#3d3d5c', relief=tk.SUNKEN, bd=2)
        if position == 'left':
            stats_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        else:
            stats_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        tk.Label(
            stats_frame, 
            text="📊 交易统计", 
            font=('Arial', 11, 'bold'),
            bg='#3d3d5c', 
            fg='#ffffff'
        ).pack(pady=5)
        
        self.stats_text = tk.Text(
            stats_frame, 
            height=5, 
            width=25,
            bg='#2d2d44',
            fg='#ffffff',
            font=('Consolas', 8),
            relief=tk.FLAT
        )
        self.stats_text.pack(padx=5, pady=5)
        
        return stats_frame
        
    def create_chart_panel(self, parent, position='right'):
        """创建图表面板"""
        chart_frame = tk.Frame(parent, bg='#3d3d5c', relief=tk.SUNKEN, bd=2)
        if position == 'left':
            chart_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        else:
            chart_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        tk.Label(
            chart_frame, 
            text="📈 性能图表", 
            font=('Arial', 11, 'bold'),
            bg='#3d3d5c', 
            fg='#ffffff'
        ).pack(pady=5)
        
        # 创建主图表画布
        self.chart_canvas = tk.Canvas(
            chart_frame,
            width=280,
            height=140,
            bg='#2d2d44',
            highlightthickness=1,
            highlightbackground='#4a4a6e'
        )
        self.chart_canvas.pack(padx=5, pady=5)
        
        # 创建辅助图表画布
        self.secondary_chart_canvas = tk.Canvas(
            chart_frame,
            width=280,
            height=100,
            bg='#2d2d44',
            highlightthickness=1,
            highlightbackground='#4a4a6e'
        )
        self.secondary_chart_canvas.pack(padx=5, pady=5)
        
        # 刷新图表按钮
        refresh_button = tk.Button(
            chart_frame,
            text="🔄",
            command=self.update_charts,
            font=('Arial', 10),
            bg='#607d8b',
            fg='white',
            width=3,
            cursor='hand2'
        )
        refresh_button.pack(pady=3)
        
        return chart_frame
        
    def create_learning_panel(self, parent, position='right'):
        """创建学习模式面板"""
        learning_frame = tk.Frame(parent, bg='#3d3d5c', relief=tk.SUNKEN, bd=2)
        if position == 'left':
            learning_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        else:
            learning_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        tk.Label(
            learning_frame, 
            text="🧠 智能模式", 
            font=('Arial', 11, 'bold'),
            bg='#3d3d5c', 
            fg='#ffffff'
        ).pack(pady=5)
        
        # 模式按钮容器
        mode_button_frame = tk.Frame(learning_frame, bg='#3d3d5c')
        mode_button_frame.pack(pady=10)
        
        self.random_button = tk.Button(
            mode_button_frame,
            text="🎲 随机模式",
            command=self.toggle_random_mode,
            font=('Arial', 10, 'bold'),
            bg='#9c27b0',
            fg='white',
            width=14,
            height=1,
            relief=tk.RAISED,
            bd=2,
            cursor='hand2'
        )
        self.random_button.pack(pady=2)
        
        self.ai_button = tk.Button(
            mode_button_frame,
            text="🤖 AI学习",
            command=self.toggle_ai_mode,
            font=('Arial', 10, 'bold'),
            bg='#00bcd4',
            fg='white',
            width=14,
            height=1,
            relief=tk.RAISED,
            bd=2,
            cursor='hand2'
        )
        self.ai_button.pack(pady=2)
        
        self.rhythm_button = tk.Button(
            mode_button_frame,
            text="🎵 节奏模式",
            command=self.toggle_rhythm_mode,
            font=('Arial', 10, 'bold'),
            bg='#e91e63',
            fg='white',
            width=14,
            height=1,
            relief=tk.RAISED,
            bd=2,
            cursor='hand2'
        )
        self.rhythm_button.pack(pady=2)
        
        self.learning_button = tk.Button(
            mode_button_frame,
            text="🧠 学习模式",
            command=self.toggle_learning_mode,
            font=('Arial', 10, 'bold'),
            bg='#673ab7',
            fg='white',
            width=14,
            height=1,
            relief=tk.RAISED,
            bd=2,
            cursor='hand2'
        )
        self.learning_button.pack(pady=2)
        
        # 状态显示
        status_frame = tk.Frame(learning_frame, bg='#2d2d44', relief=tk.SUNKEN, bd=1)
        status_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # 实时消息文本框
        self.message_text = tk.Text(
            status_frame,
            height=4,
            width=32,
            bg='#1a1a2e',
            fg='#00ff00',
            font=('Consolas', 8),
            relief=tk.FLAT
        )
        self.message_text.pack(padx=5, pady=5)
        
        # 消息滚动条
        scrollbar = tk.Scrollbar(
            self.message_text,
            command=self.message_text.yview
        )
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.message_text.config(yscrollcommand=scrollbar.set)
        
        return learning_frame
        
    def auto_start_all_modes(self):
        """自动启动所有模式"""
        try:
            # 启动游戏
            self.game_running = True
            self.game_paused = False
            
            # 更新按钮状态
            if hasattr(self, 'start_button'):
                self.start_button.config(state='disabled')
            if hasattr(self, 'pause_button'):
                self.pause_button.config(state='normal')
            
            # 更新模式按钮状态
            if hasattr(self, 'ai_button'):
                self.ai_button.config(text="🤖 AI运行中", bg='#4caf50')
            if hasattr(self, 'random_button'):
                self.random_button.config(text="🎲 随机运行中", bg='#4caf50')
            if hasattr(self, 'rhythm_button'):
                self.rhythm_button.config(text="🎵 节奏运行中", bg='#4caf50')
            if hasattr(self, 'learning_button'):
                self.learning_button.config(text="🧠 学习运行中", bg='#4caf50')
            
            # 更新状态显示
            if hasattr(self, 'status_label'):
                self.status_label.config(
                    text="🚀 全自动模式启动！AI+随机+节奏+学习 全部运行", 
                    fg='#00ff00'
                )
            
            # 添加启动消息
            if hasattr(self, 'message_text'):
                self.add_message("🚀 全自动模式启动！AI+随机+节奏+学习 全部运行", '#00ff00')
            
            # 自动开始游戏循环
            self.game_loop()
            
        except Exception as e:
            print(f"自动启动错误: {e}")
            if hasattr(self, 'message_text'):
                self.add_message(f"启动失败: {e}", '#ff0000')
        


        

        

        

        
        # AI设置
        ai_settings_frame = tk.Frame(settings_frame, bg='#2d2d44', relief=tk.SUNKEN, bd=1)
        ai_settings_frame.pack(fill=tk.X, padx=10, pady=3)
        
        tk.Label(
            ai_settings_frame,
            text="🤖 AI设置",
            font=('Arial', 10, 'bold'),
            bg='#2d2d44',
            fg='#ffffff'
        ).pack(pady=3)
        
        # 学习率调节
        learning_control = tk.Frame(ai_settings_frame, bg='#2d2d44')
        learning_control.pack(fill=tk.X, padx=5, pady=2)
        
        tk.Label(
            learning_control,
            text="学习率:",
            font=('Arial', 8),
            bg='#2d2d44',
            fg='#ffffff',
            width=6
        ).pack(side=tk.LEFT)
        
        self.learning_scale = tk.Scale(
            learning_control,
            from_=0.01, to=0.5,
            resolution=0.01,
            orient=tk.HORIZONTAL,
            command=self.update_learning_rate,
            bg='#2d2d44',
            fg='#ffffff',
            highlightthickness=0,
            showvalue=False,
            length=120
        )
        self.learning_scale.set(self.ai_learning_rate)
        self.learning_scale.pack(side=tk.LEFT, padx=5)
        
        self.learning_label = tk.Label(
            learning_control,
            text=f"{self.ai_learning_rate:.2f}",
            font=('Arial', 8, 'bold'),
            bg='#2d2d44',
            fg='#00bcd4',
            width=6
        )
        self.learning_label.pack(side=tk.LEFT)
        
        # 探索率调节
        epsilon_control = tk.Frame(ai_settings_frame, bg='#2d2d44')
        epsilon_control.pack(fill=tk.X, padx=5, pady=2)
        
        tk.Label(
            epsilon_control,
            text="探索率:",
            font=('Arial', 8),
            bg='#2d2d44',
            fg='#ffffff',
            width=6
        ).pack(side=tk.LEFT)
        
        self.epsilon_scale = tk.Scale(
            epsilon_control,
            from_=0.01, to=0.5,
            resolution=0.01,
            orient=tk.HORIZONTAL,
            command=self.update_epsilon_rate,
            bg='#2d2d44',
            fg='#ffffff',
            highlightthickness=0,
            showvalue=False,
            length=120
        )
        self.epsilon_scale.set(self.ai_epsilon)
        self.epsilon_scale.pack(side=tk.LEFT, padx=5)
        
        self.epsilon_label = tk.Label(
            epsilon_control,
            text=f"{self.ai_epsilon:.2f}",
            font=('Arial', 8, 'bold'),
            bg='#2d2d44',
            fg='#00bcd4',
            width=6
        )
        self.epsilon_label.pack(side=tk.LEFT)
        
        # 视觉设置
        visual_settings_frame = tk.Frame(settings_frame, bg='#2d2d44', relief=tk.SUNKEN, bd=1)
        visual_settings_frame.pack(fill=tk.X, padx=10, pady=3)
        
        tk.Label(
            visual_settings_frame,
            text="🎨 视觉设置",
            font=('Arial', 10, 'bold'),
            bg='#2d2d44',
            fg='#ffffff'
        ).pack(pady=3)
        
        # 动画开关
        animation_control = tk.Frame(visual_settings_frame, bg='#2d2d44')
        animation_control.pack(fill=tk.X, padx=5, pady=2)
        
        self.animation_var = tk.BooleanVar(value=True)
        animation_check = tk.Checkbutton(
            animation_control,
            text="动画效果",
            variable=self.animation_var,
            font=('Arial', 8),
            bg='#2d2d44',
            fg='#ffffff',
            selectcolor='#2d2d44',
            command=self.update_animation_setting
        )
        animation_check.pack(side=tk.LEFT, padx=10)
        
        self.grid_var_visual = tk.BooleanVar(value=True)
        grid_check = tk.Checkbutton(
            animation_control,
            text="网格线",
            variable=self.grid_var_visual,
            font=('Arial', 8),
            bg='#2d2d44',
            fg='#ffffff',
            selectcolor='#2d2d44',
            command=self.update_grid_setting
        )
        grid_check.pack(side=tk.LEFT, padx=10)
        
        # 特效开关
        effects_control = tk.Frame(visual_settings_frame, bg='#2d2d44')
        effects_control.pack(fill=tk.X, padx=5, pady=2)
        
        self.teleport_var = tk.BooleanVar(value=True)
        teleport_check = tk.Checkbutton(
            effects_control,
            text="传送特效",
            variable=self.teleport_var,
            font=('Arial', 8),
            bg='#2d2d44',
            fg='#ffffff',
            selectcolor='#2d2d44',
            command=self.update_teleport_setting
        )
        teleport_check.pack(side=tk.LEFT, padx=10)
        
        self.particle_var = tk.BooleanVar(value=True)
        particle_check = tk.Checkbutton(
            effects_control,
            text="粒子效果",
            variable=self.particle_var,
            font=('Arial', 8),
            bg='#2d2d44',
            fg='#ffffff',
            selectcolor='#2d2d44',
            command=self.update_particle_setting
        )
        particle_check.pack(side=tk.LEFT, padx=10)
        
        return settings_frame
        
    def update_game_speed(self, value):
        """更新游戏速度"""
        try:
            self.base_speed = int(value)
            self.game_speed = self.base_speed
            if hasattr(self, 'speed_label'):
                self.speed_label.config(text=f"{self.base_speed}ms")
        except Exception as e:
            print(f"更新游戏速度错误: {e}")
        
    def update_grid_size(self, value):
        """更新网格大小"""
        try:
            new_size = int(value)
            if new_size != self.grid_size:
                self.grid_size = new_size
                self.cell_size = 550 // self.grid_size  # 修正为550
                if hasattr(self, 'grid_label'):
                    self.grid_label.config(text=f"{self.grid_size}x{self.grid_size}")
                # 重新生成食物位置
                self.generate_food()
                # 重绘网格
                self.create_grid_background()
        except Exception as e:
            print(f"更新网格大小错误: {e}")
            
    def update_learning_rate(self, value):
        """更新学习率"""
        try:
            self.ai_learning_rate = float(value)
            if hasattr(self, 'learning_label'):
                self.learning_label.config(text=f"{self.ai_learning_rate:.2f}")
        except Exception as e:
            print(f"更新学习率错误: {e}")
        
    def update_epsilon_rate(self, value):
        """更新探索率"""
        try:
            self.ai_epsilon = float(value)
            if hasattr(self, 'epsilon_label'):
                self.epsilon_label.config(text=f"{self.ai_epsilon:.2f}")
        except Exception as e:
            print(f"更新探索率错误: {e}")
        
    def update_animation_setting(self):
        """更新动画设置"""
        try:
            animation_enabled = self.animation_var.get()
            # 这里可以添加动画开关逻辑
        except Exception as e:
            print(f"更新动画设置错误: {e}")
        
    def update_grid_setting(self):
        """更新网格设置"""
        try:
            grid_enabled = self.grid_var_visual.get()
            # 这里可以添加网格显示/隐藏逻辑
            if not grid_enabled:
                self.canvas.delete("grid")
            else:
                self.create_grid_background()
        except Exception as e:
            print(f"更新网格设置错误: {e}")
            
    def update_teleport_setting(self):
        """更新传送特效设置"""
        try:
            # 这里可以添加传送特效开关逻辑
            pass
        except Exception as e:
            print(f"更新传送设置错误: {e}")
        
    def update_particle_setting(self):
        """更新粒子效果设置"""
        try:
            # 这里可以添加粒子效果开关逻辑
            pass
        except Exception as e:
            print(f"更新粒子设置错误: {e}")
        
    def create_advanced_panel(self, parent):
        """创建高级功能面板"""
        advanced_frame = tk.Frame(parent, bg='#3d3d5c', relief=tk.SUNKEN, bd=2)
        advanced_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(
            advanced_frame,
            text="🔧 高级功能",
            font=('Arial', 12, 'bold'),
            bg='#3d3d5c',
            fg='#ffffff'
        ).pack(pady=8)
        
        # 性能监控
        perf_frame = tk.Frame(advanced_frame, bg='#2d2d44', relief=tk.SUNKEN, bd=1)
        perf_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(
            perf_frame,
            text="⚡ 性能监控",
            font=('Arial', 10, 'bold'),
            bg='#2d2d44',
            fg='#ffffff'
        ).pack(pady=3)
        
        self.perf_text = tk.Text(
            perf_frame,
            height=3,
            width=28,
            bg='#1a1a2e',
            fg='#81c784',
            font=('Consolas', 8),
            relief=tk.FLAT
        )
        self.perf_text.pack(padx=5, pady=5)
        
        # 学习进度
        learning_frame = tk.Frame(advanced_frame, bg='#2d2d44', relief=tk.SUNKEN, bd=1)
        learning_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(
            learning_frame,
            text="🎓 学习进度",
            font=('Arial', 10, 'bold'),
            bg='#2d2d44',
            fg='#ffffff'
        ).pack(pady=3)
        
        self.learning_text = tk.Text(
            learning_frame,
            height=3,
            width=28,
            bg='#1a1a2e',
            fg='#ff9800',
            font=('Consolas', 8),
            relief=tk.FLAT
        )
        self.learning_text.pack(padx=5, pady=5)
        
        return advanced_frame
        
        # 标题
        title_label = tk.Label(
            control_frame, 
            text="🎮 游戏控制", 
            font=('Arial', 16, 'bold'),
            bg='#2d2d44', 
            fg='#ffffff'
        )
        title_label.pack(pady=20)
        
        # 分数和资本显示
        self.score_label = tk.Label(
            control_frame, 
            text=f"分数: {self.score}", 
            font=('Arial', 14, 'bold'),
            bg='#2d2d44', 
            fg='#ffd700'
        )
        self.score_label.pack(pady=10)
        
        self.capital_label = tk.Label(
            control_frame, 
            text=f"资金: ${self.capital:,}", 
            font=('Arial', 14, 'bold'),
            bg='#2d2d44', 
            fg='#4caf50'
        )
        self.capital_label.pack(pady=10)
        
        # 控制按钮
        button_frame = tk.Frame(control_frame, bg='#2d2d44')
        button_frame.pack(pady=20)
        
        self.start_button = tk.Button(
            button_frame,
            text="🎮 开始游戏",
            command=self.start_game,
            font=('Arial', 12, 'bold'),
            bg='#4caf50',
            fg='white',
            width=15,
            height=2,
            relief=tk.RAISED,
            bd=3,
            cursor='hand2'
        )
        self.start_button.pack(pady=5)
        
        self.pause_button = tk.Button(
            button_frame,
            text="⏸️ 暂停",
            command=self.toggle_pause,
            font=('Arial', 12, 'bold'),
            bg='#ff9800',
            fg='white',
            width=15,
            height=2,
            relief=tk.RAISED,
            bd=3,
            cursor='hand2',
            state='disabled'
        )
        self.pause_button.pack(pady=5)
        
        self.reset_button = tk.Button(
            button_frame,
            text="🔄 重置游戏",
            command=self.reset_game,
            font=('Arial', 12, 'bold'),
            bg='#f44336',
            fg='white',
            width=15,
            height=2,
            relief=tk.RAISED,
            bd=3,
            cursor='hand2'
        )
        self.reset_button.pack(pady=5)
        
        # 随机模式按钮
        self.random_button = tk.Button(
            button_frame,
            text="🎲 随机模式",
            command=self.toggle_random_mode,
            font=('Arial', 12, 'bold'),
            bg='#9c27b0',
            fg='white',
            width=15,
            height=2,
            relief=tk.RAISED,
            bd=3,
            cursor='hand2'
        )
        self.random_button.pack(pady=5)
        
        # AI学习模式按钮
        self.ai_button = tk.Button(
            button_frame,
            text="🤖 AI学习",
            command=self.toggle_ai_mode,
            font=('Arial', 12, 'bold'),
            bg='#00bcd4',
            fg='white',
            width=15,
            height=2,
            relief=tk.RAISED,
            bd=3,
            cursor='hand2'
        )
        self.ai_button.pack(pady=5)
        
        # 节奏模式按钮
        self.rhythm_button = tk.Button(
            button_frame,
            text="🎵 节奏模式",
            command=self.toggle_rhythm_mode,
            font=('Arial', 12, 'bold'),
            bg='#e91e63',
            fg='white',
            width=15,
            height=2,
            relief=tk.RAISED,
            bd=3,
            cursor='hand2'
        )
        self.rhythm_button.pack(pady=5)
        
        # 学习模式按钮
        self.learning_button = tk.Button(
            button_frame,
            text="🧠 学习模式",
            command=self.toggle_learning_mode,
            font=('Arial', 12, 'bold'),
            bg='#673ab7',
            fg='white',
            width=15,
            height=2,
            relief=tk.RAISED,
            bd=3,
            cursor='hand2'
        )
        self.learning_button.pack(pady=5)
        

        
    def create_grid_background(self):
        """创建网格背景"""
        for i in range(0, self.canvas_width, self.cell_size):
            self.canvas.create_line(
                i, 0, i, self.canvas_height, 
                fill='#1a1a2e', width=1
            )
        for i in range(0, self.canvas_height, self.cell_size):
            self.canvas.create_line(
                0, i, self.canvas_width, i, 
                fill='#1a1a2e', width=1
            )
            
    def bind_keys(self):
        """绑定键盘事件"""
        self.root.bind('<Up>', lambda e: self.change_direction(0, -1))
        self.root.bind('<Down>', lambda e: self.change_direction(0, 1))
        self.root.bind('<Left>', lambda e: self.change_direction(-1, 0))
        self.root.bind('<Right>', lambda e: self.change_direction(1, 0))
        self.root.bind('<w>', lambda e: self.change_direction(0, -1))
        self.root.bind('<s>', lambda e: self.change_direction(0, 1))
        self.root.bind('<a>', lambda e: self.change_direction(-1, 0))
        self.root.bind('<d>', lambda e: self.change_direction(1, 0))
        self.root.bind('<space>', lambda e: self.toggle_pause())
        self.root.bind('<Escape>', lambda e: self.quit_game())
        
    def change_direction(self, x, y):
        """改变方向 - 禁用手动控制"""
        # 完全禁用手动控制，只允许自动模式运行
        return
                
    def activate_manual_override(self, new_direction):
        """激活手动干预"""
        # 如果已经在干预中，延长持续时间
        if self.manual_override:
            self.override_duration = 30  # 重置持续时间为30帧
        else:
            # 开始新的干预
            self.manual_override = True
            self.override_duration = 30  # 持续30帧
            self.manual_override_count += 1
            
            # 记录原始模式
            if self.random_mode:
                self.auto_mode_original = "random"
            elif self.ai_mode:
                self.auto_mode_original = "ai"
            elif self.auto_rhythm_enabled:
                self.auto_mode_original = "rhythm"
            else:
                self.auto_mode_original = None
                
            # 临时禁用自动模式
            self.random_mode = False
            self.ai_mode = False
            self.auto_rhythm_enabled = False
            
            # 更新按钮状态
            self.random_button.config(text="🎲 随机模式", bg='#9c27b0')
            self.ai_button.config(text="🤖 AI学习", bg='#00bcd4')
            self.rhythm_button.config(text="🎵 节奏模式", bg='#e91e63')
            
            # 记录手动操作
            if self.learning_from_human:
                self.record_manual_action(self.direction, new_direction)
        
        # 执行手动控制
        self.direction = new_direction
        
        # 显示干预状态
        self.status_label.config(
            text=f"🖐️ 手动干预中 ({self.override_duration//10}s) - 自动控制暂停", 
            fg='#ff5722'
        )
        
    def process_manual_override(self):
        """处理手动干预逻辑"""
        if self.manual_override:
            self.override_duration -= 1
            
            if self.override_duration <= 0:
                # 干预结束，恢复原始模式
                self.manual_override = False
                
                # 恢复原始模式
                if self.auto_mode_original == "random":
                    self.random_mode = True
                    self.random_button.config(text="🎮 手动模式", bg='#4caf50')
                elif self.auto_mode_original == "ai":
                    self.ai_mode = True
                    self.ai_button.config(text="🤖 手动模式", bg='#4caf50')
                elif self.auto_mode_original == "rhythm":
                    self.auto_rhythm_enabled = True
                    self.rhythm_button.config(text="🎵 普通模式", bg='#4caf50')
                    
                self.auto_mode_original = None
                
                # 显示恢复状态
                mode_name = {
                    "random": "随机模式",
                    "ai": "AI学习", 
                    "rhythm": "节奏模式"
                }.get(self.auto_mode_original, "自动模式")
                
                self.status_label.config(
                    text=f"✅ 手动干预结束 - 恢复{mode_name}", 
                    fg='#4caf50'
                )
            
    def record_manual_action(self, old_direction, new_direction):
        """记录手动操作用于学习"""
        if not self.snake or not self.food:
            return
            
        head = self.snake[-1]
        
        # 获取状态
        state = self.get_ai_state()
        if state is None:
            return
            
        # 计算奖励（基于食物距离变化）
        old_distance = abs(head[0] - self.food[0]) + abs(head[1] - self.food[1])
        
        # 模拟新位置
        new_head = (head[0] + new_direction[0], head[1] + new_direction[1])
        new_distance = abs(new_head[0] - self.food[0]) + abs(new_head[1] - self.food[1])
        
        # 检查是否吃到食物
        will_eat_food = new_head == self.food
        will_collide = self.is_danger(new_head[0], new_head[1])
        
        # 计算奖励
        reward = 0
        if will_eat_food:
            reward += 15  # 吃到食物的高奖励
        elif will_collide:
            reward -= 10  # 碰撞的惩罚
        elif new_distance < old_distance:
            reward += 2  # 接近食物
        else:
            reward -= 1  # 远离食物
            
        # 记录到人类专家Q表
        if state not in self.human_q_table:
            self.human_q_table[state] = {action: 0.0 for action in [(0, -1), (0, 1), (-1, 0), (1, 0)]}
            
        # 更新Q值（更高的学习率）
        old_value = self.human_q_table[state].get(new_direction, 0.0)
        new_value = old_value + 0.3 * (reward - old_value)  # 更高的学习率
        self.human_q_table[state][new_direction] = new_value
        
        # 记录操作
        self.manual_actions.append({
            'state': state,
            'action': new_direction,
            'reward': reward,
            'timestamp': self.game_time
        })
        
        # 统计
        if will_eat_food:
            self.manual_food_collected += 1
        if will_collide:
            self.manual_collisions += 1
            
    def toggle_learning_mode(self):
        """切换学习模式"""
        self.learning_from_human = not self.learning_from_human
        if self.learning_from_human:
            self.expert_demo_mode = True
            self.random_mode = False
            self.ai_mode = False
            self.auto_rhythm_enabled = False
            
            # 更新按钮状态
            self.random_button.config(text="🎲 随机模式", bg='#9c27b0')
            self.ai_button.config(text="🤖 AI学习", bg='#00bcd4')
            self.rhythm_button.config(text="🎵 节奏模式", bg='#e91e63')
            self.learning_button.config(text="🧠 结束学习", bg='#4caf50')
            
            # 重置学习统计
            self.manual_session_count += 1
            self.manual_food_collected = 0
            self.manual_collisions = 0
            self.manual_actions = []
            
            self.status_label.config(text=f"学习模式开启 - 请手动操作，AI将学习您的技巧", fg='#673ab7')
        else:
            self.expert_demo_mode = False
            self.learning_button.config(text="🧠 学习模式", bg='#673ab7')
            self.status_label.config(text="学习模式结束 - AI将应用学到的技巧", fg='#4caf50')
            
            # 合并人类学习的Q表到AI Q表
            self.merge_human_knowledge()
            
    def merge_human_knowledge(self):
        """将人类学习的知识合并到AI Q表"""
        for state, actions in self.human_q_table.items():
            if state not in self.ai_q_table:
                self.ai_q_table[state] = {}
                
            for action, value in actions.items():
                if action not in self.ai_q_table[state]:
                    self.ai_q_table[state][action] = 0.0
                    
                # 加权合并人类知识
                self.ai_q_table[state][action] = 0.7 * self.ai_q_table[state][action] + 0.3 * value
                
        # 显示学习统计
        efficiency = 0
        if self.manual_collisions > 0:
            efficiency = (self.manual_food_collected / self.manual_collisions) * 100
            
        self.status_label.config(
            text=f"学习完成! 食物:{self.manual_food_collected} 碰撞:{self.manual_collisions} 效率:{efficiency:.1f}%", 
            fg='#673ab7'
        )
        
    def get_human_enhanced_action(self, state):
        """获取人类知识增强的AI动作"""
        if state is None:
            return self.direction
            
        # 优先使用人类学习的Q表
        if state in self.human_q_table:
            best_action = self.direction
            best_value = float('-inf')
            
            for action, value in self.human_q_table[state].items():
                if (action[0] * -1, action[1] * -1) != self.direction:  # 避免反向
                    if value > best_value:
                        best_value = value
                        best_action = action
                        
            return best_action
        else:
            # 回退到普通AI
            return self.get_ai_action(state)
            
    def toggle_ai_mode(self):
        """切换AI学习模式 - 禁用手动功能"""
        self.ai_mode = not self.ai_mode
        if self.ai_mode:
            self.random_mode = False  # 关闭随机模式
            self.auto_rhythm_enabled = False  # 关闭节奏模式
            self.random_button.config(text="🎲 随机模式", bg='#9c27b0')
            self.rhythm_button.config(text="🎵 节奏模式", bg='#e91e63')
            self.ai_button.config(text="🤖 手动模式", bg='#4caf50')
            self.status_label.config(text="AI自动模式已开启", fg='#00bcd4')
        else:
            # AI关闭时自动开启随机模式
            self.ai_mode = False
            self.random_mode = True
            self.auto_rhythm_enabled = False
            self.ai_button.config(text="🤖 AI学习", bg='#00bcd4')
            self.random_button.config(text="🎮 手动模式", bg='#4caf50')
            self.status_label.config(text="切换至随机自动模式", fg='#9c27b0')
            
    def get_ai_state(self):
        """获取AI状态表示"""
        if not self.snake or not self.food:
            return None
            
        head = self.snake[-1]
        
        # 获取到食物的方向
        food_dx = self.food[0] - head[0]
        food_dy = self.food[1] - head[1]
        
        # 标准化方向 (-1, 0, 1)
        food_dir_x = 0 if food_dx == 0 else (1 if food_dx > 0 else -1)
        food_dir_y = 0 if food_dy == 0 else (1 if food_dy > 0 else -1)
        
        # 检查周围危险
        danger_ahead = self.is_danger(head[0] + self.direction[0], head[1] + self.direction[1])
        danger_left = self.is_danger(head[0] + self.direction[1], head[1] - self.direction[0])
        danger_right = self.is_danger(head[0] - self.direction[1], head[1] + self.direction[0])
        
        # 当前方向
        current_dir = self.direction
        dir_index = [(0, -1), (0, 1), (-1, 0), (1, 0)].index(current_dir) if current_dir in [(0, -1), (0, 1), (-1, 0), (1, 0)] else 0
        
        # 创建状态键
        state = (
            food_dir_x, food_dir_y,  # 食物方向
            danger_ahead, danger_left, danger_right,  # 危险检测
            dir_index  # 当前方向
        )
        
        return state
        
    def is_danger(self, x, y):
        """检查位置是否危险"""
        # 检查撞墙
        if x < 0 or x >= self.grid_size or y < 0 or y >= self.grid_size:
            return True
            
        # 检查撞自己
        if (x, y) in self.snake:
            return True
            
        return False
        
    def get_ai_action(self, state):
        """根据状态选择动作"""
        if state is None:
            return self.direction
            
        # ε-贪心策略
        if random.random() < self.ai_epsilon:
            # 探索：随机选择动作
            actions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
            valid_actions = []
            for action in actions:
                if (action[0] * -1, action[1] * -1) != self.direction:  # 避免反向
                    valid_actions.append(action)
            return random.choice(valid_actions) if valid_actions else self.direction
        else:
            # 利用：选择Q值最高的动作
            if state not in self.ai_q_table:
                self.ai_q_table[state] = {action: 0.0 for action in [(0, -1), (0, 1), (-1, 0), (1, 0)]}
            
            best_action = self.direction
            best_value = float('-inf')
            
            for action, value in self.ai_q_table[state].items():
                if (action[0] * -1, action[1] * -1) != self.direction:  # 避免反向
                    if value > best_value:
                        best_value = value
                        best_action = action
                        
            return best_action
            
    def calculate_ai_reward(self):
        """计算AI奖励"""
        if not self.snake or not self.food:
            return -1
            
        head = self.snake[-1]
        reward = 0
        
        # 距离奖励
        old_distance = abs(self.ai_last_state[0] - self.food[0]) + abs(self.ai_last_state[1] - self.food[1]) if self.ai_last_state else float('inf')
        new_distance = abs(head[0] - self.food[0]) + abs(head[1] - self.food[1])
        
        if new_distance < old_distance:
            reward += 1  # 接近食物
        else:
            reward -= 0.5  # 远离食物
            
        # 吃到食物奖励
        if head == self.food:
            reward += 10
            self.ai_food_collected += 1
            
        # 碰撞惩罚
        if self.is_danger(head[0] + self.direction[0], head[1] + self.direction[1]):
            reward -= 5
            self.ai_collision_count += 1
            
        # 存活奖励
        reward += 0.1
        
        return reward
        
    def update_ai_q_table(self, state, action, reward, next_state):
        """更新Q表"""
        if state is None or action is None:
            return
            
        # 初始化Q表
        if state not in self.ai_q_table:
            self.ai_q_table[state] = {a: 0.0 for a in [(0, -1), (0, 1), (-1, 0), (1, 0)]}
        if next_state not in self.ai_q_table:
            self.ai_q_table[next_state] = {a: 0.0 for a in [(0, -1), (0, 1), (-1, 0), (1, 0)]}
            
        # Q-learning更新公式
        old_value = self.ai_q_table[state][action]
        next_max = max(self.ai_q_table[next_state].values())
        
        new_value = old_value + self.ai_learning_rate * (reward + self.ai_discount_factor * next_max - old_value)
        self.ai_q_table[state][action] = new_value
        
    def ai_make_move(self):
        """AI决策并移动"""
        if not self.ai_mode:
            return
            
        # 获取当前状态
        current_state = self.get_ai_state()
        
        # 选择动作（优先使用人类学习的知识）
        if self.human_q_table and random.random() < 0.8:  # 80%概率使用人类知识
            action = self.get_human_enhanced_action(current_state)
        else:
            action = self.get_ai_action(current_state)
        
        # 计算奖励
        reward = self.calculate_ai_reward()
        
        # 更新Q表
        if self.ai_last_state is not None and self.ai_last_action is not None:
            self.update_ai_q_table(self.ai_last_state, self.ai_last_action, reward, current_state)
        
        # 记录状态和动作
        self.ai_last_state = current_state
        self.ai_last_action = action
        
        # 执行动作
        if (action[0] * -1, action[1] * -1) != self.direction:
            self.direction = action
            
        # 更新学习率（随着时间降低）
        self.ai_epsilon = max(0.01, self.ai_epsilon * 0.9999)
            
    def toggle_random_mode(self):
        """切换随机模式 - 禁用手动功能"""
        self.random_mode = not self.random_mode
        if self.random_mode:
            self.ai_mode = False  # 关闭AI模式
            self.auto_rhythm_enabled = False  # 关闭节奏模式
            self.ai_button.config(text="🤖 AI学习", bg='#00bcd4')
            self.rhythm_button.config(text="🎵 节奏模式", bg='#e91e63')
            self.random_button.config(text="🎮 手动模式", bg='#4caf50')
            self.status_label.config(text="自动随机模式已开启", fg='#9c27b0')
        else:
            # 随机关闭时自动开启AI模式
            self.random_mode = False
            self.ai_mode = True
            self.auto_rhythm_enabled = False
            self.random_button.config(text="🎲 随机模式", bg='#9c27b0')
            self.ai_button.config(text="🤖 手动模式", bg='#4caf50')
            self.status_label.config(text="切换至AI自动模式", fg='#00bcd4')
            
    def random_speed_change(self):
        """随机改变速度"""
        if random.random() < 0.3:  # 30%概率改变速度
            self.game_speed = random.randint(self.min_speed, self.max_speed)
            speed_text = f"速度变化: {self.game_speed}ms"
            self.status_label.config(text=speed_text, fg='#ff9800')
            
    def random_direction_change(self):
        """随机改变方向"""
        if random.random() < 0.4:  # 40%概率改变方向
            directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
            # 避免反向
            valid_directions = [
                d for d in directions 
                if (d[0] * -1, d[1] * -1) != self.direction
            ]
            if valid_directions:
                self.direction = random.choice(valid_directions)
                direction_names = {(0, -1): "上", (0, 1): "下", (-1, 0): "左", (1, 0): "右"}
                dir_name = direction_names.get(self.direction, "未知")
                if hasattr(self, 'status_label'):
                    self.status_label.config(text=f"方向变化: {dir_name}", fg='#2196f3')
                    
    def generate_food(self):
        """生成食物"""
        while True:
            x = random.randint(0, self.grid_size - 1)
            y = random.randint(0, self.grid_size - 1)
            if (x, y) not in self.snake:
                self.food = (x, y)
                self.food_lifetime = random.randint(50, 150)  # 食物生命周期
                break
                
    def draw_game(self):
        """绘制游戏画面 - 带动画效果"""
        self.canvas.delete("all")
        self.create_grid_background()
        
        # 绘制蛇身 - 带渐变效果
        for i, segment in enumerate(self.snake):
            x1 = segment[0] * self.cell_size
            y1 = segment[1] * self.cell_size
            x2 = x1 + self.cell_size
            y2 = y1 + self.cell_size
            
            # 蛇头用不同颜色
            if i == len(self.snake) - 1:
                # 蛇头带发光效果
                self.canvas.create_oval(
                    x1+2, y1+2, x2-2, y2-2,
                    fill='#00ff00',
                    outline='#00ff88',
                    width=2
                )
            else:
                # 蛇身渐变
                intensity = int(255 - (i * 255 / len(self.snake)))
                color = f'#{intensity:02x}ff{intensity:02x}'
                self.canvas.create_rectangle(
                    x1+1, y1+1, x2-1, y2-1,
                    fill=color,
                    outline='#00aa00',
                    width=1
                )
                
        # 绘制食物 - 带闪烁效果
        if self.food:
            x1 = self.food[0] * self.cell_size
            y1 = self.food[1] * self.cell_size
            x2 = x1 + self.cell_size
            y2 = y1 + self.cell_size
            
            food_type = random.choice(self.trade_types)
            
            # 闪烁效果
            if self.food_lifetime < 20:
                alpha = int(128 + 127 * (time.time() % 1))
            else:
                alpha = 255
                
            # 食物发光效果
            for i in range(3):
                offset = i * 2
                self.canvas.create_oval(
                    x1-offset, y1-offset, x2+offset, y2+offset,
                    fill='',
                    outline=food_type["color"],
                    width=1
                )
                
            self.canvas.create_oval(
                x1+3, y1+3, x2-3, y2-3,
                fill=food_type["color"],
                outline='#ffffff',
                width=2
            )
            
            # 显示交易符号
            self.canvas.create_text(
                x1 + self.cell_size//2, 
                y1 + self.cell_size//2,
                text=food_type["symbol"],
                font=('Arial', 8),
                fill='#ffffff'
            )
            
        # 绘制动画效果
        self.draw_animation_effects()
        
    def draw_animation_effects(self):
        """绘制动画效果"""
        effects_to_remove = []
        for effect in self.animation_effects:
            effect['lifetime'] -= 1
            if effect['lifetime'] <= 0:
                effects_to_remove.append(effect)
                continue
                
            # 绘制效果
            if effect['type'] == 'teleport':
                # 传送效果 - 圆形扩散
                radius = (20 - effect['lifetime']) * 3
                x, y = effect['pos']
                self.canvas.create_oval(
                    x - radius, y - radius, x + radius, y + radius,
                    fill='', outline='#9c27b0', width=2
                )
            elif effect['type'] == 'trade':
                # 交易效果 - 浮动文字
                x, y = effect['pos']
                offset = (20 - effect['lifetime']) * 2
                color = effect['color']
                text = effect['text']
                self.canvas.create_text(
                    x, y - offset,
                    text=text,
                    font=('Arial', 12, 'bold'),
                    fill=color
                )
                
        # 移除过期效果
        for effect in effects_to_remove:
            self.animation_effects.remove(effect)
            
    def add_animation_effect(self, effect_type, pos, **kwargs):
        """添加动画效果"""
        effect = {
            'type': effect_type,
            'pos': pos,
            'lifetime': 20,
            **kwargs
        }
        self.animation_effects.append(effect)
        
    def move_snake(self):
        """移动蛇"""
        if not self.game_running or self.game_paused:
            return
            
        # 计算新头部位置
        head = self.snake[-1]
        new_head = (
            (head[0] + self.direction[0]) % self.grid_size,
            (head[1] + self.direction[1]) % self.grid_size
        )
        
        # 检查碰撞
        if new_head in self.snake:
            # 撞到自己 - 传送
            self.handle_collision(new_head, "self")
            return
            
        # 移动蛇
        self.snake.append(new_head)
        
        # 检查是否吃到食物
        if new_head == self.food:
            self.eat_food()
        else:
            self.snake.popleft()
            
        # 减少食物生命周期
        self.food_lifetime -= 1
        if self.food_lifetime <= 0:
            self.generate_food()
            
        # 随机模式下的速度和方向变化
        if self.random_mode:
            self.speed_change_timer += 1
            self.direction_change_timer += 1
            
            if self.speed_change_timer >= self.speed_change_interval:
                self.random_speed_change()
                self.speed_change_timer = 0
                
            if self.direction_change_timer >= self.direction_change_interval:
                self.random_direction_change()
                self.direction_change_timer = 0
            
    def handle_collision(self, pos, collision_type):
        """处理碰撞"""
        if collision_type in ["wall", "self"]:
            # 传送效果
            center_x = pos[0] * self.cell_size + self.cell_size // 2
            center_y = pos[1] * self.cell_size + self.cell_size // 2
            self.add_animation_effect('teleport', (center_x, center_y))
            
            # 随机传送
            new_x = random.randint(2, self.grid_size - 3)
            new_y = random.randint(2, self.grid_size - 3)
            
            # 清空蛇并重新定位
            self.snake.clear()
            self.snake.append((new_x, new_y))
            
            # 穿墙增强效果
            self.teleport_effect_duration = 20  # 持续20帧
            self.game_speed = int(self.game_speed / self.teleport_speed_boost)  # 加速
            
            # 自动改变方向
            if self.teleport_direction_change:
                directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
                self.direction = random.choice(directions)
            
            # 节奏模式特殊效果
            if self.auto_rhythm_enabled:
                self.generate_rhythm_pattern()
            
            # 传送惩罚
            teleport_penalty = 1500 + (self.teleport_count * 300)
            self.capital -= teleport_penalty
            self.teleport_count += 1
            self.score -= 5
            
            if self.ai_mode:
                self.ai_collision_count += 1
                
            # 记录性能数据
            self.record_performance_data()
            
            # 更新状态
            if hasattr(self, 'status_label'):
                self.status_label.config(
                    text=f"传送! 速度提升 {self.teleport_speed_boost}x, 损失 ${teleport_penalty}", 
                    fg='#9c27b0'
                )
            
    def toggle_rhythm_mode(self):
        """切换节奏模式 - 禁用手动功能"""
        self.auto_rhythm_enabled = not self.auto_rhythm_enabled
        if self.auto_rhythm_enabled:
            self.generate_rhythm_pattern()
            self.ai_mode = False  # 关闭AI模式
            self.random_mode = False  # 关闭随机模式
            self.ai_button.config(text="🤖 AI学习", bg='#00bcd4')
            self.random_button.config(text="🎲 随机模式", bg='#9c27b0')
            self.rhythm_button.config(text="🎵 普通模式", bg='#4caf50')
            self.status_label.config(text="节奏自动模式已开启", fg='#e91e63')
        else:
            # 节奏关闭时自动开启AI模式
            self.auto_rhythm_enabled = False
            self.ai_mode = True
            self.random_mode = False
            self.rhythm_button.config(text="🎵 节奏模式", bg='#e91e63')
            self.ai_button.config(text="🤖 手动模式", bg='#4caf50')
            self.status_label.config(text="切换至AI自动模式", fg='#00bcd4')
            # 恢复正常速度
            self.game_speed = self.base_speed
            
    def generate_rhythm_pattern(self):
        """生成节奏模式"""
        # 创建节奏模式：速度变化序列
        patterns = [
            [150, 100, 150, 80, 150, 100],  # 基础节奏
            [200, 80, 120, 80, 200, 80],    # 快慢交替
            [100, 100, 100, 300, 100, 100], # 突停节奏
            [120, 150, 180, 120, 90, 120],  # 渐变节奏
            [80, 80, 80, 400, 80, 80],      # 极限节奏
        ]
        self.rhythm_pattern = random.choice(patterns)
        self.rhythm_index = 0
        
    def apply_rhythm_mode(self):
        """应用节奏模式"""
        if not self.auto_rhythm_enabled or not self.rhythm_pattern:
            return
            
        # 按节奏模式改变速度
        if self.game_time % 10 == 0:  # 每10帧改变一次速度
            new_speed = self.rhythm_pattern[self.rhythm_index]
            self.game_speed = new_speed
            
            # 改变方向（配合节奏）
            if random.random() < 0.6:  # 60%概率改变方向
                directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
                valid_directions = [
                    d for d in directions 
                    if (d[0] * -1, d[1] * -1) != self.direction
                ]
                if valid_directions:
                    self.direction = random.choice(valid_directions)
                    
            # 移动到下一个节奏
            self.rhythm_index = (self.rhythm_index + 1) % len(self.rhythm_pattern)
            
            # 更新状态显示
            if hasattr(self, 'status_label'):
                self.status_label.config(
                    text="🚀 全自动模式启动！AI+随机+节奏+学习 全部运行", 
                    fg='#00ff00'
                )
            
    def eat_food(self):
        """吃食物 - 执行交易"""
        food_type = random.choice(self.trade_types)
        
        # 计算交易结果
        if "profit" in food_type:
            profit = food_type["profit"]
            self.capital += profit
            self.score += 10
            self.trades.append(profit)
            text = f"+${profit}"
            color = food_type["color"]
            if self.ai_mode:
                self.ai_food_collected += 1
        else:
            loss = food_type["loss"]
            self.capital -= loss
            self.score -= 5
            self.trades.append(-loss)
            text = f"-${loss}"
            color = food_type["color"]
            
        # 添加交易动画效果
        food_center_x = self.food[0] * self.cell_size + self.cell_size // 2
        food_center_y = self.food[1] * self.cell_size + self.cell_size // 2
        self.add_animation_effect('trade', (food_center_x, food_center_y), 
                                 text=text, color=color)
        
        # 记录性能数据
        self.record_performance_data()
        
        # 生成新食物
        self.generate_food()
        self.update_stats()
        self.update_display()
        
        # 检查游戏结束
        if self.capital <= 0:
            self.game_over()
            
    def update_stats(self):
        """更新统计信息"""
        try:
            if hasattr(self, 'stats_text'):
                self.stats_text.delete(1.0, tk.END)
                
                if self.trades:
                    total_trades = len(self.trades)
                    winning_trades = len([t for t in self.trades if t > 0])
                    win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
                    total_profit = sum(self.trades)
                    avg_profit = total_profit / total_trades if total_trades > 0 else 0
                        
                    # AI和学习统计
                    ai_efficiency = 0
                    if self.ai_mode and self.ai_collision_count > 0:
                        ai_efficiency = (self.ai_food_collected / self.ai_collision_count) * 100
                        
                    human_efficiency = 0
                    if self.learning_from_human and self.manual_collisions > 0:
                        human_efficiency = (self.manual_food_collected / self.manual_collisions) * 100
                    
                    learning_status = "学习中" if self.learning_from_human else "关闭"
                    override_status = "干预中" if self.manual_override else "正常"
                    
                    stats = f"""交易次数: {total_trades} | 胜率: {win_rate:.1f}%
总盈亏: ${total_profit:+,.0f} | 均盈: ${avg_profit:+,.0f}
最大盈利: ${max(self.trades):,.0f} | 最大亏损: ${min(self.trades):,.0f}
传送: {self.teleport_count} | 干预: {self.manual_override_count}
时间: {self.game_time//60}min | 状态: {override_status}
AI效率: {ai_efficiency:.1f}% | 人类效率: {human_efficiency:.1f}%"""
                else:
                    stats = "暂无交易数据"
                    
                self.stats_text.insert(tk.END, stats)
        except Exception as e:
            print(f"更新统计错误: {e}")
        
    def update_charts(self):
        """更新性能图表"""
        self.chart_canvas.delete("all")
        
        if not self.capital_history:
            # 显示无数据提示
            self.chart_canvas.create_text(
                140, 75,
                text="暂无数据\n开始游戏后将显示图表",
                font=('Arial', 10),
                fill='#81c784'
            )
            return
            
        # 获取数据
        data_points = min(50, len(self.capital_history))  # 最多显示50个点
        capital_data = self.capital_history[-data_points:]
        score_data = self.score_history[-data_points:]
        
        if len(capital_data) < 2:
            return
            
        # 图表参数
        width = 260
        height = 120
        margin = 15
        chart_width = width - 2 * margin
        chart_height = height - 2 * margin
        
        # 计算数据范围
        min_capital = min(capital_data)
        max_capital = max(capital_data)
        capital_range = max_capital - min_capital if max_capital != min_capital else 1
        
        min_score = min(score_data) if score_data else 0
        max_score = max(score_data) if score_data else 1
        score_range = max_score - min_score if max_score != min_score else 1
        
        # 绘制坐标轴
        self.chart_canvas.create_line(
            margin, height - margin, width - margin, height - margin,
            fill='#666666', width=1
        )  # X轴
        self.chart_canvas.create_line(
            margin, margin, margin, height - margin,
            fill='#666666', width=1
        )  # Y轴
        
        # 绘制资金曲线
        capital_points = []
        for i, value in enumerate(capital_data):
            x = margin + (i * chart_width / (len(capital_data) - 1))
            y = height - margin - ((value - min_capital) / capital_range) * chart_height
            capital_points.extend([x, y])
            
        if len(capital_points) >= 4:
            self.chart_canvas.create_line(
                capital_points,
                fill='#4caf50',
                width=2,
                smooth=True
            )
            
        # 绘制分数曲线（标准化到资金范围）
        score_points = []
        for i, value in enumerate(score_data):
            x = margin + (i * chart_width / (len(score_data) - 1))
            # 将分数标准化到资金图表范围
            normalized_score = min_capital + (value - min_score) / score_range * capital_range
            y = height - margin - ((normalized_score - min_capital) / capital_range) * chart_height
            score_points.extend([x, y])
            
        if len(score_points) >= 4:
            self.chart_canvas.create_line(
                score_points,
                fill='#ff9800',
                width=2,
                smooth=True,
                dash=(5, 2)
            )
            
        # 绘制图例
        self.chart_canvas.create_rectangle(
            width - 65, 8, width - 8, 20,
            fill='#4caf50', outline='#ffffff'
        )
        self.chart_canvas.create_text(
            width - 68, 14,
            text="资",
            font=('Arial', 7),
            fill='#ffffff',
            anchor='e'
        )
        
        self.chart_canvas.create_rectangle(
            width - 65, 24, width - 8, 36,
            fill='#ff9800', outline='#ffffff'
        )
        self.chart_canvas.create_text(
            width - 68, 30,
            text="分",
            font=('Arial', 7),
            fill='#ffffff',
            anchor='e'
        )
        
        # 更新辅助图表 - 模式活跃度
        self.update_secondary_chart()
        # 更新分析图表
        self.update_analysis_chart()
            
    def show_options_menu(self):
        """显示选项菜单"""
        # 创建选项窗口
        options_window = tk.Toplevel(self.root)
        options_window.title("⚙️ 游戏选项")
        options_window.geometry("400x500")
        options_window.configure(bg='#2d2d44')
        options_window.resizable(False, False)
        
        # 居中显示
        options_window.transient(self.root)
        options_window.grab_set()
        
        # 标题
        tk.Label(
            options_window,
            text="⚙️ 游戏选项设置",
            font=('Arial', 16, 'bold'),
            bg='#2d2d44',
            fg='#ffffff'
        ).pack(pady=20)
        
        # 游戏设置框架
        game_frame = tk.Frame(options_window, bg='#3d3d5c', relief=tk.RAISED, bd=2)
        game_frame.pack(padx=20, pady=10, fill=tk.X)
        
        tk.Label(
            game_frame,
            text="🎮 游戏设置",
            font=('Arial', 12, 'bold'),
            bg='#3d3d5c',
            fg='#ffffff'
        ).pack(pady=10)
        
        # 游戏速度设置
        speed_frame = tk.Frame(game_frame, bg='#3d3d5c')
        speed_frame.pack(pady=5)
        
        tk.Label(
            speed_frame,
            text="游戏速度 (ms):",
            font=('Arial', 10),
            bg='#3d3d5c',
            fg='#ffffff'
        ).pack(side=tk.LEFT, padx=5)
        
        self.speed_var = tk.IntVar(value=self.base_speed)
        speed_scale = tk.Scale(
            speed_frame,
            from_=50, to=500,
            orient=tk.HORIZONTAL,
            variable=self.speed_var,
            bg='#3d3d5c',
            fg='#ffffff',
            highlightthickness=0
        )
        speed_scale.pack(side=tk.LEFT, padx=5)
        
        # 网格大小设置
        grid_frame = tk.Frame(game_frame, bg='#3d3d5c')
        grid_frame.pack(pady=5)
        
        tk.Label(
            grid_frame,
            text="网格大小:",
            font=('Arial', 10),
            bg='#3d3d5c',
            fg='#ffffff'
        ).pack(side=tk.LEFT, padx=5)
        
        self.grid_var = tk.IntVar(value=self.grid_size)
        grid_scale = tk.Scale(
            grid_frame,
            from_=15, to=30,
            orient=tk.HORIZONTAL,
            variable=self.grid_var,
            bg='#3d3d5c',
            fg='#ffffff',
            highlightthickness=0
        )
        grid_scale.pack(side=tk.LEFT, padx=5)
        
        # AI设置框架
        ai_frame = tk.Frame(options_window, bg='#3d3d5c', relief=tk.RAISED, bd=2)
        ai_frame.pack(padx=20, pady=10, fill=tk.X)
        
        tk.Label(
            ai_frame,
            text="🤖 AI设置",
            font=('Arial', 12, 'bold'),
            bg='#3d3d5c',
            fg='#ffffff'
        ).pack(pady=10)
        
        # AI学习率
        learning_frame = tk.Frame(ai_frame, bg='#3d3d5c')
        learning_frame.pack(pady=5)
        
        tk.Label(
            learning_frame,
            text="AI学习率:",
            font=('Arial', 10),
            bg='#3d3d5c',
            fg='#ffffff'
        ).pack(side=tk.LEFT, padx=5)
        
        self.learning_var = tk.DoubleVar(value=self.ai_learning_rate)
        learning_scale = tk.Scale(
            learning_frame,
            from_=0.01, to=0.5,
            resolution=0.01,
            orient=tk.HORIZONTAL,
            variable=self.learning_var,
            bg='#3d3d5c',
            fg='#ffffff',
            highlightthickness=0
        )
        learning_scale.pack(side=tk.LEFT, padx=5)
        
        # AI探索率
        epsilon_frame = tk.Frame(ai_frame, bg='#3d3d5c')
        epsilon_frame.pack(pady=5)
        
        tk.Label(
            epsilon_frame,
            text="AI探索率:",
            font=('Arial', 10),
            bg='#3d3d5c',
            fg='#ffffff'
        ).pack(side=tk.LEFT, padx=5)
        
        self.epsilon_var = tk.DoubleVar(value=self.ai_epsilon)
        epsilon_scale = tk.Scale(
            epsilon_frame,
            from_=0.01, to=0.5,
            resolution=0.01,
            orient=tk.HORIZONTAL,
            variable=self.epsilon_var,
            bg='#3d3d5c',
            fg='#ffffff',
            highlightthickness=0
        )
        epsilon_scale.pack(side=tk.LEFT, padx=5)
        
        # 视觉设置框架
        visual_frame = tk.Frame(options_window, bg='#3d3d5c', relief=tk.RAISED, bd=2)
        visual_frame.pack(padx=20, pady=10, fill=tk.X)
        
        tk.Label(
            visual_frame,
            text="🎨 视觉设置",
            font=('Arial', 12, 'bold'),
            bg='#3d3d5c',
            fg='#ffffff'
        ).pack(pady=10)
        
        # 动画开关
        self.animation_var = tk.BooleanVar(value=True)
        animation_check = tk.Checkbutton(
            visual_frame,
            text="启用动画效果",
            variable=self.animation_var,
            font=('Arial', 10),
            bg='#3d3d5c',
            fg='#ffffff',
            selectcolor='#3d3d5c'
        )
        animation_check.pack(pady=5)
        
        # 网格显示开关
        self.grid_var_visual = tk.BooleanVar(value=True)
        grid_check = tk.Checkbutton(
            visual_frame,
            text="显示网格线",
            variable=self.grid_var_visual,
            font=('Arial', 10),
            bg='#3d3d5c',
            fg='#ffffff',
            selectcolor='#3d3d5c'
        )
        grid_check.pack(pady=5)
        
        # 手动干预设置框架
        override_frame = tk.Frame(visual_frame, bg='#3d3d5c')
        override_frame.pack(pady=5)
        
        tk.Label(
            override_frame,
            text="手动干预持续时间 (帧):",
            font=('Arial', 10),
            bg='#3d3d5c',
            fg='#ffffff'
        ).pack(side=tk.LEFT, padx=5)
        
        self.override_var = tk.IntVar(value=30)
        override_scale = tk.Scale(
            override_frame,
            from_=10, to=100,
            orient=tk.HORIZONTAL,
            variable=self.override_var,
            bg='#3d3d5c',
            fg='#ffffff',
            highlightthickness=0
        )
        override_scale.pack(side=tk.LEFT, padx=5)
        
        tk.Label(
            override_frame,
            text="(100帧≈5秒)",
            font=('Arial', 8),
            bg='#3d3d5c',
            fg='#aaaaaa'
        ).pack(side=tk.LEFT, padx=5)
        
        # 按钮框架
        button_frame = tk.Frame(options_window, bg='#2d2d44')
        button_frame.pack(pady=20)
        
        # 保存设置按钮
        save_button = tk.Button(
            button_frame,
            text="💾 保存设置",
            command=lambda: self.save_options(options_window),
            font=('Arial', 12, 'bold'),
            bg='#4caf50',
            fg='white',
            width=12
        )
        save_button.pack(side=tk.LEFT, padx=5)
        
        # 恢复默认按钮
        default_button = tk.Button(
            button_frame,
            text="🔄 恢复默认",
            command=self.restore_default_options,
            font=('Arial', 12, 'bold'),
            bg='#ff9800',
            fg='white',
            width=12
        )
        default_button.pack(side=tk.LEFT, padx=5)
        
        # 取消按钮
        cancel_button = tk.Button(
            button_frame,
            text="❌ 取消",
            command=options_window.destroy,
            font=('Arial', 12, 'bold'),
            bg='#f44336',
            fg='white',
            width=12
        )
        cancel_button.pack(side=tk.LEFT, padx=5)
        
    def save_options(self, window):
        """保存选项设置"""
        # 应用游戏设置
        self.base_speed = self.speed_var.get()
        self.game_speed = self.base_speed
        
        # 应用AI设置
        self.ai_learning_rate = self.learning_var.get()
        self.ai_epsilon = self.epsilon_var.get()
        
        # 应用手动干预设置
        default_override_duration = self.override_var.get()
        # 更新默认干预持续时间
        
        # 应用视觉设置
        animation_enabled = self.animation_var.get()
        grid_enabled = self.grid_var_visual.get()
        
        # 更新显示
        self.status_label.config(text="设置已保存", fg='#4caf50')
        
        # 关闭选项窗口
        window.destroy()
        
    def restore_default_options(self):
        """恢复默认设置"""
        self.speed_var.set(150)
        self.grid_var.set(20)
        self.learning_var.set(0.1)
        self.epsilon_var.set(0.1)
        self.animation_var.set(True)
        self.grid_var_visual.set(True)
        self.override_var.set(30)
        
        # 显示当前值
        self.chart_canvas.create_text(
            8, 8,
            text=f"${self.capital:,} | {self.score}",
            font=('Arial', 7),
            fill='#ffffff',
            anchor='w'
        )
        
    def record_performance_data(self):
        """记录性能数据"""
        self.capital_history.append(self.capital)
        self.score_history.append(self.score)
        
        # 限制历史数据长度
        max_history = 100
        if len(self.capital_history) > max_history:
            self.capital_history = self.capital_history[-max_history:]
        if len(self.score_history) > max_history:
            self.score_history = self.score_history[-max_history:]
            
        # 定期更新图表
        if self.game_time % self.chart_update_interval == 0:
            self.update_charts()
        
    def update_display(self):
        """更新显示"""
        self.score_label.config(text=f"分数: {self.score}")
        capital_color = '#4caf50' if self.capital > 10000 else '#f44336' if self.capital < 5000 else '#ffd700'
        self.capital_label.config(text=f"资金: ${self.capital:,}", fg=capital_color)
        
        # 显示最近交易
        if self.trades and hasattr(self, 'status_label'):
            recent_trades = self.trades[-5:] if self.trades else []
            recent_text = "最近: " + " ".join([f"{'+{t:,}' if t > 0 else f'{t:,}'}" for t in recent_trades])
            self.status_label.config(text=recent_text, fg='#81c784')
            
    def game_loop(self):
        """游戏主循环 - 多模式并行运行"""
        if self.game_running and not self.game_paused:
            # 增加游戏时间
            self.game_time += 1
            
            # 处理传送效果持续时间
            if self.teleport_effect_duration > 0:
                self.teleport_effect_duration -= 1
                if self.teleport_effect_duration == 0:
                    # 恢复正常速度
                    self.game_speed = self.base_speed
            
            # 节奏模式 - 并行运行
            if self.auto_rhythm_enabled:
                self.apply_rhythm_mode()
            
            # AI决策 - 并行运行
            if self.ai_mode:
                self.ai_make_move()
            
            # 随机模式 - 并行运行（与AI竞争）
            if self.random_mode:
                # 随机模式不直接控制方向，而是影响决策
                self.apply_random_influence()
                
            self.move_snake()
            self.draw_game()
            
            # 定期更新高级面板信息
            if self.game_time % 10 == 0:  # 每10帧更新一次
                self.update_advanced_panels()
                
            # 定期添加运行消息
            if self.game_time % 100 == 0:  # 每100帧添加消息
                self.add_periodic_message()
            
            # 定期记录性能数据
            if self.game_time % 5 == 0:  # 每5帧记录一次
                self.record_performance_data()
            
        if self.game_running:
            self.root.after(self.game_speed, self.game_loop)
            
    def apply_random_influence(self):
        """应用随机模式影响"""
        if random.random() < 0.3:  # 30%概率影响方向
            # 随机改变方向
            directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
            valid_directions = [
                d for d in directions 
                if (d[0] * -1, d[1] * -1) != self.direction
            ]
            if valid_directions:
                self.direction = random.choice(valid_directions)
            
    def update_advanced_panels(self):
        """更新高级面板信息"""
        try:
            # 更新游戏信息
            if hasattr(self, 'game_info_text'):
                self.game_info_text.delete(1.0, tk.END)
                game_info = f"""当前模式: {self.get_current_mode()}
游戏速度: {self.game_speed}ms | FPS: {1000//max(self.game_speed, 1)}
蛇长: {len(self.snake)} | 位置: {self.snake[-1] if self.snake else 'N/A'}
食物位置: {self.food if self.food else 'N/A'} | 生命值: {max(0, self.capital//1000)}"""
                self.game_info_text.insert(tk.END, game_info)
            
            # 更新性能监控
            if hasattr(self, 'perf_text'):
                self.perf_text.delete(1.0, tk.END)
                perf_info = f"""内存使用: {len(self.ai_q_table) + len(self.human_q_table)} Q表项
渲染FPS: {1000//max(self.game_speed, 1)} | 碰撞检测: 正常
AI计算: {'活跃' if self.ai_mode else '空闲'} | 学习: {'进行中' if self.learning_from_human else '暂停'}"""
                self.perf_text.insert(tk.END, perf_info)
            
            # 更新学习进度
            if hasattr(self, 'learning_text'):
                self.learning_text.delete(1.0, tk.END)
                learning_info = f"""Q表大小: {len(self.ai_q_table)} | 人类Q表: {len(self.human_q_table)}
学习率: {self.ai_learning_rate:.3f} | 探索率: {self.ai_epsilon:.3f}
干预次数: {self.manual_override_count} | 食物收集: {self.ai_food_collected}"""
                self.learning_text.insert(tk.END, learning_info)
        except Exception as e:
            print(f"更新面板错误: {e}")
        
        # 更新设置显示
        if hasattr(self, 'game_settings_text'):
            self.update_settings_display()
        
    def update_settings_display(self):
        """更新设置显示"""
        # 游戏设置
        self.game_settings_text.delete(1.0, tk.END)
        game_settings = f"""速度: {self.base_speed}ms | 网格: {self.grid_size}x{self.grid_size}
画布: {self.cell_size*self.grid_size}x{self.cell_size*self.grid_size}px"""
        self.game_settings_text.insert(tk.END, game_settings)
        
        # AI设置
        self.ai_settings_text.delete(1.0, tk.END)
        ai_settings = f"""学习率: {self.ai_learning_rate:.2f} | 探索率: {self.ai_epsilon:.2f}
折扣因子: {self.ai_discount_factor:.2f} | 人类权重: 30%"""
        self.ai_settings_text.insert(tk.END, ai_settings)
        
        # 视觉设置
        self.visual_settings_text.delete(1.0, tk.END)
        visual_settings = f"""动画: ✅启用 | 网格线: ✅显示
传送特效: ✅启用 | 粒子效果: ✅启用"""
        self.visual_settings_text.insert(tk.END, visual_settings)
        
    def get_current_mode(self):
        """获取当前模式描述"""
        if self.manual_override:
            return "🖐️ 手动干预"
        elif self.learning_from_human:
            return "🧠 学习模式"
        elif self.auto_rhythm_enabled:
            return "🎵 节奏模式"
        elif self.ai_mode:
            return "🤖 AI学习"
        elif self.random_mode:
            return "🎲 随机模式"
        else:
            return "🎮 手动模式"
            
    def start_game(self):
        """开始游戏"""
        if not self.game_running:
            self.game_running = True
            self.game_paused = False
            self.speed_change_timer = 0
            self.direction_change_timer = 0
            
            # 自动启动AI模式
            self.ai_mode = True
            self.learning_from_human = False
            self.random_mode = False
            self.auto_rhythm_enabled = False
            
            # 更新按钮状态
            self.start_button.config(state='disabled')
            self.pause_button.config(state='normal')
            self.ai_button.config(text="🤖 手动模式", bg='#4caf50')
            self.random_button.config(text="🎲 随机模式", bg='#9c27b0')
            self.rhythm_button.config(text="🎵 节奏模式", bg='#e91e63')
            
            self.status_label.config(text="游戏自动运行中 (AI模式)", fg='#00bcd4')
            self.game_loop()
            
    def start_game(self):
        """开始游戏"""
        if not self.game_running:
            self.game_running = True
            self.game_paused = False
            self.start_button.config(state='disabled')
            self.pause_button.config(state='normal')
            self.status_label.config(text="游戏进行中...", fg='#81c784')
            self.game_loop()
            
    def toggle_pause(self):
        """切换暂停状态"""
        if self.game_running:
            self.game_paused = not self.game_paused
            if self.game_paused:
                self.pause_button.config(text="▶️ 继续", state='normal')
                self.status_label.config(text="游戏已暂停", fg='#ffd700')
            else:
                self.pause_button.config(text='⏸️ 暂停', state='normal')
                self.status_label.config(text="游戏进行中...", fg='#81c784')
                self.game_loop()
                
    def reset_game(self):
        """重置游戏"""
        self.game_running = False
        self.game_paused = False
        self.snake = deque([(10, 10)])
        self.direction = (1, 0)
        self.game_speed = self.base_speed
        self.score = 0
        self.capital = 10000
        self.trades = []
        self.teleport_count = 0
        self.animation_effects = []
        self.speed_change_timer = 0
        self.direction_change_timer = 0
        
        # 重置AI学习参数
        self.ai_mode = True  # 默认AI模式
        self.ai_last_state = None
        self.ai_last_action = None
        self.ai_collision_count = 0
        self.ai_food_collected = 0
        self.ai_epsilon = 0.1
        
        # 重置性能数据
        self.performance_history = []
        self.capital_history = []
        self.score_history = []
        self.game_time = 0
        
        # 重置穿墙增强参数
        self.teleport_effect_duration = 0
        self.rhythm_pattern = []
        self.rhythm_index = 0
        self.auto_rhythm_enabled = False
        self.rhythm_button.config(text="🎵 节奏模式", bg='#e91e63')
        
        # 重置学习参数
        self.learning_from_human = False
        self.expert_demo_mode = False
        self.manual_override = False
        self.learning_button.config(text="🧠 学习模式", bg='#673ab7')
        
        self.start_button.config(state='normal')
        self.pause_button.config(state='disabled', text="⏸️ 暂停")
        self.random_button.config(text="🎲 随机模式", bg='#9c27b0')
        self.ai_button.config(text="🤖 手动模式", bg='#4caf50')  # AI激活状态
        
        self.generate_food()
        self.draw_game()
        self.update_stats()
        self.update_display()
        
        if hasattr(self, 'status_label'):
            self.status_label.config(text="游戏已重置 - 默认AI模式", fg='#2196f3')
        
    def game_over(self):
        """游戏结束"""
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

是否重新开始?
"""
        else:
            message = "游戏结束! 是否重新开始?"
            
        result = messagebox.askyesno("游戏结束", message)
        if result:
            self.reset_game()
            self.start_game()
        else:
            self.reset_game()
            
    def quit_game(self):
        """退出游戏"""
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