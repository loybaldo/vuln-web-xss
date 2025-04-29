from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse

app = FastAPI()

# In-memory storage of posts (no database)
posts = []

HTML_HEADER = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>XSS Vulnerable App</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(to right, #f0f4f8, #d9e2ec);
            color: #333;
        }
        .container {
            max-width: 800px;
            margin: 40px auto;
            padding: 30px;
            background: #fff;
            border-radius: 12px;
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.05);
        }
        h2 {
            font-size: 26px;
            margin-bottom: 20px;
            color: #1f2937;
        }
        input[type="text"], input[type="password"], textarea {
            width: 100%;
            padding: 12px;
            margin: 10px 0 20px;
            border: 1px solid #ccc;
            border-radius: 8px;
            font-size: 16px;
            box-sizing: border-box;
        }
        button {
            padding: 10px 20px;
            font-size: 15px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: background 0.3s ease;
        }
        button.submit {
            background-color: #2563eb;
            color: white;
        }
        button.submit:hover {
            background-color: #1e40af;
        }
        button.delete {
            background-color: #ef4444;
            color: white;
        }
        button.delete:hover {
            background-color: #b91c1c;
        }
        .post {
            background: #f9fafb;
            border: 1px solid #e5e7eb;
            padding: 16px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.03);
        }
        .nav {
            margin-top: 30px;
            border-top: 1px solid #e5e7eb;
            padding-top: 20px;
        }
        .nav a {
            margin-right: 15px;
            text-decoration: none;
            color: #2563eb;
            font-weight: 500;
        }
        .nav a:hover {
            text-decoration: underline;
        }
        form {
            margin-bottom: 10px;
        }
    </style>
</head>
<body>
<div class="container">
"""

HTML_FOOTER = """
    <div class="nav">
        <a href="/">🏠 Home</a>
        <a href="/post">➕ Add Post</a>
        <a href="/feed">📰 Feed</a>
        <a href="/login">🔐 Login</a>
    </div>
</div>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def home():
    return HTML_HEADER + """
        <h2>Welcome to XSS Demo</h2>
        <p>This app contains stored and reflected XSS vulnerabilities for testing purposes.</p>
        <ul>
            <li><a href="/post">Submit a post</a> (Stored XSS)</li>
            <li><a href="/feed">View all posts</a></li>
            <li><a href="/login">Go to login</a> (Reflected XSS)</li>
        </ul>
        <form action="/delete-all" method="post" onsubmit="return confirm('Are you sure you want to delete ALL posts?');">
            <button type="submit" class="delete">Delete All Posts</button>
        </form>
    """ + HTML_FOOTER

@app.get("/login", response_class=HTMLResponse)
async def login_form():
    return HTML_HEADER + """
        <h2>Login</h2>
        <form action="/login" method="post">
            <input type="text" name="username" placeholder="Username" required />
            <input type="password" name="password" placeholder="Password" required />
            <button type="submit" class="submit">Login</button>
        </form>
    """ + HTML_FOOTER

@app.post("/login", response_class=HTMLResponse)
async def login(username: str = Form(...), password: str = Form(...)):
    return HTML_HEADER + f"""
        <h2>Login Result</h2>
        <div class="post">Welcome, {username}!</div> <!-- Reflected XSS vulnerability -->
    """ + HTML_FOOTER

@app.get("/post", response_class=HTMLResponse)
async def create_post_form():
    return HTML_HEADER + """
        <h2>Create a Post</h2>
        <form action="/post" method="post">
            <input type="text" name="title" placeholder="Title" required />
            <textarea name="content" placeholder="Write something..." rows="5" required></textarea>
            <button type="submit" class="submit">Post</button>
        </form>
    """ + HTML_FOOTER

@app.post("/post", response_class=HTMLResponse)
async def submit_post(title: str = Form(...), content: str = Form(...)):
    posts.append({'title': title, 'content': content})  # ❌ Vulnerable to Stored XSS
    return HTML_HEADER + f"""
        <h2>Post Submitted!</h2>
        <p>Your post titled <strong>{title}</strong> was added.</p>
        <a href="/feed">View Feed</a>
    """ + HTML_FOOTER

@app.get("/feed", response_class=HTMLResponse)
async def view_feed():
    post_html = ""
    for i, post in enumerate(posts):
        post_html += f"""
        <div class='post'>
            <h3>{post['title']}</h3>
            <p>{post['content']}</p>
            <form action="/delete/{i}" method="post" style="margin-top:10px;">
                <button type="submit" class="delete">Delete</button>
            </form>
        </div>
        """
    return HTML_HEADER + f"""
        <h2>Public Feed</h2>
        {post_html if post_html else "<p>No posts yet.</p>"}
    """ + HTML_FOOTER

@app.post("/delete/{post_id}", response_class=HTMLResponse)
async def delete_post(post_id: int):
    if 0 <= post_id < len(posts):
        deleted = posts.pop(post_id)
        message = f"Deleted post titled <strong>{deleted['title']}</strong>."
    else:
        message = "Invalid post ID."

    return HTML_HEADER + f"""
        <h2>Post Deleted</h2>
        <p>{message}</p>
        <a href="/feed">Back to Feed</a>
    """ + HTML_FOOTER

@app.post("/delete-all", response_class=HTMLResponse)
async def delete_all_posts():
    count = len(posts)
    posts.clear()
    return HTML_HEADER + f"""
        <h2>All Posts Deleted</h2>
        <p>{count} post(s) removed.</p>
        <a href="/">Back to Home</a>
    """ + HTML_FOOTER
