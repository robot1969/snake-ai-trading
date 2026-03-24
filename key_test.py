# 按键测试脚本
# Key Test Script

import pygame
import sys

def test_key_detection():
    """测试按键检测"""
    pygame.init()
    screen = pygame.display.set_mode((600, 400))
    pygame.display.set_caption("Key Detection Test")
    clock = pygame.time.Clock()
    
    font = pygame.font.Font(None, 24)
    
    print("按键检测测试开始...")
    print("请尝试以下按键:")
    print("- a 键 (小写)")
    print("- A 键 (大写)")
    print("- 空格键")
    print("- ESC 键")
    print("- 方向键")
    print("按任意键退出")
    
    running = True
    detected_keys = set()
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.KEYDOWN:
                key_name = pygame.key.name(event.key)
                key_code = event.key
                
                if key_name not in detected_keys:
                    detected_keys.add(key_name)
                    print(f"检测到按键: {key_name} (代码: {key_code})")
                
                    # 测试pygame常量
                    if key_code == pygame.K_a:
                        print("✅ pygame.K_a 检测到")
                    elif key_code == pygame.K_SPACE:
                        print("✅ pygame.K_SPACE 检测到")
                    elif key_code == pygame.K_ESCAPE:
                        print("✅ pygame.K_ESCAPE 检测到")
                
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        # 显示检测结果
        screen.fill((50, 50, 50))
        text_lines = [
            f"已检测到的按键: {len(detected_keys)}",
            f"按键列表: {sorted(detected_keys)}",
            "按ESC退出"
        ]
        
        for i, line in enumerate(text_lines):
            text_surface = font.render(line, True, (255, 255, 255))
            screen.blit(text_surface, (20, 20 + i * 30))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    print("按键检测完成")

if __name__ == "__main__":
    test_key_detection()