import os

from django.test import TestCase
from django.contrib.auth.models import User
from code_editor.models import Directory, File
from code_editor.views import set_file, opt_to_val, val_to_opt, z80_to_val, val_to_z80, set_to_session


def create_user_file_dir():
    User.objects.create_user(username="test_user", password="test_password")
    user = User.objects.get(username="test_user")
    Directory.objects.create(name="test_dir", owner=user)
    File.objects.create(name="test_file.c", owner=user, parent=Directory.objects.get(name="test_dir"))


class IndexViewTest(TestCase):
    def setUp(self):
        User.objects.create_user(username="test_user", password="test_password")
        User.objects.create_user(username="test_user2", password="test_password2")
        user = User.objects.get(username="test_user")
        Directory.objects.create(name="test_dir", owner=user)
        File.objects.create(name="test_file", owner=user, parent=Directory.objects.get(name="test_dir"))

    def test_index_redirect(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 301)

    def test_index_view(self):
        response = self.client.get('/code_editor/')
        self.assertEqual(response.status_code, 200)

    def test_index_view_file_unauthorized(self):
        response = self.client.get('/code_editor/' + str(File.objects.get(name="test_file").id) + '/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context.get('file') is None)

    def test_index_view_file_authorized(self):
        self.client.login(username="test_user", password="test_password")
        response = self.client.get('/code_editor/' + str(File.objects.get(name="test_file").id) + '/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context.get('file') is not None)

    def test_index_view_file_authorized_wrong_user(self):
        self.client.login(username="test_user2", password="test_password2")
        response = self.client.get('/code_editor/' + str(File.objects.get(name="test_file").id) + '/')
        self.assertEqual(response.status_code, 200)
        file = response.context.get('file')[0]
        self.assertTrue(file is not None)
        self.assertTrue(file['content'] == 'You are not the owner of this file')

    def test_index_forms(self):
        self.client.login(username="test_user", password="test_password")
        request = self.client.get('/code_editor/')
        request.user = User.objects.get(username="test_user")
        request.method = 'POST'
        request.session = self.client.session
        request.body = b'{"standard_opt":"c89"}'
        set_to_session(request)
        self.assertEqual(request.session['standard'], 'c89')
        request.body = b'{"optimization_opt":{"speed":true,"reverse":false,"nolab":false}}'
        set_to_session(request)
        request.body = b'{"processor_opt":"mcs51"}'
        set_to_session(request)
        self.assertEqual(request.session['processor'], 'mcs51')
        request.body = b'{"mcs51_opt":"small"}'
        set_to_session(request)
        self.assertEqual(request.session['mcs51'], 'small')
        request.body = b'{"z80_opt":{"callee":true,"reserve":false}}'
        set_to_session(request)
        request.body = b'{"stm8_opt":"medium"}'
        set_to_session(request)
        self.assertEqual(request.session['stm8'], 'medium')


class CompileNoFileViewTest(TestCase):
    def test_compile_no_file(self):
        response = self.client.post('/code_editor/compile/')
        self.assertEqual(response.status_code, 302)


class CompileFileViewTest(TestCase):
    def setUp(self):
        User.objects.create_user(username="test_user", password="test_password")
        user = User.objects.get(username="test_user")
        Directory.objects.create(name="test_dir", owner=user)
        File.objects.create(name="test_file.c", owner=user, parent=Directory.objects.get(name="test_dir"),
                            content="int main() { return 0; }")
        File.objects.create(name="test_wrong.c", owner=user, parent=Directory.objects.get(name="test_dir"),
                            content="int main() { return a; }")

    def test_compile_file(self):
        self.client.login(username="test_user", password="test_password")
        response = self.client.get('/code_editor/compile/' + str(File.objects.get(name="test_file.c").id))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context.get('compiled_file') is not None)
        self.assertEqual(response.context.get('compilation_status'), "Compilation successful")
        os.name = 'unix'
        response = self.client.get('/code_editor/compile/' + str(File.objects.get(name="test_file.c").id))
        self.assertEqual(response.status_code, 200)

    def test_compile_wrong_file(self):
        self.client.login(username="test_user", password="test_password")
        response = self.client.get('/code_editor/compile/' + str(File.objects.get(name="test_wrong.c").id))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context.get('compiled_file') is not None)
        self.assertEqual(response.context.get('compilation_status'), "Compilation error")


