from flask import Flask, render_template, request

from models import (add_student, delete_student, find_groups_le,
                    get_course_students, get_courses, get_groups, get_students,
                    leave_course, student_to_course)

app = Flask(__name__)  # Init the flask application


@app.route('/', methods=['GET'])
@app.route('/students/', methods=['GET'])
def show_students():
    data = get_students()
    courses = get_courses()
    return render_template('students.html', data=data, courses=courses)



@app.route('/groups/', methods=['GET'])
def show_groups():
    data = get_groups()
    return render_template('groups.html', data=data)



# Add new student
@app.route('/students/add/', methods=['POST'])
def add_new_student():
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    add_student(first_name, last_name)
    return show_students()

# Delete student by STUDENT_ID
@app.route('/students/delete/', methods=['POST'])
def delete_student_by_id():
    student_id = request.form.get('id')
    delete_student(student_id)
    return show_students()

# Remove the student from one of his or her courses
@app.route('/students/remove_from_course/', methods=['POST'])
def remove_student_from_course():
    student_id = request.form.get('student_id')
    course_name = request.form.get('course_name')
    leave_course(int(student_id), course_name)
    return show_students()

# Add a student to the course (from a list)
@app.route('/students/add/to_course/', methods=['POST'])
def add_student_to_course():
    student_id = request.form.get('student_id')
    course_name = request.form.get('course_name')
    student_to_course(student_id, course_name)
    return show_students()


# Find all groups with less or equals student count.
@app.route('/groups/find_le/', methods=['GET'])
def show_groups_with_le_wolume():
    volume = request.args.get('volume')
    data = find_groups_le(int(volume))
    return render_template('groups.html', data=data)


# Find all students related to the course with a given name.
@app.route('/students/on_course/', methods=['GET'])
def show_course_students():
    courses = get_courses()
    course_name = request.args.get('course_name')
    data = get_course_students(course_name)
    return render_template('students.html', data=data, courses=courses)


if __name__ == '__main__':
    app.run()
