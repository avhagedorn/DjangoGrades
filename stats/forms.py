from typing import Optional
from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField()

class UpdateWeightForm(forms.Form):

    def __init__(self, evals, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for t in evals: 
            self.fields[t] = forms.IntegerField(min_value=0, max_value=100, required=True)        

class CategoryForm(forms.Form):

    def __init__(self, categories, assignments, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for a in assignments:
            self.fields[a['title']] = forms.ChoiceField(choices = categories, required=True)

class GradelineForm(forms.Form):
    a = forms.IntegerField(label="A", min_value=0, max_value=100)
    a_minus = forms.IntegerField(label="A-", min_value=0, max_value=100)

    b_plus = forms.IntegerField(label="B+", min_value=0, max_value=100)
    b = forms.IntegerField(label="B", min_value=0, max_value=100)
    b_minus = forms.IntegerField(label="B-", min_value=0, max_value=100)

    c_plus = forms.IntegerField(label="C+", min_value=0, max_value=100)
    c = forms.IntegerField(label="C", min_value=0, max_value=100)
    c_minus = forms.IntegerField(label="C-", min_value=0, max_value=100)

    d_plus = forms.IntegerField(label="D+", min_value=0, max_value=100)
    d = forms.IntegerField(label="D", min_value=0, max_value=100)
    d_minus = forms.IntegerField(label="D-", min_value=0, max_value=100)

    f = forms.IntegerField(label="F", min_value=0, max_value=100)

class IdealDistributionForm(forms.Form):
    target_a = forms.IntegerField(label="% A", min_value=0, max_value=100)
    target_b = forms.IntegerField(label="% B", min_value=0, max_value=100)
    target_c = forms.IntegerField(label="% C", min_value=0, max_value=100)
    target_d = forms.IntegerField(label="% D", min_value=0, max_value=100)
    target_f = forms.IntegerField(label="% F", min_value=0, max_value=100)

class AddAssignmentForm(forms.Form):

    def __init__(self, categories, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'] = forms.CharField(label="Title", max_length=100)
        self.fields['assignment_type'] = forms.ChoiceField(choices=categories)
        self.fields['projected_avg'] = forms.FloatField(label="Expected Score (Optional)", required=False, min_value=0, max_value=100)

class DropAssignmentForm(forms.Form):

    def __init__(self, assignment_titles, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['assignment_type'] = forms.ChoiceField(label="Dropped assignment type:", choices=assignment_titles)
        self.fields['lowest_choice'] = forms.ChoiceField(label="Drop lowest", choices=[("avg", "Average score"), ("individual", "Individual scores")])