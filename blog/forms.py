from django import forms
from .models import Comment, Post, Image, User
from django.core.exceptions import ValidationError
from django.forms.widgets import DateInput

class SignupForm(forms.ModelForm):
    password = forms.CharField(max_length=250, widget=forms.PasswordInput, label='password')
    password2 = forms.CharField(max_length=250, widget=forms.PasswordInput, label='repeat password')
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'birth_date', 'job', 'bio', 'profile_img']
        widgets = {
            'profile_img': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("passwords are not same.")
        return cd['password2']
    
    def clean_email(self):
        cd = self.cleaned_data
        email = cd['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError('Email already used')
    
    birth_date = forms.DateField(widget=DateInput(attrs={'type': 'date'}))

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description', 'active','tags']

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('img_file', 'description')
        widgets = {
            'img_file': forms.FileInput(attrs={'accept': 'image/*', 'class': 'form-control'})
        }

ImageFormSet = forms.inlineformset_factory(
    Post, Image, form=ImageForm, fields=('img_file', 'description'), extra=1, can_delete=True
)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['email', 'text']  

    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your email'}))
    text = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'placeholder': 'Your message'}))

class SearchForm(forms.Form):
    query = forms.CharField()

class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description', 'tags']

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'birth_date', 'job', 'bio', 'profile_img']
        widgets = {
            'birth_date': DateInput(attrs={'type': 'date'}),
            'profile_img': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError('Email already used')
        return email
