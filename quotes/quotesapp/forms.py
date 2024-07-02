from django.forms import ModelForm, CharField, TextInput, EmailField
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Tag, Author, Quote

class TagForm(ModelForm):
    name = CharField(min_length=3, max_length=25, required=True, widget=TextInput)

    class Meta:
        model = Tag
        fields = ['name']


class UserRegisterForm(UserCreationForm):
    email = EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class AuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'biography']

class QuoteForm(ModelForm):
    class Meta:
        model = Quote
        fields = ['text', 'author', 'tags']

