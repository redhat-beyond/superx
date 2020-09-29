
import unittest
import pkg_resources



class TestRequirements(unittest.TestCase):
    

    def test_requirements(self):
       
       
        pckgs = {'flask' ,'Flask-SQLAlchemy' ,'Flask-Bootstrap', 'SQLAlchemy', 'flask_login' ,'flask_wtf', 'pymysql'}
        for pkg in pckgs:
            with self.subTest(pkg=pkg):
                pkg_resources.require(pkg)






 
                