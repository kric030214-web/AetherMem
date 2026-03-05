## 0x06 Installation and Usage

### Platform Requirements
- **Python**: 3.8 or higher
- **Operating Systems**: Windows 10+, macOS 10.15+, Linux (Ubuntu 20.04+, CentOS 8+, etc.)
- **Dependencies**: Pure Python, no platform-specific binaries

### Installation Methods

#### **Method 1: Install from GitHub (Recommended)**
```bash
pip install git+https://github.com/kric030214-web/AetherMem.git
```

#### **Method 2: Clone and Install (Development)**
```bash
git clone https://github.com/kric030214-web/AetherMem.git
cd AetherMem
pip install -e .
```

#### **Method 3: Install from Local Build**
```bash
# After cloning
cd AetherMem
pip install .
```

### Platform-Specific Setup

#### **Linux/macOS**
```bash
# Install Python 3.8+ if not already installed
# Ubuntu/Debian:
sudo apt update && sudo apt install python3 python3-pip

# macOS (with Homebrew):
brew install python

# Install AetherMem
pip install git+https://github.com/kric030214-web/AetherMem.git
```

#### **Windows**
```powershell
# Install Python 3.8+ from python.org
# Then install AetherMem
pip install git+https://github.com/kric030214-web/AetherMem.git

# Or using PowerShell with admin rights:
python -m pip install git+https://github.com/kric030214-web/AetherMem.git
```

#### **All Platforms (Development Install)**
```bash
git clone https://github.com/kric030214-web/AetherMem.git
cd AetherMem
pip install -e .
```

### Basic Protocol Initialization
```python
from aethermem import ContinuityProtocol

# Initialize protocol with configuration
protocol = ContinuityProtocol(config_path="config/protocol.yaml")
print(f"Restored {len(context)} bytes of protocol state")

# Persist state with weighted indexing
result = protocol.persist_state(
    state_vector=state_data,
    importance=2,
    metadata={"session_id": "sess_123"}
)

# Retrieve resonance-weighted context
weighted_context = protocol.get_weighted_context(
    entity_id="agent_001",
    max_bytes=20000
)
