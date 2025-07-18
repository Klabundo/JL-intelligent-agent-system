# backend/memory_store.py
import json
import os
from datetime import datetime

# Define the directory to store memory files, relative to this script's location.
# os.path.dirname(__file__) gets the directory of the current script.
# os.path.join creates a platform-independent path.
MEMORY_DIR = os.path.join(os.path.dirname(__file__), '..', 'memory')

# Ensure the memory directory exists upon module import.
os.makedirs(MEMORY_DIR, exist_ok=True)

def save_interaction(session_id: str, user_input: str, model_output: str):
    """
    Saves a single user-model interaction to a session-specific JSON file.

    Each session is stored in its own file, named after the session_id.
    Interactions are appended to a list within the JSON file.

    Args:
        session_id: A unique identifier for the chat session.
        user_input: The text provided by the user.
        model_output: The text generated by the model.
    """
    session_file = os.path.join(MEMORY_DIR, f"{session_id}.json")
    
    new_interaction = {
        "timestamp": datetime.utcnow().isoformat() + "Z",  # ISO 8601 format
        "user_input": user_input,
        "model_output": model_output
    }

    history = []
    # If the session file already exists, load its content.
    if os.path.exists(session_file):
        try:
            with open(session_file, 'r', encoding='utf-8') as f:
                history = json.load(f)
        except (json.JSONDecodeError, IOError):
            # If file is corrupted or unreadable, start with a fresh history
            history = []
    
    # Append the new interaction and write back to the file.
    history.append(new_interaction)

    try:
        with open(session_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
    except IOError as e:
        print(f"Error saving interaction to {session_file}: {e}")


def load_history(session_id: str) -> list:
    """
    Loads the full interaction history for a given session ID.

    Args:
        session_id: The unique identifier for the chat session.

    Returns:
        A list of interaction dictionaries, or an empty list if the
        session file doesn't exist or is empty.
    """
    session_file = os.path.join(MEMORY_DIR, f"{session_id}.json")

    if os.path.exists(session_file):
        try:
            with open(session_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            # Return empty list if file is corrupted or unreadable
            return []
    else:
        # Return empty list if no history exists for this session
        return []