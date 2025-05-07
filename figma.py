import os
import sys
import time
from colorama import init, Fore, Style

# Initialize Colorama
init(autoreset=True, convert=True)

BORDER_THICKNESS_SIDE = 3
BORDER_THICKNESS_TOP_BOTTOM = 2  # thinner top/bottom border
PADDING = 1  # space between border and content

# Dark green RGB color escape sequence
DARK_GREEN = '\033[90'

TITLE_COLOR = Fore.LIGHTCYAN_EX
TEXT_COLOR = Fore.LIGHTWHITE_EX
HIGHLIGHT_COLOR = Fore.LIGHTYELLOW_EX
ERROR_COLOR = Fore.LIGHTRED_EX

BORDER_STYLES = {
    'main': {'top': '═', 'side': '║', 'tl': '╔', 'tr': '╗', 'bl': '╚', 'br': '╝'},
    'add': {'top': '━', 'side': '┃', 'tl': '┏', 'tr': '┓', 'bl': '┗', 'br': '┛'},
    'delete': {'top': '─', 'side': '│', 'tl': '┌', 'tr': '┐', 'bl': '└', 'br': '┘'},
    'view': {'top': '═', 'side': '║', 'tl': '╒', 'tr': '╕', 'bl': '╘', 'br': '╛'},
    'grading': {'top': '─', 'side': '│', 'tl': '╭', 'tr': '╮', 'bl': '╰', 'br': '╯'}
}

TITLE = " STEP PROGRAM "

ASCII_ART = [
    ".·:'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''':·.",
    ": : ███████╗████████╗███████╗██████╗     ██████╗ ██████╗  ██████╗  ██████╗ ██████╗  █████╗ ███╗   ███╗ : :",
    ": : ██╔════╝╚══██╔══╝██╔════╝██╔══██╗    ██╔══██╗██╔══██╗██╔═══██╗██╔════╝ ██╔══██╗██╔══██╗████╗ ████║ : :",
    ": : ███████╗   ██║   █████╗  ██████╔╝    ██████╔╝██████╔╝██║   ██║██║  ███╗██████╔╝███████║██╔████╔██║ : :",
    ": : ╚════██║   ██║   ██╔══╝  ██╔═══╝     ██╔═══╝ ██╔══██╗██║   ██║██║   ██║██╔══██╗██╔══██║██║╚██╔╝██║ : :",
    ": : ███████║   ██║   ███████╗██║         ██║     ██║  ██║╚██████╔╝╚██████╔╝██║  ██║██║  ██║██║ ╚═╝ ██║ : :",
    ": : ╚══════╝   ╚═╝   ╚══════╝╚═╝         ╚═╝     ╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝ : :",
    "'·:....................................................................................................:·'"
]

SUBJECTS = [
    "Integral Calculus", "Physics", "Computer Programming", "Art Appreciation",
    "Science, Technology, and Society", "The Contemporary World",
    "Engineering Drawing", "PE"
]

def rotating_animation(duration=2, message="Processing"):
    animation_chars = "|/-\\"
    original_message = message
    message_length = len(original_message)
    start_time = time.time()
    end_time = start_time + duration
    wave_position = 0
    
    while time.time() < end_time:
        # Create a new animated message each frame
        current_frame = []
        for i, char in enumerate(original_message):
            if char.isalpha():
                # Calculate distance from wave position (with wrap-around)
                distance = min(
                    abs(i - wave_position),
                    abs(i - (wave_position + message_length)),
                    abs(i - (wave_position - message_length))
                )
                # Highlight characters near the wave
                if distance <= 3:
                    current_frame.append(char.upper())
                else:
                    current_frame.append(char.lower())
            else:
                current_frame.append(char)  # Non-alphabetic characters unchanged
        
        # Get current spinner character
        spinner_char = animation_chars[int((time.time() - start_time) * 8) % 4]
        
        # Display the frame
        sys.stdout.write(f"\r{''.join(current_frame)} {spinner_char}")
        sys.stdout.flush()
        
        # Move the wave forward
        wave_position = (wave_position + 2) % message_length  # Slower, smoother movement
        time.sleep(0.08)
    
    # Clean up the line when done
    sys.stdout.write("\r" + " " * (message_length + 2) + "\r")
    sys.stdout.flush()

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def strip_ansi(text):
    import re
    ansi_escape = re.compile(r'\x1b\[([0-9;]+)m')
    return ansi_escape.sub('', text)

