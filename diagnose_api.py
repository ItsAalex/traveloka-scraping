"""
API Diagnostic Tool
===================

This script helps diagnose what's wrong with the API connection.
Run this to see detailed information about requests and responses.
"""

import requests
import json
import sys
from session_config import AWS_WAF_TOKEN, get_proxy, OTHER_COOKIES
from app import SearchParams, TravelokaConfig

# Fix encoding for Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def diagnose():
    """Run diagnostic checks"""

    print("=" * 70)
    print("TRAVELOKA API DIAGNOSTIC")
    print("=" * 70)

    # Check 1: WAF Token
    print("\n1. WAF Token Check")
    print("-" * 70)
    if AWS_WAF_TOKEN:
        print(f"✓ WAF Token found: {AWS_WAF_TOKEN[:50]}...")
        print(f"✓ Token length: {len(AWS_WAF_TOKEN)} characters")
    else:
        print("✗ WAF Token is empty!")
        print("  → Update session_config.py with your AWS WAF token")

    # Check 2: Proxy
    print("\n2. Proxy Configuration")
    print("-" * 70)
    proxy = get_proxy()
    if proxy:
        print(f"✓ Proxy configured: {proxy}")
    else:
        print("✓ No proxy (direct connection)")

    # Check 3: Session Setup
    print("\n3. Session Setup")
    print("-" * 70)

    session = requests.Session()

    # Add headers
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
    }
    session.headers.update(headers)
    print("✓ Browser headers added")

    # Add WAF token as cookie
    if AWS_WAF_TOKEN:
        session.cookies.update({"aws-waf-token": AWS_WAF_TOKEN})
        print(f"✓ WAF token added as cookie")

    # Add other cookies if present
    if OTHER_COOKIES:
        session.cookies.update(OTHER_COOKIES)
        print(f"✓ {len(OTHER_COOKIES)} additional cookies added")

    print(f"\nTotal cookies: {len(session.cookies)}")
    for name, value in session.cookies.items():
        print(f"  - {name}: {value[:50]}..." if len(str(value)) > 50 else f"  - {name}: {value}")

    # Check 4: Test Simple Request
    print("\n4. Test Simple GET Request")
    print("-" * 70)

    try:
        response = session.get(
            "https://www.traveloka.com/",
            timeout=10,
            proxies={"http": proxy, "https": proxy} if proxy else None
        )
        print(f"✓ Request successful: HTTP {response.status_code}")
        if response.status_code == 200:
            print("✓ Website is accessible with your session")
        else:
            print(f"⚠️  Unexpected status code: {response.status_code}")
    except Exception as e:
        print(f"✗ GET request failed: {str(e)}")

    # Check 5: Test API Endpoint
    print("\n5. Test API Endpoint")
    print("-" * 70)

    search_params = SearchParams(
        hotel_id="9000001153383",
        check_in_date={"day": "15", "month": "12", "year": "2025"},
        check_out_date={"day": "16", "month": "12", "year": "2025"},
        num_adults=2
    )

    payload = {
        "clientInterface": "desktop",
        "tid": "test-request-1234",
        "hotelId": search_params.hotel_id,
        "checkInDate": search_params.check_in_date,
        "checkOutDate": search_params.check_out_date,
        "numAdults": search_params.num_adults,
        "numRooms": search_params.num_rooms,
        "currency": search_params.currency,
        "fields": []
    }

    print(f"API Endpoint: {TravelokaConfig.ROOMS_API_ENDPOINT}")
    print(f"Payload: {json.dumps(payload, indent=2)}")

    try:
        response = session.post(
            TravelokaConfig.ROOMS_API_ENDPOINT,
            json=payload,
            timeout=30,
            proxies={"http": proxy, "https": proxy} if proxy else None
        )

        print(f"\n✓ API Request completed")
        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            print("✓ API returned success!")
            data = response.json()
            print(f"Response keys: {list(data.keys())}")
        elif response.status_code == 404:
            print("✗ 404 Not Found - API endpoint may have changed")
            print("Response:", response.text[:200])
        elif response.status_code == 405:
            print("✗ 405 Method Not Allowed - Check request format")
            print("Response:", response.text[:200])
        else:
            print(f"Response: {response.text[:200]}")

    except Exception as e:
        print(f"✗ API request failed: {str(e)}")

    # Check 6: Session Cookies
    print("\n6. Current Session Cookies")
    print("-" * 70)
    print(f"Total cookies in session: {len(session.cookies)}")
    for name, value in session.cookies.items():
        print(f"  ✓ {name}")

    print("\n" + "=" * 70)
    print("DIAGNOSTIC COMPLETE")
    print("=" * 70)

    print("\nNEXT STEPS:")
    print("-" * 70)
    print("If you got a 200 response:")
    print("  ✓ Your setup is working! Run: python main_with_session.py")
    print("\nIf you got a 404 error:")
    print("  → The API endpoint may have changed")
    print("  → Try extracting cookies from a fresh Traveloka session")
    print("\nIf request failed:")
    print("  → Check your internet connection")
    print("  → Check if your WAF token is valid (expires in 2-4 hours)")
    print("  → Get a new token: https://www.traveloka.com → DevTools → Cookies")


if __name__ == "__main__":
    diagnose()
