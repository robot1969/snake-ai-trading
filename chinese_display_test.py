#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中文显示测试
"""

import tkinter as tk

class ChineseDisplayTest:
    def __init__(self, root):
        self.root = root
        self.root.title("中文显示测试")
        self.root.geometry("800x600")
        self.root.configure(bg='#1a1a2e')
        
        # 测试各种中文显示
        frame = tk.Frame(self.root, bg='#1a1a2e')
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 标题
        tk.Label(frame, text="🐍 量化交易贪吃蛇", 
                font=('Arial', 20, 'bold'), 
                bg='#1a1a2e', fg='#ffd700').pack(pady=10)
        
        # 中文标签
        labels = [
            "AI算法: Q-Learning / SARSA",
            "当前AI状态",
            "实时日志",
            "AI对比图表",
            "资金对比",
            "性能统计",
            "成功率对比",
            "无激活的AI",
            "等待数据..."
        ]
        
        for text in labels:
            tk.Label(frame, text=text, 
                    font=('Arial', 12), 
                    bg='#1a1a2e', fg='#00ff00').pack(pady=5)
        
        # 按钮
        btn_frame = tk.Frame(frame, bg='#1a1a2e')
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="▶ 开始", 
                 bg='#4caf50', fg='white',
                 font=('Arial', 12, 'bold')).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="⏸ 暂停", 
                 bg='#ff9800', fg='white',
                 font=('Arial', 12, 'bold')).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="🔄 重置", 
                 bg='#f44336', fg='white',
                 font=('Arial', 12, 'bold')).pack(side=tk.LEFT, padx=5)
        
        # 状态显示
        self.status_label = tk.Label(frame, text="状态: 准备就绪", 
                                    font=('Arial', 11),
                                    bg='#1a1a2e', fg='#00bcd4')
        self.status_label.pack(pady=20)
        
        # Canvas中文测试
        canvas_frame = tk.LabelFrame(frame, text="图表区域", 
                                    font=('Arial', 10, 'bold'),
                                    bg='#1a1a2e', fg='#ffffff')
        canvas_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.canvas = tk.Canvas(canvas_frame, width=700, height=200, 
                               bg='#0a0a0f',
                               highlightthickness=1,
                               highlightbackground='#4a4a6e')
        self.canvas.pack(padx=10, pady=10)
        
        # 在Canvas上绘制中文
        self.draw_chinese_on_canvas()
        
    def draw_chinese_on_canvas(self):
        """在Canvas上绘制中文"""
        canvas = self.canvas
        
        # 绘制标题
        canvas.create_text(350, 30, text="成功率对比", 
                          fill='#ffffff', font=('Arial', 14, 'bold'))
        
        # 绘制柱状图标签
        labels = ["Q-Learning", "SARSA"]
        colors = ['#4caf50', '#2196f3']
        
        for i, (label, color) in enumerate(zip(labels, colors)):
            x = 150 + i * 200
            # 柱状图
            canvas.create_rectangle(x, 100, x + 100, 150, 
                                 fill=color, outline='#ffffff', width=2)
            # 标签
            canvas.create_text(x + 50, 170, text=label, 
                              fill=color, font=('Arial', 11, 'bold'))
            # 百分比
            canvas.create_text(x + 50, 80, text="75%", 
                              fill='#ffffff', font=('Arial', 12, 'bold'))
        
        # 底部文字
        canvas.create_text(350, 190, text="AI算法性能对比 - 实时数据", 
                          fill='#888888', font=('Arial', 9))

if __name__ == "__main__":
    root = tk.Tk()
    app = ChineseDisplayTest(root)
    root.mainloop()