def typewriter_print(text, delay=0.0005):
    i = 0
    while i < len(text):
        if text[i] == '\033':  # ANSI escape sequence
            end = i + 1
            while end < len(text) and text[end] != 'm':
                end += 1
            end = min(end + 1, len(text))
            sys.stdout.write(text[i:end])
            sys.stdout.flush()
            i = end
        else:
            sys.stdout.write(text[i])
            sys.stdout.flush()
            time.sleep(delay)
            i += 1

def wait_for_keypress(prompt="Press any key to continue..."):
    typewriter_print(HIGHLIGHT_COLOR + Style.DIM + "\n" + prompt, delay=0.01)
    if os.name == 'nt':
        import msvcrt
        msvcrt.getch()
    else:
        import tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def build_frame_dimensions(content_lines):
    max_content_width = max(len(strip_ansi(line)) for line in content_lines)
    width = max_content_width + 2 * (max(BORDER_THICKNESS_SIDE, BORDER_THICKNESS_TOP_BOTTOM) + PADDING)
    height = len(content_lines) + 2 * (max(BORDER_THICKNESS_SIDE, BORDER_THICKNESS_TOP_BOTTOM) + PADDING)
    return width, height

def draw_solid_border_with_typewriter(content_lines, title=None, border_color=DARK_GREEN):
    width, height = build_frame_dimensions(content_lines)
    inner_width = width - 2 * BORDER_THICKNESS_SIDE
    inner_height = height - 2 * BORDER_THICKNESS_TOP_BOTTOM

    # Full-width decorations
    top_decoration = border_color + '╔' + '═' * (width - 2) + '╗' + Style.RESET_ALL
    bottom_decoration = border_color + '╚' + '═' * (width - 2) + '╝' + Style.RESET_ALL

    # Top border (2 lines)
    for i in range(BORDER_THICKNESS_TOP_BOTTOM):
        if i == BORDER_THICKNESS_TOP_BOTTOM - 1:
            print(top_decoration)
        else:
            print(border_color + '█' * width + Style.RESET_ALL)

    # Middle rows with vertical borders and content
    content_start_row = BORDER_THICKNESS_TOP_BOTTOM + PADDING
    content_end_row = content_start_row + len(content_lines)
    middle_row = (height - BORDER_THICKNESS_TOP_BOTTOM) // 2

    for row in range(BORDER_THICKNESS_TOP_BOTTOM, height - BORDER_THICKNESS_TOP_BOTTOM):
        # Left and right border: use '║' in the middle row, else solid
        if row == middle_row:
            left_border = border_color + '║' + '█' * (BORDER_THICKNESS_SIDE - 1) + Style.RESET_ALL
            right_border = border_color + '█' * (BORDER_THICKNESS_SIDE - 1) + '║' + Style.RESET_ALL
        else:
            left_border = border_color + '█' * BORDER_THICKNESS_SIDE + Style.RESET_ALL
            right_border = border_color + '█' * BORDER_THICKNESS_SIDE + Style.RESET_ALL

        if content_start_row <= row < content_end_row:
            content_line = content_lines[row - content_start_row]
            clean_line = strip_ansi(content_line)
            padding_left = (inner_width - len(clean_line)) // 2
            padding_right = inner_width - len(clean_line) - padding_left

            # Print left padding spaces
            sys.stdout.write(left_border + ' ' * padding_left)
            sys.stdout.flush()
            typewriter_print(content_line)
            sys.stdout.write(' ' * padding_right + right_border + '\n')
            sys.stdout.flush()
        else:
            print(left_border + ' ' * inner_width + right_border)

    # Bottom border (2 lines)
    for i in range(BORDER_THICKNESS_TOP_BOTTOM):
        if i == 0:
            print(bottom_decoration)
        else:
            print(border_color + '█' * width + Style.RESET_ALL)

