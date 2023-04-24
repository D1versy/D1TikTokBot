import os
from datetime import datetime


def log_unique_user_id(user_id, log_file='Users.log'):
    unique_user_ids = set()

    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            for line in f.readlines():
                line = line.strip()
                if line:
                    unique_user_ids.add(int(line))

    if user_id not in unique_user_ids:
        unique_user_ids.add(user_id)
        with open(log_file, 'a') as f:
            f.write(f"{user_id}\n")

# Save user request to a separate file
def user_history_logger(user_name, user_id, message_text):
    filename = f'{user_name or user_id}.txt'
    filepath = os.path.join('./logs', filename)

    # Create 'logs' directory if it doesn't exist
    os.makedirs('./logs', exist_ok=True)

    with open(filepath, "a+", encoding='utf-8') as file:
        file.write(
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {user_name or user_id} Downloaded: {message_text}")
        file.write("\n")


