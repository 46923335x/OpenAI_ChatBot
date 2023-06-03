# -*- coding: utf-8 -*-
"""
Created on Fri Jun  2 22:48:05 2023

@author: gleach
"""


import openai
openai.api_key = "key_goes_here"

# Define the model to use
model = "text-davinci-003"
    
# Define the prompt for the model
init = input("Enter an initial question or prompt to begin: ")
prompt = ("The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly. Human: Hello, who are you? AI: I am an AI created by OpenAI. How can I help you today? Human: " + init + ". AI: ")

# Define the parameters for the API call
response = openai.Completion.create(
    model=model,
    prompt=prompt,
    temperature=0.5,
    max_tokens=2048
)

# Print the response from the model
print(response.choices[0].text.strip())

# Define a list to store inputs and responses
conversation = []

# Add the initial input and response to the conversation
conversation.append({'input': prompt, 'response': response.choices[0].text.strip()})

# define variable to keep track of current position in the conversation
current_position = 0

while True:
    # Get user input
    user_input = input("User: ")

    # check if user input is 'back'
    if user_input.lower() == 'back':
        if current_position > 0:
            current_position -= 1
            del conversation[current_position + 1:]
            print("Previous response: " + conversation[current_position]['response'])
        else:
            print("Cannot go back. This is the first response.")
    elif user_input.lower() == 'exit':
        print("Exiting the chatbot...")
        break
    else:
        current_position += 1
        conversation.append({'input': user_input})

    # Build the prompt for the next API call
    prompt = "\n".join([c['input'] + " " + c.get('response','') for c in conversation])

    # !!! Note:
    # This implementation of the chatbot will break when the conversation 
    # exceeds 2048 tokens. Without tokenization, there is no obvious way to
    # ensure that prompts won't exceed the value of max_tokens in the 
    # openai.Completion.create call.

    # Define the parameters for the API call
    response = openai.Completion.create(
        model=model,
        prompt=prompt,
        temperature=0.5,
        max_tokens=2048
    )
    
    # Print the response from the model
    print(response.choices[0].text.strip())

    # Append the response to the conversation
    conversation[-1]['response'] = response.choices[0].text.strip()
