from student_server import get_report_card, get_student_details, get_student_marks, get_student_result

while True:
    print("\nStudent Management System")
    print("1. Get Student Details")
    print("2. Get Student Marks")
    print("3. Get Student Result")
    print("4. Get Student Report Card")
    print("5. Exit")

    choice = input("Enter your choice (1-5): ")

    if choice == "1":
        student_id = input("Enter student ID: ")
        result = get_student_details(student_id)
        print(result)

    elif choice == "2":
        student_id = input("Enter student ID: ")
        result = get_student_marks(student_id)
        print(result)

    elif choice == "3":
        student_id = input("Enter student ID: ")
        result = get_student_result(student_id)
        print(result)

    elif choice == "4":
        student_id = input("Enter student ID: ")
        result = get_report_card(student_id)
        print(result)

    elif choice == "5":
        print("Exiting...")
        break

    else:
        print("Invalid choice. Please try again.")