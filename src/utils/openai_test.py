# Install with: pip install openai
from openai import OpenAI

def main():
    # The client will read OPENAI_API_KEY from your environment
    client = OpenAI()

    # Replace this with whatever you want to ask
    user_query = "Tell me a three-sentence bedtime story about a unicorn."

    # Use the chat completion endpoint
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",  # or another model from your `openai models list`
        messages=[{"role": "user", "content": user_query}],
        max_tokens=150,  # adjust as needed
    )

    # Extract and print the assistant’s reply
    print(response.choices[0].message.content)

if __name__ == "__main__":
    main()


# curl https://api.openai.com/v1/fine_tuning/model_limits  -H "Authorization: Bearer $OPENAI_API_KEY"