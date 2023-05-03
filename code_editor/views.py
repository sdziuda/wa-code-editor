from django import forms
from django.shortcuts import render
from code_editor.models import Directory, File
from django.template import loader
from django.http import HttpResponseRedirect
import os


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


class OptimizationForm(forms.Form):
    speed = forms.BooleanField(label='--opt-code-speed', required=False)
    reverse = forms.BooleanField(label='--noloopreverse', required=False)
    nolab = forms.BooleanField(label='--nolabelopt', required=False)


def opt_to_val(speed, reverse, nolab):
    if speed and reverse and nolab:
        return 'speed+reverse+nolab'
    elif speed and reverse:
        return 'speed+reverse'
    elif speed and nolab:
        return 'speed+nolab'
    elif reverse and nolab:
        return 'reverse+nolab'
    elif speed:
        return 'speed'
    elif reverse:
        return 'reverse'
    elif nolab:
        return 'nolab'
    else:
        return 'none'


def val_to_opt(opt):
    if opt == 'speed+reverse+nolab':
        return True, True, True
    elif opt == 'speed+reverse':
        return True, True, False
    elif opt == 'speed+nolab':
        return True, False, True
    elif opt == 'reverse+nolab':
        return False, True, True
    elif opt == 'speed':
        return True, False, False
    elif opt == 'reverse':
        return False, True, False
    elif opt == 'nolab':
        return False, False, True
    else:
        return False, False, False


class ProcessorForm(forms.Form):
    proc = forms.ChoiceField(choices=[('mcs51', 'MCS51'), ('z80', 'Z80'), ('stm8', 'STM8')],
                             label='Choose processor')


class MCS51Form(forms.Form):
    mcs51 = forms.ChoiceField(choices=[('small', 'small'), ('medium', 'medium'), ('large', 'large'), ('huge', 'huge')],
                              label='Choose model')


class Z80Form(forms.Form):
    callee = forms.BooleanField(label='--callee-saves-bc', required=False)
    reserve = forms.BooleanField(label='--reserve-regs-iy', required=False)


def z80_to_val(z80):
    if z80 == 'none':
        return False, False
    elif z80 == 'callee':
        return True, False
    elif z80 == 'reserve':
        return False, True
    else:
        return True, True


def val_to_z80(callee, reserve):
    if callee and reserve:
        return 'callee+reserve'
    elif callee:
        return 'callee'
    elif reserve:
        return 'reserve'
    else:
        return 'none'


class STM8Form(forms.Form):
    stm8 = forms.ChoiceField(choices=[('medium', 'medium'), ('large', 'large')],
                             label='Choose model')


def get_from_session(request):
    if 'standard' in request.session:
        std = request.session['standard']
    else:
        request.session['standard'] = 'c89'
        std = 'c89'

    if 'optimization' in request.session:
        optim = request.session['optimization']
    else:
        request.session['optimization'] = 'none'
        optim = 'none'

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

    if 'z80' in request.session:
        z80 = request.session['z80']
    else:
        request.session['z80'] = 'none'
        z80 = 'none'

    if 'stm8' in request.session:
        stm8 = request.session['stm8']
    else:
        request.session['stm8'] = 'medium'
        stm8 = 'medium'

    return std, optim, proc, mcs51, z80, stm8


