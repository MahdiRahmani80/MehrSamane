from django.test import TestCase
from .models import *
from datetime import datetime

"""
### Run this test in the command line to test users module:
`python manage.py test users`

### For testing all of tast cases you can run this:
`python manage.py test`

according to this link -> https://docs.djangoproject.com/en/5.1/topics/testing/overview/
"""
class TestStudentProfile(TestCase):
    @classmethod
    def setUpTestData(cls):
        """ Create test users and student profiles """
        cls.usr1 = UserProfile.objects.create(username="student1")
        cls.usr2 = UserProfile.objects.create(username="student2")

        # Create StudentProfile instances, these should trigger student ID generation
        cls.student1 = StudentProfile(user=cls.usr1, enrollment=datetime(2025, 2, 8))
        cls.student2 = StudentProfile(user=cls.usr2, enrollment=datetime(2025, 2, 8))
        
        cls.student1.save()
        cls.student2.save()

    def test_student_id(self):
        """ Test if student IDs are generated correctly """

        # Fetch the created StudentProfile instances
        one = StudentProfile.objects.get(user=self.usr1)
        two = StudentProfile.objects.get(user=self.usr2)

        self.assertEqual(one.student_id  , "1403001")
        self.assertEqual(two.student_id  , "1403002")

    def test_student_id_format(self):
        # Validate that the student_id isalways of length 7 (Jalali year + 4-digit sequence)
        one = StudentProfile.objects.get(user=self.usr1)
        two = StudentProfile.objects.get(user=self.usr2)

        self.assertEqual(len(one.student_id), 7)  
        self.assertEqual(len(two.student_id), 7)  
