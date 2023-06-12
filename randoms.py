import deepai

response = ""

for chunk in deepai.Completion.create("What model GPT are you"):
    print(chunk, end="", flush=True)
    response += chunk

print(response)
