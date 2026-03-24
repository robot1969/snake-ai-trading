#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试版本：检查图表绘制问题
"""

import tkinter as tk
from tkinter import ttk
import random
import time
from collections import deque, defaultdict

class DebugChartAIComparisonSnake:
    def __init__(self, root):
        self.root = root
        self.root.title("DEBUG - Chart AI Comparison")
        self.root.configure(bg='#0a0a0f')
        self.root.geometry("1800x1100")
        
        # 简化参数
        self.canvas_width = 500
        self.canvas_height = 500
        self.grid_size = 20
        
        # AI算法定义
        self.ai_algorithms = {
            'Q-Learning': {
                'name': 'Q-Learning',
                'color': '#4caf50',
                'food': 5,  # 模拟数据
                'collision': 2,
                'active': True
            },
            'SARSA': {
                'name': 'SARSA',
                'color': '#2196f3',
                'food': 3,
                'collision': 1,
                'active': True
            }
        }
        
        # 模拟资金历史
        self.capital_history = defaultdict(lambda: deque(maxlen=100))
        self.capital_history['Q-Learning'] = deque([10000, 10500, 11000, 10800, 11500, 12000], maxlen=100)
        self.capital_history['SARSA'] = deque([10000, 10200, 10100, 10300, 10500], maxlen=100)
        
        self.setup_gui()
        
        # 立即绘制图表
        self.root.after(100, self.test_chart_drawing)
        
    def setup_gui(self):
        main_frame = tk.Frame(self.root, bg='#0a0a0f')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建3个简单的图表画布
        for i in range(3):
            frame = tk.LabelFrame(main_frame, text=f"Chart {i+1}", font=('Arial', 10, 'bold'),
                                 bg='#1a1a2e', fg='#ffffff')
            frame.pack(fill=tk.X, pady=5)
            
            canvas = tk.Canvas(frame, width=800, height=200, bg='#0a0a0f',
                             highlightthickness=1, highlightbackground='#4a4a6e')
            canvas.pack(padx=5, pady=5)
            
            if i == 0:
                self.test_canvas1 = canvas
            elif i == 1:
                self.test_canvas2 = canvas
            else:
                self.test_canvas3 = canvas
                
    def test_chart_drawing(self):
        """测试图表绘制"""
        print("Testing chart drawing...")
        
        # 测试1：简单的柱状图
        canvas = self.test_canvas1
        canvas.delete("all")
        
        width = 800
        height = 200
        margin = 40
        
        active_algos = [a for a in self.ai_algorithms if self.ai_algorithms[a]['active']]
        print(f"Active algorithms: {active_algos}")
        
        if not active_algos:
            canvas.create_text(width//2, height//2, text="No active AI", fill='#666666')
            return
            
        # 绘制简单的柱状图
        bar_width = 100
        spacing = 150
        
        for i, algo_name in enumerate(active_algos):
            algo = self.ai_algorithms[algo_name]
            total = algo['food'] + algo['collision']
            rate = (algo['food'] / max(1, total)) * 100
            
            # 绘制柱状图
            x = margin + i * spacing
            bar_height = (rate / 100) * (height - 2 * margin)
            y = height - margin - bar_height
            
            print(f"Drawing bar for {algo_name}: rate={rate:.1f}%, x={x}, y={y}")
            
            canvas.create_rectangle(x, y, x + bar_width, height - margin,
                                   fill=algo['color'], outline='#ffffff', width=2)
            
            # 添加文字
            canvas.create_text(x + bar_width//2, y - 20,
                              text=f"{rate:.0f}%", fill='#ffffff', font=('Arial', 12, 'bold'))
            
            canvas.create_text(x + bar_width//2, height - margin + 20,
                              text=algo_name, fill=algo['color'], font=('Arial', 10))
            
        print("Chart 1 drawn successfully")
        
        # 测试2：资金曲线
        canvas2 = self.test_canvas2
        canvas2.delete("all")
        
        for algo_name in active_algos:
            data = list(self.capital_history[algo_name])
            if len(data) < 2:
                continue
                
            algo = self.ai_algorithms[algo_name]
            color = algo['color']
            
            min_val = min(data)
            max_val = max(data)
            val_range = max_val - min_val if max_val != min_val else 1
            
            points = []
            for j, val in enumerate(data):
                x = margin + j * (width - 2 * margin) // max(1, len(data) - 1)
                y = height - margin - (val - min_val) / val_range * (height - 2 * margin)
                points.extend([x, y])
                
            if len(points) >= 4:
                print(f"Drawing line for {algo_name}: {len(data)} points")
                canvas2.create_line(points, fill=color, width=2, smooth=True)
                
        print("Chart 2 drawn successfully")
        
        # 测试3：简单的网格
        canvas3 = self.test_canvas3
        canvas3.delete("all")
        
        for i in range(5):
            y = margin + i * (height - 2 * margin) // 4
            canvas3.create_line(margin, y, width - margin, y, fill='#1a1a2e', width=1)
            
        canvas3.create_text(width//2, height//2, text="Test Grid OK", fill='#00ff00', font=('Arial', 16))
        print("Chart 3 drawn successfully")
        
        print("\nAll charts drawn! Check the GUI window.")
        
if __name__ == "__main__":
    root = tk.Tk()
    app = DebugChartAIComparisonSnake(root)
    root.mainloop()