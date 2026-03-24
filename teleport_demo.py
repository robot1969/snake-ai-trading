# 传送功能演示代码
# Teleport Feature Demo

import random
from collections import deque

# 模拟传送机制
class TeleportDemo:
    def __init__(self):
        self.snake_body = deque([(5, 5), (4, 5), (3, 5)])  # 模拟蛇身
        self.direction = (1, 0)  # 向右移动
        self.capital = 100000
        self.grid_size = 10
    
    def teleport_to_random_position(self):
        """随机传送到游戏场地中的任意位置"""
        print("💥 碰到墙了！触发传送...")
        
        # 获取所有可能的空位置
        empty_positions = []
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                if (x, y) not in self.snake_body:
                    empty_positions.append((x, y))
        
        # 记录旧位置
        old_pos = self.snake_body[0]
        print(f"📍 旧位置: {old_pos}")
        
        # 如果有空位置，随机选择一个
        if empty_positions:
            random_pos = random.choice(empty_positions)
            print(f"🎲 传送到新位置: {random_pos}")
            
            # 将蛇头传送到新位置
            self.snake_body = deque([random_pos] + list(self.snake_body)[:min(len(self.snake_body)-1, 5)])
            
            # 传送惩罚：减少一些长度和资本
            self.capital = max(10000, self.capital - 1000)
            print(f"💸 损失资本: $1,000, 剩余资本: ${self.capital:,}")
            
            if len(self.snake_body) > 3:
                removed = min(3, len(self.snake_body) - 2)
                for _ in range(removed):
                    if len(self.snake_body) > 2:
                        removed_segment = self.snake_body.pop()
                print(f"🐍 蛇身缩短: {removed} 段, 当前长度: {len(self.snake_body)}")
            
            # 传送特效描述
            print("✨ 传送特效: 紫色粒子爆散效果")
            print("🌟 视觉反馈: 蛇身闪烁并消失在旧位置，出现在新位置")
            
            return True
        else:
            print("❌ 没有可用传送位置")
            return False
    
    def simulate_move(self):
        """模拟移动和碰撞检测"""
        head = self.snake_body[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        
        print(f"\n🎮 从 {head} 向 {self.direction} 移动到 {new_head}")
        
        # 检查边界碰撞
        if (new_head[0] < 0 or new_head[0] >= self.grid_size or 
            new_head[1] < 0 or new_head[1] >= self.grid_size):
            print("🚫 撞到边界！")
            return self.teleport_to_random_position()
        
        # 检查自身碰撞
        if new_head in list(self.snake_body)[:-1]:
            print("🚫 撞到自己！")
            return self.teleport_to_random_position()
        
        # 正常移动
        self.snake_body.appendleft(new_head)
        self.snake_body.pop()
        print("✅ 正常移动")
        return True
    
    def display_status(self):
        """显示当前状态"""
        print(f"\n📍 蛇头位置: {self.snake_body[0]}")
        print(f"🐍 蛇身长度: {len(self.snake_body)}")
        print(f"💰 当前资本: ${self.capital:,}")

# 演示传送功能
if __name__ == "__main__":
    print("=" * 50)
    print("🐍 量化交易贪吃蛇 - 传送功能演示")
    print("=" * 50)
    
    demo = TeleportDemo()
    
    # 模拟几次移动，包括碰撞
    moves = [
        "向右移动",
        "向右移动", 
        "向右移动",
        "向右移动",  # 这里会撞墙
        "向左移动",
        "向左移动"   # 这里可能撞到自己
    ]
    
    for i, move_desc in enumerate(moves, 1):
        print(f"\n--- 第 {i} 次操作: {move_desc} ---")
        demo.display_status()
        
        # 设置方向
        if "向右" in move_desc:
            demo.direction = (1, 0)
        else:
            demo.direction = (-1, 0)
        
        # 执行移动
        success = demo.simulate_move()
        
        if success:
            print("✅ 操作成功")
        else:
            print("❌ 操作失败")
    
    print(f"\n--- 演示结束 ---")
    demo.display_status()
    print("\n🎯 传送功能特点:")
    print("• 撞墙或撞到自己不会游戏结束")
    print("• 随机传送到场地的空位置")
    print("• 传送有惩罚：损失$1,000和部分蛇身")
    print("• 华丽的紫色粒子传送特效")
    print("• 让游戏更有趣，减少挫败感")