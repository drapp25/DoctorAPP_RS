from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from django.utils import timezone


class Perfil(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    es_medico = models.BooleanField(default=False)
    matricula = models.CharField(max_length=50, blank=True, null=True)
    especialidad = models.CharField(max_length=100, blank=True, null=True)
    foto = models.ImageField(upload_to='perfil/', default='perfiles/default_doctor.png')
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.usuario.username


class Publication(models.Model):
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_index=True)
    contenido = models.TextField()
    imagen = models.ImageField(upload_to='publicaciones/', blank=True, null=True)
    video = models.FileField(upload_to='publicaciones/', blank=True, null=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='likes', blank=True)
    dislikes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='dislikes', blank=True)
    creado = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-creado']
        indexes = [
            models.Index(fields=['-creado', 'autor']),
        ]

    def __str__(self):
        return f'{self.autor.username} - {self.creado.strftime("%Y-%m-%d %H:%M")}'
    
    def likes_count(self):
        return self.likes.count()
    
    def dislikes_count(self):
        return self.dislikes.count()
    
    def comentarios_count(self):
        return self.comentarios.count()


class Comentario(models.Model):
    publicacion = models.ForeignKey(Publication, related_name='comentarios', on_delete=models.CASCADE, db_index=True)
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_index=True)
    contenido = models.TextField()
    creado = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['creado']
        indexes = [
            models.Index(fields=['publicacion', 'creado']),
        ]

    def __str__(self):
        return f'Comentario de {self.autor.username}'


class Usuario(AbstractUser):
    es_profesional = models.BooleanField(default=False)
    es_paciente = models.BooleanField(default=False)
    ciudad_residencia = models.CharField(max_length=100, blank=True, null=True)
    matricula = models.CharField(max_length=50, blank=True, null=True)
    especialidad = models.CharField(max_length=100, blank=True, null=True)
    TITULO_CHOICES = [
        ('Dr.', 'Dr.'),
        ('Dra.', 'Dra.'),
    ]
    titulo_profesional = models.CharField(max_length=10, choices=TITULO_CHOICES, blank=True, null=True)
    foto_perfil = models.ImageField(upload_to='perfiles/', null=True, blank=True)
    bio = models.TextField(blank=True, null=True)
    seguidores = models.ManyToManyField('self', symmetrical=False, related_name='siguiendo', blank=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['es_profesional', 'especialidad']),
            models.Index(fields=['matricula']),
        ]
    
    def __str__(self):
        return self.username
    
    def get_full_name_or_username(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username
    
    def seguidores_count(self):
        return self.seguidores.count()
    
    def siguiendo_count(self):
        return self.siguiendo.count()


class DailyChatQuota(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    input_count = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ('user', 'date')

class BloodAnalysis(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    conversation_id = models.CharField(max_length=255)
    file_name = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=20, default='processing') # processing, completed, failed
    result = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Analysis {self.id} for {self.user.username}"


class BloodTestPayment(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pendiente'),
        ('APPROVED', 'Aprobado'),
        ('DECLINED', 'Rechazado'),
        ('Error', 'Error'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reference = models.CharField(max_length=100, unique=True)
    amount_in_cents = models.IntegerField(default=2000000) # 20.000 COP
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    wompi_transaction_id = models.CharField(max_length=100, blank=True, null=True)
    is_consumed = models.BooleanField(default=False) # True solo cuando el analisis es EXITOSO
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.reference} ({self.status})"


class VitaChatMessage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='vita_messages')
    role = models.CharField(max_length=10, choices=[('user', 'User'), ('bot', 'Bot')])
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['timestamp']
        indexes = [
            models.Index(fields=['user', 'timestamp']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.role} - {self.timestamp}"


class UserWidgetPreference(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='widget_preferences')
    
    # VITA State
    vita_active = models.BooleanField(default=False) 
    vita_minimized = models.BooleanField(default=False)
    
    # ROJITO State
    rojito_active = models.BooleanField(default=False)
    rojito_minimized = models.BooleanField(default=False)
    
    # ROJITO Counter
    rojito_lifetime_count = models.IntegerField(default=0)
    
    # ROJITO Daily Limit (Window based)
    rojito_window_start = models.DateTimeField(null=True, blank=True)
    rojito_window_count = models.IntegerField(default=0)
    
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Preferences for {self.user.username}"
