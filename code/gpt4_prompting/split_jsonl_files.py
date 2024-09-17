import json

def split_jsonl_file(input_file, n):
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    total_lines = len(lines)
    num_files = (total_lines + n - 1) // n  # Calculate the number of files needed

    for i in range(num_files):
        split_file = f"split_{i + 1}.jsonl"
        with open(split_file, 'w', encoding='utf-8') as outfile:
            start = i * n
            end = start + n
            outfile.writelines(lines[start:end])
        print(f"{split_file} created with {min(n, total_lines - start)} samples.")


input_file = "/home/andalus/Research/Stance Detection/emnlp_2024_improved/code/gpt4_prompting/input_batch.jsonl"
n = 400  # Define how many samples per split file
split_jsonl_file(input_file, n)
