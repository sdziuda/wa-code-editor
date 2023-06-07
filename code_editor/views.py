from django.shortcuts import render
from code_editor.models import Directory, File, Section, SectionType
from django.template import loader
from django.http import HttpResponseRedirect, HttpResponse
from .forms import StandardForm, OptimizationForm, ProcessorForm, MCS51Form, Z80Form, STM8Form, DirForm, FileForm,\
                   UploadFileForm
import json
import os
import subprocess


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
        context['file'] = [{'content': '', 'ind': 1}]
    else:
        file = File.objects.get(id=file_id)

        if file.owner != request.user:
            context['file'] = [{'content': 'You are not the owner of this file', 'ind': 1}]
        else:
            context['file'] = [{'ind': ind + 1, 'content': line} for ind, line in enumerate(file.content.splitlines())]


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


def set_to_session(request):
    if b'standard_opt' in request.body:
        data = json.loads(request.body.decode('utf-8'))
        std = data['standard_opt']
        request.session['standard'] = std
    if b'optimization_opt' in request.body:
        data = json.loads(request.body.decode('utf-8'))
        speed = data['optimization_opt']['speed']
        reverse = data['optimization_opt']['reverse']
        nolab = data['optimization_opt']['nolab']
        optim = opt_to_val(speed, reverse, nolab)
        request.session['optimization'] = optim
    if b'processor_opt' in request.body:
        data = json.loads(request.body.decode('utf-8'))
        proc = data['processor_opt']
        request.session['processor'] = proc
    if b'mcs51_opt' in request.body:
        data = json.loads(request.body.decode('utf-8'))
        mcs51 = data['mcs51_opt']
        request.session['mcs51'] = mcs51
    if b'z80_opt' in request.body:
        data = json.loads(request.body.decode('utf-8'))
        callee = data['z80_opt']['callee']
        reserve = data['z80_opt']['reserve']
        z80 = val_to_z80(callee, reserve)
        request.session['z80'] = z80
    if b'stm8_opt' in request.body:
        data = json.loads(request.body.decode('utf-8'))
        stm8 = data['stm8_opt']
        request.session['stm8'] = stm8


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
        request.session['file_id'] = file_id
        return render(request, 'main.html', context)

    if request.method == 'POST':
        set_to_session(request)

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


def split_section(section, ind, file_name):
    title_count = 0
    i = 0
    title = ''
    while i < len(section.splitlines()):
        title += section.splitlines()[i] + '\n'
        if section.splitlines()[i].startswith(';---------------') and title_count != 1:
            title_count += 1
        elif section.splitlines()[i].startswith(';---------------') and title_count == 1:
            break
        i += 1

    section_content = []
    for line in section.splitlines()[i + 1:]:
        if line.startswith(';'):
            line_cpy = line[1:]
            line_cpy = line_cpy.lstrip()
            if line_cpy.startswith(file_name):
                line_cpy = line_cpy[len(file_name) + 1:]
                line_id = line_cpy.split()[0][:-1]
                section_content.append({'id': line_id, 'content': line})
            else:
                section_content.append({'id': None, 'content': line})
        else:
            section_content.append({'id': None, 'content': line})

    return {'title': title, 'content': section_content, 'id': ind}


def split_error(text, file_name):
    error_content = []
    for line in text.splitlines():
        if line.startswith(file_name):
            line_cpy = line[len(file_name) + 1:]
            line_id = line_cpy.split()[0]
            line_id = line_id.split(':')[0]
            error_content.append({'id': line_id, 'content': line})
        else:
            error_content.append({'id': None, 'content': line})

    return error_content


def split_sections(text, file_name):
    sections = []
    section = ''
    i = 0
    while i < len(text.splitlines()):
        if text.splitlines()[i].startswith(';---------------') and text.splitlines()[i + 1][0] == ';' and \
                ((text.splitlines()[i + 1][1].isupper() and not text.splitlines()[i - 1][1].isupper()) or
                 (text.splitlines()[i + 1][1] == ' ' and text.splitlines()[i + 1][2].isupper())):
            if section != '':
                sections.append(split_section(section, len(sections), file_name))
            section = ''
        section += text.splitlines()[i] + '\n'
        i += 1
    sections.append(split_section(section, len(sections), file_name))

    return sections


