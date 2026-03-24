#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
量化交易贪吃蛇游戏 - 图表AI对比专业版
Chart Analysis with AI Comparison Professional Version
结合图表分析和AI算法对比的综合版本
"""

import tkinter as tk
from tkinter import messagebox, ttk
import random
import time
from collections import deque, defaultdict
import math

class ChartAIComparisonSnake:
    """量化交易贪吃蛇 - 图表AI对比专业版"""
    
    # 配色方案
    COLORS = {
        'bg_dark': '#0a0a0f',
        'bg_panel': '#1a1a2e',
        'bg_frame': '#0f0f1e',
        'text_primary': '#ffffff',
        'text_secondary': '#aaaaaa',
        'text_muted': '#666666',
        'accent_green': '#4caf50',
        'accent_blue': '#2196f3',
        'accent_orange': '#ff9800',
        'accent_purple': '#9c27b0',
        'accent_red': '#f44336',
        'gold': '#ffd700',
        'grid': '#2a2a3e',
        'axis': '#4a4a6e'
    }
    
    # 预定义方向常量（优化性能）
    DIRECTIONS = ((0, -1), (0, 1), (-1, 0), (1, 0))  # 上, 下, 左, 右
    DIRECTION_NAMES = {0: '上', 1: '下', 2: '左', 3: '右'}
    
    # 食物颜色映射（优化性能）
    FOOD_COLORS = {
        '盈利': {'fill': '#4caf50', 'outline': '#81c784'},   # 绿色
        '亏损': {'fill': '#f44336', 'outline': '#e57373'},   # 红色
        '突破': {'fill': '#2196f3', 'outline': '#64b5f6'},   # 蓝色
        '反转': {'fill': '#9c27b0', 'outline': '#ba68c8'}    # 紫色
    }
    
    def __init__(self, root):
        self.root = root
        self.root.title("🐍 量化交易贪吃蛇 - 图表AI对比专业版")
        self.root.configure(bg=self.COLORS['bg_dark'])
        self.root.geometry("1400x900")
        self.root.minsize(1100, 700)
        self.root.resizable(True, True)
        
        # 游戏核心参数
        self.canvas_width = 450
        self.canvas_height = 450
        self.grid_size = 20
        self.cell_size = self.canvas_width // self.grid_size
        
        # AI算法定义（支持多AI同时运行）
        self.ai_algorithms = {
            'Q-Learning': {
                'name': 'Q学习',
                'color': '#4caf50',
                'q_table': {},
                'epsilon': 0.1,
                'learning_rate': 0.1,
                'discount': 0.9,
                'food': 0,
                'collision': 0,
                'capital': 10000,
                'score': 0,
                'active': True
            },
            'SARSA': {
                'name': 'SARSA',
                'color': '#2196f3',
                'q_table': {},
                'epsilon': 0.15,
                'learning_rate': 0.15,
                'discount': 0.85,
                'food': 0,
                'collision': 0,
                'capital': 10000,
                'score': 0,
                'active': True
            },
            'Greedy': {
                'name': '贪心算法',
                'color': '#ff9800',
                'food': 0,
                'collision': 0,
                'capital': 10000,
                'score': 0,
                'active': True
            },
            'Random': {
                'name': '随机策略',
                'color': '#9c27b0',
                'food': 0,
                'collision': 0,
                'capital': 10000,
                'score': 0,
                'active': True
            },
            # 新增AI算法
            'DQN': {
                'name': '深度Q网络',
                'color': '#00bcd4',
                'q_table': {},
                'epsilon': 0.05,
                'learning_rate': 0.2,
                'discount': 0.95,
                'food': 0,
                'collision': 0,
                'capital': 10000,
                'score': 0,
                'active': True,
                'replay_buffer': []
            },
            'AStar': {
                'name': 'A*搜索',
                'color': '#ff5722',
                'food': 0,
                'collision': 0,
                'capital': 10000,
                'score': 0,
                'active': True
            },
            'MCTS': {
                'name': '蒙特卡洛树',
                'color': '#795548',
                'food': 0,
                'collision': 0,
                'capital': 10000,
                'score': 0,
                'active': True,
                'tree': {}
            },
            'Minimax': {
                'name': '极小极大',
                'color': '#607d8b',
                'food': 0,
                'collision': 0,
                'capital': 10000,
                'score': 0,
                'active': True,
                'depth': 3
            },
            'HeuristicBFS': {
                'name': '启发式搜索',
                'color': '#e91e63',
                'food': 0,
                'collision': 0,
                'capital': 10000,
                'score': 0,
                'active': True
            },
            'Hybrid': {
                'name': '混合策略',
                'color': '#3f51b5',
                'food': 0,
                'collision': 0,
                'capital': 10000,
                'score': 0,
                'active': True,
                'q_table': {},
                'epsilon': 0.08
            }
        }
        
        # 当前激活的AI（默认全部启用）
        self.active_algorithms = ['Q-Learning', 'SARSA', 'Greedy', 'Random', 'DQN', 'AStar', 'MCTS', 'Minimax', 'HeuristicBFS', 'Hybrid']
        self.selected_algorithm = 'Q-Learning'  # 当前显示的AI
        
        # 游戏状态（每个AI有自己的游戏实例）
        self.game_instances = {}
        # 过渡：为避免运行时缺失，初始化占位字段用于未来阶段（双槽食物Phase 1准备）
        self.ai_charts = {}
        self.capital_stats_labels = {}
        self.game_running = False
        self.game_paused = False
        self.game_speed = 150
        self.game_time = 0
        
        # 共享的游戏元素（保留用于兼容性）
        self.food = None
        self.shared_food = None  # 共享食物
        
        # 每个AI独立拥有自己的食物（公平性改进）
        self.ai_foods = {}
        
        # 食物随机消失跟踪
        self.food_disappearing = {}  # 记录食物是否处于消失状态
        self.food_disappear_timer = {}  # 消失倒计时
        self.food_types = {}  # 记录每个AI的食物类型
        
        # 历史数据记录
        self.capital_history = defaultdict(lambda: deque(maxlen=100))
        self.score_history = defaultdict(lambda: deque(maxlen=100))
        self.trade_history = defaultdict(list)
        
        # 统计分析
        self.total_profit = defaultdict(int)
        self.total_loss = defaultdict(int)
        self.winning_trades = defaultdict(int)
        self.losing_trades = defaultdict(int)
        
        # 消息系统
        self.message_log = []
        self.max_messages = 15
        
        self.setup_gui()
        self.bind_keys()
        self.generate_food()
        
        # 窗口缩放相关
        self._resize_job = None
        
    def setup_gui(self):
        """设置GUI界面 - 优化版"""
        # 主容器
        main_frame = tk.Frame(self.root, bg=self.COLORS['bg_dark'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 顶部控制栏 - 渐变效果背景
        control_frame = tk.Frame(main_frame, bg=self.COLORS['bg_panel'], relief=tk.RAISED, bd=2)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 标题带图标
        title_frame = tk.Frame(control_frame, bg=self.COLORS['bg_panel'])
        title_frame.pack(side=tk.LEFT, padx=20, pady=8)
        
        tk.Label(title_frame, text="🐍", font=('Arial', 20), bg=self.COLORS['bg_panel'], fg=self.COLORS['gold']).pack(side=tk.LEFT, padx=(0, 10))
        tk.Label(title_frame, text="量化交易贪吃蛇", 
                font=('Microsoft YaHei', 14, 'bold'), bg=self.COLORS['bg_panel'], fg=self.COLORS['text_primary']).pack(side=tk.LEFT)
        tk.Label(title_frame, text="  |  AI对比专业版", 
                font=('Microsoft YaHei', 10), bg=self.COLORS['bg_panel'], fg=self.COLORS['text_secondary']).pack(side=tk.LEFT)
        
        # AI选择区域
        ai_frame = tk.Frame(control_frame, bg=self.COLORS['bg_panel'])
        ai_frame.pack(side=tk.LEFT, padx=20)
        
        tk.Label(ai_frame, text="👁 选择AI:", font=('Microsoft YaHei', 10), bg=self.COLORS['bg_panel'], fg=self.COLORS['text_secondary']).pack(side=tk.LEFT, padx=5)
        
        self.ai_var = tk.StringVar(value='Q学习 (Q-Learning)')
        self.ai_combo = ttk.Combobox(ai_frame, textvariable=self.ai_var, 
                                     values=['Q学习 (Q-Learning)', 'SARSA (SARSA)', '贪心 (Greedy)', '随机 (Random)', '深度Q (DQN)', 'A* (AStar)', 
                                            '蒙特卡洛 (MCTS)', '极小极大 (Minimax)', '启发式 (HeuristicBFS)', '混合 (Hybrid)'],
                                     state='readonly', width=15, font=('Microsoft YaHei', 9))
        self.ai_combo.pack(side=tk.LEFT, padx=5)
        self.ai_combo.bind('<<ComboboxSelected>>', self.on_ai_change)
        
        # AI启用状态复选框 - 紧凑全名
        self.ai_check_vars = {}
        algo_cn_map = {
            'Q-Learning': 'QL', 
            'SARSA': 'SARSA', 
            'Greedy': 'GR', 
            'Random': 'RD',
            'DQN': 'DQN', 
            'AStar': 'A*', 
            'MCTS': 'MC', 
            'Minimax': 'MM',
            'HeuristicBFS': 'HB', 
            'Hybrid': 'HY'
        }
        for algo_name in self.ai_algorithms:
            var = tk.BooleanVar(value=self.ai_algorithms[algo_name]['active'])
            self.ai_check_vars[algo_name] = var
            cb = tk.Checkbutton(ai_frame, text=algo_cn_map.get(algo_name, algo_name), variable=var,
                               command=lambda n=algo_name: self.toggle_ai(n),
                               bg=self.COLORS['bg_panel'], fg=self.ai_algorithms[algo_name]['color'],
                               selectcolor=self.COLORS['bg_dark'], font=('Arial', 7))
            cb.pack(side=tk.LEFT, padx=1)
        
        # 控制按钮 - 带图标
        btn_frame = tk.Frame(control_frame, bg=self.COLORS['bg_panel'])
        btn_frame.pack(side=tk.RIGHT, padx=20, pady=5)
        
        self.start_btn = tk.Button(btn_frame, text="▶ 开始游戏", command=self.start_game,
                                  bg=self.COLORS['accent_green'], fg='white', font=('Microsoft YaHei', 10, 'bold'), 
                                  width=12, bd=0, padx=10, pady=5)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.pause_btn = tk.Button(btn_frame, text="⏸ 暂停", command=self.toggle_pause,
                                  bg=self.COLORS['accent_orange'], fg='white', font=('Microsoft YaHei', 10, 'bold'), 
                                  width=10, state='disabled', bd=0, padx=10, pady=5)
        self.pause_btn.pack(side=tk.LEFT, padx=5)
        
        self.reset_btn = tk.Button(btn_frame, text="🔄 重置游戏", command=self.reset_game,
                                  bg=self.COLORS['accent_red'], fg='white', font=('Microsoft YaHei', 10, 'bold'), 
                                  width=10, bd=0, padx=10, pady=5)
        self.reset_btn.pack(side=tk.LEFT, padx=5)
        
        # 中间内容区 - 左右分栏
        content_frame = tk.Frame(main_frame, bg=self.COLORS['bg_dark'])
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # 左侧游戏区域 - 固定宽度
        left_frame = tk.Frame(content_frame, bg=self.COLORS['bg_panel'], relief=tk.RAISED, bd=2)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 10))
        
        # 右侧图表区域
        right_frame = tk.Frame(content_frame, bg='#1a1a2e', relief=tk.RAISED, bd=2)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # 状态栏 - 显示当前状态
        status_bar = tk.Frame(left_frame, bg=self.COLORS['bg_frame'], height=25)
        status_bar.pack(fill=tk.X, padx=10, pady=(5, 0))
        
        self.status_label = tk.StringVar(value="准备就绪")
        tk.Label(status_bar, textvariable=self.status_label, font=('Microsoft YaHei', 8),
                bg=self.COLORS['bg_frame'], fg=self.COLORS['text_secondary']).pack(side=tk.LEFT)
        
        # 游戏画布 - 带边框装饰
        canvas_frame = tk.Frame(left_frame, bg=self.COLORS['bg_panel'], bd=2, relief=tk.SUNKEN)
        canvas_frame.pack(padx=10, pady=5)
        
        self.game_canvas = tk.Canvas(canvas_frame, width=self.canvas_width, height=self.canvas_height,
                                    bg=self.COLORS['bg_dark'], highlightthickness=0)
        self.game_canvas.pack()
        
        # 当前选中AI的状态卡片
        self.current_ai_frame = tk.LabelFrame(left_frame, text="📊 当前AI状态", font=('Microsoft YaHei', 10, 'bold'),
                                             bg=self.COLORS['bg_panel'], fg=self.COLORS['text_primary'])
        self.current_ai_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.current_ai_labels = {}
        stats = [
            ("算法", lambda: 'Q学习 (Q-Learning)' if self.selected_algorithm == 'Q-Learning' else 
                           'SARSA (SARSA)' if self.selected_algorithm == 'SARSA' else
                           '贪心 (Greedy)' if self.selected_algorithm == 'Greedy' else
                           '随机 (Random)' if self.selected_algorithm == 'Random' else
                           '深度Q (DQN)' if self.selected_algorithm == 'DQN' else
                           'A* (AStar)' if self.selected_algorithm == 'AStar' else
                           '蒙特卡洛 (MCTS)' if self.selected_algorithm == 'MCTS' else
                           '极小极大 (Minimax)' if self.selected_algorithm == 'Minimax' else
                           '启发式 (HeuristicBFS)' if self.selected_algorithm == 'HeuristicBFS' else
                           '混合 (Hybrid)' if self.selected_algorithm == 'Hybrid' else self.selected_algorithm),
            ("资金", lambda: f"${self.ai_algorithms[self.selected_algorithm]['capital']:,.0f}"),
            ("盈亏", lambda: f"{self.ai_algorithms[self.selected_algorithm]['capital'] - 10000:+.0f}"),
            ("胜率", lambda: f"{(self.ai_algorithms[self.selected_algorithm]['food'] / max(1, self.ai_algorithms[self.selected_algorithm]['food'] + self.ai_algorithms[self.selected_algorithm]['collision']) * 100):.1f}%"),
            ("Q表", lambda: str(len(self.ai_algorithms[self.selected_algorithm].get('q_table', {})))),
        ]
        
        for name, func in stats:
            frame = tk.Frame(self.current_ai_frame, bg=self.COLORS['bg_panel'])
            frame.pack(fill=tk.X, padx=8, pady=2)
            tk.Label(frame, text=f"{name}:", font=('Microsoft YaHei', 9), 
                    bg=self.COLORS['bg_panel'], fg=self.COLORS['text_secondary']).pack(side=tk.LEFT)
            var = tk.StringVar(value="0")
            self.current_ai_labels[name] = (var, func)
            color = self.ai_algorithms[self.selected_algorithm]['color']
            tk.Label(frame, textvariable=var, font=('Microsoft YaHei', 10, 'bold'), 
                    bg=self.COLORS['bg_panel'], fg=color).pack(side=tk.RIGHT)
        
        # 食物信息面板
        self.food_info_frame = tk.LabelFrame(left_frame, text="🍎 食物信息", font=('Microsoft YaHei', 10, 'bold'),
                                             bg=self.COLORS['bg_panel'], fg=self.COLORS['text_primary'])
        self.food_info_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.food_labels = {}
        food_stats = [
            ("坐标", lambda: self._get_food_position()),
            ("类型", lambda: self._get_food_type()),
            ("奖励", lambda: self._get_food_reward()),
            ("状态", lambda: self._get_food_status()),
        ]
        
        for name, func in food_stats:
            frame = tk.Frame(self.food_info_frame, bg=self.COLORS['bg_panel'])
            frame.pack(fill=tk.X, padx=8, pady=2)
            tk.Label(frame, text=f"{name}:", font=('Microsoft YaHei', 9), 
                    bg=self.COLORS['bg_panel'], fg=self.COLORS['text_secondary']).pack(side=tk.LEFT)
            var = tk.StringVar(value="-")
            self.food_labels[name] = var
            tk.Label(frame, textvariable=var, font=('Microsoft YaHei', 10, 'bold'), 
                    bg=self.COLORS['bg_panel'], fg=self.COLORS['gold']).pack(side=tk.RIGHT)
        
        # 游戏说明卡片
        help_frame = tk.LabelFrame(left_frame, text="🎮 游戏规则", font=('Microsoft YaHei', 10, 'bold'),
                                 bg=self.COLORS['bg_panel'], fg=self.COLORS['text_primary'])
        help_frame.pack(fill=tk.X, padx=10, pady=5)
        
        help_text = """🍎 吃到黄色食物 = 盈利 (+$1500)
 📉 吃到亏损食物 = 亏损 (-$1200)
 💥 撞到自身 = 重置位置 (扣 $1,500)
 🧱 撞到墙壁 = 随机传送 (扣 $800)  
 📈 蛇身越长移动越困难
 💰 初始资金 $10,000 (所有AI相同)"""
        tk.Label(help_frame, text=help_text, justify=tk.LEFT, font=('Microsoft YaHei', 8),
                bg=self.COLORS['bg_panel'], fg=self.COLORS['text_secondary']).pack(padx=10, pady=8)
        
        # 消息日志
        msg_frame = tk.LabelFrame(left_frame, text="📋 实时日志", font=('Microsoft YaHei', 10, 'bold'),
                                 bg=self.COLORS['bg_panel'], fg=self.COLORS['text_primary'])
        msg_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.msg_text = tk.Text(msg_frame, height=6, bg=self.COLORS['bg_dark'], fg=self.COLORS['accent_green'],
                                font=('Consolas', 8), relief=tk.FLAT)
        self.msg_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar = tk.Scrollbar(self.msg_text)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.msg_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.msg_text.yview)
        
        # 创建选项卡
        self.notebook = ttk.Notebook(right_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 使用样式化选项卡
        style = ttk.Style()
        style.configure('TNotebook.Tab', font=('Microsoft YaHei', 10))
        
        # 选项卡1: AI对比图表
        self.ai_chart_frame = tk.Frame(self.notebook, bg=self.COLORS['bg_dark'])
        self.notebook.add(self.ai_chart_frame, text="📊 AI对比分析")
        self.setup_ai_charts()
        
        # 选项卡2: 资金对比
        self.capital_frame = tk.Frame(self.notebook, bg=self.COLORS['bg_dark'])
        self.notebook.add(self.capital_frame, text="💰 资金走势")
        self.setup_capital_comparison()
        
        # 选项卡3: 性能统计
        self.performance_frame = tk.Frame(self.notebook, bg=self.COLORS['bg_dark'])
        self.notebook.add(self.performance_frame, text="⚡ 性能排名")
        self.setup_performance_stats()
        
        # 选项卡4: 量化分析
        self.analysis_frame = tk.Frame(self.notebook, bg=self.COLORS['bg_dark'])
        self.notebook.add(self.analysis_frame, text="📈 量化指标")
        self.setup_quantitative_analysis()
        
        # 底部统计栏（所有AI汇总）
        stats_frame = tk.Frame(main_frame, bg=self.COLORS['bg_panel'], relief=tk.RAISED, bd=2)
        stats_frame.pack(fill=tk.X, pady=(10, 0))
        
        # 公平公正说明
        fair_frame = tk.Frame(stats_frame, bg='#1a3a1a', height=25)
        fair_frame.pack(fill=tk.X)
        tk.Label(fair_frame, text="⚖️ 公平公正 | 初始资金$10,000 | 独立食物 | 相同规则", 
                font=('Microsoft YaHei', 9), bg='#1a3a1a', fg='#4caf50').pack(pady=3)
        
        # 添加分隔符
        tk.Label(stats_frame, text="━" * 80, font=('Arial', 8), 
                bg=self.COLORS['bg_panel'], fg=self.COLORS['grid']).pack()
        
        self.all_ai_labels = {}
        algo_cn_names = {
            'Q-Learning': 'Q学习 (Q-Learning)', 
            'SARSA': 'SARSA (SARSA)', 
            'Greedy': '贪心 (Greedy)', 
            'Random': '随机 (Random)',
            'DQN': '深度Q (DQN)', 
            'AStar': 'A* (AStar)', 
            'MCTS': '蒙特卡洛 (MCTS)', 
            'Minimax': '极小极大 (Minimax)',
            'HeuristicBFS': '启发式 (HeuristicBFS)', 
            'Hybrid': '混合 (Hybrid)'
        }
        for algo_name in self.ai_algorithms:
            frame = tk.Frame(stats_frame, bg=self.COLORS['bg_frame'], width=150)
            frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=3, pady=5)
            
            color = self.ai_algorithms[algo_name]['color']
            tk.Label(frame, text=algo_cn_names.get(algo_name, algo_name), font=('Microsoft YaHei', 9, 'bold'), 
                    bg=self.COLORS['bg_frame'], fg=color).pack(pady=(2, 0))
            
            var = tk.StringVar(value="$10,000")
            self.all_ai_labels[algo_name] = var
            tk.Label(frame, textvariable=var, font=('Microsoft YaHei', 9), 
                    bg=self.COLORS['bg_frame'], fg=self.COLORS['text_primary']).pack(pady=2)
            
    def setup_ai_charts(self):
        """设置AI对比图表 - 优化版"""
        # 创建6个子图表区域
        self.ai_charts = {}
        positions = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)]
        chart_configs = [
            ("success_rate", "🎯 胜率"),
            ("capital_curve", "💰 资金"),
            ("score", "⭐ 得分"),
            ("trade_count", "📊 交易"),
            ("learning_eff", "🧠 学习"),
            ("overall", "🏆 综合")
        ]
        
        for i, ((row, col), (key, title)) in enumerate(zip(positions, chart_configs)):
            frame = tk.LabelFrame(self.ai_chart_frame, text=title, font=('Microsoft YaHei', 9, 'bold'),
                                 bg=self.COLORS['bg_panel'], fg=self.COLORS['text_primary'])
            frame.grid(row=row, column=col, padx=4, pady=4, sticky='nsew')
            
            self.ai_chart_frame.columnconfigure(col, weight=1)
            self.ai_chart_frame.rowconfigure(row, weight=1)
            
            canvas = tk.Canvas(frame, bg=self.COLORS['bg_dark'],
                             highlightthickness=0)
            canvas.pack(padx=2, pady=2, fill=tk.BOTH, expand=True)
            
            self.ai_charts[key] = canvas
            
    def setup_capital_comparison(self):
        """设置资金对比图表 - 优化版"""
        # 标题区域
        header_frame = tk.Frame(self.capital_frame, bg=self.COLORS['bg_panel'])
        header_frame.pack(fill=tk.X, padx=10, pady=(10, 5))
        
        tk.Label(header_frame, text="📈 资金走势对比", font=('Microsoft YaHei', 12, 'bold'),
                bg=self.COLORS['bg_panel'], fg=self.COLORS['text_primary']).pack(side=tk.LEFT, padx=10)
        
        tk.Label(header_frame, text="曲线上升=盈利 📈 | 曲线下降=亏损 📉 | 初始=$10,000", 
                font=('Microsoft YaHei', 9), bg=self.COLORS['bg_panel'], fg=self.COLORS['text_secondary']).pack(side=tk.LEFT, padx=20)
        
        # 主图表区域
        chart_frame = tk.Frame(self.capital_frame, bg=self.COLORS['bg_panel'], bd=2, relief=tk.SUNKEN)
        chart_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.capital_canvas = tk.Canvas(chart_frame, bg=self.COLORS['bg_dark'],
                                       highlightthickness=0)
        self.capital_canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 底部统计
        stats_frame = tk.Frame(self.capital_frame, bg=self.COLORS['bg_panel'])
        stats_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.capital_stats_labels = {}
        algo_cn_names = {
            'Q-Learning': 'Q学习 (Q-Learning)', 
            'SARSA': 'SARSA (SARSA)', 
            'Greedy': '贪心 (Greedy)', 
            'Random': '随机 (Random)',
            'DQN': '深度Q (DQN)', 
            'AStar': 'A* (AStar)', 
            'MCTS': '蒙特卡洛 (MCTS)', 
            'Minimax': '极小极大 (Minimax)',
            'HeuristicBFS': '启发式 (HeuristicBFS)', 
            'Hybrid': '混合 (Hybrid)'
        }
        for algo_name in self.ai_algorithms:
            frame = tk.Frame(stats_frame, bg=self.COLORS['bg_frame'], width=120)
            frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=3, pady=3)
            
            color = self.ai_algorithms[algo_name]['color']
            tk.Label(frame, text=algo_cn_names.get(algo_name, algo_name), font=('Microsoft YaHei', 9, 'bold'), 
                    bg=self.COLORS['bg_frame'], fg=color).pack(pady=(3, 0))
            
            var = tk.StringVar(value="$10,000")
            self.capital_stats_labels[algo_name] = var
            tk.Label(frame, textvariable=var, font=('Microsoft YaHei', 9), 
                    bg=self.COLORS['bg_frame'], fg=self.COLORS['text_primary']).pack(pady=2)
            
    def setup_performance_stats(self):
        """设置性能统计 - 优化版"""
        # 标题和说明
        header_frame = tk.Frame(self.performance_frame, bg=self.COLORS['bg_panel'])
        header_frame.pack(fill=tk.X, padx=10, pady=(10, 5))
        
        tk.Label(header_frame, text="🏆 AI性能排名", font=('Microsoft YaHei', 12, 'bold'),
                bg=self.COLORS['bg_panel'], fg=self.COLORS['text_primary']).pack(side=tk.LEFT, padx=10)
        
        tk.Label(header_frame, text="规则: 资金40% + 胜率40% + 得分20%", 
                font=('Microsoft YaHei', 9), bg=self.COLORS['bg_panel'], fg=self.COLORS['text_secondary']).pack(side=tk.LEFT, padx=20)
        
        # 创建表格
        columns = ('排名', '算法', '资金', '盈亏', '胜率', '交易', '撞墙')
        self.performance_tree = ttk.Treeview(self.performance_frame, columns=columns, 
                                            show='headings', height=12)
        
        self.performance_tree.heading('排名', text='排名')
        self.performance_tree.column('排名', width=50, anchor='center')
        self.performance_tree.heading('算法', text='算法')
        self.performance_tree.column('算法', width=70, anchor='center')
        self.performance_tree.heading('资金', text='资金')
        self.performance_tree.column('资金', width=90, anchor='center')
        self.performance_tree.heading('盈亏', text='盈亏')
        self.performance_tree.column('盈亏', width=70, anchor='center')
        self.performance_tree.heading('胜率', text='胜率')
        self.performance_tree.column('胜率', width=60, anchor='center')
        self.performance_tree.heading('交易', text='交易')
        self.performance_tree.column('交易', width=60, anchor='center')
        self.performance_tree.heading('撞墙', text='撞墙')
        self.performance_tree.column('撞墙', width=50, anchor='center')
        
        self.performance_tree.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(self.performance_tree, orient=tk.VERTICAL, command=self.performance_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.performance_tree.config(yscrollcommand=scrollbar.set)
        
    def setup_quantitative_analysis(self):
        """设置量化分析 - 优化版"""
        # 标题和说明
        header_frame = tk.Frame(self.analysis_frame, bg=self.COLORS['bg_panel'])
        header_frame.pack(fill=tk.X, padx=10, pady=(10, 5))
        
        tk.Label(header_frame, text="📈 量化指标分析", font=('Microsoft YaHei', 12, 'bold'),
                bg=self.COLORS['bg_panel'], fg=self.COLORS['text_primary']).pack(side=tk.LEFT, padx=10)
        
        tk.Label(header_frame, text="夏普=风险调整收益 | 回撤=最大亏损 | 盈亏比=平均盈利/亏损", 
                font=('Microsoft YaHei', 9), bg=self.COLORS['bg_panel'], fg=self.COLORS['text_secondary']).pack(side=tk.LEFT, padx=20)
        
        # 创建量化分析表格
        columns = ('算法', '夏普比率', '最大回撤', '盈亏比', '胜率', '平均盈利', '平均亏损', '交易频率')
        self.analysis_tree = ttk.Treeview(self.analysis_frame, columns=columns, 
                                         show='headings', height=8)
        
        for col in columns:
            self.analysis_tree.heading(col, text=col)
            self.analysis_tree.column(col, width=85, anchor='center')
        
        self.analysis_tree.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        
        # 滚动条
        scrollbar = ttk.Scrollbar(self.analysis_tree, orient=tk.VERTICAL, command=self.analysis_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.analysis_tree.config(yscrollcommand=scrollbar.set)
        
        # 创建风险对比图
        risk_frame = tk.LabelFrame(self.analysis_frame, text="📊 风险收益分布", font=('Microsoft YaHei', 10, 'bold'),
                                  bg=self.COLORS['bg_panel'], fg=self.COLORS['text_primary'])
        risk_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.risk_canvas = tk.Canvas(risk_frame, bg=self.COLORS['bg_dark'],
                                    highlightthickness=0)
        self.risk_canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
    def calculate_quantitative_metrics(self, algo_name):
        """计算量化分析指标"""
        algo = self.ai_algorithms[algo_name]
        
        # 基础统计
        wins = algo['food']
        losses = algo['collision']
        total_trades = wins + losses
        
        if total_trades == 0:
            return None
        
        # 胜率
        win_rate = wins / total_trades
        
        # 资金变化
        capital_history = list(self.capital_history[algo_name])
        if len(capital_history) < 2:
            return None
        
        # 计算收益率序列
        returns = []
        for i in range(1, len(capital_history)):
            if capital_history[i-1] > 0:
                ret = (capital_history[i] - capital_history[i-1]) / capital_history[i-1]
                returns.append(ret)
        
        # 平均盈利和平均亏损
        avg_win = 1500 if wins > 0 else 0
        avg_loss = 1500 if losses > 0 else 0
        
        # 盈亏比
        profit_loss_ratio = avg_win / avg_loss if avg_loss > 0 else 0
        
        # 计算最大回撤
        max_capital = max(capital_history)
        max_drawdown = 0
        for capital in capital_history:
            if max_capital > 0:
                drawdown = (max_capital - capital) / max_capital
                max_drawdown = max(max_drawdown, drawdown)
        
        # 计算夏普比率（简化版）
        if len(returns) > 1:
            avg_return = sum(returns) / len(returns)
            variance = sum((r - avg_return) ** 2 for r in returns) / len(returns)
            std_return = variance ** 0.5
            if std_return > 0:
                sharpe_ratio = avg_return / std_return * 10  # 简化夏普比率
            else:
                sharpe_ratio = 0
        else:
            sharpe_ratio = 0
        
        # 交易频率（每100帧的交易数）
        trade_frequency = total_trades / max(1, self.game_time / 100)
        
        return {
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown': max_drawdown * 100,
            'profit_loss_ratio': profit_loss_ratio,
            'win_rate': win_rate * 100,
            'avg_win': avg_win,
            'avg_loss': avg_loss,
            'trade_frequency': trade_frequency
        }
        
    def update_quantitative_analysis(self):
        """更新量化分析"""
        # 清空现有数据
        for item in self.analysis_tree.get_children():
            self.analysis_tree.delete(item)
        
        # 计算并插入数据
        algo_cn = {
            'Q-Learning': 'Q学习 (Q-Learning)', 'SARSA': 'SARSA (SARSA)', 'Greedy': '贪心 (Greedy)', 
            'Random': '随机 (Random)', 'DQN': '深度Q (DQN)', 'AStar': 'A* (AStar)', 
            'MCTS': '蒙特卡洛 (MCTS)', 'Minimax': '极小极大 (Minimax)',
            'HeuristicBFS': '启发式 (HeuristicBFS)', 'Hybrid': '混合 (Hybrid)'
        }
        results = []
        
        for algo_name in self.ai_algorithms:
            metrics = self.calculate_quantitative_metrics(algo_name)
            if metrics:
                results.append((algo_name, metrics))
        
        # 按夏普比率排序
        results.sort(key=lambda x: x[1]['sharpe_ratio'], reverse=True)
        
        for algo_name, metrics in results:
            self.analysis_tree.insert('', 'end', values=(
                algo_cn.get(algo_name, algo_name),
                f"{metrics['sharpe_ratio']:.2f}",
                f"{metrics['max_drawdown']:.1f}%",
                f"{metrics['profit_loss_ratio']:.2f}",
                f"{metrics['win_rate']:.1f}%",
                f"${metrics['avg_win']:.0f}",
                f"${metrics['avg_loss']:.0f}",
                f"{metrics['trade_frequency']:.1f}/100帧"
            ))
        
        # 绘制风险收益对比图
        self.draw_risk_return_chart()
        
    def draw_risk_return_chart(self):
        """绘制风险收益对比散点图"""
        canvas = self.risk_canvas
        canvas.delete("all")
        
        # 获取Canvas实际大小
        canvas.update_idletasks()
        width = max(canvas.winfo_width(), 200)
        height = max(canvas.winfo_height(), 150)
        margin = int(min(width, height) * 0.12)
        
        active_algos = [a for a in self.ai_algorithms if self.ai_algorithms[a]['active']]
        algo_cn = {
            'Q-Learning': 'QL', 'SARSA': 'SARSA', 'Greedy': 'GR', 
            'Random': 'RD', 'DQN': 'DQN', 'AStar': 'A*', 
            'MCTS': 'MC', 'Minimax': 'MM',
            'HeuristicBFS': 'HB', 'Hybrid': 'HY'
        }
        
        if not active_algos:
            canvas.create_text(width//2, height//2, text="暂无激活的AI算法", fill='#666666', font=('Arial', 14))
            return
        
        # 收集数据
        data_points = []
        for algo_name in active_algos:
            metrics = self.calculate_quantitative_metrics(algo_name)
            if metrics:
                data_points.append((algo_name, metrics['max_drawdown'], metrics['sharpe_ratio']))
        
        if not data_points:
            canvas.create_text(width//2, height//2, text="等待更多数据...", fill='#666666', font=('Arial', 14))
            return
        
        # 坐标范围
        max_dd = max(d for _, d, _ in data_points) + 10
        max_sr = max(sr for _, _, sr in data_points) + 1
        min_sr = min(sr for _, _, sr in data_points) - 1
        
        # 绘制网格
        for i in range(6):
            x = margin + i * (width - 2 * margin) / 5
            canvas.create_line(x, margin, x, height - margin, fill='#1a1a2e', width=1, dash=(2, 2))
            canvas.create_text(x, height - margin + 15, text=f"{i*20:.0f}%", fill='#888888', font=('Arial', 8))
        
        for i in range(6):
            y = margin + i * (height - 2 * margin) / 5
            canvas.create_line(margin, y, width - margin, y, fill='#1a1a2e', width=1, dash=(2, 2))
            sr = max_sr - i * (max_sr - min_sr) / 5
            canvas.create_text(margin - 8, y, text=f"{sr:.1f}", fill='#888888', font=('Arial', 8), anchor='e')
        
        # 绘制坐标轴
        canvas.create_line(margin, height - margin, width - margin, height - margin, fill='#ffffff', width=2)
        canvas.create_text(width//2, height - 5, text="最大回撤 (%)", fill='#aaaaaa', font=('Arial', 10))
        
        canvas.create_line(margin, margin, margin, height - margin, fill='#ffffff', width=2)
        canvas.create_text(15, height//2, text="夏普比率", fill='#aaaaaa', font=('Arial', 10), angle=90)
        
        # 绘制数据点
        for algo_name, max_dd_val, sharpe in data_points:
            color = self.ai_algorithms[algo_name]['color']
            
            x = margin + (max_dd_val / max_dd) * (width - 2 * margin)
            y = height - margin - ((sharpe - min_sr) / (max_sr - min_sr)) * (height - 2 * margin)
            
            # 绘制点
            canvas.create_oval(x-8, y-8, x+8, y+8, fill=color, outline='#ffffff', width=2)
            
            # 绘制标签
            canvas.create_text(x, y-15, text=algo_cn.get(algo_name, algo_name), 
                             fill=color, font=('Arial', 9, 'bold'), anchor='center')
            
            # 绘制数值
            canvas.create_text(x, y+15, text=f"({max_dd_val:.1f}%, {sharpe:.2f})", 
                             fill='#aaaaaa', font=('Arial', 7), anchor='center')
        
        # 标题
        canvas.create_text(width//2, 15, text="风险收益分布图 (左上角=低风险高收益=最佳)", 
                         fill='#4caf50', font=('Arial', 10, 'bold'))
        
    def on_ai_change(self, event=None):
        """AI切换事件"""
        cn_to_en = {
            'Q学习 (Q-Learning)': 'Q-Learning', 'SARSA (SARSA)': 'SARSA', '贪心 (Greedy)': 'Greedy', 
            '随机 (Random)': 'Random', '深度Q (DQN)': 'DQN', 'A* (AStar)': 'AStar', 
            '蒙特卡洛 (MCTS)': 'MCTS', '极小极大 (Minimax)': 'Minimax',
            '启发式 (HeuristicBFS)': 'HeuristicBFS', '混合 (Hybrid)': 'Hybrid',
            # 向后兼容旧值
            'Q学习': 'Q-Learning', 'SARSA': 'SARSA', '贪心算法': 'Greedy', '随机策略': 'Random',
            '深度Q网络': 'DQN', 'A*搜索': 'AStar', '蒙特卡洛树': 'MCTS', 
            '极小极大': 'Minimax', '启发式搜索': 'HeuristicBFS', '混合策略': 'Hybrid'
        }
        cn_name = self.ai_var.get()
        self.selected_algorithm = cn_to_en.get(cn_name, cn_name)
        self.add_message(f"🔄 切换到AI算法: {cn_name}")
        self.update_current_ai_display()
        
    def toggle_ai(self, algo_name):
        """切换AI启用状态"""
        is_active = self.ai_check_vars[algo_name].get()
        self.ai_algorithms[algo_name]['active'] = is_active
        
        if is_active and algo_name not in self.active_algorithms:
            self.active_algorithms.append(algo_name)
            self.add_message(f"✅ 启用AI算法: {algo_name}")
        elif not is_active and algo_name in self.active_algorithms:
            self.active_algorithms.remove(algo_name)
            self.add_message(f"❌ 禁用AI算法: {algo_name}")
            
    def initialize_game_instances(self):
        """初始化游戏实例 - 公平版本"""
        # 清空旧的实例
        self.game_instances.clear()
        self.ai_foods.clear()
        
        for algo_name in self.active_algorithms:
            # 每个AI独立初始化
            self.game_instances[algo_name] = {
                'snake': deque([(10, 10)], maxlen=400),
                'direction': (1, 0),
                'algorithm': algo_name
            }
            
            # 为每个AI生成独立的食物（公平性关键）
            self.ai_foods[algo_name] = self._generate_individual_food(algo_name)
            
            # 初始化资金历史
            self.capital_history[algo_name].append(self.ai_algorithms[algo_name]['capital'])
            self.score_history[algo_name].append(self.ai_algorithms[algo_name]['score'])
    
    def _generate_individual_food(self, exclude_algo=None):
        """为特定AI生成食物"""
        food_types = [
            {"name": "盈利", "amount": 1500, "emoji": "💰"},
            {"name": "亏损", "amount": -1200, "emoji": "📉"},
            {"name": "突破", "amount": 2000, "emoji": "🚀"},
            {"name": "反转", "amount": 1800, "emoji": "⚡"}
        ]
        
        while True:
            x = random.randint(0, self.grid_size - 1)
            y = random.randint(0, self.grid_size - 1)
            
            # 检查是否在任何AI的蛇身上
            collision = False
            for algo_name, instance in self.game_instances.items():
                if algo_name == exclude_algo:
                    continue
                if (x, y) in instance['snake']:
                    collision = True
                    break
            
            if not collision:
                food_type = random.choice(food_types)
                # 记录食物类型
                if exclude_algo:
                    self.food_types[exclude_algo] = food_type
                return (x, y)
    
    def randomize_food(self):
        """随机改变或消失食物"""
        for algo_name in self.ai_algorithms:
            if not self.ai_algorithms[algo_name]['active']:
                continue
            
            # 初始化跟踪
            if algo_name not in self.food_disappearing:
                self.food_disappearing[algo_name] = False
                self.food_disappear_timer[algo_name] = 0
            
            if self.food_disappearing[algo_name]:
                # 食物正在消失中
                self.food_disappear_timer[algo_name] -= 1
                if self.food_disappear_timer[algo_name] <= 0:
                    # 重新生成食物
                    self.food_disappearing[algo_name] = False
                    self.ai_foods[algo_name] = self._generate_individual_food(algo_name)
            else:
                # 随机决定是否改变或消失食物
                rand = random.random()
                
                if rand < 0.01:  # 1% 概率食物消失
                    self.food_disappearing[algo_name] = True
                    self.food_disappear_timer[algo_name] = random.randint(20, 60)  # 消失20-60帧
                    old_food = self.ai_foods.get(algo_name)
                    self.ai_foods[algo_name] = None
                    if old_food:
                        self.add_message(f"🌫️ {algo_name} 食物消失!")
                elif rand < 0.03:  # 2% 概率改变位置（总共3%）
                    self.ai_foods[algo_name] = self._generate_individual_food(algo_name)
                    self.add_message(f"🔄 {algo_name} 食物换位!")
    
    def _get_food_position(self):
        """获取当前选中AI的食物坐标"""
        if self.selected_algorithm not in self.ai_foods:
            return "无"
        food = self.ai_foods.get(self.selected_algorithm)
        if food is None:
            return "消失中"
        return f"({food[0]}, {food[1]})"
    
    def _get_food_type(self):
        """获取当前选中AI的食物类型"""
        if self.selected_algorithm not in self.food_types:
            return "未知"
        food_type = self.food_types.get(self.selected_algorithm)
        if food_type is None:
            return "消失中"
        return f"{food_type['emoji']} {food_type['name']}"
    
    def _get_food_reward(self):
        """获取当前选中AI的食物奖励"""
        if self.selected_algorithm not in self.food_types:
            return "-"
        food_type = self.food_types.get(self.selected_algorithm)
        if food_type is None:
            return "消失中"
        amount = food_type['amount']
        sign = "+" if amount > 0 else ""
        return f"{sign}${amount}"
    
    def _get_food_status(self):
        """获取当前选中AI的食物状态"""
        if self.selected_algorithm not in self.food_disappearing:
            return "正常"
        if self.food_disappearing.get(self.selected_algorithm, False):
            timer = self.food_disappear_timer.get(self.selected_algorithm, 0)
            return f"消失中 ({timer}帧)"
        return "正常"
    
    def update_food_info_display(self):
        """更新食物信息显示"""
        for name, var in self.food_labels.items():
            if name == "坐标":
                var.set(self._get_food_position())
            elif name == "类型":
                var.set(self._get_food_type())
            elif name == "奖励":
                var.set(self._get_food_reward())
            elif name == "状态":
                var.set(self._get_food_status())
    
    def get_valid_moves(self, instance):
        """获取有效的移动方向（防卡死）- 优化版"""
        head = instance['snake'][-1]
        snake_body = instance['snake']
        current_dir = instance['direction']
        grid_size = self.grid_size
        
        valid_moves = []
        
        for i, d in enumerate(self.DIRECTIONS):
            # 不能后退
            if d[0] == -current_dir[0] and d[1] == -current_dir[1]:
                continue
            
            new_x = head[0] + d[0]
            new_y = head[1] + d[1]
            
            # 检测墙壁
            if new_x < 0 or new_x >= grid_size or new_y < 0 or new_y >= grid_size:
                continue
            
            # 检测自身碰撞（使用元组）
            if (new_x, new_y) in snake_body:
                continue
            
            valid_moves.append(d)
        
        return valid_moves
    
    def get_ai_decision(self, instance):
        """获取AI决策 - 优化版"""
        algo_name = instance['algorithm']
        algorithm = self.ai_algorithms[algo_name]
        
        head = instance['snake'][-1]
        food = self.ai_foods.get(algo_name)
        
        # 计算食物方向
        if food is None:
            food_dx = 0
            food_dy = 0
        else:
            food_dx = food[0] - head[0]
            food_dy = food[1] - head[1]
        
        # 快速路径：Q-Learning 和 SARSA
        if algo_name in ('Q-Learning', 'SARSA'):
            state = (food_dx, food_dy, instance['direction'])
            q_table = algorithm['q_table']
            
            valid_moves = self.get_valid_moves(instance)
            
            if not valid_moves:
                # 无路可走，强制移动
                for d in self.DIRECTIONS:
                    if d[0] != -instance['direction'][0] or d[1] != -instance['direction'][1]:
                        return d
                return (1, 0)
            
            if random.random() < algorithm['epsilon']:
                return random.choice(valid_moves)
            
            # 优化Q表查找
            q_values = q_table.get(state)
            if q_values is None:
                q_table[state] = [0, 0, 0, 0]
                q_values = q_table[state]
            
            # 快速找到最大值索引
            best_idx = 0
            best_val = q_values[0]
            for i in range(1, 4):
                if q_values[i] > best_val:
                    best_val = q_values[i]
                    best_idx = i
            
            best_dir = self.DIRECTIONS[best_idx]
            if best_dir in valid_moves:
                return best_dir
            return valid_moves[0]
        
        # 快速路径：Greedy
        if algo_name == 'Greedy':
            valid_moves = self.get_valid_moves(instance)
            if not valid_moves:
                for d in self.DIRECTIONS:
                    if d[0] != -instance['direction'][0] or d[1] != -instance['direction'][1]:
                        return d
                return (1, 0)
            
            # 贪心选择
            preferred = self.DIRECTIONS[0] if abs(food_dx) >= abs(food_dy) else self.DIRECTIONS[1]
            if food_dx < 0:
                preferred = self.DIRECTIONS[2]
            elif food_dx > 0:
                preferred = self.DIRECTIONS[3]
            elif food_dy < 0:
                preferred = self.DIRECTIONS[0]
            elif food_dy > 0:
                preferred = self.DIRECTIONS[1]
            
            if preferred in valid_moves:
                return preferred
            
            # 选择离食物最近的有效方向
            best_dir = valid_moves[0]
            best_dist = float('inf')
            for d in valid_moves:
                dist = abs(head[0] + d[0] - food[0]) + abs(head[1] + d[1] - food[1]) if food else 0
                if dist < best_dist:
                    best_dist = dist
                    best_dir = d
            return best_dir
        
        # 快速路径：Random
        if algo_name == 'Random':
            valid_moves = self.get_valid_moves(instance)
            return random.choice(valid_moves) if valid_moves else (1, 0)
        
        # DQN
        if algo_name == 'DQN':
            state = (food_dx, food_dy, instance['direction'])
            q_table = algorithm['q_table']
            valid_moves = self.get_valid_moves(instance)
            
            if not valid_moves:
                for d in self.DIRECTIONS:
                    if d[0] != -instance['direction'][0] or d[1] != -instance['direction'][1]:
                        return d
                return (1, 0)
            
            if random.random() < algorithm['epsilon']:
                return random.choice(valid_moves)
            
            q_values = q_table.get(state)
            if q_values is None:
                q_table[state] = [0, 0, 0, 0]
                q_values = q_table[state]
            
            best_idx = 0
            best_val = q_values[0]
            for i in range(1, 4):
                if q_values[i] > best_val:
                    best_val = q_values[i]
                    best_idx = i
            
            best_dir = self.DIRECTIONS[best_idx]
            if best_dir in valid_moves:
                return best_dir
            return valid_moves[0]
        
        # A* 搜索
        if algo_name == 'AStar':
            return self.a_star_search(instance)
        
        # MCTS
        if algo_name == 'MCTS':
            return self.mcts_search(instance)
        
        # Minimax
        if algo_name == 'Minimax':
            return self.minimax_search(instance)
        
        # HeuristicBFS
        if algo_name == 'HeuristicBFS':
            return self.heuristic_bfs(instance)
        
        # Hybrid
        if algo_name == 'Hybrid':
            return self.hybrid_strategy(instance)
        
        return (1, 0)
    
    def a_star_search(self, instance):
        """A*搜索算法 - 优化版"""
        algo_name = instance['algorithm']
        head = instance['snake'][-1]
        food = self.ai_foods.get(algo_name)
        
        if food is None:
            food = self._generate_individual_food(algo_name)
            self.ai_foods[algo_name] = food
        
        if not food:
            return (1, 0)
        
        # 使用预定义常量
        grid_size = self.grid_size
        snake_body = set(instance['snake'])  # 使用set加速查找
        current_dir = instance['direction']
        
        # 快速失败：如果就在食物旁边
        if abs(head[0] - food[0]) + abs(head[1] - food[1]) == 1:
            for d in self.DIRECTIONS:
                if d[0] != -current_dir[0] or d[1] != -current_dir[1]:
                    new_pos = (head[0] + d[0], head[1] + d[1])
                    if 0 <= new_pos[0] < grid_size and 0 <= new_pos[1] < grid_size:
                        if new_pos not in snake_body:
                            return d
        
        # 使用预定义常量
        directions = self.DIRECTIONS
        
        def get_neighbors(pos):
            neighbors = []
            for i, d in enumerate(directions):
                if d[0] == -current_dir[0] and d[1] == -current_dir[1]:
                    continue
                new_x = pos[0] + d[0]
                new_y = pos[1] + d[1]
                if 0 <= new_x < grid_size and 0 <= new_y < grid_size:
                    if (new_x, new_y) not in snake_body:
                        neighbors.append((new_x, new_y))
            return neighbors
        
        # A* 搜索 - 限制迭代次数
        import heapq
        open_set = [(abs(head[0] - food[0]) + abs(head[1] - food[1]), 0, head, None)]
        closed_set = set()
        max_iterations = 100  # 限制最大迭代次数
        iterations = 0
        
        while open_set and iterations < max_iterations:
            iterations += 1
            f, g, current, parent = heapq.heappop(open_set)
            
            if current == food:
                # 找到路径，回溯方向
                while parent and parent[1] != head:
                    parent = parent[2]
                if parent:
                    return parent[1]
                return (1, 0)
            
            closed_set.add(current)
            
            for new_pos in get_neighbors(current):
                if new_pos in closed_set:
                    continue
                h = abs(new_pos[0] - food[0]) + abs(new_pos[1] - food[1])
                heapq.heappush(open_set, (g + 1 + h, g + 1, new_pos, (current, None, parent)))
        
        # 如果找不到路径，使用贪心
        valid_dirs = self.get_valid_moves(instance)
        
        if not valid_dirs:
            for d in self.DIRECTIONS:
                if d[0] != -current_dir[0] or d[1] != -current_dir[1]:
                    return d
            return (1, 0)
        
        best_dir = valid_dirs[0]
        best_dist = float('inf')
        for d in valid_dirs:
            new_pos = (head[0] + d[0], head[1] + d[1])
            dist = abs(new_pos[0] - food[0]) + abs(new_pos[1] - food[1])
            if dist < best_dist:
                best_dist = dist
                best_dir = d
        return best_dir
    
    def mcts_search(self, instance):
        """蒙特卡洛树搜索（简化版）- 优化版"""
        algo_name = instance['algorithm']
        head = instance['snake'][-1]
        food = self.ai_foods.get(algo_name)
        
        if food is None:
            food = self._generate_individual_food(algo_name)
            self.ai_foods[algo_name] = food
        
        if not food:
            return (1, 0)
        
        # 使用预定义常量
        grid_size = self.grid_size
        current_dir = instance['direction']
        snake_body = instance['snake']
        
        # 使用统一的有效移动检测
        valid_dirs = self.get_valid_moves(instance)
        
        if not valid_dirs:
            # 无路可走，强制移动
            for d in self.DIRECTIONS:
                if d[0] != -current_dir[0] or d[1] != -current_dir[1]:
                    return d
            return (1, 0)
        
        # 评估每个可能的动作
        best_dir = valid_dirs[0]
        best_score = -float('inf')
        directions = self.DIRECTIONS
        
        for d in valid_dirs:
            new_x = head[0] + d[0]
            new_y = head[1] + d[1]
            
            # 模拟评分
            score = 0
            
            # 距离食物越近越好
            dist_to_food = abs(new_x - food[0]) + abs(new_y - food[1])
            score -= dist_to_food * 2
            
            # 检查是否安全
            safe = True
            for i in range(1, 4):
                check_x = new_x + d[0] * i
                check_y = new_y + d[1] * i
                if check_x < 0 or check_x >= grid_size or check_y < 0 or check_y >= grid_size:
                    safe = False
                    score -= 50
                    break
                if (check_x, check_y) in snake_body:
                    safe = False
                    score -= 50
                    break
            
            # 空间越大越好
            space_score = 0
            for dd in directions:
                check_x = new_x + dd[0]
                check_y = new_y + dd[1]
                if 0 <= check_x < grid_size and 0 <= check_y < grid_size:
                    if (check_x, check_y) not in snake_body:
                        space_score += 1
            score += space_score * 5
            
            if score > best_score:
                best_score = score
                best_dir = d
        
        return best_dir
    
    def minimax_search(self, instance, depth=3):
        """极小极大算法 - 公平版本"""
        algo_name = instance['algorithm']
        head = instance['snake'][-1]
        food = self.ai_foods.get(algo_name)
        if food is None:
            food = self._generate_individual_food(algo_name)
            self.ai_foods[algo_name] = food
        if not food:
            return (1, 0)
        
        # 使用统一的有效移动检测
        valid_dirs = self.get_valid_moves(instance)
        directions = self.DIRECTIONS
        
        if not valid_dirs:
            # 无路可走，强制移动
            for d in directions:
                if d[0] != -instance['direction'][0] or d[1] != -instance['direction'][1]:
                    return d
            return (1, 0)
        
        def evaluate(pos, snake):
            if not food:
                return 0
            
            score = 0
            
            # 距离食物
            dist = abs(pos[0] - food[0]) + abs(pos[1] - food[1])
            score -= dist * 2
            
            # 安全性检查
            safe_dirs = 0
            for d in directions:
                check = (pos[0] + d[0], pos[1] + d[1])
                # 检测墙壁
                if check[0] < 0 or check[0] >= self.grid_size or check[1] < 0 or check[1] >= self.grid_size:
                    continue
                if check not in snake:
                    safe_dirs += 1
            score += safe_dirs * 10
            
            # 避免边界
            if pos[0] < 2 or pos[0] > self.grid_size - 3:
                score -= 20
            if pos[1] < 2 or pos[1] > self.grid_size - 3:
                score -= 20
            
            return score
        
        best_dir = valid_dirs[0] if valid_dirs else (1, 0)
        best_value = -float('inf')
        
        for d in valid_dirs:
            new_pos = (head[0] + d[0], head[1] + d[1])
            
            if new_pos in instance['snake']:
                continue
            
            value = evaluate(new_pos, instance['snake'])
            
            if value > best_value:
                best_value = value
                best_dir = d
        
        return best_dir
    
    def heuristic_bfs(self, instance):
        """启发式搜索 - 优化版"""
        algo_name = instance['algorithm']
        head = instance['snake'][-1]
        food = self.ai_foods.get(algo_name)
        if food is None:
            food = self._generate_individual_food(algo_name)
            self.ai_foods[algo_name] = food
        if not food:
            return (1, 0)
        
        # 使用统一的有效移动检测
        valid_dirs = self.get_valid_moves(instance)
        directions = self.DIRECTIONS
        
        if not valid_dirs:
            # 无路可走，强制移动
            for d in directions:
                if d[0] != -instance['direction'][0] or d[1] != -instance['direction'][1]:
                    return d
            return (1, 0)
        
        scores = []
        
        for d in valid_dirs:
            new_x = head[0] + d[0]
            new_y = head[1] + d[1]
            
            score = 0
            
            # 距离分数
            dist = abs(new_x - food[0]) + abs(new_y - food[1])
            score -= dist * 3
            
            # 安全性分数
            safe = True
            open_spaces = 0
            for dd in directions:
                check_x = new_x + dd[0]
                check_y = new_y + dd[1]
                # 检测墙壁
                if check_x < 0 or check_x >= self.grid_size or check_y < 0 or check_y >= self.grid_size:
                    continue
                if (check_x, check_y) in instance['snake']:
                    safe = False
                else:
                    open_spaces += 1
            
            if not safe:
                score -= 30
            else:
                score += open_spaces * 5
            
            # 空间大小启发式
            snake_len = len(instance['snake'])
            if open_spaces > snake_len:
                score += 10
            
            scores.append((d, score, open_spaces))
        
        # 按分数排序，相同时选择空间更大的
        scores.sort(key=lambda x: (x[1], x[2]), reverse=True)
        
        return scores[0][0] if scores else (1, 0)
    
    def hybrid_strategy(self, instance):
        """混合策略：结合贪心和Q学习 - 优化版"""
        algo_name = instance['algorithm']
        algorithm = self.ai_algorithms['Hybrid']
        head = instance['snake'][-1]
        food = self.ai_foods.get(algo_name)
        
        if food is None:
            food = self._generate_individual_food(algo_name)
            self.ai_foods[algo_name] = food
        
        if not food:
            return (1, 0)
        
        # 使用统一的有效移动检测
        valid_dirs = self.get_valid_moves(instance)
        directions = self.DIRECTIONS
        
        if not valid_dirs:
            # 无路可走，强制移动
            for d in directions:
                if d[0] != -instance['direction'][0] or d[1] != -instance['direction'][1]:
                    return d
            return (1, 0)
        
        # 贪心部分：计算到食物的距离
        best_greedy = None
        best_dist = float('inf')
        for d in valid_dirs:
            new_x = head[0] + d[0]
            new_y = head[1] + d[1]
            dist = abs(new_x - food[0]) + abs(new_y - food[1])
            if dist < best_dist:
                best_dist = dist
                best_greedy = d
        
        # Q学习部分
        state = (food[0] - head[0], food[1] - head[1], instance['direction'])
        
        if random.random() < algorithm['epsilon']:
            # 探索
            return random.choice(valid_dirs)
        else:
            # 利用：70%贪心，30%Q表
            if random.random() < 0.7 and best_greedy:
                return best_greedy
            else:
                q_table = algorithm['q_table']
                q_values = q_table.get(state)
                if q_values is None:
                    q_table[state] = [0, 0, 0, 0]
                    q_values = q_table[state]
                
                # 快速找最大值
                best_action = 0
                best_val = q_values[0]
                for i in range(1, 4):
                    if q_values[i] > best_val:
                        best_val = q_values[i]
                        best_action = i
                
                if best_action < len(directions):
                    best_dir = directions[best_action]
                    if best_dir in valid_dirs:
                        return best_dir
                
                return valid_dirs[0]
        
    def update_ai_q_table(self, algo_name, reward, state, action):
        """更新AI的Q表"""
        algorithm = self.ai_algorithms[algo_name]
        if 'q_table' not in algorithm:
            return
            
        if state not in algorithm['q_table']:
            algorithm['q_table'][state] = [0, 0, 0, 0]
            
        old_q = algorithm['q_table'][state][action]
        next_max = max(algorithm['q_table'].get(state, [0, 0, 0, 0]))
        new_q = old_q + algorithm['learning_rate'] * (reward + algorithm['discount'] * next_max - old_q)
        algorithm['q_table'][state][action] = new_q
        
    def draw_game(self):
        """绘制游戏（绘制当前选中AI的游戏状态）"""
        self.game_canvas.delete("all")
        
        if self.selected_algorithm not in self.game_instances:
            return
            
        instance = self.game_instances[self.selected_algorithm]
        
        # 绘制网格线
        for i in range(0, self.canvas_width, self.cell_size):
            self.game_canvas.create_line(i, 0, i, self.canvas_height, fill='#2a2a3e', width=1)
        for i in range(0, self.canvas_height, self.cell_size):
            self.game_canvas.create_line(0, i, self.canvas_width, i, fill='#2a2a3e', width=1)
        
        # 绘制坐标轴
        # X轴
        self.game_canvas.create_line(0, self.canvas_height - 1, self.canvas_width, self.canvas_height - 1, 
                                    fill='#4a4a6e', width=2)
        # Y轴
        self.game_canvas.create_line(1, 0, 1, self.canvas_height, fill='#4a4a6e', width=2)
        
        # 绘制刻度值（每隔5个格子显示数字）
        for i in range(0, self.grid_size, 5):
            # X轴刻度
            x = i * self.cell_size + self.cell_size // 2
            self.game_canvas.create_text(x, self.canvas_height - 3, text=str(i), fill='#666666', font=('Arial', 7))
            # Y轴刻度
            y = i * self.cell_size + self.cell_size // 2
            self.game_canvas.create_text(3, y, text=str(i), fill='#666666', font=('Arial', 7))
        
        # 蛇
        color = self.ai_algorithms[self.selected_algorithm]['color']
        for i, segment in enumerate(instance['snake']):
            x1 = segment[0] * self.cell_size
            y1 = segment[1] * self.cell_size
            x2 = x1 + self.cell_size
            y2 = y1 + self.cell_size
            
            if i == len(instance['snake']) - 1:
                self.game_canvas.create_oval(x1+2, y1+2, x2-2, y2-2,
                                            fill=color, outline='#ffffff', width=2)
            else:
                intensity = max(50, int(200 - (i * 150 / len(instance['snake']))))
                # 转换颜色为RGB
                r = int(int(color[1:3], 16) * intensity / 255)
                g = int(int(color[3:5], 16) * intensity / 255)
                b = int(int(color[5:7], 16) * intensity / 255)
                faded_color = f'#{r:02x}{g:02x}{b:02x}'
                self.game_canvas.create_rectangle(x1+1, y1+1, x2-1, y2-1,
                                                  fill=faded_color, outline=color)
                                                  
        # 绘制该AI的食物（独立食物，根据类型显示不同颜色）
        food = self.ai_foods.get(self.selected_algorithm)
        if food:
            x1 = food[0] * self.cell_size
            y1 = food[1] * self.cell_size
            x2 = x1 + self.cell_size
            y2 = y1 + self.cell_size
            
            # 根据食物类型获取颜色
            food_type = self.food_types.get(self.selected_algorithm)
            if food_type and food_type['name'] in self.FOOD_COLORS:
                colors = self.FOOD_COLORS[food_type['name']]
            else:
                colors = self.FOOD_COLORS['盈利']  # 默认绿色
            
            self.game_canvas.create_oval(x1+3, y1+3, x2-3, y2-3,
                                        fill=colors['fill'], outline=colors['outline'], width=2)
                                          
    def draw_ai_comparison_charts(self):
        """绘制AI对比图表"""
        # 成功率对比
        self.draw_success_rate_chart()
        # 资金曲线（小图）
        self.draw_capital_curve_chart()
        # 得分对比
        self.draw_score_chart()
        # 交易次数对比
        self.draw_trade_count_chart()
        # 学习效率对比
        self.draw_learning_eff_chart()
        # 综合排名对比
        self.draw_overall_chart()
        # 资金曲线对比（在大图中）
        self.draw_multi_capital_chart()
        # 性能统计
        self.update_performance_table()
        # 量化分析
        self.update_quantitative_analysis()
        
    def draw_success_rate_chart(self):
        """绘制成功率对比柱状图"""
        canvas = self.ai_charts["success_rate"]
        canvas.delete("all")
        
        # 获取Canvas实际大小
        canvas.update_idletasks()
        width = max(canvas.winfo_width(), 100)
        height = max(canvas.winfo_height(), 80)
        margin = int(min(width, height) * 0.15)
        
        active_algos = [a for a in self.ai_algorithms if self.ai_algorithms[a]['active']]
        if not active_algos:
            canvas.create_text(width//2, height//2, text="暂无激活的AI", fill='#ffffff', font=('Arial', 12))
            return
            
        # 计算柱状图布局
        chart_width = width - 2 * margin
        bar_width = min(35, chart_width // len(active_algos) - 6)
        spacing = (chart_width - bar_width * len(active_algos)) // (len(active_algos) + 1)
        max_bar_height = height - 2 * margin - 20
        
        # 绘制背景网格（更明显）
        for i in range(6):
            y = height - margin - (i / 5) * max_bar_height
            canvas.create_line(margin, y, width - margin, y, 
                              fill='#2a2a3e', width=1)
        
        # 绘制坐标轴（更粗更明显）
        # X轴
        canvas.create_line(margin, height - margin, width - margin, height - margin, 
                          fill='#ffffff', width=2)
        canvas.create_text(width//2, height - 5, text="AI算法", 
                          fill='#ffffff', font=('Arial', 9))
        
        # Y轴
        canvas.create_line(margin, margin, margin, height - margin, 
                          fill='#ffffff', width=2)
        canvas.create_text(10, height//2, text="成功率(%)", 
                          fill='#ffffff', font=('Arial', 9), angle=90)
        
        # Y轴刻度值（更明显）
        for i in range(6):
            y = height - margin - (i / 5) * max_bar_height
            canvas.create_text(margin - 5, y, text=f"{i*20}", 
                              fill='#ffffff', font=('Arial', 8), anchor='e')
        
        algo_cn = {
            'Q-Learning': 'Q学习 (Q-Learning)', 'SARSA': 'SARSA (SARSA)', 'Greedy': '贪心 (Greedy)', 
            'Random': '随机 (Random)', 'DQN': '深度Q (DQN)', 'AStar': 'A* (AStar)', 
            'MCTS': '蒙特卡洛 (MCTS)', 'Minimax': '极小极大 (Minimax)',
            'HeuristicBFS': '启发式 (HeuristicBFS)', 'Hybrid': '混合 (Hybrid)'
        }
        
        for i, algo_name in enumerate(active_algos):
            algo = self.ai_algorithms[algo_name]
            total = algo['food'] + algo['collision']
            
            if total == 0:
                rate = 0
            else:
                rate = (algo['food'] / total) * 100
            
            # 计算柱状图位置和尺寸
            x = margin + spacing + i * (bar_width + spacing)
            bar_height = (rate / 100) * max_bar_height
            y = height - margin - bar_height
            
            # 绘制柱状图
            canvas.create_rectangle(x, y, x + bar_width, height - margin,
                                   fill=algo['color'], outline='#ffffff', width=2)
            
            # 绘制数值标签（在柱状图上方）
            canvas.create_text(x + bar_width//2, y - 8, 
                              text=f"{rate:.0f}%", fill='#ffffff', font=('Arial', 10, 'bold'))
            
            # 绘制AI名称标签（在柱状图下方）
            canvas.create_text(x + bar_width//2, height - margin + 12, 
                              text=algo_cn.get(algo_name, algo_name), fill=algo['color'], font=('Arial', 9, 'bold'))
            
            # 绘制成功/失败计数
            canvas.create_text(x + bar_width//2, height - margin + 26, 
                              text=f"胜:{algo['food']} 负:{algo['collision']}", fill='#cccccc', font=('Arial', 7))
        
        # 添加中文说明
        canvas.create_text(width//2, 8, text="胜率=胜/(胜+负)", 
                          fill='#4caf50', font=('Arial', 7))
                               
    def draw_score_chart(self):
        """绘制得分对比图"""
        canvas = self.ai_charts["score"]
        canvas.delete("all")
        
        # 获取Canvas实际大小
        canvas.update_idletasks()
        width = max(canvas.winfo_width(), 100)
        height = max(canvas.winfo_height(), 80)
        margin = int(min(width, height) * 0.15)
        
        active_algos = [a for a in self.ai_algorithms if self.ai_algorithms[a]['active']]
        if not active_algos:
            canvas.create_text(width//2, height//2, text="暂无激活的AI", fill='#ffffff', font=('Arial', 12))
            return
        
        # 获取最大分数用于归一化
        max_score = max([self.ai_algorithms[a]['score'] for a in active_algos], default=100)
        max_score = max(max_score, 100)  # 至少100
        
        # 计算柱状图布局
        chart_width = width - 2 * margin
        bar_width = min(35, chart_width // len(active_algos) - 6)
        spacing = (chart_width - bar_width * len(active_algos)) // (len(active_algos) + 1)
        max_bar_height = height - 2 * margin - 20
        
        # 绘制网格
        for i in range(6):
            y = height - margin - (i / 5) * max_bar_height
            canvas.create_line(margin, y, width - margin, y, fill='#2a2a3e', width=1)
        
        # 坐标轴
        canvas.create_line(margin, height - margin, width - margin, height - margin, fill='#ffffff', width=2)
        canvas.create_text(width//2, height - 5, text="AI算法", fill='#ffffff', font=('Arial', 9))
        canvas.create_line(margin, margin, margin, height - margin, fill='#ffffff', width=2)
        canvas.create_text(10, height//2, text="得分", fill='#ffffff', font=('Arial', 9), angle=90)
        
        # 刻度
        for i in range(6):
            y = height - margin - (i / 5) * max_bar_height
            val = int(max_score * i / 5)
            canvas.create_text(margin - 5, y, text=f"{val}", fill='#ffffff', font=('Arial', 8), anchor='e')
        
        algo_cn = {
            'Q-Learning': 'Q学习 (Q-Learning)', 'SARSA': 'SARSA (SARSA)', 'Greedy': '贪心 (Greedy)', 
            'Random': '随机 (Random)', 'DQN': '深度Q (DQN)', 'AStar': 'A* (AStar)', 
            'MCTS': '蒙特卡洛 (MCTS)', 'Minimax': '极小极大 (Minimax)',
            'HeuristicBFS': '启发式 (HeuristicBFS)', 'Hybrid': '混合 (Hybrid)'
        }
        
        for i, algo_name in enumerate(active_algos):
            algo = self.ai_algorithms[algo_name]
            score = algo['score']
            
            x = margin + spacing + i * (bar_width + spacing)
            bar_height = (score / max_score) * max_bar_height
            y = height - margin - bar_height
            
            canvas.create_rectangle(x, y, x + bar_width, height - margin,
                                   fill=algo['color'], outline='#ffffff', width=2)
            canvas.create_text(x + bar_width//2, y - 8, text=f"{score}", 
                              fill='#ffffff', font=('Arial', 10, 'bold'))
            canvas.create_text(x + bar_width//2, height - margin + 12, 
                              text=algo_cn.get(algo_name, algo_name), fill=algo['color'], font=('Arial', 9, 'bold'))
        
        canvas.create_text(width//2, 8, text="累计得分", fill='#4caf50', font=('Arial', 7))
                               
    def draw_trade_count_chart(self):
        """绘制交易次数图"""
        canvas = self.ai_charts["trade_count"]
        canvas.delete("all")
        
        # 获取Canvas实际大小
        canvas.update_idletasks()
        width = max(canvas.winfo_width(), 100)
        height = max(canvas.winfo_height(), 80)
        margin = int(min(width, height) * 0.15)
        
        active_algos = [a for a in self.ai_algorithms if self.ai_algorithms[a]['active']]
        if not active_algos:
            canvas.create_text(width//2, height//2, text="暂无激活的AI", fill='#ffffff', font=('Arial', 12))
            return
        
        # 获取最大交易次数
        max_trades = max([self.ai_algorithms[a]['food'] + self.ai_algorithms[a]['collision'] for a in active_algos], default=10)
        max_trades = max(max_trades, 10)
        
        chart_width = width - 2 * margin
        bar_width = min(35, chart_width // len(active_algos) - 6)
        spacing = (chart_width - bar_width * len(active_algos)) // (len(active_algos) + 1)
        max_bar_height = height - 2 * margin - 20
        
        for i in range(6):
            y = height - margin - (i / 5) * max_bar_height
            canvas.create_line(margin, y, width - margin, y, fill='#2a2a3e', width=1)
        
        canvas.create_line(margin, height - margin, width - margin, height - margin, fill='#ffffff', width=2)
        canvas.create_text(width//2, height - 5, text="AI算法", fill='#ffffff', font=('Arial', 9))
        canvas.create_line(margin, margin, margin, height - margin, fill='#ffffff', width=2)
        canvas.create_text(10, height//2, text="次数", fill='#ffffff', font=('Arial', 9), angle=90)
        
        for i in range(6):
            y = height - margin - (i / 5) * max_bar_height
            val = int(max_trades * i / 5)
            canvas.create_text(margin - 5, y, text=f"{val}", fill='#ffffff', font=('Arial', 8), anchor='e')
        
        algo_cn = {
            'Q-Learning': 'Q学习 (Q-Learning)', 'SARSA': 'SARSA (SARSA)', 'Greedy': '贪心 (Greedy)', 
            'Random': '随机 (Random)', 'DQN': '深度Q (DQN)', 'AStar': 'A* (AStar)', 
            'MCTS': '蒙特卡洛 (MCTS)', 'Minimax': '极小极大 (Minimax)',
            'HeuristicBFS': '启发式 (HeuristicBFS)', 'Hybrid': '混合 (Hybrid)'
        }
        
        for i, algo_name in enumerate(active_algos):
            algo = self.ai_algorithms[algo_name]
            trades = algo['food'] + algo['collision']
            
            x = margin + spacing + i * (bar_width + spacing)
            bar_height = (trades / max_trades) * max_bar_height
            y = height - margin - bar_height
            
            canvas.create_rectangle(x, y, x + bar_width, height - margin,
                                   fill=algo['color'], outline='#ffffff', width=2)
            canvas.create_text(x + bar_width//2, y - 8, text=f"{trades}", 
                              fill='#ffffff', font=('Arial', 10, 'bold'))
            canvas.create_text(x + bar_width//2, height - margin + 12, 
                              text=algo_cn.get(algo_name, algo_name), fill=algo['color'], font=('Arial', 9, 'bold'))
        
        canvas.create_text(width//2, 8, text="交易次数=胜+负", fill='#4caf50', font=('Arial', 7))
                               
    def draw_learning_eff_chart(self):
        """绘制学习效率图"""
        canvas = self.ai_charts["learning_eff"]
        canvas.delete("all")
        
        # 获取Canvas实际大小
        canvas.update_idletasks()
        width = max(canvas.winfo_width(), 100)
        height = max(canvas.winfo_height(), 80)
        margin = int(min(width, height) * 0.15)
        
        active_algos = [a for a in self.ai_algorithms if self.ai_algorithms[a]['active']]
        if not active_algos:
            canvas.create_text(width//2, height//2, text="暂无激活的AI", fill='#ffffff', font=('Arial', 12))
            return
        
        # 计算学习效率 = Q表大小 / (交易次数 + 1)
        efficiencies = []
        for algo_name in active_algos:
            algo = self.ai_algorithms[algo_name]
            trades = algo['food'] + algo['collision']
            q_size = len(algo.get('q_table', {}))
            efficiency = q_size / max(trades, 1) if algo_name in ['Q-Learning', 'SARSA'] else 0
            efficiencies.append((algo_name, efficiency))
        
        max_eff = max([e[1] for e in efficiencies], default=1)
        max_eff = max(max_eff, 1)
        
        chart_width = width - 2 * margin
        bar_width = min(35, chart_width // len(active_algos) - 6)
        spacing = (chart_width - bar_width * len(active_algos)) // (len(active_algos) + 1)
        max_bar_height = height - 2 * margin - 20
        
        for i in range(6):
            y = height - margin - (i / 5) * max_bar_height
            canvas.create_line(margin, y, width - margin, y, fill='#2a2a3e', width=1)
        
        canvas.create_line(margin, height - margin, width - margin, height - margin, fill='#ffffff', width=2)
        canvas.create_text(width//2, height - 5, text="AI算法", fill='#ffffff', font=('Arial', 9))
        canvas.create_line(margin, margin, margin, height - margin, fill='#ffffff', width=2)
        canvas.create_text(10, height//2, text="效率", fill='#ffffff', font=('Arial', 9), angle=90)
        
        for i in range(6):
            y = height - margin - (i / 5) * max_bar_height
            val = max_eff * i / 5
            canvas.create_text(margin - 5, y, text=f"{val:.1f}", fill='#ffffff', font=('Arial', 8), anchor='e')
        
        algo_cn = {
            'Q-Learning': 'Q学习 (Q-Learning)', 'SARSA': 'SARSA (SARSA)', 'Greedy': '贪心 (Greedy)', 
            'Random': '随机 (Random)', 'DQN': '深度Q (DQN)', 'AStar': 'A* (AStar)', 
            'MCTS': '蒙特卡洛 (MCTS)', 'Minimax': '极小极大 (Minimax)',
            'HeuristicBFS': '启发式 (HeuristicBFS)', 'Hybrid': '混合 (Hybrid)'
        }
        
        for i, (algo_name, eff) in enumerate(efficiencies):
            algo = self.ai_algorithms[algo_name]
            
            x = margin + spacing + i * (bar_width + spacing)
            bar_height = (eff / max_eff) * max_bar_height
            y = height - margin - bar_height
            
            canvas.create_rectangle(x, y, x + bar_width, height - margin,
                                   fill=algo['color'], outline='#ffffff', width=2)
            canvas.create_text(x + bar_width//2, y - 8, text=f"{eff:.1f}", 
                              fill='#ffffff', font=('Arial', 10, 'bold'))
            canvas.create_text(x + bar_width//2, height - margin + 12, 
                              text=algo_cn.get(algo_name, algo_name), fill=algo['color'], font=('Arial', 9, 'bold'))
        
        canvas.create_text(width//2, 8, text="学习效率=Q表/交易", fill='#4caf50', font=('Arial', 7))
                               
    def draw_overall_chart(self):
        """绘制综合排名图"""
        canvas = self.ai_charts["overall"]
        canvas.delete("all")
        
        # 获取Canvas实际大小
        canvas.update_idletasks()
        width = max(canvas.winfo_width(), 100)
        height = max(canvas.winfo_height(), 80)
        margin = int(min(width, height) * 0.15)
        
        active_algos = [a for a in self.ai_algorithms if self.ai_algorithms[a]['active']]
        if not active_algos:
            canvas.create_text(width//2, height//2, text="暂无激活的AI", fill='#ffffff', font=('Arial', 12))
            return
        
        # 计算综合分数
        scores = []
        for algo_name in active_algos:
            algo = self.ai_algorithms[algo_name]
            total = algo['food'] + algo['collision']
            success_rate = (algo['food'] / max(1, total)) * 100
            net_pnl = (algo['capital'] - 10000) / 10000 * 100  # 转换为百分比
            rank_score = (algo['capital'] / 10000) * 0.4 + (success_rate / 100) * 0.4 + net_pnl * 0.2
            scores.append((algo_name, rank_score))
        
        max_score = max([s[1] for s in scores], default=1)
        max_score = max(max_score, 1)
        
        chart_width = width - 2 * margin
        bar_width = min(35, chart_width // len(active_algos) - 6)
        spacing = (chart_width - bar_width * len(active_algos)) // (len(active_algos) + 1)
        max_bar_height = height - 2 * margin - 20
        
        for i in range(6):
            y = height - margin - (i / 5) * max_bar_height
            canvas.create_line(margin, y, width - margin, y, fill='#2a2a3e', width=1)
        
        canvas.create_line(margin, height - margin, width - margin, height - margin, fill='#ffffff', width=2)
        canvas.create_text(width//2, height - 5, text="AI算法", fill='#ffffff', font=('Arial', 9))
        canvas.create_line(margin, margin, margin, height - margin, fill='#ffffff', width=2)
        canvas.create_text(10, height//2, text="综合", fill='#ffffff', font=('Arial', 9), angle=90)
        
        for i in range(6):
            y = height - margin - (i / 5) * max_bar_height
            val = max_score * i / 5
            canvas.create_text(margin - 5, y, text=f"{val:.1f}", fill='#ffffff', font=('Arial', 8), anchor='e')
        
        algo_cn = {
            'Q-Learning': 'Q学习 (Q-Learning)', 'SARSA': 'SARSA (SARSA)', 'Greedy': '贪心 (Greedy)', 
            'Random': '随机 (Random)', 'DQN': '深度Q (DQN)', 'AStar': 'A* (AStar)', 
            'MCTS': '蒙特卡洛 (MCTS)', 'Minimax': '极小极大 (Minimax)',
            'HeuristicBFS': '启发式 (HeuristicBFS)', 'Hybrid': '混合 (Hybrid)'
        }
        
        for i, (algo_name, score) in enumerate(scores):
            algo = self.ai_algorithms[algo_name]
            
            x = margin + spacing + i * (bar_width + spacing)
            bar_height = (score / max_score) * max_bar_height
            y = height - margin - bar_height
            
            canvas.create_rectangle(x, y, x + bar_width, height - margin,
                                   fill=algo['color'], outline='#ffffff', width=2)
            canvas.create_text(x + bar_width//2, y - 8, text=f"{score:.2f}", 
                              fill='#ffffff', font=('Arial', 10, 'bold'))
            canvas.create_text(x + bar_width//2, height - margin + 12, 
                              text=algo_cn.get(algo_name, algo_name), fill=algo['color'], font=('Arial', 9, 'bold'))
        
        canvas.create_text(width//2, 8, text="综合=资金40%+胜率40%+分数20%", fill='#4caf50', font=('Arial', 7))
    
    def draw_capital_curve_chart(self):
        """绘制资金曲线（小图版本，用于AI对比图表）"""
        canvas = self.ai_charts["capital_curve"]
        canvas.delete("all")
        
        # 获取Canvas实际大小
        canvas.update_idletasks()
        width = max(canvas.winfo_width(), 100)
        height = max(canvas.winfo_height(), 80)
        margin = int(min(width, height) * 0.12)
        
        active_algos = [a for a in self.ai_algorithms if self.ai_algorithms[a]['active']]
        if not active_algos:
            canvas.create_text(width//2, height//2, text="暂无激活的AI", fill='#ffffff', font=('Arial', 12))
            return
        
        # 收集数据
        all_values = []
        for algo_name in active_algos:
            all_values.extend(list(self.capital_history[algo_name]))
            all_values.append(self.ai_algorithms[algo_name]['capital'])
        
        if not all_values:
            canvas.create_text(width//2, height//2, text="等待数据...", fill='#888888', font=('Arial', 12))
            return
        
        min_val = min(all_values)
        max_val = max(all_values)
        val_range = max_val - min_val if max_val != min_val else 1
        
        # 添加缓冲
        min_val = min_val * 0.95
        max_val = max_val * 1.05
        
        # 绘制网格
        for i in range(6):
            y = margin + i * (height - 2 * margin) // 5
            canvas.create_line(margin, y, width - margin, y, fill='#2a2a3e', width=1)
        
        # 坐标轴
        canvas.create_line(margin, height - margin, width - margin, height - margin, fill='#ffffff', width=2)
        canvas.create_text(width - margin, height - 5, text="时间", fill='#ffffff', font=('Arial', 8))
        canvas.create_line(margin, margin, margin, height - margin, fill='#ffffff', width=2)
        canvas.create_text(8, height//2, text="资金", fill='#ffffff', font=('Arial', 8), angle=90)
        
        # Y轴刻度
        for i in range(6):
            y = margin + i * (height - 2 * margin) // 5
            val = max_val - (i / 5) * (max_val - min_val)
            canvas.create_text(margin - 5, y, text=f"${val/1000:.1f}K", fill='#ffffff', font=('Arial', 7), anchor='e')
        
        algo_cn = {
            'Q-Learning': 'Q学习 (Q-Learning)', 'SARSA': 'SARSA (SARSA)', 'Greedy': '贪心 (Greedy)', 
            'Random': '随机 (Random)', 'DQN': '深度Q (DQN)', 'AStar': 'A* (AStar)', 
            'MCTS': '蒙特卡洛 (MCTS)', 'Minimax': '极小极大 (Minimax)',
            'HeuristicBFS': '启发式 (HeuristicBFS)', 'Hybrid': '混合 (Hybrid)'
        }
        
        # 绘制每条曲线
        for algo_name in active_algos:
            if not self.ai_algorithms[algo_name]['active']:
                continue
            
            data = list(self.capital_history[algo_name])
            if len(data) < 1:
                continue
            data = data + [self.ai_algorithms[algo_name]['capital']]
            
            color = self.ai_algorithms[algo_name]['color']
            points = []
            
            for i, val in enumerate(data):
                x_step = max(1, len(data) - 1) if len(data) > 1 else 1
                x = margin + i * (width - 2 * margin) // x_step
                y = height - margin - (val - min_val) / (max_val - min_val + 1) * (height - 2 * margin)
                points.extend([x, y])
            
            if len(points) >= 2:
                canvas.create_line(points, fill=color, width=2)
                # 终点标记
                canvas.create_oval(points[-2]-3, points[-1]-3, points[-2]+3, points[-1]+3, fill=color, outline='#ffffff')
        
        # 图例
        legend_y = height - 15
        for i, algo_name in enumerate(active_algos):
            if i > 3:
                break
            color = self.ai_algorithms[algo_name]['color']
            x = width - 150 + i * 70
            canvas.create_line(x, legend_y, x + 15, legend_y, fill=color, width=2)
            canvas.create_text(x + 20, legend_y, text=algo_cn.get(algo_name, algo_name)[:2], fill=color, font=('Arial', 7), anchor='w')
        
        canvas.create_text(width//2, 8, text="资金变化曲线", fill='#4caf50', font=('Arial', 7))
    
    def draw_multi_capital_chart(self):
        """绘制多条资金曲线对比"""
        canvas = self.capital_canvas
        canvas.delete("all")
        
        # 获取Canvas实际大小
        canvas.update_idletasks()
        width = max(canvas.winfo_width(), 200)
        height = max(canvas.winfo_height(), 150)
        margin = int(min(width, height) * 0.1)
        
        # 收集所有激活AI的资金历史
        active_algos = [a for a in self.ai_algorithms if self.ai_algorithms[a]['active']]
        if not active_algos:
            canvas.create_text(width//2, height//2, text="暂无激活的AI算法", fill='#666666', font=('Arial', 14))
            return
            
        # 检查是否有数据
        has_data = False
        for algo_name in active_algos:
            if len(self.capital_history[algo_name]) >= 1:
                has_data = True
                break
                
        if not has_data:
            canvas.create_text(width//2, height//2, text="等待数据中...", fill='#666666', font=('Arial', 14))
            return
            
        # 计算所有数据的范围
        all_values = []
        for algo_name in active_algos:
            all_values.extend(list(self.capital_history[algo_name]))
            # 添加当前资金
            all_values.append(self.ai_algorithms[algo_name]['capital'])
        
        if not all_values:
            return
            
        min_val = min(all_values)
        max_val = max(all_values)
        val_range = max_val - min_val if max_val != min_val else 1
        
        # 添加边距缓冲
        min_val = min_val * 0.95
        max_val = max_val * 1.05
        
        # 绘制背景网格线
        for i in range(6):
            y = margin + i * (height - 2 * margin) // 5
            canvas.create_line(margin, y, width - margin, y, fill='#1a1a2e', width=1, dash=(4, 4))
        
        # 绘制坐标轴
        # X轴
        canvas.create_line(margin, height - margin, width - margin, height - margin, 
                          fill='#ffffff', width=2)
        canvas.create_text(width//2, height - 15, text="时间 (帧数)", 
                          fill='#aaaaaa', font=('Arial', 10))
        
        # Y轴
        canvas.create_line(margin, margin, margin, height - margin, 
                          fill='#ffffff', width=2)
        canvas.create_text(15, height//2, text="资金 (美元)", 
                          fill='#aaaaaa', font=('Arial', 10), angle=90)
        
        # Y轴刻度值（5个刻度）
        for i in range(6):
            y = margin + i * (height - 2 * margin) // 5
            val = max_val - (i / 5) * (max_val - min_val)
            canvas.create_text(margin - 8, y, text=f"${val:,.0f}", 
                              fill='#888888', font=('Arial', 8), anchor='e')
        
        # 绘制每个AI的资金曲线
        max_history_len = max([len(self.capital_history[a]) for a in active_algos]) if active_algos else 0
        
        for algo_name in active_algos:
            if not self.ai_algorithms[algo_name]['active']:
                continue
                
            data = list(self.capital_history[algo_name])
            if len(data) < 1:
                continue
                
            # 添加当前资金作为最后一个点
            data = list(data) + [self.ai_algorithms[algo_name]['capital']]
            
            color = self.ai_algorithms[algo_name]['color']
            points = []
            
            for i, val in enumerate(data):
                x_step = max(1, len(data) - 1) if len(data) > 1 else 1
                x = margin + i * (width - 2 * margin) // x_step
                y = height - margin - (val - min_val) / (max_val - min_val + 1) * (height - 2 * margin)
                points.extend([x, y])
                
            if len(points) >= 2:
                # 绘制线条
                canvas.create_line(points, fill=color, width=2)
                # 绘制终点标记
                canvas.create_oval(points[-2]-4, points[-1]-4, points[-2]+4, points[-1]+4, fill=color, outline='#ffffff', width=1)
                
        # 图例（右上角）
        legend_x = width - 150
        legend_y = margin + 10
        algo_cn = {
            'Q-Learning': 'Q学习 (Q-Learning)', 'SARSA': 'SARSA (SARSA)', 'Greedy': '贪心 (Greedy)', 
            'Random': '随机 (Random)', 'DQN': '深度Q (DQN)', 'AStar': 'A* (AStar)', 
            'MCTS': '蒙特卡洛 (MCTS)', 'Minimax': '极小极大 (Minimax)',
            'HeuristicBFS': '启发式 (HeuristicBFS)', 'Hybrid': '混合 (Hybrid)'
        }
        for i, algo_name in enumerate(active_algos):
            color = self.ai_algorithms[algo_name]['color']
            canvas.create_line(legend_x, legend_y + i*22, legend_x + 25, legend_y + i*22, fill=color, width=3)
            canvas.create_text(legend_x + 32, legend_y + i*22, text=algo_cn.get(algo_name, algo_name), fill=color, anchor='w', font=('Arial', 8))
            capital = self.ai_algorithms[algo_name]['capital']
            canvas.create_text(legend_x + 32, legend_y + i*22 + 10, text=f"  ${capital:,.0f}", fill='#888888', anchor='w', font=('Arial', 7))
        
        # 标题
        canvas.create_text(width//2, 15, text="资金增长对比", fill='#ffffff', font=('Arial', 11, 'bold'))
        
        # 添加中文说明
        canvas.create_text(width//2, 32, text="实时显示各AI算法的资金变化曲线，曲线上方表示盈利能力强", 
                          fill='#4caf50', font=('Arial', 8))
                
    def update_performance_table(self):
        """更新性能统计表格 - 公平版本"""
        # 清空现有数据
        for item in self.performance_tree.get_children():
            self.performance_tree.delete(item)
        
        # 计算排名 - 公平公正
        algo_stats = []
        algo_cn = {
            'Q-Learning': 'Q学习 (Q-Learning)', 'SARSA': 'SARSA (SARSA)', 'Greedy': '贪心 (Greedy)', 
            'Random': '随机 (Random)', 'DQN': '深度Q (DQN)', 'AStar': 'A* (AStar)', 
            'MCTS': '蒙特卡洛 (MCTS)', 'Minimax': '极小极大 (Minimax)',
            'HeuristicBFS': '启发式 (HeuristicBFS)', 'Hybrid': '混合 (Hybrid)'
        }
        
        for algo_name in self.ai_algorithms:
            algo = self.ai_algorithms[algo_name]
            total = algo['food'] + algo['collision']
            success_rate = (algo['food'] / max(1, total)) * 100
            net_pnl = algo['capital'] - 10000
            
            # 公平排名：考虑资金、胜率、得分
            rank_score = (algo['capital'] / 10000) * 0.4 + (success_rate / 100) * 0.4 + (algo['score'] / 100) * 0.2
            
            wall_hits = algo.get('wall_hits', 0)
            
            algo_stats.append((algo_name, rank_score, {
                'capital': algo['capital'],
                'score': algo['score'],
                'success_rate': success_rate,
                'trades': total,
                'net_pnl': net_pnl,
                'wall_hits': wall_hits
            }))
        
        # 按排名分数排序
        algo_stats.sort(key=lambda x: x[1], reverse=True)
        
        # 插入数据
        for rank, (algo_name, _, stats) in enumerate(algo_stats, 1):
            wall_hits = stats.get('wall_hits', 0)
            self.performance_tree.insert('', 'end', values=(
                f"#{rank}",
                algo_cn.get(algo_name, algo_name),
                f"${stats['capital']:,.0f}",
                f"{stats['net_pnl']:+,.0f}",
                f"{stats['success_rate']:.1f}%",
                stats['trades'],
                wall_hits
            ))
            
    def update_current_ai_display(self):
        """更新当前AI状态显示"""
        algo = self.ai_algorithms[self.selected_algorithm]
        for name, (var, func) in self.current_ai_labels.items():
            try:
                var.set(func())
            except:
                var.set("N/A")
                
    def update_all_ai_display(self):
        """更新所有AI的显示"""
        for algo_name in self.ai_algorithms:
            algo = self.ai_algorithms[algo_name]
            net_pnl = algo['capital'] - 10000
            pnl_text = f"${algo['capital']:,.0f} ({net_pnl:+,.0f})"
            
            if algo_name in self.all_ai_labels:
                self.all_ai_labels[algo_name].set(pnl_text)
                
            if algo_name in self.capital_stats_labels:
                self.capital_stats_labels[algo_name].set(pnl_text)
        
        # 更新状态栏
        if self.game_running:
            if self.game_paused:
                self.status_label.set("⏸ 已暂停")
            else:
                elapsed = self.game_time * 150 / 1000  # 约等于秒数
                active_count = len([a for a in self.ai_algorithms if self.ai_algorithms[a]['active']])
                self.status_label.set(f"▶ 运行中 ({elapsed:.1f}秒) | {active_count}个AI")
                
    def generate_food(self):
        while True:
            x = random.randint(0, self.grid_size - 1)
            y = random.randint(0, self.grid_size - 1)
            # 检查是否在任何蛇身上
            in_snake = False
            for instance in self.game_instances.values():
                if (x, y) in instance['snake']:
                    in_snake = True
                    break
            if not in_snake:
                self.food = (x, y)
                break
                
    def move_all_instances(self):
        """移动所有AI的游戏实例 - 公平版本"""
        for algo_name, instance in self.game_instances.items():
            if not self.ai_algorithms[algo_name]['active']:
                continue
            
            # 确保每个AI有食物
            if algo_name not in self.ai_foods:
                self.ai_foods[algo_name] = self._generate_individual_food(algo_name)
            
            # 获取AI决策
            instance['direction'] = self.get_ai_decision(instance)
            
            # 计算新位置（检测墙壁碰撞）
            head = instance['snake'][-1]
            dx = instance['direction'][0]
            dy = instance['direction'][1]
            
            # 检测是否撞墙
            wall_collision = False
            new_x = head[0] + dx
            new_y = head[1] + dy
            
            if new_x < 0 or new_x >= self.grid_size or new_y < 0 or new_y >= self.grid_size:
                wall_collision = True
            
            if wall_collision:
                # 撞墙惩罚 - 公平公正
                wall_penalty = 800  # 比自撞轻
                self.ai_algorithms[algo_name]['capital'] = max(0, self.ai_algorithms[algo_name]['capital'] - wall_penalty)
                self.ai_algorithms[algo_name]['score'] -= 3
                self.ai_algorithms[algo_name]['wall_hits'] = self.ai_algorithms[algo_name].get('wall_hits', 0) + 1
                
                # 随机传送到安全位置
                safe_pos = self._find_safe_position()
                instance['snake'].clear()
                instance['snake'].append(safe_pos)
                
                # 随机新方向
                directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
                instance['direction'] = random.choice(directions)
                
                algo_display = {
                    'Q-Learning': 'Q学习 (Q-Learning)', 'SARSA': 'SARSA (SARSA)', 'Greedy': '贪心 (Greedy)', 
                    'Random': '随机 (Random)', 'DQN': '深度Q (DQN)', 'AStar': 'A* (AStar)', 
                    'MCTS': '蒙特卡洛 (MCTS)', 'Minimax': '极小极大 (Minimax)',
                    'HeuristicBFS': '启发式 (HeuristicBFS)', 'Hybrid': '混合 (Hybrid)'
                }
                self.add_message(f"🚧 {algo_display.get(algo_name, algo_name)} 撞墙! 传送扣${wall_penalty}")
                
                # 记录历史
                self.capital_history[algo_name].append(self.ai_algorithms[algo_name]['capital'])
                continue
            
            new_head = (new_x, new_y)
            
            # 检查碰撞
            if new_head in instance['snake']:
                self.handle_instance_collision(algo_name, instance)
                continue
            
            instance['snake'].append(new_head)
            
            # 检查食物（使用AI自己的食物）
            food = self.ai_foods.get(algo_name)
            if new_head == food:
                self.handle_instance_eat_food(algo_name, instance)
            else:
                instance['snake'].popleft()
    
    def _find_safe_position(self):
        """找到安全位置（不与任何AI的蛇身重叠）"""
        for _ in range(100):
            x = random.randint(0, self.grid_size - 1)
            y = random.randint(0, self.grid_size - 1)
            pos = (x, y)
            
            safe = True
            for algo_name, instance in self.game_instances.items():
                if pos in instance['snake']:
                    safe = False
                    break
            
            if safe:
                return pos
        
        return (10, 10)  # 默认位置
                
    def handle_instance_collision(self, algo_name, instance):
        """处理实例碰撞 - 公平版本"""
        loss = 1500
        self.ai_algorithms[algo_name]['capital'] -= loss
        self.ai_algorithms[algo_name]['collision'] += 1
        self.ai_algorithms[algo_name]['score'] -= 5
        
        # 重置位置
        instance['snake'].clear()
        instance['snake'].append((10, 10))
        
        # 确保食物存在
        if algo_name not in self.ai_foods:
            self.ai_foods[algo_name] = self._generate_individual_food(algo_name)
        
        # 更新Q表（使用AI自己的食物）
        if algo_name in ['Q-Learning', 'SARSA']:
            head = (10, 10)
            food_pos = self.ai_foods.get(algo_name, (10, 10))
            state = (food_pos[0] - head[0], food_pos[1] - head[1], instance['direction'])
            directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
            action = directions.index(instance['direction']) if instance['direction'] in directions else 0
            self.update_ai_q_table(algo_name, -10, state, action)
        
        algo_display = {'Q-Learning': 'Q学习', 'SARSA': 'SARSA', 'Greedy': '贪心', 'Random': '随机',
                        'DQN': '深度Q', 'AStar': 'A*', 'MCTS': '蒙特卡洛', 'Minimax': '极小极大',
                        'HeuristicBFS': '启发式', 'Hybrid': '混合'}
        self.add_message(f"💥 {algo_display.get(algo_name, algo_name)} 碰撞! 损失 ${loss}")
        
        # 记录碰撞后的资金历史
        self.capital_history[algo_name].append(self.ai_algorithms[algo_name]['capital'])
        self.score_history[algo_name].append(self.ai_algorithms[algo_name]['score'])
        
        # 重置后重新生成食物
        self.ai_foods[algo_name] = self._generate_individual_food(algo_name)
        self.score_history[algo_name].append(self.ai_algorithms[algo_name]['score'])
        
        if self.ai_algorithms[algo_name]['capital'] <= 0:
            self.ai_algorithms[algo_name]['active'] = False
            self.add_message(f"☠️ {algo_name} 资金耗尽，已禁用")
            
    def handle_instance_eat_food(self, algo_name, instance):
        """处理实例吃到食物 - 公平版本"""
        food_types = [
            {"name": "盈利", "amount": 1500},
            {"name": "亏损", "amount": -1200},
            {"name": "突破", "amount": 2000},
            {"name": "反转", "amount": 1800}
        ]
        
        food = random.choice(food_types)
        amount = food['amount']
        
        self.ai_algorithms[algo_name]['capital'] += amount
        self.ai_algorithms[algo_name]['score'] += 10 if amount > 0 else -5
        
        if amount > 0:
            self.ai_algorithms[algo_name]['food'] += 1
            self.winning_trades[algo_name] += 1
            self.total_profit[algo_name] += amount
        else:
            self.losing_trades[algo_name] += 1
            self.total_loss[algo_name] += abs(amount)
        
        # 更新Q表（使用AI自己的食物位置）
        if algo_name in ['Q-Learning', 'SARSA'] and amount > 0:
            head = instance['snake'][-1]
            food_pos = self.ai_foods.get(algo_name, (10, 10))
            state = (food_pos[0] - head[0], food_pos[1] - head[1], instance['direction'])
            directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
            action = directions.index(instance['direction']) if instance['direction'] in directions else 0
            self.update_ai_q_table(algo_name, 10, state, action)
        
        # 为该AI生成新的食物（独立生成，互不影响）
        self.ai_foods[algo_name] = self._generate_individual_food(algo_name)
        
        emoji = "💰" if amount > 0 else "📉"
        algo_display = {'Q-Learning': 'Q学习', 'SARSA': 'SARSA', 'Greedy': '贪心', 'Random': '随机',
                        'DQN': '深度Q', 'AStar': 'A*', 'MCTS': '蒙特卡洛', 'Minimax': '极小极大',
                        'HeuristicBFS': '启发式', 'Hybrid': '混合'}
        self.add_message(f"{emoji} {algo_display.get(algo_name, algo_name)} {food['name']}: ${amount:+}")
        
        # 记录历史
        self.capital_history[algo_name].append(self.ai_algorithms[algo_name]['capital'])
        self.score_history[algo_name].append(self.ai_algorithms[algo_name]['score'])
        
    def add_message(self, message):
        """添加消息"""
        timestamp = time.strftime("%H:%M:%S")
        formatted = f"[{timestamp}] {message}"
        
        self.message_log.append(formatted)
        if len(self.message_log) > self.max_messages:
            self.message_log.pop(0)
            
        self.msg_text.delete(1.0, tk.END)
        for msg in self.message_log:
            self.msg_text.insert(tk.END, msg + '\n')
        self.msg_text.see(tk.END)
        
    def game_loop(self):
        """游戏主循环"""
        if not self.game_running or self.game_paused:
            return
            
        self.game_time += 1
        
        # 随机改变或消失食物
        self.randomize_food()
        
        # 移动所有实例
        self.move_all_instances()
        
        # 绘制当前选中的AI
        self.draw_game()
        
        # 定期记录资金历史（每5帧记录一次，使图表更平滑）
        if self.game_time % 5 == 0:
            for algo_name in self.active_algorithms:
                if self.ai_algorithms[algo_name]['active']:
                    current_capital = self.ai_algorithms[algo_name]['capital']
                    current_score = self.ai_algorithms[algo_name]['score']
                    # 记录当前资金
                    self.capital_history[algo_name].append(current_capital)
                    self.score_history[algo_name].append(current_score)
        
        # 更新显示
        if self.game_time % 10 == 0:
            self.update_current_ai_display()
            self.update_all_ai_display()
            self.update_food_info_display()
            self.draw_ai_comparison_charts()
            
        self.root.after(self.game_speed, self.game_loop)
        
    def start_game(self):
        """开始游戏"""
        self.game_running = True
        self.game_paused = False
        
        # 初始化所有激活的AI实例
        self.initialize_game_instances()
        
        self.start_btn.config(state='disabled')
        self.pause_btn.config(state='normal')
        
        active_count = len([a for a in self.ai_algorithms if self.ai_algorithms[a]['active']])
        self.add_message(f"🚀 启动图表AI对比版！同时运行 {active_count} 个AI算法")
        
        self.game_loop()
        
    def toggle_pause(self):
        """暂停/继续"""
        self.game_paused = not self.game_paused
        if self.game_paused:
            self.pause_btn.config(text="▶ 继续")
            self.add_message("⏸ 游戏暂停")
        else:
            self.pause_btn.config(text="⏸ 暂停")
            self.add_message("▶ 游戏继续")
            self.game_loop()
            
    def reset_game(self):
        """重置游戏"""
        self.game_running = False
        self.game_paused = False
        
        # 重置所有AI状态
        for algo_name in self.ai_algorithms:
            algo = self.ai_algorithms[algo_name]
            algo['capital'] = 10000
            algo['score'] = 0
            algo['food'] = 0
            algo['collision'] = 0
            if 'q_table' in algo:
                algo['q_table'].clear()
                
        # 清空历史
        self.capital_history.clear()
        self.score_history.clear()
        self.game_instances.clear()
        
        # 重置UI
        self.start_btn.config(state='normal')
        self.pause_btn.config(state='disabled', text="⏸ 暂停")
        
        # 清空图表
        if hasattr(self, 'ai_charts'):
            for canvas in self.ai_charts.values():
                try:
                    canvas.delete("all")
                except Exception:
                    pass
        if hasattr(self, 'capital_canvas'):
            try:
                self.capital_canvas.delete("all")
            except Exception:
                pass
        
        # 清空表格
        if hasattr(self, 'performance_tree'):
            for item in self.performance_tree.get_children():
                self.performance_tree.delete(item)
            
        self.msg_text.delete(1.0, tk.END)
        
        self.add_message("🔄 游戏已重置，所有AI状态清零")
        
    def bind_keys(self):
        """绑定键盘事件"""
        self.root.bind('<space>', lambda e: self.toggle_pause())
        self.root.bind('<Escape>', lambda e: self.quit_game())
        # 窗口大小变化时重新绘制图表
        self.root.bind('<Configure>', self.on_window_resize)
        
    def on_window_resize(self, event=None):
        """窗口大小变化事件"""
        # 防抖动：只在游戏运行时重新绘制图表
        if self.game_running and not self.game_paused:
            # 使用after延迟绘制，避免频繁重绘
            if hasattr(self, '_resize_job') and self._resize_job:
                self.root.after_cancel(self._resize_job)
            self._resize_job = self.root.after(100, self.redraw_charts)
    
    def redraw_charts(self):
        """重新绘制所有图表"""
        if self.game_running:
            try:
                self.draw_ai_comparison_charts()
            except Exception:
                pass
        
    def quit_game(self):
        if self.game_running:
            if messagebox.askokcancel("退出", "确定要退出游戏吗？"):
                self.root.quit()
        else:
            self.root.quit()
            
if __name__ == "__main__":
    try:
        root = tk.Tk()
        game = ChartAIComparisonSnake(root)
        root.mainloop()
    except Exception as e:
        print(f"游戏启动失败: {e}")
        import traceback
        traceback.print_exc()
        input("按回车键退出...")
