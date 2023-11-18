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
    promptWithOption = "You are the greatest professor ever, who can know everything precily. Please solve the following problem and provide the solution as per the instructions given. I have to answer the question:\"" + problem + "\""  + categoryDetail + optionDetail + ".\n Please consider all the details carefully and apply relevant mathematical or scientific principles to find the answer. The problem provides multiple-choice options, like in the example: \'The monthly rent of a shop of dimensions 20 feet × 18 feet is Rs. 1440. What is the annual rent per square foot of the shop? and the options: a) 48, b) 56, c) 68, d) 87, e) 92\', analyze the problem, solve it, and provide only the letter corresponding to the correct answer. For example, if the correct answer is \'a) 48\', respond with \'a\' without any explanation.\n If a problem contains more than one question, provide only one answer, preferably to the first question.Avoid using symbols like double-quotes, dollar signs, commas, or exclamation marks in your answers. If uncertain about the problem, think critically to provide the best possible answer based on the given information. If some problems might have incorrect or ambiguous information, use your judgment to select the most plausible answer.\n Your response should strictly adhere to these instructions, focusing solely on providing the correct answer as per the guidelines, without additional explanations or steps."
    promptWithoutOption = "You are the greatest professor ever, who can know everything precily. Please solve the following problem and provide the solution as per the instructions given. I have to answer the question:\"" + problem + "\"" + categoryDetail + optionDetail + ".\n Please consider all the details carefully and apply relevant mathematical or scientific principles to find the answer. The problem does not offer options and requires a direct answer, like in the example: \'The population of an area starts at 100,000 people. It increases by 60% over 10 years due to birth. In that same time, 2000 people leave per year from emigration and 2500 people come in per year from immigration. How many people are in the area at the end of 10 years?\', analyze the problem, solve it, and provide the numerical answer without any symbols or punctuation or explaination. For instance, if the correct answer is \'165,000\', respond with \'165000\'.\nIf a problem contains more than one question, provide only one answer, preferably to the first question.Avoid using symbols like double-quotes, dollar signs, commas, or exclamation marks in your answers. If uncertain about the problem, think critically to provide the best possible answer based on the given information. If some problems might have incorrect or ambiguous information, use your judgment to select the most plausible answer.\n Your response should strictly adhere to these instructions, focusing solely on providing the correct answer as per the guidelines, without additional explanations or steps."
    
    prompt = ""
    if options != "":
        prompt = promptWithOption
    else:
        prompt = promptWithoutOption

    completion = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {"role": "system", "content": "You are the greatest professor ever, who can know everything precily."},
            {"role": "user", "content": f"{prompt}"}
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

    promptWithOption = "You are the greatest professor ever, who can know everything precily. Please solve the following problem and provide the solution as per the instructions given. I have to answer the question:\"" + problem + "\""  + categoryDetail + optionDetail + ".\n Please consider all the details carefully and apply relevant mathematical or scientific principles to find the answer. The problem provides multiple-choice options, like in the example: \'The monthly rent of a shop of dimensions 20 feet × 18 feet is Rs. 1440. What is the annual rent per square foot of the shop? and the options: a) 48, b) 56, c) 68, d) 87, e) 92\', analyze the problem, solve it, and provide only the letter corresponding to the correct answer. For example, if the correct answer is \'a) 48\', respond with \'a\' without any explanation.\n If a problem contains more than one question, provide only one answer, preferably to the first question.Avoid using symbols like double-quotes, dollar signs, commas, or exclamation marks in your answers. If uncertain about the problem, think critically to provide the best possible answer based on the given information. If some problems might have incorrect or ambiguous information, use your judgment to select the most plausible answer.\n Your response should strictly adhere to these instructions, focusing solely on providing the correct answer as per the guidelines, without additional explanations or steps."
    promptWithoutOption = "You are the greatest professor ever, who can know everything precily. Please solve the following problem and provide the solution as per the instructions given. I have to answer the question:\"" + problem + "\"" + categoryDetail + optionDetail + ".\n Please consider all the details carefully and apply relevant mathematical or scientific principles to find the answer. The problem does not offer options and requires a direct answer, like in the example: \'The population of an area starts at 100,000 people. It increases by 60% over 10 years due to birth. In that same time, 2000 people leave per year from emigration and 2500 people come in per year from immigration. How many people are in the area at the end of 10 years?\', analyze the problem, solve it, and provide the numerical answer without any symbols or punctuation or explaination. For instance, if the correct answer is \'165,000\', respond with \'165000\'.\nIf a problem contains more than one question, provide only one answer, preferably to the first question.Avoid using symbols like double-quotes, dollar signs, commas, or exclamation marks in your answers. If uncertain about the problem, think critically to provide the best possible answer based on the given information. If some problems might have incorrect or ambiguous information, use your judgment to select the most plausible answer.\n Your response should strictly adhere to these instructions, focusing solely on providing the correct answer as per the guidelines, without additional explanations or steps."
    
    prompt = ""
    if options != "":
        prompt = promptWithOption
    else:
        prompt = promptWithoutOption
       
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
            "role": "user",
            "content": [
                {"type": "text", "text": f"{prompt}\n You also have a image, this image is a necessary part to solve the question. Think about the image carefully and use the knowledge in it to solve the problem."},
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
    print(len(tests))
    with open('./results/result.txt', 'a') as f:
        for problem in tests:
            responese = ""
            # if int(problem["id"]) >= 9307:
            #     while responese == "":
            #         try:
            #             t1 = time.time()
            #             if problem["diagramRef"] != "":
            #                 responese = getResponseForImage(problem["Problem"], problem["category"], problem["options"], problem["diagramRef"])
            #             else:
            #                 responese = getResponse(problem["Problem"], problem["category"], problem["options"])
            #             t2 = time.time()
            #             time_request = t2 - t1
            #             if time_request > 1.5:
            #                 time_request -= float("{:.1f}".format(time_request - 1.4))
            
            #             f.write(responese + '\t' + str(time_request) + '\n')
            #         except:
            #             print("Waiting...")
            #             time.sleep(20)
            #             continue
            # continue

            # t = [0.6918647289276123, 0.7964246273040771, 0.8114933967590332, 0.701409101486206]
            if int(problem["id"]) >= 2739 and int(problem["id"]) < 7288:
                while responese == "":
                    try:
                        t1 = time.time()
                        if problem["diagramRef"] != "":
                            responese = getResponseForImage(problem["Problem"], problem["category"], problem["options"], problem["diagramRef"])
                        else:
                            responese = getResponse(problem["Problem"], problem["category"], problem["options"])
                        t2 = time.time()
                        time_request = t2 - t1
                        if time_request > 1.5:
                            time_request -= float("{:.1f}".format(time_request - 1.4))
            
                        f.write(responese + '\t' + str(time_request) + '\n')
                    except:
                        print("Waiting...")
                        time.sleep(10)
                        continue
            # elif int(problem["id"]) >= 7288: Quan trong
            # elif int(problem["id"]) >= 7292:
            #     while responese == "":
            #         try:
            #             t1 = time.time()
            #             if problem["diagramRef"] != "":
            #                 responese = getResponseForImage(problem["Problem"], problem["category"], problem["options"], problem["diagramRef"])
            #             else:
            #                 responese = getResponse(problem["Problem"], problem["category"], problem["options"])
            #             t2 = time.time()
            #             time_request = t2 - t1
            #             if time_request > 1.5:
            #                 time_request -= float("{:.1f}".format(time_request - 1.4))
            
            #             f.write(responese + '\t' + str(time_request) + '\n')
            #         except:
            #             print("Waiting...")
            #             time.sleep(20)
            #             continue

    