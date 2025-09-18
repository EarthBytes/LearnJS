js_facts = {
    # Basics
    "javascript": "JavaScript (JS) is a programming language mainly used to make web pages interactive. It runs in the browser, but can also run on servers via Node.js.",
    "what is javascript": "JavaScript (JS) is a programming language mainly used to make web pages interactive. It runs in the browser, but can also run on servers via Node.js.",
    "basics": "JavaScript (JS) is a programming language mainly used to make web pages interactive. It runs in the browser, but can also run on servers via Node.js.",
    "syntax": "JS can be included inline with HTML (onclick), internally with <script> tags, or externally with a .js file linked in the HTML.",
    "how to write": "JavaScript code can be written in .js files or inside <script> tags in HTML. Basic syntax: statements end with semicolons, use camelCase for variables.",
    "getting started": "To start with JavaScript, you need a text editor and a web browser. Write your code in .js files or HTML script tags.",

    # Variables
    "variable": "In JavaScript, you can declare variables with var, let, or const. let is re-assignable, const cannot be re-assigned, and var is older function-scoped code.",
    "variables": "In JavaScript, you can declare variables with var, let, or const. let is re-assignable, const cannot be re-assigned, and var is older function-scoped code.",
    "var": "var is the old way to declare variables in JavaScript. It's function-scoped and can be re-declared. Example: var name = 'John';",
    "let": "let declares block-scoped variables that can be reassigned. Example: let age = 25; age = 26; // This works",
    "const": "const declares block-scoped variables that cannot be reassigned. Example: const PI = 3.14159; // Cannot change PI later",
    "declare variables": "Use let for variables that change, const for constants, and avoid var in modern code. Example: let count = 0; const MAX = 100;",

    # Data Types
    "data type": "JavaScript has different data types: String ('Hello'), Number (42, 3.14), Boolean (true/false), Null, Undefined, Object ({key: value}), Array ([1,2,3]).",
    "data types": "JavaScript has different data types: String ('Hello'), Number (42, 3.14), Boolean (true/false), Null, Undefined, Object ({key: value}), Array ([1,2,3]).",
    "types": "JavaScript has different data types: String ('Hello'), Number (42, 3.14), Boolean (true/false), Null, Undefined, Object ({key: value}), Array ([1,2,3]).",
    "string": "Strings are text data enclosed in quotes. Example: 'Hello', \"World\", `Template string with ${variable}`. Use + or template literals for concatenation.",
    "strings": "Strings are text data enclosed in quotes. Example: 'Hello', \"World\", `Template string with ${variable}`. Use + or template literals for concatenation.",
    "number": "Numbers in JavaScript include integers and decimals. Example: 42, 3.14, -17. JavaScript has one Number type for all numeric values.",
    "numbers": "Numbers in JavaScript include integers and decimals. Example: 42, 3.14, -17. JavaScript has one Number type for all numeric values.",
    "boolean": "Booleans represent true or false values. Example: let isActive = true; let isComplete = false;",
    "booleans": "Booleans represent true or false values. Example: let isActive = true; let isComplete = false;",
    "null": "null represents an intentional absence of value. Example: let data = null; // Explicitly no value",
    "undefined": "undefined means a variable has been declared but not assigned a value. Example: let x; // x is undefined",

    # Operators
    "operator": "Common operators include arithmetic (+, -, *, /, %), comparison (==, ===, !=, !==, <, >), logical (&&, ||, !), and assignment (=, +=, -=).",
    "operators": "Common operators include arithmetic (+, -, *, /, %), comparison (==, ===, !=, !==, <, >), logical (&&, ||, !), and assignment (=, +=, -=).",
    "arithmetic operators": "Arithmetic operators: + (add), - (subtract), * (multiply), / (divide), % (remainder). Example: 10 + 5 = 15, 10 % 3 = 1",
    "comparison operators": "Comparison operators: == (equal), === (strict equal), != (not equal), !== (strict not equal), < > <= >=. Always prefer === over ==.",
    "logical operators": "Logical operators: && (AND), || (OR), ! (NOT). Example: (age >= 18 && hasLicense) || isEmergency",
    "assignment operators": "Assignment operators: = (assign), += (add and assign), -= (subtract and assign), *= (multiply and assign), /= (divide and assign).",

    # Functions
    "function": "Functions are reusable blocks of code. Example: function greet(name) { return 'Hello ' + name; } or arrow functions: const add = (a, b) => a + b;",
    "functions": "Functions are reusable blocks of code. Example: function greet(name) { return 'Hello ' + name; } or arrow functions: const add = (a, b) => a + b;",
    "arrow function": "Arrow functions are shorter function syntax. Example: const multiply = (a, b) => a * b; or const square = x => x * x;",
    "arrow functions": "Arrow functions are shorter function syntax. Example: const multiply = (a, b) => a * b; or const square = x => x * x;",
    "function declaration": "Function declarations: function name(params) { return value; }. These are hoisted and can be called before definition.",
    "function expression": "Function expressions: const name = function(params) { return value; }. These are not hoisted and must be defined before use.",
    "parameters": "Parameters are inputs to functions. Example: function greet(name, age) { return `Hello ${name}, you are ${age}`; }",
    "return": "return statement sends a value back from a function. Example: function add(a, b) { return a + b; } Without return, function returns undefined.",

    # Conditionals
    "if statement": "JavaScript uses if, else if, and else statements. Example: if (age >= 18) { console.log('Adult'); } else { console.log('Minor'); }",
    "conditionals": "JavaScript uses if, else if, and else statements. Example: if (age >= 18) { console.log('Adult'); } else { console.log('Minor'); }",
    "if": "if statements execute code when a condition is true. Example: if (temperature > 30) { console.log('Hot day!'); }",
    "else": "else provides alternative code when if condition is false. Example: if (sunny) { goOutside(); } else { stayInside(); }",
    "else if": "else if checks additional conditions. Example: if (score >= 90) { grade = 'A'; } else if (score >= 80) { grade = 'B'; }",
    "switch": "switch statement compares a value against multiple cases. Example: switch(day) { case 'Monday': console.log('Start of work week'); break; }",
    "ternary operator": "Ternary operator is shorthand for if-else. Example: const message = (age >= 18) ? 'Adult' : 'Minor';",

    # Loops
    "loop": "JavaScript supports for, while, and for...of loops. Example: for (let i = 0; i < 5; i++) { console.log(i); }",
    "loops": "JavaScript supports for, while, and for...of loops. Example: for (let i = 0; i < 5; i++) { console.log(i); }",
    "for loop": "for loops repeat code a specific number of times. Example: for (let i = 0; i < 10; i++) { console.log(i); }",
    "while loop": "while loops repeat while a condition is true. Example: while (count < 5) { console.log(count); count++; }",
    "for of loop": "for...of loops iterate over arrays/strings. Example: for (let item of array) { console.log(item); }",
    "for in loop": "for...in loops iterate over object properties. Example: for (let key in object) { console.log(key, object[key]); }",
    "break": "break exits a loop early. Example: for (let i = 0; i < 10; i++) { if (i === 5) break; console.log(i); }",
    "continue": "continue skips the current iteration. Example: for (let i = 0; i < 5; i++) { if (i === 2) continue; console.log(i); }",

    # Objects
    "object": "Objects are collections of key-value pairs. Example: let person = {name: 'Cate', age: 21, isStudent: true};",
    "objects": "Objects are collections of key-value pairs. Example: let person = {name: 'Cate', age: 21, isStudent: true};",
    "object literal": "Object literals use curly braces {}. Example: const car = { brand: 'Toyota', model: 'Camry', year: 2023 };",
    "object property": "Access object properties with dot notation or brackets. Example: person.name or person['name']",
    "object methods": "Objects can contain functions as methods. Example: const calculator = { add: function(a, b) { return a + b; } };",
    "this keyword": "this refers to the current object in a method. Example: const person = { name: 'John', greet() { return `Hello, I'm ${this.name}`; } };",

    # Arrays
    "array": "Arrays store multiple values. Example: let numbers = [10, 20, 30]; console.log(numbers[1]);",
    "arrays": "Arrays store multiple values. Example: let numbers = [10, 20, 30]; console.log(numbers[1]);",
    "array methods": "Common array methods: push(), pop(), shift(), unshift(), slice(), splice(), forEach(), map(), filter(), reduce()",
    "push": "push() adds elements to the end of an array. Example: numbers.push(40); // adds 40 to end",
    "pop": "pop() removes and returns the last element. Example: let last = numbers.pop(); // removes and returns last item",
    "length": "Array length property gives the number of elements. Example: console.log(numbers.length);",
    "indexOf": "indexOf() finds the index of an element. Example: let index = numbers.indexOf(20); // returns 1 if 20 is at index 1",

    # DOM
    "dom": "The DOM lets you interact with HTML. Example: document.getElementById('demo').innerText = 'Hello!'; or document.querySelector('p').style.color = 'blue';",
    "document object model": "The DOM lets you interact with HTML. Example: document.getElementById('demo').innerText = 'Hello!'; or document.querySelector('p').style.color = 'blue';",
    "getelementbyid": "getElementById() selects an element by its ID. Example: const element = document.getElementById('myButton');",
    "queryselector": "querySelector() selects the first element matching a CSS selector. Example: document.querySelector('.my-class');",
    "innerhtml": "innerHTML gets or sets HTML content inside an element. Example: element.innerHTML = '<strong>Bold text</strong>';",
    "innertext": "innerText gets or sets text content, ignoring HTML tags. Example: element.innerText = 'Plain text';",
    "style": "Change element styles with the style property. Example: element.style.color = 'red'; element.style.fontSize = '20px';",

    # Events
    "event": "Events respond to user actions. Example: document.getElementById('btn').addEventListener('click', () => alert('Button clicked!'));",
    "events": "Events respond to user actions. Example: document.getElementById('btn').addEventListener('click', () => alert('Button clicked!'));",
    "addeventlistener": "addEventListener() attaches event handlers. Example: button.addEventListener('click', function() { console.log('Clicked!'); });",
    "click event": "click events fire when an element is clicked. Example: button.addEventListener('click', handleClick);",
    "submit event": "submit events fire when a form is submitted. Example: form.addEventListener('submit', function(e) { e.preventDefault(); });",
    "event object": "Event handlers receive an event object with details. Example: function handleClick(event) { console.log(event.target); }",

    # Console
    "console": "The console is used for debugging. console.log('Message'), console.error('Error'), console.warn('Warning').",
    "debugging": "The console is used for debugging. console.log('Message'), console.error('Error'), console.warn('Warning').",
    "console.log": "console.log() prints messages to the browser console. Example: console.log('Hello World!', variable);",
    "console.error": "console.error() prints error messages in red. Example: console.error('Something went wrong!');",
    "console.warn": "console.warn() prints warning messages in yellow. Example: console.warn('This is deprecated');",

    # Advanced Extras
    "scope": "Scope determines where variables are accessible. let/const are block-scoped, var is function-scoped.",
    "hoisting": "Function and var declarations are 'hoisted' to the top of their scope during execution.",
    "closure": "A closure is when a function remembers variables from the scope it was created in, even after that scope has finished.",
    "closures": "A closure is when a function remembers variables from the scope it was created in, even after that scope has finished.",
    "async": "JavaScript handles async code with promises and async/await. Example: const data = await fetch(url);",
    "promise": "Promises handle asynchronous operations. Example: fetch(url).then(response => response.json()).then(data => console.log(data));",
    "async await": "async/await makes promises easier to read. Example: async function getData() { const response = await fetch(url); return await response.json(); }",
    "callback": "Callbacks are functions passed as arguments to other functions. Example: setTimeout(() => console.log('Done!'), 1000);",

    # Error Handling
    "try catch": "try...catch handles errors gracefully. Example: try { riskyCode(); } catch (error) { console.error('Error:', error.message); }",
    "error handling": "Handle errors with try...catch blocks to prevent crashes. Always catch potential errors in async operations.",
    "throw": "throw creates custom errors. Example: if (age < 0) throw new Error('Age cannot be negative');",

    # ES6+ Features
    "template literal": "Template literals use backticks for string interpolation. Example: `Hello ${name}, you are ${age} years old`;",
    "destructuring": "Destructuring extracts values from arrays/objects. Example: const {name, age} = person; const [first, second] = array;",
    "spread operator": "Spread operator (...) expands arrays/objects. Example: const newArray = [...oldArray, newItem]; const newObj = {...oldObj, newProp: value};",
    "rest parameter": "Rest parameters collect multiple arguments into an array. Example: function sum(...numbers) { return numbers.reduce((a, b) => a + b); }",

    # JSON
    "json": "JSON is a data format for storing and exchanging data. Example: {\"name\": \"John\", \"age\": 30}",
    "json.parse": "JSON.parse() converts JSON string to JavaScript object. Example: const obj = JSON.parse('{\"name\": \"John\"}');",
    "json.stringify": "JSON.stringify() converts JavaScript object to JSON string. Example: const json = JSON.stringify({name: 'John'});",
}

