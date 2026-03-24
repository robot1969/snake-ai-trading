# -*- coding: utf-8 -*-
"""
简化版贪吃蛇AI对比程序 - 测试GUI
"""

import tkinter as tk
from tkinter import messagebox
import random

class SimpleSnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🐍 量化交易贪吃蛇 - AI对比测试版")
        self.root.geometry("800x600")
        self.root.configure(bg='#0a0a0f')
        
        # 简单的界面
        label = tk.Label(
            root, 
            text="🐍 贪吃蛇AI对比程序\n\n启动状态: ✅ 程序正常\n\n点击下方按钮开始游戏",
            bg='#0a0a0f',
            fg='#00ff00',
            font=('Consolas', 16),
            justify='center'
        )
        label.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        # 测试按钮
        btn_frame = tk.Frame(root, bg='#0a0a0f')
        btn_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Button(
            btn_frame,
            text="🎮 开始测试游戏",
            command=self.start_game,
            bg='#4caf50',
            fg='white',
            font=('Arial', 12, 'bold'),
            padx=20,
            pady=10
        ).pack(side=tk.LEFT, padx=10)
        
        tk.Button(
            btn_frame,
            text="❌ 退出",
            command=root.quit,
            bg='#f44336',
            fg='white',
            font=('Arial', 12, 'bold'),
            padx=20,
            pady=10
        ).pack(side=tk.LEFT, padx=10)
        
        # AI信息
        ai_frame = tk.LabelFrame(root, text="🤖 AI算法", bg='#1a1a2e', fg='#4caf50', font=('Arial', 10, 'bold'))
        ai_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ai_list = ['Q-Learning', 'SARSA', 'Greedy', 'Random', 'DQN', 'A* Search']
        for ai in ai_list:
            status = tk.Label(ai_frame, text=f"• {ai}: ✓就绪", bg='#1a1a2e', fg='#4caf50', font=('Arial', 9))
            status.pack(anchor='w')
        
        # 状态栏
        self.status_label = tk.Label(
            root,
            text="🟢 程序已就绪，可以开始游戏！",
            bg='#1a1a2e',
            fg='#ffffff',
            font=('Arial', 10)
        )
        self.status_label.pack(fill=tk.X, side=tk.BOTTOM, padx=20, pady=5)
        
    def start_game(self):
        """开始测试游戏"""
        self.status_label.config(text="🟢 游戏运行中...", fg='#ffeb3b')
        
        # 模拟游戏过程
        self.root.after(1000, self.game_loop)
        
    def game_loop(self):
        """游戏循环"""
        # 随机选择一个AI
        ai_names = ['Q-Learning', 'SARSA', 'Greedy', 'Random', 'DQN', 'A* Search']
        selected_ai = random.choice(ai_names)
        score = random.randint(1000, 5000)
        
        self.status_label.config(
            text=f"🎮 {selected_ai} 获胜！得分: ${score}",
            fg='#4caf50'
        )
        
        # 继续游戏循环
        if random.random() < 0.8:  # 80%概率继续
            self.root.after(1000, self.game_loop)
        else:
            self.status_label.config(text="🟢 游戏暂停", fg='#ffeb3b')

def main():
    """主函数"""
    try:
        root = tk.Tk()
        game = SimpleSnakeGame(root)
        root.mainloop()
    except Exception as e:
        print(f"启动失败: {e}")
        input("按回车键退出...")

if __name__ == "__main__":
    main()