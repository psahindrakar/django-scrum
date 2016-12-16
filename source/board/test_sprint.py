from datetime import date

from django.test import TestCase
from board.models import Sprint

class SprintTestCase(TestCase):

    def setUp(self):
        Sprint.objects.create(
            name='Printing machines',
            description='Printing machines available from vendors are listed here',
            end=date.today()
        )

    def test_sprint_created(self):
        machine_sprint = Sprint.objects.get(name="Printing machines")
        self.assertEqual(machine_sprint.name, 'Printing machines')