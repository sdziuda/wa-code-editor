from django.test import TestCase
from django.contrib.auth.models import User
from code_editor.models import Directory, File, Section, AppUser


class AppUserTest(TestCase):
    def setUp(self):
        AppUser.objects.create(nick="test_nick", user=User.objects.create_user(username="test_user",
                                                                               password="test_password"))

    def test_app_user(self):
        test_user = AppUser.objects.get(nick="test_nick")
        self.assertEqual(test_user.user.username, "test_user")


class DirectoryTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username="test_user", password="test_password")
        user2 = User.objects.create_user(username="test_user2", password="test_password2")
        Directory.objects.create(name="test_dir", owner=user)
        Directory.objects.create(name="test_dir_inside", owner=user, parent=Directory.objects.get(name="test_dir"))
        Directory.objects.create(name="test_dir2", owner=user2)

    def test_directory(self):
        test_dir = Directory.objects.get(name="test_dir")
        self.assertEqual(test_dir.owner.username, "test_user")

    def test_get_directories(self):
        test_dir = Directory.objects.get(name="test_dir")
        test_dir_inside = Directory.objects.get(name="test_dir_inside")
        test_dir2 = Directory.objects.get(name="test_dir2")
        self.assertEqual(test_dir.get_directories(), [test_dir_inside])
        self.assertEqual(test_dir2.get_directories(), [])

    def test_user_directories(self):
        user = User.objects.get(username="test_user")
        user2 = User.objects.get(username="test_user2")
        test_dir = Directory.objects.get(name="test_dir")
        test_dir_inside = Directory.objects.get(name="test_dir_inside")
        test_dir2 = Directory.objects.get(name="test_dir2")
        for directory in Directory.objects.filter(owner=user):
            self.assertTrue(directory in [test_dir, test_dir_inside])
        for directory in Directory.objects.filter(owner=user2):
            self.assertTrue(directory in [test_dir2])


class FileTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username="test_user", password="test_password")
        user2 = User.objects.create_user(username="test_user2", password="test_password2")
        Directory.objects.create(name="test_dir", owner=user)
        Directory.objects.create(name="test_dir_inside", owner=user, parent=Directory.objects.get(name="test_dir"))
        Directory.objects.create(name="test_dir2", owner=user2)
        File.objects.create(name="test_file", owner=user, parent=Directory.objects.get(name="test_dir"))
        File.objects.create(name="test_file2", owner=user, parent=Directory.objects.get(name="test_dir_inside"))
        File.objects.create(name="test_file3", owner=user2, parent=Directory.objects.get(name="test_dir2"))

    def test_file(self):
        test_file = File.objects.get(name="test_file")
        self.assertEqual(test_file.owner.username, "test_user")

    def test_get_files(self):
        test_dir = Directory.objects.get(name="test_dir")
        test_dir_inside = Directory.objects.get(name="test_dir_inside")
        test_dir2 = Directory.objects.get(name="test_dir2")
        test_file = File.objects.get(name="test_file")
        test_file2 = File.objects.get(name="test_file2")
        test_file3 = File.objects.get(name="test_file3")
        self.assertEqual(test_dir.get_files(), [test_file])
        self.assertEqual(test_dir_inside.get_files(), [test_file2])
        self.assertEqual(test_dir2.get_files(), [test_file3])

    def test_user_files(self):
        user = User.objects.get(username="test_user")
        user2 = User.objects.get(username="test_user2")
        test_file = File.objects.get(name="test_file")
        test_file2 = File.objects.get(name="test_file2")
        test_file3 = File.objects.get(name="test_file3")
        for file in File.objects.filter(owner=user):
            self.assertTrue(file in [test_file, test_file2])
        for file in File.objects.filter(owner=user2):
            self.assertTrue(file in [test_file3])


class SectionTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username="test_user", password="test_password")
        Directory.objects.create(name="test_dir", owner=user)
        File.objects.create(name="test_file", owner=user, parent=Directory.objects.get(name="test_dir"))
        Section.objects.create(name="test_section", parent=File.objects.get(name="test_file"), start=0, end=10,
                               type="pro")
        Section.objects.create(name="test_section2", parent=File.objects.get(name="test_file"), start=10, end=20,
                               type="con")

    def test_section(self):
        test_section = Section.objects.get(name="test_section")
        self.assertEqual(test_section.type, "pro")

    def test_file_sections(self):
        test_file = File.objects.get(name="test_file")
        test_section = Section.objects.get(name="test_section")
        test_section2 = Section.objects.get(name="test_section2")
        for section in Section.objects.filter(parent=test_file):
            self.assertTrue(section in [test_section, test_section2])
