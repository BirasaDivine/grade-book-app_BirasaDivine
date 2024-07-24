#!/usr/bin/python3
from grade_book import GradeBook
from datetime import datetime
import re
import time
import os

BLUE = "\033[38;5;33m"
RESET = "\033[0m"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_fancy_menu():
    menu = [
        "1. Add Student",
        "2. Add Course",
        "3. Register Student for Course",
        "4. Calculate Ranking",
        "5. Search by Grade",
        "6. Generate Transcript",
        "7. Exit"
    ]
    
    print("\n" + "=" * 40)
    print(f"{BLUE}        MENU OPTIONS{RESET}")
    print("=" * 40)
    
    for item in menu:
        print(f"║ {BLUE}{item:<36}{RESET} ║")
        time.sleep(0.05)
    
    print("=" * 40)

def main():
    grade_book = GradeBook()

    while True:
        print_fancy_menu()

        choice = input("\nEnter your choice: ")

        if choice == '1':
            while True:
                email = input("\nEnter student's email:")
                if not email:
                    print("\033[91mEmail is required!\033[0m\n")
                elif grade_book.get_student_by_email(email):
                    print("\033[91mEmail already exists!\033[0m\n")
                elif not email.endswith("@alustudent.com"):
                    print("\033[91mInvalid Email please Enter ALU's email!\033[0m\n")
                else:
                    break
            
            while True:
                names = input("\nEnter student's names: ")
                if not names:
                    print("\033[91mNames are required!\033[0m")
                    continue
                if not re.match(r'^[a-zA-Z\s]+$', names):
                    print("\033[91mEnter A Valid Name!\033[0m")
                    continue
                break

            while True:
                year = input("Enter student's year of enrollment: ")
                if year and not year.isdigit():
                    print("\033[91mYear should be a number!\033[0m")
                elif not year:
                    year = datetime.now().year
                    break
                else:
                    year = int(year)
                    break
    
            while True:
                unique_id = input("Enter student's ID: ")
                if not unique_id:
                    print("\033[91mID is required!\033[0m")
                    continue
                elif not unique_id.isdigit():
                    print("\033[91mID should be a number!\033[0m")
                    continue 

                if len(unique_id) < 4:
                    full_id = "0" * (4 - len(unique_id)) + unique_id
                    break
                elif len(unique_id) > 4:
                    print("\033[91mID should be 4 characters long!\033[0m")
                else:
                    full_id = unique_id
                    break

            id = f"ALU{full_id}{year}"
            grade_book.add_student(email, names, id)

        elif choice == '2':
            while True:
                name = input("Enter course name: ")
                if not name:
                    print("\033[91mCourse name is required!\033[0m")
                    continue
                if not re.match(r'^[a-zA-Z\s]+$', name):
                    print("\033[91mEnter A Valid Name of Course!\033[0m")
                    continue
                courses_list = []
                with open("./data/courses.txt", "r") as courses:
                    for line in courses:
                        if len(line.strip().split(",")) == 3:
                            course_name, trimester, credits = line.strip().split(",")
                            courses_list.append(course_name)
                    if not name:
                        print("\033[91mCourse name is required!\033[0m")
                    elif name in courses_list:
                        print("\033[91mCourse already exists!\033[0m")
                    else:
                        break
            
            trimesters = ["1st", "2nd", "3rd"]
            while True:
                trimester = input("Enter trimester(1st, 2nd, 3rd): ")
                if not trimester:
                    print("\033[91mTrimester is required!\033[0m")
                    continue
                elif trimester not in trimesters:
                    print("\033[91mInvalid trimester! Choose from 1st, 2nd, or 3rd.\033[0m")
                    continue
                else:
                    break
            while True:
                
                credits = (input("Enter course credits: "))
                if not credits:
                    print("\033[91mCredits are required!\033[0m")
                    continue
                elif re.match("^[0-9]*$", credits) == None:
                    print("\033[91mCredits must be an integer/float and greater than 0!\033[0m")
                    continue
                else:
                    break
            grade_book.add_course(name, trimester, credits)

        elif choice == '3':
            while True:
                student_email = input("Enter student's email: ")
            
                if not student_email:
                    print("\033[91mEmail is required!\033[0m")
                else:
                    student_emails = []
                    found = False
                    with open("./data/students.txt", "r") as file:
                        for line in file:
                            if len(line.strip().split(",")) == 3:
                                email, names, id = line.strip().split(",")
                                student_emails.append(email)
                                if student_email == email:
                                    print(f"\033[92mStudent Found: ({names} ID: {id})\033[0m")
                                    found = True
                                    break
            
                    if not found:
                        print("\033[91mStudent not found!\033[0m")
                    else:
                        break
            
            while True:
                course_name_input = input("Enter course name: ")
                if not course_name_input:
                    print("\033[91mCourse name is required!\033[0m")
                    continue
            
                found = False
                existing_courses = []
            
                with open("./data/courses.txt", "r") as file:
                    for line in file:
                        if len(line.strip().split(",")) == 3:
                            name, trimester, credits = line.strip().split(",")
                            existing_courses.append(name)
                            if course_name_input == name:
                                print(f"\033[92mCourse Found: {name} (Trimester: {trimester}, Credits: {credits})\033[0m")
                                found = True
            
                if not found:
                    print("\033[91mCourse not found!\033[0m")
                    print("Choose from already existing courses:")
                    for course in existing_courses:
                        print(f"\033[93m{course}\033[0m")
                    continue
            
                already_registered = False
                with open("./data/registered_courses.txt", "r") as file:
                    for line in file:
                        if len(line.strip().split(",")) == 3:
                            registered_email, registered_course_name, _ = line.strip().split(",")
                            if student_email == registered_email and course_name_input == registered_course_name:
                                print("\033[91mYou are already registered for this course. Please choose another course.\033[0m")
                                already_registered = True
                                break
            
                if not already_registered:
                    break
        
            while True:
                score = input("Enter grade (n/m): ")
                if not score:
                    print("\033[91mGrade is required!\033[0m")
                elif not re.match(r'^\d+/\d+$', score):
                    print("\033[91mInvalid grade format! Use n/m format.\033[0m")
                else:
                    try:
                        grade, highest_score = map(float, score.split('/'))
                        if grade > highest_score:
                            print("\033[91mInvalid grade! The obtained score cannot be greater than the highest possible score.\033[0m")
                        else:
                            normalized_grade = (grade / highest_score) * 4.0
                            print(f"\033[92mNormalized grade: {normalized_grade:.2f}\033[0m")
                            break
                    except ValueError:
                        print("\033[91mInvalid grade format! Use n/m format.\033[0m")
                
            grade_book.register_student_for_course(student_email, course_name_input, normalized_grade)

        elif choice == '4':
            ranking = grade_book.calculate_ranking()
            number = 1
            print(f"\n----------{BLUE}Ranking{RESET}-------------\n")
            for names, GPA in ranking:
                print(f"{number}.{names}: {GPA:.2f}\n")
                number += 1

        elif choice == '5':
            while True:
                course_name = input("Enter course name: ")
                if not course_name:
                    print("\033[91mCourse name is required!\033[0m")
                    continue

                found = False
                existing_courses = []

                with open("./data/courses.txt", "r") as file:
                    for line in file:
                        if len(line.strip().split(",")) == 3:
                            name, trimester, credits = line.strip().split(",")
                            existing_courses.append(name)
                            if course_name == name:
                                print(f"\033[92mCourse Found: {name} (Trimester: {trimester}, Credits: {credits})\033[0m")
                                found = True
                                break

                    if not found:
                        print("\033[91mCourse not found!\033[0m")
                        print("Choose from already existing courses:")
                        for course in existing_courses:
                            print(course)
                            continue

                if found:
                    break

            while True:
                min_grade = input("Enter minimum grade: ")
                if not min_grade:
                    print("\033[91mMinimum grade is required!\033[0m")
                else:
                    try:
                        min_grade = float(min_grade)
                        break
                    except ValueError:
                        raise ValueError("\033[91mThe grade must be an integer or a float!\033[0m")
            
            while True:
                max_grade = input("Enter maximum grade: ")
                if not max_grade:
                    print("\033[91mMaximum grade is required!\033[0m")
                else:
                    try:
                        max_grade = float(max_grade)
                        break
                    except ValueError:
                        raise ValueError("\033[91mThe grade must be an integer or a float!\033[0m")
            results = grade_book.search_by_grade(course_name, (min_grade, max_grade))
            print("\nSearch Results:")
            for names, grade in results:
                print(f"{names}: {grade}")

        elif choice == '6':
            while True:
                student_email = input("Enter student's email: ")
                if not student_email:
                    print("\033[91mEmail is required!\033[0m")
                else:
                    student_emails = []
                    found = False
                    with open("./data/students.txt", "r") as file:
                        for line in file:
                            if len(line.strip().split(",")) == 3:
                                email, names, id = line.strip().split(",")
                                student_emails.append(email)
                                if student_email == email:
                                    print(f"\033[92mStudent Found: ({names} ID: {id})\033[0m")
                                    found = True
                                    break

                    if not found:
                        print("\033[91mStudent not found!\033[0m")
                    else:
                        break

            transcript = grade_book.generate_transcript(student_email)
            if transcript:
                print("\n")
                print(f"{BLUE}                 STUDENT TRANSCRIPT{RESET}")
                print("=" * 60 + "\n")
                print(f"{BLUE}Student's Names{RESET}: {transcript['names']}")
                print(f"{BLUE}ID{RESET}: {id}")
                print(f"{BLUE}Email{RESET}: {transcript['email']}")
                print("\n" + "=" * 60)
                print(f"{BLUE}Courses and Grades{RESET}")
                print("=" * 60 + "\n")
                
                max_name_length = max(len(course) for course, _ in transcript['courses'])
                max_grade_length = max(len(f"{grade:.2f}") for _, grade in transcript['courses'])
                max_name_length = max(max_name_length, len("Course"))
                max_grade_length = max(max_grade_length, len("Grade"))
                
                print(f"{'Course':<{max_name_length}} | {'Grade':<{max_grade_length}}")
                print("-" * (max_name_length + max_grade_length + 3))
                
                for course, grade in transcript['courses']:
                    grade_str = f"{grade:.2f}"
                    print(f"{course:<{max_name_length}} | {grade_str:<{max_grade_length}}")
                    print("-" * (max_name_length + max_grade_length + 3))
                
                print(f"\n{BLUE}GPA{RESET}: {transcript['GPA']:.2f}")
                print("=" * 60 + "\n")

                while True:
                    choice = input("Do you want to save the transcript to a file (yes/no)? ")
                    if choice.lower() == 'yes':
                        with open("./data/students.txt", "r") as st:
                            for line in st:
                                if len(line.strip().split(",")) == 3:
                                    email, names, id = line.strip().split(",")
                                    if student_email == email:
                                        transcript['names'] = names
                                        break
                        with open(f"{transcript['names']}_transcript.txt", "w") as file:
                            file.write("="*60 + "\n")
                            file.write(f"{' '*25}STUDENT TRANSCRIPT{' '*25}\n")
                            file.write("="*60 + "\n\n")
                            file.write(f"Names: {transcript['names']}\n")
                            file.write(f"ID: {id}\n")
                            file.write(f"Email: {transcript['email']}\n")
                            file.write("\n")
                            file.write("=" * 60 + "\n")
                            file.write(f"Courses and Grades\n")
                            file.write("=" * 60 + "\n")
                            file.write(f"{'Course':<{max_name_length}} | {'Grade':<{max_grade_length}}\n")
                            file.write("-" * (max_name_length + max_grade_length + 3) + "\n")
                            for course, grade in transcript['courses']:
                                grade_str = f"{grade:.2f}"
                                file.write(f"{course:<{max_name_length}} | {grade_str:<{max_grade_length}}\n")
                                file.write("-" * (max_name_length + max_grade_length + 3) + "\n")
                            file.write(f"\nGPA: {transcript['GPA']:.2f}\n")
                            file.write("=" * 60 + "\n")
                        print("\033[92mTranscript saved successfully!\033[0m")
                        break
                    elif choice.lower() == 'no':
                        break
                    else:
                        print("\033[91mInvalid choice! Please enter 'yes' or 'no'.\033[0m")
            else:
                print("Student not found!")

        elif choice == '7':
            break

        else:
            print("\033[91mInvalid choice. Please try again.\033[0m")

if __name__ == "__main__":
    main()
