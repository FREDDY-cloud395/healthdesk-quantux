const { spawn } = require('child_process');
const http = require('http');

// Start chrome with remote debugging
const chrome = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
  '--headless',
  '--no-sandbox',
  '--disable-gpu',
  '--remote-debugging-port=9222',
  'http://localhost:8005'
]);

setTimeout(async () => {
  try {
    http.get('http://127.0.0.1:9222/json', (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        console.log("CHROME TABS:", data);
        const tabs = JSON.parse(data);
        if (tabs.length > 0 && tabs[0].webSocketDebuggerUrl) {
          const WebSocket = require('ws'); // check if available or use raw
        }
        chrome.kill();
      });
    }).on('error', err => {
      console.error("HTTP ERROR:", err.message);
      chrome.kill();
    });
  } catch (e) {
    console.error(e);
    chrome.kill();
  }
}, 3000);
