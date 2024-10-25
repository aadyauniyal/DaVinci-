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

def generate_travel_plan(schedule, flights, hotels, departure, destination, travel_dates, interests,budget,attractions):
    """Generate a travel plan based on the weekly schedule, flights, hotels, and user input"""
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    chat_session = model.start_chat(history=[])

    # Create a prompt based on the user input and travel options
    message = f"""
    I need help planning my travel from {departure} to {destination} on the following dates: {travel_dates}.
    My weekly schedule, which I have to stick to, is:
    {schedule}.
    My interests include: {interests}.
    Can you book my flights in such a way that they don't interfere with my schedule and return the adequate link so I can book it?
    Here are the available flights:
    {flights}.
    
    And here are the hotel options:
    {hotels}.

    there are the attractions in the cities: {attractions}
    
    Please suggest the best flight and hotel combination based on my schedule and interests.
    My budget is {budget}, and I want to make sure to arrive in time for important meetings and commitments. Can you give me the itenary in 
    the following fomat: Day 1 >12:00PM:..... Day 2... Make it very elaborate per day so its easy to plan for the user. book slot for user to go to attraction in the city.
    end the itenary once the person is on the flight back to the original city. Dont use "afternoon, moring, evening", use time slots for everything. Specify which bus need to be taken to get around the city.
    Can you also add the link for flight and hotel booking from the flight and hotel options. The flights run on a periodic basis. DOnt repeat the given input again in the response.
    """
    
    response = chat_session.send_message(message)
    return response.text

def main():
    # Load travel data from the JSON file
    travel_data = load_travel_data('C:/Users/aadya/OneDrive/Desktop/davinci/travel_db.json')

    # Extract flights, hotels, and schedule
    flights = travel_data["flights"]
    hotels = travel_data["hotels"]
    schedule = travel_data["weekly_schedule"]
    attractions = travel_data["attractions"]

    # Get user input for travel details
    departure = input("Enter your departure location: ")
    destination = input("Enter your destination location: ")
    travel_dates = input("Enter your travel dates (e.g., 'October 1-10, 2024'): ")
    interests = input("Enter your interests (eg: 'sightseeing, food, culture'): ")
    budget=input("Enter your budget for the entire trip (In USD) :$")

    # Generate a travel plan using the schedule, flights, hotels, and user input
    travel_plan = generate_travel_plan(schedule, flights, hotels, departure, destination, travel_dates, interests,budget,attractions)

    # Output the generated travel plan
    print(f"\n--- Travel Plan ---\n")
    print(travel_plan)

if __name__ == "__main__":
    main()
