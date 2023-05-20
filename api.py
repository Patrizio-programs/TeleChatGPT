import os

completions = "https://free.churchless.tech/v1/chat/completions"
api_key = os.environ['API_KEY']
headers = {
  "Authorization": f"Bearer {api_key}",
  "Content-Type": "application/json"
}
