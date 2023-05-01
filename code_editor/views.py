from django import forms
from django.shortcuts import render
from code_editor.models import Directory, File
from django.template import loader
from django.http import HttpResponseRedirect


def files_tree_maker(directories):
    def get_subfiles(directory):
        subdirectories = directory.get_directories()
        for subdirectory in subdirectories:
            subfiles = get_subfiles(subdirectory)
            yield loader.render_to_string('file_tree/tree_dir.html',
                                          {'file': subdirectory, 'subfiles': subfiles})
        files = directory.get_files()
        for f in files:
            yield loader.render_to_string('file_tree/tree_file.html', {'file': f})

    for dire in directories:
        sub = get_subfiles(dire)
        yield loader.render_to_string('file_tree/tree_dir.html', {'file': dire, 'subfiles': sub})


def delete_files_tree_maker(directories):
    def get_subfiles(directory):
        subdirectories = directory.get_directories()
        for subdirectory in subdirectories:
            subfiles = get_subfiles(subdirectory)
            yield loader.render_to_string('file_tree/tree_dir_delete.html',
                                          {'file': subdirectory, 'subfiles': subfiles})
        files = directory.get_files()
        for f in files:
            yield loader.render_to_string('file_tree/tree_file_delete_only.html', {'file': f})

    for dire in directories:
        sub = get_subfiles(dire)
        yield loader.render_to_string('file_tree/tree_dir_delete.html', {'file': dire, 'subfiles': sub})


def add_dir_files_tree_maker(directories):
    def get_subfiles(directory):
        subdirectories = directory.get_directories()
        for subdirectory in subdirectories:
            subfiles = get_subfiles(subdirectory)
            yield loader.render_to_string('file_tree/tree_dir_add_dir.html',
                                          {'file': subdirectory, 'subfiles': subfiles})
        files = directory.get_files()
        for f in files:
            yield loader.render_to_string('file_tree/tree_file_no_opt.html', {'file': f})

    yield loader.render_to_string('file_tree/add_root.html')
    for dire in directories:
        sub = get_subfiles(dire)
        yield loader.render_to_string('file_tree/tree_dir_add_dir.html', {'file': dire, 'subfiles': sub})


def add_file_files_tree_maker(directories):
    def get_subfiles(directory):
        subdirectories = directory.get_directories()
        for subdirectory in subdirectories:
            subfiles = get_subfiles(subdirectory)
            yield loader.render_to_string('file_tree/tree_dir_add_file.html',
                                          {'file': subdirectory, 'subfiles': subfiles})
        files = directory.get_files()
        for f in files:
            yield loader.render_to_string('file_tree/tree_file_no_opt.html', {'file': f})

    for dire in directories:
        sub = get_subfiles(dire)
        yield loader.render_to_string('file_tree/tree_dir_add_file.html', {'file': dire, 'subfiles': sub})


def index(request, file_id=None):
    if not request.user.is_authenticated:
        return render(request, 'index.html')
    directories = Directory.objects.filter(owner=request.user, parent=None, available=True)

    context = {
        'subfiles': files_tree_maker(directories)
    }
    if file_id is None:
        return render(request, 'index.html', context)
    else:
        file = File.objects.get(id=file_id)

        if file.owner != request.user:
            context['file'] = 'You are not the owner of this file'
            return render(request, 'index.html', context)

        context['file'] = file.content
        return render(request, 'index.html', context)


def delete_file(request, file_id):
    next_red = request.GET.get('next', '/')
    if not request.user.is_authenticated:
        return render(request, 'index.html')
    file = File.objects.get(id=file_id)
    directories = Directory.objects.filter(owner=request.user, parent=None, available=True)
    if file.owner != request.user:
        context = {
            'subfiles': files_tree_maker(directories),
            'file': 'You are not the owner of this file'
        }
        return render(request, 'index.html', context)
    file.delete_file()
    return HttpResponseRedirect(next_red)


def delete_dir(request, dir_id):
    next_red = request.GET.get('next', '/')
    if not request.user.is_authenticated:
        return render(request, 'index.html')
    directory = Directory.objects.get(id=dir_id)
    directories = Directory.objects.filter(owner=request.user, parent=None, available=True)
    if directory.owner != request.user:
        context = {
            'subfiles': files_tree_maker(directories),
            'file': 'You are not the owner of this directory'
        }
        return render(request, 'index.html', context)
    directory.delete_directory()
    return HttpResponseRedirect(next_red)


def delete_choose(request):
    if not request.user.is_authenticated:
        return render(request, 'index.html')
    directories = Directory.objects.filter(owner=request.user, parent=None, available=True)

    context = {
        'subfiles': delete_files_tree_maker(directories)
    }
    return render(request, 'file_tree/choose.html', context)


def add_dir_choose(request):
    if not request.user.is_authenticated:
        return render(request, 'index.html')
    directories = Directory.objects.filter(owner=request.user, parent=None, available=True)

    context = {
        'subfiles': add_dir_files_tree_maker(directories)
    }
    return render(request, 'file_tree/choose.html', context)


def add_file_choose(request):
    if not request.user.is_authenticated:
        return render(request, 'index.html')
    directories = Directory.objects.filter(owner=request.user, parent=None, available=True)

    context = {
        'subfiles': add_file_files_tree_maker(directories)
    }
    return render(request, 'file_tree/choose.html', context)


class DirForm(forms.Form):
    name = forms.CharField(label="Name", max_length=200)
    desc = forms.CharField(label="Description (optional)", max_length=600, required=False)


def add_dir(request, dir_id):
    next_red = request.GET.get('next', '/')
    if not request.user.is_authenticated:
        return render(request, 'index.html')

    if request.method == 'POST':
        form = DirForm(request.POST)
        if form.is_valid():
            if dir_id != 0:
                directory = Directory.objects.get(id=dir_id)
            else:
                directory = None
            new_dir = Directory(name=form.cleaned_data['name'], desc=form.cleaned_data['desc'],
                                owner=request.user, parent=directory)
            new_dir.save()
            return HttpResponseRedirect(next_red)
    else:
        form = DirForm()
        context = {
            'form': form,
            'dir_id': dir_id
        }
        return render(request, 'file_tree/add_dir.html', context)


class FileForm(forms.Form):
    name = forms.CharField(label="Name", max_length=200)
    desc = forms.CharField(label="Description (optional)", max_length=600, required=False)
    content = forms.CharField(label="Content", max_length=2000000, widget=forms.Textarea)


def add_file(request, dir_id):
    next_red = request.GET.get('next', '/')
    if not request.user.is_authenticated:
        return render(request, 'index.html')

    if request.method == 'POST':
        form = FileForm(request.POST)
        if form.is_valid():
            directory = Directory.objects.get(id=dir_id)
            new_file = File(name=form.cleaned_data['name'], desc=form.cleaned_data['desc'],
                            content=form.cleaned_data['content'], owner=request.user, parent=directory)
            new_file.save()
            return HttpResponseRedirect(next_red)
    else:
        form = FileForm()
        context = {
            'form': form,
            'dir_id': dir_id
        }
        return render(request, 'file_tree/add_file.html', context)
