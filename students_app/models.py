"""The models module."""

from sqlalchemy import (Column, ForeignKey, Integer, String, Table,
                        create_engine)
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

DATABASE = {
        'drivername': 'postgres',
        'host': 'localhost',
        'port': '5432',
        'username': 'Shavrin_Maksim',
        'password': '123456789',
        'database': 'students',
    }

Base = declarative_base()

engine = create_engine(URL(**DATABASE), echo=False)

Session = sessionmaker()

session = Session(bind=engine)

association_table = Table(
    'association',
    Base.metadata,
    Column('student_id', Integer, ForeignKey('student.id')),
    Column('course_id', Integer, ForeignKey('course.id')),
)


class GroupModel(Base):
    __tablename__ = 'group'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name


class StudentModel(Base):
    __tablename__ = 'student'
    id = Column(Integer, primary_key=True)
    group_id = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    courses = relationship(
        'CourseModel',
        secondary=association_table,
        backref="students",
        )

    def __init__(self, group_id, first_name, last_name):
        self.group_id = group_id
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self):
        return f'\n{self.first_name} {self.last_name}: {self.group_id}'


class CourseModel(Base):
    __tablename__ = 'course'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        return self.name


def get_students():
    students = []
    for id, first_name, last_name, group_id, student in session.query(
            StudentModel.id,
            StudentModel.first_name,
            StudentModel.last_name,
            StudentModel.group_id,
            StudentModel):
        courses_list = [course.name for course in student.courses]
        all_courses = [
            course.name for course in session.query(CourseModel.name)
            ]
        dif = list(set(all_courses) - set(courses_list))
        students.append(
            [id, f'{first_name} {last_name}', group_id, courses_list, dif],
            )
    return students



def get_groups():
    groups = []
    for id, name in session.query(GroupModel.id, GroupModel.name):
        students = []
        for student_id, first_name, last_name in session.query(
                StudentModel.id,
                StudentModel.first_name,
                StudentModel.last_name,
                ).filter(StudentModel.group_id == name):
            students.append([student_id, f'{first_name} {last_name}'])
        groups.append([id, name, len(students), students])
    return groups

def get_courses():
    courses = []
    for id, name, description, course in session.query(
            CourseModel.id,
            CourseModel.name,
            CourseModel.description,
            CourseModel):
        students_list = []
        for student in course.students:
            students_list.append(
                [student.id, f'{student.first_name} {student.last_name}'],
                )
        courses.append(
            [id, name, description, len(students_list), students_list],
            )
    return courses

def add_student(first_name: str, last_name: str):
    session.add(StudentModel(None, first_name, last_name))
    session.commit()

def delete_student(student_id: int):
    session.delete(
        session.query(
            StudentModel).filter(StudentModel.id == student_id).one())
    session.commit()

def leave_course(student_id: int, course_name: str):
    course = session.query(
        CourseModel).filter(CourseModel.name == course_name).one()
    student = session.query(
        StudentModel).filter(StudentModel.id == student_id).one()
    student.courses.remove(course)
    session.commit()

def student_to_course(student_id: int, course_name: str):
    course = session.query(
        CourseModel).filter(CourseModel.name == course_name).one()
    student = session.query(
        StudentModel).filter(StudentModel.id == student_id).one()
    student.courses.append(course)
    session.commit()