def display_grading_scale():
    clear_console()
    rotating_animation(2, "Loading up...")
    clear_console()
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
    time.sleep(5)

def add_student(students, name):
    clear_console()
    rotating_animation(2, "Checking...")
    clear_console()
    if name not in students:
        clear_console()
        rotating_animation(2, f"Adding {name} to the list...")
        clear_console()
        students[name] = {}
        print(f"\n{name} has been added successfully!")
        time.sleep(2)
    else:
        print(f"\n{name} already exists. ")
        time.sleep(2)

def add_subject_grade_and_attendance():
    name = input("\nEnter student name: ").strip()
    semester = input("\nEnter semester (Semester 1 or 2): ").strip()
    print("\nAvailable Subjects:")
    for i, subject in enumerate(SUBJECTS):
                print(f"{i + 1}. {subject}")
                print("\nInvalid input. Please enter proper values.")
                time.sleep(2)

def delete_student(students, name):
    clear_console()
    rotating_animation(2, "Checking...")
    clear_console()
    if name in students:
        clear_console()
        rotating_animation(2, f"Removing {name} from the list...")
        clear_console()
        del students[name]
        print(f"\nStudent {name} has been deleted.")
        time.sleep(2)
    else:
        print(f"\nStudent {name} not found.")
        time.sleep(2)

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
    clear_console()
    rotating_animation(2, "Checking...")
    clear_console()
    if name not in students:
        print("\nStudent not found.")
        time.sleep(2)
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
    clear_console()
    rotating_animation(2, f"Adding {subject} to {name}'s curriculum...")
    clear_console()
    print(f"\nSubject '{subject}' info added to {name}.")
    time.sleep(2)

def delete_subject(students, name, semester, subject_index):
    subject = SUBJECTS[subject_index]
    clear_console()
    rotating_animation(2, "Checking...")
    clear_console()
    if name in students and semester in students[name]:
        if subject in students[name][semester]:
            clear_console()
            rotating_animation(2, "Removing Subject...")
            clear_console()
            del students[name][semester][subject]
            print(f"\nSubject '{subject}' has been deleted from {name}'s record.")
            time.sleep(2)
        else:
            print(f"\nSubject '{subject}' not found for {name} in {semester}.")
            time.sleep(2)
    else:
        print("\nStudent or semester not found.")
        time.sleep(2)

def update_subject_info(students, name, semester, subject_index, new_grade, new_attendance):
    clear_console()
    rotating_animation(2, "Checking...")
    clear_console()
    if name in students and semester in students[name]:
        subject = SUBJECTS[subject_index]
        if subject in students[name][semester]:
            clear_console()
            rotating_animation(2, "Adding new subject info...")
            clear_console()
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
            time.sleep(2)
        else:
            print(f"\nSubject {subject} not found for {name} in {semester}.")
            time.sleep(2)
    else:
        print("\nStudent or semester not found.")
        time.sleep(2)

def view_student(students, name):
    clear_console()
    rotating_animation(2, "Checking...")
    clear_console()
    if name in students:
        clear_console()
        rotating_animation(2, f"Loading up {name}'s performance...")
        clear_console()
        print(f"\nPerformance for {name}:")
        time.sleep(2)
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
                    time.sleep(2)

            if subject_count > 0:
                avg = total_grade / subject_count
                print(f"\nAverage Grade across all subjects: {avg:.2f}")
                time.sleep(2)
            else:
                print("\nNo valid grades to compute an average.")
                time.sleep(2)
    else:
        print(f"\nStudent {name} not found.")
        time.sleep(5)

def search_student_by_name(students, keyword):
    clear_console()
    rotating_animation(2, "Checking...")
    clear_console()
    matches = [name for name in students if keyword.lower() in name.lower()]
    if matches:
        clear_console()
        rotating_animation(2, "Pulling up Matches...")
        clear_console()
        print("\nMatching Students:")
        for name in matches:
            print(f" - {name}")
            time.sleep(2)
    else:
        print("\nNo matching students found.")
        time.sleep(2)

