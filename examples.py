js_examples = {
    "function": [
        "Here are some function examples:\n\n**Function Declaration:**\n```javascript\nfunction greetUser(name) {\n    return `Hello, ${name}! Welcome to our site.`;\n}\n\nconst message = greetUser('Alice');\nconsole.log(message); // 'Hello, Alice! Welcome to our site.'\n```\n\n**Arrow Function:**\n```javascript\nconst calculateArea = (width, height) => width * height;\n\nconst area = calculateArea(5, 3);\nconsole.log(area); // 15\n```\n\n**Function with Default Parameters:**\n```javascript\nfunction createUser(name, role = 'user') {\n    return {\n        name: name,\n        role: role,\n        id: Math.random().toString(36)\n    };\n}\n\nconst admin = createUser('John', 'admin');\nconst regularUser = createUser('Jane'); // role defaults to 'user'\n```",
        
        "Here's another function example - a practical calculator:\n\n```javascript\nconst calculator = {\n    add: function(a, b) { return a + b; },\n    subtract: (a, b) => a - b,\n    multiply(a, b) { return a * b; }, // shorthand method\n    divide(a, b) {\n        if (b === 0) {\n            throw new Error('Cannot divide by zero!');\n        }\n        return a / b;\n    }\n};\n\nconsole.log(calculator.add(5, 3)); // 8\nconsole.log(calculator.multiply(4, 7)); // 28\n```"
    ],
    
    "array": [
        "Here are some array examples:\n\n**Creating and Accessing Arrays:**\n```javascript\nconst fruits = ['apple', 'banana', 'orange'];\nconst numbers = [1, 2, 3, 4, 5];\nconst mixed = ['hello', 42, true, null];\n\nconsole.log(fruits[0]); // 'apple'\nconsole.log(fruits.length); // 3\n```\n\n**Array Methods:**\n```javascript\n// Adding/removing elements\nfruits.push('grape'); // adds to end\nfruits.unshift('mango'); // adds to start\nconst lastFruit = fruits.pop(); // removes from end\nconst firstFruit = fruits.shift(); // removes from start\n\n// Finding elements\nconst index = fruits.indexOf('banana'); // returns 1\nconst exists = fruits.includes('apple'); // returns true\n```",
        
        "Here's a more advanced array example:\n\n```javascript\nconst students = [\n    {name: 'Alice', grade: 85},\n    {name: 'Bob', grade: 92},\n    {name: 'Charlie', grade: 78}\n];\n\n// Filter students with grade above 80\nconst topStudents = students.filter(student => student.grade > 80);\n\n// Get just the names\nconst names = students.map(student => student.name);\n\n// Find average grade\nconst average = students.reduce((sum, student) => sum + student.grade, 0) / students.length;\n\nconsole.log(topStudents); // [{name: 'Alice', grade: 85}, {name: 'Bob', grade: 92}]\nconsole.log(names); // ['Alice', 'Bob', 'Charlie']\nconsole.log(average); // 85\n```"
    ],
    
    "variable": [
        "Here are variable examples:\n\n**Different Declaration Types:**\n```javascript\n// const - cannot be reassigned\nconst PI = 3.14159;\nconst user = {name: 'John', age: 30};\n\n// let - can be reassigned, block-scoped\nlet counter = 0;\ncounter = counter + 1; // OK\n\nlet message = 'Hello';\nif (true) {\n    let message = 'Hi there'; // different variable\n    console.log(message); // 'Hi there'\n}\nconsole.log(message); // 'Hello'\n\n// var - old way, function-scoped (avoid in modern code)\nvar oldStyle = 'not recommended';\n```",
        
        "Here's a practical example with variables:\n\n```javascript\n// Configuration variables\nconst API_URL = 'https://api.example.com';\nconst MAX_RETRIES = 3;\n\n// State variables\nlet isLoading = false;\nlet retryCount = 0;\nlet userData = null;\n\n// Function using these variables\nasync function fetchUserData(userId) {\n    isLoading = true;\n    retryCount = 0;\n    \n    while (retryCount < MAX_RETRIES) {\n        try {\n            const response = await fetch(`${API_URL}/users/${userId}`);\n            userData = await response.json();\n            break;\n        } catch (error) {\n            retryCount++;\n            if (retryCount >= MAX_RETRIES) {\n                throw new Error('Failed to fetch user data');\n            }\n        }\n    }\n    \n    isLoading = false;\n    return userData;\n}\n```"
    ],
    
    "loop": [
        "Here are loop examples:\n\n**For Loop:**\n```javascript\n// Basic for loop\nfor (let i = 0; i < 5; i++) {\n    console.log(`Number: ${i}`);\n}\n\n// Loop through array with index\nconst colors = ['red', 'green', 'blue'];\nfor (let i = 0; i < colors.length; i++) {\n    console.log(`${i}: ${colors[i]}`);\n}\n```\n\n**For...of Loop:**\n```javascript\n// Loop through array values\nfor (const color of colors) {\n    console.log(color);\n}\n\n// Loop through string characters\nfor (const char of 'Hello') {\n    console.log(char);\n}\n```\n\n**While Loop:**\n```javascript\nlet count = 0;\nwhile (count < 3) {\n    console.log(`Count: ${count}`);\n    count++;\n}\n```",
        
        "Here's a practical loop example:\n\n```javascript\n// Processing a shopping cart\nconst cart = [\n    {name: 'Laptop', price: 999, quantity: 1},\n    {name: 'Mouse', price: 25, quantity: 2},\n    {name: 'Keyboard', price: 75, quantity: 1}\n];\n\nlet total = 0;\nlet itemCount = 0;\n\n// Calculate total price and items\nfor (const item of cart) {\n    const itemTotal = item.price * item.quantity;\n    total += itemTotal;\n    itemCount += item.quantity;\n    \n    console.log(`${item.name}: $${itemTotal}`);\n}\n\nconsole.log(`Total: $${total}`);\nconsole.log(`Items: ${itemCount}`);\n\n// Find expensive items\nconst expensiveItems = [];\nfor (const item of cart) {\n    if (item.price > 50) {\n        expensiveItems.push(item.name);\n    }\n}\n\nconsole.log('Expensive items:', expensiveItems);\n```"
    ],
    
    "object": [
        "Here are object examples:\n\n**Basic Objects:**\n```javascript\n// Object literal\nconst person = {\n    name: 'Alice',\n    age: 28,\n    city: 'New York',\n    isStudent: false\n};\n\n// Accessing properties\nconsole.log(person.name); // 'Alice'\nconsole.log(person['age']); // 28\n\n// Adding/modifying properties\nperson.email = 'alice@example.com';\nperson.age = 29;\n\n// Deleting properties\ndelete person.isStudent;\n```",
        
        "Here's a more complex object example:\n\n```javascript\n// Object with methods\nconst bankAccount = {\n    owner: 'John Doe',\n    balance: 1000,\n    transactions: [],\n    \n    deposit(amount) {\n        if (amount > 0) {\n            this.balance += amount;\n            this.transactions.push({\n                type: 'deposit',\n                amount: amount,\n                date: new Date()\n            });\n            return this.balance;\n        }\n    },\n    \n    withdraw(amount) {\n        if (amount > 0 && amount <= this.balance) {\n            this.balance -= amount;\n            this.transactions.push({\n                type: 'withdrawal',\n                amount: amount,\n                date: new Date()\n            });\n            return this.balance;\n        } else {\n            return 'Insufficient funds';\n        }\n    },\n    \n    getStatement() {\n        return {\n            owner: this.owner,\n            balance: this.balance,\n            transactionCount: this.transactions.length\n        };\n    }\n};\n\nbankAccount.deposit(500);\nbankAccount.withdraw(200);\nconsole.log(bankAccount.getStatement());\n```"
    ]
}

def get_example(topic, example_index=0):
    # Get an example for a specific topic
    if topic in js_examples:
        examples = js_examples[topic]
        if 0 <= example_index < len(examples):
            return examples[example_index]
        else:
            return examples[0]  # Return first example if index is out of range
    return f"I don't have specific examples for {topic} yet. Try asking about the basics first!"


def get_all_examples_for_topic(topic):
    return js_examples.get(topic, [])
