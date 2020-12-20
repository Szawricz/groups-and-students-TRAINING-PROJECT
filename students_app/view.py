from flask import Flask, render_template, request

from models import get_courses, get_groups, get_students, add_student, delete_student

app = Flask(__name__)  # Init the flask application


@app.route('/', methods=['GET'])
@app.route('/students/', methods=['GET'])
def show_students():
    data = get_students()
    return render_template('students.html', data=data)


@app.route('/courses/', methods=['GET'])
def show_courses():
    data = get_courses()
    return render_template('courses.html', data=data)


@app.route('/groups/', methods=['GET'])
def show_groups():
    data = get_groups()
    return render_template('groups.html', data=data)



# Add new student
@app.route('/students/add/', methods=['GET'])
def add_new_student():
    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')
    add_student(first_name, last_name)
    return show_students()

# Delete student by STUDENT_ID
@app.route('/students/delete/', methods=['GET'])
def delete_student_by_id():
    student_id = request.args.get('id')
    delete_student(student_id)
    return show_students()

# Remove the student from one of his or her courses
def delete_student_by_id(student_id: int, course_name: str):
    pass



# Find all groups with less or equals student count.
def find_groups_with_le_wolume(volume: int):
    pass

# Find all students related to the course with a given name.
def finnd_group_students(group_name: str):
    pass

# Add a student to the course (from a list)
def add_student_to_course(student_id: int, course_name: str):
    pass


if __name__ == '__main__':
    app.run()
