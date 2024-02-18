import psycopg2

class DatabaseHandler:
    def __init__(self, host: str, port: str, database: str, user: str, password: str):
        self.conn = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password
        )

        self.cursor = self.conn.cursor()

        self.cursor.execute("CREATE TABLE IF NOT EXISTS students (\
                        student_id SERIAL PRIMARY KEY,\
                        student_name VARCHAR(255) NOT NULL)")

        self.cursor.execute("CREATE TABLE IF NOT EXISTS courses (\
                        course_id SERIAL PRIMARY KEY,\
                        course_name VARCHAR(255) NOT NULL)")

        self.cursor.execute("CREATE TABLE IF NOT EXISTS enrollments (\
                        enrollment_id SERIAL PRIMARY KEY,\
                        enrollment_date DATE NOT NULL,\
                        student_id INT NOT NULL,\
                        course_id INT NOT NULL,\
                        FOREIGN KEY (student_id) REFERENCES students(student_id),\
                        FOREIGN KEY (course_id) REFERENCES courses(course_id))")
        
    def populate_students(self, students: list):
        for student in students:
            self.cursor.execute("INSERT INTO students (student_name) VALUES (%s)", (student,))
        self.conn.commit()

    def populate_courses(self, courses: list):
        for course in courses:
            self.cursor.execute("INSERT INTO courses (course_name) VALUES (%s)", (course,))
        self.conn.commit()

    def populate_enrollments(self, enrollments: list):
        for enrollment in enrollments:
            student_id, course_id, enrollment_date = enrollment
            self.cursor.execute("INSERT INTO enrollments (student_id, course_id, enrollment_date) VALUES (%s, %s, %s)",
                                (student_id, course_id, enrollment_date))
        self.conn.commit()

    def get_student_courses(self) -> list:
        self.cursor.execute("SELECT students.student_name, COALESCE(courses.course_name, 'Not enrolled') \
                             FROM students \
                             LEFT JOIN enrollments ON students.student_id = enrollments.student_id \
                             LEFT JOIN courses ON enrollments.course_id = courses.course_id;")
        
        result = self.cursor.fetchall()

        return result