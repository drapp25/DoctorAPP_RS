from django import forms
from .models import Perfil, Usuario
from django.contrib.auth.models import User

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['bio', 'foto', 'matricula', 'especialidad']

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['ciudad_residencia', 'especialidad', 'foto_perfil']

class UserUpdateForm(forms.ModelForm):
    # Campos extra no vinculados directamente al modelo pero manejados en la vista
    eliminar_foto = forms.BooleanField(required=False, label="Eliminar foto actual")
    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'titulo_profesional', 'ciudad_residencia', 'especialidad', 'bio', 'foto_perfil']
        labels = {
            'first_name': 'Nombres',
            'last_name': 'Apellidos',
            'titulo_profesional': 'Título (Dr./Dra.)',
            'ciudad_residencia': 'Ciudad',
            'especialidad': 'Especialidad (Solo Médicos)',
            'bio': 'Biografía',
            'foto_perfil': 'Actualizar Foto'
        }
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'foto_perfil': forms.FileInput(), # Use simple input to avoid 'Currently...' text
        }

 
    
    # Redefining fields to add detailed widget attrs
    current_password = forms.CharField(
        required=False, 
        widget=forms.PasswordInput(attrs={'autocomplete': 'off', 'placeholder': 'Tu contraseña actual'}), 
        label="Contraseña Actual (para cambios)"
    )
    new_password = forms.CharField(
        required=False, 
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'placeholder': 'Nueva contraseña'}), 
        label="Nueva Contraseña"
    )
    confirm_password = forms.CharField(
        required=False, 
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'placeholder': 'Repite la nueva contraseña'}), 
        label="Confirmar Nueva Contraseña"
    )

    def clean(self):
        cleaned_data = super().clean()
        current_password = cleaned_data.get('current_password')
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        # Validación básica de contraseñas
        if new_password:
            if not current_password:
                self.add_error('current_password', 'Debes ingresar tu contraseña actual para establecer una nueva.')
            elif not self.instance.check_password(current_password):
                 self.add_error('current_password', 'La contraseña actual es incorrecta.')
            elif new_password != confirm_password:
                self.add_error('confirm_password', 'Las contraseñas nuevas no coinciden.')
            else:
                # Validar complejidad de contraseña (Mismos parámetros que registro)
                import re
                if len(new_password) < 8 or not re.search(r'\d', new_password) or not re.search(r'[A-Z]', new_password):
                     self.add_error('new_password', 'La contraseña debe tener al menos 8 caracteres, una mayúscula y un número.')
        
        return cleaned_data
