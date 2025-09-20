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
    "es6": "ES6 introduced many new features like arrow functions, template literals, destructuring... etc.",
    "template literal": "Template literals use backticks for string interpolation. Example: `Hello ${name}, you are ${age} years old`;",
    "destructuring": "Destructuring extracts values from arrays/objects. Example: const {name, age} = person; const [first, second] = array;",
    "spread operator": "Spread operator (...) expands arrays/objects. Example: const newArray = [...oldArray, newItem]; const newObj = {...oldObj, newProp: value};",
    "rest parameter": "Rest parameters collect multiple arguments into an array. Example: function sum(...numbers) { return numbers.reduce((a, b) => a + b); }",

    # JSON
    "json": "JSON is a data format for storing and exchanging data. Example: {\"name\": \"John\", \"age\": 30}",
    "json.parse": "JSON.parse() converts JSON string to JavaScript object. Example: const obj = JSON.parse('{\"name\": \"John\"}');",
    "json.stringify": "JSON.stringify() converts JavaScript object to JSON string. Example: const json = JSON.stringify({name: 'John'});",

    # Misc
    "misc": "JavaScript is a versatile language used for web development, server-side programming, game development, and more. Keep practicing to improve!",
    "troubleshooting": "Common JS issues include syntax errors, undefined variables, and type errors. Use console.log and debugging tools to find problems.",
    "best practices": "Use let/const instead of var, prefer === over ==, write modular code with functions, and comment your code for clarity.",
    "resources": "Great JS learning resources include MDN Web Docs, freeCodeCamp, JavaScript.info, and various online courses on platforms like Codecademy and Udemy.",
}

# Conversational responses with priority levels

