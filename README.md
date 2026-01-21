# Adzuna Job Scraper

A Python Tkinter GUI application for searching jobs on the Adzuna job board API.

## Features

- Search for jobs using Adzuna API
- Custom search terms and locations
- Dedicated results window displaying job counts
- Error handling for API failures

## Requirements

- Python 3.6+
- `requests` library

Install dependencies:
```bash
pip install requests
```

## Setup

1. Clone or download the project
2. Create a `.env` file in the project root with your Adzuna credentials:
```
ADZUNA_APP_ID=your_app_id
ADZUNA_API_KEY=your_api_key
```

3. Get your API credentials from [Adzuna](https://developer.adzuna.com/)

## Usage

Run the application:
```bash
python AdzunaApiScraper.py
```

1. Enter your Adzuna Application ID
2. Enter your Adzuna API Key
3. (Optional) Enter a search term (defaults to "python")
4. (Optional) Enter a location (defaults to "UK")
5. Click "Fetch Total Jobs"
6. View results in the new window

## Project Structure

```
AdzunaApiScraper/
├── AdzunaApiScraper.py    # Main application
├── test_adzuna.py         # Unit tests
├── .env                   # API credentials (not in git)
└── README.md              # This file
```

## Functions

### `get_adzuna_jobs(app_id, api_key, search_term, location)`
Fetches total job count from Adzuna API.

**Parameters:**
- `app_id` (str): Adzuna Application ID
- `api_key` (str): Adzuna API Key
- `search_term` (str): Job search term (default: "python")
- `location` (str): Job location (default: "UK")

**Returns:** Integer job count or None on error

### `show_results_window(adzuna_total, search_term, location)`
Displays search results in a new Tkinter window.

**Parameters:**
- `adzuna_total` (int): Total jobs found
- `search_term` (str): The search term used
- `location` (str): The location searched

### `fetch_jobs()`
GUI event handler for the "Fetch Total Jobs" button.

## Testing

Run tests:
```bash
python -m unittest test_adzuna.py -v
```

Test coverage includes:
- Successful API calls
- API error handling
- Missing data handling

## Error Handling

- Invalid API credentials show error dialog
- Network errors are caught and logged
- Missing response data defaults to 0 jobs

## License

MIT
