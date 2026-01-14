# Traveloka Hotel Rate Scraper

A Python-based web scraper for extracting hotel room rates and availability data from Traveloka's hotel booking platform. This project demonstrates practical solutions for handling modern anti-bot protections and dynamic website data extraction.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technical Architecture](#technical-architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Output Format](#output-format)
- [Limitations & Future Improvements](#limitations--future-improvements)

## Overview

This project solves the challenge of scraping hotel pricing data from Traveloka, a major Southeast Asian travel booking platform. It implements a **hybrid two-phase approach**:

1. **Browser Automation (Selenium)** - Handles authentication and reCAPTCHA challenges
2. **API Requests (Requests)** - Retrieves structured JSON data using authenticated cookies

The scraper extracts comprehensive room information including rates, cancellation policies, breakfast inclusions, and tax breakdowns.

## Features

- **reCAPTCHA Handling** - Manual solving workflow for complex CAPTCHA challenges
- **Cookie-Based Authentication** - Extracts AWS WAF tokens from authenticated sessions
- **Compression Support** - Handles gzip, deflate, and Brotli-compressed responses
- **Structured Output** - Clean JSON format with detailed pricing breakdowns
- **Error Handling** - Retry logic and graceful error management
- **Type Safety** - Uses Python dataclasses for parameter validation
- **Hotel Rate Extraction** - Captures room types, rates, occupancy, and cancellation policies

## Technical Architecture

### Design Pattern: Hybrid Web Scraping

```
┌─────────────────────┐
│  Hotel Search Params│
└──────────┬──────────┘
           │
           ▼
┌─────────────────────────────────────┐
│ Phase 1: Browser Authentication     │
│ • Launch Chrome with Selenium       │
│ • Navigate to hotel page            │
│ • Wait for manual reCAPTCHA solve   │
│ • Extract cookies from session      │
└──────────┬──────────────────────────┘
           │
           ▼
┌─────────────────────────────────────┐
│ Phase 2: API Data Retrieval         │
│ • Build API request payload         │
│ • Execute HTTP request with cookies │
│ • Parse JSON response               │
│ • Extract room rates & details      │
└──────────┬──────────────────────────┘
           │
           ▼
┌──────────────────────┐
│ Output: traveloka_   │
│ rates.json           │
└──────────────────────┘
```

### Core Components

| Component | Purpose |
|-----------|---------|
| `TravelokaScraperWithSelenium` | Main scraper class orchestrating browser and API interactions |
| `SearchParams` | Dataclass encapsulating hotel search parameters |
| `TravelokaConfig` | Configuration constants (URLs, timeouts, API endpoints) |
| `session_config.py` | Credential and cookie storage |

## Prerequisites

- **Python 3.8+**
- **Google Chrome** (for Selenium automation)
- **pip** (Python package manager)

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ItsAalex/traveloka-scraping.git
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv .venv

   # Windows
   .venv\Scripts\activate

   # macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

### Step 1: Extract Session Credentials

The scraper requires valid AWS WAF tokens and session cookies. Extract these from your browser:

1. Open Traveloka.com in Chrome
2. Open DevTools (`F12`)
3. Go to **Application** tab → **Cookies** → filter for `traveloka.com`
4. Copy the `aws-waf-token` cookie value
5. Note any additional session cookies needed

### Step 2: Update session_config.py

Open `session_config.py` and update:

```python
AWS_WAF_TOKEN = "your-aws-waf-token-here"  # 150+ character token from cookie

OTHER_COOKIES = {
    "currentCountry": "TH",
    "selectedCurrency": "THB",
    # Add other cookies as needed
}
```

### Step 3: Configure API Headers (Optional)

Adjust country/language headers in `app.py` if needed:

```python
HEADERS = {
    "T-A-V": "262393",
    "TV-Country": "TH",      # Change to target country
    "TV-Currency": "THB",    # Change to target currency
    "TV-Language": "en_TH",  # Change to target language
}
```

## Usage

### Basic Usage

```python
from app import TravelokaScraperWithSelenium, SearchParams
import json

# Initialize scraper
scraper = TravelokaScraperWithSelenium()

# Setup browser
scraper.setup_browser()

# Define search parameters
search_params = SearchParams(
    hotel_id="9000001153383",
    check_in_date={"day": "16", "month": "12", "year": "2025"},
    check_out_date={"day": "17", "month": "12", "year": "2025"},
    num_adults=2,
    num_children=0,
    num_rooms=1,
    currency="THB",
    language="en_TH"
)

# Execute scrape
result = scraper.scrape(
    search_params,
    hotel_name="Novotel Hua Hin Cha-am Beach Resort & Spa"
)

# Save results
with open("traveloka_rates.json", "w") as f:
    json.dump(result, f, indent=2)

# Cleanup
scraper.close()
```

### Running from Command Line

```bash
python app.py
```

The script will:
1. Open a Chrome browser window
2. Prompt you to manually solve reCAPTCHA (if required)
3. Extract cookies from the authenticated session
4. Fetch hotel rate data
5. Save results to `traveloka_rates.json`

## Project Structure

```
traveloka-scraping/
├── app.py                      # Main scraper application
├── session_config.py           # Credentials and cookie storage
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation (this file)
├── traveloka_rates.json        # Output data (sample)
├── .gitignore                  # Git exclusion rules
└── .venv/                      # Python virtual environment
```

## How It Works

### Phase 1: Authentication via Selenium

1. **Browser Launch** - Initializes Chrome WebDriver with anti-detection measures
2. **Navigation** - Opens the hotel page URL to trigger authentication checks
3. **reCAPTCHA Challenge** - Displays browser window for manual CAPTCHA solving
4. **Cookie Extraction** - Retrieves `aws-waf-token` and session cookies from browser

### Phase 2: Data Retrieval via API

1. **Session Setup** - Creates requests.Session with extracted cookies
2. **Payload Building** - Constructs API request with search parameters
3. **API Call** - POSTs to `/api/v2/hotel/search/rooms` endpoint
4. **Response Parsing** - Extracts room types, rates, policies, and pricing
5. **JSON Output** - Saves structured data to file

## Output Format

The scraper generates a JSON file with the following structure:

```json
{
  "success": true,
  "hotel_name": "Novotel Hua Hin Cha-am Beach Resort & Spa",
  "check_in": {
    "day": "16",
    "month": "12",
    "year": "2025"
  },
  "check_out": {
    "day": "17",
    "month": "12",
    "year": "2025"
  },
  "num_adults": 2,
  "num_children": 0,
  "num_rooms": 1,
  "currency": "THB",
  "timestamp": "2025-12-02T19:04:06.875272",
  "rates": [
    {
      "room_name": "Superior Oceanview",
      "rate_name": "Without Breakfast",
      "number_of_guests": "2",
      "cancellation_policy": "This reservation is non-refundable.",
      "breakfast": "Not Included",
      "price": 254656,
      "currency": "THB",
      "total_taxes": 45075,
      "total_price": 299731,
      "original_price": 399641,
      "net_price_per_stay": 254656,
      "shown_price_per_stay": 254656,
      "total_price_per_stay": 299731
    }
  ]
}
```

### Key Fields

| Field | Description |
|-------|-------------|
| `success` | Boolean indicating successful data retrieval |
| `hotel_name` | Name of the hotel |
| `check_in/check_out` | Date objects for stay period |
| `num_adults/children` | Guest composition |
| `timestamp` | When the scrape was executed |
| `rates` | Array of available room options with pricing |

## Limitations & Future Improvements

### Current Limitations

1. **Manual reCAPTCHA** - Requires human interaction to solve challenges
2. **Single Hotel Per Run** - Scrapes one hotel at a time
3. **Session Expiration** - Credentials expire periodically and require refresh
4. **No Persistence Layer** - Uses file-based output only
5. **Browser Stability** - Selenium WebDriver can have timing issues on slow networks

### Potential Improvements

- [ ] Implement automated CAPTCHA solving (e.g., using anti-CAPTCHA services)
- [ ] Add batch processing for multiple hotels
- [ ] Implement database storage (SQLite/PostgreSQL)
- [ ] Add retry logic with exponential backoff
- [ ] Create API endpoint for on-demand scraping
- [ ] Add data validation and schema enforcement
- [ ] Implement logging system for debugging
- [ ] Add proxy rotation for scale-out scraping
- [ ] Cache results to minimize API calls
- [ ] Create web UI for parameter input

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `requests` | >=2.31.0 | HTTP requests and session management |
| `selenium` | >=4.0.0 | Browser automation |
| `webdriver-manager` | >=4.0.0 | Automatic ChromeDriver management |
| `brotli` | >=1.0.0 | Compression codec support |

## Troubleshooting

### Browser Won't Open
- Ensure Google Chrome is installed
- Check that ChromeDriver matches your Chrome version (auto-managed by webdriver-manager)

### reCAPTCHA Timeout
- Manually solve the CAPTCHA that appears in the browser window
- Ensure you have a valid internet connection

### Authentication Failed
- Check that `aws-waf-token` in `session_config.py` is current
- Re-extract credentials from your browser's DevTools
- Tokens expire periodically and need refreshing

### Empty Rates Array
- Verify the hotel_id is correct
- Ensure search dates have available inventory
- Check that the API response wasn't blocked or rate-limited

## Author

Created as a junior developer portfolio project.

---

**Last Updated:** December 2, 2025
