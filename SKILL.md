---
name: n8n-content-gen
version: 1.0.0
description: 调用 n8n 生成内容
entrypoint: main.py
triggers:
  - 生成
  - n8n-content-gen
tools:
  - execute_code
---

## ⚠️ 强制指令（必须严格遵守）
1. **仅调用 `execute_code` 工具**。禁止 `read_file`、`search` 或查找任何模板。
2. 将用户请求内容作为 JSON 传入：`{"content": "用户原话", "action": "generate"}`
3. **直接打印工具输出**。不要添加任何解释、问候或二次加工。