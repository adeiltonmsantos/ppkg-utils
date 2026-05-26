from unittest import TestCase

from django.conf import settings

from utils.dispatch import Dispatch


class UnitTestDispatch(TestCase):
    def setUp(self):
        super_values = super().setUp()
        self.img_path = settings.BASE_DIR / 'utils/tests/imgs_to_test'
        self.exam_report_path = settings.BASE_DIR / 'utils/tests/reposrts_to_test'
        errors = [
            'Erro 1',
            'Erro 2',
            'Erro 3'
        ]
        self.dispatch = Dispatch(list_erros=errors)
        return super_values
    
    def test_initial(self):
        dsp = self.dispatch
        dsp.geraDespachoPDF()
