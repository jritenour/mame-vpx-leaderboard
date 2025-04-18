# MameScoreUploader

MameScoreUploader is a Python-based project that automatically scans MAME high score files from multiple directories and uploads the scores to the [iScored API](https://iscored.info/api/).

## Features

- **Multi-Cabinet Support:** Supports separate directories for arcade, pinball, racing, and other cabinets.
- **Custom Parsing:** Parses high score text files (e.g., generated by hi2txt).
- **Friendly Game Name Mapping:** Converts raw ROM names to friendly game names using a mapping file.
- **Scheduled Execution:** Automatically scans for new or updated score files at a set interval (15 minutes by default).
- **API Integration:** Uploads scores to the iScored API endpoint for a centralized, TV-friendly leaderboard display.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/MameScoreUploader.git
   cd MameScoreUploader
   ```

2. **Create a Python virtual environment (optional but recommended):**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Edit the `multi_cab_score_uploader.py` file to set:

- `CABINET_DIRECTORIES`: Dictionary mapping cabinet names to directories where hi score files are stored.
- `ROM_MAPPING`: Dictionary mapping raw ROM names to friendly game names.
- `API_ENDPOINT`: URL for the iScored score submission API.

## Usage

Run the script from the command line:

```bash
python multi_cab_score_uploader.py
```

The script will process score files immediately and then run every 15 minutes. You can adjust the schedule in the code as desired.

## License

This project is open source. Feel free to customize it for your needs.
