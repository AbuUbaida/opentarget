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
            time.sleep(300)  # Wait for 3 seconds before checking the status again
            print(f"Batch job status: {batch_job.status}...trying again in 5 mintues...")
            batch_job = self.client.batches.retrieve(batch_job.id)

        # Download and save the results
        if batch_job.status == "completed":
            result_file_id = batch_job.output_file_id
            result = self.client.files.retrieve(result_file_id).decode("utf-8")

            result_file_name = "batch_job_results.jsonl"
            with open(result_file_name, "wb") as file:
                file.write(result)

            # Load data from the saved file
            results = []
            with open(result_file_name, "r") as file:
                for line in file:
                    json_object = json.loads(line.strip())
                    results.append(json_object)

            return results
        else:
            print(f"Batch job failed with status: {batch_job.status}")
            return None
        
# Initialize the OpenAIBatchProcessor
api_key = os.getenv("your-api-key-here")
processor = OpenAIBatchProcessor(api_key)

# Process the batch job
input_file_path = "input_batch.jsonl"
endpoint = "/v1/chat/completions"
completion_window = "24h"

# Process the batch job
results = processor.process_batch(input_file_path, endpoint, completion_window)

# Print the results
print(results)

