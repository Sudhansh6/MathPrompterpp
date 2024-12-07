import sys 
sys.path.append('..')
sys.path.append('../..')
sys.path.append('FinalCode')
import importlib 
import utils.compute_utils as compute_utils
importlib.reload(compute_utils)
from utils.compute_utils import perform_computational_verification, evaluate_expression, execute_python_code
from collections import defaultdict
import math

# DISCLAIMER: The following examples inside the prompts are partly generated with Claude Opus 3
# NOTE: You may adapt the prompt based on the model you use
ALGEBRAIC_FEW_SHOT_PROMPT = [
    {
        "question": "John has A apples. He gives B apples to his friend. How many apples does John have left? with variables: A, B",
        "answer": "A - B"
    },
    {
        "question": "A school has B classrooms. If each classroom has C students and D teachers, how many people are in the school? with variables: B, C, D",
        "answer": "(C + D) * B"
    },
    {
        "question": "A factory produces E widgets per hour. If the factory operates for F hours per day and G days per week, how many widgets does the factory produce in H weeks? with variables: E, F, G, H",
        "answer": "E * F * G * H"
    },
    {
        "question": "A company has I employees. Each employee works J hours per week. If the average hourly wage is K dollars and the company spends L percent of its revenue on salaries, what is the company's weekly revenue? with variables: I, J, K, L",
        "answer": "(I * J * K) / (L / 100)"
    },
    {
        "question": "A store has D shirts in stock. If they sell E shirts per day, how many days will it take to sell all the shirts? with variables: D, E ",
        "answer": "D // E"
    }
]


ALGEBRAIC_SYSTEM_PROMPT ='''
You are a highly qualified expert in finding algebra expressions for a given math problem in natural language. 
You are given a math word problem and you need to find the algebraic expression that represents the problem. You MUST FOLLOW THE EXACT INSTRUCTIONS.
1. Return only the algebraic expression that gives the final answer, without any explanations.
2. Do not create any variables, just use the given variables.
3. The expression should be a single line that can be evaluated using eval() in Python without any external libraries.
'''

def algebraic_expression_generation(question: str, SERVICE, few_shot=False):
    question = question.strip()
    if few_shot:
        messages = SERVICE.create_prompt(system_prompt=ALGEBRAIC_SYSTEM_PROMPT, few_shot_examples=ALGEBRAIC_FEW_SHOT_PROMPT, question=question)
    else:
        messages = SERVICE.create_prompt(system_prompt=ALGEBRAIC_SYSTEM_PROMPT, few_shot_examples=[], question=question)
    response = SERVICE.make_request(messages=messages)
    expression = response.strip()
    return expression


# DISCLAIMER: The following examples inside the prompts are partly generated with Claude Opus 3
# NOTE: You may adapt the prompt based on the model you use
PYTHON_FEW_SHOT_PROMPT = [
    {
        "question": "John has A apples. He gives B apples to his friend. How many apples does John have left? with variables: A, B",
        "answer": "def solution(A, B):\n    return A - B"
    },
    {
        "question": "A school has B classrooms. If each classroom has C students and D teachers, how many people are in the school? with variables: B, C, D",
        "answer": "def solution(B, C, D):\n    return (C + D) * B"
    },
    {
        "question": "A factory produces E widgets per hour. If the factory operates for F hours per day and G days per week, how many widgets does the factory produce in H weeks? with variables: E, F, G, H",
        "answer": "def solution(E, F, G, H):\n    return E * F * G * H"
    },
    {
        "question": "A company has I employees. Each employee works J hours per week. If the average hourly wage is K dollars and the company spends L percent of its revenue on salaries, what is the company's weekly revenue? with variables: I, J, K, L",
        "answer": "def solution(I, J, K, L):\n    return (I * J * K) / (L / 100)"
    },
    {
        "question": "Where does the image of an object appear when the object is placed in front of a concave mirror with radius R? with variables: R",
        "answer": "def solution(R):\n    return R / 2"
    }
]

PYTHON_SYSTEM_PROMPT = '''
You are a highly qualified expert in finding Python code for a given math problem in natural language.
You are given a math word problem and you need to find the Python code that solves the problem. You MUST FOLLOW THE EXACT INSTRUCTIONS.
1. Return only the Python code that solves the problem, without any explanations.
2. The code should contain a single function called solution that takes all the variables as input.
3. The code be executable using exec() in Python without any external libraries.
4. Do not prepend with ```python or ```
'''

def python_code_generation(question, SERVICE, few_shot=False):
    if few_shot:
        messages = SERVICE.create_prompt(system_prompt=PYTHON_SYSTEM_PROMPT, few_shot_examples=PYTHON_FEW_SHOT_PROMPT, question=question)
    else:
        messages = SERVICE.create_prompt(system_prompt=PYTHON_SYSTEM_PROMPT, few_shot_examples=[], question=question)
    response = SERVICE.make_request(messages=messages)
    function_code = response.strip()
    if function_code.startswith("```python"):
        function_code = function_code[9:]
    if function_code.endswith("```"):
        function_code = function_code[:-3]
    return function_code.strip()

