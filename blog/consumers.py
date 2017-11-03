import json

from channels import Group
from channels.auth import channel_session_user, channel_session_user_from_http
from django.contrib.auth.models import User

from .models import Post


@channel_session_user_from_http
def connect_blog(message):
    if message.user.is_authenticated():
        message.reply_channel.send({"accept": True})
        Group("blog").add(message.reply_channel)
    else:
        message.reply_channel.send({"close": True})


@channel_session_user
def disconnect_blog(message):
    Group("blog").discard(message.reply_channel)


@channel_session_user
def save_post(message):
    text = json.loads(message['text'])['text']
    title = json.loads(message['text'])['title']
    author = json.loads(message['text'])['author']
    method = json.loads(message['text'])['method']
    id = json.loads(message['text'])['id']
    requestSender = str(message.user.username)

    try:
        if method == "POST":
            author = User.objects.get(username=author)
            Post.objects.create(author=author, title=title, text=text)
        if method == "UPDATE":
            postQ = Post.objects.get(id=id)
            if requestSender == str(postQ.author):
                postQ.text = text
                postQ.title = title
                postQ.save()
            else:
                message.reply_channel.send({
                    "text": json.dumps({'error': "you are not auth this is not your post"}),
                })

        if method == "DELETE":
            postQ = Post.objects.get(id=id)
            if requestSender == str(postQ.author):
                postQ.delete()
                Group('blog').send({
                    "text": json.dumps({'deleted': True, 'id': id}),
                })
            else:
                message.reply_channel.send({
                    "text": json.dumps({'error': "you are not auth this is not your post"}),
                })

    except:
        return
