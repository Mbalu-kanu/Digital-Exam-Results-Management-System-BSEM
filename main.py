"""Digital Exam and Results Management System.

A simple console program for managing fictional student exam results.
All records are fictional demonstration data.
"""


class ExamResult:
    """One exam result: a module (subject) and a mark from 0 to 100."""

    PASS_MARK = 50
    # Tuples: fixed lists that should never change while the program runs.
    MODULES = (
        "Mathematics",
        "Python Programming",
        "Database Programming",
        "Data Systems",
        "Object-Oriented Programming",
        "Web Development",
    )
    # (minimum mark, grade)
    GRADE_BANDS = ((70, "A"), (60, "B"), (50, "C"), (40, "D"), (0, "F"))

    def __init__(self, subject, mark):
        self.subject = subject
        self.mark = mark

    @staticmethod
    def is_valid_mark(mark):
        """Static method: a mark is valid only if it is from 0 to 100."""
        return 0 <= mark <= 100

    def update_mark(self, new_mark):
        """Instance method: change this result if the new mark is valid."""
        if ExamResult.is_valid_mark(new_mark):
            self.mark = new_mark
            return True
        return False

    def get_grade(self):
        for minimum, grade in ExamResult.GRADE_BANDS:
            if self.mark >= minimum:
                return grade

    def display_info(self):
        print(f"   {self.subject}: {self.mark} (Grade {self.get_grade()})")


class Student:
    """A fictional student with a list of ExamResult objects."""

    COURSES = (
        "Software Engineering",
        "Database Programming",
        "Data Systems",
        "Object-Oriented Programming",
        "Information Technology",
    )
    GENDERS = ("Male", "Female", "Prefer not to say")

    total_students = 0  # class attribute shared by all Student objects

    def __init__(self, student_id, first_name, last_name, age, gender, course):
        self.student_id = student_id
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.gender = gender
        self.course = course
        self.results = []  # list of ExamResult objects
        Student.total_students += 1

    @classmethod
    def get_total_students(cls):
        """Class method: how many Student objects have been created."""
        return cls.total_students

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def find_result(self, subject):
        """Loop through the results list and return the matching ExamResult, or None."""
        for result in self.results:
            if result.subject == subject:
                return result
        return None

    def add_result(self, subject, mark):
        """Add a new result, or replace the mark if the subject already exists."""
        existing = self.find_result(subject)
        if existing is None:
            self.results.append(ExamResult(subject, mark))
        else:
            existing.update_mark(mark)

    def update_result(self, subject, new_mark):
        """Update an existing result. Returns False if the subject has no result."""
        result = self.find_result(subject)
        if result is None:
            return False
        return result.update_mark(new_mark)

    def average_mark(self):
        if len(self.results) == 0:
            return None
        marks = [result.mark for result in self.results]
        return sum(marks) / len(marks)

    def display_info(self):
        print(
            f"ID: {self.student_id} | Name: {self.full_name()} | Age: {self.age} "
            f"| Gender: {self.gender} | Course: {self.course}"
        )
        if len(self.results) == 0:
            print("   No results recorded yet.")
        for result in self.results:
            result.display_info()
        average = self.average_mark()
        if average is not None:
            print(f"   Average: {average:.1f}")


class ResultsManager:
    """Stores all Student objects in ONE list."""

    def __init__(self):
        self.students = []  # the ONE main data structure: a list of Student objects
        self.next_number = 1  # used to create IDs: S001, S002, S003, ...

    def create_student_id(self):
        """Make the next unused ID automatically, so IDs can never repeat."""
        student_id = "S" + str(self.next_number).zfill(3)
        while self.find_student(student_id) is not None:
            self.next_number += 1
            student_id = "S" + str(self.next_number).zfill(3)
        self.next_number += 1
        return student_id

    def add_student(self, first_name, last_name, age, gender, course):
        """Create a Student with a new ID, add it to the list, return it."""
        student_id = self.create_student_id()
        student = Student(student_id, first_name, last_name, age, gender, course)
        self.students.append(student)
        return student

    def find_student(self, student_id):
        """Loop through the list and return the matching Student, or None."""
        for student in self.students:
            if student.student_id == student_id:
                return student
        return None

    def record_result(self, student_id, subject, mark):
        student = self.find_student(student_id)
        if student is None or not ExamResult.is_valid_mark(mark):
            return False
        student.add_result(subject, mark)
        return True

    def show_student_list(self):
        """Print a short list of IDs and names so the user can pick an ID."""
        print("Students:")
        for student in self.students:
            print(f"  {student.student_id} - {student.full_name()} ({student.course})")

    def display_all(self):
        if len(self.students) == 0:
            print("No student records yet.")
            return
        print(f"Total students: {len(self.students)}")
        print("-" * 40)
        for student in self.students:
            student.display_info()
            print("-" * 40)

    def summary(self):
        marks = [
            result.mark
            for student in self.students
            for result in student.results
        ]
        print("--- Results Summary ---")
        print(f"Total students: {Student.get_total_students()}")
        print(f"Total results recorded: {len(marks)}")
        if len(marks) == 0:
            print("No marks to summarise yet.")
            return
        passed = len([m for m in marks if m >= ExamResult.PASS_MARK])
        print(f"Average mark: {sum(marks) / len(marks):.1f}")
        print(f"Highest mark: {max(marks)}")
        print(f"Lowest mark: {min(marks)}")
        print(f"Passed (>= {ExamResult.PASS_MARK}): {passed}")
        print(f"Failed: {len(marks) - passed}")

    def load_demo_data(self):
        """Fictional demonstration records only."""
        demo = (
            ("Aisha", "Bangura", 20, "Female", "Software Engineering", (78, 64, 71, 59, 82, 66)),
            ("Brian", "Mensah", 22, "Male", "Database Programming", (45, 52, 38, 61, 49, 55)),
            ("Chloe", "Davies", 21, "Female", "Data Systems", (90, 73, 55, 68, 74, 81)),
            ("David", "Okoro", 23, "Male", "Object-Oriented Programming", (34, 48, 51, 42, 60, 39)),
            ("Esther", "Koroma", 19, "Female", "Information Technology", (67, 70, 62, 75, 58, 69)),
            ("Felix", "Turay", 24, "Male", "Software Engineering", (55, 49, 63, 57, 71, 64)),
            ("Grace", "Johnson", 20, "Female", "Data Systems", (88, 92, 85, 79, 90, 94)),
            ("Hassan", "Kamara", 22, "Male", "Database Programming", (41, 36, 47, 52, 44, 50)),
            ("Isha", "Conteh", 21, "Female", "Object-Oriented Programming", (72, 66, 80, 77, 69, 73)),
            ("James", "Sesay", 25, "Male", "Information Technology", (58, 61, 54, 66, 63, 59)),
            ("Kadiatu", "Bah", 19, "Female", "Software Engineering", (96, 89, 91, 84, 87, 93)),
            ("Lamin", "Fofanah", 23, "Male", "Data Systems", (29, 44, 37, 51, 46, 40)),
        )
        for first, last, age, gender, course, marks in demo:
            student = self.add_student(first, last, age, gender, course)
            for index in range(len(marks)):
                self.record_result(
                    student.student_id, ExamResult.MODULES[index], marks[index]
                )


