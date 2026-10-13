import os
import html
import smtplib
import ssl
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re

load_dotenv()  # reads a local .env file if present (never committed -- see .gitignore)

app = Flask(__name__)

# --- EMAIL CREDENTIALS & SETTINGS ---
# Set these via environment variables (or a local .env file, gitignored) --
# never hardcode real credentials here. Gmail: use an App Password, not your
# account password. Create one at https://myaccount.google.com/apppasswords
SENDER_EMAIL = os.environ.get("GEOGAME_SENDER_EMAIL", "")
SENDER_PASSWORD = os.environ.get("GEOGAME_SENDER_APP_PASSWORD", "")
RECEIVER_EMAIL = os.environ.get("GEOGAME_RECEIVER_EMAIL", "")
# To send to a second email, uncomment the line below and set GEOGAME_RECEIVER_EMAIL_2:
# RECEIVER_EMAIL_2 = os.environ.get("GEOGAME_RECEIVER_EMAIL_2", "")

# SMTP Server settings for Gmail
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587  # Port for TLS (for starttls)


# --- Helper function to sanitize strings for safe printing/logging and email content ---
def sanitize_string_for_output(input_data):
    """
    Ensures input (which might be int/float) is converted to string and then
    sanitized to remove null bytes and control characters, preventing OSError: [Errno 22].
    """
    # 1. Convert input (if not already a string) to a string representation
    input_str = str(input_data)

    # 2. Apply sanitization to the string
    sanitized = input_str.replace('\x00', '')  # Remove null bytes (main culprit for OSError 22)

    # Replace other control characters (0x00 to 0x1F and 0x7F to 0x9F) with an underscore
    # This step is critical for console safety on Windows
    sanitized = re.sub(r'[\x00-\x1F\x7F-\x9F]', '_', sanitized)
    return sanitized


@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET,PUT,POST,DELETE,OPTIONS'
    return response


@app.route('/send_game_result', methods=['POST', 'OPTIONS'])
def send_game_result():
    if request.method == 'OPTIONS':
        return '', 204
    if not request.is_json:
        print("ERROR (Server): Request is not JSON.")
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()

    # --- Retrieve and SANITIZE incoming data immediately ---
    raw_username = data.get('username', '')
    raw_score = data.get('budget_calculated', 0)
    raw_timestamp = data.get('timestamp', '')
    raw_level_number = data.get('level_number', 0)

    username = sanitize_string_for_output(raw_username)
    score = sanitize_string_for_output(raw_score)
    timestamp = sanitize_string_for_output(raw_timestamp)
    level_number = sanitize_string_for_output(raw_level_number)

    # VITAL FIX: We now use a single, simple print statement, avoiding the problematic repr() entirely.
    print(f"DEBUG (Server): Sanitized data received: Username='{username}', Score='{score}', Level='{level_number}'")

    # Check if essential data is missing or became empty after sanitization
    if not all([username, score, timestamp, level_number]):
        print(
            f"ERROR (Server): Missing or invalid data after sanitization. Username: '{username}', Score: '{score}', Timestamp: '{timestamp}', Level: '{level_number}'")
        return jsonify(
            {"error": "Missing or invalid data after sanitization (username, score, timestamp, level_number)"}), 400

    # --- Create email content ---
    # Escape everything before interpolating into the HTML body -- all of
    # these values come straight from the request payload, so an unescaped
    # username could inject markup into the email.
    safe_username = html.escape(username)
    safe_score = html.escape(score)
    safe_timestamp = html.escape(timestamp)
    safe_level_number = html.escape(level_number)
    subject = f"Game Result: {safe_username} - Budget {safe_score} - Level {safe_level_number}"
    body = f"""
    <html>
    <body>
        <p><strong>Game Result Notification</strong></p>
        <ul>
            <li><strong>Player:</strong> {safe_username}</li>
            <li><strong>Budget:</strong> {safe_score}</li>
            <li><strong>Level:</strong> {safe_level_number}</li>
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
        # Check if email credentials are set
        if not SENDER_EMAIL or not SENDER_PASSWORD:
            print("ERROR (Server): SENDER_EMAIL or SENDER_PASSWORD not configured in the script.")
            return jsonify({"message": "Server email credentials not configured."}), 500

        context = ssl.create_default_context()
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.ehlo()
            server.starttls(context=context)  # Use starttls for port 587
            server.ehlo()

            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)

        print(f"DEBUG (Server): Email sent successfully for {username} (Level {level_number})!")
        return jsonify({"message": "Email sent successfully"}), 200

    except smtplib.SMTPAuthenticationError as e:
        print(
            f"ERROR (Server): SMTP Authentication Error: {e}. Check SENDER_EMAIL and SENDER_PASSWORD (App Password for Gmail).")
        return jsonify({"message": f"Failed to send email: Authentication error"}), 500
    except smtplib.SMTPConnectError as e:
        print(f"ERROR (Server): SMTP Connection Error: {e}. Check SMTP_SERVER and SMTP_PORT.")
        return jsonify({"message": f"Failed to send email: Connection error"}), 500
    except Exception as e:
        # Catch all other errors and print them safely
        print(f"ERROR (Server): An unexpected error occurred while sending email: {str(e)}")
        return jsonify({"message": f"Failed to send email: {str(e)}"}), 500


if __name__ == '__main__':
    # Make sure Flask debug mode is ON for detailed error messages during development
    app.run(debug=True, host='127.0.0.1', port=5000)
