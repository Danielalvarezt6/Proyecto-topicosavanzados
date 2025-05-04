from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['sex', 'age', 'expediente']
        widgets = {
            'sex': forms.Select(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '120'}),
            'expediente': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '20', 'placeholder': 'Ejemplo: 222204975'}),
        }

class CompleteProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['sex', 'age', 'expediente']  # Usa los nombres correctos de los campos

class CustomRegisterForm(forms.Form):
    nombre = forms.CharField(label='Nombre completo', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre completo'}))
    email = forms.EmailField(label='Correo electrónico', widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}))
    sex = forms.ChoiceField(label='Sexo', choices=UserProfile.SEX_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    age = forms.IntegerField(label='Edad', min_value=1, max_value=120, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Edad'}))
    expediente = forms.CharField(label='Número de expediente', max_length=20, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ejemplo: 222204975'}))
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}))
    password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmar contraseña'}))

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            self.add_error('password2', 'Las contraseñas no coinciden.')
        return cleaned_data 
    
    from .models import UserProfile  # Asegúrate de que este sea tu modelo de usuario
 