def index(request, file_id=None):
    if not request.user.is_authenticated:
        return render(request, 'index.html')

    directories = Directory.objects.filter(owner=request.user, parent=None, available=True)
    context = {'subfiles': files_tree_maker(directories)}

    std, optim, proc, mcs51, z80, stm8 = get_from_session(request)

    context['std'] = std
    context['optim'] = optim
    context['proc'] = proc
    context['mcs51'] = mcs51
    context['z80'] = z80
    context['stm8'] = stm8
    std_form = StandardForm()
    optim_form = OptimizationForm()
    proc_form = ProcessorForm()
    mcs51_form = MCS51Form()
    z80_form = Z80Form()
    stm8_form = STM8Form()
    std_form.initial['std'] = std
    optim_form.initial['speed'], optim_form.initial['reverse'], optim_form.initial['nolab'] = val_to_opt(optim)
    proc_form.initial['proc'] = proc
    mcs51_form.initial['mcs51'] = mcs51
    z80_form.initial['callee'], z80_form.initial['reserve'] = z80_to_val(z80)
    stm8_form.initial['stm8'] = stm8
    context['std_form'] = std_form
    context['optim_form'] = optim_form
    context['proc_form'] = proc_form
    context['mcs51_form'] = mcs51_form
    context['z80_form'] = z80_form
    context['stm8_form'] = stm8_form
    set_file(request, file_id, context)
    if file_id is not None:
        context['file_id'] = file_id

    if request.method == 'POST':
        if 'standard_opt' in request.POST:
            std_form = StandardForm(request.POST)
            if std_form.is_valid():
                std = std_form.cleaned_data['std']
                request.session['standard'] = std

            context['std_form'] = std_form
            context['std'] = std
        if 'optimization_opt' in request.POST:
            optim_form = OptimizationForm(request.POST)
            if optim_form.is_valid():
                optim = opt_to_val(optim_form.cleaned_data['speed'], optim_form.cleaned_data['reverse'],
                                   optim_form.cleaned_data['nolab'])
                request.session['optimization'] = optim

            context['optim_form'] = optim_form
            context['optim'] = optim
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
        if 'z80_opt' in request.POST:
            z80_form = Z80Form(request.POST)
            if z80_form.is_valid():
                z80 = val_to_z80(z80_form.cleaned_data['callee'], z80_form.cleaned_data['reserve'])
                request.session['z80'] = z80

            context['z80_form'] = z80_form
            context['z80'] = z80
        if 'stm8_opt' in request.POST:
            stm8_form = STM8Form(request.POST)
            if stm8_form.is_valid():
                stm8 = stm8_form.cleaned_data['stm8']
                request.session['stm8'] = stm8

            context['stm8_form'] = stm8_form
            context['stm8'] = stm8

    return render(request, 'index.html', context)


def opt_to_cmd(opt):
    res = ''
    if 'speed' in opt:
        res += ' --opt-code-speed'
    if 'reverse' in opt:
        res += ' --noloopreverse'
    if 'nolab' in opt:
        res += ' --nolabelopt'
    return res


def z80_proc_opt_to_cmd(opt):
    res = ''
    if 'callee' in opt:
        res += ' --callee-saves-bc'
    if 'reserve' in opt:
        res += ' --reserve-regs-iy'
    return res


def compile_no_file(request):
    return HttpResponseRedirect('/')


