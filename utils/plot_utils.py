import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import precision_score

def compute_detailed_metrics(df, columns, correct_col):
    metrics = {
        'Method': columns,
        'Accuracy': [],
        'Hallucination Rate': [],
        'Precision': []
    }
    
    df = df.replace('None', "")
        
    for col in columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        correct = df[abs(df[col] - df[correct_col]) <= abs(df[correct_col]) * 5e-2]
        accuracy = len(correct) / len(df) if len(df) > 0 else 0
        
        hallucinations = df[(abs(df[col] - df[correct_col]) / abs(df[correct_col]) > 5e-2) & (df[col].notna()) & (df[col] != 'None')]
        hallucination_rate = len(hallucinations) / len(df) if len(df) > 0 else 0
        
        binary_true = (df[correct_col] == df[col]).astype(int)
        binary_pred = (df[col].notna() & (df[col] != 'None')).astype(int)
        
        precision = precision_score(binary_true, binary_pred, zero_division=0)
        
        # Debugging prints
        print(f"\nColumn: {col}")
        print(f"Correct entries count: {len(correct)}")
        print(f"Total non-NA predictions count: {df[col].notna().sum()}")
        print(f"Accuracy: {accuracy}")
        print(f"Hallucination Rate: {hallucination_rate}")
        print(f"Precision: {precision}")
        
        metrics['Accuracy'].append(accuracy)
        metrics['Hallucination Rate'].append(hallucination_rate)
        metrics['Precision'].append(precision)

    return pd.DataFrame(metrics)

def plot_individual_metrics(df_metrics, filename="temp.png"):
    metrics = df_metrics.columns[1:]
    fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(18, 6))
    for i, metric in enumerate(metrics):
        # Changed to set 'Method' as the hue and disable the legend directly.
        bar_plot = sns.barplot(x='Method', y=metric, hue='Method', data=df_metrics, ax=axes[i], palette='deep', legend=False)
        axes[i].set_title(f'{metric} Comparison by Method')
        axes[i].set_ylim(0, 1)

        # Adding labels inside the bars
        for p in bar_plot.patches:
            bar_plot.annotate(format(p.get_height(), '.2f'), 
                              (p.get_x() + p.get_width() / 2., p.get_height()), 
                              ha='center', va='center', 
                              size=9, xytext=(0, -12), 
                              textcoords='offset points')

    plt.tight_layout()
    plt.savefig(os.path.join('plots', filename))
    plt.close()

def plot_all_methods(folder_name):
    df_mathprompter = pd.read_csv(os.path.join('results', folder_name, 'mathprompter_results.csv'))
    df_mathprompterpp = pd.read_csv(os.path.join('results', folder_name, 'mathprompterpp_results.csv'))
    df_zeroshot_cot = pd.read_csv(os.path.join('results', folder_name, 'zeroshot_cot_results.csv'))

    # Compute metrics
    print("MathPrompter")
    mathprompter_metrics = compute_detailed_metrics(df_mathprompter, ['Predicted Answer', 'Predicted Algebraic Answer', 'Predicted Python Answer'], 'Correct Answer')
    print("MathPrompter++")
    mathprompterpp_metrics = compute_detailed_metrics(df_mathprompterpp, ['Predicted Answer', 'Predicted Algebraic Answer', 'Predicted Python Answer'], 'Correct Answer')
    print("Zeroshot CoT")
    zeroshot_cot_metrics = compute_detailed_metrics(df_zeroshot_cot, ['Predicted Answer'], 'Correct Answer')

    # # Plot metrics together 
    
    # fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(18, 6))
    # # The first plot will be the accuracy plot by taking the first element of the Accuracy column
    # sns.barplot(x='Method', y='Accuracy', hue='Method', data=mathprompter_metrics['Accuracy'][0], ax=axes[0], palette='deep', legend=False)
    # plt.savefig(os.path.join('results', folder_name, 'all_methods_accuracy.png'))
    # plt.close()

if __name__ == "__main__":
    all = input("Plot all methods? (y/n): ")
    if all == 'y':
        folder_name = input("Enter the folder name: ")
        plot_all_methods(folder_name)
    elif all == 'n':
        file_name = input("Enter the file name: ")
        columns = ["Predicted Answer", "Predicted Algebraic Answer", "Predicted Python Answer"]
        metrics = compute_detailed_metrics(file_name, columns, "Correct Answer")
        plot_individual_metrics(metrics)
    else:
        print("Invalid input. Please enter 'y' or 'n'.")
