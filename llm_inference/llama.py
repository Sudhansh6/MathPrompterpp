from .llm_interface import LLMInterface
from transformers import pipeline, AutoTokenizer
from mlx_lm import load, generate  # Add this import
from mlx_lm.sample_utils import make_sampler

class Llama(LLMInterface):
    def __init__(self, model_name="mlx-community/Llama-3.2-1B-Instruct-4bit", temperature=0.7, max_tokens=200):
        # Set up the model and tokenizer using the Transformers library
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens
        
        # Initialize the tokenizer
        self.model, self.tokenizer = load("mlx-community/Llama-3.2-1B-Instruct-4bit")
        self.sampler = make_sampler(self.temperature)

    def create_prompt(self, system_prompt = None, few_shot_examples = None, question = None):
        # Prepare the prompt similar to OpenAIService
        messages = []
        if system_prompt is not None:
            messages.append({"role": "system", "content": system_prompt})
        if few_shot_examples is not None:
            for example in few_shot_examples:
                messages.append({"role": "user", "content": example['question']})
                messages.append({"role": "assistant", "content": example['answer']})
        if question is not None:
            messages.append({"role": "user", "content": question})
        return messages  # Return the structured messages

    def make_request(self, messages, max_tokens=None):
        # Construct the formatted input using the tokenizer
        if hasattr(self.tokenizer, "apply_chat_template") and self.tokenizer.chat_template is not None:
            prompt = self.tokenizer.apply_chat_template(
                messages, tokenize=False, add_generation_prompt=True
            )
        else:
            prompt = messages
        # Use the mlx_lm generate function to produce a response
        response = generate(self.model, 
                            self.tokenizer, 
                            prompt=prompt, 
                            verbose=False,
                            sampler=self.sampler,
                            max_tokens=max_tokens if max_tokens is not None else self.max_tokens)  # Update this line
        
        # Return the generated text from the response
        return response  # Adjusted to return the response directly