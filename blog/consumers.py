import json

from channels import Group
from django.contrib.auth.models import User

from .models import Post


def connect_blog(message):
    message.reply_channel.send({"accept": True})
    print "connected"
    Group("blog").add(message.reply_channel)


def disconnect_blog(message):
    print "disconnected"
    Group("blog").discard(message.reply_channel)


def save_post(message):
    text = json.loads(message['text'])['text']
    title = json.loads(message['text'])['title']
    author = json.loads(message['text'])['author']
    method = json.loads(message['text'])['method']
    id = json.loads(message['text'])['id']

    if method == "POST":
        try:
            author = User.objects.get(username=author)
        except:
            return
        Post.objects.create(author=author, title=title, text=text)

    if method == "UPDATE":
        print "update1"
        try:
            author = User.objects.get(username=author)
            postQ = Post.objects.get(id=id)
        except:
            print "error"
            return
        postQ.text = text
        postQ.title = title

        postQ.save()
    if method == "DELETE":
        try:
            postQ = Post.objects.get(id=id)
        except:
            return

        postQ.delete()
