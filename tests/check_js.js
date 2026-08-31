const fs = require('fs');
const appCode = fs.readFileSync('frontend/js/app.js', 'utf8');
const apiCode = fs.readFileSync('frontend/js/api.js', 'utf8');

const definedFunctions = new Set([
  'alert', 'confirm', 'prompt', 'switchMobileCockpitTab', 'switchView', 
  'toggleUserStatus', 'deleteUser', 'deleteArticle', 'toggleInstPlatform', 'saveAllPlatformConfigs'
]);

// Extract functions
for (const m of appCode.matchAll(/function\s+([a-zA-Z0-9_$]+)\s*\(/g)) {
  definedFunctions.add(m[1]);
}
for (const m of appCode.matchAll(/(?:const|let|var)\s+([a-zA-Z0-9_$]+)\s*=/g)) {
  definedFunctions.add(m[1]);
}

// Find all function calls in appCode
const calls = [...appCode.matchAll(/([a-zA-Z0-9_$]+)\s*\(/g)].map(m => m[1]);
const knownGlobals = new Set([
  'require', 'parseInt', 'parseFloat', 'isNaN', 'isFinite', 'encodeURIComponent', 'decodeURIComponent',
  'fetch', 'setTimeout', 'clearTimeout', 'setInterval', 'clearInterval', 'addEventListener',
  'removeEventListener', 'querySelector', 'querySelectorAll', 'getElementById', 'getElementsByClassName',
  'createElement', 'appendChild', 'removeChild', 'remove', 'classList', 'add', 'toggle', 'contains',
  'setAttribute', 'getAttribute', 'removeAttribute', 'forEach', 'map', 'filter', 'find', 'reduce',
  'some', 'every', 'includes', 'indexOf', 'push', 'pop', 'shift', 'unshift', 'splice', 'slice', 'join',
  'concat', 'split', 'replace', 'replaceAll', 'match', 'matchAll', 'trim', 'toLowerCase', 'toUpperCase',
  'substring', 'substr', 'startsWith', 'endsWith', 'keys', 'values', 'entries', 'assign', 'stringify',
  'parse', 'log', 'error', 'warn', 'info', 'table', 'scrollIntoView', 'focus', 'blur', 'click',
  'submit', 'reset', 'preventDefault', 'stopPropagation', 'getTime', 'toISOString', 'toLocaleTimeString',
  'toLocaleDateString', 'min', 'max', 'round', 'floor', 'ceil', 'abs', 'random', 'writeText', 'print',
  'Date', 'URL', 'Array', 'Object', 'String', 'Number', 'Boolean', 'RegExp', 'JSON', 'Math', 'Set', 'Map',
  'if', 'for', 'while', 'switch', 'catch', 'function', 'return', 'async', 'new', 'typeof', 'delete'
]);

const missing = new Set();
for (const c of calls) {
  if (!definedFunctions.has(c) && !knownGlobals.has(c)) {
    missing.add(c);
  }
}
console.log('MISSING FUNCTIONS IN APP.JS:', Array.from(missing));

// Also check onclick occurrences
const onclickRegex = /onclick="([^"(]+)\(/g;
let match;
while ((match = onclickRegex.exec(appCode)) !== null) {
  const funcName = match[1].trim();
  if (!definedFunctions.has(funcName) && !knownGlobals.has(funcName)) {
    console.log('MISSING ONCLICK:', funcName);
  }
}
