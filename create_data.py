import json

# Read the JSON file
with open('train/train_data.json', 'r') as file:
    data = json.load(file)

# Function to format a single entry
def format_entry(entry):
    messages = []
    # Add user message (the problem)
    if entry['options'] != "":
        messages.append({"role": "user", "content": f"The question is: {entry['Problem']}. And the option are {entry['options']}"})
    else:
        messages.append({"role": "user", "content": f"The question is: {entry['Problem']}."})  
    # Add assistant message (options and rationale)
    assistant_response = entry['correct']
    messages.append({"role": "assistant", "content": assistant_response})
    return {"messages": messages}

# Format all entries
formatted_data = [format_entry(entry) for entry in data]

# Write formatted data to a new file
with open('formatted_chatgpt_data.json', 'w') as file:
    for item in formatted_data:
        json.dump(item, file)
        file.write('\n')