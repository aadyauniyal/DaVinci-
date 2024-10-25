import os
import requests
import google.generativeai as genai

# Configure the Google Gemini API key
api_key_gemini = os.getenv("AI_API_KEY")  # Read from environment variable
genai.configure(api_key=api_key_gemini)

# RapidAPI key
rapidapi_key = os.getenv("YOUR_RAPID_KEY")  # Read from environment variable

# Gemini configuration
generation_config = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
}

# Start the chat with Gemini model
def get_gemini_response(user_input):
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )

    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [user_input],
            },
        ]
    )
    return chat_session.send_message(user_input)

# Extract flight information from the Gemini response
def extract_travel_details(response_text):
    if "Toronto" in response_text and "New York" in response_text:
        return {
            "origin": "YYZ",  # Toronto Pearson
            "destination": "JFK",  # New York JFK
            "departure_date": "2024-11-05",
            "return_date": "2024-11-10",
            "adults": 1,
        }
    else:
        return None

# Function to fetch flights using the RapidAPI
def get_flight_info(api_key, origin, destination, departure_date, return_date, adults):
    url = "https://booking-com15.p.rapidapi.com/v1/flights"  # Use the correct endpoint

    query_params = {
        "origin": origin,
        "destination": destination,
        "departure_date": departure_date,
        "return_date": return_date,
        "adults": adults
    }

    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "booking-com15.p.rapidapi.com"  # Correct host
    }

    response = requests.get(url, headers=headers, params=query_params)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to retrieve flights: {response.status_code}"}

# Main travel planner function
def travel_planner():
    print("Welcome to the Travel Planner!")
    
    # User input via Gemini
    user_input = input("What are your travel plans? ")

    # Get a Gemini response based on natural language input
    gemini_response = get_gemini_response(user_input)
    gemini_text = gemini_response.text
    print("Gemini understood: ", gemini_text)

    # Extract travel details from Gemini's response
    travel_details = extract_travel_details(gemini_text)
    
    if travel_details:
        # Fetch flight information using RapidAPI
        flight_data = get_flight_info(
            api_key=rapidapi_key, 
            origin=travel_details["origin"], 
            destination=travel_details["destination"], 
            departure_date=travel_details["departure_date"], 
            return_date=travel_details["return_date"], 
            adults=travel_details["adults"]
        )
        
        # Display the flight data
        print("Flight Options: ", flight_data)
    else:
        print("Could not extract travel details from the response. Please try again.")

# Run the planner
travel_planner()
