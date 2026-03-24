#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化版图表AI对比 - 带完整坐标轴
"""

import tkinter as tk
from tkinter import ttk
import random
import time
from collections import deque, defaultdict

class SimpleChartWithAxes:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Chart with Axes")
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
        tk.Label(main_frame, text="AI Comparison Charts with Axes", 
                font=('Arial', 16, 'bold'),
                bg='#0a0a0f', fg='#ffd700').pack(pady=10)
        
        # 图表1: 成功率（带坐标轴）
        frame1 = tk.LabelFrame(main_frame, text="Success Rate Chart with Axes", 
                              font=('Arial', 11, 'bold'), bg='#1a1a2e', fg='#ffffff')
        frame1.pack(fill=tk.X, pady=10)
        
        self.canvas1 = tk.Canvas(frame1, width=800, height=250, bg='#0a0a0f',
                                highlightthickness=2, highlightbackground='#4a4a6e')
        self.canvas1.pack(padx=10, pady=10)
        
        # 图表2: 资金（带坐标轴）
        frame2 = tk.LabelFrame(main_frame, text="Capital Chart with Axes", 
                              font=('Arial', 11, 'bold'), bg='#1a1a2e', fg='#ffffff')
        frame2.pack(fill=tk.X, pady=10)
        
        self.canvas2 = tk.Canvas(frame2, width=800, height=250, bg='#0a0a0f',
                                highlightthickness=2, highlightbackground='#4a4a6e')
        self.canvas2.pack(padx=10, pady=10)
        
        # 刷新按钮
        tk.Button(main_frame, text="Refresh Charts", command=self.draw_charts,
                 bg='#4caf50', fg='white', font=('Arial', 12, 'bold')).pack(pady=20)
        
    def draw_charts(self):
        """绘制图表"""
        self.draw_success_rate_with_axes()
        self.draw_capital_with_axes()
        
    def draw_success_rate_with_axes(self):
        """绘制带坐标轴的成功率柱状图"""
        canvas = self.canvas1
        canvas.delete("all")
        
        width = 800
        height = 250
        margin = 60
        
        # X轴
        canvas.create_line(margin, height - margin, width - margin, height - margin, 
                          fill='#ffffff', width=2)
        canvas.create_text(width - margin + 20, height - margin + 5, text="AI算法", 
                          fill='#ffffff', font=('Arial', 9))
        
        # Y轴
        canvas.create_line(margin, margin, margin, height - margin, 
                          fill='#ffffff', width=2)
        canvas.create_text(margin - 20, margin - 15, text="成功率 (%)", 
                          fill='#ffffff', font=('Arial', 9))
        
        # Y轴刻度和网格线
        max_rate = 100
        for i in range(6):
            y = height - margin - (i / 5) * (height - 2 * margin)
            # 刻度线
            canvas.create_line(margin - 5, y, margin, y, fill='#ffffff', width=1)
            # 刻度值
            canvas.create_text(margin - 10, y, text=f"{i*20}", 
                              fill='#888888', font=('Arial', 8), anchor='e')
            # 网格线
            if i > 0:
                canvas.create_line(margin, y, width - margin, y, 
                                  fill='#1a1a2e', width=1, dash=(3, 3))
        
        # 绘制柱状图
        bar_width = 100
        spacing = 250
        
        for i, (name, data) in enumerate(self.ai_data.items()):
            total = data['food'] + data['collision']
            rate = (data['food'] / max(1, total)) * 100
            
            x = margin + 80 + i * spacing
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
            canvas.create_text(x + bar_width//2, height - margin + 20,
                              text=name, fill=data['color'], 
                              font=('Arial', 11, 'bold'))
            
            # 统计
            canvas.create_text(x + bar_width//2, height - margin + 40,
                              text=f"Success: {data['food']}/{total}", 
                              fill='#888888', font=('Arial', 9))
                              
    def draw_capital_with_axes(self):
        """绘制带坐标轴的资金对比"""
        canvas = self.canvas2
        canvas.delete("all")
        
        width = 800
        height = 250
        margin = 60
        
        # 计算数值范围
        capitals = [d['capital'] for d in self.ai_data.values()]
        min_val = min(capitals)
        max_val = max(capitals)
        val_range = max_val - min_val if max_val != min_val else 1
        
        # X轴
        canvas.create_line(margin, height - margin, width - margin, height - margin, 
                          fill='#ffffff', width=2)
        canvas.create_text(width - margin + 20, height - margin + 5, text="AI算法", 
                          fill='#ffffff', font=('Arial', 9))
        
        # Y轴
        canvas.create_line(margin, margin, margin, height - margin, 
                          fill='#ffffff', width=2)
        canvas.create_text(margin - 25, margin - 15, text="资金 ($)", 
                          fill='#ffffff', font=('Arial', 9))
        
        # Y轴刻度和网格线
        for i in range(6):
            y = height - margin - (i / 5) * (height - 2 * margin)
            # 刻度线
            canvas.create_line(margin - 5, y, margin, y, fill='#ffffff', width=1)
            # 刻度值
            val = min_val + (i / 5) * val_range
            canvas.create_text(margin - 10, y, text=f"${val:,.0f}", 
                              fill='#888888', font=('Arial', 8), anchor='e')
            # 网格线
            if i > 0:
                canvas.create_line(margin, y, width - margin, y, 
                                  fill='#1a1a2e', width=1, dash=(3, 3))
        
        # 绘制数据点
        for i, (name, data) in enumerate(self.ai_data.items()):
            x = margin + 130 + i * 300
            y = height - margin - (data['capital'] - min_val) / val_range * (height - 2 * margin)
            
            # 数据点
            canvas.create_oval(x-10, y-10, x+10, y+10, 
                           fill=data['color'], outline='#ffffff', width=2)
            
            # 连接线
            if i > 0:
                prev_x = margin + 130 + (i-1) * 300
                prev_y = height - margin - (list(self.ai_data.values())[i-1]['capital'] - min_val) / val_range * (height - 2 * margin)
                canvas.create_line(prev_x, prev_y, x, y, fill=data['color'], width=3)
            
            # 数值标签
            canvas.create_text(x, y - 25,
                              text=f"${data['capital']:,}",
                              fill=data['color'], font=('Arial', 11, 'bold'))
            
            # AI名称
            canvas.create_text(x, height - margin + 25,
                              text=name, fill=data['color'], 
                              font=('Arial', 11, 'bold'))
            
            # 盈亏
            pnl = data['capital'] - 10000
            pnl_color = '#4caf50' if pnl > 0 else '#f44336'
            canvas.create_text(x, height - margin + 45,
                              text=f"P&L: ${pnl:+,}",
                              fill=pnl_color, font=('Arial', 10))

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleChartWithAxes(root)
    root.mainloop()