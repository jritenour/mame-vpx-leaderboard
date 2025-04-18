import os
import re
import time
import requests
import schedule

# ─── CONFIGURATION ─────────────────────────────────────────────────────────────

# Map cabinet identifiers to the directories where their hi score files are located.
CABINET_DIRECTORIES = {
    "arcade": r"/path/to/mame/arcade/hi_scores",      # e.g., used by LaunchBox/BigBox
    "pinball": r"/path/to/vpin/hi_scores",             # e.g., VPIN Studio / Pinup Popper
    "racing": r"/path/to/racing/hi_scores",            # e.g., Drive Turbo Racing Collection
    "flying": r"/path/to/flying/hi_scores"             # Additional dedicated cabinet if needed.
}

# ROM name mapping for friendly display.
ROM_MAPPING = {
    "pacman": "Pac-Man",
    "galaga": "Galaga",
    # Add more mappings as required.
}

# iScored API endpoint for score submission.
API_ENDPOINT = "https://iscored.info/api/score"  # Verify against iScored API documentation

# Dictionary to track processed files (to avoid duplicate uploads).
# We use a mapping: filepath -> last modified timestamp.
processed_files = {}

# ─── FUNCTIONS ──────────────────────────────────────────────────────────────────

def parse_score_file(filepath):
    """
    Parse a text-based hi score file.
    
    Expected format example per line:
      Player: ABC   Score: 123456
    Adjust the regex pattern below to match your actual file format.
    
    Returns:
        A list of tuples: [(player, score), ...]
    """
    scores = []
    try:
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                # Adjust this pattern if your hi score file has a different format.
                match = re.match(r"Player:\s*(\S+)\s+Score:\s*(\d+)", line)
                if match:
                    player = match.group(1)
                    score = int(match.group(2))
                    scores.append((player, score))
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
    return scores

def upload_scores(rom_name, scores, cabinet):
    """
    Map the ROM name to a friendly game name and upload each score
    to the iScored API.
    """
    game_name = ROM_MAPPING.get(rom_name.lower(), rom_name)
    for player, score in scores:
        payload = {
            "game_name": game_name,
            "player": player,
            "score": score,
            "cabinet": cabinet
        }
        try:
            response = requests.post(API_ENDPOINT, json=payload)
            if response.status_code == 201:
                print(f"Uploaded: {game_name} ({cabinet}) - {player}: {score}")
            else:
                print(f"Upload failed for {game_name} ({cabinet}) - {player}.")
                print(f"Status: {response.status_code} | Response: {response.text}")
        except Exception as e:
            print(f"Exception uploading score for {game_name}: {e}")

def process_directory(cabinet, directory):
    """
    Scan the given directory for new or updated score files,
    parse them, and upload the scores.
    """
    global processed_files
    if not os.path.isdir(directory):
        print(f"Directory for cabinet '{cabinet}' does not exist: {directory}")
        return

    for file in os.listdir(directory):
        if file.endswith('.txt'):
            filepath = os.path.join(directory, file)
            last_modified = os.path.getmtime(filepath)
            # Skip files that haven't been updated since last processed.
            if filepath in processed_files and processed_files[filepath] >= last_modified:
                continue

            rom_name = os.path.splitext(file)[0]  # Assumes filename is like 'pacman.txt'
            print(f"Processing file: {filepath} (ROM: {rom_name}, Cabinet: {cabinet})")
            scores = parse_score_file(filepath)
            if scores:
                upload_scores(rom_name, scores, cabinet)
                processed_files[filepath] = last_modified
            else:
                print(f"No valid scores found in {filepath}")

def process_all_directories():
    """
    Process all score directories defined in CABINET_DIRECTORIES.
    """
    for cabinet, directory in CABINET_DIRECTORIES.items():
        process_directory(cabinet, directory)

def job():
    """
    Scheduled job to process score files.
    """
    print("Starting scheduled score processing...")
    process_all_directories()
    print("Scheduled job complete.")

# ─── MAIN EXECUTION ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Schedule the job to run every 15 minutes.
    schedule.every(15).minutes.do(job)
    # Optionally run immediately at startup.
    job()
    
    while True:
        schedule.run_pending()
        time.sleep(1)
