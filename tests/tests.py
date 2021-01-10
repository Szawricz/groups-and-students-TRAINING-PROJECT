"""The unit tests for the students_app."""

from unittest import TestCase

from students_app.view import app


class TestReporterMethods(TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_add_new_student(self):
        students_before = self.client.get('/api/v1.0/students/').\
            get_data(as_text=True)
        self.assertNotIn('Martic', students_before)
        self.assertNotIn('Andrew', students_before)
        response = self.client.post(
            '/api/v1.0/students/',
            data=dict(first_name='Andrew', last_name='Martic'),
            ).get_data(as_text=True)
        self.assertIn('{"mesage": "Andrew Martic added."}', response)
        students_after = self.client.get('/api/v1.0/students/').\
            get_data(as_text=True)
        self.assertIn('Martic', students_after)
        self.assertIn('Andrew', students_after)

    def test_add_student_to_course(self):
        course_before = self.client.post(
            '/api/v1.0/students/',
            data=dict(course_name='biology')
        ).get_data(as_text=True)
        response = self.client.put(
            '/api/v1.0/students/201/course/',
            data=dict(course_name='biology'),
        ).get_data(as_text=True)
        self.assertIn(
            '{"mesage": "Student with the ID = 201 added to the biology course."}',
            response,
            )
        course_after = self.client.post(
            '/api/v1.0/students/',
            data=dict(course_name='biology'),
        ).get_data(as_text=True)
        self.assertNotIn('Martic', course_before)
        self.assertIn('Martic', course_after)

    def test_remove_student_from_course(self):
        course_before = self.client.post(
            '/api/v1.0/students/',
            data=dict(course_name='biology')
        ).get_data(as_text=True)
        response = self.client.delete(
            '/api/v1.0/students/201/course/',
            data=dict(course_name='biology'),
            ).get_data(as_text=True)
        self.assertIn(
            '{"mesage": "Student with the ID = 201 removed from the biology course."}',
            response,
            )
        course_after = self.client.post(
            '/api/v1.0/students/',
            data=dict(course_name='biology'),
        ).get_data(as_text=True)
        self.assertIn('Martic', course_before)
        self.assertNotIn('Martic', course_after)

    def test_delete_student_by_id(self):
        students_before = self.client.get('/api/v1.0/students/').\
            get_data(as_text=True)
        self.assertIn('Martic', students_before)
        response = self.client.delete(
            '/api/v1.0/students/201/',
        ).get_data(as_text=True)
        self.assertIn(
            '{"mesage": "Student with the ID = 201 deleted."}',
            response,
            )
        students_after = self.client.get('/api/v1.0/students/').\
            get_data(as_text=True)
        self.assertNotIn('Martic', students_after)
