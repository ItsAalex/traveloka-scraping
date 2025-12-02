"""
Traveloka Hotel Room Scraper
==============================
A responsible web scraper for extracting hotel room rates from Traveloka.
Implements rate limiting, respectful delays, and proper error handling.

Usage:
    Before running this script, manually solve the reCAPTCHA on Traveloka
    and provide the necessary information below.

Author: Data Extraction Team
"""

import requests
import json
import time
import logging
from typing import Dict, List, Optional
from datetime import datetime
from urllib.parse import urlencode
from dataclasses import dataclass
import uuid

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class SearchParams:
    """Data class for hotel search parameters"""
    hotel_id: str
    check_in_date: Dict[str, str]  # {day, month, year}
    check_out_date: Dict[str, str]  # {day, month, year}
    num_adults: int
    num_children: int = 0
    child_ages: List[int] = None
    num_infants: int = 0
    num_rooms: int = 1
    currency: str = "THB"
    language: str = "en"
    guest_nationality: str = "TH"

    def __post_init__(self):
        if self.child_ages is None:
            self.child_ages = []


class TravelokaConfig:
    """Configuration for Traveloka API requests"""

    # API Endpoints
    BASE_URL = "https://www.traveloka.com"
    ROOMS_API_ENDPOINT = "https://www.traveloka.com/api/v2/hotel/search/rooms"

    # Request configuration
    REQUEST_DELAY = 3  # seconds between requests
    TIMEOUT = 30  # request timeout in seconds
    MAX_RETRIES = 3
    RETRY_DELAY = 5  # seconds to wait before retrying

    # Headers to appear as a legitimate browser
    DEFAULT_HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
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


