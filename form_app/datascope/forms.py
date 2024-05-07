from django import forms
from .models import CustomUser
from .models import Questionnaire, CourseInformation


class RegisterForm(forms.ModelForm):
    email = forms.EmailField(label="Email", max_length=254)
    college_name = forms.CharField(label="College Name", max_length=100)
    university_name = forms.CharField(label="University Name", max_length=100)
    college_type = forms.CharField(label="College Type", max_length=100)
    name_nodal_officer = forms.CharField(label="Name of Nodal Officer", max_length=50)
    mobile_nodal_officer = forms.IntegerField(label="Mobile of Nodal Officer")

    class Meta:
        model = CustomUser
        fields = ("email", "college_type", "college_name",
                  "university_name","name_nodal_officer","mobile_nodal_officer")


class QuestionnaireForm(forms.ModelForm):
    class Meta:
        model = Questionnaire
        fields = '__all__'

class CoursesInformationForm(forms.ModelForm):
    class Meta:
        model = CourseInformation
        fields = '__all__'