"""
Proxy Usage Examples
====================

This file contains practical examples of how to use proxies with the Traveloka scraper.
"""

from app import TravelokaScraper, SearchParams
import json
import time


def example_1_basic_proxy():
    """Example 1: Basic proxy usage"""

    print("\n" + "="*60)
    print("Example 1: Basic HTTP Proxy")
    print("="*60)

    # Create scraper with proxy
    scraper = TravelokaScraper(proxy_url="http://proxy.example.com:8080")

    try:
        params = SearchParams(
            hotel_id="9000001153383",
            check_in_date={"day": "15", "month": "12", "year": "2025"},
            check_out_date={"day": "16", "month": "12", "year": "2025"},
            num_adults=2
        )

        result = scraper.scrape(params, hotel_name="Novotel Hua Hin")

        if result["success"]:
            print(f"✓ Found {len(result['rates'])} rates via proxy")
        else:
            print(f"✗ Failed: {result.get('error')}")

    finally:
        scraper.close()


def example_2_proxy_with_authentication():
    """Example 2: Proxy with username and password"""

    print("\n" + "="*60)
    print("Example 2: Proxy with Authentication")
    print("="*60)

    # Proxy with authentication
    proxy_url = "http://username:password@proxy.example.com:8080"

    scraper = TravelokaScraper(proxy_url=proxy_url)

    try:
        params = SearchParams(
            hotel_id="9000001153383",
            check_in_date={"day": "15", "month": "12", "year": "2025"},
            check_out_date={"day": "16", "month": "12", "year": "2025"},
            num_adults=2
        )

        result = scraper.scrape(params)

        if result["success"]:
            print(f"✓ Authenticated proxy working")
        else:
            print(f"✗ Authentication failed or proxy error")

    finally:
        scraper.close()


def example_3_socks5_proxy():
    """Example 3: SOCKS5 proxy (requires pysocks)"""

    print("\n" + "="*60)
    print("Example 3: SOCKS5 Proxy")
    print("="*60)

    # SOCKS5 proxy URL
    proxy_url = "socks5://proxy.example.com:1080"

    scraper = TravelokaScraper(proxy_url=proxy_url)

    try:
        params = SearchParams(
            hotel_id="9000001153383",
            check_in_date={"day": "15", "month": "12", "year": "2025"},
            check_out_date={"day": "16", "month": "12", "year": "2025"},
            num_adults=2
        )

        result = scraper.scrape(params)

        if result["success"]:
            print(f"✓ SOCKS5 proxy working")
        else:
            print(f"✗ SOCKS5 proxy failed")

    finally:
        scraper.close()


def example_4_change_proxy_runtime():
    """Example 4: Change proxy during runtime"""

    print("\n" + "="*60)
    print("Example 4: Changing Proxy at Runtime")
    print("="*60)

    # Start with first proxy
    scraper = TravelokaScraper(proxy_url="http://proxy1.example.com:8080")

    try:
        params = SearchParams(
            hotel_id="9000001153383",
            check_in_date={"day": "15", "month": "12", "year": "2025"},
            check_out_date={"day": "16", "month": "12", "year": "2025"},
            num_adults=2
        )

        # Request 1: With proxy 1
        print("\n1. Scraping with Proxy 1...")
        result1 = scraper.scrape(params)
        print(f"   Status: {'✓ Success' if result1['success'] else '✗ Failed'}")

        # Switch to second proxy
        print("\n2. Switching to Proxy 2...")
        scraper.change_proxy("http://proxy2.example.com:8080")

        # Request 2: With proxy 2
        print("\n3. Scraping with Proxy 2...")
        result2 = scraper.scrape(params)
        print(f"   Status: {'✓ Success' if result2['success'] else '✗ Failed'}")

        # Switch to third proxy
        print("\n4. Switching to Proxy 3...")
        scraper.change_proxy("socks5://proxy3.example.com:1080")

        # Request 3: With proxy 3
        print("\n5. Scraping with Proxy 3...")
        result3 = scraper.scrape(params)
        print(f"   Status: {'✓ Success' if result3['success'] else '✗ Failed'}")

    finally:
        scraper.close()