class TravelokaScraper:
    """
    Main scraper class for extracting hotel room data from Traveloka

    Key Features:
    - Respectful rate limiting (3 second delays)
    - Automatic retry logic with exponential backoff
    - Session management for connection pooling
    - Comprehensive error handling
    - Data validation and normalization
    - Optional proxy support for testing
    """

    def __init__(self, proxy_url: Optional[str] = None,
                 waf_token: Optional[str] = None):
        """
        Initialize the scraper with session and configuration

        Args:
            proxy_url: Optional proxy URL in format:
                      - "http://proxy.example.com:8080"
                      - "https://proxy.example.com:8080"
                      - "socks5://proxy.example.com:1080"
                      - "socks5://username:password@proxy.example.com:1080"
            waf_token: Optional AWS WAF token for authentication
                      - Obtained from Chrome after solving reCAPTCHA
                      - Allows bypassing reCAPTCHA on subsequent requests
        """
        self.session = requests.Session()
        self.session.headers.update(TravelokaConfig.DEFAULT_HEADERS)
        self.last_request_time = 0
        self.proxy_url = proxy_url
        self.waf_token = waf_token

        # Configure WAF token if provided
        if waf_token:
            self._set_waf_token(waf_token)
            logger.info("AWS WAF token configured for authentication")

        # Configure proxy if provided
        if proxy_url:
            self._set_proxy(proxy_url)
            logger.info(f"Traveloka Scraper initialized with proxy: {self._mask_proxy_url(proxy_url)}")
        else:
            logger.info("Traveloka Scraper initialized (no proxy)")

    def _set_waf_token(self, waf_token: str) -> None:
        """
        Set AWS WAF token for Traveloka authentication

        Args:
            waf_token: AWS WAF token obtained from Chrome after solving reCAPTCHA
        """
        try:
            self.session.cookies.update({"aws-waf-token": waf_token})
            logger.info("AWS WAF token set successfully")
        except Exception as e:
            logger.error(f"Error setting WAF token: {str(e)}")
            raise

    def update_waf_token(self, new_waf_token: str) -> None:
        """
        Update AWS WAF token during runtime

        Args:
            new_waf_token: New WAF token to use
        """
        self.waf_token = new_waf_token
        self._set_waf_token(new_waf_token)
        logger.info("AWS WAF token updated")

    def clear_waf_token(self) -> None:
        """Remove AWS WAF token and use reCAPTCHA auth instead"""
        self.session.cookies.pop("aws-waf-token", None)
        self.waf_token = None
        logger.info("AWS WAF token removed")

    def _set_proxy(self, proxy_url: str) -> None:
        """
        Set proxy for the session

        Args:
            proxy_url: Proxy URL in format http://host:port or socks5://host:port
        """
        try:
            # Configure proxies for both http and https
            proxies = {
                "http": proxy_url,
                "https": proxy_url
            }
            self.session.proxies.update(proxies)
            logger.info(f"Proxy configured successfully")
        except Exception as e:
            logger.error(f"Error configuring proxy: {str(e)}")
            raise

    def _mask_proxy_url(self, proxy_url: str) -> str:
        """
        Mask credentials in proxy URL for logging

        Args:
            proxy_url: Full proxy URL with potential credentials

        Returns:
            Masked proxy URL safe to log
        """
        # Extract parts and mask credentials
        if "@" in proxy_url:
            protocol_and_creds, host_port = proxy_url.rsplit("@", 1)
            return f"{protocol_and_creds.split(':')[0]}://***:***@{host_port}"
        return proxy_url

    def change_proxy(self, new_proxy_url: str) -> None:
        """
        Change proxy during runtime

        Args:
            new_proxy_url: New proxy URL to use
        """
        self.proxy_url = new_proxy_url
        self._set_proxy(new_proxy_url)
        logger.info(f"Proxy changed to: {self._mask_proxy_url(new_proxy_url)}")

    def disable_proxy(self) -> None:
        """Disable proxy and use direct connection"""
        self.session.proxies.clear()
        self.proxy_url = None
        logger.info("Proxy disabled, using direct connection")

    def _respect_rate_limit(self):
        """Ensure at least REQUEST_DELAY seconds between requests"""
        elapsed = time.time() - self.last_request_time
        if elapsed < TravelokaConfig.REQUEST_DELAY:
            sleep_time = TravelokaConfig.REQUEST_DELAY - elapsed
            logger.debug(f"Rate limiting: sleeping for {sleep_time:.2f}s")
            time.sleep(sleep_time)

    def _build_request_payload(
        self,
        params: SearchParams,
        contexts: Optional[Dict] = None,
        prev_search_id: str = "undefined"
    ) -> Dict:
        """
        Build the payload for the rooms API request

        Args:
            params: SearchParams object with hotel details
            contexts: Optional context data from previous requests
            prev_search_id: Previous search ID for session continuity

        Returns:
            Dictionary containing the complete request payload
        """

        if contexts is None:
            contexts = {
                "searchContext": "",
                "sortContext": "",
                "filterContext": "",
                "pricingContext": ""
            }

        payload = {
            "clientInterface": "desktop",
            "tid": str(uuid.uuid4()),
            "fields": [],
            "data": {
                "contexts": contexts,
                "prevSearchId": prev_search_id,
                "numInfants": params.num_infants,
                "labelContext": {},
                "monitoringSpec": {
                    "referrer": "",
                    "lastKeyword": ""
                },
                "hotelDetailURL": f"https://www.traveloka.com/en-th/hotel/detail?spec={params.check_in_date['day']}-{params.check_in_date['month']}-{params.check_in_date['year']}.{params.check_out_date['day']}-{params.check_out_date['month']}-{params.check_out_date['year']}.{params.num_rooms}.{params.num_adults}.HOTEL.{params.hotel_id}",
                "marketingContextCapsule": {
                    "amplitude_device_id": "F1Up8i860MRVqAZjCanqM5",
                    "amplitude_session_id": int(datetime.now().timestamp() * 1000),
                    "client_user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
                    "fb_browser_id_fbp": "fb.1.1764514737732.977017059618964463",
                    "ga_client_id": "613465115.1764514738",
                    "ga_session_id": f"s{int(datetime.now().timestamp())}$o1$g0$t{int(datetime.now().timestamp())}$j1$l0$h1",
                    "page_full_url": f"https://www.traveloka.com/en-th/hotel/detail?spec={params.check_in_date['day']}-{params.check_in_date['month']}-{params.check_in_date['year']}.{params.check_out_date['day']}-{params.check_out_date['month']}-{params.check_out_date['year']}.{params.num_rooms}.{params.num_adults}.HOTEL.{params.hotel_id}",
                    "timestamp": str(int(datetime.now().timestamp() * 1000))
                },
                "shouldDisplayAllRooms": False,
                "sourceIdentifier": "HOTEL_DETAIL"
            },
            "ccGuaranteeOptions": {
                "ccInfoPreferences": ["CC_TOKEN", "CC_FULL_INFO"],
                "ccGuaranteeRequirementOptions": ["CC_GUARANTEE"]
            },
            "checkInDate": params.check_in_date,
            "checkOutDate": params.check_out_date,
            "childAges": params.child_ages,
            "currency": params.currency,
            "hasPromoLabel": False,
            "hotelId": params.hotel_id,
            "isExtraBedIncluded": True,
            "isJustLogin": False,
            "isReschedule": False,
            "numAdults": params.num_adults,
            "numChildren": params.num_children,
            "numOfNights": self._calculate_nights(params.check_in_date, params.check_out_date),
            "numRooms": params.num_rooms,
            "preview": False,
            "rateTypes": ["PAY_NOW", "PAY_AT_PROPERTY"],
            "supportedRoomHighlightTypes": ["ROOM"]
        }

        return payload

    @staticmethod
    def _calculate_nights(check_in: Dict[str, str], check_out: Dict[str, str]) -> int:
        """Calculate number of nights between check-in and check-out"""
        check_in_date = datetime(
            int(check_in["year"]),
            int(check_in["month"]),
            int(check_in["day"])
        )
        check_out_date = datetime(
            int(check_out["year"]),
            int(check_out["month"]),
            int(check_out["day"])
        )
        return (check_out_date - check_in_date).days

    def _make_request(self, payload: Dict) -> Optional[Dict]:
        """
        Make API request with retry logic and proxy error handling

        Args:
            payload: Request payload

        Returns:
            Response JSON or None if request fails
        """
        self._respect_rate_limit()

        for attempt in range(TravelokaConfig.MAX_RETRIES):
            try:
                proxy_info = f" (via proxy: {self._mask_proxy_url(self.proxy_url)})" if self.proxy_url else ""
                logger.info(f"Making API request{proxy_info} (attempt {attempt + 1}/{TravelokaConfig.MAX_RETRIES})")
                cookie_keys = list(self.session.cookies.keys())
                has_waf_token = "aws-waf-token" in cookie_keys
                logger.info(f"Cookies being sent: {cookie_keys}")
                logger.info(f"WAF token present: {has_waf_token}")
                logger.debug(f"Request endpoint: {TravelokaConfig.ROOMS_API_ENDPOINT}")
                logger.debug(f"Request payload: {json.dumps(payload, default=str)[:200]}...")

                response = self.session.post(
                    TravelokaConfig.ROOMS_API_ENDPOINT,
                    json=payload,
                    timeout=TravelokaConfig.TIMEOUT
                )

                self.last_request_time = time.time()

                if response.status_code in [200, 202]:
                    logger.info("Request successful")
                    try:
                        return response.json()
                    except:
                        # 202 with empty response is acceptable, return empty data
                        logger.info("Response received (202 with empty body)")
                        return {"success": True}
                elif response.status_code == 429:
                    logger.warning("Rate limited (429). Waiting before retry...")
                    time.sleep(TravelokaConfig.RETRY_DELAY * (attempt + 1))
                elif response.status_code == 407:
                    logger.error("Proxy authentication failed (407)")
                    if attempt < TravelokaConfig.MAX_RETRIES - 1:
                        time.sleep(TravelokaConfig.RETRY_DELAY)
                else:
                    logger.error(f"Request failed with status {response.status_code}")
                    try:
                        error_details = response.text[:500]  # First 500 chars of response
                        logger.error(f"Response: {error_details}")
                    except:
                        pass
                    # Don't retry on 404/403/405 errors - they indicate auth/API issues, not temporary failures
                    if response.status_code in [400, 403, 404, 405]:
                        logger.error("API error - stopping retries (not retryable)")
                        return None
                    if attempt < TravelokaConfig.MAX_RETRIES - 1:
                        time.sleep(TravelokaConfig.RETRY_DELAY)

            except requests.exceptions.ProxyError:
                logger.error(f"Proxy error: Cannot connect to proxy {self._mask_proxy_url(self.proxy_url)}")
                if attempt < TravelokaConfig.MAX_RETRIES - 1:
                    logger.info("Retrying with same proxy...")
                    time.sleep(TravelokaConfig.RETRY_DELAY)
            except requests.exceptions.Timeout:
                logger.error("Request timeout (may be proxy-related)")
                if attempt < TravelokaConfig.MAX_RETRIES - 1:
                    time.sleep(TravelokaConfig.RETRY_DELAY)
            except requests.exceptions.ConnectionError as e:
                logger.error(f"Connection error: {str(e)}")
                if attempt < TravelokaConfig.MAX_RETRIES - 1:
                    time.sleep(TravelokaConfig.RETRY_DELAY)
            except Exception as e:
                logger.error(f"Unexpected error: {str(e)}")
                if attempt < TravelokaConfig.MAX_RETRIES - 1:
                    time.sleep(TravelokaConfig.RETRY_DELAY)

        logger.error("All retry attempts failed")
        return None

    def _extract_rates(self, response_data: Dict) -> List[Dict]:
        """
        Extract and normalize rate information from API response

        Args:
            response_data: Response JSON from API

        Returns:
            List of normalized rate dictionaries
        """
        rates = []

        try:
            rooms = response_data.get("data", {}).get("rooms", [])

            for room in rooms:
                room_name = room.get("name", "")

                # Extract rates for each room
                rate_list = room.get("rates", [])
                for rate in rate_list:
                    normalized_rate = self._normalize_rate(room_name, rate)
                    if normalized_rate:
                        rates.append(normalized_rate)

            logger.info(f"Extracted {len(rates)} rates from response")
            return rates

        except Exception as e:
            logger.error(f"Error extracting rates: {str(e)}")
            return []

    def _normalize_rate(self, room_name: str, rate_data: Dict) -> Optional[Dict]:
        """
        Normalize a single rate entry to match the required schema

        Args:
            room_name: Name of the room
            rate_data: Rate data from API response

        Returns:
            Normalized rate dictionary or None if data is invalid
        """
        try:
            rate_name = rate_data.get("name", "")

            # Extract pricing information
            price_data = rate_data.get("price", {})
            net_price = price_data.get("netPrice", 0)
            net_price_per_night = price_data.get("netPricePerNight", net_price)

            shown_price = price_data.get("shownPrice", net_price)
            shown_price_per_night = price_data.get("shownPricePerNight", shown_price)

            total_price = price_data.get("totalPrice", shown_price)
            total_price_per_night = price_data.get("totalPricePerNight", total_price)

            # Extract taxes
            taxes_data = price_data.get("taxes", {})
            total_taxes = taxes_data.get("totalTaxAmount", 0)

            # Determine if there's a discount
            discounted_price = None
            original_price = None
            if shown_price < net_price:
                discounted_price = shown_price
                original_price = net_price

            # Extract amenities and policies
            includes = rate_data.get("includes", [])
            breakfast_included = any(
                inc.get("id", "").lower() == "free_breakfast"
                for inc in includes
            )

            policies = rate_data.get("policies", [])
            cancellation_policy = next(
                (p.get("description", "") for p in policies
                 if p.get("type", "").lower() == "cancellation"),
                "Not specified"
            )

            # Extract guest information
            occupancy = rate_data.get("occupancy", {})
            num_guests = occupancy.get("numAdults", 0) + occupancy.get("numChildren", 0)

            normalized = {
                "room_name": room_name,
                "rate_name": rate_name,
                "number_of_guests": num_guests,
                "cancellation_policy": cancellation_policy,
                "breakfast": "Included" if breakfast_included else "Not included",
                "currency": rate_data.get("currency", "THB"),
                "total_taxes": total_taxes
            }

            # Add price fields
            if discounted_price is not None:
                normalized["price"] = discounted_price
                normalized["original_price"] = original_price
            else:
                normalized["price"] = shown_price

            normalized["total_price"] = total_price

            # Add per-night pricing if available
            if shown_price_per_night:
                normalized["shown_price_per_stay"] = shown_price_per_night
                normalized["net_price_per_stay"] = net_price_per_night
                normalized["total_price_per_stay"] = total_price_per_night

            return normalized

        except Exception as e:
            logger.error(f"Error normalizing rate: {str(e)}")
            return None

    def _generate_deep_link(self, params: SearchParams) -> str:
        """
        Generate a deep link to the hotel page on Traveloka

        Args:
            params: SearchParams object
            hotel_name: Optional hotel name for URL

        Returns:
            Deep link URL string
        """
        # Format dates as YYYYMMDD
        check_in_str = f"{params.check_in_date['year']}{params.check_in_date['month'].zfill(2)}{params.check_in_date['day'].zfill(2)}"
        check_out_str = f"{params.check_out_date['year']}{params.check_out_date['month'].zfill(2)}{params.check_out_date['day'].zfill(2)}"

        # Build search parameters
        search_params = {
            "hotelId": params.hotel_id,
            "checkIn": check_in_str,
            "checkOut": check_out_str,
            "room": params.num_rooms,
            "adult": params.num_adults,
            "child": params.num_children,
            "currency": params.currency
        }

        query_string = urlencode(search_params)
        deep_link = f"{TravelokaConfig.BASE_URL}/en/hotel/search?{query_string}"

        logger.info(f"Generated deep link: {deep_link}")
        return deep_link

    def scrape(
        self,
        params: SearchParams,
        hotel_name: str = ""
    ) -> Dict:
        """
        Main scraping function

        Args:
            params: SearchParams with hotel search criteria
            hotel_name: Optional hotel name for context

        Returns:
            Dictionary containing rates and metadata
        """
        logger.info(f"Starting scrape for hotel ID: {params.hotel_id}")

        # Build and send request
        payload = self._build_request_payload(params)
        response_data = self._make_request(payload)

        if not response_data:
            logger.error("Failed to retrieve data from API")
            return {
                "success": False,
                "error": "Failed to retrieve data from Traveloka API",
                "hotel_id": params.hotel_id,
                "hotel_name": hotel_name,
                "check_in": params.check_in_date,
                "check_out": params.check_out_date,
                "rates": [],
                "deep_link": self._generate_deep_link(params)
            }

        # Extract rates
        rates = self._extract_rates(response_data)

        # Generate deep link
        deep_link = self._generate_deep_link(params)

        result = {
            "success": True,
            "hotel_id": params.hotel_id,
            "hotel_name": hotel_name,
            "check_in": params.check_in_date,
            "check_out": params.check_out_date,
            "num_adults": params.num_adults,
            "num_children": params.num_children,
            "num_rooms": params.num_rooms,
            "currency": params.currency,
            "deep_link": deep_link,
            "timestamp": datetime.now().isoformat(),
            "rates": rates
        }

        logger.info(f"Scrape completed successfully. Found {len(rates)} rates")
        return result

    def close(self):
        """Close the session"""
        self.session.close()
        logger.info("Scraper session closed")


