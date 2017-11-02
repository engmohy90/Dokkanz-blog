from __future__ import unicode_literals

import json

from channels import Group
from django.db import models
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
        default=timezone.now)
    published_date = models.DateTimeField(
        blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def send_notification(self):
        notification = {
            "id": self.id,
            "author": self.author.username,
            "title": self.title,
            "text": self.text,
            "created_date": self.created_date.strftime("%a %d %b %Y %H:%M"),
        }
        print("======notification====")
        print(notification)
        Group('blog').send({

            "text": json.dumps(notification),
        })

    def save(self, *args, **kwargs):
        print "updat from model how xxcom"
        result = super(Post, self).save(*args, **kwargs)
        self.send_notification()
        return result

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey('blog.Post', related_name='comments')
    author = models.ForeignKey('auth.User')
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text
