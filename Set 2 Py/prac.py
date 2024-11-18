import os
import json
import re
import matplotlib.pyplot as plt
from fpdf import FPDF
from datetime import datetime
from collections import Counter

# Validate functions
def is_positive_integer(value):
    return isinstance(value, int) and value > 0

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def is_valid_grade(grade):
    return grade in ["A", "B", "C", "F"]

def validate_student_data(student):
    errors = []
    if not is_positive_integer(student.get("Student ID", -1)):
        errors.append("Invalid Student ID")
    if not isinstance(student.get("Name", ""), str) or not student["Name"]:
        errors.append("Invalid Name")
    if not is_valid_email(student.get("Email", "")):
        errors.append("Invalid Email")
    if not isinstance(student.get("Course Name", ""), str) or not student["Course Name"]:
        errors.append("Invalid Course Name")
    if not is_positive_integer(student.get("Credits", -1)):
        errors.append("Invalid Credits")
    if not is_valid_grade(student.get("Grade", "")):
        errors.append("Invalid Grade")
    return errors

# Load and validate JSON file
def load_json(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {file_path} does not exist.")
    with open(file_path, 'r') as file:
        return json.load(file)

# Generate bar chart
def generate_bar_chart(course_counts):
    courses, counts = zip(*course_counts.items())
    plt.bar(courses, counts, color='skyblue')
    plt.xlabel('Course Name')
    plt.ylabel('Number of Students')
    plt.title('Course Enrollment Distribution')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('course_distribution.png')
    plt.close()

# Generate PDF report
def generate_pdf_report(course_counts, avg_credits, grade_counts):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, f"University Course Enrollment Report - {datetime.now().strftime('%Y-%m-%d')}", 0, 1, 'C')

    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"\nCourse Distribution Summary", 0, 1)
    for course, count in course_counts.items():
        pdf.cell(0, 10, f"{course}: {count} students", 0, 1)

    pdf.cell(0, 10, f"\nAverage Credits per Student: {avg_credits:.2f}", 0, 1)

    pdf.cell(0, 10, "\nGrade Distribution Summary", 0, 1)
    for grade, count in grade_counts.items():
        pdf.cell(0, 10, f"{grade}: {count} students", 0, 1)

    pdf.image('course_distribution.png', x=10, y=pdf.get_y() + 10, w=180)
    pdf.output("Course_Enrollment_Report.pdf")
    
def main():
    file_path = "data.json"
    
    try:
        # Load JSON data
        data = load_json(file_path)
        valid_data = []
        errors = []
        
        # Validate student data
        for student in data:
            validation_errors = validate_student_data(student)
            if validation_errors:
                errors.append({"Student ID": student.get("Student ID"), "Errors": validation_errors})
                continue
            valid_data.append(student)
        
        # Log errors
        if errors:
            with open("validation_errors.log", "w") as log_file:
                for error in errors:
                    log_file.write(f"{error}\n")
        
        # Calculate course distribution, average credits, and grade distribution
        course_counts = Counter([student["Course Name"] for student in valid_data])
        avg_credits = sum(student["Credits"] for student in valid_data) / len(valid_data)
        grade_counts = Counter([student["Grade"] for student in valid_data])
        
        # Generate bar chart
        generate_bar_chart(course_counts)
        
        # Generate PDF report
        generate_pdf_report(course_counts, avg_credits, grade_counts)
        print("Report successfully created.")
    
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except json.JSONDecodeError:
        print("Error: Invalid JSON format.")
    except ZeroDivisionError:
        print("Error: No valid student data to process.")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
