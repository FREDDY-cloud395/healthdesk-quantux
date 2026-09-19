const fs = require('fs');

const code = fs.readFileSync('frontend/js/app.js', 'utf8');
const lines = code.split('\n');

// Check line by line or find the unclosed braces
let openBraces = 0;
let openParens = 0;
let openBrackets = 0;

for (let i = 0; i < lines.length; i++) {
  const line = lines[i];
  // Ignore single-line comments
  const clean = line.replace(/\/\/.*$/, '');
  for (let c of clean) {
    if (c === '{') openBraces++;
    else if (c === '}') openBraces--;
    else if (c === '(') openParens++;
    else if (c === ')') openParens--;
    else if (c === '[') openBrackets++;
    else if (c === ']') openBrackets--;
  }
  if (openBraces < 0 || openParens < 0 || openBrackets < 0) {
    console.log(`Mismatch at line ${i + 1}: braces=${openBraces}, parens=${openParens}, brackets=${openBrackets}`);
  }
}

console.log(`Final: braces=${openBraces}, parens=${openParens}, brackets=${openBrackets}`);