# Common code issues and their explanations
code_issues = {
    "missing quotes": {
        "patterns": [r"console\.log\([^'\"]*[a-zA-Z][^'\"]*\)", r"alert\([^'\"]*[a-zA-Z][^'\"]*\)"],
        "explanation": "Strings must be enclosed in quotes. Use 'Hello' or \"Hello\" instead of Hello.",
        "fix": "Wrap text in single or double quotes: console.log('Hello') or console.log(\"Hello\")"
    },
    "missing semicolon": {
        "patterns": [r"console\.log\([^)]+\)(?!\s*;)", r"let\s+\w+\s*=\s*[^;]+(?!\s*;)"],
        "explanation": "While not always required, semicolons are good practice to end statements.",
        "fix": "Add a semicolon at the end of the statement: console.log('Hello');"
    },
    "wrong variable declaration": {
        "patterns": [r"var\s+", r"\w+\s*=\s*[^;]+(?!let|const|var)"],
        "explanation": "Use 'let' for variables that change or 'const' for constants instead of 'var'.",
        "fix": "Use let or const: let name = 'John'; or const PI = 3.14;"
    },
    "assignment vs equality": {
        "patterns": [r"if\s*\([^)]*=(?!=)[^)]*\)", r"while\s*\([^)]*=(?!=)[^)]*\)"],
        "explanation": "Use == for comparison, not = (which is assignment). Better yet, use === for strict equality.",
        "fix": "Use === for comparison: if (age === 18) instead of if (age = 18)"
    },
    "missing parentheses": {
        "patterns": [r"console\.log[^(]", r"alert[^(]"],
        "explanation": "Function calls require parentheses, even with no arguments.",
        "fix": "Add parentheses: console.log('Hello') not console.log 'Hello'"
    },
    "wrong array access": {
        "patterns": [r"\w+\.\d+", r"\w+\s*\(\s*\d+\s*\)"],
        "explanation": "Access array elements with square brackets, not dots or parentheses.",
        "fix": "Use square brackets: array[0] not array.0 or array(0)"
    }
}
