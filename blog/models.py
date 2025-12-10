from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField 


class Author(models.Model):
    name = models.CharField(max_length=255)
    avatar = models.ImageField(upload_to='avatars/', blank=False, null=False)
    field = models.CharField(max_length=255)
    description = RichTextField()                    
    slug = models.SlugField(max_length=255, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = RichTextField()                        
    cover_photo = models.ImageField(upload_to='covers/', blank=False, null=False)
    date_published = models.DateField()
    slug = models.SlugField(max_length=255, unique=True)  
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='posts')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Comment(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    text = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return f'Comment by {self.name} on {self.post.title}'

