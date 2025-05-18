# 月子中心专家 Agent

本项目是一个基于MCP-Server的月子中心专家Agent，用于辅助销售为用户介绍月子中心的服务。

## 功能特点

1. **信息收集**：记录并处理用户与销售的语音交流，生成用户画像
2. **服务推荐**：基于用户画像，从销售心得数据库中匹配合适的话术
3. **案例展示**：展示与用户情况相近的成功合作案例

## 安装方法

```bash
# 安装依赖
pip install -r requirements.txt
```

## 使用方法

```bash
# 启动服务
python -m venv .venv

source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

## 项目结构

- `main.py`: 主程序入口
- `care_elite/`: 主要代码目录
  - `server.py`: MCP服务器实现
  - `tools/`: 工具函数
    - `information_collector.py`: 信息收集工具
    - `service_recommender.py`: 服务推荐工具
    - `case_presenter.py`: 案例展示工具
  - `voice/`: 语音处理相关
    - `speech_to_text.py`: 语音转文字
    - `text_to_speech.py`: 文字转语音
  - `database/`: 数据库操作
    - `user_profile.py`: 用户画像数据库
    - `sales_experience.py`: 销售心得数据库
    - `case_database.py`: 案例数据库
  - `utils/`: 工具函数目录
    - `profile_generator.py`: 用户画像生成器
    - `common.py`: 通用工具函数 