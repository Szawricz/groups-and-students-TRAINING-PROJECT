from flask import Flask
from flask_restful import Api, Resource, reqparse
from json import dumps

from models import CourseModel, GroupModel, StudentModel, session

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
        return students

    def post(self):
        args = parser.parse_args()
        first_name = args['first_name']
        last_name = args['last_name']
        session.add(StudentModel(None, first_name, last_name))
        session.commit()
        return {'mesage': f'{first_name} {last_name} added.'}

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
        return groups

    def post(self):
        args = parser.parse_args()
        volume = args['volume']
        groups = {}
        for key, value in self.get().items():
            if value['volume'] <= volume:
                groups[key] = value
        return groups


class StudentsOnCourse(Resource):
    def get(self):
        args = parser.parse_args()
        course_name = args['course_name']
        students = {}
        for key, value in Students.get().items():
            if course_name in value['courses']:
                students[key] = value
        return students

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


api.add_resource(Students, '/students/', methods=['GET', 'POST'], endpoint='students')
api.add_resource(Students, '/students/<student_id>', methods=['DELETE'], endpoint='student')
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
