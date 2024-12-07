import json
import sys 
import dotenv
dotenv.load_dotenv()
from tqdm import tqdm
sys.path.append('..')
from llm_inference.openai_service import OpenAIService

# Load the JSON data
with open('domain.json', 'r') as file:
    data = json.load(file)

# Initialize the OpenAIService
openai_service = OpenAIService(model_name="gpt-3.5-turbo", temperature=0.7, max_tokens=150)

# Function to verify questions and answers
def verify_questions_answers(data):
    results = []
    for item in tqdm(data):
        question = item['Body'] + "\n" + item['Question']
        answer = item['Answer']
        
        # Create a prompt for verification
        prompt = f"Question: {question}\nAnswer: {answer}\nIs this answer correct? Please respond with 'Yes' or 'No' and provide a brief explanation."
        
        # Create messages for the OpenAI API
        messages = openai_service.create_prompt(system_prompt="You are a knowledgeable assistant.", question=prompt)
        
        # Make the request to OpenAI
        response = openai_service.make_request(messages)
        
        # Store the result
        results.append({
            "ID": item['ID'],
            "Question": question,
            "Answer": answer,
            "Verification": response
        })
        print(results[-1])
    return results

# Verify the questions and answers
verification_results = verify_questions_answers(data)

# # Print the verification results
# for result in verification_results:
#     print(f"ID: {result['ID']}\nQuestion: {result['Question']}\nAnswer: {result['Answer']}\nVerification: {result['Verification']}\n")