ROUGH_SOLUTION_SYSTEM_PROMPT = '''
You are a highly qualified expert in finding the rough steps to solve a given math problem in natural language.
You are given a math word problem and you need to find the rough steps to solve the problem. You MUST FOLLOW THE EXACT INSTRUCTIONS.
1. Think step by step and give the answer as a numbered list of steps.
2. Mention known mathematical formulas, shortcuts or concepts based on the given variables.
3. Do not provide the complete exhaustive solution, only the rough steps.
4. Do not create any variables, just use the given variables.
5. Do not use any numbers from the questions in the steps.
'''
ROUGH_SOLUTION_FEW_SHOT_PROMPT = [
    {
        "question": "Mike invited A friends to a birthday party, but B couldn't come. If he wanted to buy enough cupcakes so each person could have exactly C, how many should he buy?",
        "answer": "1. Subtract the number of friends who couldn't come from the total number of friends invited to find out how many people will be at the party.\n2. Multiply the number of people at the party by the number of cupcakes each person should have to find out how many cupcakes Mike should buy."
    },
    {
        "question": "At a restaurant, each adult meal costs $ A and kids eat free. If a group of B people came in and C were kids, how much would it cost for the group to eat?",
        "answer": "1. Subtract the number of kids from the total number of people to find out how many adults are at the restaurant.\n2. Multiply the number of adults by the cost of each adult meal to find out how much it would cost for the group to eat."
    },
    {
        "question": "A store has D shirts in stock. If they sell E shirts per day, how many days will it take to sell all the shirts?",
        "answer": "1. Divide the total number of shirts by the number of shirts sold per day to find out how many days it will take to sell all the shirts."
    },
    {
        "question": "What is the area under the curve y = x^A + B from x = C to x = D?",
        "answer": "1. Find the antiderivative of the function.\n2. Subtract the antiderivative at x = C from the antiderivative at x = D to find the area under the curve."
    },
    {
        "question": "What are the roots of the quadratic equation x^2 + Bx + C = 0?",
        "answer": "1. Use the quadratic formula to find the roots of the equation.\n2. Calculate the discriminant \n3. If the discriminant is negative, the roots are complex. If it's zero, there's one real root. If positive, there are two real roots."
    }
]

def generate_rough_solution(qt, SERVICE, few_shot=False):
    prompt = f"Provide a rough solution to: {qt}"
    if few_shot:
        messages = SERVICE.create_prompt(system_prompt=ROUGH_SOLUTION_SYSTEM_PROMPT, few_shot_examples=ROUGH_SOLUTION_FEW_SHOT_PROMPT, question=prompt)
    else:
        messages = SERVICE.create_prompt(system_prompt=ROUGH_SOLUTION_SYSTEM_PROMPT, few_shot_examples=[], question=prompt)
    response = SERVICE.make_request(messages=messages)
    return response.strip()


def generate_math_prompts(qt, SERVICE, few_shot=False):
    exp = algebraic_expression_generation(qt, SERVICE=SERVICE, few_shot=few_shot)
    code = python_code_generation(qt, SERVICE=SERVICE, few_shot=few_shot)
    return {"Expression": exp, "Code": code}

def mathprompterpp(question, qt, variable_mapping, SERVICE, k = 5, few_shot=False): 
    result = defaultdict(lambda: None)
    try:
        rough_solution = generate_rough_solution(question, SERVICE, few_shot=few_shot)
        result["Rough_Solution"] = rough_solution
        prompt = f"{qt} with variables: {', '.join(variable_mapping.keys())}. Use the rough steps to solve the problem: {rough_solution}"
        math_prompts = generate_math_prompts(prompt, SERVICE, few_shot=few_shot)
        result["Expression"] = math_prompts["Expression"]
        result["Code"] = math_prompts["Code"]
        results, res = perform_computational_verification(math_prompts, variable_mapping, sample_size=k)
        result["Results"] = results
        result["Result"] = res
        result["Expression_Result"] = evaluate_expression(math_prompts["Expression"], variable_mapping)
        result["Code_Result"] = execute_python_code(math_prompts["Code"], variable_mapping)
        if res is None:
            res = math_prompts["Code_Result"]
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
    question = " Danny collects bottle caps and wrappers. He found 66 wrappers and 39 bottle caps at the park. Now he has 16 bottle caps and 68 wrappers in his collection. How many wrappers did Danny have at first?"
    qt, variable_mapping = generating_algebraic_template(question)
    # SERVICE = get_llm_service("llama", "mlx-community/Llama-3.2-1B-Instruct-4bit", 0.0, 200)
    SERVICE = get_llm_service("openai", "gpt-4o-mini", 0.0, 200)
    print(mathprompterpp(question, qt, variable_mapping, SERVICE=SERVICE, few_shot=True))
    
