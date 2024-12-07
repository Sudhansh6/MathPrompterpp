import random
import math 
def create_random_input(mapping):
    """ Generate a random test input based on variable mappings. """
    return {var: random.randint(1, 500) for var in mapping}

def evaluate_expression(expression, mapping):
    """ Evaluates a mathematical expression safely using a dictionary of variable replacements. """
    try:
        local_dict = mapping.copy()
        local_dict['math'] = math  # Add this line to include the math module
        # print(f"Expression: {expression}")
        return eval(expression, {"__builtins__": None}, local_dict)
    except SyntaxError as e:
        print(f"Syntax error in the expression: {e}")
        return None
    except Exception as e:
        print(f"Runtime error during expression evaluation: {e}")
        return None

def execute_python_code(code, mapping):
    """
    Executes Python code with a specified input mapping.
    This code assumes the function 'solution' is defined within the passed code.
    """
    local_locals = mapping.copy()
    local_locals['math'] = math  # Add this line to include the math module
    wrapped_code = code + f"\nresult = solution({', '.join(f'{k}={v}' for k, v in mapping.items())})"
    try:
        exec(wrapped_code, local_locals)
        if 'result' in local_locals:
            return local_locals['result']
        else:
            print("No 'result' key was found in the local variables after executing the code.")
            return None
    except Exception as e:
        print(f"Error when executing Python code: {e}")
        return None

def perform_computational_verification(solutions, variable_mapping, sample_size=5):
    """
    Verifies that the execution results of both an expression and Python code are consistent across random inputs.
    This verification is repeated for a defined number of times specified by 'sample_size'.
    If consistent results are found, it evaluates them again with actual mappings to ensure accuracy.
    """
    results = {}
    for key in solutions.keys():
        results[key] = []
    results["Test_Input"] = []
    for _ in range(sample_size):
        test_input = create_random_input(variable_mapping)
        results_temp = {}
        for key in solutions.keys():
            if key == "Expression":
                result = float(evaluate_expression(solutions[key], test_input))
            elif key == "Code":
                result = float(execute_python_code(solutions[key], test_input))
            else:
                continue
            results_temp[key] = result
        results["Test_Input"].append(test_input)
        for key in results_temp.keys():
            # print(f"{key}: {results_temp[key]}")
            results[key].append(results_temp[key])

        if results_temp["Expression"] is None:
            # print("Expression is None")
            break

        if abs(results_temp["Expression"] - results_temp["Code"]) > abs(results_temp["Expression"]) * 5e-2:
            # print("Expression and Code are not consistent")
            # print(results_temp["Expression"], results_temp["Code"])
            return results, None
    # Consensus found, calculate result for real variable mapping
    exp_result = float(evaluate_expression(solutions["Expression"], variable_mapping))
    code_result = float(execute_python_code(solutions["Code"], variable_mapping))
    if abs(exp_result - code_result) / abs(exp_result) <= 5e-2 or exp_result is None:
        return results, code_result
    else:
        return results, None
    
    



