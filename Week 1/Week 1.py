from ollama import chat

response = chat(model='gemma3:1b', messages=[
  {
    'role': 'user',
    'content': 'Whats thousand minus seven?',
  },
])
# notice your exact answer could be different due to some random processes in the model (learn about that later)
print(response.message.content)