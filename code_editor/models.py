from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.
class Directory(models.Model):
    name = models.CharField(max_length=200)
    desc = models.CharField(max_length=600, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    creation_date = models.DateTimeField('creation date', auto_now_add=True)
    last_modified = models.DateTimeField('last modified', auto_now=True)
    available = models.BooleanField(default=True)
    availability_change_date = models.DateTimeField('availability change date', default=timezone.now)

    def __str__(self):
        return self.name

    def get_directories(self):
        return [subdirectory for subdirectory in Directory.objects.filter(parent=self, available=True)]

    def get_files(self):
        return [file for file in File.objects.filter(parent=self, available=True)]

    def delete_directory(self):
        self.available = False
        self.availability_change_date = timezone.now()
        self.save()


class File(models.Model):
    name = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    desc = models.CharField(max_length=600, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey(Directory, on_delete=models.CASCADE)
    creation_date = models.DateTimeField('creation date', auto_now_add=True)
    last_modified = models.DateTimeField('last modified', auto_now=True)
    available = models.BooleanField(default=True)
    availability_change_date = models.DateTimeField('availability change date', default=timezone.now)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return "/code_editor/%i/" % self.id

    def delete_file(self):
        self.available = False
        self.availability_change_date = timezone.now()
        self.save()


class SectionType(models.TextChoices):
    PROCEDURE = 'pro', 'procedure'
    COMMENT = 'com', 'comment'
    COMPILER_DIRECTIVE = 'dir', 'compiler directive'
    VARIABLE_DECLARATION = 'var', 'variable declaration'
    ASEMBLER_CODE = 'asm', 'asembler code'


class SectionStatus(models.TextChoices):
    WITH_WARNINGS = 'ww', 'compiling with warnings'
    COMPILING = 'co', 'compiling without warnings'
    NOT_COMPILING = 'nc', 'not compiling'


class Section(models.Model):
    name = models.CharField(max_length=200, blank=True)
    desc = models.CharField(max_length=600, blank=True)
    parent = models.ForeignKey(File, on_delete=models.CASCADE)
    creation_date = models.DateTimeField('creation date', auto_now_add=True)
    start = models.IntegerField()
    end = models.IntegerField()
    type = models.CharField(max_length=3, choices=SectionType.choices)
    status = models.CharField(max_length=2, choices=SectionStatus.choices, blank=True)
    status_desc = models.CharField(max_length=600, blank=True)

    def __str__(self):
        return self.name


class AppUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nick = models.CharField(max_length=200)

    def __str__(self):
        return self.nick
