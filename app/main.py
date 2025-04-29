from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse

app = FastAPI()

# In-memory storage of posts (no database)
posts = []

HTML_HEADER = """
<!DOCTYPE html>
<html>
<head>
    <title>Vulnerable XSS Demo</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background-color: #f0f0f0; }
        .container { max-width: 600px; margin: auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        input[type="text"], input[type="password"], textarea {
            width: 100%; padding: 12px; margin-bottom: 20px; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box;
        }
        button {
            padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer;
        }
        button.submit { background-color: #007bff; color: white; }
        button.submit:hover { background-color: #0056b3; }
        button.delete { background-color: #dc3545; color: white; }
        button.delete:hover { background-color: #c82333; }
        .post {
            background-color: #fff3cd;
            border: 1px solid #ffeeba;
            padding: 10px;
            margin-bottom: 15px;
            border-radius: 4px;
        }
        a {
            display: inline-block;
            margin-top: 10px;
            color: #007bff;
            text-decoration: none;
        }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
<div class="container">
"""

HTML_FOOTER = """
    <br><a href="/">Home</a> | <a href="/post">Add Post</a> | <a href="/feed">View Feed</a> | <a href="/login">Login</a>
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
