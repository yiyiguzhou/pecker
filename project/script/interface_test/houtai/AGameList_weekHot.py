from project.script.testsuite.TestsuiteNormal import *
from project.lib.interface_test.testcase import testcase_reader_file_sheet as ts


class AGameList_weekHot(TestsuiteNormal):
    def setup(self):
        pass

    def test(self):
        file = os.path.join(os.path.dirname(__file__), 'AGameList_weekHot.xml')
        ts.run_test_case(file)

    def teardown(self):
        pass
