import base64
import requests
from openai import OpenAI

# OpenAI API Key
with open("openai_api_key.txt", "r") as f:
    api_key = f.readline()

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

def describeImage(problem, category, options, base64_image):
    categoryDetail = ""
    if category != "":
       categoryDetail = f"The category of this problem is {category}."

    client = OpenAI(api_key = api_key)
       
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
            "role": "user",
            "content": [
                {"type": "text", "text": f"I have to answer the question:\"{problem}\" {categoryDetail} This image is a necessary part to solve the question. Please find the answer! Note that you only need to return the answer without explain."},
                {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}",
                },
                },
            ],
            }
        ],
        max_tokens=300,
    )

    print(response.choices[0].message.content)
    return response.choices[0].message.content

if __name__ == "__main__":
    # Path to your image
    image_path = "data/diagrams/diagram0.png"

    # Getting the base64 string
    base64_image = encode_image(image_path)

    problem = "The figure above shows three spinners A, B and C with numbers on it. If each of every number has an equal probability of being the sector on which the arrow stops, what is the probability that the sum of these three numbers is an even number?"
    category = ""
    options = ""
    describeImage(problem, category, options, base64_image)