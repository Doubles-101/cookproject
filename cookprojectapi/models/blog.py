from django.db import models
from .customer import Customer

class Blog(models.Model):
    title = models.CharField(max_length=50)
    article = models.CharField(max_length=1200)
    customer = models.ForeignKey(Customer, related_name='blog', on_delete=models.DO_NOTHING,)
    blog_pic = models.ImageField(
        upload_to='blogimages', height_field=None,
        width_field=None, max_length=None, null=True)