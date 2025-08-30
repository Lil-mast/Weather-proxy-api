# test_api_key.py

import requests
from decouple import config

# --- CONFIGURATION ---
# Read the API key from the .env file. If it's not found, default to None.
API_KEY = config('OPENWEATHERMAP_API_KEY', default=None)
TEST_CITY = "London"
# Construct the full URL for the API request
API_URL = f"https://api.openweathermap.org/data/2.5/weather?q={TEST_CITY}&appid={API_KEY}&units=metric"

# --- SCRIPT EXECUTION ---
print("--- OpenWeatherMap API Key Test ---")

# First, check if the API key was even found in the .env file.
if not API_KEY:
    print("\n[ERROR] FAILED: API Key not found in .env file.")
    print("Please ensure your .env file is in the project's root directory and contains the line:")
    print("OPENWEATHERMAP_API_KEY=your_key")
else:
    print(f"Found API Key. Attempting to make a test call with city: {TEST_CITY}")
    
    try:
        # Make the actual GET request to the OpenWeatherMap server
        response = requests.get(API_URL)
        
        # This is a critical line: it checks if the response status code is an error (like 401, 404, 500).
        # If it is an error, it will raise an exception and jump to the 'except' block.
        response.raise_for_status()
        
        # If we successfully get past the line above, it means the request was a success (HTTP 200 OK).
        data = response.json()
        temperature = data['main']['temp']
        description = data['weather'][0]['description']
        
        # Print the success message with all details.
        print("\n[SUCCESS] --- Your API Key is ACTIVE and WORKING correctly! ---")
        print("----------------------------------------------------------------")
        print(f"Successfully connected to OpenWeatherMap.")
        print(f"Weather in {TEST_CITY}: {description.capitalize()}")
        print(f"Current Temperature: {temperature}°C")
        print("----------------------------------------------------------------")

    except requests.exceptions.HTTPError as err:
        # This block runs ONLY if the server responded with an error code (4xx or 5xx).
        print("\n[ERROR] FAILED: The server responded with an HTTP error.")
        
        if err.response.status_code == 401:
            print("--> Status Code: 401 (Unauthorized)")
            print("--> REASON: This is an AUTHENTICATION FAILED error. This almost always means one of three things:")
            print("    1. Your API key in the .env file has a typo or is incorrect.")
            print("    2. Your API key is new and not yet active (wait up to 2 hours).")
            print("    3. Your account subscription with OpenWeatherMap does not allow this request.")
            
        elif err.response.status_code == 404:
            print(f"--> Status Code: 404 (Not Found) - The city '{TEST_CITY}' could not be found by the API.")
            
        else:
            print(f"--> Status Code: {err.response.status_code}")
            print(f"--> Details from server: {err.response.text}")

    except requests.exceptions.RequestException as err:
        # This block runs if there was a network problem (e.g., no internet connection).
        print(f"\n[ERROR] FAILED: A network-related error occurred. Could not connect to the server.")
        print(f"--> Details: {err}")