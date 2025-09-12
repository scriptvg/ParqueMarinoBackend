from django.db import models
from django.contrib.auth.models import User, Group

# Modelo del perfil del usuario
class UserProfile(models.Model):
  user =  models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
  phone = models.CharField(max_length=20, blank=True, null=True)
  address = models.CharField(max_length=200, blank=True, null=True)
  birth_date = models.DateField(null=True, blank=True)
  profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
  
  class Meta:
    db_table = 'user_profile'
    verbose_name = 'Perfil de usuario'
    verbose_name_plural = 'Perfiles de usuarios'
  
  def __str__(self):
    return f'Perfil de {self.user.username}'
  
  