def example_5_proxy_to_direct():
    """Example 5: Switch from proxy to direct connection"""

    print("\n" + "="*60)
    print("Example 5: Proxy to Direct Connection")
    print("="*60)

    scraper = TravelokaScraper(proxy_url="http://proxy.example.com:8080")

    try:
        params = SearchParams(
            hotel_id="9000001153383",
            check_in_date={"day": "15", "month": "12", "year": "2025"},
            check_out_date={"day": "16", "month": "12", "year": "2025"},
            num_adults=2
        )

        # Request 1: With proxy
        print("\n1. Scraping with proxy...")
        result1 = scraper.scrape(params)
        print(f"   Status: {'✓ Success' if result1['success'] else '✗ Failed'}")

        # Disable proxy
        print("\n2. Disabling proxy...")
        scraper.disable_proxy()

        # Request 2: Direct connection
        print("\n3. Scraping without proxy (direct)...")
        result2 = scraper.scrape(params)
        print(f"   Status: {'✓ Success' if result2['success'] else '✗ Failed'}")

    finally:
        scraper.close()


def example_6_proxy_error_handling():
    """Example 6: Handle proxy errors gracefully"""

    print("\n" + "="*60)
    print("Example 6: Error Handling")
    print("="*60)

    proxies_to_test = [
        ("http://valid-proxy.example.com:8080", "Valid Proxy"),
        ("http://invalid-proxy.example.com:8080", "Invalid Proxy"),
        (None, "Direct Connection (No Proxy)"),
    ]

    for proxy_url, proxy_name in proxies_to_test:
        print(f"\nTesting: {proxy_name}")
        print("-" * 40)

        try:
            scraper = TravelokaScraper(proxy_url=proxy_url)

            params = SearchParams(
                hotel_id="9000001153383",
                check_in_date={"day": "15", "month": "12", "year": "2025"},
                check_out_date={"day": "16", "month": "12", "year": "2025"},
                num_adults=2
            )

            result = scraper.scrape(params)

            if result["success"]:
                print(f"✓ {proxy_name}: Success ({len(result['rates'])} rates)")
            else:
                print(f"✗ {proxy_name}: Failed")

            scraper.close()

        except Exception as e:
            print(f"✗ {proxy_name}: Exception - {str(e)}")


def example_7_compare_performance():
    """Example 7: Compare performance with and without proxy"""

    print("\n" + "="*60)
    print("Example 7: Performance Comparison")
    print("="*60)

    params = SearchParams(
        hotel_id="9000001153383",
        check_in_date={"day": "15", "month": "12", "year": "2025"},
        check_out_date={"day": "16", "month": "12", "year": "2025"},
        num_adults=2
    )

    results = []

    # Test 1: Direct connection
    print("\n1. Testing direct connection (no proxy)...")
    scraper = TravelokaScraper()
    start_time = time.time()
    result1 = scraper.scrape(params)
    time1 = time.time() - start_time
    results.append(("Direct Connection", time1, result1["success"]))
    scraper.close()

    # Test 2: HTTP Proxy
    print("\n2. Testing HTTP proxy...")
    scraper = TravelokaScraper(proxy_url="http://proxy.example.com:8080")
    start_time = time.time()
    result2 = scraper.scrape(params)
    time2 = time.time() - start_time
    results.append(("HTTP Proxy", time2, result2["success"]))
    scraper.close()

    # Test 3: SOCKS5 Proxy
    print("\n3. Testing SOCKS5 proxy...")
    scraper = TravelokaScraper(proxy_url="socks5://proxy.example.com:1080")
    start_time = time.time()
    result3 = scraper.scrape(params)
    time3 = time.time() - start_time
    results.append(("SOCKS5 Proxy", time3, result3["success"]))
    scraper.close()

    # Analysis
    print("\n" + "="*60)
    print("PERFORMANCE ANALYSIS")
    print("="*60)

    print(f"\n{'Connection Type':<25} {'Time (s)':<12} {'Status':<10}")
    print("-" * 50)

    for connection_type, elapsed_time, success in results:
        status = "✓ Success" if success else "✗ Failed"
        print(f"{connection_type:<25} {elapsed_time:<12.2f} {status:<10}")

    # Calculate overhead
    direct_time = results[0][1]
    print("\n" + "-" * 50)
    for connection_type, elapsed_time, _ in results[1:]:
        if direct_time > 0:
            overhead = ((elapsed_time - direct_time) / direct_time) * 100
            print(f"{connection_type} overhead: {overhead:+.1f}%")