conversation_prompts = {
    # Help requests (high priority when standalone, but lower when mixed with learning)
    "help": {"response": "You can just ask me about JS stuff. Like:\n - 'What is a function?'\n - 'Show me arrays'\n - 'How do I use loops?'\n - 'Explain variables'\n\nGo ahead, ask me anything about JS!", "priority": 3 },
    "how do i use this": { "response": "Just ask about JavaScript! I can explain concepts or show examples. Try something like 'What are variables?' or 'How do functions work?'", "priority": 3 },
    "how do i use you": { "response": "Ask me about JavaScript stuff and I'll try to explain it. Variables, functions, arrays, loops—you name it.", "priority": 3 },
    "how do i use learnjs": { "response": "Just type any JS question and I'll help out. Something like 'What is an array?' works fine.", "priority": 3 },
    "how does this work": { "response": "Ask me any JS question and I'll try to explain. Could be basics like variables or advanced stuff.", "priority": 3 },
    "what can you do": { "response": "I can answer JS questions, explain concepts, and show examples. What do you want to try first?", "priority": 3 },
    "what can you help with": { "response": "I can help with anything in JS. Ask me about variables, functions, loops, arrays, or objects.", "priority": 3 },

    # Identity questions (medium priority)
    "what are you": { "response": "I'm LearnJS - I help you learn Javascript. I can show you code examples and explain concepts.", "priority": 2 },
    "who are you": { "response": "Just LearnJS, here to help you learn JavaScript!", "priority": 2 },
    "what is this": { "response": "This is LearnJS, a chatbot to help you learn JavaScript.", "priority": 2 },
    "what is learnjs": { "response": "LearnJS is a small chatbot to explain JS topics and show examples.", "priority": 2 },
    "tell me about yourself": { "response": "I'm a JS helper here to answer questions and show examples. Nothing fancy!", "priority": 2 },
    "are you a bot": { "response": "Yep, just a simple JS helper bot.", "priority": 2 },
    "are you a robot": { "response": "Yep, just a simple JS helper bot.", "priority": 2 },
    "are you ai": { "response": "Yep, just a simple JS helper bot.", "priority": 2 },
    "are you artificial intelligence": { "response": "Yep, just a simple JS helper bot.", "priority": 2 },
    "do you have feelings": { "response": "Not really, just here to help with JS!", "priority": 2 },
    "do you have emotions": { "response": "Not really, just here to help with JS!", "priority": 2 },
    "what's your name": { "response": "I'm LearnJS, your JavaScript helper bot.", "priority": 2 },
    "what is your name": { "response": "I'm LearnJS, your JavaScript helper bot.", "priority": 2 },
    "who built you": { "response": "I was built by a developer called Cate who wanted to make learning JS easier.", "priority": 2 },
    "who created you": { "response": "I was built by a developer called Cate who wanted to make learning JS easier.", "priority": 2 },
    "who made you": { "response": "I was built by a developer called Cate who wanted to make learning JS easier.", "priority": 2 },
    "what are you made of": { "response": "My brain was created using Python, however my appearance was built with HTML, CSS and JS!", "priority": 2 },
    "what are you built with": { "response": "My brain was created using Python, however my appearance was built with HTML, CSS and JS!", "priority": 2 },
    "what are you made from": { "response": "My brain was created using Python, however my appearance was built with HTML, CSS and JS!", "priority": 2 },
    "what technologies are you built with": { "response": "My brain was created using Python, however my appearance was built with HTML, CSS and JS!", "priority": 2 },

    # Greetings (low priority)
    "hello": {"response": "Hey!", "priority": 1},
    "hi": {"response": "Hi!", "priority": 1}, 
    "hey": {"response": "Hey there!", "priority": 1},
    "good morning": {"response": "Morning!", "priority": 1},
    "good afternoon": {"response": "Afternoon!", "priority": 1},
    "good evening": {"response": "Evening!", "priority": 1},
    "morning": {"response": "Morning!", "priority": 1},
    "afternoon": {"response": "Afternoon!", "priority": 1},
    "evening": {"response": "Evening!", "priority": 1},
    "what's new": {"response": "Not much, just messing around with JS. You?", "priority": 1},
    "whats new": {"response": "Not much, just messing around with JS. You?", "priority": 1},
    "cool": {"response": "Yeah, JS can be fun! Want to try something?", "priority": 1},
    "sup": {"response": "Not much, just here to help with JS. You?", "priority": 1},
    "yo": {"response": "Yo! Ready to learn some JS?", "priority": 1},
    "greetings": {"response": "Greetings! How can I assist you with JavaScript today?", "priority": 1},

    # How are you variations (low priority)
    "how are you": {"response": "I'm good! How about you?", "priority": 1},
    "how are you doing": {"response": "Doing fine, thanks! What are you working on?", "priority": 1},
    "how's it going": {"response": "Pretty good! Ready to mess with some JS?", "priority": 1},
    "hows it going": {"response": "Pretty good! Ready to mess with some JS?", "priority": 1},
    "what's up": {"response": "Not much, just here to help with JS. You?", "priority": 1},
    "whats up": {"response": "Not much, just here to help with JS. You?", "priority": 1},

    # Gratitude (low priority)
    "thank you": {"response": "No problem!", "priority": 1},
    "thanks": {"response": "You're welcome!", "priority": 1},
    "thx": {"response": "Anytime!", "priority": 1},
    "appreciate it": {"response": "Glad to help!", "priority": 1},
    "cheers": {"response": "Cheers!", "priority": 1},
    "many thanks": {"response": "You're welcome!", "priority": 1},
    "thanks a lot": {"response": "No problem!", "priority": 1},
    "thank you very much": {"response": "Anytime!", "priority": 1},
    "thank you so much": {"response": "Glad to help!", "priority": 1},
    "i appreciate it": {"response": "You're welcome!", "priority": 1},
    "much appreciated": {"response": "No problem!", "priority": 1},
    "thanks a bunch": {"response": "Anytime!", "priority": 1},
    "thanks so much": {"response": "Glad to help!", "priority": 1},
    
    # Farewell (medium priority)
    "bye": {"response": "Bye! Catch you later.", "priority": 2},
    "goodbye": {"response": "See you!", "priority": 2},
    "see you": {"response": "See you soon!", "priority": 2},
    "see you later": {"response": "See you later!", "priority": 2},
    "catch you later": {"response": "Catch you later!", "priority": 2},
    
    # Encouragement/Motivation (medium priority)
    "this is hard": {"response": "Yeah, JS can be tricky. Take it slow. Which part's giving you trouble?", "priority": 2},
    "i'm confused": {"response": "No worries, it happens. What exactly is confusing?", "priority": 2},
    "im confused": {"response": "No worries, it happens. What exactly is confusing?", "priority": 2},
    "i don't understand": {"response": "That's okay, learning JS takes time. What part should I explain differently?", "priority": 2},
    "i dont understand": {"response": "That's okay, learning JS takes time. What part should I explain differently?", "priority": 2},
    "this is frustrating": {"response": "I get it, programming can be frustrating. Want to try a different topic or take a break?", "priority": 2},
}

