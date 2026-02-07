import os
import django
import sys

# Add the project root to sys.path
sys.path.append(os.getcwd())

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "redsocialmed.settings")
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

username = 'doctorappsu'
email = 'doctor.app.2023@gmail.com'
password = 'doctorapp123' 

try:
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username, email, password)
        print(f"Superusuario '{username}' creado exitosamente.")
        print(f"Correo: {email}")
        print(f"Contraseña tempora: {password}")
    else:
        print(f"El superusuario '{username}' ya existe.")
except Exception as e:
    print(f"Error: {e}")
