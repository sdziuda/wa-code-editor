# Generated by Django 4.0.2 on 2023-04-30 19:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Directory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('desc', models.CharField(blank=True, max_length=600)),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='creation date')),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name='last modified')),
                ('available', models.BooleanField(default=True)),
                ('availability_change_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='availability change date')),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='code_editor.directory')),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('content', models.TextField(blank=True)),
                ('desc', models.CharField(blank=True, max_length=600)),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='creation date')),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name='last modified')),
                ('available', models.BooleanField(default=True)),
                ('availability_change_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='availability change date')),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='code_editor.directory')),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200)),
                ('desc', models.CharField(blank=True, max_length=600)),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='creation date')),
                ('section_start', models.IntegerField()),
                ('section_end', models.IntegerField()),
                ('status_desc', models.CharField(blank=True, max_length=600)),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='code_editor.file')),
            ],
        ),
    ]
