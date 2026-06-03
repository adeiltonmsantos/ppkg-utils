from django.test import SimpleTestCase
from django.urls import resolve, reverse

from appDocuments import views


class IpemDataViewsTest(SimpleTestCase):

    def test_ipem_data_based_function_view_is_correct(self):
        resolve_obj = resolve(reverse('appDocuments:ipem-data-send'))
        bcv_wanted = resolve_obj.func.view_class
        bcv = views.IpemData
        self.assertIs(bcv, bcv_wanted)

    def test_ipem_data_template_is_correct(self):
        response = self.client.get(reverse('appDocuments:ipem-data-send'))
        self.assertTemplateUsed(response, 'appDocuments/pages/ipem_data.html')


class HighErrorDispatchTest(SimpleTestCase):
    def test_high_error_dispatch_based_function_view_is_correct(self):
        resolve_obj = resolve(reverse('appDocuments:high-error-dispatch'))
        bcv_wanted = resolve_obj.func.view_class
        bcv = views.HighErrorDispatch
        self.assertIs(bcv, bcv_wanted)

    def test_high_error_dispatch_template_is_correct(self):
        response = self.client.get(reverse('appDocuments:high-error-dispatch'))
        self.assertTemplateUsed(response, 'appDocuments/pages/high_error_dispatch.html')


class ExtractExamScheduleViewsTest(SimpleTestCase):

    def test_upload_exam_schedule_based_function_view_is_correct(self):
        resolve_obj = resolve(reverse('appDocuments:upload-exam-schedule'))
        bcv_wanted = resolve_obj.func.view_class
        bcv = views.UploadExamSchedule
        self.assertIs(bcv, bcv_wanted)

    def test_extract_exam_schedule_template_is_correct(self):
        response = self.client.get(reverse('appDocuments:ipem-data-send'))
        self.assertTemplateUsed(response, 'appDocuments/pages/ipem_data.html')

