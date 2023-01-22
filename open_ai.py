import os
import openai

 
openai.api_key = "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"
 
response = openai.Completion.create(
  model="text-davinci-003",
  prompt="Platon is a chatbot.\n\nDu: Write an app to calculate fizz buzz.  \nPlaton:",
  temperature=0.6,
  max_tokens=300,
  top_p=1,
  frequency_penalty=1,
  presence_penalty=1
)
print(response)

# that reluctantly answers questions with sarcastic responses