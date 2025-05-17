# MCP服务器 API参考

## API基本信息

- 基础URL: `http://your-server-address:8000`
- API前缀: `/api/v1`
- 完整API URL: `http://your-server-address:8000/api/v1`

## 认证

大多数API端点需要认证。认证方式采用Bearer令牌:

```
Authorization: Bearer <token>
```

## 健康检查

### 检查服务器状态

```
GET /api/v1/health
```

响应示例:

```json
{
  "status": "ok",
  "service": "mcp-server"
}
```

## WebSocket API

### 实时对话

建立WebSocket连接进行实时交互:

```
WebSocket: /ws/{client_id}
```

#### 消息类型

1. 语音输入:

```json
{
  "type": "speech",
  "text": "我对母乳喂养很关注",
  "speaker": "customer"  // customer或sales
}
```

2. 销售指令:

```json
{
  "type": "command",
  "command": "小美，根据宝妈张娜的情况，我们有什么样的专业服务适合她?"
}
```

3. 阶段切换:

```json
{
  "type": "stage_change",
  "stage": "consultation"  // initial, tour, consultation, case_presentation
}
```

#### 响应类型

1. 信息收集响应:

```json
{
  "type": "info_collection",
  "extracted": {
    "name": "张娜",
    "age": 32,
    "pregnancy_status": "产后",
    "birth_type": "剖腹产"
  }
}
```

2. 反馈分析响应:

```json
{
  "type": "feedback_analysis",
  "analysis": {
    "interests": ["母婴护理", "产后修复"],
    "concerns": ["母乳喂养", "恢复速度"],
    "sentiment": "正面",
    "priority_needs": ["母乳喂养指导"]
  }
}
```

3. AI回应:

```json
{
  "type": "ai_response",
  "response": "根据您的情况，我们的母乳喂养指导服务非常适合您。我们的专业顾问会帮助您解决泌乳不足的问题，并教您正确的哺乳姿势..."
}
```

4. 销售指令回应:

```json
{
  "type": "ai_command_response",
  "response": "针对张娜宝妈剖腹产后的情况，我们有专业的产后修复课程，包括伤口愈合护理和腹直肌修复。同时，考虑到她对母乳喂养的关注，我们的母乳喂养专家会提供一对一指导..."
}
```

5. 相似案例:

```json
{
  "type": "similar_cases",
  "cases": [
    {
      "case_id": "case_12",
      "title": "剖腹产二胎产妇的恢复案例",
      "description": "32岁张女士，剖腹产二胎，入住本中心28天，在专业指导下解决了产后恢复慢、母乳不足等问题...",
      "before_after_images": ["url1", "url2"],
      "testimonial": "在这里的28天，我的恢复速度超出预期..."
    }
  ]
}
```

## REST API

### 知识库管理

#### 列出知识库文档

```
GET /api/v1/knowledge
```

#### 上传知识库文档

```
POST /api/v1/knowledge/upload
Content-Type: multipart/form-data

file: <file>
document_type: 'nutrition'
```

### 案例库管理

#### 列出所有案例

```
GET /api/v1/cases
```

#### 获取特定案例

```
GET /api/v1/cases/{case_id}
```

#### 创建新案例

```
POST /api/v1/cases
Content-Type: application/json

{
  "title": "剖腹产二胎产妇的恢复案例",
  "type": "产后修复",
  "date": "2023-08-15",
  "description": "32岁张女士，剖腹产二胎，入住本中心28天...",
  "before_after_images": ["url1", "url2"],
  "testimonial": "在这里的28天，我的恢复速度超出预期..."
}
```

#### 搜索相似案例

```
POST /api/v1/cases/search
Content-Type: application/json

{
  "age": 32,
  "pregnancy_status": "产后",
  "birth_type": "剖腹产",
  "interests": ["母乳喂养", "产后修复"]
}
```

### AI服务

#### 分析客户文本

```
POST /api/v1/ai/analyze
Content-Type: application/json

{
  "content": "我对母乳喂养很关注，因为我之前生大宝的时候奶水不太够"
}
```

#### 生成AI回应

```
POST /api/v1/ai/generate-response
Content-Type: application/json

{
  "query": "母乳喂养有什么技巧吗？",
  "customer_profile": {
    "name": "张娜",
    "age": 32,
    "pregnancy_status": "产后",
    "birth_type": "剖腹产"
  },
  "context": [
    {
      "role": "customer",
      "content": "我对母乳喂养很关注"
    },
    {
      "role": "sales",
      "content": "我们中心有专业的母乳喂养指导"
    }
  ]
}
```

### 客户管理

#### 创建客户资料

```
POST /api/v1/customers
Content-Type: application/json

{
  "name": "张娜",
  "age": 32,
  "pregnancy_status": "产后",
  "birth_type": "剖腹产",
  "birth_count": 2,
  "source_channel": "朋友介绍"
}
```

#### 获取客户资料

```
GET /api/v1/customers/{customer_id}
```

## 错误处理

所有API错误响应采用统一格式:

```json
{
  "detail": "错误详情描述"
}
```

常见HTTP状态码:

- 200: 请求成功
- 400: 错误的请求
- 401: 未授权
- 404: 资源未找到
- 500: 服务器内部错误

## Cursor客户端接入

### 接入步骤

1. 在Cursor中初始化WebSocket连接:

```javascript
const ws = new WebSocket('ws://your-server-address:8000/ws/cursor-client-123');

ws.onopen = function() {
  console.log('Connected to MCP Server');
  
  // 发送阶段切换消息
  ws.send(JSON.stringify({
    type: "stage_change",
    stage: "initial"
  }));
};

ws.onmessage = function(e) {
  const response = JSON.parse(e.data);
  
  // 处理服务器响应
  switch(response.type) {
    case "info_collection":
      // 处理信息收集响应
      displayExtractedInfo(response.extracted);
      break;
    case "feedback_analysis":
      // 处理反馈分析响应
      displayAnalysis(response.analysis);
      break;
    case "ai_response":
    case "ai_command_response":
      // 处理AI回应
      displayAIResponse(response.response);
      break;
    case "similar_cases":
      // 处理相似案例
      displayCases(response.cases);
      break;
  }
};
```

2. 发送语音输入:

```javascript
// 语音识别获取文本后
function onSpeechRecognized(text, speaker) {
  ws.send(JSON.stringify({
    type: "speech",
    text: text,
    speaker: speaker // "customer" 或 "sales"
  }));
}
```

3. 发送销售指令:

```javascript
function sendSalesCommand(command) {
  ws.send(JSON.stringify({
    type: "command",
    command: command
  }));
}

// 例如:
// sendSalesCommand("小美，根据宝妈的情况，推荐一下适合她的产后修复方案");
```

4. 切换交互阶段:

```javascript
function changeStage(stage) {
  ws.send(JSON.stringify({
    type: "stage_change",
    stage: stage // "initial", "tour", "consultation", "case_presentation"
  }));
}
``` 