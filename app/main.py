from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse

app = FastAPI()

HTML_HEADER = """
<!DOCTYPE html>
<html>
<head>
    <title>Vulnerable Login - XSS Demo</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 40px;
            background-color: #f0f0f0;
        }
        .container {
            max-width: 400px;
            margin: auto;
            background: white;
            padding: 30px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
            border-radius: 10px;
        }
        input[type="text"], input[type="password"] {
            width: 100%;
            padding: 12px;
            margin-bottom: 20px;
            box-sizing: border-box;
            border-radius: 4px;
            border: 1px solid #ccc;
        }
        button {
            background-color: #28a745;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 4px;
            cursor: pointer;
        }
        button:hover {
            background-color: #218838;
        }
        .output {
            margin-top: 20px;
            padding: 15px;
            background-color: #fff3cd;
            border: 1px solid #ffeeba;
            border-radius: 4px;
        }
        a {
            display: inline-block;
            margin-top: 20px;
            color: #007bff;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
<div class="container">
"""

HTML_FOOTER = """
</div>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def login_form():
    return HTML_HEADER + """
        <h2>Login</h2>
        <form action="/login" method="post">
            <input type="text" name="username" placeholder="Username" required />
            <input type="password" name="password" placeholder="Password" required />
            <button type="submit">Login</button>
        </form>
    """ + HTML_FOOTER

@app.post("/login", response_class=HTMLResponse)
async def login(username: str = Form(...), password: str = Form(...)):
    # VULNERABLE: reflects unsanitized username
    return HTML_HEADER + f"""
        <h2>Login Result</h2>
        <div class="output">Welcome, {username}!</div> <!-- XSS vulnerability -->
        <a href="/">Try again</a>
    """ + HTML_FOOTER
