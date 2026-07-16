# email_backend_server.py

import os
import html
import smtplib
import ssl
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()  # reads a local .env file if present (never committed -- see .gitignore)

app = Flask(__name__)

# --- EMAIL CREDENTIALS & SETTINGS ---
# Set these via environment variables (or a local .env file, gitignored) --
# never hardcode real credentials here, even for a burner account.
SENDER_EMAIL = os.environ.get("GEOGAME_SENDER_EMAIL", "")
SENDER_PASSWORD = os.environ.get("GEOGAME_SENDER_APP_PASSWORD", "")
RECEIVER_EMAIL = os.environ.get("GEOGAME_RECEIVER_EMAIL", "")

# SMTP Server settings for Gmail
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587 # Port for TLS

@app.route('/send_game_result', methods=['POST'])
def send_game_result():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    username = data.get('username')
    score = data.get('score')
    timestamp = data.get('timestamp')

    if not all([username, score, timestamp]):
        return jsonify({"error": "Missing data (username, score, timestamp)"}), 400

    # Create the email content. Escape everything before interpolating into
    # the HTML body -- these values come straight from the request payload.
    safe_username = html.escape(str(username))
    safe_score = html.escape(str(score))
    safe_timestamp = html.escape(str(timestamp))
    subject = f"Game Result: {safe_username} - Score {safe_score}"
    body = f"""
    <html>
    <body>
        <p><strong>Game Result Notification</strong></p>
        <ul>
            <li><strong>Player:</strong> {safe_username}</li>
            <li><strong>Score:</strong> {safe_score}</li>
            <li><strong>Attempt Time:</strong> {safe_timestamp}</li>
        </ul>
        <p>Good job, {safe_username}!</p>
    </body>
    </html>
    """

    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))

    try:
        # Check if credentials are set (even though they are hardcoded, good practice)
        if not SENDER_EMAIL or not SENDER_PASSWORD:
            print("Error: SENDER_EMAIL or SENDER_PASSWORD not configured in the script.")
            return jsonify({"message": "Server email credentials not configured."}), 500

        # Create a secure SSL context
        context = ssl.create_default_context()
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.ehlo()
            server.starttls(context=context) # Start TLS encryption
            server.ehlo()

            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        print(f"Email sent successfully for {username}!")
        return jsonify({"message": "Email sent successfully"}), 200
    except Exception as e:
        print(f"Error sending email: {e}")
        return jsonify({"message": f"Failed to send email: {str(e)}"}), 500

if __name__ == '__main__':
    # The server will run locally on your PC at http://127.0.0.1:5000/
    # `debug=True` is good for testing (reloads on changes, shows more errors)
    app.run(debug=True, host='127.0.0.1', port=5000)