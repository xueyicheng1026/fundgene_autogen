#!/usr/bin/env python3
import os
import sys
import argparse
from pathlib import Path
from simulation_app import SimulationApp

def main():
    parser = argparse.ArgumentParser(description="2008金融危机基金投资模拟系统")
    parser.add_argument('--capital', type=float, default=100000, help="初始资金，默认100000元")
    parser.add_argument('--debug', action='store_true', help="启用调试模式")
    parser.add_argument('--import-file', type=str, help="导入历史投资记录文件路径")
    args = parser.parse_args()
    
    # 获取当前脚本所在目录
    current_dir = Path(__file__).parent
    
    # 创建保存目录
    save_dir = current_dir / "save"
    os.makedirs(save_dir, exist_ok=True)
    
    # 原始数据目录
    original_data_dir = Path(os.path.dirname(current_dir)) /"database"/ "scene" / "2008金融危机"
    
    print("启动2008金融危机投资模拟系统...")
    print(f"数据目录: {original_data_dir}")
    print(f"保存目录: {save_dir}")
    
    if args.debug:
        print("调试模式已启用")
    
    try:
        app = SimulationApp(current_dir, args.capital)
        
        # 如果指定了导入文件，则先导入历史记录
        if args.import_file:
            print(f"正在导入历史记录: {args.import_file}")
            import_result = app.simulator.import_history(args.import_file)
            if import_result['success']:
                print(f"成功导入历史记录，从 {import_result['last_date']} 继续投资")
            else:
                print(f"导入历史记录失败: {import_result['message']}")
                return
        
        app.start()
    except KeyboardInterrupt:
        print("\n程序被用户中断")
    except Exception as e:
        print(f"\n程序遇到错误: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()
    
    print("\n感谢使用2008金融危机投资模拟系统!")
    
if __name__ == "__main__":
    main()
