#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化版图表AI对比 - 确保图表正常显示
"""

import tkinter as tk
from tkinter import ttk
import random
import time
from collections import deque, defaultdict

class SimpleChartAIComparison:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Chart AI Comparison")
        self.root.configure(bg='#0a0a0f')
        self.root.geometry("1400x900")
        
        # AI数据
        self.ai_data = {
            'Q-Learning': {'color': '#4caf50', 'food': 5, 'collision': 2, 'capital': 11500},
            'SARSA': {'color': '#2196f3', 'food': 3, 'collision': 1, 'capital': 10500}
        }
        
        self.setup_ui()
        self.draw_charts()
        
    def setup_ui(self):
        main_frame = tk.Frame(self.root, bg='#0a0a0f')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 标题
        tk.Label(main_frame, text="AI Comparison Charts", font=('Arial', 16, 'bold'),
                bg='#0a0a0f', fg='#ffd700').pack(pady=10)
        
        # 创建2个图表
        # 图表1: 成功率
        frame1 = tk.LabelFrame(main_frame, text="Success Rate Comparison", 
                              font=('Arial', 11, 'bold'), bg='#1a1a2e', fg='#ffffff')
        frame1.pack(fill=tk.X, pady=10)
        
        self.canvas1 = tk.Canvas(frame1, width=800, height=200, bg='#0a0a0f',
                                highlightthickness=2, highlightbackground='#4a4a6e')
        self.canvas1.pack(padx=10, pady=10)
        
        # 图表2: 资金
        frame2 = tk.LabelFrame(main_frame, text="Capital Comparison", 
                              font=('Arial', 11, 'bold'), bg='#1a1a2e', fg='#ffffff')
        frame2.pack(fill=tk.X, pady=10)
        
        self.canvas2 = tk.Canvas(frame2, width=800, height=200, bg='#0a0a0f',
                                highlightthickness=2, highlightbackground='#4a4a6e')
        self.canvas2.pack(padx=10, pady=10)
        
        # 刷新按钮
        tk.Button(main_frame, text="Refresh Charts", command=self.draw_charts,
                 bg='#4caf50', fg='white', font=('Arial', 12, 'bold')).pack(pady=20)
        
    def draw_charts(self):
        """绘制图表"""
        self.draw_success_rate()
        self.draw_capital()
        
    def draw_success_rate(self):
        """绘制成功率柱状图"""
        canvas = self.canvas1
        canvas.delete("all")
        
        width = 800
        height = 200
        margin = 50
        
        # 绘制基准线
        canvas.create_line(margin, height-margin, width-margin, height-margin, 
                          fill='#4a4a6e', width=2)
        
        # 绘制柱状图
        bar_width = 150
        spacing = 250
        
        for i, (name, data) in enumerate(self.ai_data.items()):
            total = data['food'] + data['collision']
            rate = (data['food'] / max(1, total)) * 100
            
            x = margin + 50 + i * spacing
            bar_height = (rate / 100) * (height - 2 * margin)
            y = height - margin - bar_height
            
            # 柱状图
            canvas.create_rectangle(x, y, x + bar_width, height - margin,
                                   fill=data['color'], outline='#ffffff', width=2)
            
            # 百分比
            canvas.create_text(x + bar_width//2, y - 20,
                              text=f"{rate:.0f}%", fill='#ffffff', 
                              font=('Arial', 14, 'bold'))
            
            # AI名称
            canvas.create_text(x + bar_width//2, height - margin + 25,
                              text=name, fill=data['color'], 
                              font=('Arial', 11, 'bold'))
            
            # 统计
            canvas.create_text(x + bar_width//2, height - margin + 45,
                              text=f"Success: {data['food']}/{total}", 
                              fill='#888888', font=('Arial', 9))
                              
    def draw_capital(self):
        """绘制资金对比"""
        canvas = self.canvas2
        canvas.delete("all")
        
        width = 800
        height = 200
        margin = 50
        
        # 基准线
        canvas.create_line(margin, height-margin, width-margin, height-margin,
                          fill='#4a4a6e', width=2)
        canvas.create_line(margin, margin, margin, height-margin,
                          fill='#4a4a6e', width=2)
        
        # 显示当前资金
        y_pos = 80
        for i, (name, data) in enumerate(self.ai_data.items()):
            x = margin + 50 + i * 300
            
            # 颜色块
            canvas.create_rectangle(x, y_pos - 10, x + 30, y_pos + 10, 
                                 fill=data['color'], outline='#ffffff')
            
            # 文字
            canvas.create_text(x + 100, y_pos, 
                              text=f"{name}: ${data['capital']:,}",
                              fill=data['color'], font=('Arial', 12, 'bold'),
                              anchor='w')
            
            # 盈亏
            pnl = data['capital'] - 10000
            color = '#4caf50' if pnl > 0 else '#f44336'
            canvas.create_text(x + 100, y_pos + 25,
                              text=f"P&L: ${pnl:+,}",
                              fill=color, font=('Arial', 11))

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleChartAIComparison(root)
    root.mainloop()