class SaveFileViewTest(TestCase):
    def setUp(self):
        create_user_file_dir()
        User.objects.create_user(username="test_user2", password="test_password2")

    def test_save_file(self):
        response = self.client.post('/code_editor/save/' + str(File.objects.get(name="test_file.c").id))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(File.objects.filter(name="test_file.c")[0].available)

    def test_save_file_unauthorized(self):
        response = self.client.post('/code_editor/save/' + str(File.objects.get(name="test_file.c").id))
        self.assertEqual(response.status_code, 200)

    def test_save_file_wrong_user(self):
        self.client.login(username="test_user2", password="test_password2")
        response = self.client.post('/code_editor/save/' + str(File.objects.get(name="test_file.c").id))
        self.assertEqual(response.status_code, 200)


class DeleteViewTest(TestCase):
    def setUp(self):
        create_user_file_dir()
        User.objects.create_user(username="test_user2", password="test_password2")

    def test_delete_file(self):
        self.client.login(username="test_user", password="test_password")
        response = self.client.post('/code_editor/delete_file/' + str(File.objects.get(name="test_file.c").id))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(File.objects.filter(name="test_file.c")[0].available)

    def test_delete_file_wrong_user(self):
        self.client.login(username="test_user2", password="test_password2")
        response = self.client.post('/code_editor/delete_file/' + str(File.objects.get(name="test_file.c").id))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(File.objects.filter(name="test_file.c")[0].available)

    def test_delete_file_unauthorized(self):
        response = self.client.post('/code_editor/delete_file/' + str(File.objects.get(name="test_file.c").id))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(File.objects.filter(name="test_file.c")[0].available)

    def test_delete_dir(self):
        self.client.login(username="test_user", password="test_password")
        response = self.client.post('/code_editor/delete_dir/' + str(Directory.objects.get(name="test_dir").id))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Directory.objects.filter(name="test_dir")[0].available)

    def test_delete_dir_wrong_user(self):
        self.client.login(username="test_user2", password="test_password2")
        response = self.client.post('/code_editor/delete_dir/' + str(Directory.objects.get(name="test_dir").id))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Directory.objects.filter(name="test_dir")[0].available)

    def test_delete_dir_unauthorized(self):
        response = self.client.post('/code_editor/delete_dir/' + str(Directory.objects.get(name="test_dir").id))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Directory.objects.filter(name="test_dir")[0].available)


class DeleteNoReloadViewTest(TestCase):
    def setUp(self):
        create_user_file_dir()

    def test_delete_file(self):
        self.client.login(username="test_user", password="test_password")
        response = self.client.post('/code_editor/delete_file_no/' + str(File.objects.get(name="test_file.c").id))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(File.objects.filter(name="test_file.c")[0].available)

    def test_delete_dir(self):
        self.client.login(username="test_user", password="test_password")
        response = self.client.post('/code_editor/delete_dir_no/' + str(Directory.objects.get(name="test_dir").id))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Directory.objects.filter(name="test_dir")[0].available)