def compile_file(request, file_id):
    file = File.objects.get(id=file_id)
    context = {'file_id': file_id}

    std, optim, proc, mcs51, z80, stm8 = get_from_session(request)

    proc_opt = ''
    if proc == 'mcs51':
        proc_opt = mcs51
    elif proc == 'z80':
        proc_opt = z80
    elif proc == 'stm8':
        proc_opt = stm8

    std_cmd = '--std-' + std
    optim_cmd = opt_to_cmd(optim)
    proc_cmd = '-m' + proc
    if proc == 'mcs51' or proc == 'stm8':
        proc_opt_cmd = '--model-' + proc_opt
    else:
        proc_opt_cmd = z80_proc_opt_to_cmd(proc_opt)

    cmd = 'sdcc -S ' + std_cmd + ' ' + optim_cmd + ' ' + proc_cmd + ' ' + proc_opt_cmd + ' ' + file.name
    cmd = cmd.replace('  ', ' ')
    file_to_compile = open(file.name, 'w')
    for line in file.content.split('\r\n'):
        file_to_compile.write(line + '\n')
    file_to_compile.close()

    shell_result = subprocess.run(cmd, shell=True, check=False, stderr=subprocess.PIPE, stdout=subprocess.PIPE,
                                  text=True)

    if shell_result.returncode == 0:
        compiled_file = open(file.name[:-2] + '.asm', 'r')
        context['compilation_status'] = 'Compilation successful'
        context['compiled_file'] = compiled_file.read()
        compiled_file.close()
        context['compiled_sections'] = split_sections(context['compiled_file'], file.name)
    else:
        context['compilation_status'] = 'Compilation error'
        context['compiled_file'] = shell_result.stderr
        context['compiled_errors'] = split_error(shell_result.stderr, file.name)

    request.session['compiled_file'] = context['compiled_file']

    if os.path.isfile(file.name[:-2] + '.asm'):
        os.remove(file.name[:-2] + '.asm')
    os.remove(file.name)

    return render(request, 'snippet.html', context)


