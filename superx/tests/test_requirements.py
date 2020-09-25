
import unittest
from pathlib import Path

import pkg_resources


_REQUIREMENTS_PATH = Path(__file__).parent.parent.with_name("requirments.txt")


class TestRequirements(unittest.TestCase):
    

    def test_requirements(self):
       
       
        requirements = pkg_resources.parse_requirements(_REQUIREMENTS_PATH.open())
        for requirement in requirements:
            requirement = str(requirement)
            with self.subTest(requirement=requirement):
                pkg_resources.require(requirement)

                