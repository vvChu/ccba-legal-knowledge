import urllib.request
import json

try:
    with urllib.request.urlopen("http://localhost:9222/json", timeout=3) as resp:
        data = json.loads(resp.read().decode())
        print(f"Open tabs ({len(data)}):")
        for t in data:
            title = t.get("title", "")
            url = t.get("url", "")
            print(f" - {title} | {url}")
except Exception as e:
    print("Error connecting to Chrome port 9222:", e)
