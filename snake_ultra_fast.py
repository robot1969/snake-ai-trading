# 超快版贪吃蛇 - 极简优化
# Super Fast Snake - Minimal Optimized

import random
import os
import time

class FastSnake:
    def __init__(self):
        self.size = 10
        self.snake = [(5,5), (4,5), (3,5)]
        self.dir = (1,0)
        self.money = 100000
        self.food = []
        self.make_food()
    
    def clear(self):
        os.system('cls')
    
    def draw(self):
        self.clear()
        print(f"Money: ${self.money:,} | Snake: {len(self.snake)}")
        print("=" * 20)
        
        # 快速绘制
        for y in range(self.size):
            row = ""
            for x in range(self.size):
                if (x,y) == self.snake[0]:
                    row += "S"
                elif (x,y) in self.snake:
                    row += "o"
                elif (x,y) in self.food:
                    row += "$"
                else:
                    row += "."
            print(row)
        
        print("\nWASD=Move Q=Quit")
    
    def make_food(self):
        if len(self.food) < 2:
            while True:
                x, y = random.randint(0,self.size-1), random.randint(0,self.size-1)
                if (x,y) not in self.snake and (x,y) not in self.food:
                    self.food.append((x,y))
                    break
    
    def move(self):
        head = self.snake[0]
        new = (head[0] + self.dir[0], head[1] + self.dir[1])
        
        # 碰墙检测 - 传送
        if not (0 <= new[0] < self.size and 0 <= new[1] < self.size):
            self.teleport()
            return
        
        # 撞自己检测 - 传送
        if new in self.snake[1:]:
            self.teleport()
            return
        
        self.snake.insert(0, new)
        
        # 吃食物
        if new in self.food:
            self.food.remove(new)
            self.money += 1000
            print("+$1000!")
        else:
            self.snake.pop()
        
        self.make_food()
    
    def teleport(self):
        # 随机传送
        while True:
            x, y = random.randint(0,self.size-1), random.randint(0,self.size-1)
            if (x,y) not in self.snake and (x,y) not in self.food:
                self.snake[0] = (x,y)
                self.money = max(10000, self.money - 2000)
                print(f"Teleport! -$2000, Money: ${self.money:,}")
                if len(self.snake) > 2:
                    self.snake = self.snake[:-1]
                break
    
    def run(self):
        print("Fast Snake Game!")
        time.sleep(1)
        
        import threading
        running = True
        
        def input_thread():
            nonlocal running
            while running:
                try:
                    key = input().lower()
                    if key == 'q':
                        running = False
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
        
        # 启动输入线程
        t = threading.Thread(target=input_thread, daemon=True)
        t.start()
        
        # 主游戏循环
        while running:
            self.draw()
            self.move()
            
            if self.money < 10000:
                print("Game Over!")
                break
            
            time.sleep(0.3)
        
        print(f"Final Money: ${self.money:,}")

if __name__ == "__main__":
    game = FastSnake()
    game.run()