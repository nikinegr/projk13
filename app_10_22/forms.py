from django import forms
from .models import Project, Task, Post, Comment, User, Profile
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm



class Form(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    phone_number = forms.IntegerField()
    adress = forms.CharField()
    photo = forms.FileField()
    date = forms.DateField(widget=forms.SelectDateWidget())


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['text']


class TestForm(forms.Form):
    name = forms.CharField()


class TaskCreateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['text', 'status', 'deadline']
        widgets ={'text': forms.TextInput(attrs={'id': 'text'}),
            "status": forms.CheckboxInput(attrs={'id':'status'}),
            "deadline": forms.DateInput(attrs={'id':'deadline'})}




class SearchForm(forms.Form):
    search_query = forms.CharField(label='Search users', max_length=100)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']


class ProfileForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    bio = forms.CharField(widget=forms.Textarea)
    email = forms.EmailField()
    profile_picture = forms.ImageField()


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

    def init(self, *args, **kwargs):
        super(CommentForm, self).init(*args, **kwargs)


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio']


