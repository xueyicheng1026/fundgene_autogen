
async def calculator_tool(expression: str) -> dict:
    """
    执行金融数据分析相关的数学计算，包括基本运算和常用金融公式。
    
    参数:
        expression: 一个字符串表达式，如 "2 + 3 * 4" 或 "5000 * 0.05"。
                    也支持特殊命令格式：
                    - "percentage:100,25" 计算百分比(25/100 = 25%)
                    - "roi:1000,1200" 计算投资回报率((1200-1000)/1000 = 20%)
                    - "annualized:20,2" 计算年化收益率(对20%收益率按2年年化)
    
    返回:
        一个包含计算结果的字典 {"result": value}
    
    示例:
        calculator_tool("2 + 3") -> {"result": 5}
        calculator_tool("10 * 5 / 2") -> {"result": 25}
        calculator_tool("percentage:10000,2500") -> {"result": 25.0} (25%)
        calculator_tool("roi:1000,1200") -> {"result": 20.0} (20%的回报率)
        calculator_tool("annualized:20,2") -> {"result": 9.54} (2年内20%收益的年化率)
    """
    import re
    import math
    
    # 检查是否是特殊命令格式
    if ":" in expression:
        cmd, args = expression.split(":", 1)
        cmd = cmd.strip().lower()
        
        try:
            # 处理各种特殊金融计算命令
            if cmd == "percentage":
                # 计算百分比
                total, part = map(float, args.split(","))
                return {"result": (part / total) * 100 if total != 0 else 0}
                
            elif cmd == "roi":
                # 计算投资回报率 (Return on Investment)
                initial, final = map(float, args.split(","))
                return {"result": ((final - initial) / initial) * 100 if initial != 0 else 0}
                
            elif cmd == "annualized":
                # 计算年化收益率
                total_return, years = map(float, args.split(","))
                return {"result": (math.pow(1 + total_return/100, 1/years) - 1) * 100 if years > 0 else 0}
                
            elif cmd == "compound":
                # 计算复利
                principal, rate, years = map(float, args.split(","))
                rate = rate / 100  # 转换为小数
                return {"result": principal * math.pow(1 + rate, years)}
                
            elif cmd == "weighted_avg":
                # 计算加权平均值
                values_weights = args.split(";")
                total_weight = 0
                weighted_sum = 0
                for vw in values_weights:
                    value, weight = map(float, vw.split(","))
                    weighted_sum += value * weight
                    total_weight += weight
                return {"result": weighted_sum / total_weight if total_weight != 0 else 0}
                
            elif cmd == "asset_allocation":
                # 计算资产配置百分比
                values = list(map(float, args.split(",")))
                total = sum(values)
                percentages = [round((v / total) * 100, 2) if total != 0 else 0 for v in values]
                return {"result": percentages}
                
            else:
                return {"error": f"未知的特殊命令: {cmd}"}
                
        except Exception as e:
            return {"error": f"特殊命令计算错误: {str(e)}"}
    
    # 处理常规数学表达式
    try:
        # 创建安全的数学环境
        safe_globals = {
            "abs": abs, "round": round, "max": max, "min": min,
            "sum": sum, "pow": pow, 
            "sqrt": math.sqrt, "log": math.log, "log10": math.log10,
            "exp": math.exp, "floor": math.floor, "ceil": math.ceil,
            "sin": math.sin, "cos": math.cos, "tan": math.tan,
            "pi": math.pi, "e": math.e
        }
        
        # 验证表达式安全性
        if re.search(r"[^0-9\s\.\+\-\*\/\(\)\,\%\^]", re.sub(r"\b(abs|round|max|min|sum|pow|sqrt|log|log10|exp|floor|ceil|sin|cos|tan|pi|e)\b", "", expression)):
            return {"error": "表达式包含不允许的字符或函数"}
            
        # 预处理: 将^转换为**
        expression = expression.replace("^", "**")
        
        # 使用eval计算, 但提供有限的全局变量
        result = eval(expression, {"__builtins__": {}}, safe_globals)
        
        # 对结果进行格式化处理
        if isinstance(result, (int, float, complex)):
            # 对浮点数进行四舍五入到小数点后两位
            if isinstance(result, float):
                result = round(result, 2)
            return {"result": result}
        elif isinstance(result, (list, tuple)):
            # 如果结果是列表或元组，对每个元素进行格式化
            formatted = [round(x, 2) if isinstance(x, float) else x for x in result]
            return {"result": formatted}
        else:
            return {"error": "计算结果类型不支持"}
            
    except ZeroDivisionError:
        return {"error": "除数不能为零"}
    except ValueError as e:
        return {"error": f"值错误: {str(e)}"}
    except SyntaxError:
        return {"error": "表达式语法错误"}
    except NameError as e:
        return {"error": f"未知函数或变量: {str(e)}"}
    except Exception as e:
        return {"error": f"计算错误: {str(e)}"}