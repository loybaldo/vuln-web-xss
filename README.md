# XSS Vulnerable Application

This is a demonstration of a web application vulnerable to Cross-Site Scripting (XSS) attacks. The application is built using FastAPI and serves as an educational tool to understand the risks and implications of XSS vulnerabilities.

## Requirements

- [Python 3](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)

## Features

- A simple login form that reflects user input without sanitization.
- Demonstrates how unsanitized input can lead to XSS attacks.

## Installation

1. Create a virtual environment:

   ```bash
   # On Windows
   python -m venv venv

   # On macOS/Linux
   python3 -m venv venv
   ```

2. Activate the virtual environment:

   ```bash
   # On Windows
   venv\Scripts\activate

   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:

   ```bash
   uvicorn app.main:app --reload
   ```

5. Open your browser and navigate to `http://localhost:8000`.

## Usage

- Enter a username and password in the login form.
- Observe how the application reflects the username input directly in the response.
- Test XSS payloads by entering malicious scripts in the username field.

## Example XSS Payload

Try entering the following payload in the username field:

```html
<script>alert('XSS');</script>
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.
