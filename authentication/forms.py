from django import forms


css_classes = "bg-gray-800 rounded-lg p-2 w-full"


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': css_classes,
            'placeholder': 'Nom d\'utilisateur',
        }),
        label='Nom d\'utilisateur'
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': css_classes, 
            'placeholder': 'Mot de passe'
        }),
        label='Mot de passe'
    )
