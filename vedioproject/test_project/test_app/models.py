from django.db import models

# Create your models here.
class VedioGallery(models.Model):
	vedio_id=	models.AutoField(primary_key=True)
	vedio_material=models.FileField(upload_to = "vedio/vedio_files/",blank=True,null=True)