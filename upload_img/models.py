from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Image(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=225)
    pub_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='images')

    def __str__(self):
        return '%s %s %s' % (self.id, self.title, self.image)
        # return self.title

# this will remove image file from file system when image post is deleted
    def delete(self):
    	self.image.delete()
    	super().delete()

    # see views.py – classbasedview class UploadImageView when not using reverse_lazy
    # from django.urls import reverse

    # def get_absolute_url(self):
    #     return reverse('classbasedview:newsfeed')

class CommentManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset()

    def replies_only(self):
        return super().filter(reply__isnull=False)

    def comments_only(self):
        return super().filter(reply__isnull=True)


class Comment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    image = models.ForeignKey(Image, on_delete=models.CASCADE, default=1)
    text = models.CharField(max_length=225)
    reply = models.ForeignKey('Comment', null=True, on_delete=models.CASCADE, related_name="replies")
    pub_date = models.DateTimeField(auto_now_add=True)

    objects = CommentManager()

    def __str__(self):
        return '%s "%s" %s image' % (self.owner, self.text, self.image.owner)



