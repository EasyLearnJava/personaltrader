#!/usr/bin/env python3
"""
Test script to verify Polygon.io API key permissions
"""
import requests
import os

# API Key
API_KEY = os.getenv('POLYGON_API_KEY', 'wsWMG2p9vhDDjVxAHSRz6qbSR_a7B1wL')

print("=" * 60)
print("POLYGON.IO API KEY TEST")
print("=" * 60)
print(f"API Key: {API_KEY[:10]}...{API_KEY[-10:]}")
print()

# Test 1: Get NDX current price (stocks endpoint)
print("Test 1: Fetching NDX price (stocks endpoint)...")
try:
    url = f"https://api.polygon.io/v2/aggs/ticker/NDX/prev?apiKey={API_KEY}"
    response = requests.get(url, timeout=10)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ SUCCESS: {data}")
    else:
        print(f"❌ FAILED: {response.text}")
except Exception as e:
    print(f"❌ ERROR: {e}")

print()

# Test 2: Get options contract (options endpoint)
print("Test 2: Fetching options contract (options endpoint)...")
try:
    # Try to get a simple options contract
    url = f"https://api.polygon.io/v3/reference/options/contracts?underlying_ticker=NDX&limit=1&apiKey={API_KEY}"
    response = requests.get(url, timeout=10)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ SUCCESS: {data}")
    else:
        print(f"❌ FAILED: {response.text}")
        if response.status_code == 403:
            print("\n⚠️  ERROR 403: Your API key doesn't have access to options data!")
            print("You need a paid Polygon.io plan (Starter or higher) for options data.")
except Exception as e:
    print(f"❌ ERROR: {e}")

print()
print("=" * 60)