class ChooseViewTest(TestCase):
    def setUp(self):
        create_user_file_dir()

    def test_delete_choose(self):
        self.client.login(username="test_user", password="test_password")
        response = self.client.post('/code_editor/delete/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context.get('subfiles') is not None)

    def test_delete_choose_unauthorized(self):
        response = self.client.post('/code_editor/delete/')
        self.assertEqual(response.status_code, 200)

    def test_add_dir_choose(self):
        self.client.login(username="test_user", password="test_password")
        response = self.client.post('/code_editor/add_dir/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context.get('subfiles') is not None)

    def test_add_dir_choose_unauthorized(self):
        response = self.client.post('/code_editor/add_dir/')
        self.assertEqual(response.status_code, 200)

    def test_add_file_choose(self):
        self.client.login(username="test_user", password="test_password")
        response = self.client.post('/code_editor/add_file/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context.get('subfiles') is not None)

    def test_add_file_choose_unauthorized(self):
        response = self.client.post('/code_editor/add_file/')
        self.assertEqual(response.status_code, 200)


class AddViewTest(TestCase):
    def setUp(self):
        User.objects.create_user(username="test_user", password="test_password")
        Directory.objects.create(name="test_dir", owner=User.objects.get(username="test_user"))

    def test_add_dir(self):
        self.client.login(username="test_user", password="test_password")
        response = self.client.get('/code_editor/add_dir/0')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context.get('form') is not None)
        response = self.client.post('/code_editor/add_dir/0', {'name': 'test_dir2', 'add': 'Add'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Directory.objects.filter(name="test_dir2").exists())

    def test_add_dir_unauthorized(self):
        response = self.client.get('/code_editor/add_dir/0')
        self.assertEqual(response.status_code, 200)

    def test_add_file(self):
        self.client.login(username="test_user", password="test_password")
        response = self.client.get('/code_editor/add_file/' + str(Directory.objects.get(name="test_dir").id))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context.get('form') is not None)
        response = self.client.post('/code_editor/add_file/' + str(Directory.objects.get(name="test_dir").id),
                                    {'name': 'test_file.c', 'content': 'int main() { return 0; }', 'add': 'Add'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(File.objects.filter(name="test_file.c").exists())
        self.assertEqual(File.objects.filter(name="test_file.c")[0].content, 'int main() { return 0; }')

    def test_upload_file(self):
        self.client.login(username="test_user", password="test_password")
        self.client.get('/code_editor/add_file/' + str(Directory.objects.get(name="test_dir").id))
        file = open('test_file.c', 'w')
        file.write('int main() { return 0; }')
        file.close()
        file = open('test_file.c', 'rb')
        response = self.client.post('/code_editor/add_file/' + str(Directory.objects.get(name="test_dir").id),
                                    {'name': 'test_file.c', 'file': file, 'upload': 'Upload'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(File.objects.filter(name="test_file.c").exists())
        self.assertEqual(File.objects.filter(name="test_file.c")[0].content, 'int main() { return 0; }')

    def test_add_file_unauthorized(self):
        response = self.client.get('/code_editor/add_file/0')
        self.assertEqual(response.status_code, 200)


class SetFileTest(TestCase):
    def setUp(self):
        create_user_file_dir()

    def test_set_none_file(self):
        context = {}
        response = self.client.get('/code_editor/')
        set_file(response, None, context)


class OptTest(TestCase):
    def test_all_opt(self):
        self.assertEqual(opt_to_val(True, True, True), 'speed+reverse+nolab')
        self.assertEqual(opt_to_val(True, True, False), 'speed+reverse')
        self.assertEqual(opt_to_val(True, False, True), 'speed+nolab')
        self.assertEqual(opt_to_val(False, True, True), 'reverse+nolab')
        self.assertEqual(opt_to_val(False, False, True), 'nolab')
        self.assertEqual(opt_to_val(False, True, False), 'reverse')
        self.assertEqual(opt_to_val(True, False, False), 'speed')
        self.assertEqual(opt_to_val(False, False, False), 'none')

    def test_all_val(self):
        self.assertEqual(val_to_opt('speed+reverse+nolab'), (True, True, True))
        self.assertEqual(val_to_opt('speed+reverse'), (True, True, False))
        self.assertEqual(val_to_opt('speed+nolab'), (True, False, True))
        self.assertEqual(val_to_opt('reverse+nolab'), (False, True, True))
        self.assertEqual(val_to_opt('nolab'), (False, False, True))
        self.assertEqual(val_to_opt('reverse'), (False, True, False))
        self.assertEqual(val_to_opt('speed'), (True, False, False))
        self.assertEqual(val_to_opt('none'), (False, False, False))


class Z80Test(TestCase):
    def test_all_z80(self):
        self.assertEqual(z80_to_val('callee+reserve'), (True, True))
        self.assertEqual(z80_to_val('callee'), (True, False))
        self.assertEqual(z80_to_val('reserve'), (False, True))
        self.assertEqual(z80_to_val('none'), (False, False))

    def test_all_val(self):
        self.assertEqual(val_to_z80(True, True), 'callee+reserve')
        self.assertEqual(val_to_z80(True, False), 'callee')
        self.assertEqual(val_to_z80(False, True), 'reserve')
        self.assertEqual(val_to_z80(False, False), 'none')
