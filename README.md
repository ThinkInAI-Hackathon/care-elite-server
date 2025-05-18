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

## 工作场景：
1. 知识库构建阶段（销售话术知识库、往期案例数据库）
2. 月子会所介绍阶段：输入对话信息，提取用户信息（mcp），记录进入数据库（mcp）
- 选择一个音频文件，输入：将这段语音转成文字并存入数据库当中，用户的手机号是：13598988984
3. 辅助销售场景：销售或者用户提问，语音识别（mcp），构建知识库检索+恢复（mcp），语音输出（mcp）
- 选择音频文件，向这位三胎妈妈推荐一下我们的月子服务，回答时只允许查询 mcp 知识库，不知道就说不知道，然后语音回答，总结回答时不要以销售的视角回答，因为这个场景下，用户和销售都在现场，侧重于说服用户，我希望你以亲切，有停顿的介绍。
4. 案例推荐场景：获取手机号为 13598988984 的用户信息（mcp），用获取的信息，检索案例库 rag（mcp），将得到的恢复通过语音（mcp）+图文的形式演示。
- 选择音频文件，输入：为手机号为13598988984这位妈妈演示与她情况相似的恢复案例。
