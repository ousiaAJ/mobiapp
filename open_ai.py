import os
import openai

 
openai.api_key = "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"
 
response = openai.Completion.create(
  model="text-davinci-003",
  prompt="Platon is a chatbot that reluctantly answers questions with sarcastic responses.\n\nDu: Warum ist Gras grün? \nPlaton:",
  temperature=0.6,
  max_tokens=150,
  top_p=1,
  frequency_penalty=1,
  presence_penalty=1
)
print(response)