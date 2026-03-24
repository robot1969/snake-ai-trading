# 量化交易贪吃蛇 - 纯ASCII统计版
# Quantitative Trading Snake - Pure ASCII Statistics

import random
import os
import time
from collections import deque

class TradingSnakeStats:
    def __init__(self):
        self.size = 12
        self.snake = [(6,6), (5,6), (4,6)]
        self.dir = (1,0)
        self.money = 100000
        self.initial_money = 100000
        self.food = []
        
        # 交易统计
        self.trades = []
        self.money_history = deque([100000], maxlen=20)
        self.trade_count = 0
        self.win_count = 0
        self.loss_count = 0
        self.profit_total = 0
        self.loss_total = 0
        self.teleport_count = 0
        self.game_time = 0
        
        # 交易类型统计
        self.trade_types = {"profit": 0, "loss": 0, "breakout": 0, "reversal": 0}
        self.trade_values = {"profit": [], "loss": [], "breakout": [], "reversal": []}
        
        self.make_food()
        self.last_update = time.time()
    
    def clear(self):
        os.system('cls')
    
    def draw_barchart(self, data, labels, title, height=8, width=50):
        """绘制ASCII柱状图"""
        if not data:
            return
        
        print(f"\n📊 {title}")
        print("=" * width)
        
        max_val = max(data) if max(data) > 0 else 1
        bar_width = (width - 20) // len(data)
        
        # 绘制柱状图
        for level in range(height, 0, -1):
            threshold = (max_val * level) / height
            line = "  "
            for i, val in enumerate(data):
                if val >= threshold:
                    bar_length = int((val / max_val) * bar_width * 0.8)
                    line += "█" * bar_length + " " * (bar_width - bar_length)
                else:
                    line += " " * bar_width
            print(line)
        
        # 底部和标签
        line = "  "
        for i in range(len(data)):
            line += "─" * bar_width
        print(line + "┘")
        
        # 数值标签
        line = "  "
        for i, val in enumerate(data):
            line += f"{val:>{bar_width}}"
        print(line)
        
        # 类型标签
        line = "  "
        for i, label in enumerate(labels):
            line += f"{label[:bar_width]:^{bar_width}}"
        print(line)
        print("=" * width)
    
    def draw_linechart(self, data, title, height=6, width=40):
        """绘制ASCII折线图"""
        if len(data) < 2:
            return
        
        print(f"\n📈 {title}")
        print("=" * width)
        
        max_val = max(data)
        min_val = min(data)
        range_val = max_val - min_val if max_val != min_val else 1
        
        # 数据点数量限制
        points = data[-width:] if len(data) > width else data
        
        # 绘制图表
        for level in range(height, 0, -1):
            threshold = min_val + (range_val * level / height)
            line = ""
            for i, val in enumerate(points):
                if i == len(points) - 1:  # 最后一个点
                    line += "●" if val >= threshold else " "
                else:
                    next_val = points[i+1] if i+1 < len(points) else val
                    if val >= threshold and next_val >= threshold:
                        line += "━"
                    elif val >= threshold and next_val < threshold:
                        line += "┃"
                    elif val < threshold and next_val >= threshold:
                        line += "┃"
                    else:
                        line += " "
            print(f"  {line}")
        
        # 底部
        print("  " + "─" * len(points))
        
        # 显示关键数值
        if len(points) <= 10:
            value_line = "  "
            for i, val in enumerate(points[::2]):  # 每隔一个显示
                value_line += f"{val:>6}"
            print(value_line)
        
        print("=" * width)
    
    def draw_main_stats(self):
        """绘制主要统计信息"""
        print("🐍 量化交易贪吃蛇 - 实时统计面板")
        print("=" * 70)
        
        # 基础统计
        win_rate = (self.win_count / max(1, self.trade_count)) * 100
        current_pnl = self.money - self.initial_money
        pnl_percentage = (current_pnl / self.initial_money) * 100
        game_time = int(time.time() - self.last_update)
        
        # 第一行统计
        print(f"💰 资本: ${self.money:>10,} | 📈 盈亏: {current_pnl:>+9,} ({pnl_percentage:+5.1f}%) | ⏱️ 时间: {game_time:3d}秒")
        
        # 第二行统计
        print(f"🤝 交易: {self.trade_count:3d} | 🎯 胜率: {win_rate:5.1f}% | ⚡ 传送: {self.teleport_count:2d} | 🐍 长度: {len(self.snake):2d}")
        
        # 第三行统计
        if self.profit_total > 0:
            avg_profit = self.profit_total / max(1, self.win_count)
            avg_loss = abs(self.loss_total) / max(1, self.loss_count)
            profit_factor = avg_profit / max(0.1, avg_loss)
            print(f"💎 平均盈利: ${avg_profit:>6.0f} | 📉 平均亏损: ${avg_loss:>6.0f} | 📊 盈亏比: {profit_factor:>4.2f}")
        
        print("=" * 70)
    
    def draw_game_area(self):
        """绘制游戏区域"""
        print("\n🎮 游戏区域 | Game Area")
        print("-" * 30)
        
        for y in range(self.size):
            row = ""
            for x in range(self.size):
                if (x,y) == self.snake[0]:
                    row += "S"
                elif (x,y) in self.snake:
                    row += "o"
                elif (x,y) in [f[:2] for f in self.food]:
                    # 找到食物类型
                    food_type = next(f[2] for f in self.food if f[0]==x and f[1]==y)
                    symbols = {"profit": "$", "loss": "L", "breakout": "B", "reversal": "R"}
                    row += symbols.get(food_type, "?")
                else:
                    row += "."
            print(row)
        
        print("-" * 30)
        print("控制: WASD=移动 SPC=统计 C=图表 Q=退出")
        print("符号: $盈利 L亏损 B突破 R反转")
    
    def make_food(self):
        """生成食物"""
        if len(self.food) < 3:
            while True:
                x, y = random.randint(0,self.size-1), random.randint(0,self.size-1)
                if (x,y) not in self.snake and not any((x,y)==(f[0],f[1]) for f in self.food):
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
        self.money_history.append(self.money)
    
    def take_trade(self, trade_type):
        """处理交易"""
        values = {"profit": 1500, "loss": -1200, "breakout": 2000, "reversal": 2500}
        pnl = int(values[trade_type] * random.uniform(0.8, 1.2))
        
        self.money += pnl
        self.trade_count += 1
        self.trades.append(pnl)
        
        # 更新统计
        self.trade_types[trade_type] += 1
        self.trade_values[trade_type].append(pnl)
        
        if pnl > 0:
            self.win_count += 1
            self.profit_total += pnl
            print(f"✨ {trade_type.upper()} +${pnl:,}")
            if len(self.snake) < 8:
                self.snake.append(self.snake[-1])
        else:
            self.loss_count += 1
            self.loss_total += pnl
            print(f"💸 {trade_type.upper()} {pnl:,}")
    
    def teleport(self):
        """传送"""
        while True:
            x, y = random.randint(0,self.size-1), random.randint(0,self.size-1)
            if (x,y) not in self.snake and not any((x,y)==(f[0],f[1]) for f in self.food):
                self.snake[0] = (x,y)
                self.teleport_count += 1
                
                penalty = 2000 + (self.teleport_count - 1) * 500
                self.money = max(10000, self.money - penalty)
                print(f"⚡ 传送#{self.teleport_count} -${penalty:,}")
                
                if len(self.snake) > 2:
                    self.snake = self.snake[:-1]
                break
    
    def show_statistics(self):
        """显示详细统计"""
        self.clear()
        print("📊 详细统计分析报告")
        print("=" * 80)
        
        # 基础指标
        win_rate = (self.win_count / max(1, self.trade_count)) * 100
        current_pnl = self.money - self.initial_money
        pnl_percentage = (current_pnl / self.initial_money) * 100
        
        print(f"💰 资本分析:")
        print(f"   初始资本: ${self.initial_money:,}")
        print(f"   当前资本: ${self.money:,}")
        print(f"   净盈亏: ${current_pnl:+,} ({pnl_percentage:+.1f}%)")
        
        print(f"\n📈 交易绩效:")
        print(f"   总交易次数: {self.trade_count}")
        print(f"   盈利交易: {self.win_count}")
        print(f"   亏损交易: {self.loss_count}")
        print(f"   胜率: {win_rate:.1f}%")
        
        if self.win_count > 0 and self.loss_count > 0:
            avg_profit = self.profit_total / self.win_count
            avg_loss = abs(self.loss_total) / self.loss_count
            profit_factor = avg_profit / avg_loss
            
            print(f"   平均盈利: ${avg_profit:.0f}")
            print(f"   平均亏损: ${avg_loss:.0f}")
            print(f"   盈亏比: {profit_factor:.2f}")
        
        print(f"\n⚡ 风险控制:")
        print(f"   传送次数: {self.teleport_count}")
        print(f"   传送总成本: ${self.teleport_count * 2000 + (self.teleport_count-1)*self.teleport_count//2*500:,}")
        print(f"   当前蛇身长度: {len(self.snake)}")
        
        # 交易类型图表
        if any(self.trade_types.values()):
            type_data = [self.trade_types[t] for t in ["profit", "loss", "breakout", "reversal"]]
            type_labels = ["盈利", "亏损", "突破", "反转"]
            self.draw_barchart(type_data, type_labels, "交易类型分布")
        
        # 盈亏趋势图
        if len(self.money_history) > 1:
            self.draw_linechart(list(self.money_history), "资本变化趋势")
        
        # 最近交易记录
        if self.trades:
            print(f"\n📜 最近10次交易记录:")
            print("-" * 50)
            for i, trade in enumerate(self.trades[-10:], 1):
                status = "✅盈利" if trade > 0 else "❌亏损"
                print(f"   {i:2d}. {status:6} ${trade:+6,}")
        
        print("\n" + "=" * 80)
        print("按回车键返回游戏...")
        input()
    
    def show_charts(self):
        """显示图表"""
        self.clear()
        print("📊 实时图表分析")
        print("=" * 70)
        
        # 资本变化图表
        if len(self.money_history) > 1:
            self.draw_linechart(list(self.money_history), "实时资本变化 (最近20次)")
        
        # 交易频率分析
        if self.trades:
            # 将交易分组统计
            profit_trades = [t for t in self.trades if t > 0]
            loss_trades = [t for t in self.trades if t < 0]
            
            # 盈亏对比
            data = []
            labels = []
            
            if profit_trades:
                data.append(sum(profit_trades))
                labels.append("总盈利")
            if loss_trades:
                data.append(abs(sum(loss_trades)))
                labels.append("总亏损")
            
            if data:
                self.draw_barchart(data, labels, "总盈亏对比")
            
            # 平均值对比
            avg_data = []
            avg_labels = []
            
            if profit_trades:
                avg_data.append(sum(profit_trades)/len(profit_trades))
                avg_labels.append("平均盈利")
            if loss_trades:
                avg_data.append(abs(sum(loss_trades))/len(loss_trades))
                avg_labels.append("平均亏损")
            
            if avg_data:
                self.draw_barchart(avg_data, avg_labels, "平均单次交易")
        
        # 交易类型详细统计
        if any(self.trade_types.values()):
            print(f"\n📋 交易类型详细统计:")
            types = ["profit", "loss", "breakout", "reversal"]
            for trade_type in types:
                count = self.trade_types[trade_type]
                if count > 0:
                    values = self.trade_values[trade_type]
                    avg_val = sum(values) / len(values)
                    max_val = max(values)
                    min_val = min(values)
                    print(f"   {trade_type.capitalize():8}: {count:2d}次 | "
                          f"平均: ${avg_val:+6.0f} | "
                          f"范围: ${min_val:+6.0f} ~ ${max_val:+6.0f}")
        
        print("\n" + "=" * 70)
        print("按回车键返回游戏...")
        input()
    
    def run(self):
        """主游戏循环"""
        print("🐍 量化交易贪吃蛇 - 统计图表版")
        print("控制: WASD移动, SPC详细统计, C图表, Q退出")
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
                        self.show_statistics()
                    elif key == 'c':
                        self.show_charts()
                    elif key == 'w' and self.dir != (0,1):
                        self.dir = (0,-1)
                    elif key == 's' and self.dir != (0,-1):
                        self.dir = (0,1)
                    elif key == 'a' and self.dir != (1,0):
                        self.dir = (-1,0)
                    elif key == 'd' and self.dir != (-1,0):
                        self.dir = (1,0)
                except:
                    pass
        
        t = threading.Thread(target=input_thread, daemon=True)
        t.start()
        
        while running:
            self.clear()
            self.draw_main_stats()
            self.draw_game_area()
            
            self.move()
            
            if self.money < 10000:
                print("\n💔 游戏结束 - 资本耗尽!")
                time.sleep(2)
                break
            
            time.sleep(0.25)
        
        # 最终报告
        self.show_statistics()

if __name__ == "__main__":
    game = TradingSnakeStats()
    game.run()