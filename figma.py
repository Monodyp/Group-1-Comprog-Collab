SUBJECTS = [
    "Integral Calculus", "Physics", "Computer Programming", "Art Appreciation",
    "Science, Technology, and Society", "The Contemporary World",
    "Engineering Drawing", "PE"
]

def display_grading_scale():
    print("\nCollege Grading System:")
    print("------------------------")
    print("1.00 - Excellent")
    print("1.25 - Very Good")
    print("1.50 - Very Good")
    print("1.75 - Good")
    print("2.00 - Good")
    print("2.25 - Satisfactory")
    print("2.50 - Satisfactory")
    print("2.75 - Passing")
    print("3.00 - Passing")
    print("5.00 - Failed")

def add_student(students, name):
    if name not in students:
        students[name] = {}
        print(f"\nStudent {name} added successfully!")
    else:
        print(f"\nStudent {name} already exists.")

def delete_student(students, name):
    if name in students:
        del students[name]
        print(f"\nStudent {name} has been deleted.")
    else:
        print(f"\nStudent {name} not found.")

def generate_remarks(college_grade):
    if college_grade == 1.00:
        return "Excellent"
    elif college_grade in (1.25, 1.50):
        return "Very Good"
    elif college_grade in (1.75, 2.00):
        return "Good"
    elif college_grade in (2.25, 2.50):
        return "Satisfactory"
    elif college_grade in (2.75, 3.00):
        return "Passing"
    else:
        return "Failing"

def convert_percent_to_college_grade(final_grade_percent):
    if final_grade_percent >= 97:
        return 1.00
    elif final_grade_percent >= 94:
        return 1.25
    elif final_grade_percent >= 91:
        return 1.50
    elif final_grade_percent >= 88:
        return 1.75
    elif final_grade_percent >= 85:
        return 2.00
    elif final_grade_percent >= 82:
        return 2.25
    elif final_grade_percent >= 79:
        return 2.50
    elif final_grade_percent >= 76:
        return 2.75
    elif final_grade_percent >= 75:
        return 3.00
    else:
        return 5.00

def add_subject_info(students, name, semester, subject_index, grade, attendance):
    subject = SUBJECTS[subject_index]
    if name not in students:
        print("\nStudent not found.")
        return

    if semester not in students[name]:
        students[name][semester] = {}

    college_grade = convert_percent_to_college_grade(grade)
    remarks = generate_remarks(college_grade)

    students[name][semester][subject] = {
        'grade': grade,
        'attendance': attendance,
        'college_grade': college_grade,
        'remarks': remarks
    }

    print(f"\nSubject '{subject}' info added to {name}.")

def delete_subject(students, name, semester, subject_index):
    subject = SUBJECTS[subject_index]
    if name in students and semester in students[name]:
        if subject in students[name][semester]:
            del students[name][semester][subject]
            print(f"\nSubject '{subject}' has been deleted from {name}'s record.")
        else:
            print(f"\nSubject '{subject}' not found for {name} in {semester}.")
    else:
        print("\nStudent or semester not found.")

def update_subject_info(students, name, semester, subject_index, new_grade, new_attendance):
    if name in students and semester in students[name]:
        subject = SUBJECTS[subject_index]
        if subject in students[name][semester]:
            new_grade = float(new_grade)
            college_grade = convert_percent_to_college_grade(new_grade)
            remarks = generate_remarks(college_grade)

            students[name][semester][subject] = {
                'grade': new_grade,
                'attendance': new_attendance,
                'college_grade': college_grade,
                'remarks': remarks
            }
            print(f"\nSubject {subject} info updated for {name}.")
        else:
            print(f"\nSubject {subject} not found for {name} in {semester}.")
    else:
        print("\nStudent or semester not found.")

