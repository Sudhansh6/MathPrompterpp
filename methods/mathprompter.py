import sys 
sys.path.append('..')
sys.path.append('../..')
sys.path.append('FinalCode')
import importlib 
import utils.compute_utils as compute_utils
importlib.reload(compute_utils)
from utils.compute_utils import perform_computational_verification, evaluate_expression, execute_python_code
from collections import defaultdict

# DISCLAIMER: The following examples inside the prompts are partly generated with Claude Opus 3
# NOTE: You may adapt the prompt based on the model you use
ALGEBRAIC_FEW_SHOT_PROMPT = [
    {
        "question": "John has A apples. He gives B apples to his friend. How many apples does John have left?",
        "answer": "A - B"
    },
    {
        "question": "A school has B classrooms. If each classroom has C students and D teachers, how many people are in the school?",
        "answer": "(C + D) * B"
    },
    {
        "question": "A factory produces E widgets per hour. If the factory operates for F hours per day and G days per week, how many widgets does the factory produce in H weeks?",
        "answer": "E * F * G * H"
    },
    {
        "question": "A company has I employees. Each employee works J hours per week. If the average hourly wage is K dollars and the company spends L percent of its revenue on salaries, what is the company's weekly revenue?",
        "answer": "(I * J * K) / (L / 100)"
    },
    {
        "question": "A store has D shirts in stock. If they sell E shirts per day, how many days will it take to sell all the shirts?",
        "answer": "D // E"
    }
]


ALGEBRAIC_SYSTEM_PROMPT ='''
You are a highly qualified expert in finding algebra expressions for a given math problem in natural language. 
You are given a math word problem and you need to find the algebraic expression that represents the problem.
Only the algebraic expression is required, without explanations. The expression must be in the form of a valid Python expression.
'''

def algebraic_expression_generation(question: str, SERVICE, few_shot):
    question = question.strip()
    if few_shot:
        messages = SERVICE.create_prompt(system_prompt=ALGEBRAIC_SYSTEM_PROMPT, few_shot_examples=ALGEBRAIC_FEW_SHOT_PROMPT, question=question)
    else:
        messages = SERVICE.create_prompt(system_prompt=ALGEBRAIC_SYSTEM_PROMPT, few_shot_examples=None, question=question)
    response = SERVICE.make_request(messages=messages)
    expression = response.strip()
    return expression


# DISCLAIMER: The following examples inside the prompts are partly generated with Claude Opus 3
# NOTE: You may adapt the prompt based on the model you use
PYTHON_FEW_SHOT_PROMPT = [
    {
        "question": "John has A apples. He gives B apples to his friend. How many apples does John have left?",
        "answer": "def solution(A, B):\n    return A - B"
    },
    {
        "question": "A school has B classrooms. If each classroom has C students and D teachers, how many people are in the school?",
        "answer": "def solution(B, C, D):\n    return (C + D) * B"
    },
    {
        "question": "A factory produces E widgets per hour. If the factory operates for F hours per day and G days per week, how many widgets does the factory produce in H weeks?",
        "answer": "def solution(E, F, G, H):\n    return E * F * G * H"
    },
    {
        "question": "A company has I employees. Each employee works J hours per week. If the average hourly wage is K dollars and the company spends L percent of its revenue on salaries, what is the company's weekly revenue?",
        "answer": "def solution(I, J, K, L):\n    return (I * J * K) / (L / 100)"
    },
    {
        "question": "A store has D shirts in stock. If they sell E shirts per day, how many days will it take to sell all the shirts?",
        "answer": "def solution(D, E):\n    return D // E"
    }
]

PYTHON_SYSTEM_PROMPT = '''
You are a highly qualified expert in finding Python code for a given math problem in natural language.
You are given a math word problem and you need to find the Python code that solves the problem.
Only the Python code is required, without explanations. The code must be a single function called solution.
'''

def python_code_generation(question, SERVICE, few_shot):
    if few_shot:
        messages = SERVICE.create_prompt(system_prompt=PYTHON_SYSTEM_PROMPT, few_shot_examples=PYTHON_FEW_SHOT_PROMPT, question=question)
    else:
        messages = SERVICE.create_prompt(system_prompt=PYTHON_SYSTEM_PROMPT, few_shot_examples=None, question=question)
    response = SERVICE.make_request(messages=messages)
    function_code = response.strip()
    if function_code.startswith("```python"):
        function_code = function_code[9:]
    if function_code.endswith("```"):
        function_code = function_code[:-3]
    return function_code.strip()


def generate_math_prompts(qt, SERVICE, few_shot):
    exp = algebraic_expression_generation(qt, SERVICE=SERVICE, few_shot=few_shot)
    code = python_code_generation(qt, SERVICE=SERVICE, few_shot=few_shot)
    return {"Expression": exp, "Code": code}

def mathprompter(qt, variable_mapping, SERVICE, k = 5, few_shot=False): 
    result = defaultdict(lambda: None)
    try:
        math_prompts = generate_math_prompts(qt, SERVICE, few_shot=few_shot)
        result["Expression"] = math_prompts["Expression"]
        result["Code"] = math_prompts["Code"]
        results, res = perform_computational_verification(math_prompts, variable_mapping, sample_size=k)
        result["Result"] = res
        result["Results"] = results
        result["Expression_Result"] = evaluate_expression(math_prompts["Expression"], variable_mapping)
        result["Code_Result"] = execute_python_code(math_prompts["Code"], variable_mapping)
        result["Error"] = False
        result["Error_Message"] = ""
    except Exception as e:
        result["Error"] = True
        result["Error_Message"] = str(e)
        print(f"An error occurred during the verification process: {e}")
    return result

if __name__ == "__main__":
    from utils.method_utils import generating_algebraic_template
    from llm_inference.llm_factory import get_llm_service
    question = "Danny collects bottle caps and wrappers. He found 66 wrappers and 39 bottle caps at the park. Now he has 16 bottle caps and 68 wrappers in his collection. How many wrappers did Danny have at first?"
    qt, variable_mapping = generating_algebraic_template(question)
    # SERVICE = get_llm_service("llama", "mlx-community/Llama-3.2-1B-Instruct-4bit", 0.0, 200)
    SERVICE = get_llm_service("openai", "gpt-4o-mini", 0.0, 200)
    print(mathprompter(qt, variable_mapping, SERVICE=SERVICE, few_shot=True))
