from student import Student
from course import Course

class GradeBook:
    def __init__(self):
        self.student_list = self.load_students()
        self.course_list = self.load_courses()

    def load_students(self):
        students = []
        with open("data/students.txt", "r") as file:
            for line in file:
                email, names, id = line.strip().split(",")
                student = Student(email, names, id)
                students.append(student)
        return students

    def load_courses(self):
        courses = []
        with open("data/courses.txt", "r") as file:
            for line in file:
                name, trimester, credits = line.strip().split(",")
                course = Course(name, trimester, int(credits))
                courses.append(course)
        return courses

    def load_registered_courses(self):
        registered_courses = []
        with open("data/registered_courses.txt", "r") as file:
            for line in file:
                student_email, course_name, grade = line.strip().split(",")
                registered_courses.append((student_email, course_name, float(grade)))
        return registered_courses

    def add_student(self, email, names, id):
        student = Student(email, names, id)
        self.student_list.append(student)
        with open("data/students.txt", "a") as file:
            file.write(f"{email},{names},{id}\n")

    def add_course(self, name, trimester, credits):
        course = Course(name, trimester, credits)
        self.course_list.append(course)
        with open("data/courses.txt", "a") as file:
            file.write(f"{name},{trimester},{credits}\n")

    def register_student_for_course(self, student_email, course_name, grade):
        with open("data/registered_courses.txt", "a") as file:
            file.write(f"{student_email},{course_name},{grade}\n")

    def calculate_ranking(self):
        students = self.load_students()
        courses = self.load_courses()
        registered_courses = self.load_registered_courses()

        course_credits = {course.name: course.credits for course in courses}
        student_grades = {student.email: [] for student in students}

        for email, course_name, grade in registered_courses:
            if email in student_grades and course_name in course_credits:
                student_grades[email].append((grade, course_credits[course_name]))

        student_GPAs = []
        for student in students:
            grades_with_credits = student_grades[student.email]
            if grades_with_credits:
                total_weighted_grades = sum(grade * credits for grade, credits in grades_with_credits)
                total_credits = sum(credits for _, credits in grades_with_credits)
                GPA = total_weighted_grades / total_credits
                student_GPAs.append((student.names, GPA))

        student_GPAs.sort(key=lambda x: x[1], reverse=True)
        return student_GPAs

    def search_by_grade(self, course_name, grade_range):
        registered_courses = self.load_registered_courses()
        student_emails = set(email for email, course, grade in registered_courses if course == course_name and grade_range[0] <= grade <= grade_range[1])

        students = self.load_students()
        results = [(student.names, grade) for student in students for email, course, grade in registered_courses if student.email == email and course == course_name and grade_range[0] <= grade <= grade_range[1]]

        return results

    def generate_transcript(self, student_email):
        students = self.load_students()
        courses = self.load_courses()
        registered_courses = self.load_registered_courses()
        student = next((student for student in students if student.email == student_email), None)

        if student:
            student_courses = [(course, grade) for email, course, grade in registered_courses if email == student_email]
            course_credits = {course.name: course.credits for course in courses}
            total_weighted_grades = sum(grade * course_credits[course] for course, grade in student_courses)
            total_credits = sum(course_credits[course] for course, _ in student_courses)
            GPA = total_weighted_grades / total_credits if total_credits else 0.0

            transcript = {
                'email': student.email,
                'names': student.names,
                'GPA': GPA,
                'courses': student_courses
            }
            return transcript
        return None

    def get_student_by_email(self, email):
        for student in self.load_students():
            if student.email == email:
                return student
        return None

    def get_course_by_name(self, name):
        for course in self.load_courses():
            if course.name == name:
                return course
        return None
grade_book = GradeBook()