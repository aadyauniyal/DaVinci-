import json
import os
import google.generativeai as genai

# Use the API key from the environment variable
api_key = os.environ.get("AI_API_KEY")
genai.configure(api_key=api_key)

def load_travel_data(filename):
    """Load travel data from a JSON file"""
    with open(filename, 'r') as file:
        data = json.load(file)
    return data

def generate_travel_plan(schedule, flights, hotels):
    """Generate a travel plan based on the weekly schedule, flights, and hotels"""
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    chat_session = model.start_chat(history=[])

    # Create a prompt based on the schedule and travel options
    message = f"""
    I need help planning my travel based on this weekly schedule:
    {schedule}.
    
    Here are the available flights:
    {flights}.
    
    And here are the hotel options:
    {hotels}.
    
    Please suggest the best flight and hotel combination based on my schedule.
    My budget is under $180 per night, and I want to make sure to arrive in time for important meetings and commitments.
    """
    
    response = chat_session.send_message(message)
    return response.text

def main():
    # Load travel data from the JSON file
    travel_data = load_travel_data('travel_data.json')

    # Extract flights, hotels, and schedule
    flights = travel_data["flights"]
    hotels = travel_data["hotels"]
    schedule = travel_data["weekly_schedule"]

    # Generate a travel plan using the schedule, flights, and hotels
    travel_plan = generate_travel_plan(schedule, flights, hotels)

    # Output the generated travel plan
    print(f"\n--- Travel Plan ---\n")
    print(travel_plan)

if __name__ == "__main__":
    main()
