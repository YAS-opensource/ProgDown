import os
import unittest
import coverage

from flask_script import Manager

from src import app

manager = Manager(app)

COV = coverage.coverage(
    branch=True,
    include="src/*",
    omit=["src/tests/*", "src/*/__init__.py", "src/*/*/__init__.py"],
)
COV.start()

@manager.command
def cov():
    """Runs the unit tests with coverage."""
    tests = unittest.TestLoader().discover("src/tests")
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print("Coverage Summary:")
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, "tmp/coverage")
        COV.html_report(directory=covdir)
        print("HTML version: file://%s/index.html" % covdir)
        COV.erase()
        return 0
    return 1

if __name__ == "__main__":
    manager.run()