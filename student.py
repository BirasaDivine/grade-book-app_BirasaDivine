#!/usr/bin/python3


class Student:
    def __init__(self, email, names, id):
        self.email = email
        self.names = names
        self.id = id
        self.courses_registered = []
        self.GPA = 0.0
        self.credits = 0

    def load_courses(self):
        with open("data/registered_courses.txt", "r") as file:
            for line in file:
                student_email, course_name, grade = line.strip().split(",")
                if student_email == self.email:
                    self.courses_registered.append({'course': course_name, 'grade': float(grade)})
        
        with open("data/courses.txt", "r") as file:
            for line in file:
                name, trimester, credits = line.strip().split(",")
                for course in self.courses_registered:
                    if course['course'] == name:
                        self.credits += int(credits)

    def register_for_course(self, course, grade):
        self.courses_registered.append({'course': course, 'grade': grade})

    def calculate_GPA(self):
        total_grades = sum(course['grade'] for course in self.courses_registered)
        self.GPA = total_grades / len(self.courses_registered) if self.courses_registered else 0.0
