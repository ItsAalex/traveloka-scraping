"""
Session Configuration
=====================
"""

# ==============================================================================
# PRIMARY AUTHENTICATION - AWS WAF TOKEN (MOST IMPORTANT!)
# ==============================================================================

AWS_WAF_TOKEN = "7a32e8e9-74b9-48a6-86e7-99c1395b7ee7:DgoAnPVeKO9gAAAA:xOhdKj5WMaU987D4TDqngLd5/mPxs2mMBCz1CXsb8dtZpZg4kHnA83yzx/77V6sxWFwcerGdbluXUcLT7Cm41pXbudAvVY1D/d9dDdNKZzG3tzzrI1ZO/1UMQwk4hp400ZwWab6LZV/5BdRKayA5deOuCmD2txwWQ1kaKSABrw173Xw2xlHnii0Iq0kVEwZythl1fvfXN5QXxJ0TZErAf7IGfo/k/clNjQLIlqveEpS38of2HynnT+eYNPRqCm7Q"

# ==============================================================================
# ADDITIONAL SESSION COOKIES (OPTIONAL)
# ==============================================================================
TRAVELOKA_SESSION = ""

# Example: Any other authentication cookies
OTHER_COOKIES = {
    "currentCountry": "RS",
    "selectedCurrency": "RSD",
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
    "__lt__sid": "7f3a1c07-d489bfb3",
    "ABTastySession": "mrasn=",
    "amp_f4354c": "YxB5e3J0GgEKMclNsBBDIH...1jbfjaqot.1jbfkdea6.0.e.e",
    "wcs_bt": "s_2cb982ada97c:1764682545",
    "cto_bundle": "9dIr4V9jekZPRGVZOExiZ3Z6MGpVeFNoY1dkQ1NETG5kJTJGUlFrcGlaMllZZThPSFZxU3F0bkxnRWJaN081UyUyQkhLNHZZdGx2MVYxJTJCU1BSWjVqRlIxdHNlWWxtT3lqTG1lY1hBRFhqeFRxOU9KMTA3VkYyQUpjbXg3REoySDh4VEo4cTVpNnF6dXJsajUzMTFPWnhrNkt0V3ZXbFZ0T0FjM1IlMkY1RmMxZllRR0pEeVpydnFseUFwRVRaWTRDN2t6OFNnTGhWbERTQ3dEZG9yOU92TllNV3I5MDk1bkElM0QlM0Q",
    "ttcsid_CFNI0BRC77UEUGLEG00G": "1764681414469::NEzdGfo-ISU7c5bXPVCp.11.1764682546691.0",
    "_ga": "GA1.2.613465115.1764514738",
    "amp_1a5adb": "F1Up8i860MRVqAZjCanqM5...1jbfjaqoq.1jbfkdn2u.4a.e.4o",
    "tvl": "qgdHX7GvehrD9XH5a3S4PUiOJGezXQ9yizVaSxTklwrLYY64AE4apiD1qmHRGaV8gGAQoV6xR5wi1hxtboYegx0JoHbuxL9J5IDMykh7yrn/kmgjvZe3CXlrOt5A94G1h8SGYm0D03zEW7S7g02l9zkAPbkMGQ6AJj+0Bs51j2eJWUUfSgVRqwTDzqipwQI3E8EyIH757Gns+WXTKiHMrEx7DTtkiW3DQvacQnC2TS4BDfxM5AKaL3BV57FQcr/POUY2cWxVPMm8jroO7mWZapq7tP+4mnWc++fDDUD1I5HM0WMA1zSky7I1/5su3gOq8drebnubrSsQUrxquO4VJsT1DY9mAfBGKhL9GRyCUkztC0Qrpfc93mzd8ISGj5NLxbVWc9mUJC6U6r8wkx04c+4CDTx/jJt5ZXoEQTwGFtnKf2gOTYlhb3NCvgFLiPdcxUWvlqKv28eDb2BLCyAyqaqzoBRDz8OG9o8/qkIA122LlqaxXKLAXtO4VBqVI8t42ndIFKV80oqyu2hQkwt5DqBxSdMMGI1wRQokx15o4WE=",
    "tvs": "qgdHX7GvehrD9XH5a3S4PXWKx93/3Xi103f/kPpnhg2VIjp9ir9QAw31NZn2tzJWK/7HSCLbeZ7zv3hxjygOHAJXNKBpJJKziyI1t67KAUQXAClo4NtmN8RDLD50g7akd+gyQzq70AhHhvg65it3EHJ8QJVLDxjwhIbxYg4fKH9bPZBZuDO5H0NNMHQUyz3U1N+0NjAmWhSTtggf9gIHJIaLKSmYGn4epBOkel7pAXzTEEzXgYvUndksxp0RyTokrIgf3gMDGaFdmm79302k4n2QmXE3eQLSvgvRCmmDT3u3NsKhJDtFI1afSbeKadSyXEw2bImmv0C+7A4wSqGznc3wWdOLlzemGQX5jLyfTly7DOej8j0JYXTE/QQBsRQ0dTCOy40pa1AdOWQtNkVOQIvVNfTzlW7ZEM7TsTU0hwz/US3d/Ykd4EWqO2p/tmmLsupfQDFWfHfzzgDFNDYr0M0FrsT6G0XUR6seEe8Ej8Wnw1YOnGV8kt4JC4QoMk74iDroN4P3WbnpgVh8UITypc82T/q88N1401dh6iGcoTodyhX99FtThxxbL49q+hSd",
    "tvo": "L2FwaS92MS90dmxrL2V2ZW50cw==",
    "ttcsid": "1764681414469::9OSc_IdPWmRD2_Adls7n.10.1764682555754.0",
    "ttcsid_CUM82PBC77U4QKJNCRL0": "1764681463295::W43uaqEB2Foe7gNSUhAP.10.1764682555755.0",
    "_ga_RSRSMMBH0X": "GS2.1.s1764681413$o10$g1$t1764682610$j60$l0$h1949565001",
    "datadome": "YdkfHhfvWCWwtHrgpq8e706ufEyNxXoegJRzNgjS~z8Rf09cmtKtM1sKMBn7W~k4WXHW9eSN_OZl7A7E0SrHlDDONhI__5NrOyKnH7cDwmWuigACB1LcJYfC69LHnB9j",
    "_dd_s": "rum=0&expire=1764683511219&logs=1&id=af6af201-8617-4f28-85dd-da8b92ed049e&created=1764681411120",
}

BROWSER_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9,sr;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Content-Type": "application/json",
    "Origin": "https://www.traveloka.com",
    "Priority": "u=1, i",
    "Sec-CH-UA": "\"Chromium\";v=\"142\", \"Google Chrome\";v=\"142\", \"Not_A Brand\";v=\"99\"",
    "Sec-CH-UA-Mobile": "?0",
    "Sec-CH-UA-Platform": "\"Windows\"",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Cache-Control": "no-cache",
    "Pragma": "no-cache",
    "T-A-V": "262393",
    "TV-Country": "TH",
    "TV-Currency": "THB",
    "TV-Language": "en_TH",
    "WWW-App-Version": "release_webacd_20251127-402408096b",
    "X-Client-Interface": "desktop",
    "X-DID": "MDFLQkFNQ0FLMkNCOEVKVkVIRDVRODJFU0g=",
    "X-Domain": "accomRoom",
    "X-Route-Prefix": "en-th"
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
