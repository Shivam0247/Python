import pandas as pd

file_path = r"C:\Data\workspace\Advance Python\Practical 3\student_grades.csv"
try:
    df = pd.read_csv(file_path)
    print(df)
except IOError:
    print("Error reading the CSV file.")
    exit()

average_scores = {}
total_average_score = 0
student_count = 0

# Calculate and store the average score for each student
for index, row in df.iterrows():
    maths_score = row['Maths'] if pd.notna(row['Maths']) else 0
    science_score = row['Science'] if pd.notna(row['Science']) else 0
    english_score = row['English'] if pd.notna(row['English']) else 0
    
    total_score = maths_score + science_score + english_score
    average_score = total_score / 3
    
    average_scores[row['roll_no']] = {'name': row['name'], 'average_score': average_score}
    
    # Total score
    total_average_score += average_score
    student_count += 1

# Calculate the class average score
class_average_score = total_average_score / student_count

print(f"Average score of the class: {class_average_score:.2f}")

# Convert the dictionary to a DataFrame
average_scores_df = pd.DataFrame.from_dict(average_scores, orient='index')

# Add the class average score to the DataFrame
average_scores_df.loc['Class Average'] = {'name': 'Class Average', 'average_score': class_average_score}

# Save the DataFrame to a new CSV file
output_file_path = r"C:\Data\workspace\Advance Python\Practical 3\student_average_grades.csv"
average_scores_df.to_csv(output_file_path, index_label='roll_no')

print(f"Average scores saved to {output_file_path}")