# Follow-up responses to "how are you" replies
user_status_responses = {
    "im good": {"response": "Glad to hear that!", "priority": 1},
    "i'm good": {"response": "Glad to hear that!", "priority": 1},
    "good": {"response": "Nice!", "priority": 1},
    "fine": {"response": "Cool!", "priority": 1},
    "not bad": {"response": "That's good to hear.", "priority": 1},
    "okay": {"response": "Alright!", "priority": 1},
    "doing well": {"response": "Great!", "priority": 1},
    "doing fine": {"response": "Good to know!", "priority": 1},
    "all good": {"response": "Awesome!", "priority": 1},
    "so-so": {"response": "Hope your day gets better!", "priority": 1},
    "not great": {"response": "Oh, hope things improve soon.", "priority": 1},
}

# Topic synonyms for keyword matching

topic_synonyms = {
    "function": ["function", "functions", "method", "methods", "func", "functon", "fucntion", "funtion", "functin"],
    "variable": ["variable", "variables", "var", "let", "const", "declaration", "variabel", "varaible", "varibles"],
    "array": ["array", "arrays", "list", "lists", "aray", "arays", "ary", "array methods"],
    "object": ["object", "objects", "obj", "dictionary", "objct"],
    "loop": ["loop", "loops", "iteration", "iterate", "for", "while", "for loop", "while loop", "looping"],
    "conditional": ["if", "else", "switch", "condition", "conditional", "if statement", "conditionals"],
    "event": ["event", "events", "listener", "click", "submit", "eventlistener"],
    "string": ["string", "strings", "text", "str", "strng"],
    "number": ["number", "numbers", "numeric", "num", "integer", "float"],
    "boolean": ["boolean", "booleans", "true", "false", "bool"],
    "dom": ["dom", "document", "html", "element", "document object model"],
    "async": ["async", "await", "promise", "promises", "asynchronous", "asyncronous"],
    "json": ["json", "parse", "stringify", "json.parse", "json.stringify"],
    "console": ["console", "log", "debug", "debugging", "console.log"],
    "es6": ["es6", "ecmascript 6", "modern javascript", "es2015", "ecmascript6"],
    "error handling": ["error", "errors", "try", "catch", "throw", "exception", "error handling"],
    "scope": ["scope", "scoping", "global", "local", "block scope", "function scope"],
    "closure": ["closure", "closures", "lexical scope"],
    "callback": ["callback", "callbacks", "higher-order function"],
    "spread operator": ["spread", "spread operator", "..."],
    "rest parameter": ["rest", "rest parameter", "rest parameters"],
    "destructuring": ["destructure", "destructuring", "destructuring assignment"],
    "template literal": ["template", "template literal", "template literals", "template strings"],
    "hoisting": ["hoisting", "hoist"],
    "basics": ["basics", "basic", "introduction", "getting started", "syntax", "beginner"],
    "operators": ["operator", "operators", "arithmetic", "comparison", "logical", "assignment"],
    "troubleshooting": ["troubleshooting", "troubleshoot", "not working", "broken", "fix", "debug", "issue", "problem"],
    "data types": ["data type", "data types", "type", "types", "datatypes"],
}

# Question type patterns

question_patterns = {
    "definition": [
        r"what (is|are)",
        r"define",
        r"definition of",
        r"meaning of",
        r"explain",
        r"tell me about",
        r"describe",
        r"can you explain"
    ],
    "example": [
        r"example",
        r"show me",
        r"demonstrate",
        r"sample",
        r"can you show",
        r"give me an example",
        r"examples"
    ],
    "how_to": [
        r"how (do|to)",
        r"how can i",
        r"steps to",
        r"process of",
        r"how do you",
        r"guide",
        r"tutorial"
    ],
    "comparison": [
        r"difference between",
        r"compare",
        r"vs",
        r"versus",
        r"better",
        r"which is",
        r"what's the difference"
    ],
    "troubleshooting": [
        r"error",
        r"not working",
        r"problem",
        r"issue",
        r"fix",
        r"debug",
        r"broken",
        r"wrong",
        r"help.*fix",
        r"why.*not.*work"
    ]
}