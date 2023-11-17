import json

def split_json(input_file, output_prefix, num_files):
    with open(input_file, 'r') as f:
        data = json.load(f)

    total_records = len(data)
    records_per_file = total_records // num_files

    for i in range(num_files):
        start_index = i * records_per_file
        end_index = start_index + records_per_file if i < num_files - 1 else total_records

        output_file = f"{output_prefix}_{i + 1}.json"
        with open(output_file, 'w') as f:
            json.dump(data[start_index:end_index], f, indent=2)

if __name__ == "__main__":
    input_file = "knowledges.json"
    output_prefix = "knowledges_small"
    num_files = 10

    split_json(input_file, output_prefix, num_files)