import traceback, os
import litellm # library for abstracting LLM API Calls https://github.com/BerriAI/litellm
from litellm import embedding, completion

# set model keys in .env 

litellm.set_verbose = True # useful for debugging, comment out if not needed.

model_fallback_list = ["claude-instant-1", "gpt-3.5-turbo", "gpt-3.5-turbo-16k"]


def model_fallback(input):
    response = None
    messages=[{"role": "user", "content": input}]
    for model in model_fallback_list:
        try:
            response = completion(model=model, messages=messages)
            if response != None:
                return response
        except Exception as e:
            print(f"error occurred: {traceback.format_exc()}") 
            pass
            
    return response 