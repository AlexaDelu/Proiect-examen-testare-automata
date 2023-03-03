import unittest
from HtmlTestRunner import HTMLTestRunner
from TestEmag import TestEMag
from TestEmag2 import TestEmag2


def test_suite():
    test_cases = unittest.TestSuite()
    test_cases.addTests([
         unittest.defaultTestLoader.loadTestsFromTestCase(TestEMag),
         unittest.defaultTestLoader.loadTestsFromTestCase(TestEmag2),
    ])
    return test_cases

if __name__ == '__main__':
    runner = HTMLTestRunner(verbosity=2, output="./reports/", report_title='Test report', report_name='report',
                            open_in_browser=True, combine_reports=True)
    runner.run(test_suite())