def ask_text(prompt):
    """Keep asking until the user types something that is not empty."""
    while True:
        value = input(prompt).strip()
        if value != "":
            return value
        print("Input cannot be empty. Please try again.")


def ask_id(prompt):
    return ask_text(prompt).upper()


def ask_age(prompt):
    """Keep asking until the user types a whole number from 10 to 100."""
    while True:
        text = input(prompt).strip()
        if text.isdigit() and 10 <= int(text) <= 100:
            return int(text)
        print("Invalid age. Please enter a whole number from 10 to 100.")


def ask_mark(prompt):
    """Keep asking until the user types a number from 0 to 100."""
    while True:
        text = input(prompt).strip()
        try:
            mark = float(text)
        except ValueError:
            print("Invalid input. Please enter a number, for example 75.")
            continue
        if ExamResult.is_valid_mark(mark):
            return int(mark) if mark == int(mark) else mark
        print("Invalid mark. Marks must be from 0 to 100.")


def ask_choice(title, options):
    """Show a numbered list and return the option the user picks."""
    print(title)
    for index in range(len(options)):
        print(f"  {index + 1}. {options[index]}")
    while True:
        text = input(f"Choose a number (1-{len(options)}): ").strip()
        if text.isdigit() and 1 <= int(text) <= len(options):
            return options[int(text) - 1]
        print(f"Invalid choice. Please enter a number from 1 to {len(options)}.")


def show_menu():
    print("\n=== Digital Exam and Results Management System ===")
    print("1. Add a student record")
    print("2. Record an exam result")
    print("3. Display all student records and results")
    print("4. Search for a student by ID")
    print("5. Update an exam result")
    print("6. Display results summary")
    print("7. Exit")


def main():
    manager = ResultsManager()
    manager.load_demo_data()
    print(f"Demo data loaded: {len(manager.students)} fictional students (S001 to S{len(manager.students):03d}).")

    while True:
        show_menu()
        choice = input("Choose an option (1-7): ").strip()

        if choice == "1":
            first_name = ask_text("Enter student first name: ").title()
            last_name = ask_text("Enter student last name: ").title()
            age = ask_age("Enter student age: ")
            gender = ask_choice("Select gender:", Student.GENDERS)
            course = ask_choice("Select course:", Student.COURSES)
            student = manager.add_student(first_name, last_name, age, gender, course)
            print(
                f"Student added successfully. ID: {student.student_id} | "
                f"Name: {student.full_name()} | Course: {student.course}"
            )
            print(f"Total students now: {len(manager.students)}")

        elif choice == "2":
            manager.show_student_list()
            student_id = ask_id("Enter student ID from the list (e.g. S002): ")
            student = manager.find_student(student_id)
            if student is None:
                print(f"No student found with ID {student_id}.")
                continue
            subject = ask_choice("Select module:", ExamResult.MODULES)
            mark = ask_mark("Enter mark (0-100): ")
            if student.find_result(subject) is not None:
                print(f"Note: the old {subject} mark will be replaced.")
            manager.record_result(student_id, subject, mark)
            print(f"Result saved: {subject} = {mark}.")

        elif choice == "3":
            manager.display_all()

        elif choice == "4":
            manager.show_student_list()
            student_id = ask_id("Enter student ID to search: ")
            student = manager.find_student(student_id)
            if student is None:
                print(f"No student found with ID {student_id}.")
            else:
                student.display_info()

        elif choice == "5":
            manager.show_student_list()
            student_id = ask_id("Enter student ID: ")
            student = manager.find_student(student_id)
            if student is None:
                print(f"No student found with ID {student_id}.")
                continue
            if len(student.results) == 0:
                print(f"{student.full_name()} has no results to update yet.")
                continue
            subject = ask_choice("Select module to update:", [result.subject for result in student.results])
            new_mark = ask_mark("Enter new mark (0-100): ")
            student.update_result(subject, new_mark)
            print(f"Updated: {subject} is now {new_mark}.")

        elif choice == "6":
            manager.summary()

        elif choice == "7":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number from 1 to 7.")


if __name__ == "__main__":
    main()