from django.db import models

# Create your models here.
class Option(models.Model):
    objects = models.Manager()
    fes_name = models.TextField(default = '')
    fes_start_year = models.IntegerField(default = 0)
    fes_start_month = models.IntegerField(default = 0)
    fes_start_day = models.IntegerField(default = 0)
    fes_end_year = models.IntegerField(default = 0)
    fes_end_month = models.IntegerField(default = 0)
    fes_end_day = models.IntegerField(default = 0)

