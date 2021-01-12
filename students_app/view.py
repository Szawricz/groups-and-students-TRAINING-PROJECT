from flask import Flask
from flask_restful import Api, Resource, reqparse
from sqlalchemy import func
from sqlalchemy.orm.exc import NoResultFound

from models import CourseModel, GroupModel, StudentModel, session

app = Flask(__name__)  # Init the flask application
api = Api(app, prefix='/api/v1.0')


name_parser = reqparse.RequestParser(bundle_errors=True)
name_parser.add_argument('first_name', type=str, required=True)
name_parser.add_argument('last_name', type=str, required=True)

course_name_parser = reqparse.RequestParser()
course_name_parser.add_argument('course_name', type=str, required=True)

group_volume_parser = reqparse.RequestParser()
group_volume_parser.add_argument('volume', type=int, required=True)


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

    # Add new student
    def post(self):
        args = name_parser.parse_args(strict=True)
        first_name = args['first_name']
        last_name = args['last_name']
        session.add(StudentModel(None, first_name, last_name))
        session.commit()
        return {'code': 201, 'message': f'{first_name} {last_name} added'}, 201

    # Delete student by STUDENT_ID
    def delete(self, student_id: int):
        try:
            session.delete(
                session.query(
                    StudentModel).filter(StudentModel.id == student_id).one())
            session.commit()
            return {
                'code': 200,
                'message': f'Student with the ID = {student_id} deleted.',
            }, 200
        except NoResultFound:
            return {'code': 404, 'message': 'Student not found'}, 404


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

    # Find all groups with less or equals student count
    def post(self):
        args = group_volume_parser.parse_args(strict=True)
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
        return groups


class StudentsOnCourse(Resource):
    # Find all students related to the course with a given name.
    def get(self):
        args = course_name_parser.parse_args(strict=True)
        course_name = args['course_name']
        courses_list = [crse.name for crse in session.query(CourseModel).all()]
        if course_name not in courses_list:
            return {'code': 404, 'message': 'Course not found'}, 404
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
        return students

    # Add a student to the course (from a list)
    def put(self, student_id: int):
        args = course_name_parser.parse_args(strict=True)
        course_name = args['course_name']
        courses_list = [crse.name for crse in session.query(CourseModel).all()]
        if course_name not in courses_list:
            return {'code': 404, 'message': 'Course not found'}, 404
        course = session.query(
            CourseModel).filter(CourseModel.name == course_name).one()
        try:
            student = session.query(
                StudentModel).filter(StudentModel.id == student_id).one()
            student.courses.append(course)
            session.commit()
            return {
                'code': 401,
                'mesage': f'Student with the ID = {student_id} added to the {course_name} course.',
                }, 401
        except NoResultFound:
            return {'code': 404, 'message': 'Student not found'}, 404


    # Remove the student from one of his or her courses
    def delete(self, student_id: int):
        args = course_name_parser.parse_args(strict=True)
        course_name = args['course_name']
        courses_list = [crse.name for crse in session.query(CourseModel).all()]
        if course_name not in courses_list:
            return {'code': 404, 'message': 'Course not found'}, 404
        course = session.query(
            CourseModel).filter(CourseModel.name == course_name).one()
        try:
            student = session.query(
                StudentModel).filter(StudentModel.id == student_id).one()
            student.courses.remove(course)
            session.commit()
            return {
                'code': 404,
                'mesage': f'Student with the ID = {student_id} removed from the {course_name} course.',
                }, 404
        except NoResultFound:
            return {'code': 404, 'message': 'Student not found'}, 404


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