def view_top_performers(students):
    clear_console()
    rotating_animation(2, "Checking...")
    clear_console()
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
        clear_console()
        rotating_animation(2, "Loading up top students...")
        clear_console()
        print("\nTop Performers (With an Average of 90 and above):")
        for name, avg in sorted(top_students, key=lambda x: x[1], reverse=True):
            print(f" - {name}: {avg:.2f}")
            time.sleep(5)
    else:
        print("\nNo students have an average of 90 or above.")
        time.sleep(5)

def exit_program():
    clear_console()
    typewriter_print(ERROR_COLOR + Style.BRIGHT + "\nExiting program...\n", delay=0.01)

def show_start_menu():
    clear_console()
    rotating_animation(2, "Booting Up the Step Program...")
    # Celtic line decorations
    celtic_line = "⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯"
    subtext = "Student Tracker For Engineering Performance"

    # Combine ASCII art + celtic lines + subtext
    content_lines = ASCII_ART.copy()
    content_lines.append('')  # spacing
    content_lines.append(celtic_line)
    content_lines.append(subtext)
    content_lines.append(celtic_line)

    width, height = build_frame_dimensions(content_lines)
    inner_width = width - 2 * BORDER_THICKNESS_SIDE

    # Center all lines horizontally inside inner width
    typed_lines = []
    for line in content_lines:
        clean_line = strip_ansi(line)
        padding_left = (inner_width - len(clean_line)) // 2
        padding_right = inner_width - len(clean_line) - padding_left
        typed_lines.append(' ' * padding_left + line + ' ' * padding_right)

    draw_solid_border_with_typewriter(typed_lines, title=TITLE, border_color=DARK_GREEN)

    wait_for_keypress()

#Transition effect
    # Retro transition effect
    clear_console()
    rotating_animation(2, "Loading the Main Menu...")

def show_main_menu():
    clear_console()

    menu_lines = [
        TEXT_COLOR + Style.BRIGHT + "╔═════════════════════════════════════╗",
        TEXT_COLOR + "║ " + Fore.CYAN + "1. Add New Student                 " + TEXT_COLOR + " ║",
        TEXT_COLOR + "║ " + Fore.CYAN + "2. Add Subject Grade and Attendance" + TEXT_COLOR + " ║",
        TEXT_COLOR + "║ " + Fore.CYAN + "3. Delete Student                  " + TEXT_COLOR + " ║",
        TEXT_COLOR + "║ " + Fore.CYAN + "4. Delete Subject from Student     " + TEXT_COLOR + " ║",
        TEXT_COLOR + "║ " + Fore.CYAN + "5. View Student Performance        " + TEXT_COLOR + " ║",
        TEXT_COLOR + "║ " + Fore.CYAN + "6. View Top Performer              " + TEXT_COLOR + " ║",
        TEXT_COLOR + "║ " + Fore.CYAN + "7. View Grading System             " + TEXT_COLOR + " ║",
        TEXT_COLOR + "║ " + Fore.CYAN + "8. Update Subject Info             " + TEXT_COLOR + " ║",
        TEXT_COLOR + "║ " + Fore.CYAN + "9. Search Student by Name          " + TEXT_COLOR + " ║",
        TEXT_COLOR + "║ " + Fore.RED +  "0. Exit Program                    " + TEXT_COLOR + " ║",
        TEXT_COLOR + "╚═════════════════════════════════════╝"
    ]

    width, height = build_frame_dimensions(menu_lines)
    inner_width = width - 2 * BORDER_THICKNESS_SIDE

    typed_lines = []
    for line in menu_lines:
        clean_line = strip_ansi(line)
        padding_left = (inner_width - len(clean_line)) // 2
        padding_right = inner_width - len(clean_line) - padding_left
        typed_lines.append(' ' * padding_left + line + ' ' * padding_right)

    draw_solid_border_with_typewriter(typed_lines, title=" MAIN MENU ", border_color=DARK_GREEN)

    while True:
        try:
            typewriter_print(HIGHLIGHT_COLOR + "\nSelect an option (0-9): ", delay=0.01)
            choice = int(input())
            if 0 <= choice <= 9:
                return choice
            typewriter_print(ERROR_COLOR + "Invalid selection! Please choose 1-5", delay=0.01)
        except ValueError:
            typewriter_print(ERROR_COLOR + "Please enter a number!", delay=0.01)

