from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User, Group
from .models import Directory, File, Section, AppUser

admin.site.register(Section)


class AppUserInline(admin.TabularInline):
    model = AppUser
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = [AppUserInline]


admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(User, UserAdmin)


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
