"""
Session Configuration
=====================

This file contains all the session/authentication data you need to paste
from your browser. Just copy & paste the values here from DevTools.

HOW TO GET YOUR SESSION DATA:
=============================

1. Open Chrome with your VPN (Urban VPN)
2. Go to https://www.traveloka.com
3. Solve the reCAPTCHA when prompted
4. Press F12 (open DevTools)
5. Click "Application" tab (or "Storage" in Firefox)
6. Left sidebar → "Cookies" → "https://www.traveloka.com"
7. Find the cookies listed below and copy their values
8. Paste them here

WHAT COOKIES TO LOOK FOR:
=========================

aws-waf-token:
  - The main authentication token
  - Long string (150+ characters)
  - Looks like: "326937dd-5b99-4e79-a8ea-ca127f0789c3:EQoAji1jqVqxAAAA:..."
  - THIS IS THE MOST IMPORTANT ONE

Other useful cookies:
  - traveloka_session: Session identifier
  - any other cookies with "traveloka" in the name

"""

# ==============================================================================
# PRIMARY AUTHENTICATION - AWS WAF TOKEN (MOST IMPORTANT!)
# ==============================================================================

# Copy & paste your aws-waf-token value here
# Found in: DevTools → Application → Cookies → aws-waf-token
# This is the KEY token that proves you solved reCAPTCHA
AWS_WAF_TOKEN = "7a32e8e9-74b9-48a6-86e7-99c1395b7ee7:DgoApS58H65bAAAA:5YFfwjLo9ehrn2R6De5hqY7KSK7S1T0QiOjtUB51qxpZtIbB3ppJH4b3skn8EOL2Dg9/wHvtQ6FhTOIH8OQxNZUZNj7mWVLiGoliaLs2m+51ieP4FsqSJODRRXhSwqD6465CZ+cDfJR1WJvMgUnZTsmLW7Zk8eIxoiba9JhPMg/RcEBRqYEdevybhlC59HlgKsvNu4GSIumSNsFSE/+CxZVLUd2/S8GM4ZEhCjMZZD8p5xdZGv0NYJ2Tr8nxnt/3"

# ==============================================================================
# ADDITIONAL SESSION COOKIES (OPTIONAL)
# ==============================================================================

# Copy & paste other Traveloka cookies here if needed
# You can find these in the same location: DevTools → Cookies

# Example: Traveloka session cookie (if present)
TRAVELOKA_SESSION = ""  # e.g., "abc123def456xyz789"

# Example: Any other authentication cookies
OTHER_COOKIES = {
    "currentCountry": "RS",  # CRITICAL - Your country code
    "selectedCurrency": "RSD",  # CRITICAL - Your currency
    "tv-repeat-visit": "true",
    "countryCode": "RS",
    "_gcl_au": "1.1.821755296.1764514738",
    "_tt_enable_cookie": "1",
    "_ttp": "01KBAMCBGC3TTN3GDB86Y0VCH5_.tt.1",
    "_fbp": "fb.1.1764514737732.977017059618964463",
    "_fwb": "78n583br65Hh1vhIjdCyL1.1764514737953",
    "_gid": "GA1.2.1112214255.1764514738",
    "__lt__cid": "a5a0aad5-eee8-47eb-a97c-4943197887a0",
    "tv_user": "{\"authorizationLevel\":100,\"id\":null}",
    "_ly_su": "1764514739.71b7976c-6ce2-4a10-b5f0-9f6b3ce1f730",
    "_yjsu_yjad": "1764514739.4562b3f4-f612-4193-9e07-b6d434590241",
    "g_state": "{\"i_l\":0,\"i_ll\":1764514740049,\"i_b\":\"jOjDS3NMqIkwYCE6/QcX+tQ/zkKTMcEDD3bMLzKtMyM\"}",
    "_cs_ex": "1760605804",
    "_cs_c": "1",
    "__lt__sid": "7f3a1c07-1febe622",
    "ABTastySession": "mrasn",
    "amp_f4354c": "YxB5e3J0GgEKMclNsBBDIH...1jbddhq0t.1jbdejmu8.0.c.c",
    "_gat_UA-29776811-12": "1",
    "wcs_bt": "s_2cb982ada97c:1764609351",
    "cto_bundle": "pFVapV9jekZPRGVZOExiZ3Z6MGpVeFNoY1dkRWFna3cwMXR2RnllUUk0djhuZk1tNjlrcE5tTlUwVk93a3ElMkZRWDJCREJ2THh3T1dENU9jTVlvOWxNTzlka3Z2WmxxaXRKQmE4YSUyQlRMY1Awa2xkajZ3eU5TUG5ra25qMCUyRjBERVkzVTlrRURXNkp1YkNQY1B1TTNzY1ZXWFRTMnJCelF4N3ZwQSUyRndIRElMcFpJVnkxUzlzVzR6NnhmN2xMQXRwMjIlMkZxQ21yV0F4RjU0NHdmMyUyQlRET3BlT3hUSURRJTNEJTNE",
    "ttcsid_CFNI0BRC77UEUGLEG00G": "1764608241882::vZsjF2jGQ0dDtFEZnz0S.9.1764609352827.0",
    "datadome": "y0LW6Elpa3tK7LLumrUYtSFBahtr4y1tyUlY6YCFwaIg~KaC2D0aC40R06qEbK7gwIe2g5LpYiABkhePU25TIPnTfF_3zY5WYbQTrZ8xZNDrNJUZpYcfaXBCM7XZI6~M",
    "_ga": "GA1.2.613465115.1764514738",
    "_ga_RSRSMMBH0X": "GS2.1.s1764608237$o8$g1$t1764609365$j44$l0$h1862309198",
    "amp_1a5adb": "F1Up8i860MRVqAZjCanqM5...1jbddhq0r.1jbdek55m.3b.c.3n",
    "ttcsid": "1764608241883::epn06dm-UHbYrppJ3JfT.8.1764609366498.0",
    "ttcsid_CUM82PBC77U4QKJNCRL0": "1764608253561::aD11DUb16jgt3EYGtUxC.8.1764609366498.0",
    "_dd_s": "rum",
}