def view_student(students, name):
    if name in students:
        print(f"\nPerformance for {name}:")
        if not students[name]:
            print("\nNo semesters or subjects recorded yet.")
        else:
            total_grade = 0
            subject_count = 0

            for semester, subjects in students[name].items():
                print(f"\n  Semester: {semester}")
                for subject, info in subjects.items():
                    try:
                        grade = float(info['grade'])
                        total_grade += grade
                        subject_count += 1
                    except ValueError:
                        print(f"\nInvalid grade for subject '{subject}'.")
                        continue

                    print(f"   Subject: {subject}")
                    print(f"     Grade: {info['grade']}%")
                    print(f"College Grade: {info['college_grade']}")
                    print(f"Attendance: {info['attendance']}")
                    print(f"   Remarks: {info['remarks']}")
                    print("-" * 35)

            if subject_count > 0:
                avg = total_grade / subject_count
                print(f"\nAverage Grade across all subjects: {avg:.2f}")
            else:
                print("\nNo valid grades to compute an average.")
    else:
        print(f"\nStudent {name} not found.")

def search_student_by_name(students, keyword):
    matches = [name for name in students if keyword.lower() in name.lower()]
    if matches:
        print("\nMatching Students:")
        for name in matches:
            print(f" - {name}")
    else:
        print("\nNo matching students found.")

def view_top_performers(students):
    top_students = []

    for name, semesters in students.items():
        total = 0
        count = 0
        for subjects in semesters.values():
            for info in subjects.values():
                try:
                    total += float(info['grade'])
                    count += 1
                except ValueError:
                    continue
        if count > 0:
            avg = total / count
            if avg >= 90:
                top_students.append((name, avg))

    if top_students:
        print("\nTop Performers (With an Average of 90 and above):")
        for name, avg in sorted(top_students, key=lambda x: x[1], reverse=True):
            print(f" - {name}: {avg:.2f}")
    else:
        print("\nNo students have an average of 90 or above.")

def main():
    students = {}

    while True:
        print("\nWelcome to the Student Performance Tracker!")
        print("Please choose an option:")
        print("1. Add Student")
        print("2. Add Subject Grade and Attendance")
        print("3. Delete Student")
        print("4. Delete Subject from Student")
        print("5. View Student Performance")
        print("6. View Top Performer")
        print("7. View Grading System")
        print("8. Update Subject Info")
        print("9. Search Student by Name")
        print("10. Exit")
        option = input("\nEnter your choice (1-10): ").strip()

        if option == '1':
            name = input("\nEnter student name: ").strip()
            add_student(students, name)

        elif option == '2':
            name = input("\nEnter student name: ").strip()
            semester = input("\nEnter semester (Semester 1 or 2): ").strip()

            print("\nAvailable Subjects:")
            for i, subject in enumerate(SUBJECTS):
                print(f"{i + 1}. {subject}")

            try:
                subject_choice = int(input("\nEnter subject number: ")) - 1
                grade = float(input("\nEnter grade (percent): "))
                attendance = input("\nEnter attendance count: ")
                add_subject_info(students, name, semester, subject_choice, grade, attendance)
            except ValueError:
                print("\nInvalid input. Please enter proper values.")

        elif option == '3':
            name = input("\nEnter student name to delete: ").strip()
            delete_student(students, name)

        elif option == '4':
            name = input("\nEnter student name: ").strip()
            semester = input("\nEnter semester: ").strip()

            print("\nAvailable Subjects:")
            for i, subject in enumerate(SUBJECTS):
                print(f"{i + 1}. {subject}")

            try:
                subject_choice = int(input("\nEnter subject number to delete: ")) - 1
                delete_subject(students, name, semester, subject_choice)
            except ValueError:
                print("\nInvalid input.")
        
        elif option == '5':
            name = input("\nEnter student name: ").strip()
            view_student(students, name)

        elif option == '6':
            view_top_performers(students)

        elif option == '7':
            display_grading_scale()
        
        elif option == '8':
            name = input("\nEnter student name: ").strip()
            semester = input("\nEnter semester: ").strip()

            print("\nAvailable Subjects:")
            for i, subject in enumerate(SUBJECTS):
                print(f"{i + 1}. {subject}")

            try:
                subject_choice = int(input("\nEnter subject number to update: ")) - 1
                grade = float(input("\nEnter new grade (percent): "))
                attendance = input("\nEnter new attendance: ")
                update_subject_info(students, name, semester, subject_choice, grade, attendance)
            except ValueError:
                print("\nInvalid input.")

        elif option == '9':
            keyword = input("\nEnter part of the student name to search: ").strip()
            search_student_by_name(students, keyword)

        elif option == '10':
            print("\nThank you for using the Student Performance Tracker!")
            break

        else:
            print("\nInvalid choice. Please try again.")

main()