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


def set_file(request, file_id, context):
    if file_id is None:
        context['file'] = ''
    else:
        file = File.objects.get(id=file_id)

        if file.owner != request.user:
            context['file'] = 'You are not the owner of this file'
        else:
            context['file'] = file.content


class StandardForm(forms.Form):
    std = forms.ChoiceField(choices=[('c89', 'C89'), ('c99', 'C99'), ('c11', 'C11')],
                            label='Choose C standard')


class ProcessorForm(forms.Form):
    proc = forms.ChoiceField(choices=[('mcs51', 'MCS51'), ('z80', 'Z80'), ('stm8', 'STM8')],
                             label='Choose processor')


class MCS51Form(forms.Form):
    mcs51 = forms.ChoiceField(choices=[('small', 'small'), ('medium', 'medium'), ('large', 'large'), ('huge', 'huge')],
                              label='Choose model')


class STM8Form(forms.Form):
    stm8 = forms.ChoiceField(choices=[('medium', 'medium'), ('large', 'large')],
                             label='Choose model')


def index(request, file_id=None):
    if not request.user.is_authenticated:
        return render(request, 'index.html')

    directories = Directory.objects.filter(owner=request.user, parent=None, available=True)
    context = {'subfiles': files_tree_maker(directories)}

    if 'standard' in request.session:
        std = request.session['standard']
    else:
        request.session['standard'] = 'c89'
        std = 'c89'

    if 'processor' in request.session:
        proc = request.session['processor']
    else:
        request.session['processor'] = 'mcs51'
        proc = 'mcs51'

    if 'mcs51' in request.session:
        mcs51 = request.session['mcs51']
    else:
        request.session['mcs51'] = 'small'
        mcs51 = 'small'

    if 'stm8' in request.session:
        stm8 = request.session['stm8']
    else:
        request.session['stm8'] = 'medium'
        stm8 = 'medium'

    context['std'] = std
    context['proc'] = proc
    context['mcs51'] = mcs51
    context['stm8'] = stm8
    std_form = StandardForm()
    proc_form = ProcessorForm()
    mcs51_form = MCS51Form()
    stm8_form = STM8Form()
    std_form.initial['std'] = std
    proc_form.initial['proc'] = proc
    mcs51_form.initial['mcs51'] = mcs51
    stm8_form.initial['stm8'] = stm8
    context['std_form'] = std_form
    context['proc_form'] = proc_form
    context['mcs51_form'] = mcs51_form
    context['stm8_form'] = stm8_form
    set_file(request, file_id, context)

    if request.method == 'POST':
        if 'standard_opt' in request.POST:
            std_form = StandardForm(request.POST)
            if std_form.is_valid():
                std = std_form.cleaned_data['std']
                request.session['standard'] = std

            context['std_form'] = std_form
            context['std'] = std
        if 'processor_opt' in request.POST:
            proc_form = ProcessorForm(request.POST)
            if proc_form.is_valid():
                proc = proc_form.cleaned_data['proc']
                request.session['processor'] = proc

            context['proc_form'] = proc_form
            context['proc'] = proc
        if 'mcs51_opt' in request.POST:
            mcs51_form = MCS51Form(request.POST)
            if mcs51_form.is_valid():
                mcs51 = mcs51_form.cleaned_data['mcs51']
                request.session['mcs51'] = mcs51

            context['mcs51_form'] = mcs51_form
            context['mcs51'] = mcs51
        if 'stm8_opt' in request.POST:
            stm8_form = STM8Form(request.POST)
            if stm8_form.is_valid():
                stm8 = stm8_form.cleaned_data['stm8']
                request.session['stm8'] = stm8

            context['stm8_form'] = stm8_form
            context['stm8'] = stm8

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
