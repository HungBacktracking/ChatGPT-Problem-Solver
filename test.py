import base64
import requests

# OpenAI API Key
api_key = "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"

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

# Path to your image
image_path = "data/diagrams/diagram0.png"

# Getting the base64 string
base64_image = encode_image(image_path)

headers = {
  "Content-Type": "application/json",
  "Authorization": f"Bearer {api_key}"
}

payload = {
  "model": "gpt-4-vision-preview",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "I have to answer the question:\"The figure above shows three spinners A, B and C with numbers on it. If each of every number has an equal probability of being the sector on which the arrow stops, what is the probability that the sum of these three numbers is an even number?\" This image is a necessary part to solve the question. Please find the answer! Note that you only need to return the answer without explain."
        },
        {
          "type": "image_url",
          "image_url": {
            "url": f"data:image/jpeg;base64,{base64_image}"
          }
        }
      ]
    }
  ],
  "max_tokens": 300
}

response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

print(response.json()['choices'][0]['message']['content'])