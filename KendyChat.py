import openai

# Load the API key securely
try:
    with open("D:\\KendyChatBot\\config\\apikey.txt", "r") as file:
        openai.api_key = file.read().strip()
except FileNotFoundError:
    print("Error: API key file not found. Make sure 'apikey.txt' exists in the config folder.")
    exit()

while True:
    user_input = input("You: ")

    if user_input.lower() in ["exit", "quit"]:
        print("Goodbye!")
        break

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Specify the model
        messages=[{"role": "user", "content": user_input}]
)
reply = response['choices'][0]['message']['content'] if "message" in response['choices'][0] else response['choices'][0]['text']
print("Chatbot:", reply)
