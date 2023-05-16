from django.test import TestCase
from django.contrib.auth.models import User
from code_editor.models import Directory, File


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
        self.assertTrue(response.context.get('file') == 'You are not the owner of this file')


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

    def test_compile_wrong_file(self):
        self.client.login(username="test_user", password="test_password")
        response = self.client.get('/code_editor/compile/' + str(File.objects.get(name="test_wrong.c").id))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context.get('compiled_file') is not None)
        self.assertEqual(response.context.get('compilation_status'), "Compilation error")


class SaveFileViewTest(TestCase):
    def setUp(self):
        User.objects.create_user(username="test_user", password="test_password")
        user = User.objects.get(username="test_user")
        Directory.objects.create(name="test_dir", owner=user)
        File.objects.create(name="test_file.c", owner=user, parent=Directory.objects.get(name="test_dir"))

    def test_save_file(self):
        response = self.client.post('/code_editor/save/' + str(File.objects.get(name="test_file.c").id))
        self.assertEqual(response.status_code, 200)


class DeleteViewTest(TestCase):
    def setUp(self):
        User.objects.create_user(username="test_user", password="test_password")
        user = User.objects.get(username="test_user")
        Directory.objects.create(name="test_dir", owner=user)
        File.objects.create(name="test_file.c", owner=user, parent=Directory.objects.get(name="test_dir"))

    def test_delete_file(self):
        self.client.login(username="test_user", password="test_password")
        response = self.client.post('/code_editor/delete_file/' + str(File.objects.get(name="test_file.c").id))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(File.objects.filter(name="test_file.c")[0].available)

    def test_delete_dir(self):
        self.client.login(username="test_user", password="test_password")
        response = self.client.post('/code_editor/delete_dir/' + str(Directory.objects.get(name="test_dir").id))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Directory.objects.filter(name="test_dir")[0].available)


class ChooseViewTest(TestCase):
    def test_delete_choose(self):
        response = self.client.post('/code_editor/delete/')
        self.assertEqual(response.status_code, 200)

    def test_add_dir_choose(self):
        response = self.client.post('/code_editor/add_dir/')
        self.assertEqual(response.status_code, 200)

    def test_add_file_choose(self):
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
