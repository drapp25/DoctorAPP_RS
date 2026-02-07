# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Perfil, Publication, Comentario

# Configuración personalizada para el modelo Usuario
class CustomUserAdmin(UserAdmin):
    model = Usuario
    # Lista de campos a mostrar en la lista de usuarios
    list_display = ('username', 'email', 'first_name', 'last_name', 'es_profesional', 'especialidad')
    list_filter = ('es_profesional', 'es_paciente', 'is_staff', 'is_active')
    
    fieldsets = UserAdmin.fieldsets + (
        ('Información Profesional', {'fields': ('es_profesional', 'es_paciente', 'especialidad', 'matricula', 'titulo_profesional', 'ciudad_residencia', 'foto_perfil', 'bio')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información Profesional', {'fields': ('es_profesional', 'es_paciente', 'especialidad', 'matricula', 'titulo_profesional', 'ciudad_residencia', 'foto_perfil')}),
    )

admin.site.register(Usuario, CustomUserAdmin)
admin.site.register(Perfil)
admin.site.register(Publication)
admin.site.register(Comentario)