class TravelokaDataValidator:
    """Validates and verifies extracted data"""

    @staticmethod
    def validate_rate(rate: Dict) -> bool:
        """
        Validate that a rate has all required fields

        Args:
            rate: Rate dictionary to validate

        Returns:
            True if valid, False otherwise
        """
        required_fields = [
            "room_name",
            "rate_name",
            "number_of_guests",
            "cancellation_policy",
            "breakfast",
            "price",
            "currency",
            "total_taxes",
            "total_price"
        ]

        return all(field in rate for field in required_fields)

    @staticmethod
    def validate_result(result: Dict) -> bool:
        """Validate the overall result structure"""
        return (
            "rates" in result and
            isinstance(result["rates"], list) and
            "deep_link" in result and
            "success" in result
        )


# Example usage
def main():
    """
    Example of how to use the Traveloka scraper

    IMPORTANT: Before running this, you need to:
    1. Get your AWS WAF token from Chrome DevTools
    2. Update session_config.py with your token
    3. Run this script
    """

    # Try to import session configuration
    try:
        from session_config import AWS_WAF_TOKEN, get_proxy, get_session_cookies, BROWSER_HEADERS
        waf_token = AWS_WAF_TOKEN if AWS_WAF_TOKEN else None
        proxy = get_proxy()
        session_cookies = get_session_cookies()
        browser_headers = BROWSER_HEADERS if BROWSER_HEADERS else TravelokaConfig.DEFAULT_HEADERS

        if not waf_token:
            print("⚠️  WARNING: AWS_WAF_TOKEN not set in session_config.py")
            print("   The script will still run but may get HTTP 405 errors")
            print("   To fix: Update session_config.py with your token")
            waf_token = None
            proxy = None
    except ImportError as e:
        print("⚠️  session_config.py not found or incomplete, running without WAF token")
        print(f"   Error: {str(e)}")
        waf_token = None
        proxy = None
        session_cookies = {}
        browser_headers = TravelokaConfig.DEFAULT_HEADERS

    # Initialize scraper with WAF token if available
    scraper = TravelokaScraper(waf_token=waf_token, proxy_url=proxy)

    # Update headers with browser headers from session_config
    scraper.session.headers.update(browser_headers)
    logger.info(f"Updated headers with browser User-Agent: {browser_headers.get('User-Agent', 'unknown')[:50]}...")

    # Add all session cookies (including other_cookies, not just WAF token)
    if session_cookies:
        scraper.session.cookies.update(session_cookies)
        logger.info(f"Loaded {len(session_cookies)} session cookies")

    try:
        # Define search parameters
        # IMPORTANT: Update these with actual values from your search
        search_params = SearchParams(
            hotel_id="9000001153383",  # Example: Novotel Hua Hin
            check_in_date={"day": "15", "month": "12", "year": "2025"},
            check_out_date={"day": "16", "month": "12", "year": "2025"},
            num_adults=2,
            num_children=0,
            num_rooms=1,
            currency="THB"
        )

        # Perform scrape
        result = scraper.scrape(search_params, hotel_name="Novotel Hua Hin Cha-Am Beach Resort")

        # Validate result
        if TravelokaDataValidator.validate_result(result):
            logger.info("Data validation passed")

            # Save results to file
            output_file = "traveloka_rates.json"
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            logger.info(f"Results saved to {output_file}")

            # Print summary
            print(f"\n{'='*60}")
            print(f"Scrape Results Summary")
            print(f"{'='*60}")
            print(f"Hotel: {result['hotel_name']}")
            print(f"Check-in: {result['check_in']}")
            print(f"Check-out: {result['check_out']}")
            print(f"Total Rates Found: {len(result['rates'])}")
            print(f"Deep Link: {result['deep_link']}")
            print(f"{'='*60}\n")

            if result['rates']:
                print("Sample Rate:")
                print(json.dumps(result['rates'][0], indent=2))
        else:
            logger.error("Data validation failed")

    finally:
        scraper.close()


if __name__ == "__main__":
    main()
