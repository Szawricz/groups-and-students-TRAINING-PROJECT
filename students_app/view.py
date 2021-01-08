from json import dumps

from flask import Flask
from flask_restful import Api, Resource, reqparse
from sqlalchemy import func
from models import CourseModel, GroupModel, StudentModel, session

JSON_DUMPS_PARAMS = dict(
            indent=4,
            separators=[', ', ' = '],
            ensure_ascii=False,
)

app = Flask(__name__)  # Init the flask application
api = Api(app, prefix='/api/v1.0')


parser = reqparse.RequestParser()
parser.add_argument('first_name', type=str)
parser.add_argument('last_name', type=str)
parser.add_argument('volume', type=int)
parser.add_argument('course_name', type=str)


class Students(Resource):
    def get(self):
        students = {}
        for student in session.query(StudentModel).all():
            students[student.id] = dict(
                id=student.id,
                first_name=student.first_name,
                last_name=student.last_name,
                group_id=student.group_id,
                courses=[course.name for course in student.courses],
            )
        return dumps(students, **JSON_DUMPS_PARAMS)

    # Add new student
    def post(self):
        args = parser.parse_args()
        first_name = args['first_name']
        last_name = args['last_name']
        session.add(StudentModel(None, first_name, last_name))
        session.commit()
        return {'mesage': f'{first_name} {last_name} added.'}

    # Delete student by STUDENT_ID
    def delete(self, student_id: int):
        session.delete(
            session.query(
                StudentModel).filter(StudentModel.id == student_id).one())
        session.commit()
        return {'mesage': f'Student with the ID = {student_id} deleted.'}


class Groups(Resource):
    def get(self):
        groups = {}
        for group in session.query(GroupModel).all():
            students = {}
            for student in session.query(
                    StudentModel).filter(StudentModel.group_id == group.name):
                students[student.id] = dict(
                    id=student.id,
                    name=f'{student.first_name} {student.last_name}',
                )
            groups[group.name] = dict(
                id=group.id,
                name=group.name,
                volume=len(students),
                students=students,
            )
        return dumps(groups, **JSON_DUMPS_PARAMS)

    # Find all groups with less or equals student count
    def post(self):
        args = parser.parse_args()
        volume = args['volume']
        groups = {}
        for group in session.query(GroupModel).\
            outerjoin(StudentModel, GroupModel.name == StudentModel.group_id).\
                group_by(GroupModel.id, GroupModel.name).\
                    having(func.count(GroupModel.name) <= volume).all():
            groups[group.name] = dict(
                id=group.id,
                name=group.name,
            )
        return dumps(groups, **JSON_DUMPS_PARAMS)


class StudentsOnCourse(Resource):
    # Find all students related to the course with a given name.
    def get(self):
        args = parser.parse_args()
        course_name = args['course_name']
        students = {}
        for student in session.query(StudentModel).\
            select_from(CourseModel).\
                join(StudentModel.courses).\
                    filter(CourseModel.name == course_name):
            students[student.id] = dict(
                id=student.id,
                first_name=student.first_name,
                last_name=student.last_name,
                group_id=student.group_id,
            )
        return dumps(students, **JSON_DUMPS_PARAMS)

    # Add a student to the course (from a list)
    def put(self, student_id: int):
        args = parser.parse_args()
        course_name = args['course_name']
        course = session.query(
            CourseModel).filter(CourseModel.name == course_name).one()
        student = session.query(
            StudentModel).filter(StudentModel.id == student_id).one()
        student.courses.append(course)
        session.commit()
        return {'mesage': f'Student with the ID = {student_id} added to the {course_name} course.'}

    # Remove the student from one of his or her courses
    def delete(self, student_id: int):
        args = parser.parse_args()
        course_name = args['course_name']
        course = session.query(
            CourseModel).filter(CourseModel.name == course_name).one()
        student = session.query(
            StudentModel).filter(StudentModel.id == student_id).one()
        student.courses.remove(course)
        session.commit()
        return {'mesage': f'Student with the ID = {student_id} removed from the {course_name} course.'}


api.add_resource(
    Students,
    '/students/',
    methods=['GET', 'POST'],
    endpoint='students',
    )
api.add_resource(
    Students,
    '/students/<student_id>',
    methods=['DELETE'],
    endpoint='student',
    )
api.add_resource(Groups, '/groups/', methods=['GET', 'POST'])
api.add_resource(StudentsOnCourse, '/course/', methods=['GET'])
api.add_resource(
    StudentsOnCourse,
    '/students/<student_id>/course/',
    methods=['PUT', 'DELETE'],
    endpoint='student_on_course',
    )


if __name__ == '__main__':
    app.run()
