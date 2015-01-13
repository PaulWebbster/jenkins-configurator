import unittest, os
import inspect

# Set up the path for unittets
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
print parentdir
os.sys.path.insert(0, parentdir)

from src.xmlinterface import JobPraser

class TestJobParser(unittest.TestCase):

    def setUp(self):
        self.job = JobPraser('test_data/config.xml')

    def test_get_shell_command(self):
        print self.job.get_shell_command(0)

