import json

# Load the JSON data
with open('domain.json', 'r') as file:
    data = json.load(file)

# Initialize a set to track seen questions and a list for duplicates
seen_questions = set()
duplicates = []

# Iterate through the challenges to find duplicates
print(len(data))
for item in data:
    question = item['Question']
    if question in seen_questions:
        duplicates.append(question)
    else:
        seen_questions.add(question)

# Print the duplicate questions
if duplicates:
    print("Duplicate Questions Found:")
    for question in duplicates:
        print(question)
else:
    print("No duplicate questions found.")
