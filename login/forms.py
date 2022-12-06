from django import forms

from .models import CustomerAddress


class CustomerProfileForm(forms.ModelForm):
    class Meta:
      model = CustomerAddress
      fields = ['user','name','phone_number','house_name','street_name','city','state','country','Zip_code']
      widgets = {'user':forms.TextInput(attrs=
      {'class':'form_control'}),'name':forms.TextInput(attrs=
      {'class':'form-control'}),'phone_number':forms.TextInput(attrs=
      {'class':'form_control'}),'house_name':forms.TextInput(attrs=
      {'class':'form_control'}),'street_name':forms.TextInput(attrs=
      {'class':'form_control'}),'city':forms.TextInput(attrs=
      {'class':'form_control'}),'state':forms.TextInput(attrs=
      {'class':'form_control'}),'country':forms.TextInput(attrs=
      {'class':'form_control'}),'Zip_code':forms.NumberInput(attrs=
      {'class':'form_control'})}
 
 