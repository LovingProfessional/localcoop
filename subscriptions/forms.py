from django import forms
from django.forms import fields, ValidationError
from subscriptions.models import CoopUser
from django.contrib.auth.models import User
#from django.contrib.auth.models import User

class CoopUserForm(forms.ModelForm):
    class Meta:
        model = CoopUser
        fields = ['firstname','lastname','phone','wesid','email']
        help_texts = { 'phone':"Example: '8605567802'",
                       'email':"Please enter a valid @wesleyan.edu account"}
    password = fields.CharField(max_length=20,min_length=8)
    confirmpassword = fields.CharField(max_length=20,min_length=8,label="Confirm Password")

    def clean(self): #Override form clean method
        print("cleaned data: " + str(self.cleaned_data))
        data = self.cleaned_data
        if not data['password'] == data['confirmpassword']:
            #self.errors['password'] = 'Passwords must match'
            print("They don't match")
            raise ValidationError('Passwords must match')
        print("errors: " + str(self.errors))
        return self.cleaned_data

class LogInForm(forms.Form):
    username = fields.CharField()
    password = fields.CharField()

    def clean(self):
        try:
            thisUser = User.objects.get(username=self.cleaned_data['username'])
        except:
            raise ValidationError("No such username, it should be your Wesleyan account name without the '@wesleyan.edu'")
        if not thisUser.check_password(password):
            raise ValidationError("Incorrect Password")
        return self.cleaned_data
        
