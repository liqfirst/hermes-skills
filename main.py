#!/usr/bin/env python3
import sys, json, os, urllib.request, datetime

def main():
    # 解析 Hermes 传入的参数
    try:
        raw = sys.stdin.read()
        data = json.loads(raw) if raw.strip() else {}
    except:
        data = {}
    
    user_content = data.get("content", data.get("user_input", "请写一首诗"))
    
    # 配置（支持环境变量覆盖，方便部署）
    N8N_URL = os.getenv('N8N_WEBHOOK_URL', 'http://host.docker.internal:5678/webhook/generate-content')
    TIMEOUT = int(os.getenv('N8N_TIMEOUT', '30'))
    
    # 构建请求载荷
    payload = {
        "action": "generate",
        "content": user_content,
        "model": "qwen2.5:7b-64k",
        "source": "hermes-skill",
        "timestamp": datetime.datetime.now().isoformat()
    }
    
    try:
        # 发送 POST 请求到 n8n
        req_data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(
            N8N_URL,
            data=req_data,
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            result = json.loads(resp.read().decode('utf-8'))
            
            # 格式化输出（Hermes 会捕获 print 内容展示给用户）
            if 'content' in result:
                print(f"🎨 生成结果：\n{'─'*40}\n{result['content']}\n{'─'*40}")
            elif 'executionId' in result:
                print(f"⏳ 任务已提交，执行 ID: {result['executionId']}")
                print(f"💡 提示: 可使用 /skills run n8n-content-gen --query {result['executionId']} 查询结果")
            else:
                print(f"✅ n8n 响应: {json.dumps(result, ensure_ascii=False)}")
                
            return {"status": "success", "result": result}
            
    except urllib.error.HTTPError as e:
        print(f"❌ HTTP {e.code}: {e.read().decode('utf-8')[:200]}")
        return {"status": "error", "message": f"HTTP {e.code}"}
    except Exception as e:
        print(f"❌ 调用失败: {type(e).__name__}: {e}")
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    result = main()
    if result:
        # 结构化结果写入 stderr（供 Hermes 内部解析）
        sys.stderr.write(json.dumps(result, ensure_ascii=False) + "\n")