BROWSER_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US",
    "Accept-Encoding": "gzip, deflate, br",
    "Content-Type": "application/json",
    "Origin": "https://www.traveloka.com",
    "Referer": "https://www.traveloka.com/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Cache-Control": "no-cache",
    "Pragma": "no-cache"
}

# ==============================================================================
# PROXY CONFIGURATION (IF USING PROXY)
# ==============================================================================

# Your VPN/Proxy URL (if using one)
# Format: "http://proxy.example.com:8080" or "socks5://proxy.example.com:1080"
PROXY_URL = None  # Leave as None if not using proxy

# If your proxy requires authentication:
# Format: "http://username:password@proxy.example.com:8080"
PROXY_WITH_AUTH = None

# ==============================================================================
# HELPER FUNCTION - USE THIS IN YOUR SCRIPT
# ==============================================================================

def get_session_cookies():
    """
    Get all session cookies as a dictionary

    Returns:
        Dictionary of cookies ready to use with requests.Session()
    """
    cookies = {}

    # Add AWS WAF token (most important)
    if AWS_WAF_TOKEN:
        cookies["aws-waf-token"] = AWS_WAF_TOKEN

    # Add Traveloka session if present
    if TRAVELOKA_SESSION:
        cookies["traveloka_session"] = TRAVELOKA_SESSION

    # Add any other cookies
    if OTHER_COOKIES:
        cookies.update(OTHER_COOKIES)

    return cookies


def get_proxy():
    """
    Get proxy URL if configured

    Returns:
        Proxy URL string or None
    """
    return PROXY_WITH_AUTH if PROXY_WITH_AUTH else PROXY_URL


# ==============================================================================
# USAGE EXAMPLES
# ==============================================================================

"""
EXAMPLE 1: Using in your script
=================================

from session_config import get_session_cookies, get_proxy
from app import TravelokaScraper, SearchParams

# Get cookies and proxy from this config file
cookies = get_session_cookies()
proxy = get_proxy()

# Create scraper with your configuration
scraper = TravelokaScraper(
    waf_token=cookies.get("aws-waf-token"),
    proxy_url=proxy
)

# Make requests
params = SearchParams(hotel_id="9000001153383", ...)
result = scraper.scrape(params)


EXAMPLE 2: Direct usage
=================================

from session_config import AWS_WAF_TOKEN, PROXY_URL
from app import TravelokaScraper, SearchParams

scraper = TravelokaScraper(
    waf_token=AWS_WAF_TOKEN,
    proxy_url=PROXY_URL
)

params = SearchParams(hotel_id="9000001153383", ...)
result = scraper.scrape(params)


EXAMPLE 3: Manual cookie management
=================================

from session_config import get_session_cookies
from app import TravelokaScraper, SearchParams

scraper = TravelokaScraper()

# Add all cookies from session_config
cookies = get_session_cookies()
scraper.session.cookies.update(cookies)

params = SearchParams(hotel_id="9000001153383", ...)
result = scraper.scrape(params)
"""

# ==============================================================================
# STEP-BY-STEP: HOW TO FILL THIS FILE
# ==============================================================================

"""
STEP 1: Get AWS WAF Token
========================

1. Open Chrome
2. Activate your VPN (Urban VPN)
3. Go to https://www.traveloka.com
4. Solve the reCAPTCHA
5. Press F12 (DevTools)
6. Click "Application" tab
7. In left sidebar, expand "Cookies"
8. Click "https://www.traveloka.com"
9. Look for a cookie named "aws-waf-token"
10. Click on it and copy the VALUE (the long string)
11. Paste it here, replacing the example value:

    AWS_WAF_TOKEN = "your_token_here"

The token looks like:
    326937dd-5b99-4e79-a8ea-ca127f0789c3:EQoAji1jqVqxAAAA:C3kgvd/...


STEP 2: Get Other Cookies (Optional)
====================================

1. In the same Cookies section
2. Look for any other cookies (traveloka_session, etc.)
3. Copy their values
4. Add them to OTHER_COOKIES dictionary:

    OTHER_COOKIES = {
        "traveloka_session": "value_here",
        "another_cookie": "value_here",
    }


STEP 3: Set Proxy (If Needed)
=============================

If you're using a VPN/Proxy, set:

    PROXY_URL = "http://proxy.example.com:8080"

Or with authentication:

    PROXY_WITH_AUTH = "http://username:password@proxy.example.com:8080"


STEP 4: Use in Your Script
==========================

Then in your main script:

    from session_config import get_session_cookies, get_proxy
    from app import TravelokaScraper, SearchParams

    scraper = TravelokaScraper(
        waf_token=get_session_cookies().get("aws-waf-token"),
        proxy_url=get_proxy()
    )

Done! Your cookies will be automatically added to every request.
"""
