import os
import google.generativeai as genai

# Use the API key from the environment variable
api_key = os.environ["AI_API_KEY"]

genai.configure(api_key=api_key)

def get_travel_details():
    # Collect user input for the trip
    destination = input("Enter your travel destination: ")
    start_date = input("Enter your departure date (YYYY-MM-DD): ")
    end_date = input("Enter your return date (YYYY-MM-DD): ")
    budget = input("Enter your budget (in USD): ")

    return destination, start_date, end_date, budget

def generate_travel_plan(destination, start_date, end_date, budget):
    # Start a chat session with the generative AI model
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    chat_session = model.start_chat(history=[])

    # Define the message with the user's input
    message = f"I want to plan a trip to {destination} from {start_date} to {end_date}. My budget is {budget} USD. Can you recommend flights, hotels, and transportation?"

    # Send message to model
    response = chat_session.send_message(message)

    # Return the response (travel plan)
    return response.text

def main():
    # Step 1: Collect trip details
    destination, start_date, end_date, budget = get_travel_details()

    # Step 2: Generate a travel plan based on the details
    travel_plan = generate_travel_plan(destination, start_date, end_date, budget)

    # Step 3: Output the plan
    print("\n--- Your Travel Plan ---\n")
    print(travel_plan)

if __name__ == "__main__":
    main()
