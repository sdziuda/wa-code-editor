from django.shortcuts import render
from code_editor.models import Directory, File
from django.template import loader
from django.http import HttpResponseRedirect


def files_tree_maker(directories):
    def get_subfiles(directory):
        subdirectories = directory.get_directories()
        for subdirectory in subdirectories:
            subfiles = get_subfiles(subdirectory)
            yield loader.render_to_string('tree_dir.html',
                                          {'file': subdirectory, 'subfiles': subfiles})
        files = directory.get_files()
        for f in files:
            yield loader.render_to_string('tree_file.html', {'file': f})

    for dire in directories:
        sub = get_subfiles(dire)
        yield loader.render_to_string('tree_dir.html', {'file': dire, 'subfiles': sub})


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


def add_dir(request, dir_id):
    next_red = request.GET.get('next', '/')
    return HttpResponseRedirect(next_red)


def add_file(request, dir_id):
    next_red = request.GET.get('next', '/')
    return HttpResponseRedirect(next_red)
