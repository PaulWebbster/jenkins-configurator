#!/usr/bin/env python2

import unittest, os
import inspect

# Set up the path for unittets
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
print parentdir
os.sys.path.insert(0, parentdir)

from src.editor import Editor

class TestEditor(unittest.TestCase):

    def setUp(self):
        self.editor = Editor('test_data/config.xml')

    def test_edit_command(self):
        text = self.editor.edit_command()