def save_file(request, file_id):
    if not request.user.is_authenticated:
        return render(request, 'index.html')

    directories = Directory.objects.filter(owner=request.user, parent=None, available=True)

    file = File.objects.get(id=file_id)
    name = file.name[:-2] + '.asm'
    if file.owner != request.user:
        context = {
            'subfiles': files_tree_maker(directories),
            'file': 'You are not the owner of this file'
        }
        return render(request, 'index.html', context)

    compiled_file = request.session['compiled_file']
    response = HttpResponse(compiled_file, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=' + name

    return response


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


def delete_file_no(request, file_id):
    if request.user.is_authenticated:
        file = File.objects.get(id=file_id)
        if file.owner == request.user:
            file.delete_file()
    return HttpResponse()


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


def delete_dir_no(request, dir_id):
    if request.user.is_authenticated:
        directory = Directory.objects.get(id=dir_id)
        if directory.owner == request.user:
            directory.delete_directory()
    return HttpResponse()


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


def find_variables(text):
    res = []
    it = 0
    for line in text.splitlines():
        sline = line.split()
        it += 1
        if len(sline) > 0:
            if sline[0] == 'int' or sline[0] == 'float' or sline[0] == 'double' or sline[0] == 'char' \
                    or sline[0] == 'bool' or sline[0] == 'string' or sline[0] == 'long' or sline[0] == 'short':
                if sline[1][-1] == ';':
                    res.append((it, it))
                elif sline[2] == '=' and sline[3][-1] == ';':
                    res.append((it, it))
    return res


def find_directives(text):
    res = []
    it = 0
    for line in text.splitlines():
        sline = line.split()
        it += 1
        if len(sline) > 0:
            if sline[0] == '#include' or sline[0] == '#define' or sline[0] == '#undef' or sline[0] == '#error' \
                    or sline[0] == '#pragma' or sline[0] == '#line':
                res.append((it, it))
    return res


def find_asm(text):
    res = []
    it = 0
    for line in text.splitlines():
        sline = line.split()
        it += 1
        if len(sline) > 0:
            if sline[0] == '__asm':
                end_it = it
                for line_end in text.splitlines()[it:]:
                    end_it += 1
                    if len(line_end) > 0 and line_end.split()[0] == '__endasm;':
                        res.append((it, end_it))
                        break
    return res


def find_comments(text):
    res = []
    it = 0
    for line in text.splitlines():
        it += 1
        if line.find('//') != -1:
            res.append((it, it))
        elif line.find('/*') != -1:
            if line.find('*/') != -1:
                res.append((it, it))
            else:
                end_it = it
                for line_end in text.splitlines()[it:]:
                    end_it += 1
                    if line_end.find('*/') != -1:
                        res.append((it, end_it))
                        break
    return res


def find_functions(text):
    res = []
    it = 0
    for line in text.splitlines():
        it += 1
        if line.find('(') != -1 and line.find(')') != -1 and not line.split()[0].startswith('if') \
                and not line.split()[0].startswith('for') and not line.split()[0].startswith('while') \
                and not line.split()[0].startswith('switch'):
            started = False
            l_count = 0
            r_count = 0
            if line.find('{') != -1:
                started = True
                l_count += 1
            end_it = it
            for line_end in text.splitlines()[it:]:
                end_it += 1
                if line_end.find('{') != -1:
                    started = True
                    l_count += 1
                if line_end.find('}') != -1:
                    r_count += 1
                if started and l_count == r_count:
                    res.append((it, end_it))
                    break
    return res


def split_file_to_sections(text):
    res = {
        'variables': find_variables(text),
        'directives': find_directives(text),
        'asm': find_asm(text),
        'comments': find_comments(text),
        'functions': find_functions(text)
    }
    return res


def save_sections(file):
    sec = split_file_to_sections(file.content)
    var_sec = sec['variables']
    for v in var_sec:
        new_sec = Section(parent=file, start=v[0], end=v[1], name=f'var {v[0]}-{v[1]} {file.id}',
                          type=SectionType.VARIABLE_DECLARATION)
        new_sec.save()
    dir_sec = sec['directives']
    for d in dir_sec:
        new_sec = Section(parent=file, start=d[0], end=d[1], name=f'dir {d[0]}-{d[1]} {file.id}',
                          type=SectionType.COMPILER_DIRECTIVE)
        new_sec.save()
    asm_sec = sec['asm']
    for a in asm_sec:
        new_sec = Section(parent=file, start=a[0], end=a[1], name=f'asm {a[0]}-{a[1]} {file.id}',
                          type=SectionType.ASEMBLER_CODE)
        new_sec.save()
    com_sec = sec['comments']
    for c in com_sec:
        new_sec = Section(parent=file, start=c[0], end=c[1], name=f'com {c[0]}-{c[1]} {file.id}',
                          type=SectionType.COMMENT)
        new_sec.save()
    fun_sec = sec['functions']
    for f in fun_sec:
        new_sec = Section(parent=file, start=f[0], end=f[1], name=f'fun {f[0]}-{f[1]} {file.id}',
                          type=SectionType.PROCEDURE)
        new_sec.save()


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
                save_sections(new_file)
        elif 'upload' in request.POST:
            up_form = UploadFileForm(request.POST, request.FILES)
            if up_form.is_valid():
                uploaded_file = request.FILES['file']
                new_file = File(name=uploaded_file.name, desc='', content=uploaded_file.read().decode('utf-8'),
                                owner=request.user, parent=directory)
                new_file.save()
                save_sections(new_file)
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
