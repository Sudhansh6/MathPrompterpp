import sys 
sys.path.append('..')
sys.path.append('../..')
sys.path.append('FinalCode')

import re
from collections import defaultdict
def zeroshotCoT(question, SERVICE, max_tokens):
    error, error_message = False, ""
    result = defaultdict(lambda: None)
    result["Error"] = error
    result["Error_Message"] = error_message
    try:
        prompt = f"Q: {question}\nA: \nLet's think step by step."
        messages = SERVICE.create_prompt(question=prompt)
        response0 = SERVICE.make_request(messages=messages, max_tokens=max_tokens)

        # Get answer from response
        prompt = f"{prompt}\n{response0.strip()}\nTherefore, the answer (arabic numerals) is:"
        messages = SERVICE.create_prompt(question=prompt)
        response = SERVICE.make_request(messages=messages, max_tokens=max_tokens)
        cleaned_response = response.replace(",", "")
        # Assuming cleaned_response is defined
        match = re.search(r'answer is.*?(-?\d+\.?\d*)', cleaned_response, re.IGNORECASE)
        if match:
            answer = float(match.group(1))  # Get the first captured group as a float
        else:
            answer = None
            numbers = [s for s in re.findall(r'-?\d+\.?\d*', cleaned_response)]
            # Convert to float if there's only one number
            if len(numbers) >= 1:
                answer = float(numbers[0])
        result["Response"] = response0 + response
        result["Answer"] = answer
    except Exception as e:
        result["Error"] = True
        result["Error_Message"] = str(e)
        print(f"An error occurred during the verification process: {e}")

    return result

if __name__ == "__main__":
    from llm_inference.llm_factory import get_llm_service
    question = " Danny collects bottle caps and wrappers. He found 66 wrappers and 39 bottle caps at the park. Now he has 16 bottle caps and 68 wrappers in his collection. How many wrappers did danny have at first?"
    
    # SERVICE = get_llm_service("llama", "mlx-community/Llama-3.2-1B-Instruct-4bit", 0.0, 200)
    SERVICE = get_llm_service("openai", "gpt-4o-mini", 0.0, 200)
    print(zeroshotCoT(question, SERVICE, max_tokens=100))