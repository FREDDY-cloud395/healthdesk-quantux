import subprocess, time, json, urllib.request

try:
    import websocket
except ImportError:
    subprocess.run(["pip", "install", "websocket-client"], check=True)
    import websocket

chrome = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
cmd = [
    chrome,
    '--headless=new',
    '--remote-debugging-port=9222',
    '--remote-allow-origins=*',
    '--window-size=390,844',
    'http://127.0.0.1:8000/cockpit'
]
proc = subprocess.Popen(cmd)
time.sleep(2)

try:
    tabs = json.loads(urllib.request.urlopen('http://localhost:9222/json').read())
    target_tab = None
    for t in tabs:
        if '127.0.0.1:8000' in t.get('url', ''):
            target_tab = t
            break
    if not target_tab:
        target_tab = tabs[0]
    ws_url = target_tab['webSocketDebuggerUrl']
    ws = websocket.create_connection(ws_url)

    # Evaluate JS script to find elements wider than window.innerWidth
    js_code = """
    (() => {
        const vw = window.innerWidth;
        const results = [];
        const all = document.querySelectorAll('*');
        for (const el of all) {
            const rect = el.getBoundingClientRect();
            if (rect.right > vw || el.scrollWidth > vw || el.offsetWidth > vw) {
                results.push({
                    tag: el.tagName,
                    id: el.id,
                    className: el.className,
                    offsetWidth: el.offsetWidth,
                    scrollWidth: el.scrollWidth,
                    rectRight: rect.right,
                    rectWidth: rect.width
                });
            }
        }
        return {
            windowInnerWidth: window.innerWidth,
            documentElementClientWidth: document.documentElement.clientWidth,
            bodyScrollWidth: document.body.scrollWidth,
            overflowElements: results.slice(0, 25)
        };
    })()
    """

    req = {
        "id": 1,
        "method": "Runtime.evaluate",
        "params": {
            "expression": js_code,
            "returnByValue": True
        }
    }
    ws.send(json.dumps(req))
    res = json.loads(ws.recv())
    print("DOM OVERFLOW DIAGNOSTIC RESULT:")
    print(json.dumps(res.get('result', {}).get('value', {}), indent=2))

    ws.close()
finally:
    proc.terminate()
