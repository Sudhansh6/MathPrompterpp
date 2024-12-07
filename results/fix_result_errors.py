import pandas as pd

# Load the CSV file
file_path = 'FinalCode/results/1419903_multiarith_gpt-4o-mini_600/mathprompter_results.csv'
df = pd.read_csv(file_path)

# Function to check and update the Predicted Answer
def update_predicted_answer(row):
    predicted_answer = row['Predicted Answer']
    predicted_algebraic = row['Predicted Algebraic Answer']
    predicted_code = row['Predicted Python Answer']
    
    # Check if Predicted Answer is empty
    if pd.isna(predicted_answer):
        # Check if both Predicted Algebraic and Predicted Code are not NaN
        if not pd.isna(predicted_algebraic) and not pd.isna(predicted_code):
            # Calculate the percentage difference
            algebraic_value = predicted_algebraic
            code_value = predicted_code
            
            # Check if they are within 5%
            if abs(algebraic_value - code_value) <= 0.05 * max(algebraic_value, code_value):
                return code_value  # Fill with Predicted Code Answer
    return predicted_answer  # Return original if no update

# Apply the function to update the Predicted Answer
df['Predicted Answer'] = df.apply(update_predicted_answer, axis=1)

# Save the updated DataFrame back to the CSV file
df.to_csv(file_path, index=False)

print("CSV file has been updated successfully.")
