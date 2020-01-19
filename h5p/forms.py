from django import forms


class H5PFileForm(forms.Form):
    h5p_file = forms.FileField(label="Choose a H5P File")
    name = forms.CharField(label="Name")


class H5PUpdateForm(forms.Form):
    h5p_file = forms.FileField(label="Upload H5P Official Release")
