# 量化交易贪吃蛇 - 统计图表版
# Quantitative Trading Snake - Statistics & Charts

import random
import os
import time
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # 非交互式后端
import numpy as np
from collections import deque

class TradingSnakeWithStats:
    def __init__(self):
        self.size = 12
        self.snake = [(6,6), (5,6), (4,6)]
        self.dir = (1,0)
        self.money = 100000
        self.initial_money = 100000
        self.food = []
        
        # 交易统计
        self.trades = []
        self.money_history = [100000]
        self.profit_history = []
        self.trade_count = 0
        self.win_count = 0
        self.loss_count = 0
        self.profit_total = 0
        self.loss_total = 0
        self.teleport_count = 0
        
        # 不同类型交易统计
        self.trade_types = {"profit": 0, "loss": 0, "breakout": 0, "reversal": 0}
        self.trade_values = {"profit": [], "loss": [], "breakout": [], "reversal": []}
        
        self.make_food()
        self.game_start_time = time.time()
    
    def clear(self):
        os.system('cls')
    
    def draw_stats_panel(self):
        """绘制统计面板"""
        print("=" * 80)
        print("📊 交易统计面板 | Trading Statistics Dashboard")
        print("=" * 80)
        
        # 基础统计
        win_rate = (self.win_count / max(1, self.trade_count)) * 100
        current_pnl = self.money - self.initial_money
        pnl_percentage = (current_pnl / self.initial_money) * 100
        
        print(f"💰 资本: ${self.money:,} | 📈 总盈亏: ${current_pnl:+,} ({pnl_percentage:+.1f}%)")
        print(f"🤝 交易次数: {self.trade_count} | 🎯 胜率: {win_rate:.1f}% | ⚡ 传送次数: {self.teleport_count}")
        
        # 盈亏统计
        if self.profit_total > 0:
            avg_profit = self.profit_total / max(1, self.win_count)
            avg_loss = abs(self.loss_total) / max(1, self.loss_count)
            profit_factor = avg_profit / max(0.1, avg_loss)
            print(f"💎 平均盈利: ${avg_profit:.0f} | 📉 平均亏损: ${avg_loss:.0f} | 📊 盈亏比: {profit_factor:.2f}")
        
        # 交易类型统计
        print(f"\n📋 交易类型分析:")
        for trade_type, count in self.trade_types.items():
            if count > 0:
                values = self.trade_values[trade_type]
                avg_val = sum(values) / len(values) if values else 0
                print(f"   {trade_type.capitalize()}: {count}次, 平均值: ${avg_val:+.0f}")
        
        print("=" * 80)
    
    def draw_ascii_chart(self, data, title, height=5):
        """绘制ASCII图表"""
        if not data:
            return
        
        max_val = max(data)
        min_val = min(data)
        range_val = max_val - min_val if max_val != min_val else 1
        
        print(f"\n📈 {title}")
        
        # 绘制图表
        for level in range(height, 0, -1):
            threshold = min_val + (range_val * level / height)
            line = "  "
            for i, val in enumerate(data):
                if val >= threshold:
                    if i == len(data) - 1:  # 最新值
                        line += "█"
                    else:
                        line += "▓"
                else:
                    line += " "
            print(line)
        
        # X轴
        print("  └" + "─" * min(len(data), 20))
        
        # 数值
        if len(data) <= 10:
            value_line = "   "
            for val in data[-10:]:
                value_line += f"{val:4.0f}"
            print(value_line)
    
    def draw_game_area(self):
        """绘制游戏区域"""
        print("\n🐍 游戏区域 | Game Area")
        print("-" * 40)
        
        for y in range(self.size):
            row = ""
            for x in range(self.size):
                if (x,y) == self.snake[0]:
                    row += "S"
                elif (x,y) in self.snake:
                    row += "o"
                elif (x,y) in self.food:
                    # 不同食物类型
                    food_type = next((f[2] for f in self.food if f[0]==x and f[1]==y), "profit")
                    symbols = {"profit": "$", "loss": "L", "breakout": "B", "reversal": "R"}
                    row += symbols.get(food_type, "?")
                else:
                    row += "."
            print(row)
        
        print("-" * 40)
        print("控制: WASD=移动 SPACE=统计 Q=退出")
        print("符号: $盈利 L亏损 B突破 R反转")
    
    def make_food(self):
        """生成食物"""
        if len(self.food) < 3:
            while True:
                x, y = random.randint(0,self.size-1), random.randint(0,self.size-1)
                if (x,y) not in self.snake and not any((x,y)==(f[0],f[1]) for f in self.food):
                    # 随机食物类型
                    types = ["profit", "loss", "breakout", "reversal"]
                    weights = [0.4, 0.25, 0.2, 0.15]
                    food_type = random.choices(types, weights)[0]
                    self.food.append((x, y, food_type))
                    break
    
    def move(self):
        """移动蛇"""
        head = self.snake[0]
        new = (head[0] + self.dir[0], head[1] + self.dir[1])
        
        # 碰墙检测
        if not (0 <= new[0] < self.size and 0 <= new[1] < self.size):
            self.teleport()
            return
        
        # 撞自己检测
        if new in self.snake[1:]:
            self.teleport()
            return
        
        self.snake.insert(0, new)
        
        # 吃食物
        ate = False
        for i, food in enumerate(self.food):
            if new[0] == food[0] and new[1] == food[1]:
                self.take_trade(food[2])
                self.food.pop(i)
                ate = True
                break
        
        if not ate:
            self.snake.pop()
        
        self.make_food()
        
        # 更新历史数据
        self.money_history.append(self.money)
        if len(self.money_history) > 20:  # 只保留最近20个数据点
            self.money_history.pop(0)
    
    def take_trade(self, trade_type):
        """处理交易"""
        values = {"profit": 1500, "loss": -1200, "breakout": 2000, "reversal": 2500}
        pnl = values[trade_type]
        
        # 添加随机波动
        pnl = int(pnl * random.uniform(0.8, 1.2))
        
        self.money += pnl
        self.trade_count += 1
        self.trades.append(pnl)
        self.profit_history.append(pnl)
        
        # 更新统计
        self.trade_types[trade_type] += 1
        self.trade_values[trade_type].append(pnl)
        
        if pnl > 0:
            self.win_count += 1
            self.profit_total += pnl
            print(f"✨ {trade_type.upper()} 交易! +${pnl:,}")
            if len(self.snake) < 8:  # 最大长度限制
                self.snake.append(self.snake[-1])
        else:
            self.loss_count += 1
            self.loss_total += pnl
            print(f"💸 {trade_type.upper()} 交易! {pnl:,}")
    
    def teleport(self):
        """传送"""
        while True:
            x, y = random.randint(0,self.size-1), random.randint(0,self.size-1)
            if (x,y) not in self.snake and not any((x,y)==(f[0],f[1]) for f in self.food):
                self.snake[0] = (x,y)
                self.teleport_count += 1
                
                # 传送惩罚
                penalty = 2000 + (self.teleport_count - 1) * 500  # 递增惩罚
                self.money = max(10000, self.money - penalty)
                print(f"⚡ 传送 #{self.teleport_count}! -${penalty:,}, 资本: ${self.money:,}")
                
                if len(self.snake) > 2:
                    self.snake = self.snake[:-1]
                break
    
    def save_chart(self):
        """保存统计图表到文件"""
        try:
            if len(self.money_history) < 2:
                return
            
            # 创建图表
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))
            fig.suptitle('量化交易贪吃蛇 - 统计分析', fontsize=16)
            
            # 资本曲线
            ax1.plot(range(len(self.money_history)), self.money_history, 'b-', linewidth=2)
            ax1.set_title('💰 资本变化曲线')
            ax1.set_ylabel('资本 ($)')
            ax1.grid(True, alpha=0.3)
            ax1.axhline(y=self.initial_money, color='r', linestyle='--', alpha=0.5, label='初始资本')
            
            # 盈亏分布
            if self.trades:
                profits = [t for t in self.trades if t > 0]
                losses = [t for t in self.trades if t < 0]
                
                if profits:
                    ax2.hist(profits, bins=5, alpha=0.7, color='green', label='盈利交易')
                if losses:
                    ax2.hist(losses, bins=5, alpha=0.7, color='red', label='亏损交易')
                
                ax2.set_title('📊 盈亏分布')
                ax2.set_xlabel('盈亏金额 ($)')
                ax2.set_ylabel('频次')
                ax2.legend()
                ax2.grid(True, alpha=0.3)
            
            # 交易类型饼图
            if any(self.trade_types.values()):
                labels = []
                sizes = []
                colors = []
                for trade_type, count in self.trade_types.items():
                    if count > 0:
                        labels.append(trade_type.capitalize())
                        sizes.append(count)
                        colors.append(['green', 'red', 'orange', 'purple'][['profit', 'loss', 'breakout', 'reversal'].index(trade_type)])
                
                ax3.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%')
                ax3.set_title('🎯 交易类型分布')
            
            # 统计指标
            ax4.axis('off')
            stats_text = f"""
            📈 关键指标
            
            总交易次数: {self.trade_count}
            胜率: {(self.win_count/max(1,self.trade_count))*100:.1f}%
            
            总盈利: ${self.profit_total:,}
            总亏损: ${self.loss_total:,}
            净盈亏: ${self.profit_total + self.loss_total:,}
            
            平均盈利: ${self.profit_total/max(1,self.win_count):.0f}
            平均亏损: ${abs(self.loss_total/max(1,self.loss_count)):.0f}
            
            传送次数: {self.teleport_count}
            当前资本: ${self.money:,}
            """
            
            ax4.text(0.1, 0.5, stats_text, fontsize=12, verticalalignment='center',
                    bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
            
            plt.tight_layout()
            plt.savefig('trading_stats.png', dpi=100, bbox_inches='tight')
            plt.close()
            
            print("📈 统计图表已保存为 'trading_stats.png'")
            
        except Exception as e:
            print(f"⚠️ 图表生成失败: {e}")
    
    def show_detailed_stats(self):
        """显示详细统计"""
        self.clear()
        print("=" * 80)
        print("📊 详细交易统计分析 | Detailed Trading Analysis")
        print("=" * 80)
        
        # 时间统计
        play_time = time.time() - self.game_start_time
        
        # 计算各种指标
        win_rate = (self.win_count / max(1, self.trade_count)) * 100
        current_pnl = self.money - self.initial_money
        pnl_percentage = (current_pnl / self.initial_money) * 100
        
        print(f"⏱️ 游戏时间: {play_time:.1f}秒")
        print(f"💰 初始资本: ${self.initial_money:,}")
        print(f"💰 当前资本: ${self.money:,}")
        print(f"📈 净盈亏: ${current_pnl:+,} ({pnl_percentage:+.1f}%)")
        print(f"🤝 总交易次数: {self.trade_count}")
        print(f"🎯 胜率: {win_rate:.1f}%")
        print(f"⚡ 传送次数: {self.teleport_count}")
        
        if self.win_count > 0 and self.loss_count > 0:
            avg_profit = self.profit_total / self.win_count
            avg_loss = abs(self.loss_total) / self.loss_count
            profit_factor = avg_profit / avg_loss
            sharpe_ratio = (current_pnl / 100000) / (max(0.01, np.std(self.trades)/1000) if self.trades else 1)
            
            print(f"💎 平均盈利: ${avg_profit:.0f}")
            print(f"📉 平均亏损: ${avg_loss:.0f}")
            print(f"📊 盈亏比: {profit_factor:.2f}")
            print(f"📈 夏普比率: {sharpe_ratio:.2f}")
        
        # 交易类型详情
        print(f"\n📋 交易类型详细统计:")
        total_trades = sum(self.trade_types.values())
        for trade_type, count in self.trade_types.items():
            if count > 0:
                values = self.trade_values[trade_type]
                avg_val = sum(values) / len(values)
                max_val = max(values)
                min_val = min(values)
                percentage = (count / total_trades) * 100
                print(f"   {trade_type.capitalize():10}: {count:3}次 ({percentage:5.1f}%) | "
                      f"平均: ${avg_val:+6.0f} | 最大: ${max_val:+6.0f} | 最小: ${min_val:+6.0f}")
        
        # 最近交易历史
        if self.trades:
            print(f"\n📜 最近10次交易:")
            for i, trade in enumerate(self.trades[-10:], 1):
                status = "✅" if trade > 0 else "❌"
                print(f"   {i:2d}. {status} ${trade:+6,}")
        
        # 绘制ASCII图表
        if len(self.money_history) > 1:
            self.draw_ascii_chart(self.money_history, "资本变化趋势 (最近20次)")
        
        if self.trades:
            cumulative_pnl = np.cumsum(self.trades)
            if len(cumulative_pnl) > 1:
                self.draw_ascii_chart(list(cumulative_pnl[-15:]), "累计盈亏 (最近15次)")
        
        print("\n" + "=" * 80)
        print("按回车键继续游戏...")
        input()
    
    def run(self):
        """主游戏循环"""
        print("🐍 量化交易贪吃蛇 - 统计图表版")
        print("按 SPACE 查看详细统计")
        time.sleep(1.5)
        
        import threading
        running = True
        
        def input_thread():
            nonlocal running
            while running:
                try:
                    key = input().lower()
                    if key == 'q':
                        running = False
                    elif key == ' ':
                        self.show_detailed_stats()
                    elif key == 's' and self.dir != (0,1):
                        self.dir = (0,-1)
                    elif key == 'w' and self.dir != (0,-1):
                        self.dir = (0,1)
                    elif key == 'a' and self.dir != (1,0):
                        self.dir = (-1,0)
                    elif key == 'd' and self.dir != (-1,0):
                        self.dir = (1,0)
                    elif key == 'c':  # 保存图表
                        self.save_chart()
                except:
                    pass
        
        t = threading.Thread(target=input_thread, daemon=True)
        t.start()
        
        while running:
            self.clear()
            self.draw_stats_panel()
            self.draw_game_area()
            
            self.move()
            
            if self.money < 10000:
                print("\n💔 游戏结束 - 资本耗尽!")
                self.save_chart()
                break
            
            time.sleep(0.3)
        
        # 最终统计
        print(f"\n📊 最终统计:")
        print(f"最终资本: ${self.money:,}")
        print(f"总交易次数: {self.trade_count}")
        print(f"胜率: {(self.win_count/max(1,self.trade_count))*100:.1f}%")
        print(f"传送次数: {self.teleport_count}")
        self.save_chart()

if __name__ == "__main__":
    game = TradingSnakeWithStats()
    game.run()