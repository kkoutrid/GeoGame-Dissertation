# email_backend_server.py

import os
import html
import smtplib
import ssl
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re  # <--- IMPORTANT: Added for sanitization

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
def sanitize_string_for_output(input_str):
    """
    Removes null bytes and replaces other non-printable/control characters
    to prevent OSError: [Errno 22] Invalid argument in console and ensure clean logs.
    """
    if not isinstance(input_str, str):  # Ensure it's a string before processing
        return str(input_str)

    sanitized = input_str.replace('\x00', '')  # Remove null bytes (main culprit for OSError 22)
    # Replace other control characters (0x00 to 0x1F and 0x7F to 0x9F) with an underscore
    sanitized = re.sub(r'[\x00-\x1F\x7F-\x9F]', '_', sanitized)
    return sanitized


@app.route('/send_game_result', methods=['POST'])
def send_game_result():
    if not request.is_json:
        print("ERROR (Server): Request is not JSON.")
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()

    # --- Retrieve and SANITIZE incoming data immediately ---
    # Apply sanitization to ensure no problematic characters are carried forward
    # to print statements, log files, or email content.
    raw_username = data.get('username', '')
    raw_score = data.get('budget_calculated', 0)
    raw_timestamp = data.get('timestamp', '')
    raw_level_number = data.get('level_number', 0)  # <--- NEW: Retrieve level_number

    username = sanitize_string_for_output(raw_username)
    score = sanitize_string_for_output(raw_score)  # Ensure score is handled as string for body
    timestamp = sanitize_string_for_output(raw_timestamp)
    level_number = sanitize_string_for_output(raw_level_number)  # <--- NEW: Sanitize level_number

    # DEBUG: Print the sanitized versions to confirm they are clean
    # Using repr() is crucial here to reveal any remaining hidden characters if sanitization fails
    print(f"DEBUG (Server): Sanitized username: '{repr(username)}'")
    print(f"DEBUG (Server): Sanitized score: '{repr(score)}'")
    print(f"DEBUG (Server): Sanitized timestamp: '{repr(timestamp)}'")
    print(f"DEBUG (Server): Sanitized level_number: '{repr(level_number)}'")

    # Check if essential data is missing or became empty after sanitization
    if not all([username, score, timestamp, level_number]):
        print(
            f"ERROR (Server): Missing or invalid data after sanitization. Username: '{username}', Score: '{score}', Timestamp: '{timestamp}', Level: '{level_number}'")
        return jsonify(
            {"error": "Missing or invalid data after sanitization (username, score, timestamp, level_number)"}), 400

    # Create the email content. Escape everything before interpolating into
    # the HTML body -- all of these values come straight from the request
    # payload, so an unescaped username could inject markup into the email.
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

    # Set 'To' header for single or multiple recipients
    # If you uncommented RECEIVER_EMAIL_2 above, change this to:
    # msg['To'] = f"{RECEIVER_EMAIL}, {RECEIVER_EMAIL_2}"
    msg['To'] = RECEIVER_EMAIL  # Default to single recipient

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
            server.ehlo()  # Re-identify after TLS (good practice)

            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)

        # This print should now be safe because all variables used are sanitized
        print(f"DEBUG (Server): Email sent successfully for {username} (Level {level_number})!")
        return jsonify({"message": "Email sent successfully"}), 200  # <--- UNCOMMENTED

    except smtplib.SMTPAuthenticationError as e:
        print(
            f"ERROR (Server): SMTP Authentication Error: {e}. Check SENDER_EMAIL and SENDER_PASSWORD (App Password for Gmail).")
        return jsonify({"message": f"Failed to send email: Authentication error"}), 500
    except smtplib.SMTPConnectError as e:
        print(f"ERROR (Server): SMTP Connection Error: {e}. Check SMTP_SERVER and SMTP_PORT.")
        return jsonify({"message": f"Failed to send email: Connection error"}), 500
    except Exception as e:
        # Using repr(e) to safely print the exception details without risking another OSError
        print(f"ERROR (Server): An unexpected error occurred while sending email: {repr(e)}")
        return jsonify({"message": f"Failed to send email: {str(e)}"}), 500


if __name__ == '__main__':
    # Make sure Flask debug mode is ON for detailed error messages during development
    app.run(debug=True, host='127.0.0.1', port=5000)