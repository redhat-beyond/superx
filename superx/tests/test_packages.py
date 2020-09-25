
import unittest
from pathlib import Path

import pkg_resources





class TestRequirements(unittest.TestCase):
    

    def test_requirements(self):
       
       
        pckgs = {'Flask', 'Flask-SQLAlchemy', 'flask_login', 'flask_wtf', 'PyMySQL'}
        for pkg in pckgs:
            with self.subTest(pkg=pkg):
                pkg_resources.require(pkg)

                