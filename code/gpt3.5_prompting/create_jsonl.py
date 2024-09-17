import pandas as pd
from jsonl_operator import JsonlFileOperator

#tg
prompt = "You will be provided with a text, and your task is to generate a target for this text. A target should be the topic on which the text is talking. The target can be a single word or a phrase, but its maximum length MUST be 5 words. The output should only be the target, no other words."

#sd
# prompt = "Stance classification is the task of determining the expressed or implied opinion, or stance, of a statement toward a certain, specified target. Analyze the following text and determine its stance towards the provided target. If the stance is in favor of the target, write FAVOR, if it is against the target write AGAINST and if it is ambiguous, write NONE. Only return the stance as a single word, and no other text."

# tgnsd
# prompt = "Stance classification is the task of determining the expressed or implied opinion, or stance, of a statement toward a certain, specified target. Analyze the following text, generate the target for this text, and determine its stance towards the generated target. A target should be the topic on which the text is talking. The target can be a single word or a phrase, but its maximum length MUST be 5 words.  If the stance is in favor of the target, write FAVOR, if it is against the target write AGAINST and if it is ambiguous, write NONE. If the stance is in favor of the generated target, write FAVOR, if it is against the target write AGAINST and if it is ambiguous, write NONE. The answer only has to be one of these three words: FAVOR, AGAINST, or NONE. The output format should be: ```Target: <target>, Stance: <stance>```."

def create_messages_from_csv(file_path):
    df = pd.read_csv(file_path, sep=',')

    messages = []

    for index, row in df.iterrows():
        text = row['post']
        # target = row["gpt3.5_target_tg_plus_sd"]
        text_only = "Text: "+text
        # text_with_target = "Text: "+text+"\nTarget: "+target
        message = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": text_only}
        ]
        messages.append(message)

    return messages

if __name__ == "__main__":
    file_path = "csv_file_path"
    model_name = 'gpt-3.5-turbo'
    messages = create_messages_from_csv(file_path)

    jsonl_creator = JsonlFileOperator(model_name, messages, filename="input_batch.jsonl")
    jsonl_creator.write_jsonl_file()