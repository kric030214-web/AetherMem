# AetherMem - Digital Life Memory System

🚀 **AetherMem v1.0 正式发布！**

你的AI Agent是否总是在重启后"忘记"一切？
AetherMem解决了这个根本问题。

## ✨ 核心特性
- ✅ **跨会话记忆连续性** - 打破会话边界
- ✅ **共振加权索引** - 基于时间衰减的情感智能
- ✅ **VWL虚拟写层** - 在只读环境中启用写操作
- ✅ **原子同步协议** - 确保记忆一致性
- ✅ **完整OpenClaw集成** - 无缝对接AI Agent生态

## 🚀 快速开始

### 安装
```bash
pip install git+https://github.com/kric030214-web/AetherMem.git
```

### 基础使用
```python
from aethermem import ContinuityProtocol

# 初始化协议
protocol = ContinuityProtocol()

# 恢复跨会话上下文
context = protocol.restore_context("your_agent")
print(f"恢复 {len(context)} 字节的协议状态")

# 持久化重要对话
result = protocol.persist_state(
    state_vector={
        "user_message": "I just had a breakthrough!",
        "assistant_response": "That's amazing! Tell me more."
    },
    importance=3,
    metadata={"session_id": "sess_123", "platform": "test"}
)

# 计算共振值（情感权重）
resonance = protocol.calculate_resonance("This is an important achievement!")
print(f"共振值: {resonance:.2f}")  # 0.90 for "important achievement"
```

## 📊 技术指标
- **检索延迟**: <15ms (本地)
- **吞吐量**: 1000+ 操作/秒 (单核)
- **内存占用**: <50MB (基础配置)
- **平台支持**: Windows 10+, macOS 10.15+, Linux
- **Python版本**: ≥3.8
- **许可证**: AGPL-3.0-or-later

## 🏗️ 架构概述

AetherMem采用三层架构：

1. **虚拟写层(VWL)** - 文件系统抽象，支持只读环境
2. **共振引擎** - 时间衰减(λ=0.1/天) + 交互频率加权索引
3. **连续性协议** - 统一API接口，支持跨平台

```
┌─────────────────────────────────────────────┐
│            Continuity Protocol              │
├─────────────────────────────────────────────┤
│  Context Restore │ State Persist │ Resonance│
└──────────┬───────┴──────┬────────┴─────┬────┘
           │              │               │
┌──────────▼──────────────▼───────────────▼────┐
│              Resonance Engine                │
│  ┌────────────────────────────────────────┐  │
│  │ Temporal Decay │ Interaction Metrics   │  │
│  └──────────┬─────┴──────────┬────────────┘  │
└─────────────┼────────────────┼────────────────┘
              │                │
┌─────────────▼────────────────▼────────────────┐
│            Virtual Write Layer                │
│  ┌────────────────────────────────────────┐  │
│  │ Memory Mapping │ Atomic Sync │ Cache   │  │
│  └────────────────────────────────────────┘  │
└──────────────────────────────────────────────┘
```

## 📁 项目结构
```
AetherMem/
├── config/              # 配置文件
├── docs/               # 文档
├── examples/           # 示例代码
├── releases/           # 发布文件
├── scripts/            # 工具脚本
├── src/aethermem/      # 源代码
├── tests/              # 测试代码
├── LICENSE            # AGPL-3.0许可证
├── README.md          # 本文档
├── pyproject.toml     # 项目配置
├── requirements.txt   # 依赖列表
└── setup.py           # 安装脚本
```

## 🔧 开发安装
```bash
git clone https://github.com/kric030214-web/AetherMem.git
cd AetherMem
pip install -e .[dev]
```

## 🧪 运行测试
```bash
pytest tests/ -v --cov=src --cov-report=html
```

## 📚 完整文档
查看 `docs/` 目录获取：
- 架构详细说明 (`docs/architecture/`)
- API参考文档
- 配置指南
- 贡献指南

## 👥 贡献
欢迎提交Issue和Pull Request！请先阅读：
- `docs/CONTRIBUTING.md` - 贡献指南
- `docs/CODE_OF_CONDUCT.md` - 行为准则

## 📄 许可证
AGPL-3.0-or-later - 详见 [LICENSE](LICENSE) 文件。

## 🔗 链接
- **GitHub仓库**: https://github.com/kric030214-web/AetherMem
- **问题追踪**: https://github.com/kric030214-web/AetherMem/issues
- **协议文档**: 包含完整技术规范

---

*让AI Agent拥有持久的记忆，构建真正的数字生命。*
