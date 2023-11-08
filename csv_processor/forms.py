from django import forms

class CSVUploadForm(forms.Form):
    csv_files = forms.FileField()
    column_to_process = forms.IntegerField()
