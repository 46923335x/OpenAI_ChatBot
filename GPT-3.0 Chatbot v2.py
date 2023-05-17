# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 01:40:54 2023

@author: gleach

NOTE:
THIS MODEL IS RELATIVELY COSTLY TO RUN.
IT COSTS APPROX. 4 CENTS PER INTERACTION.
"""

import openai
openai.api_key = "key_goes_here"

# Define your API key
api_key = "key_goes_here"

# Define the model to use
model = "text-davinci-003"

# Initialize the tokenizer
from transformers import GPT2TokenizerFast
tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")

def trim_prompt(prompt,n=2048):
    # Tokenize the prompt
    tokens = tokenizer.tokenize(prompt)
    
    # Keep only the last 5 tokens
    n = n
    trimmed_tokens = tokens[-n:]
    
    # Convert the tokens to token ids
    trimmed_tokens_ids = tokenizer.convert_tokens_to_ids(trimmed_tokens)
    
    # Convert the token ids back to a string
    trimmed_prompt = tokenizer.decode(trimmed_tokens_ids, skip_special_tokens=True)
    
    return(trimmed_prompt)
    
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
print(response.choices[0].text)

# Define a list to store inputs and responses
conversation = []

# Add the initial input and response to the conversation
conversation.append({'input': prompt, 'response': response.choices[0].text})

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

    # Trim memory to the last 2048 tokens
    prompt = trim_prompt(prompt, 2048)

    # Define the parameters for the API call
    response = openai.Completion.create(
        model=model,
        prompt=prompt,
        temperature=0.5,
        max_tokens=2048
    )
    
    # Print the response from the model
    print(response.choices[0].text)

    # Append the response to the conversation
    conversation[-1]['response'] = response.choices[0].text
