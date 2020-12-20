from flask import Flask, render_template, request
from models import Session, engine, StudentModel, CourseModel, get_students

app = Flask(__name__)  # Init the flask application



@app.route('/', methods=['GET'])
@app.route('/students/', methods=['GET'])
def show_students():
    return render_template('students.html', students=get_students())


@app.route('/courses/', methods=['GET'])
def show_courses():
    return render_template('groups.html')


@app.route('/groups/', methods=['GET'])
def show_groups():
    return render_template('courses.html')



# Find all groups with less or equals student count.
def find_groups_with_le_wolume(volume: int):
    pass
# Find all students related to the course with a given name.
def finnd_group_students(group_name: str):
    pass
# Add new student
def add_new_student(first_name: str, last_name: str):
    pass
# Delete student by STUDENT_ID
def delete_student_by_id(student_id: int):
    pass
# Add a student to the course (from a list)
def add_student_to_course(student_id: int, course_name: str):
    pass
# Remove the student from one of his or her courses
def delete_student_by_id(student_id: int, course_name: str):
    pass