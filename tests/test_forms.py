from django.test import TestCase
import code_editor.views as views


class StandardFormTest(TestCase):
    def test_standard_form_with_correct_data(self):
        form = views.StandardForm(data={'std': 'c89'})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['std'], 'c89')

    def test_standard_form_with_incorrect_data(self):
        form = views.StandardForm(data={'std': 'c88'})
        self.assertFalse(form.is_valid())


class OptimizationFormTest(TestCase):
    def test_optimization_form_with_correct_data(self):
        form = views.OptimizationForm(data={'speed': True, 'reverse': True, 'nolab': False})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['speed'], True)
        self.assertEqual(form.cleaned_data['reverse'], True)
        self.assertEqual(form.cleaned_data['nolab'], False)

    def test_optimization_form_with_missing_data(self):
        form = views.OptimizationForm(data={'reverse': True, 'nolab': False})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['speed'], False)
        self.assertEqual(form.cleaned_data['reverse'], True)
        self.assertEqual(form.cleaned_data['nolab'], False)


class ProcessorFormTest(TestCase):
    def test_processor_form_with_correct_data(self):
        form = views.ProcessorForm(data={'proc': 'mcs51'})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['proc'], 'mcs51')

    def test_processor_form_with_incorrect_data(self):
        form = views.ProcessorForm(data={'proc': 'mcs52'})
        self.assertFalse(form.is_valid())


class MCS51FormTest(TestCase):
    def test_mcs51_form_with_correct_data(self):
        form = views.MCS51Form(data={'mcs51': 'small'})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['mcs51'], 'small')

    def test_mcs51_form_with_incorrect_data(self):
        form = views.MCS51Form(data={'mcs51': 'mid'})
        self.assertFalse(form.is_valid())


class Z80FormTest(TestCase):
    def test_z80_form_with_correct_data(self):
        form = views.Z80Form(data={'callee': True, 'reserve': False})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['callee'], True)
        self.assertEqual(form.cleaned_data['reserve'], False)

    def test_z80_form_with_missing_data(self):
        form = views.Z80Form(data={'reserve': False})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['callee'], False)
        self.assertEqual(form.cleaned_data['reserve'], False)


class STM8FormTest(TestCase):
    def test_stm8_form_with_correct_data(self):
        form = views.STM8Form(data={'stm8': 'medium'})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['stm8'], 'medium')

    def test_stm8_form_with_incorrect_data(self):
        form = views.STM8Form(data={'stm8': 'mid'})
        self.assertFalse(form.is_valid())


class DirFormTest(TestCase):
    def test_dir_form_with_correct_data(self):
        form = views.DirForm(data={'name': 'test_dir', 'desc': 'test_dir_desc'})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['name'], 'test_dir')
        self.assertEqual(form.cleaned_data['desc'], 'test_dir_desc')

    def test_dir_form_with_missing_data(self):
        form = views.DirForm()
        self.assertFalse(form.is_valid())

    def test_dir_form_with_incorrect_name(self):
        form = views.DirForm(data={'name': 300 * 'a'})
        self.assertFalse(form.is_valid())

    def test_dir_form_with_incorrect_desc(self):
        form = views.DirForm(data={'name': 'test_dir', 'desc': 700 * 'a'})
        self.assertFalse(form.is_valid())


class UploadFileFormTest(TestCase):
    def test_upload_file_form_with_missing_data(self):
        form = views.UploadFileForm()
        self.assertFalse(form.is_valid())


class FileFormTest(TestCase):
    def test_file_form_with_correct_data(self):
        form = views.FileForm(data={'name': 'test_file', 'content': 'test_file_content'})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['name'], 'test_file')
        self.assertEqual(form.cleaned_data['content'], 'test_file_content')

    def test_file_form_with_missing_data(self):
        form = views.FileForm()
        self.assertFalse(form.is_valid())

    def test_file_form_with_incorrect_name(self):
        form = views.FileForm(data={'name': 300 * 'a'})
        self.assertFalse(form.is_valid())

    def test_file_form_with_incorrect_desc(self):
        form = views.FileForm(data={'name': 'test_file', 'desc': 700 * 'a'})
        self.assertFalse(form.is_valid())
