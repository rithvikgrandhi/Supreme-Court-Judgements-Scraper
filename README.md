
# Indian Kanoon Case Scraper

## Description
This Python script automates the process of fetching legal case details from the Indian Kanoon website for years 1949 through 2023. It scrapes data monthly and extracts various elements like case issues, facts, arguments, and conclusions. The output is stored in a JSON Lines file format (`output.jsonl`), which could be useful for further analysis or legal research.

## Prerequisites
To run this script, you will need Python 3 and the following packages:
- `requests`
- `bs4` (BeautifulSoup)
- `re`
- `json`
- `time`

These packages can be installed via pip:
```bash
pip install requests beautifulsoup4
```

## Usage
1. Make sure all prerequisites are installed.
2. Place the script in your desired directory.
3. Run the script using:
   ```bash
   python main.py
   ```
4. The script will start processing data from the year 1949 to 2023, pausing briefly to respect the server's rate limits.
5. Output will be appended to `output.jsonl` in the same directory.

## Features
- **Rate Limiting**: Ensures compliance with web scraping best practices by incorporating delays.
- **Robust Scraping**: Uses BeautifulSoup to parse and extract detailed case information.
- **JSON Lines Output**: Each case's details are saved in a structured JSON Lines format, allowing for easy integration with data processing pipelines.

## Output Format
Each line in `output.jsonl` contains a JSON object with the following keys:
- `instruction`: A general description of the document content.
- `input`: Summarized details including issue, facts, petitioner's arguments, and more.
- `output`: Conclusion and court's reasoning.

## Disclaimer
This script is for educational purposes only. Ensure that you comply with Indian Kanoon's terms of service and relevant legal regulations concerning data scraping and privacy.
