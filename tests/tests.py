"""The unit tests for the students_app."""

from unittest import TestCase
from students_app.view import app


class TestReporterMethods(TestCase):
    def setUp(self):
        self.client = app.test_client()
    
    def test_show_students(self):
        response = self.client.get('/').get_data(as_text=True)
        response_students = self.client.get('/students/').get_data(as_text=True)
        self.assertEqual(201, response_students.count('<tr>'))
        self.assertEqual(response, response_students)
        sample = '<body>\n  <h1>STUDENTS</h1>\n  <a href="/groups/">GROUPS</a>\n  <p></p>\n  <form method="POST" action="/students/add/">\n    <input required name="first_name" placeholder="First Name"></input>\n    <input required name="last_name" placeholder="Last Name"></input>\n    <button type="submit">Add new student</button>\n  </form>\n  <form action="/students/on_course/">\n    <select name="course_name">\n      Show selected course students:\n      <option disabled>Select a course</option>'
        self.assertIn(sample, response_students)

    def test_show_groups(self):
        response = self.client.get('/groups/').get_data(as_text=True)
        self.assertEqual(21, response.count('<tr>'))
        response_sample = '<body>\n   <h1>GROUPS</h1>\n   <a href="/students/">STUDENTS</a>\n   <p></p>\n   <form action="/groups/find_le/">\n      <input name="volume" min="0" step="1" required placeholder="less or equal"></input>\n      <button formmethod="GET" type="submit">Find groups</button>\n   </form>\n   <p></p>\n   <table border="1">\n      <tr>\n         <th>ID</th>\n         <th>Group</th>\n         <th>Volume</th>\n         <th>Students</th>'
        self.assertIn(response_sample, response)

    def test_add_new_student(self):
        response_before = self.client.get('/students/').get_data(as_text=True)
        self.assertNotIn('Martic', response_before)
        response_after = self.client.post('/students/add/', data=dict(first_name='Andrew',last_name='Martic')).get_data(as_text=True)
        self.assertIn('Martic', response_after)
        self.assertEqual(response_after.count('<tr>') - response_before.count('<tr>'), 1)

    def test_add_student_to_course(self):
        response_before = self.client.get('/students/').get_data(as_text=True)
        sample_before = ' <tr>\n      <td>201</td>\n      <td>\n        Milo Martic\n        <form>\n          <button formmethod="POST" type="submit" formaction="/students/delete/" name="id" value="203">\n            DELETE\n          </button>\n        </form>\n      </td>\n      <td>None</td>\n      <td>\n        <form action="/students/add/to_course/">\n          <select name="course_name">\n            <option disabled>Select a course</option>'
        response_after = self.client.post(
            '/students/add/to_course/', data=dict(student_id='201', course_name='biology')).get_data(as_text=True)
        sample_after = '      <td>203</td>\n      <td>\n        Milo Martic\n        <form>\n          <button formmethod="POST" type="submit" formaction="/students/delete/" name="id" value="203">\n            DELETE\n          </button>\n        </form>\n      </td>\n      <td>None</td>\n      <td>\n        <form method="POST">\n          russian language\n          <button type="submit" formaction="/students/remove_from_course/" name="course_name" value="russian language">\n            LEAVE\n          </button>'
        self.assertIn(sample_before, response_before)
        self.assertIn(sample_after, response_after)

    def test_remove_student_from_course(self):
        response_after = self.client.post(
            '/students/remove_from_course/', data=dict(student_id='201', course_name='biology')).get_data(as_text=True)
        sample_after = '      <td>203</td>\n      <td>\n        Milo Martic\n        <form>\n          <button formmethod="POST" type="submit" formaction="/students/delete/" name="id" value="203">\n            DELETE\n          </button>\n        </form>\n      </td>\n      <td>None</td>\n      <td>\n        <form method="POST">\n          russian language\n          <button type="submit" formaction="/students/remove_from_course/" name="course_name" value="russian language">\n            LEAVE\n          </button>'
        response_before = self.client.get('/students/').get_data(as_text=True)
        sample_before = ' <tr>\n      <td>201</td>\n      <td>\n        Milo Martic\n        <form>\n          <button formmethod="POST" type="submit" formaction="/students/delete/" name="id" value="203">\n            DELETE\n          </button>\n        </form>\n      </td>\n      <td>None</td>\n      <td>\n        <form action="/students/add/to_course/">\n          <select name="course_name">\n            <option disabled>Select a course</option>'
        self.assertIn(sample_before, response_before)
        self.assertIn(sample_after, response_after)

    def test_delete_student_by_id(self):
        response_before = self.client.get('/students/').get_data(as_text=True)
        self.assertIn('Martic', response_before)
        response_after = self.client.post('/students/delete/', data=dict(id='201')).get_data(as_text=True)
        self.assertNotIn('Martic', response_after)
        self.assertEqual(response_before.count('<tr>') - response_after.count('<tr>'), 1)

    