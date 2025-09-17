from django.db import models


class Sections(models.Model):
  name = models.CharField(max_length=30, unique=True, null=False, verbose_name="Section Name")
  
  class Meta:
      verbose_name = "Section"
      verbose_name_plural = "Sections"
      ordering = ["name"]
      
  def __str__(self):
     return self.name

  @property
  def num_habitats(self):
    return self.habitats.count()
  


