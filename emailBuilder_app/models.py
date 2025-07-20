from django.db import models
from django.utils.text import slugify

class Folder(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class File(models.Model):
    id = models.AutoField(primary_key=True)
    folder = models.ForeignKey(Folder, related_name='files', on_delete=models.CASCADE, null=True, blank=True)  # Allow null & blank
    name = models.CharField(max_length=255)
    content = models.TextField()
    json_content = models.TextField(default='-')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class SavedRows(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    image = models.BinaryField()
    json = models.TextField(default='-')
    html = models.TextField()

    def __str__(self):
        return self.name