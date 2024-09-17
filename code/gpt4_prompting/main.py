from openai import OpenAI
import time
import json
import os

class OpenAIBatchProcessor:
    def __init__(self, api_key):
        client = OpenAI(api_key=api_key)
        self.client = client

    def process_batch(self, input_file_path, endpoint, completion_window):
        # Upload the input file
        with open(input_file_path, "rb") as file:
            uploaded_file = self.client.files.create(
                file=file,
                purpose="batch"
            )

        # Create the batch job
        batch_job = self.client.batches.create(
            input_file_id=uploaded_file.id,
            endpoint=endpoint,
            completion_window=completion_window
        )

        # Monitor the batch job status
        while batch_job.status not in ["completed", "failed", "cancelled"]:
            time.sleep(10)  # Wait for 10 seconds before checking the status again
            print(f"Batch job status: {batch_job.status}...trying again in 10 seconds...")
            batch_job = self.client.batches.retrieve(batch_job.id)

        # Download and save the results
        if batch_job.status == "completed":
            result_file_id = batch_job.output_file_id
            result = self.client.files.content(result_file_id).text

            input_file_name = os.path.splitext(os.path.basename(input_file_path))[0]
            result_file_name = f"batch_result_{input_file_name}.jsonl"

            json_lines = result.splitlines()
            with open(result_file_name, 'w', encoding='utf-8') as file:
                for line in json_lines:
                    file.write(line + '\n')

            print(f"Input: {input_file_name}, Output: {result_file_name}")

            # # Load data from the saved file
            # results = []
            # with open(result_file_name, "r") as file:
            #     for line in file:
            #         json_object = json.loads(line.strip())
            #         results.append(json_object)

            # return results
        else:
            print(f"Batch job failed with status: {batch_job.status}")
        
# Initialize the OpenAIBatchProcessor
api_key = "your-api-key"
processor = OpenAIBatchProcessor(api_key)

# Process the batch job
input_file_paths = ["list_of_file_paths"]
endpoint = "/v1/chat/completions"
completion_window = "24h"

# Process the batch job
for file_path in input_file_paths:
    processor.process_batch(file_path, endpoint, completion_window)