def compile_file(request, file_id):
    if not request.user.is_authenticated:
        return render(request, 'index.html')

    directories = Directory.objects.filter(owner=request.user, parent=None, available=True)
    context = {'file_id': file_id, 'subfiles': files_tree_maker(directories)}
    file = File.objects.get(id=file_id)
    if file is None:
        context['file'] = 'File not found'
    if file.owner != request.user:
        context['file'] = 'You are not the owner of this file'

    std, optim, proc, mcs51, z80, stm8 = get_from_session(request)

    context['std'] = std
    context['optim'] = optim
    context['proc'] = proc
    if proc == 'mcs51':
        context['proc_opt'] = mcs51
    elif proc == 'z80':
        context['proc_opt'] = z80
    elif proc == 'stm8':
        context['proc_opt'] = stm8
    context['mcs51'] = mcs51
    context['z80'] = z80
    context['stm8'] = stm8
    context['std_form'] = StandardForm(initial={'std': std})
    context['optim_form'] = OptimizationForm()
    context['proc_form'] = ProcessorForm(initial={'proc': proc})
    context['mcs51_form'] = MCS51Form(initial={'mcs51': mcs51})
    context['z80_form'] = Z80Form()
    context['stm8_form'] = STM8Form(initial={'stm8': stm8})
    proc_opt = context['proc_opt']
    context['file_name'] = ''

    if file is not None and file.owner == request.user:
        context['file'] = file.content
        context['file_name'] = file.name

    if request.method == 'POST':
        if 'standard_opt' in request.POST:
            std_form = StandardForm(request.POST)
            if std_form.is_valid():
                std = std_form.cleaned_data['std']
                request.session['standard'] = std

            context['std_form'] = std_form
            context['std'] = std
        if 'optimization_opt' in request.POST:
            optim_form = OptimizationForm(request.POST)
            if optim_form.is_valid():
                optim = opt_to_val(optim_form.cleaned_data['speed'], optim_form.cleaned_data['reverse'],
                                   optim_form.cleaned_data['nolab'])
                request.session['optimization'] = optim

            context['optim_form'] = optim_form
            context['optim'] = optim
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
        if 'z80_opt' in request.POST:
            z80_form = Z80Form(request.POST)
            if z80_form.is_valid():
                z80 = val_to_z80(z80_form.cleaned_data['callee'], z80_form.cleaned_data['reserve'])
                request.session['z80'] = z80

            context['z80_form'] = z80_form
            context['z80'] = z80
        if 'stm8_opt' in request.POST:
            stm8_form = STM8Form(request.POST)
            if stm8_form.is_valid():
                stm8 = stm8_form.cleaned_data['stm8']
                request.session['stm8'] = stm8

            context['stm8_form'] = stm8_form
            context['stm8'] = stm8
    else:
        std_cmd = '--std-' + std
        optim_cmd = opt_to_cmd(optim)
        proc_cmd = '-m' + proc
        if proc == 'mcs51' or proc == 'stm8':
            proc_opt_cmd = '--model-' + proc_opt
        else:
            proc_opt_cmd = z80_proc_opt_to_cmd(proc_opt)

        cmd = 'sdcc -S ' + std_cmd + ' ' + optim_cmd + ' ' + proc_cmd + ' ' + proc_opt_cmd + ' ' + context['file_name']
        file_to_compile = open(file.name, 'w')
        for line in file.content.split('\n'):
            file_to_compile.write(line)
        file_to_compile.close()
        os.system(cmd)

        if os.path.isfile(file.name[:-2] + '.asm'):
            compiled_file = open(file.name[:-2] + '.asm', 'r')
            context['compiled_file'] = compiled_file.read()
            compiled_file.close()
        else:
            context['compiled_file'] = 'Compilation error'

        if os.name == 'nt':
            if os.path.isfile(file.name[:-2] + '.asm'):
                os.system('del ' + file.name[:-2] + '.asm')
            os.system('del ' + file.name)
        else:
            if os.path.isfile(file.name[:-2] + '.asm'):
                os.system('rm ' + file.name[:-2] + '.asm')
            os.system('rm ' + file.name)

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


class UploadFileForm(forms.Form):
    file = forms.FileField(label="Upload file")


class FileForm(forms.Form):
    name = forms.CharField(label="Name", max_length=200)
    desc = forms.CharField(label="Description (optional)", max_length=600, required=False)
    content = forms.CharField(label="Content", max_length=2000000, widget=forms.Textarea)


def add_file(request, dir_id):
    next_red = request.GET.get('next', '/')
    if not request.user.is_authenticated:
        return render(request, 'index.html')

    if request.method == 'POST':
        directory = Directory.objects.get(id=dir_id)
        if 'add' in request.POST:
            form = FileForm(request.POST)
            if form.is_valid():
                new_file = File(name=form.cleaned_data['name'], desc=form.cleaned_data['desc'],
                                content=form.cleaned_data['content'], owner=request.user, parent=directory)
                new_file.save()
        elif 'upload' in request.POST:
            up_form = UploadFileForm(request.POST, request.FILES)
            if up_form.is_valid():
                uploaded_file = request.FILES['file']
                new_file = File(name=uploaded_file.name, desc='', content=uploaded_file.read().decode('utf-8'),
                                owner=request.user, parent=directory)
                new_file.save()
            else:
                print(up_form.errors)
        return HttpResponseRedirect(next_red)
    else:
        form = FileForm()
        up_form = UploadFileForm()
        context = {
            'form': form,
            'up_form': up_form,
            'dir_id': dir_id
        }
        return render(request, 'file_tree/add_file.html', context)
