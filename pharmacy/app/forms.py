from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import UserProfile,Clanak
from django.contrib.auth import authenticate,get_user_model

User=get_user_model()

class UserLoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput)

    def clean(self,*args,**kwargs):
        username=self.cleaned_data.get("username")
        password=self.cleaned_data.get("password")
        user=authenticate(username=username,password=password)
        if username and password:
            if not user:
                raise forms.ValidationError("Korisnik ne postoji.")
            if not user.check_password(password):
                raise forms.ValidationError("Password nije ispravan")
            if not user.is_active:
                raise forms.ValidationError("Korisnik nije aktivan.")
        return super(UserLoginForm, self).clean(*args,**kwargs)

class ExtendedUserForm(UserCreationForm):

    def __init__(self,*args,**kwargs):
        super(ExtendedUserForm,self).__init__(*args,**kwargs)
        for field in self.fields.values():
            field.widget.attrs={'class':'form-control'}

    username=forms.Field(label="Korisničko ime")
    password1 = forms.CharField(widget=forms.PasswordInput,label="password",help_text="Password ne smije biti sličan ostalim podacima,mora sadržavati najmanje 8 karaktera, ne smije biti često korišten password,ne smije biti skroz numerički.")
    password2 = forms.CharField(widget=forms.PasswordInput,label="potvrda passworda")

    class Meta:
        model=User
        widget={
            'password1':forms.PasswordInput(),
            'password2':forms.PasswordInput()
        }
        fields=('username','first_name','last_name','email','password1','password2')
        labels={
            'username':'Korisničko ime',
            'first_name':'Ime',
            'last_name':'Prezime',
            'email':'Email',
        }

    def save(self,commit=True):
        user=super().save(commit=False)
        user.email=self.cleaned_data['email']
        user.first_name=self.cleaned_data['first_name']
        user.last_name=self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):

    def __init__(self,*args,**kwargs):
        super(ProfileForm,self).__init__(*args,**kwargs)
        for field in self.fields.values():
            field.widget.attrs={'class':'form-control'}

    class Meta:
        model=UserProfile
        fields=('notification',)
        widget={
            'notification':forms.CheckboxInput(attrs={'class':'onoffswitch'},)
        }
        labels={
            'notification':'Želim obavještenja o sniženju!'
        }

class ClanakForma(forms.ModelForm):
    class Meta:
        model=Clanak
        fields=('naslov','body','slug',)
        labels={'naslov':'Naslov',
                'body':'Tekst',
                'slug':'Sifra (po vasoj zelji)'
                }