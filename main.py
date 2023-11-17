import base64
import json
import requests
import time 
from openai import OpenAI
import random

def read_jsonl(path: str):
    with open(path) as f:
        data = json.load(f)
        return data

# OpenAI API Key
with open("openai_api_key.txt", "r") as f:
    api_key = f.readline()

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')
  
def getResponse(problem, category, options):
    categoryDetail = ""
    if category != "":
       categoryDetail = f"The category of this problem is {category}."

    optionDetail = ""
    if options != "":
        optionDetail = f"And the options is {options}."

    client = OpenAI(api_key = api_key)

    completion = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {"role": "system", "content": "You are a excellent professor, who can answer exactly anything."},
            {"role": "user", "content": f"I have to answer the question:\"{problem}\" {categoryDetail} {optionDetail} Let\'s find the answer! Note that you only need to return the answer without explain.\n For example, if you have a question \"a large box contains 18 small boxes and each small box contains 25 chocolate bars . how many chocolate bars are in the large box ?\" If there is no options, you have to write the answer directly: \"450\". But if it has the options is \"a ) 350 , b ) 250 , c ) 450 , d ) 550 , e ) 650\" Then just write the answer: \"c\", do not write \"c ) 450\" or \"450\". Remember just write \"c\". If the question is asked about the percentage or something include \"%\" or \"!\" or \"$\" and the answer is \"50%\", you don\'t need to write \"50%\", just write \"50\". And do not include the double-quotes \" in answer. \n Remember just write the \"a\" or \"b\" or \"c\" or \"d\" if the question has options.\n If you are confused about the question, just write one answer, do not explain anything. Do not write the ways like \"The answer is: b\". Just write \"b\"."}
        ],
        max_tokens = 20,
        temperature = 0.2
    )
    print(completion.choices[0].message.content)
    return str(completion.choices[0].message.content)

def getResponseForImage(problem, category, options, image_path):
    image_path = "./data/diagrams/" + image_path
    base64_image = encode_image(image_path)

    categoryDetail = ""
    if category != "":
       categoryDetail = f"The category of this problem is {category}."
    
    optionDetail = ""
    if options != "":
        optionDetail = f"And the options is {options}."

    client = OpenAI(api_key = api_key)
       
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
            "role": "user",
            "content": [
                {"type": "text", "text": f"You are a excellent professor, who can answer exactly anything.\nI have to answer the question:\"{problem}\" {categoryDetail} {optionDetail} You also have a image, this image is a necessary part to solve the question. Please find the answer! Note that you only need to return the answer without explain.\n For example, if you have a question \"a large box contains 18 small boxes and each small box contains 25 chocolate bars . how many chocolate bars are in the large box ?\" If there is no options, you have to write the answer directly: \"450\". But if it has the options is \"a ) 350 , b ) 250 , c ) 450 , d ) 550 , e ) 650\" Then just write the answer: \"c\", do not write \"c ) 450\" or \"450\". Remember just write \"c\". If the question is asked about the percentage or something include \"%\" or \"!\" or \"$\" and the answer is \"50%\", you don\'t need to write \"50%\", just write \"50\". And do not include the double-quotes \" in answer.\n Remember just write the \"a\" or \"b\" or \"c\" or \"d\" if the question has options.\n If you are confused about the question, just write one answer, do not explain anything. Do not write the ways like \"The answer is: b\". Just write \"b\"."},
                {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}",
                },
                },
            ],
            }
        ],
        max_tokens = 20,
        temperature = 0.2
    )
    print(response.choices[0].message.content, "image")
    return str(response.choices[0].message.content)


if __name__ == "__main__":
    tests = read_jsonl("./data/all_test_round1.json")
    with open('./results/result.txt', 'a') as f:
        for problem in tests:
            responese = ""
            while responese == "":
                try:
                    t1 = time.time()
                    if problem["diagramRef"] != "":
                        responese = getResponseForImage(problem["Problem"], problem["category"], problem["options"], problem["diagramRef"])
                    else:
                        responese = getResponse(problem["Problem"], problem["category"], problem["options"])
                    t2 = time.time()
                    time_request = t2 - t1
        
                    f.write(responese + '\t' + str(time_request) + '\n')
                except:
                    print("Waiting...")
                    time.sleep(20)
                    continue

    