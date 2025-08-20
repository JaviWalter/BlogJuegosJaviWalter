from django import forms
from .models import ComentarioJuego

class ComentarioJuegoForm(forms.ModelForm):
    
    class Meta:
        model = ComentarioJuego
        fields = ['texto']
        widgets = {
            'texto' : forms.Textarea(attrs={
                'rows' : 4,
                'placeholder' : 'Escribe tu comentario aquí...',
            })
        }

    def clean_texto(self):
        texto = self.cleaned_data.get('texto')
        if len(texto) < 10:
            raise forms.ValidationError("El comentario debe tener al menos 10 caracteres.")
        return texto