from django.db import models

# Create your models here.
class Option(models.Model):
    objects = models.Manager()
    fes_name = models.CharField(default="", max_length = 100)
    fes_start_year = models.IntegerField(default = 0)
    fes_start_month = models.IntegerField(default = 0)
    fes_start_day = models.IntegerField(default = 0)
    fes_end_year = models.IntegerField(default = 0)
    fes_end_month = models.IntegerField(default = 0)
    fes_end_day = models.IntegerField(default = 0)


class Results(models.Model):
    objects = models.Manager()
    total_visitor = models.FloatField(default=0.0)
    평균기온 = models.FloatField(default = 0.0) 
    최저기온 = models.FloatField(default = 0.0) 
    최고기온 = models.FloatField(default = 0.0)
