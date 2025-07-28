import requests # For making HTTP requests to the API
import json     # For parsing JSON responses
import sys      # For system-specific parameters and functions (e.g., exiting)

# --- Configuration ---
# Base URL for the WeatherAPI current weather endpoint
BASE_URL = "http://api.weatherapi.com/v1/current.json"
# Your API key provided by the user
API_KEY = "c5729c55433b442dbf900948252307"

def get_weather_data(city_name):
    """
    Fetches current weather data for a given city using WeatherAPI.

    :param city_name: The name of the city to get weather for.
    :return: A dictionary containing weather data if successful, None otherwise.
    """
    # Construct the full API URL with the city name and API key
    params = {
        "key": API_KEY,
        "q": city_name,
        "aqi": "no" # We are not requesting Air Quality Index in this example
    }

    try:
        print(f"Fetching weather for {city_name}...")
        # Make the GET request to the WeatherAPI
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)

        # Parse the JSON response
        weather_data = response.json()
        return weather_data

    except requests.exceptions.HTTPError as http_err:
        # Handle specific HTTP errors (e.g., 400 for invalid city, 401/403 for invalid API key)
        if response.status_code == 400:
            error_message = weather_data.get('error', {}).get('message', 'Bad request, check city name.')
            print(f"Error: Invalid city or request. {error_message}")
        else:
            print(f"HTTP error occurred: {http_err} - Status Code: {response.status_code}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}. Please check your internet connection.")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Request timed out: {timeout_err}. The server took too long to respond.")
    except requests.exceptions.RequestException as req_err:
        print(f"An unexpected request error occurred: {req_err}")
    except json.JSONDecodeError:
        print("Error: Could not decode JSON response from the API.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return None

def display_weather(data):
    """
    Displays the extracted weather information in a user-friendly format.

    :param data: The dictionary containing parsed weather data.
    """
    if not data or "current" not in data or "location" not in data:
        print("Invalid weather data received. Cannot display.")
        return

    location = data["location"]
    current = data["current"]

    city = location.get("name", "N/A")
    region = location.get("region", "N/A")
    country = location.get("country", "N/A")
    local_time = location.get("localtime", "N/A")

    temp_c = current.get("temp_c", "N/A")
    temp_f = current.get("temp_f", "N/A")
    condition_text = current.get("condition", {}).get("text", "N/A")
    humidity = current.get("humidity", "N/A")
    wind_kph = current.get("wind_kph", "N/A")
    wind_dir = current.get("wind_dir", "N/A")
    pressure_mb = current.get("pressure_mb", "N/A")
    feelslike_c = current.get("feelslike_c", "N/A")
    feelslike_f = current.get("feelslike_f", "N/A")

    print("\n--- Current Weather Conditions ---")
    print(f"Location: {city}, {region}, {country}")
    print(f"Local Time: {local_time}")
    print(f"Condition: {condition_text}")
    print(f"Temperature: {temp_c}°C ({temp_f}°F)")
    print(f"Feels like: {feelslike_c}°C ({feelslike_f}°F)")
    print(f"Humidity: {humidity}%")
    print(f"Wind: {wind_kph} kph {wind_dir}")
    print(f"Pressure: {pressure_mb} mb")
    print("----------------------------------")

def main():
    """
    Main function to run the weather application.
    Allows the user to enter a city name.
    """
    print("Welcome to the Python Weather App!")
    print("Type 'exit' or 'quit' to close the application.")

    while True:
        try:
            city = input("\nEnter city name (e.g., London, New York, Tokyo): ").strip()
            if city.lower() in ["exit", "quit"]:
                print("Exiting Weather App. Goodbye!")
                sys.exit()
            
            if not city:
                print("City name cannot be empty. Please try again.")
                continue

            weather_data = get_weather_data(city)
            if weather_data:
                display_weather(weather_data)
            else:
                print("Could not retrieve weather data for the specified city.")
        except EOFError: # Handle Ctrl+D
            print("\nExiting Weather App. Goodbye!")
            sys.exit()
        except Exception as e:
            print(f"An unexpected error occurred in the main loop: {e}")

if __name__ == "__main__":
    main()