def example_8_multiple_hotels_with_proxy():
    """Example 8: Batch process multiple hotels through proxy"""

    print("\n" + "="*60)
    print("Example 8: Batch Processing with Proxy")
    print("="*60)

    hotels = [
        {"id": "9000001153383", "name": "Novotel Hua Hin"},
        {"id": "9000001234567", "name": "Sample Hotel 2"},
        {"id": "9000001345678", "name": "Sample Hotel 3"},
    ]

    scraper = TravelokaScraper(proxy_url="http://proxy.example.com:8080")

    try:
        all_rates = []

        for i, hotel in enumerate(hotels, 1):
            print(f"\n{i}. Scraping {hotel['name']}...")

            params = SearchParams(
                hotel_id=hotel["id"],
                check_in_date={"day": "15", "month": "12", "year": "2025"},
                check_out_date={"day": "16", "month": "12", "year": "2025"},
                num_adults=2
            )

            result = scraper.scrape(params, hotel_name=hotel["name"])

            if result["success"]:
                all_rates.extend(result["rates"])
                print(f"   ✓ Found {len(result['rates'])} rates")
            else:
                print(f"   ✗ Failed")

        # Save all results
        print(f"\nSaving {len(all_rates)} total rates to file...")
        with open("batch_results_via_proxy.json", "w") as f:
            json.dump(all_rates, f, indent=2)
        print("✓ Saved to batch_results_via_proxy.json")

    finally:
        scraper.close()


def example_9_environment_variable_proxy():
    """Example 9: Use proxy from environment variable"""

    print("\n" + "="*60)
    print("Example 9: Proxy from Environment Variable")
    print("="*60)

    import os

    # Get proxy from environment variable
    # Usage: export TRAVELOKA_PROXY="http://proxy.example.com:8080"
    proxy_url = os.environ.get("TRAVELOKA_PROXY")

    if not proxy_url:
        print("No TRAVELOKA_PROXY environment variable set")
        print("Usage: export TRAVELOKA_PROXY='http://proxy.example.com:8080'")
        return

    print(f"Using proxy from environment variable...")

    scraper = TravelokaScraper(proxy_url=proxy_url)

    try:
        params = SearchParams(
            hotel_id="9000001153383",
            check_in_date={"day": "15", "month": "12", "year": "2025"},
            check_out_date={"day": "16", "month": "12", "year": "2025"},
            num_adults=2
        )

        result = scraper.scrape(params)

        if result["success"]:
            print(f"✓ Success with proxy from environment")
        else:
            print(f"✗ Failed")

    finally:
        scraper.close()


# Run examples
if __name__ == "__main__":
    print("\n" + "="*60)
    print("PROXY USAGE EXAMPLES")
    print("="*60)

    # Uncomment the examples you want to run

    example_1_basic_proxy()
    # example_2_proxy_with_authentication()
    # example_3_socks5_proxy()
    # example_4_change_proxy_runtime()
    # example_5_proxy_to_direct()
    # example_6_proxy_error_handling()
    # example_7_compare_performance()
    # example_8_multiple_hotels_with_proxy()
    # example_9_environment_variable_proxy()

    print("\n" + "="*60)
    print("EXAMPLES COMPLETED")
    print("="*60)
