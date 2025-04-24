# AutoGen 使用文档

## 1. AutoGen 0.4 简介
AutoGen 0.4 是一个全新的多代理框架，旨在提供更强大、可扩展且易于使用的工具，用于构建 AI 代理。主要特性包括：
- 异步消息传递
- 支持分布式代理
- 模块化设计，易于扩展

## 2. 官方文档
### 2.1 核心功能
- **ConversableAgent**：基础代理类型，用于处理消息交换和响应生成。
- **AutoGen Studio**：提供无代码 GUI，用于快速构建多代理应用。
- **AutoGen Bench**：提供代理性能评估的基准测试套件。

### 2.2 安装与配置
```bash
pip install autogen
```

## 3. GitHub 资源
### 3.1 仓库地址
- [AutoGen GitHub 仓库](https://github.com/microsoft/autogen)

### 3.2 社区贡献
- **AutoGen Studio**：正在重写以支持 AutoGen 0.4 的新特性。
- **示例代码**：提供多代理通信的示例，如信息验证工作流。

## 4. 使用示例
### 4.1 创建代理
```python
from autogen import ConversableAgent

agent1 = ConversableAgent(name="Agent1")
agent2 = ConversableAgent(name="Agent2")
```

### 4.2 代理通信
```python
response = agent1.send_message("Hello, Agent2!", agent2)
print(response)
```

## 5. 注意事项
- AutoGen 0.4 目前为预览版，接口可能变动。
- 建议使用完全限定的路径调用可执行文件。

---

如需进一步了解，请参考 [官方文档](https://docs.microsoft.com/autogen) 或 [GitHub 仓库](https://github.com/microsoft/autogen)。