from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.

class historia(models.Model):
	Naran_eskola=models.CharField(max_length=50)
	Motto =RichTextUploadingField()
	visaun=RichTextUploadingField()
	Missaun=RichTextUploadingField()
	historia_eskola=RichTextUploadingField()
	images=models.ImageField(upload_to='images/', null=True, blank=True )

	def __str__(self):
		template='{0.Naran_eskola}'
		return template.format(self)
