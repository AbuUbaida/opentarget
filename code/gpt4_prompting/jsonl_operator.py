import random
import string
import json

class JsonlFileOperator:
    def __init__(self, model_name, messages, filename='input.jsonl', max_tokens=100):
        self.model_name = model_name
        self.messages = messages
        self.filename = filename
        self.max_tokens = max_tokens
        self.message_list = self.create_message_list()
    
    @staticmethod
    def generate_random_custom_id(prefix='request', length=6):
        random_id = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        return f"{prefix}-{random_id}"
    
    def create_message_list(self):
        message_list = []
        for i in range(len(self.messages)):
            message_list.append({
                "custom_id": self.generate_random_custom_id(),
                "method": "POST",
                "url": "/v1/chat/completions",
                "body": {
                    "model": self.model_name,
                    "temperature": 0,
                    "messages": self.messages[i],
                    "max_tokens": self.max_tokens
                }
            })
        return message_list
    
    def write_jsonl_file(self):
        with open(self.filename, 'w') as f:
            for item in self.message_list:
                f.write(json.dumps(item) + '\n')

    @staticmethod
    def jsonl_to_dict(self, jsonl_string):
        dict_list = []
        for line in jsonl_string.strip().split('\n'):
            if line.strip():    #check if the line is not empty
                dict_list.append(json.loads(line))
        return dict_list