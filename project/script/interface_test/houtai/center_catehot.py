from project.script.testsuite.TestsuiteNormal import *
from project.lib.interface_test.testcase import testcase_reader_file_sheet as ts


class center_catehot(TestsuiteNormal):
    def setup(self):
        pass

    def test(self):
        file = os.path.join(os.path.dirname(__file__), 'center_catehot.xml')
        ts.run_test_case(file)

    def teardown(self):
        pass
