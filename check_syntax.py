#!/usr/bin/env python3
"""
语法检查脚本 - 绕过中文字符
Syntax Check Script - bypass Chinese characters
"""

import ast
import re

def check_syntax():
    """检查Python语法错误"""
    filename = 'quant_trading_snake_simple.py'
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            source = f.read()
        
        # Parse to check for syntax errors
        try:
            ast.parse(source)
            print('✅ 语法检查通过 - Syntax check PASSED')
            return True
        except SyntaxError as e:
            print(f'❌ 语法错误: {e}')
            
            # Show location
            lines = source.split('\n')
            error_line = e.lineno - 1 if hasattr(e, 'lineno') else 0
            print(f'错误位置: 第{error_line + 1}行')
            
            if 0 <= error_line < len(lines):
                print(f'错误行内容: {lines[error_line].strip()}')
                # Show context
                start = max(0, error_line - 2)
                end = min(len(lines), error_line + 2)
                print('上下文:')
                for i in range(start, end):
                    print(f'{i+1}: {lines[i]}')
            return False
            
    except Exception as e:
        print(f'❌ 检查时出现错误: {e}')
        return False

def check_common_issues():
    """检查常见问题"""
    filename = 'quant_trading_snake_simple.py'
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            source = f.read()
        
        # 检查未定义的变量
        issues = []
        
        # 检查常见的pygame错误
        if 'pygame.K_A' in source:
            issues.append('发现 pygame.K_A (不存在)')
        
        # 检查缩进问题
        lines = source.split('\n')
        for i, line in enumerate(lines):
            if line.strip().startswith('def ') or line.strip().startswith('class '):
                # 简单的缩进检查
                indent_level = len(line) - len(line.lstrip())
                if indent_level == 0:
                    issues.append(f'第{i+1}行: 函数/类定义缩进问题')
        
        if issues:
            print('⚠️ 发现的问题:')
            for issue in issues:
                print(f'  - {issue}')
        else:
            print('✅ 没有发现常见问题')
        
        return not issues
        
    except Exception as e:
        print(f'❌ 检查时出错: {e}')
        return False

def check_game_specific():
    """检查游戏特定的可能问题"""
    filename = 'quant_trading_snake_simple.py'
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            source = f.read()
        
        # 检查关键函数是否存在
        required_functions = [
            'handle_events',
            'update',
            'draw',
            'run',
            'reset_game'
        ]
        
        missing_functions = []
        for func in required_functions:
            if f'def {func}(' not in source:
                missing_functions.append(func)
        
        if missing_functions:
            print('⚠️ 缺失的函数:')
            for func in missing_functions:
                print(f'  - {func}')
        else:
            print('✅ 所有必要函数都存在')
        
        # 检查导入
        required_imports = [
            'import pygame',
            'import random',
            'import math',
            'from collections import deque',
            'from enum import Enum'
        ]
        
        missing_imports = []
        for imp in required_imports:
            if imp not in source:
                missing_imports.append(imp)
        
        if missing_imports:
            print('⚠️ 缺失的导入:')
            for imp in missing_imports:
                print(f'  - {imp}')
        else:
            print('✅ 所有必要的导入都存在')
        
        return not missing_functions and not missing_imports
        
    except Exception as e:
        print(f'❌ 检查时出错: {e}')
        return False

if __name__ == "__main__":
    print('正在检查量化交易贪吃蛇系统代码...')
    print('Checking Quant Trading Snake System...')
    
    # 基本语法检查
    syntax_ok = check_syntax()
    
    if syntax_ok:
        # 常见问题检查
        common_ok = not check_common_issues()
        
        if common_ok:
            # 游戏特定检查
            game_ok = check_game_specific()
            
            if game_ok:
                print('\\n🎉 所有检查都通过了！代码应该可以正常运行。')
                print('All checks passed! Code should run without errors.')
                print('\\n如果运行时仍有错误，可能是:')
                print('1. pygame模块未安装')
                print('2. 系统字体问题')
                print('3. 运行时权限问题')
            else:
                print('\\n⚠️ 发现了一些问题，建议修复后再运行。')
                print('Some issues found, suggest fixing before running.')
    
    print('\\n按任意键退出...')
    input()