from django import forms


class StandardForm(forms.Form):
    std = forms.ChoiceField(choices=[('c89', 'C89'), ('c99', 'C99'), ('c11', 'C11')],
                            label='Choose C standard')


class OptimizationForm(forms.Form):
    speed = forms.BooleanField(label='--opt-code-speed', required=False)
    reverse = forms.BooleanField(label='--noloopreverse', required=False)
    nolab = forms.BooleanField(label='--nolabelopt', required=False)


class ProcessorForm(forms.Form):
    proc = forms.ChoiceField(choices=[('mcs51', 'MCS51'), ('z80', 'Z80'), ('stm8', 'STM8')],
                             label='Choose processor')


class MCS51Form(forms.Form):
    mcs51 = forms.ChoiceField(choices=[('small', 'small'), ('medium', 'medium'), ('large', 'large'), ('huge', 'huge')],
                              label='Choose model')


class Z80Form(forms.Form):
    callee = forms.BooleanField(label='--callee-saves-bc', required=False)
    reserve = forms.BooleanField(label='--reserve-regs-iy', required=False)


class STM8Form(forms.Form):
    stm8 = forms.ChoiceField(choices=[('medium', 'medium'), ('large', 'large')],
                             label='Choose model')


class DirForm(forms.Form):
    name = forms.CharField(label="Name", max_length=200)
    desc = forms.CharField(label="Description (optional)", max_length=600, required=False)


class UploadFileForm(forms.Form):
    file = forms.FileField(label="Upload file")


class FileForm(forms.Form):
    name = forms.CharField(label="Name", max_length=200)
    desc = forms.CharField(label="Description (optional)", max_length=600, required=False)
    content = forms.CharField(label="Content", max_length=2000000, widget=forms.Textarea)
