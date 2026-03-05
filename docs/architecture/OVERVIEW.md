# AetherMem Architecture Overview

## Project Structure

```
AetherMem/
├── README.md                 # 项目主文档
├── LICENSE                   # AGPL-3.0许可证
├── .gitignore               # Git忽略规则
├── pyproject.toml           # 项目配置
├── setup.py                 # 安装脚本
├── requirements.txt         # 依赖列表
│
├── config/                  # 配置文件
│   ├── config.example.yaml  # 配置模板
│   └── schemas/             # 配置验证模式
│
├── src/                     # 源代码
│   └── aethermem/          # 主包
│       ├── __init__.py     # 包入口
│       ├── core/           # 核心引擎
│       │   └── vwl_layer.py # 虚拟写层
│       ├── resonance/      # 共振引擎
│       │   ├── temporal_decay.py    # 时间衰减
│       │   └── interaction_metrics.py # 交互指标
│       ├── integration/    # 平台集成
│       │   ├── config_manager.py    # 配置管理
│       │   └── openclaw/   # OpenClaw集成
│       │       ├── adapter.py      # 适配器
│       │       ├── skill_registry.py # 技能注册
│       │       └── __init__.py
│       └── utils/          # 工具函数
│           ├── __init__.py
│           └── platform.py # 平台检测
│
├── tests/                  # 测试代码
│   ├── unit/              # 单元测试
│   ├── integration/       # 集成测试
│   └── test_*.py          # 测试文件
│
├── docs/                  # 文档
│   ├── architecture/      # 架构文档
│   ├── api/              # API文档
│   ├── CODE_OF_CONDUCT.md # 行为准则
│   ├── CONTRIBUTING.md   # 贡献指南
│   └── index.md          # 文档首页
│
├── examples/              # 示例代码
│   └── basic_protocol.py # 基础协议示例
│
├── scripts/              # 工具脚本
│   ├── add_license_headers.py  # 许可证头添加
│   ├── find_hardcoded_paths.py # 硬编码路径查找
│   ├── quick_validation.py     # 快速验证
│   └── validate_project.py     # 项目验证
│
└── releases/             # 发布文件
    └── dist/             # 构建包
        ├── aethermem-1.0.0-py3-none-any.whl
        └── aethermem-1.0.0.tar.gz
```

## Core Components

### 1. Virtual Write Layer (VWL)
- **Location**: `src/aethermem/core/vwl_layer.py`
- **Purpose**: 文件系统抽象，在只读环境中启用写操作
- **Key Features**: 内存映射持久化、原子同步操作、可配置一致性保证

### 2. Resonance Engine
- **Location**: `src/aethermem/resonance/`
- **Purpose**: 加权索引系统，基于时间衰减和交互频率
- **Key Features**: 时间衰减函数(λ=0.1/天)、交互频率指标、多因素评分算法

### 3. Continuity Protocol
- **Location**: `src/aethermem/__init__.py`
- **Purpose**: 统一协议接口，提供跨会话记忆连续性
- **Key Features**: 上下文恢复、状态持久化、共振计算、协议统计

### 4. Platform Integration
- **Location**: `src/aethermem/integration/`
- **Purpose**: 平台特定适配和配置管理
- **Key Features**: OpenClaw运行时集成、配置验证、技能注册

## Development Workflow

### Building
```bash
# 安装开发依赖
pip install -e .[dev]

# 构建发布包
python -m build

# 运行测试
pytest tests/ -v
```

### Code Quality
```bash
# 代码格式化
black src/ tests/ examples/

# 导入排序
isort src/ tests/ examples/

# 代码检查
flake8 src/ tests/ examples/

# 类型检查
mypy src/
```

## Configuration

### Protocol Configuration
See `config/config.example.yaml` for complete configuration options:

```yaml
protocol:
  version: "1.0"
  environment: "production"
  
vwl:
  enabled: true
  sync_interval: 300
  max_virtual_size: 1048576
  consistency: "eventual"
  
resonance:
  decay_rate: 0.1
  weight_factors:
    importance: 0.4
    recency: 0.3
    frequency: 0.3
```

## Installation Methods

### From GitHub
```bash
pip install git+https://github.com/kric030214-web/AetherMem.git
```

### Development Install
```bash
git clone https://github.com/kric030214-web/AetherMem.git
cd AetherMem
pip install -e .
```

## License
AGPL-3.0-or-later - See LICENSE file for details.
