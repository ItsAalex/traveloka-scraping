"""
Traveloka Hotel Room Scraper with Selenium
===========================================
Uses real Chrome browser for authentication, then extracts data via API.

How it works:
1. Opens real Chrome browser (you control it)
2. You manually solve reCAPTCHA
3. Script extracts cookies from Chrome session
4. Script makes API requests using YOUR session
5. Returns hotel room data

Usage:
    python scraper_with_selenium.py
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

import requests
import json
import time
import logging
from typing import Dict, List, Optional
from datetime import datetime
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
    BASE_URL = "https://www.traveloka.com"
    ROOMS_API_ENDPOINT = "https://www.traveloka.com/api/v2/hotel/search/rooms"
    REQUEST_DELAY = 3
    TIMEOUT = 30
    MAX_RETRIES = 3
    RETRY_DELAY = 5


class TravelokaScraperWithSelenium:
    """Scraper using real browser + requests for API calls"""

    def __init__(self):
        """Initialize with Chrome browser"""
        self.driver = None
        self.session = requests.Session()
        self.last_request_time = 0

        # Add proper headers to mimic browser
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9,sr;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Content-Type": "application/json",
            "Origin": "https://www.traveloka.com",
            "Priority": "u=1, i",
            "Referer": "https://www.traveloka.com/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            # Critical Traveloka headers
            "T-A-V": "262393",
            "TV-Country": "TH",
            "TV-Currency": "THB",
            "TV-Language": "en_TH",
            "WWW-App-Version": "release_webacd_20251127-402408096b",
            "X-Client-Interface": "desktop",
            "X-DID": "MDFLQkFNQ0FLMkNCOEVKVkVIRDVRODJFU0g=",
            "X-Domain": "accomRoom",
            "X-Route-Prefix": "en-th"
        })

        logger.info("TravelokaScraperWithSelenium initialized")

    def setup_browser(self):
        """Open Chrome browser for user to solve reCAPTCHA"""
        try:
            # Configure Chrome options
            chrome_options = Options()
            chrome_options.add_argument("--start-maximized")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)

            # Initialize Chrome driver
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            logger.info("Chrome browser opened successfully")

            return True
        except Exception as e:
            logger.error(f"Failed to open browser: {str(e)}")
            return False

    def wait_for_recaptcha_solve(self, hotel_detail_url: str):
        """
        Navigate to hotel page and wait for user to solve reCAPTCHA

        This is the KEY STEP:
        1. Opens hotel detail page in REAL Chrome
        2. User sees reCAPTCHA
        3. User solves it manually
        4. reCAPTCHA validation happens in this Chrome
        5. Cookies issued in this Chrome
        """
        try:
            logger.info("Opening hotel detail page in Chrome...")
            logger.info("Please solve the reCAPTCHA when it appears in the browser window")
            logger.info("Do NOT close the browser - I'll wait for you to finish")
            logger.info(f"URL: {hotel_detail_url}")

            # Navigate to hotel page
            self.driver.get(hotel_detail_url)

            # IMPORTANT: Traveloka requires user to solve reCAPTCHA
            logger.info("Waiting 20 seconds for initial page load...")
            time.sleep(20)

            logger.info("Page load complete. Proceeding to extract cookies...")

            return True

        except Exception as e:
            logger.error(f"Error during reCAPTCHA solve: {str(e)}")
            return False

    def extract_cookies_from_browser(self) -> Dict:
        """
        Extract all cookies from the Chrome session
        """
        cookies = {}

        logger.info("Extracting cookies from Chrome session...")

        try:
            # Get all cookies from Chrome using Selenium API
            for cookie in self.driver.get_cookies():
                cookies[cookie['name']] = cookie['value']

            logger.info(f"Successfully extracted {len(cookies)} cookies from Chrome session")
            if cookies:
                logger.debug(f"Cookie names: {list(cookies.keys())}")

            return cookies

        except Exception as e:
            logger.error(f"Failed to extract cookies: {str(e)}")
            logger.info("WebDriver crashed or disconnected - this is a known Selenium stability issue")
            logger.info("Returning empty cookies dict")
            return {}

    def update_session_with_browser_cookies(self, cookies: Dict):
        """
        Update requests.Session with cookies from real Chrome session
        """
        self.session.cookies.update(cookies)
        logger.info("requests.Session updated with browser cookies")

    def _build_request_payload(
        self,
        params: SearchParams,
        contexts: Optional[Dict] = None,
        prev_search_id: str = "undefined"
    ) -> Dict:
        """Build the payload for the rooms API request"""

        hotel_detail_url = f"https://www.traveloka.com/en-th/hotel/detail?spec={params.check_in_date['day']}-{params.check_in_date['month']}-{params.check_in_date['year']}.{params.check_out_date['day']}-{params.check_out_date['month']}-{params.check_out_date['year']}.{params.num_rooms}.{params.num_adults}.HOTEL.{params.hotel_id}"

        if contexts is None:
            contexts = {
                "hotelDetailURL": hotel_detail_url,
                "bookingId": None,
                "sourceIdentifier": "HOTEL_DETAIL",
                "shouldDisplayAllRooms": False,
                "marketingContextCapsule": {
                    "amplitude_session_id": int(datetime.now().timestamp() * 1000),
                    "ga_session_id": str(int(datetime.now().timestamp())),
                    "ga_client_id": "613465115.1764514738",
                    "amplitude_device_id": "F1Up8i860MRVqAZjCanqM5",
                    "fb_browser_id_fbp": "fb.1.1764514737732.977017059618964463",
                    "timestamp": str(int(datetime.now().timestamp() * 1000)),
                    "page_full_url": hotel_detail_url,
                    "client_user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36"
                }
            }

        payload = {
            "fields": [],
            "data": {
                "contexts": contexts,
                "prevSearchId": prev_search_id,
                "numInfants": params.num_infants,
                "ccGuaranteeOptions": {
                    "ccInfoPreferences": ["CC_TOKEN", "CC_FULL_INFO"],
                    "ccGuaranteeRequirementOptions": ["CC_GUARANTEE"]
                },
                "rateTypes": ["PAY_NOW", "PAY_AT_PROPERTY"],
                "isJustLogin": False,
                "isReschedule": False,
                "preview": False,
                "monitoringSpec": {
                    "referrer": "",
                    "lastKeyword": ""
                },
                "hotelId": params.hotel_id,
                "currency": params.currency,
                "labelContext": {},
                "isExtraBedIncluded": True,
                "hasPromoLabel": False,
                "supportedRoomHighlightTypes": ["ROOM"],
                "checkInDate": {
                    "day": params.check_in_date["day"],
                    "month": params.check_in_date["month"],
                    "year": params.check_in_date["year"]
                },
                "checkOutDate": {
                    "day": params.check_out_date["day"],
                    "month": params.check_out_date["month"],
                    "year": params.check_out_date["year"]
                },
                "numOfNights": self._calculate_nights(params.check_in_date, params.check_out_date),
                "numAdults": params.num_adults,
                "numRooms": params.num_rooms,
                "numChildren": params.num_children,
                "childAges": params.child_ages,
                "tid": str(uuid.uuid4())
            },
            "clientInterface": "desktop"
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

    def _make_api_request(self, payload: Dict) -> Optional[Dict]:
        """Make API request using browser session cookies"""
        try:
            logger.info("Making API request to get room rates...")
            logger.debug(f"Payload: {json.dumps(payload, indent=2, default=str)[:500]}...")

            response = self.session.post(
                TravelokaConfig.ROOMS_API_ENDPOINT,
                json=payload,
                timeout=TravelokaConfig.TIMEOUT
            )

            logger.info(f"API Response status: {response.status_code}")
            logger.info(f"Response headers: {dict(response.headers)}")
            logger.info(f"Response content length: {len(response.content)}")
            logger.info(f"Response text length: {len(response.text)}")

            # Check if response is gzip-encoded
            if response.headers.get('Content-Encoding') == 'gzip':
                logger.info("Response is gzip-encoded, requests should handle it...")

            # Try different decoding approaches
            logger.info(f"Response text preview (first 500 chars): {response.text[:500]}")

            if response.status_code in [200, 202]:
                try:
                    # Try to parse as JSON
                    data = response.json()
                    logger.info(f"Successfully parsed JSON response")
                    logger.info(f"Response data keys: {data.keys() if isinstance(data, dict) else 'Not a dict'}")

                    # Save raw response for inspection
                    with open("api_response_raw.json", "w", encoding="utf-8") as f:
                        json.dump(data, f, indent=2, ensure_ascii=False)
                    logger.info("Raw API response saved to api_response_raw.json")

                    return data
                except Exception as e:
                    logger.warning(f"Failed to parse JSON: {str(e)}")

                    # Try to see if content is actually valid
                    try:
                        # Maybe the text is corrupted, try content
                        logger.info(f"Attempting to decode content as utf-8...")
                        decoded_text = response.content.decode('utf-8')
                        logger.info(f"Decoded text preview: {decoded_text[:200]}")
                        data = json.loads(decoded_text)
                        logger.info(f"Successfully parsed JSON from decoded content")
                        return data
                    except Exception as e2:
                        logger.error(f"Could not decode: {str(e2)}")
                        return {"data": {"rooms": []}}
            else:
                logger.error(f"API Error: {response.status_code}")
                logger.error(f"Response: {response.text[:500]}")
                return None

        except Exception as e:
            logger.error(f"Error making API request: {str(e)}")
            return None

    def _extract_rates(self, response_data: Dict) -> List[Dict]:
        """Extract room rates from API response - matches task requirements exactly"""
        try:
            if not response_data:
                return []

            # Traveloka API structure: data.recommendedEntries[] -> each has hotelRoomInventoryList[]
            recommended_entries = response_data.get("data", {}).get("recommendedEntries", [])
            rates = []

            for room in recommended_entries:
                room_name = room.get("name", "Unknown Room")
                max_occupancy = room.get("maxOccupancy", room.get("baseOccupancy", "2"))

                # Each room has multiple inventory options (different rates/breakfast combos)
                inventory_list = room.get("hotelRoomInventoryList", [])

                for inventory in inventory_list:
                    try:
                        # Extract pricing information
                        rate_display = inventory.get("rateDisplay", {})
                        total_fare = rate_display.get("totalFare", {})
                        base_fare = rate_display.get("baseFare", {})
                        original_rate = inventory.get("originalRateDisplay", {})
                        original_total = original_rate.get("totalFare", {})

                        # Extract cancellation policy
                        cancellation_policy = inventory.get("roomCancellationPolicy", {})
                        cancellation_label = cancellation_policy.get("cancellationPolicyLabel", "N/A")

                        # Check if breakfast is included
                        meal_plan = inventory.get("mealPlanDisplay", {})
                        breakfast_display = meal_plan.get("displayMealPlanIncluded", "")
                        is_breakfast_included = inventory.get("isBreakfastIncluded", False)

                        # Calculate prices (per night)
                        total_price_per_night = int(total_fare.get("amount", 0))
                        net_price_per_night = int(base_fare.get("amount", 0))
                        total_taxes = total_price_per_night - net_price_per_night
                        original_price = int(original_total.get("amount", 0))
                        currency = total_fare.get("currency", "THB")

                        # Determine if there's a discount
                        has_discount = original_price > 0 and original_price != total_price_per_night

                        # Build rate object matching exact requirements
                        rate = {
                            "room_name": room_name,
                            "rate_name": inventory.get("roomInventoryGroupOption", "Standard"),
                            "number_of_guests": str(max_occupancy),
                            "cancellation_policy": cancellation_label,
                            "breakfast": breakfast_display if is_breakfast_included else "Not Included",
                            "price": net_price_per_night if has_discount else total_price_per_night,
                            "currency": currency,
                            "total_taxes": total_taxes,
                            "total_price": total_price_per_night,
                        }

                        # Add original price if discounted
                        if has_discount:
                            rate["original_price"] = original_price

                        # Per night breakdown (as required)
                        rate["net_price_per_stay"] = net_price_per_night
                        rate["shown_price_per_stay"] = net_price_per_night
                        rate["total_price_per_stay"] = total_price_per_night

                        rates.append(rate)

                    except Exception as item_e:
                        logger.warning(f"Error parsing inventory item: {str(item_e)}")
                        continue

            logger.info(f"Extracted {len(rates)} room rates from {len(recommended_entries)} room types")
            return rates

        except Exception as e:
            logger.error(f"Error extracting rates: {str(e)}")
            logger.error(f"Response data keys: {response_data.keys() if isinstance(response_data, dict) else 'Not a dict'}")
            return []

    def scrape(self, params: SearchParams, hotel_name: str = "") -> Dict:
        """
        Main scraping function

        FLOW:
        1. Build hotel detail URL (with hotel name!)
        2. Open in Chrome (user solves reCAPTCHA)
        3. Extract cookies from Chrome quickly before browser crashes
        4. Use cookies to make API requests
        5. Parse and return data
        """
        logger.info(f"Starting scrape for hotel: {hotel_name}")

        # Build hotel detail URL - CRITICAL: Include hotel name at end!
        from urllib.parse import quote
        hotel_name_encoded = quote(hotel_name.replace(" ", " "))
        hotel_detail_url = f"https://www.traveloka.com/en-th/hotel/detail?spec={params.check_in_date['day']}-{params.check_in_date['month']}-{params.check_in_date['year']}.{params.check_out_date['day']}-{params.check_out_date['month']}-{params.check_out_date['year']}.{params.num_rooms}.{params.num_adults}.HOTEL.{params.hotel_id}.{hotel_name_encoded}.2"

        # Step 1: Open browser and wait for reCAPTCHA solve
        if not self.wait_for_recaptcha_solve(hotel_detail_url):
            logger.error("Failed to handle reCAPTCHA")
            return {"success": False, "error": "Failed to handle reCAPTCHA"}

        # Step 2: Extract page HTML to inspect what's actually rendered
        logger.info("Capturing page HTML for inspection...")
        try:
            page_source = self.driver.page_source
            with open("page_source.html", "w", encoding="utf-8") as f:
                f.write(page_source)
            logger.info(f"Page HTML saved to page_source.html (length: {len(page_source)})")
        except Exception as e:
            logger.warning(f"Could not capture page source: {str(e)}")

        # Step 3: Extract cookies from Chrome session
        logger.info("Extracting cookies immediately to avoid browser instability...")
        cookies = self.extract_cookies_from_browser()
        if cookies:
            logger.info(f"Extracted {len(cookies)} cookies from browser")
            # Step 4: Update requests.Session with these cookies
            self.update_session_with_browser_cookies(cookies)
        else:
            logger.warning("No cookies extracted from browser - continuing with existing session")
            # Try to use cookies from session_config as fallback
            try:
                from session_config import get_session_cookies
                fallback_cookies = get_session_cookies()
                if fallback_cookies:
                    logger.info(f"Using {len(fallback_cookies)} cookies from session_config as fallback")
                    self.update_session_with_browser_cookies(fallback_cookies)
                else:
                    logger.warning("No fallback cookies available")
            except Exception as e:
                logger.warning(f"Could not load fallback cookies: {str(e)}")

        # Step 4: Build and send API request
        payload = self._build_request_payload(params)
        response_data = self._make_api_request(payload)

        # Step 5: Extract rates
        rates = self._extract_rates(response_data) if response_data else []

        # Step 6: Assemble result
        result = {
            "success": True,
            "hotel_name": hotel_name,
            "check_in": params.check_in_date,
            "check_out": params.check_out_date,
            "num_adults": params.num_adults,
            "num_children": params.num_children,
            "num_rooms": params.num_rooms,
            "currency": params.currency,
            "timestamp": datetime.now().isoformat(),
            "rates": rates,
            "deep_link": f"https://www.traveloka.com/en/hotel/search?hotelId={params.hotel_id}&checkIn={params.check_in_date['day']}{params.check_in_date['month']}{params.check_in_date['year']}&checkOut={params.check_out_date['day']}{params.check_out_date['month']}{params.check_out_date['year']}&room={params.num_rooms}&adult={params.num_adults}&child={params.num_children}&currency={params.currency}"
        }

        logger.info(f"Scrape completed. Found {len(rates)} rates")
        return result

    def close(self):
        """Close browser and session"""
        if self.driver:
            self.driver.quit()
            logger.info("Browser closed")
        self.session.close()
        logger.info("Session closed")


def main():
    """Main execution"""
    scraper = TravelokaScraperWithSelenium()

    try:
        # Setup browser
        if not scraper.setup_browser():
            logger.error("Failed to setup browser")
            return

        # Define search parameters
        search_params = SearchParams(
            hotel_id="9000001153383",
            check_in_date={"day": "16", "month": "12", "year": "2025"},
            check_out_date={"day": "17", "month": "12", "year": "2025"},
            num_adults=2,
            num_children=0,
            num_rooms=1,
            currency="THB"
        )

        # Perform scrape
        result = scraper.scrape(search_params, hotel_name="novotel hua hin cha-am beach resort & spa")

        # Save results
        with open("traveloka_rates.json", "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        logger.info("Results saved to traveloka_rates.json")

        # Print summary
        print("\n" + "="*60)
        print("SCRAPE RESULTS")
        print("="*60)
        print(f"Hotel: {result.get('hotel_name', 'N/A')}")
        print(f"Check-in: {result.get('check_in', {}).get('day', '?')}-{result.get('check_in', {}).get('month', '?')}-{result.get('check_in', {}).get('year', '?')}")
        print(f"Check-out: {result.get('check_out', {}).get('day', '?')}-{result.get('check_out', {}).get('month', '?')}-{result.get('check_out', {}).get('year', '?')}")
        print(f"Total Rates Found: {len(result.get('rates', []))}")
        if result.get('rates'):
            print(f"\nFirst Room Rate:")
            print(json.dumps(result['rates'][0], indent=2))
        print("="*60 + "\n")

    except Exception as e:
        logger.error(f"Error in main: {str(e)}")
    finally:
        # Keep browser open for a moment so user can see results
        logger.info("Browser will close in 10 seconds...")
        time.sleep(10)
        scraper.close()


if __name__ == "__main__":
    main()
