#!/usr/bin/env python3
"""
ESC和空格键无反应问题修复
ESC and Space Key Unresponsive Fix
"""

import pygame
import sys

def create_debug_version():
    """创建一个带有详细调试信息的版本"""
    
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Quant Trading Snake - Debug Version")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 24)
    
    # 游戏对象
    try:
        # 模拟原有的类和逻辑
        from collections import deque
        from enum import Enum
        from datetime import datetime
        
        class MarketCondition(Enum):
            BULL = "bull"
            BEAR = "bear"
            SIDEWAYS = "sideways"
            VOLATILE = "volatile"

        class TradingState(Enum):
            MENU = "menu"
            TRADING = "trading"
            AUTO_TRADING = "auto_trading"
            PAUSED = "paused"
            GAME_OVER = "game_over"

        # 简化版的游戏状态
        state = TradingState.MENU
        event_queue = []
        
        def handle_events():
            """事件处理函数"""
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                
                if event.type == pygame.KEYDOWN:
                    print(f"按键事件: {pygame.key.name(event.key)} (代码: {event.key})")
                    event_queue.append((event.type, event.key))
                    
                    if state == TradingState.MENU:
                        if event.key == pygame.K_SPACE:
                            print("状态: MENU -> TRADING")
                            state = TradingState.TRADING
                        elif event.key == pygame.K_ESCAPE:
                            print("状态: MENU -> 退出")
                            return False
                    
                    elif state == TradingState.TRADING:
                        if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                            print(f"手动控制: {pygame.key.name(event.key)}")
                            state = TradingState.TRADING
                        elif event.key == pygame.K_a:
                            print("状态: TRADING -> AUTO_TRADING")
                            state = TradingState.AUTO_TRADING
                        elif event.key == pygame.K_p:
                            print("状态: TRADING -> PAUSED")
                            state = TradingState.PAUSED
                        elif event.key == pygame.K_SPACE:
                            print("空格键被按下 (交易中)")
                        elif event.key == pygame.K_m:
                            print("M键被按下: AUTO -> MANUAL")
                            state = TradingState.TRADING
                        elif event.key == pygame.K_ESCAPE:
                            print("状态: TRADING -> MENU")
                            state = TradingState.MENU
                    
                    elif state == TradingState.AUTO_TRADING:
                        if event.key == pygame.K_p:
                            print("状态: AUTO_TRADING -> PAUSED")
                            state = TradingState.AUTO_TRADING
                        elif event.key == pygame.K_m:
                            print("M键被按下: AUTO -> MANUAL")
                            state = TradingState.TRADING
                        elif event.key == pygame.K_SPACE:
                            print("空格键被按下 (自动模式)")
                        elif event.key == pygame.K_UP:
                            print("自动模式: 方向干预")
                            state = TradingState.AUTO_TRADING
                        elif event.key == pygame.K_DOWN:
                            print("自动模式: 方向干预")
                            state = TradingState.AUTO_TRADING
                        elif event.key == pygame.K_LEFT:
                            print("自动模式: 方向干预")
                            state = TradingState.AUTO_TRADING
                        elif event.key == pygame.K_RIGHT:
                            print("自动模式: 方向干预")
                            state = TradingState.AUTO_TRADING
                        elif event.key == pygame.K_ESCAPE:
                            print("状态: AUTO_TRADING -> MENU")
                            state = TradingState.MENU
                    
                    elif state == TradingState.PAUSED:
                        if event.key == pygame.K_p:
                            print("状态: PAUSED -> TRADING")
                            state = TradingState.TRADING
                        elif event.key == pygame.K_SPACE:
                            print("空格键被按下 (暂停时)")
                        elif event.key == pygame.K_ESCAPE:
                            print("状态: PAUSED -> MENU")
                            state = TradingState.MENU
            
            return True
        
        def update_display():
            """更新显示"""
            screen.fill((30, 30, 40))
            
            # 显示状态和事件队列
            info_lines = [
                f"当前状态: {state.value}",
                f"事件队列长度: {len(event_queue)}",
                "最近事件:",
                ""
            ]
            
            # 显示最近的按键事件
            for event in event_queue[-5:]:  # 显示最近5个事件
                info_lines[-1] += f"  {event[0]} - {pygame.key.name(event[1])}"
            
            # 显示提示信息
            info_lines.extend([
                "",
                "按键测试说明:",
                "- 主菜单: 空格键开始游戏，ESC退出",
                "- 游戏中: 方向键移动，A键自动模式",
                "- 任何状态: ESC返回主菜单",
                "",
                "预期行为:",
                "- 主菜单空格键 → 应该切换到游戏状态",
                "- 游戏中空格键 → 应该被识别",
                "- 游戏中ESC键 → 应该切换到主菜单"
                "- 自动模式M键 → 应该切换到手动模式",
                ""
                "调试信息: 查看控制台输出"
            ])
            
            y_offset = 50
            for line in info_lines:
                text_surface = font.render(line, True, (200, 200, 200))
                screen.blit(text_surface, (50, y_offset))
                y_offset += 30
            
            # 显示按键状态
            if event_queue:
                key_status = "最近按键: 无"
                if event_queue:
                    last_event = event_queue[-1]
                    if last_event[0] == pygame.KEYDOWN:
                        key_status = f"最近按键: {pygame.key.name(last_event[1])}"
                        if len(event_queue) > 1:
                            prev_event = event_queue[-2]
                            if prev_event[0] == pygame.KEYDOWN and prev_event[1] == last_event[1]:
                                key_status += f" (重复按键)"
                
                status_color = (100, 255, 100) if key_status == "无" else (255, 255, 100)
                status_text = font.render(key_status, True, status_color)
                screen.blit(status_text, (50, 450))
            
            pygame.display.flip()
            clock.tick(30)
        
        # 主循环
        running = True
        while running:
            running = handle_events()
            update_display()
        
        pygame.quit()
    
    if __name__ == "__main__":
        print("=== ESC和空格键无反应问题诊断 ===")
        print("这是一个调试版本，专门用于诊断按键问题")
        print()
        
        try:
            create_debug_version()
        except KeyboardInterrupt:
            print("用户中断了程序")
        except Exception as e:
            print(f"程序出错: {e}")