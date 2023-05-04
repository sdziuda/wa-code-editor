from django.contrib import admin

# Register your models here.
from .models import Directory, File, Section, AppUser

admin.site.register(Section)
admin.site.register(AppUser)


class SectionInline(admin.TabularInline):
    model = Section
    max_num = 0


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner')
    inlines = [SectionInline]


class FileInline(admin.TabularInline):
    model = File
    max_num = 0


@admin.register(Directory)
class DirectoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner')
    inlines = [FileInline]
