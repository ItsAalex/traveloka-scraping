"""
Configuration settings for Traveloka Scraper
=============================================

This file contains adjustable configuration parameters for the scraper.
Modify these values based on your specific requirements.
"""

# Rate Limiting Configuration
REQUEST_DELAY = 3  # Seconds between API requests (respect rate limits)
TIMEOUT = 30  # Request timeout in seconds
MAX_RETRIES = 3  # Maximum number of retries for failed requests
RETRY_DELAY = 5  # Base delay between retries (increases exponentially)

# Browser Headers Configuration
# These headers make the scraper appear as a legitimate browser
BROWSER_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

BROWSER_ACCEPT_LANGUAGE = "en-US,en;q=0.9"

# API Configuration
API_BASE_URL = "https://www.traveloka.com"
API_ROOMS_ENDPOINT = "https://www.traveloka.com/api/v2/hotel/search/rooms"

# Output Configuration
OUTPUT_FORMAT = "json"  # json or csv
OUTPUT_DIRECTORY = "./"  # Directory to save output files
DEFAULT_OUTPUT_FILE = "traveloka_rates.json"

# Logging Configuration
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Data Validation Configuration
VALIDATE_REQUIRED_FIELDS = True
VALIDATE_PRICE_RANGES = False  # Set to True to validate price data
MIN_PRICE = 0  # Minimum allowed price
MAX_PRICE = 100000  # Maximum allowed price

# Session Configuration
USE_SESSION_POOLING = True  # Use connection pooling for efficiency
KEEP_ALIVE_TIMEOUT = 30  # Keep-alive timeout in seconds

# Scraping Strategy
MINIMIZE_API_CALLS = True  # Only scrape what's needed
BATCH_PROCESSING_ENABLED = True  # Support batch processing
CACHE_RESPONSES = False  # Cache API responses (requires Redis or similar)

# Default Search Parameters
DEFAULT_CURRENCY = "THB"
DEFAULT_LANGUAGE = "en"
DEFAULT_GUEST_NATIONALITY = "TH"
DEFAULT_NUM_ADULTS = 2
DEFAULT_NUM_CHILDREN = 0
DEFAULT_NUM_ROOMS = 1

# Features
INCLUDE_DEEP_LINKS = True  # Generate shareable deep links
INCLUDE_TIMESTAMPS = True  # Include timestamps in output
EXTRACT_CANCELLATION_POLICY = True
EXTRACT_BREAKFAST_INFO = True
EXTRACT_DISCOUNT_INFO = True
EXTRACT_PER_NIGHT_PRICING = True

# Error Handling
CONTINUE_ON_ERROR = True  # Continue processing if one hotel fails
RETRY_ON_TIMEOUT = True  # Automatically retry on timeout
RETRY_ON_RATE_LIMIT = True  # Automatically retry on rate limit (429)

# Performance Tuning
ENABLE_COMPRESSION = True  # Enable gzip compression for requests
CONNECTION_POOL_SIZE = 10  # Number of connections to maintain
MAX_CONNECTIONS_PER_HOST = 3  # Max connections per host
