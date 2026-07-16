# backend_notifier.py

import requests
import json
from datetime import datetime

# --- BACKEND SERVER URL ---
# This is the address where your backend server (email_backend_server.py) is running.
BACKEND_URL = "http://127.0.0.1:5000/send_game_result"


def send_game_result_to_backend(username: str, score: int, attempt_timestamp: datetime, level: int):
    """
    Sends game results (including level) to the backend service for email notification.

    Args:
        username (str): The player's username.
        score (int): The player's score.
        attempt_timestamp (datetime): The timestamp of the successful attempt.
        level (int): The level number achieved.
    """

    # Convert the datetime object to an ISO format string for JSON transfer
    timestamp_str = attempt_timestamp.isoformat()

    # The data we'll send to the backend
    payload = {
        "username": username,
        "budget_calculated": score,
        "timestamp": timestamp_str,
        "level_number": level,  # <--- NEW: Include level number
    }

    try:
        print(f"[Notifier] Sending results to backend: {payload}")
        response = requests.post(BACKEND_URL, json=payload, timeout=5)

        # Check the server's response
        if response.status_code == 200:
            print("[Notifier] Game result sent successfully to backend. Check your email!")
        else:
            print(f"[Notifier] Error sending results. Status Code: {response.status_code}")
            print(f"[Notifier] Backend Response: {response.text}")

    except requests.exceptions.ConnectionError as e:
        print(f"[Notifier] Connection error with backend service: {e}")
        print("[Notifier] Ensure the backend server is running and the URL is correct.")
    except requests.exceptions.Timeout as e:
        print(f"[Notifier] Request to backend service timed out: {e}")
    except requests.exceptions.RequestException as e:
        print(f"[Notifier] General request error: {e}")
    except Exception as e:
        print(f"[Notifier] Unexpected error: {e}")


# --- Example of how you might call this function in your main game logic ---
# (This part is for your reference, don't just paste it blindly into the file)
if __name__ == '__main__':
    # This block is just for testing this script in isolation
    from datetime import datetime
    import time

    test_username = "TestPlayer"
    test_score = 7500
    test_level = 5  # Example level

    print("--- Running a test send ---")
    send_game_result_to_backend(test_username, test_score, datetime.now(), test_level)
    print("--- Test send complete ---")

    # Simulate another player/attempt after a short delay
    time.sleep(2)
    test_username_2 = "AnotherPlayer"
    test_score_2 = 9200
    test_level_2 = 7
    print("\n--- Running a second test send ---")
    send_game_result_to_backend(test_username_2, test_score_2, datetime.now(), test_level_2)
    print("--- Second test send complete ---")