#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
量化交易贪吃蛇游戏 - AI算法对比版
AI Algorithm Comparison Version
"""

import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
import math
from collections import deque, defaultdict
import threading
import copy

class AIAlgorithmComparisonSnake:
    def __init__(self, root):
        self.root = root
        self.root.title("🐍 量化交易贪吃蛇 - AI算法对比版")
        self.root.configure(bg='#0a0a0f')
        self.root.geometry("1600x1000")
        
        # 性能参数
        self.max_history_points = 100
        self.chart_update_interval = 500
        
        # 游戏核心参数
        self.canvas_width = 600
        self.canvas_height = 600
        self.grid_size = 20
        self.cell_size = self.canvas_width // self.grid_size
        
        # AI算法定义
        self.ai_algorithms = {
            'Q-Learning': {
                'name': 'Q-Learning',
                'color': '#4caf50',
                'q_table': {},
                'epsilon': 0.1,
                'learning_rate': 0.1,
                'discount_factor': 0.9,
                'strategy': 'q_learning'
            },
            'SARSA': {
                'name': 'SARSA',
                'color': '#2196f3',
                'q_table': {},
                'epsilon': 0.15,
                'learning_rate': 0.15,
                'discount_factor': 0.85,
                'strategy': 'sarsa'
            },
            'Deep Q': {
                'name': 'Deep Q Network',
                'color': '#ff9800',
                'experience_buffer': deque(maxlen=1000),
                'epsilon': 0.2,
                'learning_rate': 0.01,
                'discount_factor': 0.95,
                'strategy': 'deep_q'
            },
            'Random': {
                'name': 'Random Baseline',
                'color': '#9c27b0',
                'strategy': 'random'
            },
            'Greedy': {
                'name': 'Greedy',
                'color': '#f44336',
                'strategy': 'greedy'
            }
        }
        
        # 当前选中的算法
        self.current_algorithm = 'Q-Learning'
        self.comparison_mode = False
        self.comparison_algorithms = ['Q-Learning', 'SARSA']
        
        # 游戏状态
        self.game_instances = {}
        self.game_running = False
        self.game_paused = False
        self.game_speed = 150
        self.global_game_time = 0
        
        # 性能跟踪
        self.algorithm_performance = {}
        self.comparison_history = {}
        
        # 初始化性能跟踪
        for algo_name in self.ai_algorithms:
            self.algorithm_performance[algo_name] = {
                'food_collected': 0,
                'collisions': 0,
                'total_score': 0,
                'total_capital': 10000,
                'success_rate': 0,
                'avg_reward': 0,
                'q_table_size': 0
            }
            
        # 创建UI
        self.setup_ui()
        self.bind_keys()
        
    def setup_ui(self):
        """设置用户界面"""
        main_container = tk.Frame(self.root, bg='#0a0a0f')
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 顶部控制面板
        self.create_control_panel(main_container)
        
        # 中间内容区域
        content_frame = tk.Frame(main_container, bg='#0a0a0f')
        content_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # 左侧游戏区域
        game_frame = tk.Frame(content_frame, bg='#1a1a2e', relief=tk.RAISED, bd=2)
        game_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)
        
        self.setup_game_area(game_frame)
        
        # 右侧对比区域
        comparison_frame = tk.Frame(content_frame, bg='#1a1a2e', relief=tk.RAISED, bd=2)
        comparison_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        self.setup_comparison_area(comparison_frame)
        
    def create_control_panel(self, parent):
        """创建控制面板"""
        control_frame = tk.Frame(parent, bg='#1a1a2e', relief=tk.RAISED, bd=2)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 算法选择
        algo_frame = tk.Frame(control_frame, bg='#1a1a2e')
        algo_frame.pack(side=tk.LEFT, padx=10, pady=10)
        
        tk.Label(algo_frame, text="AI算法选择:", font=('Arial', 10, 'bold'),
                bg='#1a1a2e', fg='#ffffff').pack(side=tk.LEFT, padx=5)
        
        self.algorithm_var = tk.StringVar(value=self.current_algorithm)
        self.algorithm_combo = ttk.Combobox(algo_frame, textvariable=self.algorithm_var,
                                           values=list(self.ai_algorithms.keys()),
                                           state='readonly', width=15)
        self.algorithm_combo.pack(side=tk.LEFT, padx=5)
        self.algorithm_combo.bind('<<ComboboxSelected>>', self.on_algorithm_change)
        
        # 对比模式
        comparison_frame = tk.Frame(control_frame, bg='#1a1a2e')
        comparison_frame.pack(side=tk.LEFT, padx=10, pady=10)
        
        self.comparison_var = tk.BooleanVar(value=False)
        self.comparison_check = tk.Checkbutton(comparison_frame, text="对比模式",
                                              variable=self.comparison_var,
                                              command=self.toggle_comparison_mode,
                                              bg='#1a1a2e', fg='#ffffff',
                                              selectcolor='#1a1a2e',
                                              font=('Arial', 10, 'bold'))
        self.comparison_check.pack(side=tk.LEFT, padx=5)
        
        # 对比算法选择
        self.comparison_algo_frame = tk.Frame(comparison_frame, bg='#1a1a2e')
        
        tk.Label(self.comparison_algo_frame, text="对比算法:", font=('Arial', 10, 'bold'),
                bg='#1a1a2e', fg='#ffffff').pack(side=tk.LEFT, padx=5)
        
        self.comparison_var1 = tk.StringVar(value='Q-Learning')
        self.comparison_combo1 = ttk.Combobox(self.comparison_algo_frame, textvariable=self.comparison_var1,
                                            values=list(self.ai_algorithms.keys()),
                                            state='readonly', width=12)
        self.comparison_combo1.pack(side=tk.LEFT, padx=3)
        
        tk.Label(self.comparison_algo_frame, text="vs", font=('Arial', 10, 'bold'),
                bg='#1a1a2e', fg='#ffffff').pack(side=tk.LEFT, padx=3)
        
        self.comparison_var2 = tk.StringVar(value='SARSA')
        self.comparison_combo2 = ttk.Combobox(self.comparison_algo_frame, textvariable=self.comparison_var2,
                                            values=list(self.ai_algorithms.keys()),
                                            state='readonly', width=12)
        self.comparison_combo2.pack(side=tk.LEFT, padx=3)
        
        # 游戏控制按钮
        button_frame = tk.Frame(control_frame, bg='#1a1a2e')
        button_frame.pack(side=tk.RIGHT, padx=10, pady=10)
        
        self.start_button = tk.Button(button_frame, text="🎮 开始", command=self.start_game,
                                     bg='#4caf50', fg='white', font=('Arial', 10, 'bold'), width=10)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.pause_button = tk.Button(button_frame, text="⏸️ 暂停", command=self.toggle_pause,
                                     bg='#ff9800', fg='white', font=('Arial', 10, 'bold'), width=10, state='disabled')
        self.pause_button.pack(side=tk.LEFT, padx=5)
        
        self.reset_button = tk.Button(button_frame, text="🔄 重置", command=self.reset_game,
                                     bg='#f44336', fg='white', font=('Arial', 10, 'bold'), width=10)
        self.reset_button.pack(side=tk.LEFT, padx=5)
        
    def setup_game_area(self, parent):
        """设置游戏区域"""
        # 标题
        tk.Label(parent, text="🎮 游戏区域", font=('Arial', 12, 'bold'),
                bg='#1a1a2e', fg='#ffffff').pack(pady=10)
        
        # 游戏画布
        self.canvas = tk.Canvas(parent, width=self.canvas_width, height=self.canvas_height,
                               bg='#0a0a0f', highlightthickness=2, highlightbackground='#4a4a6e')
        self.canvas.pack(padx=10, pady=10)
        
        # 状态显示
        self.game_status_frame = tk.Frame(parent, bg='#1a1a2e')
        self.game_status_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.current_algo_label = tk.Label(self.game_status_frame, 
                                          text=f"当前算法: {self.current_algorithm}",
                                          font=('Arial', 10, 'bold'),
                                          bg='#1a1a2e', fg='#4caf50')
        self.current_algo_label.pack()
        
        self.game_info_label = tk.Label(self.game_status_frame, text="准备就绪",
                                       font=('Arial', 10),
                                       bg='#1a1a2e', fg='#00ff00')
        self.game_info_label.pack(pady=5)
        
    def setup_comparison_area(self, parent):
        """设置对比区域"""
        # 标题
        tk.Label(parent, text="📊 算法性能对比", font=('Arial', 12, 'bold'),
                bg='#1a1a2e', fg='#ffffff').pack(pady=10)
        
        # 性能对比表格
        self.create_performance_table(parent)
        
        # 实时对比图表
        self.create_comparison_charts(parent)
        
        # 算法配置面板
        self.create_algorithm_config_panel(parent)
        
    def create_performance_table(self, parent):
        """创建性能对比表格"""
        table_frame = tk.LabelFrame(parent, text="📈 性能指标对比", 
                                   bg='#1a1a2e', fg='#ffffff', font=('Arial', 10, 'bold'))
        table_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # 创建Treeview表格
        columns = ('Algorithm', 'Score', 'Success Rate', 'Avg Reward', 'Q-Table Size')
        self.performance_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=6)
        
        # 设置列标题
        for col in columns:
            self.performance_tree.heading(col, text=col)
            if col == 'Algorithm':
                self.performance_tree.column(col, width=120)
            else:
                self.performance_tree.column(col, width=100)
                
        self.performance_tree.pack(padx=5, pady=5)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.performance_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.performance_tree.config(yscrollcommand=scrollbar.set)
        
    def create_comparison_charts(self, parent):
        """创建对比图表"""
        chart_frame = tk.LabelFrame(parent, text="📊 实时性能图表", 
                                   bg='#1a1a2e', fg='#ffffff', font=('Arial', 10, 'bold'))
        chart_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # 成功率对比图
        self.comparison_canvas = tk.Canvas(chart_frame, width=600, height=200,
                                          bg='#0a0a0f', highlightthickness=1,
                                          highlightbackground='#4a4a6e')
        self.comparison_canvas.pack(padx=5, pady=5)
        
    def create_algorithm_config_panel(self, parent):
        """创建算法配置面板"""
        config_frame = tk.LabelFrame(parent, text="⚙️ 算法参数配置", 
                                    bg='#1a1a2e', fg='#ffffff', font=('Arial', 10, 'bold'))
        config_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 配置选项
        self.config_frame = tk.Frame(config_frame, bg='#1a1a2e')
        self.config_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.update_algorithm_config_display()
        
    def update_algorithm_config_display(self):
        """更新算法配置显示"""
        # 清空现有内容
        for widget in self.config_frame.winfo_children():
            widget.destroy()
            
        algo = self.ai_algorithms.get(self.current_algorithm, {})
        
        if self.current_algorithm == 'Random':
            tk.Label(self.config_frame, text="随机算法 - 无参数配置",
                    bg='#1a1a2e', fg='#ffffff', font=('Arial', 10)).pack(pady=20)
        elif self.current_algorithm == 'Greedy':
            tk.Label(self.config_frame, text="贪心算法 - 总是选择最优路径",
                    bg='#1a1a2e', fg='#ffffff', font=('Arial', 10)).pack(pady=20)
        else:
            # 显示可配置参数
            params = []
            if 'epsilon' in algo:
                params.append(('探索率 (ε)', algo['epsilon'], 0.0, 1.0, 'epsilon'))
            if 'learning_rate' in algo:
                params.append(('学习率 (α)', algo['learning_rate'], 0.01, 1.0, 'learning_rate'))
            if 'discount_factor' in algo:
                params.append(('折扣因子 (γ)', algo['discount_factor'], 0.5, 1.0, 'discount_factor'))
                
            for param_name, value, min_val, max_val, param_key in params:
                param_frame = tk.Frame(self.config_frame, bg='#1a1a2e')
                param_frame.pack(fill=tk.X, pady=5)
                
                tk.Label(param_frame, text=f"{param_name}:", width=15, anchor='w',
                        bg='#1a1a2e', fg='#ffffff', font=('Arial', 10)).pack(side=tk.LEFT)
                
                var = tk.DoubleVar(value=value)
                scale = tk.Scale(param_frame, from_=min_val, to=max_val, resolution=0.01,
                               orient=tk.HORIZONTAL, variable=var, length=200,
                               bg='#1a1a2e', fg='#ffffff', troughcolor='#2a2a3e')
                scale.pack(side=tk.LEFT, padx=10)
                
                value_label = tk.Label(param_frame, text=f"{value:.2f}", width=8,
                                     bg='#1a1a2e', fg='#ffffff', font=('Arial', 10))
                value_label.pack(side=tk.LEFT)
                
                def update_param(val, key=param_key, label=value_label, var=var, algo_name=self.current_algorithm):
                    actual_value = var.get()
                    label.config(text=f"{actual_value:.2f}")
                    self.ai_algorithms[algo_name][key] = actual_value
                    
                var.trace_add('write', lambda *args, func=update_param: func(var.get()))
                
    def bind_keys(self):
        """绑定键盘事件"""
        self.root.bind('<space>', lambda e: self.toggle_pause())
        self.root.bind('<Escape>', lambda e: self.quit_game())
        
    def on_algorithm_change(self, event=None):
        """算法切换事件"""
        self.current_algorithm = self.algorithm_var.get()
        self.current_algo_label.config(text=f"当前算法: {self.current_algorithm}",
                                     fg=self.ai_algorithms[self.current_algorithm]['color'])
        self.update_algorithm_config_display()
        
    def toggle_comparison_mode(self):
        """切换对比模式"""
        self.comparison_mode = self.comparison_var.get()
        
        if self.comparison_mode:
            self.comparison_algo_frame.pack(side=tk.LEFT, padx=10)
            self.comparison_algorithms = [self.comparison_var1.get(), self.comparison_var2.get()]
        else:
            self.comparison_algo_frame.pack_forget()
            
    def initialize_game_instances(self):
        """初始化游戏实例"""
        if self.comparison_mode:
            # 对比模式：创建多个游戏实例
            algorithms = self.comparison_algorithms
        else:
            # 单算法模式
            algorithms = [self.current_algorithm]
            
        for algo_name in algorithms:
            game_instance = {
                'snake': deque([(10, 10)], maxlen=400),
                'direction': (1, 0),
                'food': None,
                'score': 0,
                'capital': 10000,
                'algorithm': algo_name,
                'game_time': 0,
                'food_lifetime': 0
            }
            
            # 生成初始食物
            self.generate_food_for_instance(game_instance)
            
            self.game_instances[algo_name] = game_instance
            
    def generate_food_for_instance(self, instance):
        """为游戏实例生成食物"""
        while True:
            x = random.randint(0, self.grid_size - 1)
            y = random.randint(0, self.grid_size - 1)
            if (x, y) not in instance['snake']:
                instance['food'] = (x, y)
                instance['food_lifetime'] = random.randint(50, 150)
                break
                
    def get_ai_decision(self, instance):
        """获取AI决策"""
        algo_name = instance['algorithm']
        algorithm = self.ai_algorithms[algo_name]
        strategy = algorithm['strategy']
        
        head = instance['snake'][-1]
        food_pos = instance['food']
        
        if strategy == 'random':
            # 随机策略
            return self.random_decision(instance)
        elif strategy == 'greedy':
            # 贪心策略
            return self.greedy_decision(instance)
        elif strategy == 'q_learning':
            # Q学习策略
            return self.q_learning_decision(instance, algorithm)
        elif strategy == 'sarsa':
            # SARSA策略
            return self.sarsa_decision(instance, algorithm)
        elif strategy == 'deep_q':
            # Deep Q策略
            return self.deep_q_decision(instance, algorithm)
        else:
            return self.random_decision(instance)
            
    def random_decision(self, instance):
        """随机决策"""
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        valid_directions = []
        
        head = instance['snake'][-1]
        for direction in directions:
            new_head = (head[0] + direction[0], head[1] + direction[1])
            
            # 检查边界穿越
            if 0 <= new_head[0] < self.grid_size and 0 <= new_head[1] < self.grid_size:
                if new_head not in instance['snake']:
                    valid_directions.append(direction)
            else:
                valid_directions.append(direction)  # 允许穿越
                
        return random.choice(valid_directions) if valid_directions else (1, 0)
        
    def greedy_decision(self, instance):
        """贪心决策 - 总是朝向食物"""
        head = instance['snake'][-1]
        food = instance['food']
        
        if not food:
            return self.random_decision(instance)
            
        # 计算到食物的方向
        dx = food[0] - head[0]
        dy = food[1] - head[1]
        
        # 优先移动到食物
        if abs(dx) > abs(dy):
            direction = (1 if dx > 0 else -1, 0)
        else:
            direction = (0, 1 if dy > 0 else -1)
            
        # 检查是否安全
        new_head = (head[0] + direction[0], head[1] + direction[1])
        
        if 0 <= new_head[0] < self.grid_size and 0 <= new_head[1] < self.grid_size:
            if new_head in instance['snake']:
                # 避免碰撞，选择安全方向
                return self.random_decision(instance)
            else:
                return direction
        else:
            # 允许穿越边界
            return direction
            
    def q_learning_decision(self, instance, algorithm):
        """Q学习决策"""
        head = instance['snake'][-1]
        food = instance['food']
        
        if not food:
            return self.random_decision(instance)
            
        # 简化的状态表示
        state = (head[0] - food[0], head[1] - food[1], instance['direction'])
        
        # 探索或利用
        if random.random() < algorithm['epsilon']:
            # 探索：随机选择
            return self.random_decision(instance)
        else:
            # 利用：基于Q表选择
            if state not in algorithm['q_table']:
                algorithm['q_table'][state] = [0, 0, 0, 0]  # 上下左右的Q值
                
            # 选择最优动作
            q_values = algorithm['q_table'][state]
            best_action = q_values.index(max(q_values))
            
            directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
            chosen_direction = directions[best_action]
            
            # 检查是否安全
            new_head = (head[0] + chosen_direction[0], head[1] + chosen_direction[1])
            
            if 0 <= new_head[0] < self.grid_size and 0 <= new_head[1] < self.grid_size:
                if new_head in instance['snake']:
                    # 选择随机方向避免碰撞
                    return self.random_decision(instance)
                else:
                    return chosen_direction
            else:
                # 允许穿越边界
                return chosen_direction
                
    def sarsa_decision(self, instance, algorithm):
        """SARSA决策 - 与Q学习类似，但使用不同的更新策略"""
        # SARSA与Q学习的决策过程相同，主要区别在于值更新
        return self.q_learning_decision(instance, algorithm)
        
    def deep_q_decision(self, instance, algorithm):
        """Deep Q Network决策 - 简化版"""
        # 这里简化为与Q学习相同的逻辑，实际应用中会使用神经网络
        return self.q_learning_decision(instance, algorithm)
        
    def update_algorithm_q_table(self, instance, algorithm, reward, state, action):
        """更新算法的Q表"""
        if algorithm['strategy'] in ['q_learning', 'sarsa', 'deep_q']:
            if state not in algorithm['q_table']:
                algorithm['q_table'][state] = [0, 0, 0, 0]
                
            old_q = algorithm['q_table'][state][action]
            next_max_q = max(algorithm['q_table'].get(state, [0, 0, 0, 0]))
            new_q = old_q + algorithm['learning_rate'] * (reward + algorithm['discount_factor'] * next_max_q - old_q)
            
            algorithm['q_table'][state][action] = new_q
            
    def update_instance(self, instance):
        """更新单个游戏实例"""
        # AI决策
        direction = self.get_ai_decision(instance)
        instance['direction'] = direction
        
        # 计算新位置
        head = instance['snake'][-1]
        new_head = (head[0] + direction[0], head[1] + direction[1])
        
        # 边界穿越逻辑
        if 0 <= new_head[0] < self.grid_size and 0 <= new_head[1] < self.grid_size:
            if new_head in instance['snake']:
                self.handle_instance_collision(instance)
                return
        else:
            self.handle_instance_teleport(instance, new_head)
            
        instance['snake'].append(new_head)
        
        # 检查是否吃到食物
        if new_head == instance['food']:
            self.handle_instance_food(instance)
        else:
            instance['snake'].popleft()
            
        # 更新食物生命周期
        if instance['food']:
            instance['food_lifetime'] -= 1
            if instance['food_lifetime'] <= 0:
                self.generate_food_for_instance(instance)
                
        instance['game_time'] += 1
        
    def handle_instance_collision(self, instance):
        """处理实例碰撞"""
        algo_name = instance['algorithm']
        self.algorithm_performance[algo_name]['collisions'] += 1
        
        # 碰撞惩罚
        penalty = 200
        instance['capital'] -= penalty
        instance['score'] = max(0, instance['score'] - 1)
        
        # 更新算法学习
        if instance['food']:
            algorithm = self.ai_algorithms[algo_name]
            head = instance['snake'][-1]
            state = (head[0] - instance['food'][0], head[1] - instance['food'][1], instance['direction'])
            
            directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
            action = directions.index(instance['direction']) if instance['direction'] in directions else 0
            
            self.update_algorithm_q_table(instance, algorithm, -10, state, action)
            
    def handle_instance_teleport(self, instance, new_head):
        """处理实例穿越"""
        # 计算穿越位置
        if new_head[0] < 0:
            new_head = (self.grid_size - 1, new_head[1])
        elif new_head[0] >= self.grid_size:
            new_head = (0, new_head[1])
        elif new_head[1] < 0:
            new_head = (new_head[0], self.grid_size - 1)
        elif new_head[1] >= self.grid_size:
            new_head = (new_head[0], 0)
            
        # 更新新头部位置
        instance['snake'][-1] = new_head
        
        # 穿越惩罚
        penalty = 50
        instance['capital'] -= penalty
        
    def handle_instance_food(self, instance):
        """处理实例食物消费"""
        algo_name = instance['algorithm']
        self.algorithm_performance[algo_name]['food_collected'] += 1
        
        instance['score'] += 1
        
        # 随机奖励
        rewards = [100, 150, 200, 250, 300]
        reward = random.choice(rewards)
        instance['capital'] += reward
        
        # 更新算法学习
        algorithm = self.ai_algorithms[algo_name]
        head = instance['snake'][-1]
        state = (head[0] - instance['food'][0], head[1] - instance['food'][1], instance['direction'])
        
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        action = directions.index(instance['direction']) if instance['direction'] in directions else 0
        
        self.update_algorithm_q_table(instance, algorithm, 10, state, action)
        
        # 生成新食物
        self.generate_food_for_instance(instance)
        
    def draw_game(self):
        """绘制游戏画面"""
        self.canvas.delete("all")
        
        # 绘制网格背景
        for i in range(0, self.canvas_width, self.cell_size):
            self.canvas.create_line(i, 0, i, self.canvas_height, fill='#1a1a2e', width=1)
        for i in range(0, self.canvas_height, self.cell_size):
            self.canvas.create_line(0, i, self.canvas_width, i, fill='#1a1a2e', width=1)
            
        # 绘制当前活动的游戏实例
        if self.game_instances:
            if self.comparison_mode:
                # 对比模式：绘制所有实例（用不同颜色）
                for algo_name, instance in self.game_instances.items():
                    color = self.ai_algorithms[algo_name]['color']
                    self.draw_instance(instance, color, f"{algo_name[:4]}")
            else:
                # 单算法模式：只绘制当前实例
                instance = list(self.game_instances.values())[0]
                color = self.ai_algorithms[instance['algorithm']]['color']
                self.draw_instance(instance, color, "")
                
    def draw_instance(self, instance, color, label):
        """绘制单个游戏实例"""
        # 绘制蛇身
        for i, segment in enumerate(instance['snake']):
            x1 = segment[0] * self.cell_size
            y1 = segment[1] * self.cell_size
            x2 = x1 + self.cell_size
            y2 = y1 + self.cell_size
            
            if i == len(instance['snake']) - 1:  # 蛇头
                self.canvas.create_oval(x1+2, y1+2, x2-2, y2-2, 
                                      fill=color, outline='#ffffff', width=2)
                if label:
                    self.canvas.create_text((x1+x2)//2, (y1+y2)//2, text=label,
                                          fill='#000000', font=('Arial', 8, 'bold'))
            else:  # 蛇身
                intensity = max(50, int(200 - (i * 150 / len(instance['snake']))))
                # 调整颜色亮度
                if color.startswith('#'):
                    base_color = color[1:]
                    r = int(base_color[0:2], 16)
                    g = int(base_color[2:4], 16)
                    b = int(base_color[4:6], 16)
                    
                    # 混合颜色
                    r = int(r * intensity / 255)
                    g = int(g * intensity / 255)
                    b = int(b * intensity / 255)
                    
                    faded_color = f'#{r:02x}{g:02x}{b:02x}'
                else:
                    faded_color = color
                    
                self.canvas.create_rectangle(x1+1, y1+1, x2-1, y2-1, 
                                           fill=faded_color, outline=color)
                
        # 绘制食物
        if instance['food']:
            x1 = instance['food'][0] * self.cell_size
            y1 = instance['food'][1] * self.cell_size
            x2 = x1 + self.cell_size
            y2 = y1 + self.cell_size
            
            food_color = '#ffd700'  # 食物保持金色
            self.canvas.create_oval(x1+3, y1+3, x2-3, y2-3, 
                                   fill=food_color, outline='#ffffff', width=2)
                                   
    def update_performance_display(self):
        """更新性能显示"""
        # 计算性能指标
        for algo_name, instance in self.game_instances.items():
            perf = self.algorithm_performance[algo_name]
            
            # 更新基本统计
            perf['total_score'] = instance['score']
            perf['total_capital'] = instance['capital']
            
            # 计算成功率
            total_actions = perf['food_collected'] + perf['collisions']
            if total_actions > 0:
                perf['success_rate'] = (perf['food_collected'] / total_actions) * 100
            else:
                perf['success_rate'] = 0
                
            # 计算平均奖励
            if perf['food_collected'] > 0:
                total_reward = perf['food_collected'] * 200 - perf['collisions'] * 200
                perf['avg_reward'] = total_reward / (perf['food_collected'] + perf['collisions'])
            else:
                perf['avg_reward'] = 0
                
            # Q表大小
            algorithm = self.ai_algorithms[algo_name]
            if 'q_table' in algorithm:
                perf['q_table_size'] = len(algorithm['q_table'])
            else:
                perf['q_table_size'] = 0
                
        # 更新表格
        self.update_performance_table()
        
        # 更新图表
        self.update_comparison_chart()
        
        # 更新游戏信息
        self.update_game_info()
        
    def update_performance_table(self):
        """更新性能表格"""
        # 清空表格
        for item in self.performance_tree.get_children():
            self.performance_tree.delete(item)
            
        # 添加性能数据
        for algo_name, perf in self.algorithm_performance.items():
            # 只显示活跃算法的数据
            if algo_name in self.game_instances:
                color = self.ai_algorithms[algo_name]['color']
                values = (
                    algo_name,
                    f"{perf['total_score']}",
                    f"{perf['success_rate']:.1f}%",
                    f"{perf['avg_reward']:.1f}",
                    f"{perf['q_table_size']}"
                )
                
                item = self.performance_tree.insert('', 'end', values=values)
                self.performance_tree.set(item, 'Algorithm', algo_name)
                
    def update_comparison_chart(self):
        """更新对比图表"""
        canvas = self.comparison_canvas
        canvas.delete("all")
        
        if not self.game_instances:
            canvas.create_text(300, 100, text="等待游戏数据...", fill='#666666', font=('Arial', 12))
            return
            
        width = 600
        height = 200
        padding = 20
        
        # 获取数据
        algorithms = list(self.game_instances.keys())
        if len(algorithms) < 2:
            canvas.create_text(300, 100, text="需要至少2个算法进行对比", fill='#666666', font=('Arial', 12))
            return
            
        # 绘制成功率对比柱状图
        bar_width = 80
        bar_spacing = 150
        start_x = padding + 50
        
        max_success_rate = max([self.algorithm_performance[algo]['success_rate'] for algo in algorithms])
        if max_success_rate == 0:
            max_success_rate = 1
            
        for i, algo_name in enumerate(algorithms):
            perf = self.algorithm_performance[algo_name]
            success_rate = perf['success_rate']
            color = self.ai_algorithms[algo_name]['color']
            
            # 绘制柱状图
            bar_height = int((success_rate / 100) * (height - 2*padding))
            x = start_x + i * bar_spacing
            y = height - padding - bar_height
            
            canvas.create_rectangle(x, y, x + bar_width, height - padding,
                                   fill=color, outline='#ffffff', width=1)
            
            # 绘制标签
            canvas.create_text(x + bar_width//2, height - padding + 10,
                              text=algo_name[:8], fill=color, font=('Arial', 9, 'bold'))
            
            canvas.create_text(x + bar_width//2, y - 5,
                              text=f"{success_rate:.1f}%", fill='#ffffff', font=('Arial', 8))
                              
    def update_game_info(self):
        """更新游戏信息"""
        if self.game_instances:
            if self.comparison_mode:
                info_text = f"对比模式 - {len(self.game_instances)} 个算法运行中"
            else:
                instance = list(self.game_instances.values())[0]
                info_text = f"时间: {instance['game_time']//60:02d}:{instance['game_time']%60:02d} | "
                info_text += f"分数: {instance['score']} | "
                info_text += f"资金: ${instance['capital']:,}"
                
            self.game_info_label.config(text=info_text)
            
    def game_loop(self):
        """游戏主循环"""
        if self.game_running and not self.game_paused:
            # 更新所有游戏实例
            for instance in self.game_instances.values():
                self.update_instance(instance)
                
            # 绘制游戏
            self.draw_game()
            
            # 更新性能显示
            self.update_performance_display()
            
            # 继续游戏循环
            self.root.after(self.game_speed, self.game_loop)
            
    def start_game(self):
        """开始游戏"""
        self.game_running = True
        self.game_paused = False
        self.global_game_time = 0
        
        # 初始化游戏实例
        self.initialize_game_instances()
        
        # 更新按钮状态
        self.start_button.config(state='disabled')
        self.pause_button.config(state='normal')
        
        # 开始游戏循环
        self.game_loop()
        
    def toggle_pause(self):
        """切换暂停状态"""
        self.game_paused = not self.game_paused
        
        if self.game_paused:
            self.pause_button.config(text="▶️ 继续")
        else:
            self.pause_button.config(text="⏸️ 暂停")
            self.game_loop()
            
    def reset_game(self):
        """重置游戏"""
        self.game_running = False
        self.game_paused = False
        
        # 重置游戏实例
        self.game_instances.clear()
        
        # 重置性能数据
        for algo_name in self.ai_algorithms:
            self.algorithm_performance[algo_name] = {
                'food_collected': 0,
                'collisions': 0,
                'total_score': 0,
                'total_capital': 10000,
                'success_rate': 0,
                'avg_reward': 0,
                'q_table_size': 0
            }
            
        # 清空Q表（可选）
        # for algorithm in self.ai_algorithms.values():
        #     if 'q_table' in algorithm:
        #         algorithm['q_table'].clear()
                
        # 更新按钮状态
        self.start_button.config(state='normal')
        self.pause_button.config(state='disabled', text="⏸️ 暂停")
        
        # 清空显示
        self.canvas.delete("all")
        self.game_info_label.config(text="准备就绪")
        
        # 清空表格
        for item in self.performance_tree.get_children():
            self.performance_tree.delete(item)
            
        # 清空图表
        self.comparison_canvas.delete("all")
        
    def quit_game(self):
        """退出游戏"""
        if self.game_running:
            if messagebox.askokcancel("退出", "确定要退出游戏吗？"):
                self.root.quit()
        else:
            self.root.quit()
            
def main():
    root = tk.Tk()
    game = AIAlgorithmComparisonSnake(root)
    root.mainloop()

if __name__ == "__main__":
    main()