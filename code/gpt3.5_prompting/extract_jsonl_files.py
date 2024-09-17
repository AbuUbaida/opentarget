import json
import csv

# Given a list of jsonl files, the function will return only the contents in a csv
def extract_content_to_csv(files, output_csv):
    content_list = []

    # Iterate through each file in the order they are provided
    for file in files:
        with open(file, 'r') as f:
            # Read each line of the JSONL file
            for line in f:
                data = json.loads(line)
                
                # Extract "content" from the dictionary
                content = data.get("response", {}).get("body", {}).get("choices", [])[0].get("message", {}).get("content")
                
                if content:
                    content_list.append(content)

    # Write the contents to a CSV file
    with open(output_csv, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        
        # Write header
        csvwriter.writerow(['Content'])
        
        # Write each content to the CSV
        for content in content_list:
            csvwriter.writerow([content])

if __name__ == "__main__":
    files = ["file_to_be_extracted_path"]
    output_csv = "generated_targets.csv"  # Replace with your desired output file name

    extract_content_to_csv(files, output_csv)

    print(f"Contents merged and written to {output_csv}")