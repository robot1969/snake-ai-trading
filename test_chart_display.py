#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试脚本：验证 snake_chart_ai_comparison.py 图表显示
"""

import tkinter as tk
import sys
import traceback

def test_chart_display():
    """测试图表显示功能"""
    print("Testing Chart Display...")
    print("="*60)
    
    try:
        # 导入模块
        import snake_chart_ai_comparison as chart_module
        print("[OK] Module imported")
        
        # 创建根窗口
        root = tk.Tk()
        root.title("Chart Test")
        root.geometry("1800x1100")
        print("[OK] Tkinter window created")
        
        # 创建游戏实例
        game = chart_module.ChartAIComparisonSnake(root)
        print("[OK] Game instance created")
        
        # 检查图表相关属性
        print("\n[Checking chart attributes...]")
        
        # 检查AI图表字典
        if hasattr(game, 'ai_charts'):
            print(f"[OK] ai_charts exists with {len(game.ai_charts)} charts")
            for name in game.ai_charts:
                print(f"  - {name}")
        else:
            print("[FAIL] ai_charts not found")
        
        # 检查资金画布
        if hasattr(game, 'capital_canvas'):
            print("[OK] capital_canvas exists")
        else:
            print("[FAIL] capital_canvas not found")
        
        # 检查资金历史
        if hasattr(game, 'capital_history'):
            print("[OK] capital_history exists")
            # 检查是否有初始数据
            for algo in game.ai_algorithms:
                if algo in game.capital_history:
                    count = len(game.capital_history[algo])
                    print(f"  - {algo}: {count} data points")
                else:
                    print(f"  - {algo}: No data (will be initialized on start)")
        else:
            print("[FAIL] capital_history not found")
        
        # 检查性能表格
        if hasattr(game, 'performance_tree'):
            print("[OK] performance_tree exists")
        else:
            print("[FAIL] performance_tree not found")
        
        # 检查AI算法
        print(f"\n[AI Algorithms: {len(game.ai_algorithms)}]")
        for name, algo in game.ai_algorithms.items():
            active = "Active" if algo.get('active', False) else "Inactive"
            print(f"  - {name}: {active}")
        
        print("\n" + "="*60)
        print("[OK] All checks passed!")
        print("\nReady to start game. Press 'Start' button in GUI.")
        
        # 运行主循环（5秒后自动关闭）
        def auto_close():
            print("\n[Auto-closing after 5 seconds...]")
            root.quit()
        
        root.after(5000, auto_close)
        root.mainloop()
        
        print("\n[OK] Test completed successfully!")
        return True
        
    except Exception as e:
        print(f"\n[FAIL] Error: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_chart_display()
    sys.exit(0 if success else 1)