import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
import csv
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Student:
    def __init__(self, email, names, profile_picture=None):
        self.email = email
        self.names = names
        self.courses_registered = []
        self.GPA = 0.0
        self.profile_picture = profile_picture
    
    def calculate_GPA(self):
        if not self.courses_registered:
            self.GPA = 0.0
            return self.GPA
        total_points = sum(course['grade'] * course['credits'] for course in self.courses_registered)
        total_credits = sum(course['credits'] for course in self.courses_registered)
        self.GPA = total_points / total_credits if total_credits != 0 else 0.0
        return self.GPA
    
    def register_for_course(self, course, grade):
        self.courses_registered.append({'name': course['name'], 'credits': course['credits'], 'grade': grade})

class Course:
    def __init__(self, name, trimester, credits):
        self.name = name
        self.trimester = trimester
        self.credits = credits

class GradeBook:
    def __init__(self):
        self.student_list = []
        self.course_list = []
    
    def add_student(self, email, names, profile_picture=None):
        new_student = Student(email, names, profile_picture)
        self.student_list.append(new_student)
    
    def add_course(self, name, trimester, credits):
        new_course = Course(name, trimester, credits)
        self.course_list.append(new_course)
    
    def register_student_for_course(self, email, course_name, grade):
        student = next((s for s in self.student_list if s.email == email), None)
        course = next((c for c in self.course_list if c.name == course_name), None)
        if student and course:
            student.register_for_course({'name': course.name, 'credits': course.credits}, grade)
    
    def calculate_GPA(self, email):
        student = next((s for s in self.student_list if s.email == email), None)
        if student:
            return student.calculate_GPA()
        return None
    
    def calculate_ranking(self):
        self.student_list.sort(key=lambda s: s.calculate_GPA(), reverse=True)
        return [(s.email, s.GPA) for s in self.student_list]
    
    def search_by_grade(self, min_grade, max_grade):
        filtered_students = []
        for student in self.student_list:
            for course in student.courses_registered:
                if min_grade <= course['grade'] <= max_grade:
                    filtered_students.append((student.email, course['name'], course['grade']))
                    break
        return filtered_students
    
    def generate_transcript(self, email):
        student = next((s for s in self.student_list if s.email == email), None)
        if student:
            transcript = {
                'email': student.email,
                'names': student.names,
                'GPA': student.calculate_GPA(),
                'courses': student.courses_registered
            }
            return transcript
        return None
    
    def save_to_file(self, filename):
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Email', 'Names', 'Courses Registered', 'GPA'])
            for student in self.student_list:
                writer.writerow([student.email, student.names, student.courses_registered, student.GPA])

