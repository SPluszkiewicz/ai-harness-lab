import json
import sys
import urllib.request

model = sys.argv[1]
body = json.dumps(
    {
        "model": model,
        "messages": [{"role": "user", "content": "ping"}],
        "max_tokens": 8,
    }
).encode()
req = urllib.request.Request(
    "http://127.0.0.1:8080/v1/chat/completions",
    data=body,
    headers={"Content-Type": "application/json"},
    method="POST",
)
with urllib.request.urlopen(req, timeout=300) as resp:
    data = json.load(resp)
print(data.get("model"), data["choices"][0]["message"].get("content"))
print("usage", data.get("usage"))
