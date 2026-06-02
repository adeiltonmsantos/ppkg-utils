from unittest import TestCase

from django.conf import settings

from utils.appDocuments import extractScheduleToDataFrame


class FileHanderUnitTest(TestCase):
    def setUp(self):
        super_obj = super().setUp()
        self.url_files_to_test = settings.BASE_DIR / 'utils/tests/timelines_to_test'
        return super_obj
    
    def test_if_file_is_valid(self):
        url_file = self.url_files_to_test / 'timeline03.pdf'
        fileobj = None
        with open(url_file, 'rb') as f:
            fileobj = f
            data = extractScheduleToDataFrame(fileobj)
        
        cols_list = data.columns.to_list()
        list_wantd = ['data', 'tc', 'produto', 'marca', 'qn', 'quant']

        self.assertEqual(cols_list, list_wantd)