"""The data generating and database filling module."""

from random import choice, choices, randint
from string import ascii_uppercase, digits

from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker

from models import CourseModel, GroupModel, StudentModel, metadata

DATABASE = {
        'drivername': 'postgres',
        'host': 'localhost',
        'port': '5432',
        'username': 'Shavrin_Maksim',
        'password': '123456789',
        'database': 'students',
    }


def generate_courses() -> list:
    courses = {
        'algebra': 'the study of mathematical symbols and the rules for manipulating these symbols',
        'biology': 'the natural science that studies life and living organisms, including their physical structure, chemical processes, molecular interactions, physiological mechanisms, development and evolution.',
        'history': 'the study of the past',
        'literature': 'an academic discipline devoted to the study of American literature',
        'chemistry': 'the scientific discipline involved with elements and compounds composed of atoms, molecules and ions: their composition, structure, properties, behavior and the changes they undergo during a reaction with other substances.',
        'physics': 'the natural science that studies matter, its motion and behavior through space and time, and the related entities of energy and force.',
        'geography': 'a field of science devoted to the study of the lands, features, inhabitants, and phenomena of the Earth and planets.',
        'geometry': 'one of the oldest branches of mathematics. It is concerned with properties of space that are related with distance, shape, size, and relative position of figures.',
        'russian language': 'an East Slavic language native to the Russians in Eastern Europe. It is an official language in Russia, Belarus, Kazakhstan, Kyrgyzstan, as well as being widely used throughout the Baltic states, the Caucasus and Central Asia.',
        'english language': 'a West Germanic language first spoken in early medieval England which eventually became the leading language of international discourse in today´s world',
    }
    return [CourseModel(name, descr) for name, descr in courses.items()]


def generate_students_names(students_number: int) -> set:
    students_names = set()
    first_names = [
        'Liam', 'Olivia', 'Noah', 'Emma', 'Oliver', 'Ava', 'William', 'Sophia',
        'Elijah', 'Isabella', 'James', 'Charlotte', 'Benjamin', 'Amelia',
        'Lucas', 'Mia', 'Mason', 'Harper', 'Ethan', 'Evelyn',
        ]
    second_names = [
        'Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller',
        'Davis', 'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez',
        'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin',
        ]
    while len(students_names) < students_number:
        full_name = (choice(first_names), choice(second_names))
        students_names.add(full_name)
    return students_names


def generate_groups(groups_number: int) -> list:
    groups_names = set()
    while len(groups_names) < groups_number:
        two_characters = ''.join(choices(ascii_uppercase, k=2))
        two_digits = ''.join(choices(digits, k=2))
        name = f'{two_characters}-{two_digits}'
        groups_names.add(name)
    return [GroupModel(name) for name in groups_names]


def generate_groups_volumes(groups_number: int, students_number: int,
                            min_in_group: int, max_in_group: int) -> dict:
    groups = generate_groups(groups_number)
    groups_volumes = {}
    for group in groups:
        if students_number > max_in_group:
            volume = randint(min_in_group, max_in_group)
        elif students_number in range(min_in_group, max_in_group + 1):
            volume = randint(min_in_group, students_number)
        else:
            volume = 0
        students_number -= volume
        groups_volumes[group.name] = volume
    return (groups_volumes, groups)


def generate_students_and_groups(
        groups_number: int, students_number: int,
        min_in_group: int, max_in_group: int) -> tuple:
    groups_volumes_groups = generate_groups_volumes(
        groups_number, students_number, min_in_group, max_in_group)
    groups_volumes = groups_volumes_groups[0]
    groups = groups_volumes_groups[1]
    students_names = generate_students_names(students_number)
    students = []
    for group_name, volume in groups_volumes.items():
        for n in range(volume):
            full_name = students_names.pop()
            first_name = full_name[0]
            last_name = full_name[1]
            students.append(StudentModel(group_name, first_name, last_name))
    for full_name in students_names:
        students.append(StudentModel(None, full_name[0], full_name[1]))
    return (students, groups)


if __name__ == "__main__":
    engine = create_engine(URL(**DATABASE), echo=True)
    metadata.create_all(engine)

    students_groups = generate_students_and_groups(20,200, 10, 30)
    students = students_groups[0]
    groups = students_groups[1]
    courses = generate_courses()

    Session = sessionmaker()
    session = Session(bind=engine)
    session.add_all(students)
    session.add_all(groups)
    session.add_all(courses)
    session.commit()