def draw_dynamic_border(content_lines, title=None, border_style='main'):
    width, height = build_frame_dimensions(content_lines)
    style = BORDER_STYLES.get(border_style, BORDER_STYLES['main'])
    
    # Top border
    top_border = style['tl'] + style['top'] * (width - 2) + style['tr']
    print(DARK_GREEN + top_border)
    
    # Content area
    inner_width = width - 2 * BORDER_THICKNESS_SIDE
    for line in content_lines:
        clean_line = strip_ansi(line)
        padding = (inner_width - len(clean_line)) // 2
        centered_line = ' ' * padding + line + ' ' * (inner_width - len(clean_line) - padding)
        print(DARK_GREEN + style['side'] + ' ' * BORDER_THICKNESS_SIDE + 
              Style.RESET_ALL + centered_line + 
              DARK_GREEN + ' ' * BORDER_THICKNESS_SIDE + style['side'])
        
     # Bottom border
    bottom_border = style['bl'] + style['top'] * (width - 2) + style['br']
    print(DARK_GREEN + bottom_border)

def main():
    students = {}
    show_start_menu()
    while True:
        choice = show_main_menu()

        if choice == 1:
            clear_console()
            rotating_animation(2, "Preparing to add a student...")
            clear_console()
            draw_dynamic_border(["ADD NEW STUDENT"], border_style='add')
            name = input("\nEnter student name: ").strip()
            add_student(students, name)
        elif choice == 2:
            clear_console()
            rotating_animation(2, "Preparing to add grades and attendance...")
            draw_dynamic_border(["ADD YOUR SUBJECT GRADE AND ATTENDANCE"], border_style='add')
            name = input("\nEnter student name: ").strip()
            semester = input("\nEnter semester (Semester 1 or 2): ").strip()
            clear_console()
            rotating_animation(2, f"Getting list of {name}'s curriculum ")
            clear_console()
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
        elif choice == 3:
            clear_console()
            rotating_animation(2, "Let's go ahead and delete a student...")
            clear_console()
            name = input("\nEnter student name: ").strip()
            delete_student(students, name)
        elif choice == 4:
            clear_console()
            rotating_animation(2, "Let's go ahead and choose a student first...")
            name = input("\nEnter student name: ").strip()
            semester = input("\nEnter semester: ").strip()
            rotating_animation(2, f"Let's remove a subject from {name} ...")
            print("\nAvailable Subjects:")
            for i, subject in enumerate(SUBJECTS):
                print(f"{i + 1}. {subject}")

            try:
                subject_choice = int(input("\nEnter subject number to delete: ")) - 1
                delete_subject(students, name, semester, subject_choice)
            except ValueError:
                print("\nInvalid input.")
        elif choice == 5:
            clear_console()
            rotating_animation(2, "Let's choose your student...")
            clear_console()
            name = input("\nEnter student name: ").strip()
            view_student(students, name)
        elif choice == 6:
            clear_console()
            view_top_performers(students)
        elif choice == 7:
            clear_console()
            display_grading_scale()
        elif choice == 8:
            clear_console()
            clear_console()
            rotating_animation(2, "Let's pick a student first...")
            clear_console()
            name = input("\nEnter student name: ").strip()
            semester = input("\nEnter semester: ").strip()
            clear_console()
            rotating_animation(2, f"Loading up {name}'s curriculum...")
            clear_console()
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
        elif choice == 9:
            clear_console()
            rotating_animation(2, "Let's find your student...")
            clear_console()
            keyword = input("\nEnter part of the student name to search: ").strip()
            search_student_by_name(students, keyword)
        elif choice == 0:
            clear_console()
            print("\nThank you for using the Student Performance Tracker!")
            exit_program()
            break



main()