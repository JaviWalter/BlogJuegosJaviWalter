from django import forms
from .models import ComentarioJuego

class ComentarioForm(forms.ModelForm):
    
    class Meta:
        model = ComentarioJuego
        fields = ['texto']
        widgets = {
            'texto' : forms.Textarea(attrs={
                'rows' : 4,
                'placeholder' : 'Escribe tu comentario aquí...',
            })
        }