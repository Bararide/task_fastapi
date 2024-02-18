from db_handler import DatabaseHandler

def main():
    db_handler = DatabaseHandler(host='', port='', database='', user='', password='')

    students = ['John Doe', 'Jane Smith', 'Michael Johnson']
    db_handler.populate_students(students)

    courses = ['Math', 'Science', 'English']
    db_handler.populate_courses(courses)

    enrollments = [
        (1, 1, '2022-01-01'),
        (1, 2, '2022-02-15'),
        (2, 3, '2022-03-10')
    ]
    db_handler.populate_enrollments(enrollments)

    student_courses = db_handler.get_student_courses()
    print(student_courses)

if __name__ == '__main__':
    main()
