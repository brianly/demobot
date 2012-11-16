"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
#from hackday.tasks import add
#from celery import group

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
#        jobs = []
#
#        for x in range(1,10):
#            st = add.subtask((1, x))
#            jobs.append(st)
#
#        job = group(jobs)
#        result = job.apply_async()
#        joined = result.join()
#
#        self.assertEqual(1 + 1, 2)
