# backend_notifier.py

import requests
import json
from datetime import datetime

# --- BACKEND SERVER URL ---
# This is the address where your backend server (email_backend_server.py) is running.
# Since it's running on your local machine, '127.0.0.1' (localhost) is correct,
# and '5000' is the port it's using.
BACKEND_URL = "http://127.0.0.1:5000/send_game_result"


def send_game_result_to_backend(username: str, score: int, attempt_timestamp: datetime):
    """
    Sends game results to the backend service for email notification.

    Args:
        username (str): The player's username.
        score (int): The player's score.
        attempt_timestamp (datetime): The timestamp of the successful attempt.
    """

    # Convert the datetime object to an ISO format string for JSON transfer
    timestamp_str = attempt_timestamp.isoformat()

    # The data we'll send to the backend
    payload = {
        "username": username,
        "score": score,
        "timestamp": timestamp_str
    }

    try:
        print(f"[Notifier] Sending results to backend: {payload}")
        # Make a POST request to your backend server
        # 'json=payload' automatically converts the dictionary to JSON
        # 'timeout=5' prevents your game from freezing if the server doesn't respond
        response = requests.post(BACKEND_URL, json=payload, timeout=5)

        # Check the server's response
        if response.status_code == 200:  # 200 means success
            print("[Notifier] Game result sent successfully to backend. Check your email!")
        else:
            # If the server responded with an error code (e.g., 400, 500)
            print(f"[Notifier] Error sending results. Status Code: {response.status_code}")
            print(f"[Notifier] Backend Response: {response.text}")

    except requests.exceptions.ConnectionError as e:
        # This error happens if it can't connect to the server at all
        print(f"[Notifier] Connection error with backend service: {e}")
        print("[Notifier] Ensure the backend server is running and the URL is correct.")
    except requests.exceptions.Timeout as e:
        # This error happens if the server doesn't respond within the timeout period
        print(f"[Notifier] Request to backend service timed out: {e}")
    except requests.exceptions.RequestException as e:
        # Catches other general request-related errors
        print(f"[Notifier] General request error: {e}")
    except Exception as e:
        # Catches any other unexpected errors
        print(f"[Notifier] Unexpected error: {e}")