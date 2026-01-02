#!/usr/bin/env python3
"""
Test script to check which Polygon API endpoint works for getting NDX price
"""
import requests
import json

API_KEY = "wsWMG2p9vhDDjVxAHSRz6qbSR_a7B1wL"

print("=" * 80)
print("TESTING POLYGON API ENDPOINTS FOR NDX PRICE")
print("=" * 80)

# Test 1: Indices snapshot
print("\n1. Testing indices snapshot endpoint...")
print("URL: https://api.polygon.io/v2/snapshot/indices/I:NDX")
try:
    url = f"https://api.polygon.io/v2/snapshot/indices/I:NDX?apiKey={API_KEY}"
    response = requests.get(url, timeout=10)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ SUCCESS!")
        print(json.dumps(data, indent=2))
    else:
        print(f"❌ FAILED: {response.text}")
except Exception as e:
    print(f"❌ ERROR: {e}")

# Test 2: Previous day aggregates
print("\n2. Testing previous day aggregates...")
print("URL: https://api.polygon.io/v2/aggs/ticker/I:NDX/prev")
try:
    url = f"https://api.polygon.io/v2/aggs/ticker/I:NDX/prev?apiKey={API_KEY}"
    response = requests.get(url, timeout=10)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ SUCCESS!")
        print(json.dumps(data, indent=2))
        if 'results' in data and len(data['results']) > 0:
            price = data['results'][0]['c']
            print(f"\n💰 NDX Price (previous close): ${price:,.2f}")
    else:
        print(f"❌ FAILED: {response.text}")
except Exception as e:
    print(f"❌ ERROR: {e}")

# Test 3: Current day aggregates (today)
print("\n3. Testing current day aggregates...")
print("URL: https://api.polygon.io/v2/aggs/ticker/I:NDX/range/1/day/...")
try:
    from datetime import datetime, timedelta
    today = datetime.now().strftime("%Y-%m-%d")
    url = f"https://api.polygon.io/v2/aggs/ticker/I:NDX/range/1/day/{today}/{today}?apiKey={API_KEY}"
    response = requests.get(url, timeout=10)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ SUCCESS!")
        print(json.dumps(data, indent=2))
        if 'results' in data and len(data['results']) > 0:
            price = data['results'][0]['c']
            print(f"\n💰 NDX Price (today's close): ${price:,.2f}")
    else:
        print(f"❌ FAILED: {response.text}")
except Exception as e:
    print(f"❌ ERROR: {e}")

# Test 4: Stocks snapshot (wrong endpoint but let's try)
print("\n4. Testing stocks snapshot endpoint (probably wrong)...")
print("URL: https://api.polygon.io/v2/snapshot/locale/us/markets/stocks/tickers/I:NDX")
try:
    url = f"https://api.polygon.io/v2/snapshot/locale/us/markets/stocks/tickers/I:NDX?apiKey={API_KEY}"
    response = requests.get(url, timeout=10)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ SUCCESS!")
        print(json.dumps(data, indent=2))
    else:
        print(f"❌ FAILED: {response.text}")
except Exception as e:
    print(f"❌ ERROR: {e}")

print("\n" + "=" * 80)
print("RECOMMENDATION:")
print("Use whichever endpoint returned SUCCESS with the most recent price data")
print("=" * 80)

