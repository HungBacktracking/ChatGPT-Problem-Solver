from openai import OpenAI

# Key
api_key = "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"
client = OpenAI(api_key=api_key)


# Upload a file with an "assistants" purpose
# file = client.files.create(
#   file=open("knowledges.json", "rb"),
#   purpose='assistants'
# )

# Upload a file with an "assistants" purpose
file_names = ["knowledges_small_1.json", "knowledges_small_2.json", "knowledges_small_3.json", "knowledges_small_4.json",
              "knowledges_small_5.json", "knowledges_small_6.json", "knowledges_small_7.json", "knowledges_small_8.json",
              "knowledges_small_9.json", "knowledges_small_10.json"]

# Loop through each file name and upload it
file_ids = []
for file_name in file_names:
    with open(file_name, "rb") as file:
        file_object = client.files.create(
            file=file,
            purpose='assistants'
        )
        file_ids.append(file_object.id)
        print(f"Uploaded {file_name}")

# Add the file to the assistant
assistant = client.beta.assistants.create(
  instructions="You are a excellent professor, who can answer exactly anything.\nI have to answer the question:\"{problem}\" {categoryDetail} {optionDetail} You also have a image, this image is a necessary part to solve the question. Please find the answer! Note that you only need to return the answer without explain.\n For example, if you have a question \"a large box contains 18 small boxes and each small box contains 25 chocolate bars . how many chocolate bars are in the large box ?\" If there is no options, you have to write the answer directly: \"450\". But if it has the options is \"a ) 350 , b ) 250 , c ) 450 , d ) 550 , e ) 650\" Then just write the answer: \"c\", do not write \"c ) 450\" or \"450\". Remember just write \"c\". If the question is asked about the percentage or something include \"%\" or \"!\" or \"$\" and the answer is \"50%\", you don\'t need to write \"50%\", just write \"50\". And do not include the double-quotes \" in answer.\n Remember just write the \"a\" or \"b\" or \"c\" or \"d\" if the question has options.\n If you are confused about the question, just write one answer, do not explain anything. Do not write the ways like \"The answer is: b\". Just write \"b\".",
  model="gpt-4-1106-preview",
  tools=[{"type": "retrieval"}],
  file_ids=file_ids
)

# Create thread
thread = client.beta.threads.create()

# Ask for user input
user_question = input("Please enter your question: ")

# Add message to thread with the user input
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content=user_question
)

# Run the assistant
run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id,
    instructions="You are a excellent professor, who can answer exactly anything.\nI have to answer the question:\"{problem}\" {categoryDetail} {optionDetail} You also have a image, this image is a necessary part to solve the question. Please find the answer! Note that you only need to return the answer without explain.\n For example, if you have a question \"a large box contains 18 small boxes and each small box contains 25 chocolate bars . how many chocolate bars are in the large box ?\" If there is no options, you have to write the answer directly: \"450\". But if it has the options is \"a ) 350 , b ) 250 , c ) 450 , d ) 550 , e ) 650\" Then just write the answer: \"c\", do not write \"c ) 450\" or \"450\". Remember just write \"c\". If the question is asked about the percentage or something include \"%\" or \"!\" or \"$\" and the answer is \"50%\", you don\'t need to write \"50%\", just write \"50\". And do not include the double-quotes \" in answer.\n Remember just write the \"a\" or \"b\" or \"c\" or \"d\" if the question has options.\n If you are confused about the question, just write one answer, do not explain anything. Do not write the ways like \"The answer is: b\". Just write \"b\"."
)

# Wait for the assistant response and retrieve it
run = client.beta.threads.runs.retrieve(
    thread_id=thread.id,
    run_id=run.id
)

# Fetching all messages in the thread
messages = client.beta.threads.messages.list(
    thread_id=thread.id
)

# Printing the assistant's response
for msg in messages.data:
    if msg.role == "assistant":
        print(msg.content)