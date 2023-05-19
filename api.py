import os

completions = "https://api.pawan.krd/v1/chat/completions"
api_key = os.environ['API_KEY']
headers = {
  "Authorization": f"Bearer {api_key}",
  "Content-Type": "application/json"
}
