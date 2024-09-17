import transformers
import torch
import os
import pandas as pd
import time

def extract_target_and_stance(strings):
    targets = []
    stances = []
    for s in strings:
        if ',' in s:
            parts = s.rsplit(',', 1)
        elif "Stance:" in s:
            parts = s.split("Stance:", 1)
        # else:
        #     continue
        first_part = parts[0].strip()
        second_part = parts[1].strip()
        if "Target: " in first_part:
            target = first_part.split("Target: ", 1)[1].strip()
        else:
            target = first_part.strip()
        stance = second_part.strip()
        targets.append(target)
        stances.append(stance)
    return targets, stances

#remove "stance:" from output
def remove_stance(input_string):
    # Check if "Stance:" is in the string
    if "Stance:" in input_string:
        # Remove "Stance:" and return the processed string
        return input_string.replace("Stance:", "").strip()
    else:
        # If "Stance:" is not found, return the original string
        return input_string.strip()

def chat(system, user):
    assert isinstance(system, str), "`system` should be a string"
    assert isinstance(user, str), "`user` should be a string"

    messages = [
    {"role": "system", "content": system},
    {"role": "user", "content": user},
    ]

    prompt = pipeline.tokenizer.apply_chat_template(
        messages, 
        tokenize=False, 
        add_generation_prompt=True
    )

    outputs = pipeline(
        prompt,
        max_new_tokens=256,
        eos_token_id=terminators,
        do_sample=False,
        # temperature=0.9,
        top_p=0.9,
    )

    result = outputs[0]["generated_text"][len(prompt):]
    return result

start = time.time()

model_id = "meta-llama/Meta-Llama-3-8B-Instruct"
HF_TOKEN = "your_hf_token"
# HF_TOKEN = os.environ.get("HF_TOKEN")

pipeline = transformers.pipeline(
"text-generation",
model=model_id,
model_kwargs={"torch_dtype": torch.bfloat16},
device="cuda",
token=HF_TOKEN
)

terminators = [
        pipeline.tokenizer.eos_token_id,
        pipeline.tokenizer.convert_tokens_to_ids("<|eot_id|>")
]

#CHANGE IT
paths = ["ex_file_path",
         "im_file_path"]
prompts = ["You will be provided with a text, and your task is to generate a target for this text. A target should be the topic on which the text is talking. The target can be a single word or a phrase, but its maximum length MUST be 4 words. The output should only be the target, NO OTHER WORDS or EXPLANATION.",
        "Stance classification is the task of determining the expressed or implied opinion, or stance, of a statement toward a certain, specified target. Analyze the following text and determine its stance towards the provided target. If the stance is in favor of the target, write FAVOR, if it is against the target write AGAINST and if it is ambiguous, write NONE. Only return the stance as a single word, NO OTHER WORDS or EXPLANATION.",
        "Stance classification is the task of determining the expressed or implied opinion, or stance, of a statement toward a certain, specified target. Analyze the following text, generate the target for this text, and determine its stance towards the generated target. A target should be the topic on which the text is talking. The target can be a single word or a phrase, but its maximum length MUST be 4 words. If the stance is in favor of the generated target, write FAVOR; if it is against the target, write AGAINST; if it is ambiguous, write NONE. The answer only has to be one of these three words: FAVOR, AGAINST, or NONE. The output format should be: ```Target: <target>, Stance: <stance>```. NO OTHER WORDS or EXPLANATION."
        ]

#0: tg (tg+sd)
#1: sd (tg+sd)
#2: tg&sd

for id_path,path in enumerate(paths):
    df = pd.read_csv(path, sep=",")
    for idx,prompt in enumerate(prompts):
        responses = []
        count = 0
        if idx==0:
            for index, row in df.iterrows():
                text = row["tweet"]
                text = "Text: "+text
                response = chat(prompt, text)
                responses.append(response)
                count+=1
                print(count)
            df["llama_target_tg_plus_sd"] = responses
            print("prompt, file:", idx, id_path)
        elif idx==1:
            for index, row in df.iterrows():
                text = row["tweet"]
                target = row["llama_target_tg_plus_sd"]
                text_with_target = "Text: "+text+"\nTarget: "+target
                response = chat(prompt, text_with_target)
                responses.append(response)
                count+=1
                print(count)
            df["llama_stance_tg_plus_sd"] = responses
            print("prompt, file:", idx, id_path)
        elif idx==2:
            for index, row in df.iterrows():
                text = row["Text"]
                text = "Text: "+text
                response = chat(prompt, text)
                responses.append(response)
                count+=1
                print(count)
            df["llama_tg_n_sd"] = responses
            print("prompt, file:", idx, id_path)

    strings = df["llama_tg_n_sd"].tolist()
    targets, stances = extract_target_and_stance(strings)
    df["llama_target_tg_n_sd"] = targets
    df["llama_stance_tg_n_sd"] = stances    

    processed_stance = []
    
    for idx,row in df.iterrows():
        processed_string = remove_stance(row["llama_stance_tg_n_sd"])
        processed_stance.append(processed_string)
    df["llama_stance_tg_n_sd"] = processed_stance
    df.to_csv(f"your_file_path", index=False)

end = time.time()
print("Elapsed time: ", end-start)