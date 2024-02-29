from django import forms

class ConfigurarPerfil(forms.Form):
  phone_number = forms.CharField(max_length=12)
  telphone_number = forms.CharField(max_length=12)
  age = forms.IntegerField()
  gender = forms.CharField(max_length=2)
  password = forms.CharField(required=False)
  password_confirm = forms.CharField(required=False)
  
  def clean(self):
    cleaned_data = super().clean()
    password = cleaned_data.get('password')
    password_confirm = cleaned_data.get('password_confirm')
    
    if password and password_confirm and password != password_confirm:
        raise forms.ValidationError("Las contraseñas no coinciden")

    return cleaned_data