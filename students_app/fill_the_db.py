"""The data generating and database filling module."""

from random import choice, choices, randint
from string import ascii_uppercase, digits

from models import Base, CourseModel, GroupModel, StudentModel, engine, session

GROUPS_NUMBER = 20
STUDENTS_NUMBER = 200
MIN_STUDENTS_IN_GROUP = 10
MAX_STUDENTS_IN_GROUP = 30


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


def generate_students(students_number: int) -> list:
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
    return [StudentModel(None, *name) for name in students_names]


def generate_groups(groups_number: int) -> list:
    groups_names = set()
    while len(groups_names) < groups_number:
        two_characters = ''.join(choices(ascii_uppercase, k=2))
        two_digits = ''.join(choices(digits, k=2))
        name = f'{two_characters}-{two_digits}'
        groups_names.add(name)
    return [GroupModel(name) for name in groups_names]


def generate_groups_volumes(groups_number: int, students_number: int,
                            min_in_group: int, max_in_group: int) -> list:
    groups_volumes = []
    for group in range(groups_number):
        volume = 0
        if students_number > min_in_group:
            volume = randint(min_in_group, min(max_in_group, students_number))
        students_number -= volume
        groups_volumes.append(volume)
    return groups_volumes


def add_students_to_groups(
        groups: list, students: list,
        min_in_group: int, max_in_group: int) -> tuple:
    groups_volumes = generate_groups_volumes(
        len(groups),
        len(students),
        min_in_group,
        max_in_group,
        )
    students_counter = 0
    for group_number, volume in enumerate(groups_volumes):
        for n in range(volume):
            students[students_counter + n].group_id = groups[group_number].name
        students_counter += volume
    return (students, groups)


if __name__ == "__main__":
    Base.metadata.create_all(engine)

    students, groups = add_students_to_groups(
        generate_groups(GROUPS_NUMBER),
        generate_students(STUDENTS_NUMBER),
        MIN_STUDENTS_IN_GROUP,
        MAX_STUDENTS_IN_GROUP,
        )
    courses = generate_courses()

    for student in students:
        choiced_courses = set(choices(courses, k=randint(1, 3)))
        student.courses.extend(choiced_courses)

    session.add_all(students)
    session.add_all(groups)
    session.add_all(courses)
    session.commit()
