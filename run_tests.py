import unittest
import tests.all_tests
testSuite = tests.all_tests.create_test_suite()
text_runner = unittest.TextTestRunner().run(testSuite)