class GradeBookApp:
    def __init__(self, root):
        self.grade_book = GradeBook()
        self.root = root
        self.root.title("ALU Grade Book Application")
        self.root.configure(bg='white')
        self.create_dashboard()

    def create_dashboard(self):
        self.clear_frame()
        
        frame = tk.Frame(self.root, bg='white')
        frame.pack(pady=20, padx=20)
        
        tk.Label(frame, text="ALU Grade Book Dashboard", font=("Helvetica", 16, 'bold'), bg='white', fg='red').pack(pady=10)
        
        summary_frame = tk.Frame(frame, bg='white')
        summary_frame.pack(pady=10)
        
        num_students = len(self.grade_book.student_list)
        num_courses = len(self.grade_book.course_list)
        avg_gpa = sum(student.calculate_GPA() for student in self.grade_book.student_list) / num_students if num_students > 0 else 0
        
        tk.Label(summary_frame, text=f"Number of Students: {num_students}", font=("Helvetica", 12), bg='white', fg='blue').grid(row=0, column=0, padx=20)
        tk.Label(summary_frame, text=f"Number of Courses: {num_courses}", font=("Helvetica", 12), bg='white', fg='blue').grid(row=0, column=1, padx=20)
        tk.Label(summary_frame, text=f"Average GPA: {avg_gpa:.2f}", font=("Helvetica", 12), bg='white', fg='blue').grid(row=0, column=2, padx=20)
        
        button_frame = tk.Frame(frame, bg='white')
        button_frame.pack(pady=20)
        
        buttons = [
            ("Add Student", self.add_student),
            ("Add Course", self.add_course),
            ("Register Student for Course", self.register_student_for_course),
            ("Calculate GPA", self.calculate_GPA),
            ("Calculate Ranking", self.calculate_ranking),
            ("Search by Grade", self.search_by_grade),
            ("Generate Transcript", self.generate_transcript),
            ("Save to File", self.save_to_file),
            ("View GPA Chart", self.view_gpa_chart),
            ("Exit", self.root.quit)
        ]
        
        for text, command in buttons:
            button = tk.Button(button_frame, text=text, command=command, width=30, height=2, bg='red', fg='white')
            button.pack(pady=5)
    
    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def add_student(self):
        email = simpledialog.askstring("Input", "Enter student email:")
        names = simpledialog.askstring("Input", "Enter student names:")
        profile_picture = filedialog.askopenfilename(title="Select Profile Picture", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        profile_image = Image.open(profile_picture)
        profile_image.thumbnail((100, 100))
        profile_image.save(f"images/{email}.png")
        self.grade_book.add_student(email, names, profile_picture=f"images/{email}.png")
        messagebox.showinfo("Info", "Student added successfully.")
    
    def add_course(self):
        name = simpledialog.askstring("Input", "Enter course name:")
        trimester = simpledialog.askstring("Input", "Enter trimester:")
        credits = simpledialog.askinteger("Input", "Enter course credits:")
        self.grade_book.add_course(name, trimester, credits)
        messagebox.showinfo("Info", "Course added successfully.")
    
    def register_student_for_course(self):
        email = simpledialog.askstring("Input", "Enter student email:")
        course_name = simpledialog.askstring("Input", "Enter course name:")
        grade = simpledialog.askfloat("Input", "Enter grade:")
        self.grade_book.register_student_for_course(email, course_name, grade)
        messagebox.showinfo("Info", "Student registered for course successfully.")
    
    def calculate_GPA(self):
        email = simpledialog.askstring("Input", "Enter student email:")
        gpa = self.grade_book.calculate_GPA(email)
        if gpa is not None:
            messagebox.showinfo("Info", f"GPA for {email}: {gpa}")
        else:
            messagebox.showerror("Error", "Student not found.")
    
    def calculate_ranking(self):
        ranking = self.grade_book.calculate_ranking()
        result = "Student Ranking by GPA:\n"
        for rank, (email, gpa) in enumerate(ranking, start=1):
            result += f"{rank}. {email} - GPA: {gpa}\n"
        messagebox.showinfo("Ranking", result)
    
    def search_by_grade(self):
        min_grade = simpledialog.askfloat("Input", "Enter minimum grade:")
        max_grade = simpledialog.askfloat("Input", "Enter maximum grade:")
        results = self.grade_book.search_by_grade(min_grade, max_grade)
        result = "Students with grades in range:\n"
        for email, course_name, grade in results:
            result += f"{email} - {course_name}: {grade}\n"
        messagebox.showinfo("Search Results", result)
    
    def generate_transcript(self):
        email = simpledialog.askstring("Input", "Enter student email:")
        transcript = self.grade_book.generate_transcript(email)
        if transcript:
            result = f"Transcript for {email}:\n"
            result += f"Names: {transcript['names']}\n"
            result += f"GPA: {transcript['GPA']}\n"
            result += "Courses Registered:\n"
            for course in transcript['courses']:
                result += f"  - {course['name']}: {course['grade']} (Credits: {course['credits']})\n"
            messagebox.showinfo("Transcript", result)
        else:
            messagebox.showerror("Error", "Student not found.")
    
    def save_to_file(self):
        filename = simpledialog.askstring("Input", "Enter filename to save:")
        self.grade_book.save_to_file(filename)
        messagebox.showinfo("Info", "Data saved to file.")
    
    def view_gpa_chart(self):
        students = self.grade_book.student_list
        if not students:
            messagebox.showinfo("Info", "No students available to display GPA chart.")
            return

        emails = [student.email for student in students]
        gpas = [student.calculate_GPA() for student in students]

        fig, ax = plt.subplots()
        ax.barh(emails, gpas, color='skyblue')
        ax.set_xlabel('GPA')
        ax.set_title('Student GPA Chart')

        chart_window = tk.Toplevel(self.root)
        chart_window.title("GPA Chart")
        canvas = FigureCanvasTkAgg(fig, master=chart_window)
        canvas.draw()
        canvas.get_tk_widget().pack()

def main():
    root = tk.Tk()
    app = GradeBookApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
