import json
import matplotlib.pyplot as plt
import os
import numpy as np
import seaborn as sns

def load_data(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def print_data_statistics(data):
    total_questions = len(data)
    types = [item['Type'] for item in data]
    type_counts = {t: types.count(t) for t in set(types)}
    
    print(f"Total Questions: {total_questions}")
    print("Question Types Count:")
    for t, count in type_counts.items():
        print(f"{t}: {count}")

def plot_data_distribution(data):
    types = [item['Type'] for item in data]
    type_counts = {t: types.count(t) for t in set(types)}
    
    plt.figure(figsize=(10, 6))
    plt.bar(type_counts.keys(), type_counts.values())
    plt.title('Distribution of Question Types')
    plt.xlabel('Question Type')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    
    # Ensure the results directory exists
    os.makedirs('data_analysis_results', exist_ok=True)
    plt.savefig('data_analysis_results/question_type_distribution.png')
    plt.close()

def print_answer_range(data):
    answers = [item['Answer'] for item in data if 'Answer' in item]
    if answers:
        min_answer = min(answers)
        max_answer = max(answers)
        print(f"Range of Answers: {min_answer} to {max_answer}")
        
        # Plotting the histogram of answers
        plt.figure(figsize=(10, 6))
        plt.hist(answers, bins=20, color='blue', alpha=0.7)
        plt.title('Histogram of Answers')
        plt.xlabel('Answer Value')
        plt.ylabel('Frequency')
        plt.axvline(min_answer, color='red', linestyle='dashed', linewidth=1, label=f'Min: {min_answer}')
        plt.axvline(max_answer, color='green', linestyle='dashed', linewidth=1, label=f'Max: {max_answer}')
        plt.legend()
        
        # Ensure the results directory exists
        os.makedirs('data_analysis_results', exist_ok=True)
        plt.savefig('data_analysis_results/answer_range_histogram.png')
        plt.close()
    else:
        print("No answers found in the data.")

def plot_violin_plot(data):
    answers = [item['Answer'] for item in data if 'Answer' in item]
    if answers:
        plt.figure(figsize=(10, 6))
        
        # Create the violin plot
        sns.violinplot(x=answers)
        
        # Set the title and labels
        plt.title('Violin Plot of Answers (Log Scale)', fontsize=16)
        plt.xlabel('Answer Value', fontsize=14)
        plt.ylabel('Density', fontsize=14)  # Label for the y-axis
        
        # Set the x-axis to logarithmic scale
        plt.xscale('log')
        
        # Ensure the results directory exists
        os.makedirs('data_analysis_results', exist_ok=True)
        plt.savefig('data_analysis_results/answer_range_violin_plot_log.png')
        plt.close()
    else:
        print("No answers found in the data.")

def analyze_data(file_path):
    data = load_data(file_path)
    print_data_statistics(data)
    print_answer_range(data)
    plot_data_distribution(data)
    plot_violin_plot(data)

# Example usage
if __name__ == "__main__":
    analyze_data('../data/SVAMP.json') 